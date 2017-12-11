import scrapy
import datetime, time

# got error stating service_identity cannot import opentype, despite it and pyasn1 being installed
# RUNNING THE following, I noted scrapy was using python 3 and not 2
# scrapy version -v
# Ithen installed it via pip3 install 'service_identity' and it worked!


class PersonalAssetsSpider(scrapy.Spider):
	name = "PersonalAssets"
	allowed_domains = ['https://patplc.co.uk']
	start_urls = ['https://patplc.co.uk//literature/quarterly-reports', ]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {}
	custom_settings['RSS_TITLE'] = 'Personal Assets Trust'
	custom_settings['RSS_LINK'] = start_urls[0]
	custom_settings['RSS_OUTPUT_FILE'] = 'PersonalAssets.rss'

	def getPubDate(self):
		"""Creates a RSS date/time"""
		pubDate = datetime.date.today().strftime("%d %B %Y")
		pubTime = time.strftime('%H:%M')
		return(pubDate + " " +  pubTime)


	def parse(self, response):
		"""Select page elements to pick for the generated xml element"""

		# Best Methed:
		# Curl page onto localhost for dev
		# run 'scrapy shell http://127.0.0.1/test.html'
		# Can then experiment: response.css('li.views-row a::attr(title)') 
		# dot to specify class.  Space separated sub elements
		for viewRow in response.css('li.views-row'):

			# Note the guid is a unique descriptor, just repeat url
			# I've set the order here in FEED_EXPORT_FIELDS cfg variable
			title = viewRow.css('a::attr("title")').extract_first()		
			link = viewRow.css('a::attr("href")').extract_first()

			yield {
			'title': title,
			'link': link,
			'guid' : link,
			'description': "Personal Assets "+title,
			}
		
		# Don't really casre about next page, but if I did then this might work:	
		#next_page = response.css('li.pager-next a::attr("href")').extract_first()
		#if next_page is not None:
		#	yield response.follow(next_page, self.parse)
