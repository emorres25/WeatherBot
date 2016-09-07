import json, requests, random, re
from pprint import pprint
import json
from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
access_token = 'EAAZAd1C9D1SkBAF5Vsb0j3MpNtAZCoDYWMiSdoNzPMdxfv4eC1Ai9E6GoWhkSUSOTJZCL5r7r1Pis753XjQgu4rRlqtTZAzOEqp9ziwpUR2IPEMPjCl2wZAxLYN9reD20ZBnwtHqcDx6ZC0dFSyGt8e14992ew1wE01iVorURPs5AZDZD'
verify_token = '8510865767'
yo_token = 'a9e75c9f-a085-4c5f-be02-4faa915eac29'
yo_username = 'EMORRES25'
weather_api = 'cbeab3a7abb6575f1db5828d3cee0f06'
#url = 'http://api.wordnik.com:80/v4/word.json/tycoon/definitions?limit=200&includeRelated=true&useCanonical=false&includeTags=false&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'
'''
def get_meaning(fbid, recieved_message):
    url = 'http://api.wordnik.com:80/v4/word.json/' + recieved_message.lower() + '/definitions?limit=200&includeRelated=true&useCanonical=false&includeTags=false&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'
    try:
        r = requests.get(url).json()[0]["text"]
        fdata = str(r)
    except:
        fdata = "The word was noy found!"

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'% access_token
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":fdata}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
'''
def send_yo():
    requests.post("http://api.justyo.co/yo/", data={'api_token': yo_token, 'username': yo_username, 'text': "dictbot was recently used."})

def get_weather(fbid, lati,longi):
    url = 'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=%s' % (lati,longi,weather_api)
    r = requests.get(url)
    data = json.loads(r.text())
    main = data['weather'][0]['description']

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'% access_token
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":main}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


def post_msg(fbid, text):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'% access_token
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":text})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class dictbot(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == verify_token:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
 
 
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']: 
                if 'message' in message: 
                    try:  
                        #lati = message['message']['attachments'][0]['payload']['coordinates']['lat']
                        #longi = message['message']['attachments'][0]['payload']['coordinates']['long']
                        lati = 'papa'
                        longi = 'mama'
                        text = "lat is: %s and long is %s" % (lati, longi)
                        post_msg(message['sender']['id'], text)

                        #get_weather(message['sender']['id'], lati, longi)

                        #get_meaning(message['sender']['id'], message['message']['attachments'][0]['payload']['coordinates'])
                        #get_meaning(message['sender']['id'], message['message']['text'])
                        #send_yo()
                    except Exception as e:
                        print e
                        get_meaning(message['sender']['id'], 'Please send a valid text.')    
                        send_yo()
        return HttpResponse()