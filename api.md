# 导入第三方简历API文档 


### POST /resume

+ 描述: 导入第三方简历

#### 51job 智联 猎聘 请求示例

headre:
Authorization:Bearer T6vzEw2n0sBH33ko

```
{
    "name":"hljmlshiyan123@163.com",
    "password":"ml57086151",
    "web_name":"51job/liepin/zhilian",
    "customerId":"564ed0ea32d2e40928c8efb8",
    "flag":"preview/insert"  
}
```
+PS:
	flag为previe时代表是预览操作

####领英 请求示例

headre:
Authorization:Bearer T6vzEw2n0sBH33ko

```
{
    "name":"hljmlshiyan123@163.com",
    "password":"ml57086151",
    "web_name":"linkin",
    "customerId":"564ed0ea32d2e40928c8efb8",
    "url":"https://www.linkedin.com/in/%E9%93%B6-%E6%9D%8E-4866b010b?authType=name&authToken=KduM&trk=api*a3227641*s3301901*",
    "cookie":'bcookie="v=2&134a4bbf-2780-4ce0-8470-8e19d72ec94d"; ',
    "flag":"preview/insert"  
}
```
#### 正确 响应示例(预览)

```
{
  "message": "ok",
  "code": 200,
  "data": {
    "customerId": "569de57a1d41c81d0dde4584"
  }
}
```

#### 正确 响应示例(插入)
```
{
  "data": {
    "applications": null,
    "articles": null,
    "businessProfiles": null,
    "comments": null,
    "companies": null,
    "customerProfiles": [
      {
        "id": "564ed0ea32d2e40928c8efb8",
        "userId": "564ec19632d2e40928c816f3",
        "avatar": "",
        "fullName": "石岩",
        "gender": "男",
        "birthday": "",
        "score": 0,
        "integrity": 14,
        "descriptions": {
          "sign": "",
          "city": "北京-朝阳区",
          "interest": "",
          "personalStatement": "",
          "expectCity": "北京",
          "workLife": 0,
          "contactPhoneNumber": "15010258799",
          "contactEmail": "hljmlshiyan123@163.com",
          "message": "我的专业是对每一个项目的嗅觉，对每一笔巨额资金的掌控！",
          "expectedIndustry": ""
        },
        "privacy": {
          "profile": "",
          "education": "",
          "workExperience": "",
          "socialExperience": ""
        },
        "defaultResume": null,
        "videoResume": null,
        "languages": null,
        "skills": null,
        "workExperiences": null,
        "socialExperiences": null,
        "educations": null,
        "certifications": null,
        "counts": {
          "restApplyTimes": 0
        },
        "status": "default",
        "type": "customerProfile",
        "flags": {
          "haveVideoResume": false,
          "disableVideoPrompt": true,
          "deliverVideoResume": false,
          "applied": false,
          "invited": false
        },
        "lastActivityTime": "2016-01-19T15:14:22.992+08:00",
        "hideFromSearch": false
      }
    ],
    "moments": null,
    "positions": null,
    "interviews": null,
    "interviewContacts": null,
    "replies": null,
    "resumes": null,
    "users": null,
    "histories": null,
    "notifications": null,
    "total": 0
  },
  "code": 200,
  "message": "OK"
}
```


#### 错误 响应示例
```
{
  "message": "not found",
  "code": 404,
  "data": {}
}
```
