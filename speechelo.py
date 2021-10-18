import requests
import re
from subprocess import Popen
import time


class Speechelo:

    def __init__(self, config):

        self.headers = headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.voice = {
            "languageSelected":"en-US",
            "engineSelected":"neural",
            "voiceSelected":"Salli",
            "toneSelected":"normal"
        }

        self.device = 'hw:0,0'  


    def auth(self, user, password):
        data = {
            'email': user, 
            'password': password
        }

        r = requests.post("https://app.blasteronline.com/user/authenticate", 
                          data=data, headers=self.headers)
        self.cookies = r.cookies

        return self


    def campaign(self, campaignId):
        self.campaignId = campaignId
        return self

    def voice(self, voice):
        self.voice = voice
        return self

    def device(self, device):
        self.device = device
        return self

    def text2url(self, text):
        data = {
            "text":text,
            "charCount": len(text),
            "wordsCount": len(re.findall(r'\S+', text, re.M)),
            "campaignId": self.campaignId
        }

        data = {**self.voice, **data}

        r = requests.post("https://app.blasteronline.com/speechelo/blastVoice", 
                          data=data, headers=self.headers, cookies=self.cookies)
        
        self.cookies = r.cookies
        
        r = requests.get("https://app.blasteronline.com/speechelo/getMyBlasters/?_="+
                         str(int(time.time())), headers=self.headers, cookies=self.cookies)
        
        self.cookies = r.cookies

        response = r.json()
        print(r.json())

        url = response['data'][-1]['download_link']

        return url

    def playhttp(url):
        p = Popen(['watch', 
                   'gst-launch-1.0 souphttpsrc location=' + url +
                   ' ! mpegaudioparse ! avdec_mp3 ! audioconvert ! ' +
                   'alsasink -e device=' + self.device]) 

        time.sleep(1)
        p.terminate()


    def say(self, text):
        url = self.text2url(text)
        playhttp(url)
        
        
