import scrapy
import datetime, time
import urllib
import re

# IMPORTANT:
# Going to use one spider for each iii forum page, instead of combining into 1
# Each page has 40 entries and so teh feed reader ill have to remember at least that many items.
# FreshRss was set to 60 or so, so would hit problems if have multiple forum pages in one spider
class iiiRCPForumSpider(scrapy.Spider):
	name = "iiiRCPForum"
	allowed_domains = ['http://www.iii.co.uk']
	start_urls = [
			'http://www.iii.co.uk/investment/detail?code=cotn:RCP.L&display=discussion'
	]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {}
	custom_settings['RSS_TITLE'] = 'III RCP Forum'
	custom_settings['RSS_LINK'] = 'http://www.iii.co.uk'
	custom_settings['RSS_OUTPUT_FILE'] = 'iiiRCPForum.rss'


	def getPubDate(self):
		"""Creates a RSS date/time"""
		pubDate = datetime.date.today().strftime("%d %B %Y")
		pubTime = time.strftime('%H:%M')
		return(pubDate + " " +  pubTime)



	def GetTitleAndLink(self, extractedLinks):
		"""Creates a title and link from the list of links grepped from the page"""

		#This link had Ticker and subject in it.  We'll extract them
		if extractedLinks[1]:
			titleInfo = urllib.parse.unquote(extractedLinks[1])
			matches = re.findall("code=cotn:(.*?)\.L.*subject=(.*?)\&", titleInfo)
			ticker, threadTitle = matches[0]
			title = ticker + " - " + threadTitle
		else:
			title = "failed to fetch link that has title"

		if extractedLinks[0]:
			link = self.allowed_domains[0] + extractedLinks[0]
		else:
			link = "Failed to fetch link"
		
		return title, link


	def parse(self, response):
		"""Select page elements to pick for the generated xml element"""

		pubDateTime = self.getPubDate()

		for viewRow in response.css('tr td.content.comment'):

			# Extract our params.  Note could be None if fails.
			extractedLinks = viewRow.css('div ul li a::attr("href")').extract()
			title,link = self.GetTitleAndLink(extractedLinks)

			# Desc is list with muiltiple items.  Suspect <br> split these up instead of one
			extractedDescs =  viewRow.css('div div::text').extract()		
			if extractedDescs:
				desc = "".join(extractedDescs)
			else:
				desc = "Failed to fetch description"

			# I've set the order here in FEED_EXPORT_FIELDS cfg variable
			yield {
			'title': title,
			'link': link,
			'guid' : link,
			'pubDate' : pubDateTime,
			'description': desc,
			}

