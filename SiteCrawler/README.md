# Site Crawler

This is a scrapy project that I developed to provide RSS Feeds for sites that don't offer them.

Each site I wish to scrape has its own individual spider, detailed in the `spiders` folder.  These are set up to look for css elements and 
pass back data to crawler engine where it is processed and output as RSS Feeds.

The feeds are output to `output_feeds/<spidername>.rss` folder.  In my setup, the feeds are symlinked from the `/var/www/` folder where my 
RSS Reader can pick them up.

The script `CrawlSites.sh` executes a crawl using each spider we wish to use, it lists all available spiders in alphabetical order along 
with their status. This script is ran on a CRON, executed as the user (`crontab -u pi -e`) 

More info [here](http://www.iainbenson.com/linux/2017/12/05/RssSiteCrawler.html)


