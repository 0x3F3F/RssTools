#!/bin/bash

# Debug cron:
# Redirects stdout/err to log
#exec &>/home/pi/Dev/RssTools/SiteCrawler/SiteCrawlerCron.log
# Shows command about to execute
#set -x

# Script failing from cron as scrapy not found, likely as bashrc not called. Following missing
export PATH=$PATH:/usr/local/bin

# cd into SiteCrawler project dir
cd /home/pi/Dev/RssTools/SiteCrawler

#################################################
# Detail Spiders and Status. ALPHABETICAL ORDER !
#################################################

# Spider: british-empire_co_uk_spider.py
# Output: british-empire_co_uk.rss
# Status: Not used as using financialexpress_net_spider.py instead 
#scrapy crawl british-empire_co_uk

# Spider: fincialexpressde_net_spider.py
# Output: fincialexpress_net.rss
# Status: Main Spider that fetches all IT Reports from theaic.so.uk data provider
scrapy crawl financialexpress_net

# Spider: hansatrust_com_spider.py
# Output: hansatrust_com.rss
# Status: Not used as using financialexpress_net_spider.py instead 
#scrapy crawl hansatrust_com

# Spider: iii_co_uk_XXX_spider.py
# Output: iii_co_uk_XXX.rss
# Status: Use diff spider for each forum.
scrapy crawl iii_co_uk_RCP

# Spider: patplc_co_uk_spider.py
# Output: patplc_co_uk.rss
# Status: Not used as using financialexpress_net_spider.py instead 
#scrapy crawl patplc_co_uk

# Spider: ruffer_co_uk_spider.py
# Output: ruffer_co_uk.rss
# Status:Only used for Ruffer Comment.  Monthly/Annual reprots from finanicalExpress_new_spider.py
scrapy crawl ruffer_co_uk

#########################################################################
# Note:
# Setup symlinks for desired feeds from web dir to feed output directory
# Can then just add the feesd into local feedreader, pointing to localhost
#
# Run this on a cron. RUN AS USER, NOT ROOT: crontab -u pi -e
##########################################################################



