import scrapy
import datetime, time

# TODO: Add in processing for Annual Reports
class RufferSpider(scrapy.Spider):
	name = "Ruffer"
	allowed_domains = ['https://www.ruffer.co.uk']
	start_urls = ['https://www.ruffer.co.uk/about/investment-review', ]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {}
	custom_settings['RSS_TITLE'] = 'Ruffer Investment Trust'
	custom_settings['RSS_LINK'] = start_urls[0]
	custom_settings['RSS_OUTPUT_FILE'] = name + '.rss'
 
	def getPubDate(self):
		"""Creates a RSS date/time"""
		pubDate = datetime.date.today().strftime("%d %B %Y")
		pubTime = time.strftime('%H:%M')
		return(pubDate + " " +  pubTime)


	def parse(self, response):
		"""Select page elements to pick for the generated xml element"""

		for viewRow in response.css('article.review'):

			# I've set the order here in FEED_EXPORT_FIELDS cfg variable
			title = viewRow.css('h2::text').extract_first()		
			link = self.allowed_domains[0]+"/"+viewRow.css('a::attr("href")').extract_first()
			pubDateTime = self.getPubDate()

			yield {
			'title': title,
			'link': link,
			'guid' : link,
			'pubDate' : pubDateTime,
			'description': self.name  + " " + title,
			}
		
		# Don't really casre about next page, but if I did then this might work:	
		#next_page = response.css('li.pager-next a::attr("href")').extract_first()
		#if next_page is not None:
		#	yield response.follow(next_page, self.parse)
