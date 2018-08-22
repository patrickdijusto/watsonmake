import json
import time
import re
from unicodedata import normalize
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException
import twitter
from settings import *

global api
## Run entire twitter infrasctucture

global handler
handler = "botrandrussell"



def estapi():
	print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nestablish the twitter object')
	# see "Authentication" section below for tokens and keys
	twapi = twitter.Api(consumer_key=CONSUMER_KEY,
	consumer_secret=CONSUMER_SECRET,
	access_token_key=OAUTH_TOKEN,
	access_token_secret=OAUTH_SECRET,
    )
	print('twitter object established')
	return twapi

	
def getMentions():
	
	namename=[]
	ment = api.GetMentions(count=1)
	print("\n\n\nLast mention:")
	
	##print(json.dumps("["+ment[0]+"]", indent=2))

	
	print(ment[0])
	print("\n\n")
	reply = ment[0].user.screen_name
	print("Reply to: %s\n\n" % reply)
	#print(ment[0].text)
	
	handler = re.sub(r'@\S+', '', ment[0].text).lstrip()
	
	# print(ment[1])
	print("\n\n")
	print(handler)
	# print("\n\n\n\n\n\n\n\n\n")
	
	# stat=api.GetStatus(ment[0])
	print("\n\n\n ID:")
	print(ment[0].id)
	# print("\n\n\n\n\n\n\n\n\n")
	namename.append(reply)
	namename.append(handler) 
	namename.append(ment[0].id)
	
	return namename
	
	
	
def getPast():
	## open file
	## 	Read # of previous tweet
	## Close file?

	try:
		flx = open('mypastNumber.txt',"r")
	except:
		flx = open('mypastNumber.txt',"w")
		flx.write("0")
		flx.close()
		flx = open('pastNumber.txt',"r")
		
	
	row = flx.read()

	flx.close()

	#writeLog("Writing past number: ", int(row), "w")
	               
	return int(row)

def getCurrent(onameka):
	
	##Contact twitter
	## Read Trump's most recent tweet
	## Extract Tweet ID Number

	putput=[]
	
	
	##St = api.GetUserTimeline(0,onameka,pastNumber,0,1)
	
	try:
		St = api.GetUserTimeline(screen_name=onameka,count=1)
	except Exception as err:
	#except twitter.error.TwitterError as err:
		return 0
	
	
	
	writeLog("Gotten current: ", 1, "a")

	print("And now we print the Status of the last Tweet")
	print(St)
		
	# print("And now just the first entry")
	# print (St[0].id)
	putput.append(St[0].id)


	
	print("\nThe text: \n")
	# mid_text = normalize('NFKD', St[0].text).encode('ascii','ignore')
	
	# midi_text = re.sub(r'https://\S+', '', mid_text)
	
	# out_text = re.sub(r'@\S+', '', midi_text)
	
	# mid_text = normalize('NFKD', St[0].text).encode('ascii','ignore')
	
	# midi_text = re.sub(r'https://\S+', '', normalize('NFKD', St[0].text).encode('ascii','ignore'))
	
	mid_text = re.sub(r'@\S+', '', re.sub(r'https://\S+', '', normalize('NFKD', St[0].text).encode('ascii','ignore')))
	
	out_text = mid_text.lstrip()
	
	print(out_text)	
	
	putput.append(out_text)

	
	return putput
	
	
	
	

def writePast(ccc):
        flx = open('mypastNumber.txt', "w")
        flx.write(str(ccc))
        flx.close()
        writeLog("writing past: ", int(ccc), "a")

		
def writeLog(TweetText, currentNumber, mode):

        ##print("Writing a log...")
        # now = datetime.datetime.now()
        # message = "\n"+str(now)
        
        fly = open("writeLog.txt", mode)
        # fly.write(message)
        fly.write(TweetText)
        fly.write(str(currentNumber))
        fly.close()

		

##  THE WATSON SECTION OF THE CODE
##  https://www.ibm.com/watson/developercloud/tone-analyzer/api/v3/python.html?python#tone
						
						
						
# 2017-09-21: The service can return results for the following tone IDs: anger, fear, joy, and sadness (emotional tones); analytical, confident, and tentative (language tones). The service returns results only for tones whose scores meet a minimum threshold of 0.5.
# 2016-05-19: The service can return results for the following tone IDs of the different categories: for the emotion category: anger, disgust, fear, joy, and sadness; for the language category: analytical, confident, and tentative; for the social category: openness_big5, conscientiousness_big5, extraversion_big5, agreeableness_big5, and emotional_range_big5. The service returns scores for all tones of a category, regardless of their values.
						
						
def watsonapi():						
						
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
		trone = tone_analyzer.tone({"text": outlist[1]},content_type, True)
	except WatsonApiException as ex:
	#except:
		print "Method failed with status code " + str(ex.code) + ": " + ex.message
		#print("Failure!")


	print(json.dumps(trone, indent=2))

	##print(tone)	

	return trone
	

	
def parser(tone):	
	
	result=""
	
	try:
		t0=(tone[u'document_tone'][u'tones'][0][u'tone_name'])
		s0=(tone[u'document_tone'][u'tones'][0][u'score'])
		result+="\n\r%s out of 100 for %s" % ((s0* 100),t0)
	except:
		result+=('\nNothing to report')


	try:	
		t1=(tone[u'document_tone'][u'tones'][1][u'tone_name'])
		s1=(tone[u'document_tone'][u'tones'][1][u'score'])
		result+="\n\r%s out of 100 for %s" % ((s1* 100),t1)
	except:
		print('Nothing further to report')
		
		
		
	try:
		t2=(tone[u'document_tone'][u'tones'][2][u'tone_name'])
		s2=(tone[u'document_tone'][u'tones'][2][u'score'])
		result+="\n\r%s out of 100 for %s" % ((s2* 100),t2)
	except:
		print('Nothing further to report')
		

	try:	
		t3=(tone[u'document_tone'][u'tones'][3][u'tone_name'])
		s3=(tone[u'document_tone'][u'tones'][3][u'score'])
		result+="\n\r%s out of 100 for %s" % ((s3* 100),t3)
	except:
		print('Nothing further to report')
		
	return result	


def answer(names, text):

	reply = "@"+names[0]+ " : "

	if(text =="RT"):
		reply +="The last tweet from "+names[1]+" was a retweet and therefore unsuitable for analysis."
	elif (text =="NO"):
		reply +="The user "+names[1]+" doesn't seem to exist."
	else:
		reply += "The last tweet from "+names[1]+" gets: \n"+text
	
	print(reply)
	api.PostUpdate(reply)
	
		
		
if __name__ == "__main__":		
		
	api = estapi()		

	while(1):
		names= getMentions()
		pastNumber = getPast()
		print("Past number is:")
		print(pastNumber)
		print("Current number is:")
		print(names[2])
		if(pastNumber<names[2]):
			outlist = getCurrent(names[1])
			print(outlist)
			if(outlist!=0):
				writePast(names[2])
				if(outlist[1][:2] != "RT"):
					results = parser(watsonapi())
					answer(names, results)
				else:
					answer(names, "RT")
			else:
				answer(names,"NO")
		else:
			time.sleep(60)
		time.sleep(60)