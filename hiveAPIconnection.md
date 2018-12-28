#First try with t'internet
## This blog
http://www.smartofthehome.com/2016/05/hive-rest-api-v6/

## API documentation
https://api.prod.bgchprod.info/omnia/swagger-ui.html

# Neither worked very well
Instead I decided to create a new action that turned on the socket for an 
hour. I then booted up fiddler, gave it https access then logged onto my Hive
account. In the dashboard I pressed the new action button. Fiddler had then 
recoreded a login command and a quick-action command.  

## Logon command

###Request
**Only the content-type was needed in the request header**
POST https://beekeeper.hivehome.com/1.0/global/login HTTP/1.1
Accept: */*
content-type: application/json
Referer: https://my.hivehome.com/login
Accept-Language: en-GB
Origin: https://my.hivehome.com
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
Host: beekeeper.hivehome.com
Content-Length: 128
Connection: Keep-Alive
Cache-Control: no-cache

{
"username":"XXX",
"password":"XXX",
"devices":true,
"products":true,
"actions":true,
"homes":true}

### Response
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Content-Length: 16225
Connection: keep-alive
Date: Fri, 28 Dec 2018 16:59:47 GMT
x-amzn-RequestId: XXX
Access-Control-Allow-Origin: *
x-amz-apigw-id: XXX
X-Amzn-Trace-Id: XXX
X-Cache: Miss from cloudfront
Via: 1.1 XXX.cloudfront.net (CloudFront)
X-Amz-Cf-Id: XXX

Response body was very verbose, trimmed for brevity (and security, it contains
everything they know about you, all your devices, schedules, etc etc. Even the 
lat/long of your house).

you simpply need one key:value pair

token:auth-token

this is the auth header of all future requests







# All requests must have the following headers:

Content-Type:application/vnd.alertme.zoo-6.5+json
Accept:application/vnd.alertme.zoo-6.5+json
X-Omnia-Client:Hive Web Dashboard

## All but tthe first also need 
X-Omnia-Access-Token: {{TOKEN}}

TOKEN is aquired by the first call:

# Call 1:
POST https://api-prod.bgchprod.info:443/omnia/auth/sessions

## With body:

{
    "sessions": [{
        "username": "{{EMAIL}}",
        "password": "{{PASSWORD}}",
        "caller": "WEB"
    }]
}

## Which returns:
{
    "meta": {},
    "links": {},
    "linked": {},
    "sessions": [
        {
            "id": "xx",
            "username": "xx",
            "userId": "xx",
            "extCustomerLevel": n,
            "latestSupportedApiVersion": "x",
            "sessionId": "TOKEN" <- THIS IS WHAT YOU WANT 
        }
    ]
}

# List all devices:
GET https://api.prod.bgchprod.info/omnia/nodes

You can find your devices by name, it also lists your rules/alerts. 

