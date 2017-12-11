import scrapy
import datetime, time

# TODO: Add in processing for Annual Reports
class BritishEmpireSpider(scrapy.Spider):
	name = "british-empire_co_uk"
	allowed_domains = ['https://www.british-empire.co.uk']
	start_urls = ['https://www.british-empire.co.uk/commentary-updates/monthly-newsletters', ]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {}
	custom_settings['RSS_TITLE'] = 'British Empire Trust'
	custom_settings['RSS_LINK'] = start_urls[0]
	custom_settings['RSS_OUTPUT_FILE'] = name + '.rss'
 
	def getPubDate(self):
		"""Creates a RSS date/time"""
		pubDate = datetime.date.today().strftime("%d %B %Y")
		pubTime = time.strftime('%H:%M')
		return(pubDate + " " +  pubTime)


	def parse(self, response):
		"""Select page elements to pick for the generated xml element"""

		for viewRow in response.css('article.comment'):

			# I've set the order here in FEED_EXPORT_FIELDS cfg variable
			title = viewRow.css('h1::text').extract_first()		
			link = viewRow.css('a::attr("href")').extract_first()

			yield {
			'title': title,
			'link': link,
			'guid' : link,
			'description': self.name  + " " + title,
			}
		
