import json
##import datetime
import re
import requests
from unicodedata import normalize
#from watson_developer_cloud import ToneAnalyzerV3
#from watson_developer_cloud import WatsonApiException
import twitter
from textblob import TextBlob
#from settings import *

global api
threshold = 0.80

## Run entire twitter infrastructure
#BrooklynRadioTelegraph - Configuration
CONSUMER_KEY = "yq9tPAOkB6EnBg9c3LBA" 
CONSUMER_SECRET = "OSZeqNlIdJWmQRRkNBkMJsrW1YHmILE9ydPrcXcFF0" 
OAUTH_TOKEN = "813679214-mHPxrpt8vdnw2bAM8FPSC6pNTGXu1IecHrHzXJ9I" 
OAUTH_SECRET = "Rw0T5ryKt94ccCw0FD7WSLbOKKz2S12z1mfCAcRqY" 

print('\n\n\nestablish the twitter object')
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
	## Read most recent tweet(s) that mentions @make, but is not a retweet
	## return tweet

	St = api.GetSearch(term='@ejgertz', since_id = pastNumber, lang = 'en', result_type = 'recent')
	return St

def cleanTweet(tweet):
	
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \n])|(\w+:\/\/\S+)"," ", tweet).split())



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
	b = "with text: '"+text+"' has an emotional rating of "+str(score)+" in the category "+name+"."
	c=a+b
	print(a+b)
	z = "https://maker.ifttt.com/trigger/make_slack_threshold/with/key/oLkGeEI6UrkiMC4sK3nQNLZStJaMhKJC1JZT4kumhxm"
	data = { "value1" : c}
	r = requests.post(url = z, data = data)

def sheet(id, text, name, score):
    ##sad, frustrated, satisfied, excited, polite, impolite, and sympathetic
	## This is the section that sends data to a Google Spreadhseet
	## Uses the same emotional threshold as Slack
	## Open the Spreadsheet.txt file to read number of the spreadsheet row
	## POST the following data to spreadsheet cells:
	##	Column A: Datetime
	##	Column B: Tweet URL
	##	Column C: Tweet Text
	##	Column D: Sad Score
	##	Column E: Frustrated Score
	##	Column F: impolite score
	##	Column G: Satisfied score
	##	Column H: Excited Score
	##	Column I: Polite Score
	##	Column J: Sympathetic score
	

	#Get new row number
	flx = open('pastRow.txt',"r")
	row = int(flx.read())
	print(row)
	flx.close()

	print("Internal index == 1")
	col = 'B'+str(row)



	a = "http://twitter.com/anyuser/status/"+str(id)+" "

	z = "https://maker.ifttt.com/trigger/spreadsheet/with/key/oLkGeEI6UrkiMC4sK3nQNLZStJaMhKJC1JZT4kumhxm"
	data = { "value1" : col, "value2": a}
	print(data)
	r = requests.post(url = z, data = data)
	print(r)


	col = 'C'+str(row)
	data = { "value1" : col, "value2": text}
	print(data)
	r = requests.post(url = z, data = data)
	print(r)



	if(name == "Sad"):
		col = 'D'+str(row)
	elif(name == "Frustrated"):
		col = 'E'+str(row)
	elif(name == "Impolite"):
		col = 'F'+str(row)
	elif(name == "Satisfied"):
		col = 'G'+str(row)
	elif(name == "Excited"):
		col = 'H'+str(row)
	elif(name == "Polite"):
		col = 'I'+str(row)
	elif(name == "Sympathetic"):
		col = 'J'+str(row)

	print(col)
	data = { "value1" : col, "value2": score}

	print(data)
	r = requests.post(url = z, data = data)
	print(r)

	print("pre Row ")
	print(row)
	row = row+1
	print("final Row ")
	print(row)
	flx = open('pastRow.txt', "w")
	print(flx)
	result = flx.write(str(row))
	print(result)
	result = flx.close()
	print(result)


def getTweetSentiment(tweet):

	analysis = TextBlob(tweet)
	print(analysis.sentiment)
	print(analysis.sentiment.polarity)
	
	if analysis.sentiment.polarity >0:
		return "Positive"
		
	if analysis.sentiment.polarity <0:
		return "Negative"
		
	return "Neutral"






pastNumber = getPast()

print("Past number is:")

print(pastNumber)

outlist = getCurrent(pastNumber)

print(outlist)


for tweet in outlist:
	#print(tweet.quoted_status)
	print(tweet.text)
	print(cleanTweet(tweet.text))
	print(getTweetSentiment(cleanTweet(tweet.text)))
	print("\n")


#writePast(outlist[0].id)




# ##  THE WATSON SECTION OF THE CODE
# ##  https://www.ibm.com/watson/developercloud/tone-analyzer/api/v3/python.html?python#tone


# # 2017-09-21: The service can return results for the following tone IDs: anger, fear, joy, and sadness (emotional tones); analytical, confident, and tentative (language tones). The service returns results only for tones whose scores meet a minimum threshold of 0.5.
# # 2016-05-19: The service can return results for the following tone IDs of the different categories: for the emotion category: anger, disgust, fear, joy, and sadness; for the language category: analytical, confident, and tentative; for the social category: openness_big5, conscientiousness_big5, extraversion_big5, agreeableness_big5, and emotional_range_big5. The service returns scores for all tones of a category, regardless of their values.




# tone_analyzer = ToneAnalyzerV3(
    # version='2017-09-21',
	# ##version='2016-05-19',
    # username='419a0281-d84a-4281-bc03-3def84761f7f',
    # password='aTC4VyXndf2v'
# )


# tone_analyzer.set_url('https://gateway.watsonplatform.net/tone-analyzer/api')

# tone_analyzer.set_detailed_response(False)

# content_type = 'application/json'



# counter = 0
# print(counter)
# for index in outlist:
	# print("index: ")
	# print(index)
	# counter = counter +1
	# print("Counter: ") 
	# print(counter)
	# ax = index.text.encode('ascii','ignore').decode('utf-8')
	# print("ax:")
	# print(ax)
	# mx = re.sub(r'https://\S+', '', normalize('NFKD', index.text).encode('ascii','ignore').decode('utf-8'))
	# print("MX:")
	# print(mx)
	# xx= mx.lstrip()
	# print("xx")
	# print(xx)
	# jayson = [{"text": xx, "user":"customer"}]
	# tone = tone_analyzer.tone_chat(jayson)
	# print("Jayson dumps tone:")
	# print(json.dumps(tone, indent=2))
	# aa = tone[u'utterances_tone'][0][u'tones']
	# print("Jayson dumps utterances")
	# print(aa)
	# if (aa):
		# print("The tweet %s" % tone[u'utterances_tone'][0][u'utterance_text'])
		# print(outlist[counter].id)
		# print("has an emotional rating of:")
		# for outdex in aa:
			# print(outdex[u'tone_name'])
			# print(outdex[u'score'])
			# print("\n")
			# if(outdex[u'score'])> threshold:
				# slack(outlist[counter].id, xx, outdex[u'tone_name'], outdex[u'score'])
				# sheet(outlist[counter].id, xx, outdex[u'tone_name'], outdex[u'score'])
			
	# else:
		# print("\n")


# ## This is the section that sends data to the Google Sheet via POST via IFTTT
# ## First -- extract the URL of the tweet
# ## Then combine tone name and score into a single string
# ## Then use POST to send to IFTTT via webhooks
# ## Then let IFTTT update Google Sheet

