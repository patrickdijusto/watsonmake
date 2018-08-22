import json
import datetime
import re
from unicodedata import normalize
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException
import twitter
from settings import *

global api
## Run entire twitter infrasctucture


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

	putput=[]
	
	
	St = api.GetSearch(term='@make', since_id = pastNumber)

	print("And now we print the Status of the last Tweets")
	
	for index in St:
		mx = re.sub(r'@\S+', '', re.sub(r'https://\S+', '', normalize('NFKD', index.text).encode('ascii','ignore')))
		print(mx.lstrip())
		print("\n\n\n\n")

	# print(re.sub(r'@\S+', '', re.sub(r'https://\S+', '', normalize('NFKD', St[1].text).encode('ascii','ignore'))))
	# print(re.sub(r'@\S+', '', re.sub(r'https://\S+', '', normalize('NFKD', St[2].text).encode('ascii','ignore'))))
	# print(re.sub(r'@\S+', '', re.sub(r'https://\S+', '', normalize('NFKD', St[3].text).encode('ascii','ignore'))))
	# print(re.sub(r'@\S+', '', re.sub(r'https://\S+', '', normalize('NFKD', St[4].text).encode('ascii','ignore'))))
	
		
	print("And now just the first entry")
	print (St[0].id)
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
        flx = open('pastNumber.txt', "w")
        flx.write(str(ccc))
        flx.close()
        writeLog("writing past: ", int(ccc), "a")

		
def writeLog(TweetText, currentNumber, mode):

        ##print("Writing a log...")
        now = datetime.datetime.now()
        message = "\n"+str(now)
        
        fly = open("writeLog.txt", mode)
        fly.write(message)
        fly.write(TweetText)
        fly.write(str(currentNumber))
        fly.close()

pastNumber = getPast()

print ("Past number is:")

print (pastNumber)


##outlist = getCurrent(pastNumber,handler)
outlist = getCurrent(pastNumber)

print(outlist)

#writePast(outlist[0])


# if (currentNumber > pastNumber):
        # postReply(TweetText, currentNumber)
						

##  THE WATSON SECTION OF THE CODE
##  https://www.ibm.com/watson/developercloud/tone-analyzer/api/v3/python.html?python#tone
						
						
						
# 2017-09-21: The service can return results for the following tone IDs: anger, fear, joy, and sadness (emotional tones); analytical, confident, and tentative (language tones). The service returns results only for tones whose scores meet a minimum threshold of 0.5.
# 2016-05-19: The service can return results for the following tone IDs of the different categories: for the emotion category: anger, disgust, fear, joy, and sadness; for the language category: analytical, confident, and tentative; for the social category: openness_big5, conscientiousness_big5, extraversion_big5, agreeableness_big5, and emotional_range_big5. The service returns scores for all tones of a category, regardless of their values.
						
						
						
						
# tone_analyzer = ToneAnalyzerV3(
    # ##version='2017-09-21',
	# version='2016-05-19',
    # username='419a0281-d84a-4281-bc03-3def84761f7f',
    # password='aTC4VyXndf2v'
# )


# tone_analyzer.set_url('https://gateway.watsonplatform.net/tone-analyzer/api')

# tone_analyzer.set_detailed_response(False)

# content_type = 'application/json'


# try:
	# if(outlist[1][:2] != "RT"):
		# tone = tone_analyzer.tone({"text": outlist[1]},content_type, True)
# except WatsonApiException as ex:
# #except:
    # print "Method failed with status code " + str(ex.code) + ": " + ex.message
	# #print("Failure!")


# print(json.dumps(tone, indent=2))

# print(tone)	

# try:
	# t0=(tone[u'document_tone'][u'tones'][0][u'tone_name'])
	# s0=(tone[u'document_tone'][u'tones'][0][u'score'])
	# print("\nThis tweet gets %s out of 100 for %s" % ((s0* 100),t0))
# except:
	# print('\nNothing to report')


# try:	
	# t1=(tone[u'document_tone'][u'tones'][1][u'tone_name'])
	# s1=(tone[u'document_tone'][u'tones'][1][u'score'])
	# print("This tweet gets %s out of 100 for %s" % ((s1* 100),t1))
# except:
	# print('Nothing further to report')
	
	
	
# try:
	# t2=(tone[u'document_tone'][u'tones'][2][u'tone_name'])
	# s2=(tone[u'document_tone'][u'tones'][2][u'score'])
	# print("This tweet gets %s out of 100 for %s" % ((s2* 100),t2))
# except:
	# print('Nothing further to report')
	

# try:	
	# t3=(tone[u'document_tone'][u'tones'][3][u'tone_name'])
	# s3=(tone[u'document_tone'][u'tones'][3][u'score'])
	# print("This tweet gets %s out of 100 for %s" % ((s3* 100),t3))
# except:
	# print('Nothing further to report')


