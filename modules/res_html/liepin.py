# coding=utf-8
import hashlib
import time

from pyquery import PyQuery as pq
import requests
import json
from flask import request, Response

s = requests.session()


def resume_liepin(db, name, password, customerId, accessToken, tpyeFlag):
    url = 'http://www.liepin.com/webUser/login4c.json'
    m = hashlib.md5()
    pwd = m.update(password)
    newPassword = m.hexdigest()
    raw_form = {
        'user_login': name,
        'user_pwd': newPassword,
        'chk_remember_pwd': 'on'}
    headers = {
        'X-Requested-With': 'XMLHttpRequest'}
    response = s.post(url, data=raw_form, headers=headers)
    url1 = 'http://c.liepin.com/?time=1452681632664'
    response1 = s.get(url1)
    d1 = pq(response1.text)
    try:
        url2 = d1('td').filter('.text-right').html().split('"')[1]
    except Exception as e:
        return new_response_error()
    response2 = s.get('http://c.liepin.com' + url2)
    d2 = pq(response2.text)

    def resEducationStartTime_liepin(timeStr):
        try:
            a = str(timeStr).strip().replace(".", "-") + "-01T00:00:00.000+08:00"
            return a
        except Exception as e:
            return ""

    def resEducationEndTime_liepin(timeStr):
        try:
            if "至今" in timeStr:
                now = int(time.time())
                timeArray = time.localtime(now)
                timeNow = time.strftime("%Y-%m-%dT%H:%M:%S+08:00", timeArray)
                return timeNow
            else:
                a = str(timeStr).strip().replace(".", "-") + "-01T00:00:00.000+08:00"
                return a
        except Exception as e:
            return ""

    def resWorkLife_liepin():
        try:
            a = d2('li').filter(lambda i: "工作年限：" in pq(this).text()).children('p').text()[0:2].replace("年", "")
            return int(a)
        except Exception as e:
            return ""

    def resCity_liepin():
        try:
            a = d2('li').filter(lambda i: "所在地点：" in pq(this).text()).children('p').text()
            return a
        except Exception as e:
            return ""

    def resPersonalStatement_liepin():
        try:
            a = d2('div').filter(lambda i: "自我评价" in pq(this).text()).children('p').text()
            return a
        except Exception as e:
            return ""

    def resExpectCity_liepin():
        try:
            a = d2('span').filter(lambda i: "期望地点：" in pq(this).text()).next().text()
            return a
        except Exception as e:
            return ""

    def resEmail_liepin():
        try:
            a = d2('span').filter(lambda i: "邮　　箱：" in pq(this).text()).next().text()
            return a
        except Exception as e:
            return ""

    def resPhoneNumber_liepin():
        try:
            a = d2('span').filter(lambda i: "手　　机：" in pq(this).text()).next().text()
            return a
        except Exception as e:
            return ""

    def resOriginalId_liepin():
        try:
            a = d1('td').filter('.text-right').html().split('"')[1].split("res_id_encode=")[1]
            return a
        except Exception as e:
            return ""

    def resFullName_liepin():
        try:
            a = d2('div').filter('.card-main').children('h3').text().split(" ")[0]
            return a
        except Exception as e:
            return ""

    def resGender_liepin():
        try:
            a = d2('div').filter('.card-main').children('h3').text().split(" ")[1]
            return a
        except Exception as e:
            return ""

    def resLastActivityTime_liepin():
        try:
            now = int(time.time())
            timeArray = time.localtime(now)
            timeNow = time.strftime("%Y-%m-%dT%H:%M:%S+08:00", timeArray)
            return timeNow
        except Exception as e:
            return ""

    res = {
        "source": 'liepin',
        "originalId": resOriginalId_liepin(),
        "avatar": '',
        "fullName": resFullName_liepin(),
        "gender": resGender_liepin(),
        "birthday": '',
        "descriptions": {
            "city": resCity_liepin(),
            "interest": '',
            "personalStatement": resPersonalStatement_liepin(),
            "expectCity": resExpectCity_liepin(),
            "workLife": resWorkLife_liepin(),
            "contactPhoneNumber": resPhoneNumber_liepin(),
            "contactEmail": resEmail_liepin()
        },
        "skills": [],
        "languages": [],
        "certifications": [],
        "educations": [],
        "socialExperiences": [],
        "workExperiences": [],
        "lastActivityTime": resLastActivityTime_liepin()
    }

    try:
        skill = {}
        skills = d2('h3').filter(lambda i: "擅长技能" in pq(this).text()).next().text().split(' ')
        for i in skills:
            skill["name"] = i
            skill["proficiency"] = '一般'
            res["skills"] += [skill]
            skill = {}
            continue
    except Exception as e:
        res["skills"] = []

    try:
        language = {}
        languages = d2('h3').filter(lambda i: "语言能力" in pq(this).text()).next().text().split('、')
        for i in languages:
            language["name"] = i.split('(')[0]
            if u'粤语' in i.split('(')[0]:
                proficiency = '精通'
            elif u'简单' in i.split('(')[1]:
                proficiency = '一般'
            elif u'精通' in i.split('(')[1]:
                proficiency = '熟练'
            else:
                proficiency = '精通'
            language["proficiency"] = proficiency
            res["languages"] += [language]
            language = {}
            continue
    except Exception as e:
        res["languages"] = []

    cnt_liepin = 0
    education = {}
    while cnt_liepin < 5:
        educations = d2('div').filter('.view-table').children('dl').eq(cnt_liepin).children('dt').text()
        if educations == None:
            break
        education["school"] = educations.split("（")[0]
        education["startTime"] = resEducationStartTime_liepin(
            educations.split("（")[1].split("-")[0].strip().replace("）", ""))
        education["endTime"] = resEducationEndTime_liepin(
            educations.split("（")[1].split("-")[1].strip().replace("）", ""))
        education["major"] = d2('div').filter('.view-table').children('dl').eq(cnt_liepin).children('dd').children(
            'span').eq(0).text()[5:]
        education["degree"] = d2('div').filter('.view-table').children('dl').eq(cnt_liepin).children('dd').children(
            'span').eq(1).text()[3:]
        res["educations"] += [education]
        education = {}
        cnt_liepin += 1
        continue

    try:
        cnt1_liepin = 0
        workExperience = {}
        while cnt1_liepin < 5:
            flag = d2('div').filter('.view-company').children('h3').eq(cnt1_liepin).children('b').text()
            if flag == None:
                break
            workExperience["startTime"] = resEducationStartTime_liepin(
                    d2('div').filter('.view-company').children('h3').eq(cnt1_liepin).children('b').text().strip().split(
                        "-")[0])
            workExperience["endTime"] = resEducationEndTime_liepin(
                    d2('div').filter('.view-company').children('h3').eq(cnt1_liepin).children('b').text().strip().split(
                        "-")[1])
            workExperience["organization"] = \
            d2('div').filter('.view-company').children('h3').eq(cnt1_liepin).text().split(' ')[2]
            workExperience["position"] = \
            d2('div').filter('.view-company').children('div').eq(cnt1_liepin).children('div').children(
                'h4').text().split(' ')[0]
            workExperience["duties"] = d2('div').filter('.view-company').children('div').eq(cnt1_liepin).children(
                'div').children('ul').children("li").filter(lambda i: "工作职责：" in pq(this).text()).children('p').text()
            workExperience["department"] = d2('div').filter('.view-company').children('div').eq(cnt1_liepin).children(
                'div').children('ul').children("li").filter(lambda i: "所在部门：" in pq(this).text()).children('p').text()
            workExperience["address"] = d2('div').filter('.view-company').children('div').eq(cnt1_liepin).children(
                'div').children('ul').children("li").filter(lambda i: "工作地点：" in pq(this).text()).children('p').text()
            res["workExperiences"] += [workExperience]
            workExperience = {}
            cnt1_liepin += 1
            continue
    except Exception as e:
        res["workExperiences"] = []
    if tpyeFlag == "preview":
        old = db.customerProfiles.find_one({"source": "liepin", "originalId": str(res["originalId"])})
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