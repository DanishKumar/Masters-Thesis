import tweepy
import csv
import os

ckey = "lTtJFQw7VcSmGuq2rXEPPtiRM"
csecret = "bbEpVT3VLptOw2k8SoVn4HgFP6B0REAxbXwQrxmuGacYb15I5K"
atoken = "2217386142-N9Zg6ySIWmLZm2mHFsBGIf9A32OsKp9jOQZ24gf"
asecret = "cqq2HCyJAzPkbGcWL0ySWqvHuwWYqF7TF4O4czI1Dqqoa"

OAUTH_KEYS = {'consumer_key':ckey, 'consumer_secret':csecret,
    'access_token_key':atoken, 'access_token_secret':asecret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)

file_exists = os.path.isfile('C:\Users\Danish Kumar\Desktop\dataset\americanidol.csv')
csvFile = open('americanidol.csv', 'ab')
fields = ('Tweet_Id', 'Tweet_Text','Tweet_authorscreen_name','Tweet_author_id','Tweet_created_at','Tweet_coordinates','Tweet_source','Tweet_user_verified','Tweet_retweet_count','Tweet_lang','Tweet_favcount','Tweet_username','Tweet_userid','Tweet_location') #field names
csvWriter = csv.DictWriter(csvFile, fieldnames=fields)
if not file_exists:
    csvWriter.writeheader()
    
c = tweepy.Cursor(api.search, q="#americanidol", since="2019-04-14", until="2019-04-19", lang="en", tweet_mode="extended").items()

count=0;
while True:
    try:
        tweet = c.next()
        for tweet in tweepy.Cursor(api.search, q="#psl", since="2019-04-14", until="2019-04-19", tweet_mode="extended").items():
            print (tweet.id_str, (tweet.full_text.encode('utf-8').replace('\n', '').replace('\r', ' ').decode('unicode_escape').encode('ascii','ignore').strip()), tweet.author.screen_name, tweet.author.id, tweet.created_at,tweet.coordinates,tweet.source,tweet.user.verified,tweet.retweet_count,tweet.lang,tweet.user.favourites_count,tweet.user.name,tweet.user.id_str,tweet.user.location)
            csvWriter.writerow({'Tweet_Id': tweet.id_str, 'Tweet_Text': (tweet.full_text.encode('utf-8').replace('\n', '').replace('\r', ' ').decode('unicode_escape').encode('ascii','ignore').strip()),'Tweet_authorscreen_name':tweet.author.screen_name.encode('utf-8').strip(),'Tweet_author_id':tweet.author.id,'Tweet_created_at':tweet.created_at,'Tweet_coordinates':tweet.coordinates,'Tweet_source':tweet.source.encode('utf-8').strip(),'Tweet_user_verified':tweet.user.verified,'Tweet_retweet_count':tweet.retweet_count,'Tweet_lang':tweet.lang.encode('utf-8').strip(),'Tweet_favcount':tweet.user.favourites_count,'Tweet_username':tweet.user.name.encode('utf8').strip(),'Tweet_userid':tweet.user.id_str,'Tweet_location':tweet.user.location.encode('utf-8').strip()})
            count +=1
            
    except tweepy.TweepError:
        print("Whoops, could not fetch more! just wait for 15 minutes :")
        time.sleep(900)
        continue
    except StopIteration:
        break
csvFile.close()
print(count)
