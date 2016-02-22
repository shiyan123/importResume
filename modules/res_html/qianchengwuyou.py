# coding=utf-8
import sys
import time

import requests
from pyquery import PyQuery as pq
import response
import json
from flask import request, Response
reload(sys)
sys.setdefaultencoding("utf-8")
s = requests.session()


def resume_51job(db, name, password, customerId, accessToken, flag):
    url = 'http://my.51job.com:80/my/passport_login.php'
    raw_form = {
        'from_domain': 'www.51job.com',
        'passport_password': password,
        'passport_loginName': name}
    response = s.post(url, data=raw_form)
    newurl = 'http://my.51job.com/my/My_Pmc.php'
    newresponse = s.get(newurl)
    d = pq(newresponse.content)
    a = d('div').filter('.main').children('ul').children('li').eq(5).html().strip()
    resumeUrl = str(a).split('"')[1]
    resumeResponse = s.get(resumeUrl)
    d1 = pq(resumeResponse.content)
    a1 = d1('tr').filter('.resumeName ').children('td').eq(1).html().strip()
    lastActivityTime = d1('tr').filter('.resumeName ').children('td').eq(4).html().strip()
    resumeUrl1 = str(a1).split('"')[1]
    resumeResponse1 = s.get(resumeUrl1)
    html = pq(resumeResponse1.content)

    def resLastActivityTime(lastActivityTimeStr):
        try:
            a = lastActivityTimeStr + "T00:00:00.000+08:00"
            return a
        except Exception as e:
            return ""

    def resName_51job():
        try:
            a = html('div').filter('.inptext_fl').eq(0).text()
            return a
        except Exception as e:
            return ""

    def resGender_51job():
        try:
            a = html('div').filter('.inptext_fl').eq(2).text()
            return a
        except Exception as e:
            return ""

    def resBirthday_51job():
        try:
            a = html('div').filter('.inptext_fl').eq(3).text()
            return a
        except Exception as e:
            return ""

    def resOriginalId_51job():
        try:
            a = html('#Resume_form').children('input').eq(0).attr('value')
            return a
        except Exception as e:
            return ""

    def resCity_51job():
        try:
            a = html('dl').filter(lambda i: "居住地：" in pq(this).text()).children('dd').children('div').text()
            return a
        except Exception as e:
            return ""

    def resPhoneNumber_51job():
        try:
            a = html('dl').filter(lambda i: "手机号码：" in pq(this).text()).children('dd').children('div').text()[0:11]
            return a
        except Exception as e:
            return ""

    def resEmail_51job():
        try:
            a = html('dl').filter(lambda i: "Email：" in pq(this).text()).children('dd').children('div').text()
            return a
        except Exception as e:
            return ""

    def resWorkLife_51job():
        try:
            a = html('dl').filter(lambda i: "工作年限：" in pq(this).text()).children('dd').children('div').text().replace(
                "", "")
            if u"年" in a:
                a1 = int(a[0:1])
            elif u"以上" in a:
                a1 = int(a[0:2])
            else:
                a1 = 0
            return a1
        except Exception as e:
            return 0

    def resInterest_51job():
        try:
            a = html('dl').filter(lambda i: "兴趣爱好" in pq(this).text()).next().text()[4:]
            return a
        except Exception as e:
            return ""

    def resPersonalStatement_51job():
        try:
            a = html('dl').filter(lambda i: "自我评价：" in pq(this).text()).children().text()[6:]
            return a
        except Exception as e:
            return ""

    def resExpectCity_51job():
        try:
            a = html('dl').filter(lambda i: "地点：" in pq(this).text()).children().text()[4:]
            return a
        except Exception as e:
            return ""

    def resEducationStartTime(timeStr):
        try:
            a = timeStr.split("-")[0].replace("/", "-").split("-")[1]
            b = timeStr.split("-")[0].replace("/", "-")
            if int(a) > 10:
                c = b + "-01T00:00:00.000+08:00"
                return c
            else:
                d = timeStr.split("-")[0].replace("/", "-").split("-")[0] + "-0" + str(a) + "-01T00:00:00.000+08:00"
                return d
        except Exception as e:
            return ""

    def resEducationEndTime(timeStr):
        try:
            a = timeStr.split("-")[1]
            if u"至今" in a:
                now = int(time.time())
                timeArray = time.localtime(now)
                timeNow = time.strftime("%Y-%m-%dT%H:%M:%S+08:00", timeArray)
                return timeNow
            else:
                b = timeStr.split("-")[1].replace("/", "-").split("-")[1]
                c = timeStr.split("-")[1].replace("/", "-")
                if int(b) > 10:
                    d = c + "-01T00:00:00.000+08:00"
                    return d
                else:
                    e = timeStr.split("-")[1].replace("/", "-").split("-")[0] + "-0" + str(b) + "-01T00:00:00.000+08:00"
                    return e
        except Exception as e:
            return ""

    res = {
        'source': '51job',
        'originalId': resOriginalId_51job(),
        'avatar': '',
        'fullName': resName_51job(),
        'gender': resGender_51job(),
        'birthday': resBirthday_51job(),
        'descriptions': {
            'city': resCity_51job(),
            'interest': resInterest_51job(),
            'personalStatement': resPersonalStatement_51job(),
            'expectCity': resExpectCity_51job(),
            'workLife': resWorkLife_51job(),
            'contactPhoneNumber': resPhoneNumber_51job(),
            'contactEmail': resEmail_51job()
        },
        'skills': [],
        'languages': [],
        'certifications': [],
        'educations': [],
        'socialExperiences': [],
        'workExperiences': [],
        'lastActivityTime': resLastActivityTime(lastActivityTime)
    }
    # 51job skills
    try:
        skill = {}
        skills = html('p').filter('.studyTxet_more').filter(lambda i: "技能：" in pq(this).text()).text().split("技能：")
        for i in skills:
            if i == "":
                continue
            skill["name"] = i.split("使用时间：")[0]
            skill["proficiency"] = i.split("使用时间：")[1].strip()[-2:]
            res["skills"] += [skill]
            skill = {}
            continue
    except Exception as e:
        res["skills"] = []
    # 51job languages
    try:
        language = {}
        languages = html('dl').filter(lambda i: "语言类别：" in pq(this).text()).text().split("语言类别：")
        for i in languages:
            if i == "":
                continue
            language["name"] = i.split("掌握程度：")[0].strip()
            language["proficiency"] = i.split("掌握程度：")[1].strip()
            res["languages"] += [language]
            language = {}
            continue
    except Exception as e:
        res["languages"] = []
    # 51job certifications
    try:
        certification = {}
        cnt_51job = 0
        while cnt_51job < 10:
            if cnt_51job % 2 != 0:
                a = html('div').filter(lambda i: "成绩：" in pq(this).text()).children('p').children('span').eq(
                    cnt_51job).text()
                if a == None:
                    break
                else:
                    certification["name"] = html('div').filter(lambda i: "成绩：" in pq(this).text()).children(
                        'p').children('span').eq(cnt_51job).text()
                    res["certifications"] += [certification]
                    certification = {}
                    cnt_51job += 1
                    continue
            else:
                cnt_51job += 1
                continue
    except Exception as e:
        res["certifications"] = []
    # 51job educations
    try:
        education = {}
        cnt1_51job = 0
        while cnt1_51job < 5:
            educationTime = html('div').filter('#EDU').children('div').children('div').children('div').filter(
                '.studyTxet_title').eq(cnt1_51job).children('span').eq(0).text()
            if educationTime == None:
                break
            education["startTime"] = resEducationStartTime(educationTime)
            education["endTime"] = resEducationEndTime(educationTime)
            education["school"] = html('div').filter('#EDU').children('div').children('div').children('div').filter(
                '.studyTxet_title').eq(cnt1_51job).children('span').eq(1).text()
            education["major"] = html('div').filter('#EDU').children('div').children('div').children('div').filter(
                '.studyTxet_title').eq(cnt1_51job).children('span').eq(2).text()
            education["degree"] = html('div').filter('#EDU').children('div').children('div').children('div').filter(
                '.studyTxet_title').eq(cnt1_51job).children('span').eq(3).text()
            res["educations"] += [education]
            education = {}
            cnt1_51job += 1
            continue
    except Exception as e:
        res["educations"] = []
    # 51job 	workExperiences
    try:
        workExperience = {}
        cnt2_51job = 0
        while cnt2_51job < 5:
            workExperienceTime = html('div').filter('#WORK').children('div').children('div').children('div').filter(
                '.studyTxet_title').eq(cnt2_51job).children('span').eq(0).text()
            if workExperienceTime == None:
                break
            workExperience["startTime"] = resEducationStartTime(workExperienceTime)
            workExperience["endTime"] = resEducationEndTime(workExperienceTime)
            workExperience["organization"] = html('div').filter('#WORK').children('div').children('div').children(
                'div').filter('.studyTxet_title').eq(cnt2_51job).children('span').eq(1).children('b').text()
            workExperience["position"] = html('div').filter('#WORK').children('div').filter('.studyUnit').eq(
                cnt2_51job).children('div').filter('.studyText').children('dl').filter(
                lambda i: "职位名称：" in pq(this).text()).children('dd').text()
            workExperience["department"] = html('div').filter('#WORK').children('div').filter('.studyUnit').eq(
                cnt2_51job).children('div').filter('.studyText').children('dl').filter(
                lambda i: "部门：" in pq(this).text()).children('dd').text()
            workExperience["duties"] = html('div').filter('#WORK').children('div').filter('.studyUnit').eq(
                cnt2_51job).children('div').filter('.studyText').children('dl').filter(
                lambda i: "工作描述：" in pq(this).text()).children('dd').text()
            workExperience["workType"] = html('div').filter('#WORK').children('div').filter('.studyUnit').eq(
                cnt2_51job).children('div').filter('.studyText').children('dl').filter(
                lambda i: "工作类型：" in pq(this).text()).children('dd').text()
            res["workExperiences"] += [workExperience]
            workExperience = {}
            cnt2_51job += 1
            continue
    except Exception as e:
        res["workExperiences"] = []

    if flag == "preview":
        old = db.customerProfiles.find_one({"source": "51job", "originalId": str(res["originalId"])})
        if old:
            db.customerProfiles.update({"_id": old["_id"]}, res)
            return new_response({"customerId": str(old["_id"])})
        else:
            return new_response({"customerId": str(db.customerProfiles.insert(res))})
    else:
        customerData = patch_api_customer(res, accessToken, customerId)
        return customerData

def patch_api_customer(res, accessToken, customerId):
    url = "http://api.beta.dev.careerdream.org/core/v1/customerProfiles/" + customerId
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken}
    print(json.dumps(res, ensure_ascii=False))
    response = s.patch(url, data=json.dumps(res), headers=headers)
    return str(response.text)


def new_response(data):
    data = json.dumps({
        'code': 200,
        'message': "ok",
        'data': data
    })
    return Response(
            response=data,
            status=200,
            mimetype="application/json")


def new_response_error():
    data = {}
    data = json.dumps({
        'code': 404,
        'message': "not found",
        'data': data
    })
    return Response(
            response=data,
            status=200,
            mimetype="application/json")