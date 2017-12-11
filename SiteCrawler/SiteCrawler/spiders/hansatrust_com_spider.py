import scrapy
import datetime, time

class HansaTrustSpider(scrapy.Spider):
	name = "hansatrust_com"
	allowed_domains = ['https://www.hansatrust.com']
	start_urls = ['http://www.hansatrust.com/shareholder-information/financial-and-investment-reporting', ]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {}
	custom_settings['RSS_TITLE'] = 'Hansa Trust'
	custom_settings['RSS_LINK'] = start_urls[0]
	custom_settings['RSS_OUTPUT_FILE'] = name + '.rss'
 
	def __init__(self):
		"""Need to initialise start_url as has current year in it""" 	
		now = datetime.datetime.now()
		self.start_urls[0] += "/year-" + str(now.year) + ".aspx"
		# Now call the original init function
		scrapy.Spider.__init__(self)

	def getPubDate(self):
		"""Creates a RSS date/time"""
		pubDate = datetime.date.today().strftime("%d %B %Y")
		pubTime = time.strftime('%H:%M')
		return(pubDate + " " +  pubTime)


	def parse(self, response):
		"""Select page elements to pick for the generated xml element"""

		for viewRow in response.css('div.report-background'):

			# I've set the order here in FEED_EXPORT_FIELDS cfg variable
			title = viewRow.css('a div.trust-icon::text').extract_first()		
			link = self.allowed_domains[0] + viewRow.css('a::attr("href")').extract_first()

			yield {
			'title': title,
			'link': link,
			'guid' : link,
			'description': self.name  + " " + title,
			}
		
		# Don't really casre about next page, but if I did then this might work:	
		#next_page = response.css('li.pager-next a::attr("href")').extract_first()
		#if next_page is not None:
		#	yield response.follow(next_page, self.parse)
