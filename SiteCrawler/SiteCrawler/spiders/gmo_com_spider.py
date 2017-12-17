import scrapy
import datetime, time



class GMOSpider(scrapy.Spider):
	name = "gmo_com"
	allowed_domains = ['https://www.gmo.com']
	start_urls = ['https://www.gmo.com', ]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {}
	custom_settings['RSS_TITLE'] = 'GMO Quarterly'
	custom_settings['RSS_LINK'] = start_urls[0]
	custom_settings['RSS_OUTPUT_FILE'] = name + '.rss'


	def CheckExtractedElements(self, title, link, descript):
		"""If scrape failed then lets flag it up in the feed.  Fixes relative link."""

		retTitle = "Prob Scrapting Title" if not title else title
		retLink = "Prob Scrapting Title" if not link else self.start_urls[0]+link
		retDesc = "Prob Scrapting Description" if not descript else descript

		return retTitle, retLink, retDesc



	def parse(self, response):
		"""Select page elements to pick for the generated xml element"""

		for viewRow in response.css('div.sf_3cols_1in_33'):

			# Note the guid is a unique descriptor, just repeat url
			# I've set the order here in FEED_EXPORT_FIELDS cfg variable
			title = viewRow.css('a::attr("title")').extract_first()		
			link = viewRow.css('a::attr("href")').extract_first()
			descript = viewRow.css('p::text').extract_first()
		
			validatedTitle, validatedLink, validatedDesc = self.CheckExtractedElements(title, link, descript)

			yield {
			'title': validatedTitle,
			'link': validatedLink,
			'guid' : validatedLink,
			'description': validatedDesc
			}

