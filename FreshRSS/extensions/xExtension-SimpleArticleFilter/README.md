# SimpleArticleFilter extension

A FreshRSS extension which give ability to filter articles based on a json configuration file.

To use it, upload this directory in your `./extensions` directory and enable it on the extension panel in FreshRSS. 

A user specific json file needs to be created in the script folder which details the sites to be filtered. The filename should contain the users id.  An example setup is given.  
Note that:

## 'site' parameter
Descriptor for the entry, but not used.  Originally intended this to determine if fikter spevified, but some rss links did't contain the site

## feedId parameter
This is used to determine the feed where the filters eill apply.
It can be ascertained by selrvting a feed and looking at the number in the url 

## 'default' parameter
When set to 'hide', the script will hide all entries unless a word in 'filters' is present in the title or content.
When set to 'show', the script will show all entries unless a word in 'filters' is present in the title or content.


