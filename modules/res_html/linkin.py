# coding=utf-8
import sys
import time

from pyquery import PyQuery as pq
import requests
import json
from flask import request, Response
reload(sys)
sys.setdefaultencoding("utf-8")
s = requests.session()


def resume_linkin(db, name, password, customerId, accessToken, flag, url, cookie):
    cookie = 'bcookie="v=2&134a4bbf-2780-4ce0-8470-8e19d72ec94d"; bscookie="v=1&201509280415165d0fa483-7554-447d-8955-e402b175bc4fAQHEpF7eC52VMR_ZmPMsoH5faAzfpdQj"; visit="v=1&M"; _leo_profile=""; VID=V_2016_01_05_00_61437; token=Y1hwwoFat6z8ht4vvtc%2BC5%2FLN%2BY%3D%7CQAwMxIxupQgfFwmzZ0OnWwYiOVG9c%2BIkdeJxw3Ag8%2Bxde5GiSUbgxAMrsQ5HKj1MunM8KgN5%2FKIT6mA5FwUuG8%2Fwb96Pt9EDdk5s43UGovJxjTe1nbkQFOFWS3cd2X3iJJPawTw8BpIflUGW%2BFuiyxy90wBaI3vv9tH4AoazGYs0ewE%2B6jrwir3W6wjnVZhmFfPAbe7iAlnhNpDzNGUDsfEdGs15G3taTQvlRgyJ13uOLhFJagyqFrVPMV1pbf%2FcIbOEB2UPucEPWMzLFgYS3A%3D%3D; __utma=226841088.988934834.1452135439.1452234640.1452587561.3; __utmz=226841088.1452587561.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=226841088.authorized; li_at=AQEDARwRmAYDhgcvAAABUj451OMAAAFSQ9p9Z0sAf99Yl1tzZKEb_kjUHpeL6NfGPl_u0jEgAKHDitVP1efleT90qzX9H5xItEvj6KegioRvS6Tcx72DJcmjX_1ZZla30Rh0ZkBU6JDR_iDWTlCBTpkh; liap=true; sl="v=1&SLgK2"; JSESSIONID="ajax:7988878064080772902"; L1c=33142229; oz_props_fetch_size1_undefined=undefined; wutan=B7oB1CInAf3VPIJFySdLMnrC+w1xXnek5WYA5kqoXEA=; share_setting=PUBLIC; _gat=1; gdfCookie=QnDM6kTkyA6UFmfE26gn5lGClB0%3D%7CdbaznvWWXPh7UogyXRi%2FNQ5mO%2B%2B1nz1hZ%2BKcSgv8SPY%3D; L1e=a98019b; SID=ef1d2b4a-7e17-48cc-afc3-05a5470cde4e; RT=s=1452830229177&r=https%3A%2F%2Fwww.linkedin.com%2Fuas%2Foauth2%2Fauthorization; _lipt=0_1L5-ZR1gdZdKWGss9Hjn3kQAmjAOhaGNBAjQ0mPuIJ47nEnftXqFJhfeN5sQdnbG0TogGzl6spqqlnStIPVJHfoG63tRyWvY5w6iNUeQbT0oZirBkfqBb8LKUXSANUkmjsy8_I5DSA09mTHAUgBhZFjNjn9r90-aq2RlX81_NH5btnglyW85Z2rI1YoWcuDrpIkJvS1QfkFtLkb1zrnPea; lang="v=2&lang=zh-cn"; _ga=GA1.2.988934834.1452135439; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; lidc="b=LGST08:g=11:u=1:i=1452830264:t=1452916538:s=AQFsNSphOFhxaACTzmA74rvRJboJSrNN"'
    html = pq(url, headers={'Cookie': cookie})
    userName = html("span[class='full-name']").text()
    userName = userName.replace(" ", "")
    if u"(未添加外文名)" in userName:
        userName = userName.replace("(未添加外文名)", "")
    self_evaluation = html("p[class='description']").text()
    if not self_evaluation:
        self_evaluation = ""

    resume_id = html("a[class='view-public-profile']").text()
    originalId = resume_id.split("-")[2]

    meta_experience = html("#background-experience").children()
    workExperiences = []
    if not meta_experience:
        workExperiences = []
    else:
        for i in range(1, len(meta_experience) - 1):
            work_end = meta_experience.eq(i)("span[class='experience-date-locale']").eq(0).find("time").eq(1).text()
        if not work_end:
            work_end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            positionName = meta_experience.eq(i)("div[class='editable-item section-item current-position']").find(
                "a[title='详细了解']").text()
            companyName = meta_experience.eq(i)("div[class='editable-item section-item current-position']").find(
                "a[name='company']").text()
            work_start = meta_experience.eq(i)("span[class='experience-date-locale']").eq(0).find("time").eq(0).text()
        else:
            positionName = meta_experience.eq(i)("div[class='editable-item section-item past-position']").find(
                "a[title='详细了解']").text()
            companyName = meta_experience.eq(i)("div[class='editable-item section-item past-position']").find(
                "strong").text()
            if companyName == "":
                companyName = meta_experience.eq(i)("div[class='editable-item section-item past-position']").find(
                    "a[name='company']").text()
            work_start = meta_experience.eq(i)("span[class='experience-date-locale']").eq(0).find("time").eq(0).text()
            work_end = meta_experience.eq(i)("span[class='experience-date-locale']").eq(0).find("time").eq(1).text()
            work_end = work_end.replace(" ", "")
            if u"年" in work_end:
                work_end = work_end.replace("年", "-")
            if u"月" in work_end:
                year = work_end.replace("月", "").split("-")[0]
                mouth = work_end.replace("月", "").split("-")[1]
            if int(mouth) > 9:
                work_end = year + "-" + mouth
            else:
                work_end = year + "-0" + mouth
            work_end = work_end + "-01T00:00:00.000+08:00"
        duty = meta_experience.eq(i)("p[class='description summary-field-show-more']").text()
        work_start = work_start.replace(" ", "")
        if u"年" in work_start:
            work_start = work_start.replace("年", "-")
        if u"月" in work_start:
            year = work_start.replace("月", "").split("-")[0]
            mouth = work_start.replace("月", "").split("-")[1]
            if int(mouth) > 9:
                work_start = year + "-" + mouth
            else:
                work_start = year + "-0" + mouth
        work_start = work_start + "-01T00:00:00.000+08:00"
        work = {
            "organization": companyName,
            "position": positionName,
            "department": "",
            "address": "",
            "startTime": work_start,
            "endTime": work_end,
            "duties": duty,
            "workType": "全职"
        }
        workExperiences += [work]
    meta_eduction = html("#background-education").children()
    educations = []
    if not meta_eduction:
        educations = []
    else:
        for i in range(1, len(meta_eduction) - 1):
            schoolName = meta_eduction.eq(i)("div[class='editable-item section-item']").find("a[title='学校详细信息']").text()
        major = meta_eduction.eq(i)("div[class='editable-item section-item']").find("span[class='major']").find(
            "a").text()
        degree = meta_eduction.eq(i)("div[class='editable-item section-item']").find("span[class='degree']").text()
        eduction_start = meta_eduction.eq(i)("span[class='education-date']").eq(0).find("time").eq(0).text()
        eduction_end = meta_eduction.eq(i)("span[class='education-date']").eq(0).find("time").eq(1).text()
        eduction_end = eduction_end.replace("– ", "")
        eduction_start = eduction_start + "-09-01T00:00:00.000+08:00"
        eduction_end = eduction_end + "-06-30T00:00:00.000+08:00"
        courses = meta_eduction.eq(i).find("li").text()
        courses = courses.replace(" ", ",")
        eduction = {
            "school": schoolName,
            "major": major,
            "degree": degree,
            "startTime": eduction_start,
            "endTime": eduction_end,
            "courses": courses,
            "grade": "大一",
            "award": "",
            "gpa": 0,
            "gpaMax": 0,
            "minor": ""
        }
        educations += [eduction]
    meta_skill = html("ul[class='skills-section']").children()
    skills = []
    if not meta_skill:
        skills = []
    else:
        for i in range(0, len(meta_skill)):
            skillName = meta_skill.eq(i)("span[class='endorse-item-name-text']").text()
            skill = {
                "name": skillName,
                "proficiency": "",
            }
            skills += [skill]

    meta_language = html.find("li[class='section-item']")
    languages = []
    if not meta_language:
        languages = []
    else:
        for i in range(0, len(meta_language)):
            languageName = meta_language.eq(i)("span[dir='auto']").text()
        language = {
            "name": languageName,
            "proficiency": "熟练",
            "subject": "",
            "score": ""
        }
        languages += [language]

    res = {
        "source": 'LinkedIn',
        "originalId": originalId,
        "avatar": "",
        "fullName": userName,
        "gender": "男",
        "birthday": "",
        "descriptions": {
            "city": "",
            "interest": self_evaluation,
            "sign": "",
            "expectCity": "",
            "message": "",
            "worklife": 0,
            "contactphonenumber": "",
            "contactEmail": name
        },
        "skills": skills,
        "languages": languages,
        "workExperiences": workExperiences,
        "educations": educations,
    }
    if flag == "preview":
        old = db.customerProfiles.find_one({"source": "linkin", "originalId": str(res["originalId"])})
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