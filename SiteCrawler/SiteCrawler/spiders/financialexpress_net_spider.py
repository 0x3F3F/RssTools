import scrapy
import subprocess
import datetime, time


# This uses the site that theaic.co.uk uses to get IT reports
# Advantage is that everythin is in one place and I don't need to scrape multple sites
class InvestmentTrustRepsSpider(scrapy.Spider):
	name = "financialexpress_net"
	allowed_domains = ['http://webfund6.financialexpress.net']
	start_urls = []

	# Custom settings that I can read in the pipeline & put in feed.
	custom_settings = {}
	custom_settings['RSS_TITLE'] = 'Investment Trust Reports'
	custom_settings['RSS_LINK'] = 'http://www.theaic.co.uk'
	custom_settings['RSS_OUTPUT_FILE'] = name + '.rss'

	# Funds we're looking for.  Site needs ISIN code, but we'll display Ticker instead.
	isinMappings = {
			'GB0007366395':'RIT', 
			'GB00B018CS46':'RICA',
			'GB0006827546':'PNL',
			'GB0001738615':'CGT',
			'GB0007879835':'HANA',
			'GB0001335081':'BTEM',
			'GB0001216000':'CLDN',
			'GB0001639920':'HAST',
			'GB0007836132':'SST',
			'GB0000100767':'AAS',
			'GB00B3SXM832':'BRFI',
			'GG00B1W59J17':'AFMC',
			'GB0003450359':'JII',
			'GB0006048770':'ANII',
			'GB0000385517':'BIOG',
			'GB0004559349':'IBT',
			'GB0004148507':'PIN',
			'GB0003921052':'HGT',
			'GB0004228648':'HRI'
	}

	def __init__(self, name=None, **kwargs):

		# scrapy wants start_urls.  Generate here from our dictionary.
		for isin,fund in self.isinMappings.items():
			self.start_urls += ['http://webfund6.financialexpress.net/Clients/aic/documentPage.aspx?isincode='+isin]

		# Donm't need to Call original Init function, it just sets name/start_urls
		#scrapy.Spider.__init__(self, name=None, **kwargs)


	def getPubDate(self):
		"""Creates a RSS date/time"""
		pubDate = datetime.date.today().strftime("%d %B %Y")
		pubTime = time.strftime('%H:%M')
		return(pubDate + " " +  pubTime)



	def getRedirectUrl(self, sourceUrl):
		"""
		The LatestReport url uses a redirect and changes every day
		Useless for guid.  Get the actual url
		"""
		#Use curl as can just fetch headers
		# I=just headers, s=silent,F=follow redirect
		destUrl = subprocess.check_output(['curl','-LsI','-o','/dev/null','-w','%{url_effective}',sourceUrl])
		return destUrl



	def GetCleanTitleLink(self, response, extractedTitle, extractedLink ):
		"""Checks titl/link for scrape error (None), adds in Info to title"""

		# ISIN is the first parameter in the link.  This is out dict index.
		isinCode = response.url.split('=')[1]

		if not extractedTitle:
			title = isinCode + ": Problem Extracting link text (title)"
		else:
			title = self.isinMappings[isinCode] + ': ' + extractedTitle

		if not extractedLink:
			link = "Problem Extracting Link Href"
		else:
			link = extractedLink

		return title, link
		

	def parse(self, response):
		"""Select page elements to pick for the generated xml element"""

		for viewRow in response.css('tr'):

			# Extract our params.  Note couild be None if fails.
			extractedTitle =  viewRow.css('a::text').extract_first()		
			extractedLink = viewRow.css('a::attr("href")').extract_first()

			# Tydy up extracted params, check for failures etc
			title, link = self.GetCleanTitleLink( response, extractedTitle, extractedLink )

			if "Factsheet" in title:
				# Factsheets use redirects and it changes every day. get permanentlink for guid
				permUrl = self.getRedirectUrl(link)
			else:
				# Annual reps use permanent links
				permUrl = link

			# I've set the order here in FEED_EXPORT_FIELDS cfg variable
			yield {
			'title': title,
			'link': link,
			'guid' : permUrl,
			'description': title,
			}

