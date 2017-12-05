from scrapy.exporters import XmlItemExporter 

# The default feedexporter is missing <rss> and <channel> tags from the xml
# Looking at scrapy/exporters.py/XmlItemExporter it appeared clear where the tag should go
# Create subclas of XmlItemExporter Override the default XmlItemExporter and update cfg FEED_EXPORTERS to use this instead
class RssXmlItemExporter(XmlItemExporter):

	# Apparently not essential to define, as takes from parent class
	# Doing so just in case I want to add more into to it
	def __init__(self, file, **kwargs):
		XmlItemExporter.__init__(self, file, **kwargs)

	def start_exporting_rss(self, rss_title, rss_link):
		"""
		Adds opening tags, including channel and rss
		Additionall adds a title and link to teh feed.
		"""
		self.xg.startDocument()

		# IRB MYsuff
		self.xg.startElement("rss", {'version':'2.0'})
		self._beautify_newline(new_item=True)
		self.xg.startElement("channel", {})
		self._beautify_newline(new_item=True)
		self._export_xml_field('title',rss_title,1)
		self._export_xml_field('link',rss_link,1)
		# End Mysuff
		
		self.xg.startElement(self.root_element, {})
		self._beautify_newline(new_item=True)

		#print(self.__dict__)


	def finish_exporting_rss(self):
		"""Closes off my custom rss and channel tags"""
		self.xg.endElement(self.root_element)

		# IRB MYsuff
		self._beautify_newline(new_item=True)
		self.xg.endElement("channel")
		self._beautify_newline(new_item=True)
		self.xg.endElement("rss")
		# End Mysuff

		self.xg.endDocument()

