import scrapy
import datetime, time
import urllib
import re

################################################################################
#
# Class:	iiiForumSpider
#
# Method:	Each iii spider should be derived from this parent class.
#			Derived classes inherit methods, not attributes which need to be set
#			scrapy wants some atributes set right at start eg name not in init
#
# Note:		Going to use one spider for each iii forum page, instead of combining 
#			into 1 as each page has 40 entries and so the feed reader will have to 
#			remember at least that many items per feed. Could be problematic. 
#
################################################################################
class iiiForumSpider(scrapy.Spider):
	# Srapy wants these defined
	name = ""	
	allowed_domains = ['']
	start_urls = ['']

	# Classes derived from this need to set these
	custom_settings = {}
	custom_settings['RSS_TITLE'] = ''
	custom_settings['RSS_LINK'] = ''
	custom_settings['RSS_OUTPUT_FILE'] = ''

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


	def GetDescription(self, extractedDescs):
		"""Fetch the description in desired form"""
		if extractedDescs:
			# Desc is list with muiltiple items.  Suspect <br> split these up instead of one
			# Add p tags. Brs don't appear to work in feedreader for newlines, need to use <p>
			descsWithTags = ["<p>"+ x +"</p>" for x in extractedDescs] 

			# Create our description
			description = "".join(descsWithTags)

			# Tidy up the output.  Bit hacky, but hey.
			description=description.replace("<p>\n</p>","" )
			description=description.replace("\n","" )
			description=description.replace("</p>","</p>\n" )
		else:
			description = "Failed to fetch description"

		return description


	def parse(self, response):
		"""Select page elements to pick for the generated xml element"""


		for viewRow in response.css('tr td.content.comment'):

			# Extract our params.  Note could be None if fails.
			extractedLinks = viewRow.css('div ul li a::attr("href")').extract()
			title,link = self.GetTitleAndLink(extractedLinks)

			extractedDescs =  viewRow.css('div div::text').extract()		
			desc = self.GetDescription(extractedDescs)

			# I've set the order here in FEED_EXPORT_FIELDS cfg variable
			yield {
			'title': title,
			'link': link,
			'guid' : link,
			'description': desc,
			}

# Caledonia Investment Trust Spider
class iiiForumSpider_CLDN(iiiForumSpider):

	# Need only change this
	tikr = 'CLDN'

	# Scrapy needs these defined here otherwise cant find spider
	# Tried in init fn via common code but didn't work.  Bugger.
	name ="iii_co_uk_" + tikr
	allowed_domains = ['http://www.iii.co.uk']
	start_urls = ['http://www.iii.co.uk/investment/detail?code=cotn:'+tikr+'.L&display=discussion'	]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {
				'RSS_TITLE':'III Forum: '+tikr,
				'RSS_LINK':start_urls[0],
				'RSS_OUTPUT_FILE':name +'.rss'
			}


# Capital Gearing Investment Trust Spider
class iiiForumSpider_CGT(iiiForumSpider):

	# Need only change this
	tikr = 'CGT'

	# Scrapy needs these defined here otherwise cant find spider
	# Tried in init fn via common code but didn't work.  Bugger.
	name ="iii_co_uk_" + tikr
	allowed_domains = ['http://www.iii.co.uk']
	start_urls = ['http://www.iii.co.uk/investment/detail?code=cotn:'+tikr+'.L&display=discussion'	]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {
				'RSS_TITLE':'III Forum: '+tikr,
				'RSS_LINK':'http://www.iii.co.uk',
				'RSS_OUTPUT_FILE':name +'.rss'
			}


#  RIT Capital Partners Spider
class iiiForumSpider_RCP(iiiForumSpider):

	# Need only change this
	tikr = 'RCP'

	# Scrapy needs these defined here otherwise cant find spider
	# Tried in init fn via common code but didn't work.  Bugger.
	name ="iii_co_uk_" + tikr
	allowed_domains = ['http://www.iii.co.uk']
	start_urls = ['http://www.iii.co.uk/investment/detail?code=cotn:'+tikr+'.L&display=discussion'	]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {
				'RSS_TITLE':'III Forum: '+tikr,
				'RSS_LINK':'http://www.iii.co.uk',
				'RSS_OUTPUT_FILE':name +'.rss'
			}


# Personal Assets Trust Spider
class iiiForumSpider_PNL(iiiForumSpider):

	# Need only change this
	tikr = 'PNL'

	# Scrapy needs these defined here otherwise cant find spider
	# Tried in init fn via common code but didn't work.  Bugger.
	name ="iii_co_uk_" + tikr
	allowed_domains = ['http://www.iii.co.uk']
	start_urls = ['http://www.iii.co.uk/investment/detail?code=cotn:'+tikr+'.L&display=discussion'	]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {
				'RSS_TITLE':'III Forum: '+tikr,
				'RSS_LINK':'http://www.iii.co.uk',
				'RSS_OUTPUT_FILE':name +'.rss'
			}



# British Empire Trust Spider
class iiiForumSpider_BTEM(iiiForumSpider):

	# Need only change this
	tikr = 'BTEM'

	# Scrapy needs these defined here otherwise cant find spider
	# Tried in init fn via common code but didn't work.  Bugger.
	name ="iii_co_uk_" + tikr
	allowed_domains = ['http://www.iii.co.uk']
	start_urls = ['http://www.iii.co.uk/investment/detail?code=cotn:'+tikr+'.L&display=discussion'	]

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {
				'RSS_TITLE':'III Forum: '+tikr,
				'RSS_LINK':'http://www.iii.co.uk',
				'RSS_OUTPUT_FILE':name +'.rss'
			}


