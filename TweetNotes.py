import twitter
import re
from appscript import app
from appscript import k
from osax import OSAX

Notes = []
# These strings are used to identify notes. Feel free to change them!
MATCH_STRING 		= "#TwtNotes"
CONTINUE_STRING 	= "#con"
# Get your API credentials from twitter and put them here!
CONSUMER_KEY 		= ""
CONSUMER_SECRET 	= ""
ACCESS_TOKEN 		= ""
ACCESS_TOKEN_SECRET = ""

def extractNotes() :
	tweets = getTweets()
	
	for i,tweet in enumerate(tweets):
		flag = 0
		match = re.search(MATCH_STRING, tweet, re.IGNORECASE)

		if match:
			continuing_tweets = []
			# check if the note continues			
			if continue_match(tweet) :				
				note_text = ' '.join(tweet.split(" ")[1:-1])				
				flag += 1

				# Keep checking if the note continues
				while True:					
					next_tweet = tweets[i - flag]					

					if continue_match(next_tweet):
						continuing_tweets.append(strip_tag(next_tweet))
						flag += 1

					else :				
						continuing_tweets.append(next_tweet)
						break
				
				createNote(note_text, continuing_tweets)
					
			else:
				# Extract note from the matching tweet
				note_text = ' '.join(tweet.split(" ")[1:])			
				# create a textedit note with the text of the note
				createNote(note_text, [])


def createNote(tweet, continued):
	app_ref = app('TextEdit').make(new=k.document,with_properties={k.text:tweet})
	if len(continued) != 0:
		for note in continued:
			app_ref.make(new = k.paragraph, at=app_ref.text.end ,with_data=" "+note)



def continue_match(tweet) :

	return re.search(CONTINUE_STRING, tweet, re.IGNORECASE)	

def strip_tag(tweet) :

	return ' '.join(tweet.split(" ")[:-1])
	

def getTweets() :
	print("Fetching Tweets from your timeline!")
	statuses = api.GetUserTimeline(user, count=20)
	tweets = []

	for status in statuses:
		tweets.append(status.text)

	return tweets



try:
	# Provide Twitter API Credentials
	api = twitter.Api(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, access_token_key = ACCESS_TOKEN, access_token_secret = ACCESS_TOKEN_SECRET)
	
	# Verify API Credentials
	user = api.VerifyCredentials()
	if user :
		print("Verified API Credentials")

	Notes = extractNotes()
	print("All notes fetched!")
	mac = OSAX()
	mac.say("All notes have been fetched, sir!", using="victoria")



except Exception as e:
	print("Error Occurred : {0}").format(e)


