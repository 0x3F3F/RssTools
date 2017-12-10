#!/bin/bash

# cd into SiteCrawler project dir
cd /home/pi/Dev/RssTools/SiteCrawler

#################################################
# Detail Spiders and Status. ALPHABETICAL ORDER !
#################################################

# Spider: british-empire_co_uk_spider.py
# Output: BritishEmpire.rss
# Notes: Not used as 
#scrapy crawl BritishEmpire

# Spider: fincialexpressde_net_spider.py
# Output: InvestmentTrustReps.rss
# Notes: Main Spider that fetches all IT Reports from theaic.so.uk data provider
scrapy crawl InvestmentTrustReps

# Spider: hansatrust_com_spider.py
# Output: HansaTrust.rss
# Notes: Not used as using financialexpress_net_spider.py instead 
#scrapy crawl HansaTrust

# Spider: iii_co_uk_RCP_spider.py
# Output: HansaTrust.rss
# Notes: Use diff spider for each forum.
scrapy crawl iiiRCPForum

# Spider: patplc_co_uk_spider.py
# Output: PersonalAssets.rss
# Notes: Not used as using financialexpress_net_spider.py instead 
#scrapy crawl PersonalAssets

# Spider: ruffer_co_uk_spider.py
# Output: Ruffer.rss
# Notes:Only used for Ruffer Comment.  Monthly/Annual reprots from finanicalExpress_new_spider.py
scrapy crawl Ruffer

#########################################################################
# Note:
# Setup symlinks for desired feeds from web dir to feed output directory
# Can then just add the feesd into local feedreader, pointing to localhost
#
# Run this on a cron
##########################################################################



