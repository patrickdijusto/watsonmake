import json
import datetime
import re
import requests
from unicodedata import normalize
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException
import twitter
from settings import *

global api
threshold = 0.51

## Run entire twitter infrastructure


print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nestablish the twitter object')
# see "Authentication" section below for tokens and keys
api = twitter.Api(consumer_key=CONSUMER_KEY,
	consumer_secret=CONSUMER_SECRET,
	access_token_key=OAUTH_TOKEN,
	access_token_secret=OAUTH_SECRET,
    )

print('twitter object established')

def getPast():
	## open file
	## 	Read # of last read tweet
	## Close file

	try:
		flx = open('pastNumber.txt',"r")
	except:
		flx = open('pastNumber.txt',"w")
		flx.write("0")
		flx.close()
		flx = open('pastNumber.txt',"r")
		
	
	row = flx.read()

	flx.close()
	               
	return int(row)

def getCurrent(pastNumber):
	
	##Contact twitter
	## Read most recent tweet that mentions @make
	## Extract Tweet ID Number	
	
	St = api.GetSearch(term='@make -RT', since_id = pastNumber, result_type = 'recent')
	
	return St
	
	
	
	

def writePast(ccc):
	flx = open('pastNumber.txt', "w")
	flx.write(str(ccc))
	flx.close()
        

		
def slack(id, text, name, score):

	## This is the section that sends data to a Slack channel
	## First, set the emotional threshold as a global at the top of the program, i.e. global threshold = 0.85 -- DONE
	## Then, see if a particular tweet equals or exceeds the threshold in any emotion -- DONE
	## Then format a string to send to Slack. "The tweet http://xxxxx/ shows unusually high levels of SADNESS in reference to @make. Some human should check it out." -- DONE
	## Then, establish the Slack API
	## Then send the string
	##message = "The tweet http://xxxxx/ shows unusually high levels of SADNESS in reference to @make. Some human should check it out.
	a = "The tweet http://twitter.com/anyuser/status/"+str(id)+" "
	b = "with text: '"+text+"' has an emotional rating of "+str(score)+" in the category "+name+". Someone should look into it."
	c=a+b
	print(a+b)
	z = "https://maker.ifttt.com/trigger/make_slack_threshold/with/key/oLkGeEI6UrkiMC4sK3nQNLZStJaMhKJC1JZT4kumhxm"
	data = { "value1" : c}
	r = requests.post(url = z, data = data)
	
	
	
	
	
	
	
	
		
		
pastNumber = getPast()

print ("Past number is:")

print (pastNumber)

outlist = getCurrent(pastNumber)

###writePast(outlist[0].id)




##  THE WATSON SECTION OF THE CODE
##  https://www.ibm.com/watson/developercloud/tone-analyzer/api/v3/python.html?python#tone
						
						
						
# 2017-09-21: The service can return results for the following tone IDs: anger, fear, joy, and sadness (emotional tones); analytical, confident, and tentative (language tones). The service returns results only for tones whose scores meet a minimum threshold of 0.5.
# 2016-05-19: The service can return results for the following tone IDs of the different categories: for the emotion category: anger, disgust, fear, joy, and sadness; for the language category: analytical, confident, and tentative; for the social category: openness_big5, conscientiousness_big5, extraversion_big5, agreeableness_big5, and emotional_range_big5. The service returns scores for all tones of a category, regardless of their values.
						
						
						
						
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
	##version='2016-05-19',
    username='419a0281-d84a-4281-bc03-3def84761f7f',
    password='aTC4VyXndf2v'
)


tone_analyzer.set_url('https://gateway.watsonplatform.net/tone-analyzer/api')

tone_analyzer.set_detailed_response(False)

content_type = 'application/json'


try:
	counter = 0
	for index in outlist:
		counter = counter +1
		mx = re.sub(r'https://\S+', '', normalize('NFKD', index.text).encode('ascii','ignore'))
		xx= mx.lstrip()
		jayson = [{"text": xx, "user":"customer"}]
		tone = tone_analyzer.tone_chat(jayson)
		##print(json.dumps(tone, indent=2))
		aa = tone[u'utterances_tone'][0][u'tones']
		if (aa):
			print("The tweet %s" % tone[u'utterances_tone'][0][u'utterance_text'])
			print(outlist[counter].id)
			print("has an emotional rating of:")
			for outdex in aa:
				print outdex[u'tone_name']
				print outdex[u'score']
				print("\n")
				if(outdex[u'score'])> threshold:
					slack(outlist[counter].id, xx, outdex[u'tone_name'], outdex[u'score'])
		else:
			print("\n")
		
except:
    #print "Method failed with status code " + str(ex.code) + ": " + ex.message
	print("Failure!")

	
	
## This is the section that sends data to the Google Sheet via POST via IFTTT
## First -- extract the URL of the tweet
## Then combine tone name and score into a single string
## Then use POST to send to IFTTT via webhooks
## Then let IFTTT update Google Sheet




