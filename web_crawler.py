import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import json
import sys



def main():
	if (len(sys.argv) < 2):
		print("Usage: python3 web_crawler.py '2015-06-01'")
		print("Max range 1 year")
		return


	# {"username": username, "ts": time, "retweets": retweets, "likes": likes, "tweet_text": tweet_text}
	def write_to_file(data):
		f = open("data/twitter_jpm_" + sys.argv[1] + ".tsv","a+")
		print("Writing to file", len(data))
		for tweet_id in data.keys():
			f.write(str(tweet_id) + "\t" + str(data[tweet_id]) + "\n")
		f.close()

	earliest_time = -1
	start_date_str = sys.argv[1]
	start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
	end_date = start_date + datetime.timedelta(days=365)
	end_date_str = end_date.strftime('%Y-%m-%d')
	start_date_unix = time.mktime(start_date.timetuple())

	url = 'https://twitter.com/search?q=jp%20morgan%20since%3A' + start_date_str + '%20until%3A' + end_date_str +'&src=typd&lang=en'
	print(url)
	MAX_SCROLLS = 50

	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome('/Users/linna/Development/chromedriver', chrome_options=chrome_options)
	driver.get(url)

	while(earliest_time < 0 or start_date_unix < earliest_time):
		#This code will scroll down to the end
		for i in range(MAX_SCROLLS):	
			# Action scroll down
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			print(str(i) + " Scrolling...")
			time.sleep(3)

		print("DONE SCROLLING!")

		tweets_unique = {}

		response = driver.page_source

		start_date = earliest_time
		end_date = start_date + datetime.timedelta(days=365)
		end_date_str = end_date.strftime('%Y-%m-%d')
		start_date_unix = time.mktime(start_date.timetuple())

		url = 'https://twitter.com/search?q=jp%20morgan%20since%3A' + start_date_str + '%20until%3A' + end_date_str +'&src=typd&lang=en'
		print(url)
		driver = webdriver.Chrome('/Users/linna/Development/chromedriver', chrome_options=chrome_options)
		driver.get(url)


		soup = BeautifulSoup(response, "html.parser")
		# print(soup)
		tweets_raw = soup.findAll('div', {"class": "tweet"})

		print("Size:", len(tweets_raw))
		for tweet_raw in tweets_raw:
			tweet_text = tweet_raw.find('p', {'class': 'tweet-text'}).text
			if ("jp morgan" in tweet_text.lower()):
				tweet_text = tweet_text.replace('\n', ' ').replace('\t', ' ')
				data_tweet_id = tweet_raw.attrs['data-tweet-id']
				time_div = tweet_raw.find('span', {'class': '_timestamp'}).attrs['data-time-ms']
				username = tweet_raw.find('span', {'class': 'username'}).find("b").text
				retweets = tweet_raw.find('div', {'class': 'ProfileTweet-action--retweet'}).find('span', {'class': 'ProfileTweet-actionCountForPresentation'}).text
				likes = tweet_raw.find('div', {'class': 'ProfileTweet-action--favorite'}).find('span', {'class': 'ProfileTweet-actionCountForPresentation'}).text
				earliest_time = int(time_div)/1000
				print(earliest_time, datetime.datetime.utcfromtimestamp(earliest_time))
				tweets_unique[data_tweet_id] = str(username)+"\t"+str(datetime.datetime.utcfromtimestamp(earliest_time))+"\t"+str(retweets)+"\t"+str(likes)+"\t"+str(tweet_text)
				
				# print("ID:", data_tweet_id)
				# print(time_div, datetime.datetime.utcfromtimestamp(int(time_div)/1000))
				# print("u", username, "retweets:", retweets, "likes:", likes, "tweet", tweet_text)
				# print()
				# print('-----')
			# else:
			# 	print("tweet has no jpm:", tweet_text)
			# 	print('-----')

		print("after filter count:", len(tweets_unique), "scraped count:", len(tweets_raw))
		print("Latest time unix", earliest_time, datetime.datetime.utcfromtimestamp(earliest_time))
		write_to_file(tweets_unique)


if __name__== "__main__":
	main()
