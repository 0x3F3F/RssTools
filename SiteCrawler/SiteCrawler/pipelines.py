# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from SiteCrawler.feedexport import RssXmlItemExporter 

class SitecrawlerPipeline(object):

	def __init__(self, settings):

		# Following items were set in spider using custom_setting dict.
		self.rss_title = settings.get("RSS_TITLE")
		self.rss_link = settings.get("RSS_LINK")
		self.rss_output_file = "output_feeds/" + settings.get("RSS_OUTPUT_FILE")

		# Setting for the exporter.  These are comings from gloabal settings.py
		exporterSettings = 	{}
		exporterSettings['fields_to_export'] = settings.get("FEED_EXPORT_FIELDS")
		exporterSettings['indent'] = settings.get("FEED_EXPORT_INDENT")
		exporterSettings['encoding'] = 'utf-8'
		#exporterSettings['export_empty_fields'] = False 
		#exporterSettings['item_element'] = 
		#exporterSettings['root_element'] = 
		
		# Open the rss file for writing 
		self.file = open(self.rss_output_file,"wb")	# Overwrites existing

		# Now setup the exporter to be used.  Can pass params separately, but I'm using dict.
		self.exporter = RssXmlItemExporter(self.file, **exporterSettings)

		# Useful to know how to tie signals to functions.  open/close_spider automatically setup
		# dispatcher.connect(self.SpiderOpenFunc, signals.spider_opened)
		# dispatcher.connect(self.SpiderCloseFunc, signals.spider_closed)


	@classmethod
	def from_crawler(cls, crawler):
		"""
		This function changes how the crawler engine calls the pipeline __init__ function
		The additional parameters are added.  Therefore need to update init above to include extra param(s)
		This allows access to global settings (settings.py) and custom setting from within spider
		"""
		settings = crawler.settings
		return cls(settings)
	
	def open_spider(self, spider):
		"""Use custom functions I defined that add rss and channel tags"""
		self.exporter.start_exporting_rss(self.rss_title, self.rss_link);

	def close_spider(self, spider):
		"""USe custom function that closes the new rss and channel tags"""
		self.exporter.finish_exporting_rss();
		self.file.close()

	def process_item(self, item, spider):
		"""Unchanged to what was here before"""
		self.exporter.export_item(item)
		return item

