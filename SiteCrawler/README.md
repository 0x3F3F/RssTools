# Site Crawler

This is a scrapy project that I developed to provide rss feeds for sites that don't offer them.

Each site I wish to scrape has its own individual spider, detailed in the `spiders` folder.  These are set up to look for css elements and 
pass them back to crawler engine where they are output as rss feeds.

The feeds are output to `output_feeds/<spidername>.rss` folder.  In my setup, the feeds are symlinked to the /var/www/ folder where my 
rss reader can pick them up.

The script `CrawlSites.sh` executes a `crawl` using each spider we wish to use.  This script is ran on a CRON.

More info [here](http://www.iainbenson.com/linux/2017/12/05/RssSiteCrawler.html)


