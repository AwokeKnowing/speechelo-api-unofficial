import asyncio
import json
import requests
import re
import time


class Speechelo:

    def __init__(self):

        self.headers = headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.voiceConfig = {
            "languageSelected":"en-US",
            "engineSelected":"neural",
            "voiceSelected":"Salli",
            "toneSelected":"normal"
        }

        self.devicehw = 'hw:0,0'  


    def auth(self, user, password):
        data = {
            'email': user, 
            'password': password
        }

        self.rsession = requests.Session() 

        self.rsession.post("https://app.blasteronline.com/user/authenticate", 
                          data=data, headers=self.headers)

        return self


    def campaign(self, campaignId):
        self.campaignId = campaignId
        return self

    def voice(self, voiceConfig):
        self.voiceConfig = voiceConfig
        return self

    def device(self, hwdevice):
        self.hwdevice = hwdevice
        return self

    async def text2url(self, text):
        data = {
            "text":text,
            "charCount": len(text),
            "wordsCount": len(re.findall(r'\S+', text, re.M)),
            "campaignId": self.campaignId
        }

        body = {"data": json.dumps({**self.voiceConfig, **data})}

        r = self.rsession.post(
            "https://app.blasteronline.com/speechelo/blastVoice", 
            data=body, headers=self.headers)
        
        r = self.rsession.get(
            "https://app.blasteronline.com/speechelo/getMyBlasters/?_=" +
            str(int(time.time()*1000)), headers=self.headers)
        response = r.json()
          
        url = response['data'][-1]['download_link']

        return url

    async def playhttp(self, url):
        command = ('gst-launch-1.0 souphttpsrc location=' + url +
                   ' ! mpegaudioparse ! avdec_mp3 ! audioconvert' +
                   ' ! alsasink -e device=' + self.hwdevice)
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

    async def say(self, text):
        url = await self.text2url(text)
        print(url)
        
        return await self.playhttp(url)
        
