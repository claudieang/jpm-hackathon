import got as got
import csv
import codecs
import time
import threading
from datetime import datetime, timedelta

def getTweet(keyword, start, end):
	print ("in tweet -- %s" %keyword)
	print (end)
	print (start)
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setSince(end).setUntil(start).setMaxTweets(10000000)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)

	print ("number of Tweets: %d" % len(tweet))
	print ('')
	return tweet

def receiveBuffer(fname,tweets):
	outputFileName = './data/' + fname +".csv"
	outputFile = codecs.open(outputFileName, "a", "utf-8")

	for t in tweets:
		if (fname in t.username):
			continue
		outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags)))
		outputFile.flush()

def start(keywords, start_time):
	for k in keywords:
		print ('Getting keyword %s' % k)
		receiveBuffer(k,getTweet(k))
		elapsed_time = time.time() - start_time
		print ('elapsed_time for keyword: %s for time %s' % (k,time.strftime("%H:%M:%S",time.gmtime(elapsed_time))))
		print ('')
		
def start_thread(k):
	start_time = time.time()
	print ('Getting keyword %s' % k)
	d = datetime(2019,6,30)
	while (datetime(2015,1,01) < d):
		end = (d - timedelta(days=30)).strftime('%Y-%m-%d')
		start = d.strftime('%Y-%m-%d')
		receiveBuffer(k,getTweet(k, start, end))
		d = d - timedelta(days=31)

	elapsed_time = time.time() - start_time
	print ('elapsed_time for keyword: %s for time %s' % (k,time.strftime("%H:%M:%S",time.gmtime(elapsed_time))))
	print ('')


jpm_keywords=['gold','bank','silver','usbank','instrument','stock','bond']

start_time = time.time()
# Main Function
# start(jpm_keywords, start_time)

# myThread = threading.Thread(target=start_thread, args=jpm_keywords)
# myThread.daemon = True
# myThread.start()


threads = list()
for k in jpm_keywords:
    print ("Main    : create and start thread --- %s.", k)
    x = threading.Thread(target=start_thread, args=(k,))
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    print("Main    : before joining thread %d.", index)
    thread.join()
    print("Main    : thread %d done", index)
    print ('elapsed_time for keyword: %s for time %s' % ("END OF PROGRAM", time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))))



