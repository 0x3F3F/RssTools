import scrapy
import datetime, time
from collections import namedtuple

# Structure to store our css in
CssItems = namedtuple('CssItems', ['LoopCss', 'TitleCss', 'LinkCss'])

class RufferSpider(scrapy.Spider):
	name = "Ruffer"
	allowed_domains = ['https://www.ruffer.co.uk']
	start_urls = [ ] # setup later

	# Store the Css elements we want for each url.  
	# EXAMPLE MORE COMPLICATED AS WAS GOING TO FETCH ITEMS FROM MUILTIPLE PAGES, but in end not.
	# HAck: Using http/https as 2 areas of that page we and to scrape, 2 dict entries.
	urlItemsDict = {}
	urlItemsDict['https://www.ruffer.co.uk/about/investment-review'] = CssItems('article.review','h2::text','a::attr("href")')	# Ruffer Coment
	#urlItemsDict['https://www.ruffer.co.uk/funds/ruffer-investment-company'] = CssItems('section.not-white','a::text','a::attr("href")') # Annual Report USE AIC INSTEAD
	#urlItemsDict['http://www.ruffer.co.uk/funds/ruffer-investment-company'] = CssItems('div.filters ul','li button::text','li button::attr("data-value")') # Monthly Reaport USE AIC INSTEAD

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {}
	custom_settings['RSS_TITLE'] = 'Ruffer Investment Trust'
	custom_settings['RSS_LINK'] = 'http://www.ruffer.co.uk'
	custom_settings['RSS_OUTPUT_FILE'] = name + '.rss'
 

	def __init__(self, name=None, **kwargs):

		# scrapy wants start_urls.  To avoid duplication, I'll populate here
		self.start_urls = list(self.urlItemsDict.keys()) 

		# Call original Init function.  Dont need to callm as just sets name and start_url
		#scrapy.Spider.__init__(self, name, kwargs)


	def GetCleanTitleLink(self, extractedTitle, extractedLink ):
		"""Checks titl/link for scrape error (None).  Adds domain to link. """

		if not extractedTitle:
			title = "RICA: Problem Extracting h2 text (title)"
		else:
			title = extractedTitle

		if not extractedLink:
			link = "Problem Extracting Link Href"
		else:
			# It's a relative link, so add the domain back in
			link = self.allowed_domains[0] + "/" + extractedLink

		return title, link


	def parse(self, response):
		"""Select page elements to pick for the generated xml element"""

		# Get the appropriate selectors, depending on the page we're scraping
		itemsSelector = self.urlItemsDict[response.url].LoopCss 
		titleSelector = self.urlItemsDict[response.url].TitleCss 
		linkSelector = self.urlItemsDict[response.url].LinkCss 

		for viewRow in response.css(itemsSelector):

			# I've set the order here in FEED_EXPORT_FIELDS cfg variable
			extractedTitle = viewRow.css(titleSelector).extract_first()		
			extractedLink = viewRow.css(linkSelector).extract_first()

			title, link = self.GetCleanTitleLink(extractedTitle, extractedLink )

			yield {
			'title': title,
			'link': link,
			'guid' : link,
			'description': self.name  + " " + title,
			}
