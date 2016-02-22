# coding=utf-8
from pyquery import PyQuery as pq
import time
import sys
import requests
import json
from flask import request, Response
reload(sys)
sys.setdefaultencoding("utf-8")
s = requests.session()


def resume_zhilian(db, name, password, customerId, accessToken, flag):
    url = 'https://passport.zhaopin.com/account/login'
    raw_form = {
        'int_count': '999',
        'errUrl': 'https://passport.zhaopin.com/account/login',
        'RememberMe': 'true',
        'requestFrom': 'portal',
        'loginname': name,
        'Password': password}
    response = s.post(url, data=raw_form)
    newUrl = 'http://i.zhaopin.com/'
    newResponse = s.get(newUrl)
    d = pq(newResponse.content)
    try:
        a = d('div').filter('.myLink').html().strip().split('<a')[3]
    except Exception as e:
        return new_response_error()
    url1 = str(a).split('"')[3]
    url2 = url1.replace("amp;", "")
    newResponse1 = s.get(url2)
    d1 = pq(newResponse1.text)

    def resFullName_zhilian():
        try:
            a = d1('div').filter('.rightRow1').children('h3').text()
            return a
        except Exception as e:
            return ""

    def resOriginalId_zhilian():
        try:
            a = d1('div').filter('.leftRowCon').eq(0).children('ul').children('li').eq(1).html().split("Resume_ID=")[1][
                0:9]
            return a
        except Exception as e:
            return ""

    def resEducationsEndTime_zhilian(timeStr):
        try:
            if u"至今" in timeStr:
                now = int(time.time())
                timeArray = time.localtime(now)
                timeNow = time.strftime("%Y-%m-%dT%H:%M:%S+08:00", timeArray)
                return timeNow
            else:
                a = timeStr.replace("/", "-") + "-01T00:00:00.000+08:00"
                return a
        except Exception as e:
            return ""

    def resEducationsStartTime_zhilian(timeStr):
        try:
            a = timeStr.replace("/", "-") + "-01T00:00:00.000+08:00"
            return a
        except Exception as e:
            return ""

    def resInterest_zhilian():
        try:
            a = d1('h3').filter(lambda i: "兴趣爱好" in pq(this).text()).next().text()
            return a
        except Exception as e:
            return ""

    def resPersonalStatement_zhilian():
        try:
            a = d1('div').filter('.resume_p').text()
            return a
        except Exception as e:
            return ""

    def resExpectCity_zhilian():
        try:
            a = d1('td').filter(lambda i: "期望工作地区：" in pq(this).text()).next().text()
            return a
        except Exception as e:
            return ""

    def resEmail_zhilian():
        try:
            a = d1('div').filter('.rightRow1').children('p').eq(1).text().split("|")[5].split(" ")[4]
            return a
        except Exception as e:
            return ""

    def resPhoneNumber_zhilian():
        try:
            a = d1('div').filter('.rightRow1').children('p').eq(1).text().split("|")[5].split(" ")[2]
            return a
        except Exception as e:
            return ""

    def resWorkLife_zhilian():
        try:
            a = d1('div').filter('.rightRow1').children('p').eq(1).text().split("|")[4].split(" ")[2][0:2].replace("年",
                                                                                                                   "")
            return int(a)
        except Exception as e:
            return 0

    def resBirthday_zhilian():
        try:
            a = d1('div').filter('.rightRow1').children('p').eq(1).text().split("|")[2].strip()[0:7].replace("年",
                                                                                                             "-").replace(
                "月", "")
            return a
        except Exception as e:
            return ""

    def resCity_zhilian():
        try:
            a = d1('div').filter('.rightRow1').children('p').eq(1).text().split("|")[4].split(" ")[1][4:]
            return a
        except Exception as e:
            return ""

    def resLastActivityTime_zhilian():
        try:
            now = int(time.time())
            timeArray = time.localtime(now)
            timeNow = time.strftime("%Y-%m-%dT%H:%M:%S+08:00", timeArray)
            return timeNow
        except Exception as e:
            return ""

    def resGender_zhilian():
        try:
            a = d1('div').filter('.rightRow1').children('p').eq(1).text()[0:1]
            return a
        except Exception, e:
            return ""

    res = {
        "source": 'zhilian',
        "originalId": resOriginalId_zhilian(),
        "avatar": '',
        "fullName": resFullName_zhilian(),
        "gender": resGender_zhilian(),
        "birthday": resBirthday_zhilian(),
        "descriptions": {
            "city": resCity_zhilian(),
            "interest": resInterest_zhilian(),
            "personalStatement": resPersonalStatement_zhilian(),
            "expectCity": resExpectCity_zhilian(),
            "workLife": resWorkLife_zhilian(),
            "contactPhoneNumber": resPhoneNumber_zhilian(),
            "contactEmail": resEmail_zhilian(),
        },
        "skills": [],
        "languages": [],
        "certifications": [],
        "educations": [],
        "socialExperiences": [],
        "workExperiences": [],
        "lastActivityTime": resLastActivityTime_zhilian()
    }
    # zhilian skills
    try:
        skill = {}
        skills = d1('h3').filter(lambda i: "专业技能" in pq(this).text()).next().text().split(" | ")
        cnt_zhilian = 0
        for i in skills:
            if cnt_zhilian % 2 == 0:
                if u"月" in i:
                    try:
                        skill["name"] = i.split(" ")[1]
                    except Exception as e:
                        break
                else:
                    skill["name"] = i
                cnt_zhilian += 1
                continue
            else:
                skill["proficiency"] = i
                cnt_zhilian += 1
            res["skills"] += [skill]
            skill = {}
            continue
    except Exception as e:
        res["skills"] = []
    # zhilian languages
    try:
        language = {}
        languages = d1('h3').filter(lambda i: "语言能力" in pq(this).text()).next().text().split(" ")
        cnt1_zhilian = 0
        for i in languages:
            if cnt1_zhilian % 3 == 0:
                language["name"] = i.split("：")[0]
                language["proficiency"] = i.split("：")[1].split("力")[1]
                res["languages"] += [language]
                language = {}
                cnt1_zhilian += 1
                continue
            else:
                cnt1_zhilian += 1
                continue
    except Exception as e:
        res["languages"] = []
    # zhilian educations
    try:
        education = {}
        educations = d1('h3').filter(lambda i: "教育背景" in pq(this).text()).next().text().split("招")
        for i in educations:
            if i == "":
                break
            education["startTime"] = resEducationsStartTime_zhilian(
                i.split(" | ")[0].split("：")[0].split(" -- ")[0].strip())
            education["endTime"] = resEducationsEndTime_zhilian(
                i.split(" | ")[0].split("：")[0].split(" -- ")[1].strip())
            education["school"] = i.split(" | ")[0].split("：")[1]
            education["major"] = i.split(" | ")[1].strip()
            education["degree"] = i.split(" | ")[2].strip()
            res["educations"] += [education]
            education = {}
            continue
    except Exception as e:
        res["educations"] = []
    try:
        certification = {}
        certifications = d1('h3').filter(lambda i: "证书" in pq(this).text()).next().text().split(" ")
        cnt2_zhilian = 0
        for i in certifications:
            if cnt2_zhilian % 2 != 0:
                certification["name"] = i
                res["certifications"] += [certification]
                certification = {}
                cnt2_zhilian += 1
                continue
            else:
                cnt2_zhilian += 1
                continue
    except Exception as e:
        res["certifications"] = []
    try:
        workExperience = {}
        workExperiences = d1('div').filter('#itemWorkexpe').children('table').text().split(" ")
        cnt3_zhilian = 0
        for i in workExperiences:
            if "--" in i:
                a = cnt3_zhilian - 1
                b = cnt3_zhilian + 1
                c = cnt3_zhilian + 2
                d = cnt3_zhilian + 4
                e = cnt3_zhilian + 12
                f = cnt3_zhilian + 8
                workExperience["startTime"] = resEducationsStartTime_zhilian(workExperiences[a])
                workExperience["endTime"] = resEducationsEndTime_zhilian(workExperiences[b].replace("：", ""))
                workExperience["organization"] = workExperiences[c]
                workExperience["position"] = workExperiences[d]
                if workExperiences[f] != "|":
                    workExperience["duties"] = workExperiences[f]
                else:
                    workExperience["duties"] = workExperiences[e]
                res["workExperiences"] += [workExperience]
                workExperience = {}
                a = 0
                b = 0
                cnt3_zhilian += 1
                continue
            cnt3_zhilian += 1
    except Exception as e:
        res["workExperiences"] = []

    if flag == "preview":
        old = db.customerProfiles.find_one({"source": "zhilian", "originalId": str(res["originalId"])})
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