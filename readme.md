# pi setup
## getting it working on the pi  
sudo apt-get install python3-pip  git  
pip3 install -r requirements.txt

## installing temperature/humidity sensor code
This is done in C but the package below wraps that up for you (phew!)

git clone https://github.com/adafruit/Adafruit_Python_DHT.git
sudo python3 setup.py install

for C code (and wiring) check [here](http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/)

## settng cron job
crontab -e
*/1 * * * * /usr/bin/python3 /home/pi/officemonitoring/send_updates.py
for every 1 min

# Connecting to Hive
## First try with t'internet
### This blog
http://www.smartofthehome.com/2016/05/hive-rest-api-v6/

### API documentation
https://api.prod.bgchprod.info/omnia/swagger-ui.html

## Neither worked very well
Instead I decided to create a new action that turned on the socket for an 
hour. I then booted up fiddler, gave it https access then logged onto my Hive
account. In the dashboard I pressed the new action button. Fiddler had then 
recoreded a login command and a quick-action command.  

### Logon command

#### Request
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

#### Response
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

You first need the following key:value pair

json_response['token']

this is the auth header of all future requests.

Then you need to find the entry that relates to what you want to control. In
my case that was the action with the name Shed heater on:

json_response['actions']

will list all stored actions, find the one with the correct name and extract 
the id.

### Running a command 
todo

### logging out
MIGHT BE POST. CHECK FIDDLER
DELETE https://beekeeper-uk.hivehome.com/1.0/auth/logout HTTP/1.1
Accept: */*
content-type: application/json
authorization: {{TOKEN}}
Referer: https://my.hivehome.com/actions
Accept-Language: en-GB
Origin: https://my.hivehome.com
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
Host: beekeeper-uk.hivehome.com
Content-Length: 2
Connection: Keep-Alive
Cache-Control: no-cache

{}

