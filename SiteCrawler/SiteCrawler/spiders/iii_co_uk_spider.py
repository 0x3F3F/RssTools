import scrapy
import datetime, time
import urllib
import re

# Descriptor: How pythons proprty type implemented ie get / set methods
class GetSpiderNameFromClassName:
	def __get__(self, instance, owner):
		"""
		Generate the spider name from the classname. Classes expected to have format _TICKR
		This TICKR is extracted and used to create the correct spider name
		"""
		className = owner.__name__
		tickerIndex = className.rfind("_") + 1
		return('iii_co_uk_' + className[tickerIndex:])


class GetStartUrlFromClassName:
	def __get__(self, instance, owner):
		"""
		Generate the iii start url from the classname. Classes expected to have format _TICKR
		This TICKR is extracted and used to create the correct start url for the forum in quesiton
		"""
		className = owner.__name__
		tickerIndex = className.rfind("_") + 1
		start_urls = ['http://www.iii.co.uk/investment/detail?code=cotn:'+className[tickerIndex:]+'.L&display=discussion'	]
		return start_urls


class GetCustomSettingsFromClassName:
	def __get__(self, instance, owner):
		"""
		Generate the scrapy custom settings  from the classname. Classes expected to have format _TICKR
		This TICKR is extracted and used to create the required custom setting values.
		"""
		className = owner.__name__
		tickerIndex = className.rfind("_") + 1
		ticker = className[tickerIndex:]

		custom_settings = {}
		custom_settings['RSS_TITLE'] = 'III Forum: '+ ticker
		custom_settings['RSS_LINK'] = 'http://www.iii.co.uk/investment/detail?code=cotn:'+ ticker +'.L&display=discussion'	
		custom_settings['RSS_OUTPUT_FILE'] = 'iii_co_uk_' + ticker + '.rss'
		return custom_settings



################################################################################
#
# Class:	iiiForumSpider
#
# Method:	Each iii spider should be derived from this parent class.
#			Derived classes inherit methods
#			Attributes scrapy requires are set with getters which reply on derived 
#			classes being named with an ending of _TICKER
#
# Note:		Going to use one spider for each iii forum page, instead of combining 
#			into 1 as each page has 40 entries and so the feed reader will have to 
#			remember at least that many items per feed. Could be problematic. 
#
################################################################################
class iiiForumSpider(scrapy.Spider):

	# Srapy wants these defined
	# Use descriptors (getter) so as can populate based on Class Name, expected to end with _TICKER
	# Derived classes will inherit and so won't need additional config providing named correctly.
	name = GetSpiderNameFromClassName()
	start_urls = GetStartUrlFromClassName()
	allowed_domains = ['http://www.iii.co.uk']

	# Custom settings that I can read in the pipeline & put in feed.
	# Again, use descriptor so as can populate based on derived Class Name. 
	custom_settings = GetCustomSettingsFromClassName()

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
	# pass as nothing to do.
	# Required attributes set via inherited getters which rely on class name ending _CLDN
	pass


# Capital Gearing Investment Trust Spider
class iiiForumSpider_CGT(iiiForumSpider):
	# pass as nothing to do.
	# Required attributes set via inherited getters which rely on class name ending _CGT
	pass



#  RIT Capital Partners Spider
class iiiForumSpider_RCP(iiiForumSpider):
	# pass as nothing to do.
	# Required attributes set via inherited getters which rely on class name ending _RCP
	pass



# Personal Assets Trust Spider
class iiiForumSpider_PNL(iiiForumSpider):
	# pass as nothing to do.
	# Required attributes set via inherited getters which rely on class name ending _PNL
	pass



# British Empire Trust Spider
class iiiForumSpider_BTEM(iiiForumSpider):
	# pass as nothing to do.
	# Required attributes set via inherited getters which rely on class name ending _BTEM
	pass

