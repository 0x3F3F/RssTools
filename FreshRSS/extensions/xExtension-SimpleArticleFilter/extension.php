<?php 

// Performs a very simple filtering operation on rss feeds.
// configuration is stored in per user config filter, see example file for details.
// Setting 'default' to 'show' shows all articles EXCEPT if the defines words appear in article
// Setting 'default' to 'hide' hides all articles EXCEPT if the defines words appear in article
class SimpleArticleFilterExtension extends Minz_Extension {
	public function init() {
		$this->registerHook('entry_before_insert', array($this, 'checkForStrings'));

		// Was using this one for debug.  Doesn't store in Db.  
		// It leaves the count unmodified - nice to see how many skipped.... 
		//$this->registerHook('entry_before_display', array($this, 'checkForStrings'));
	}

	public function checkForStrings($entry) {
		// $entry is FreshRSS_Entry object
		// Accessible fields:
		// title, author, content, link, date, is_read, is_favourite, feed

		// Get json settings filename
		// Each user can have their own json file: "DefinedFilters.User.json"
		$current_user = Minz_Session::param('currentUser');
		$filename =  'DefinedFilters.'.$current_user.'.json';
		$filepath = join_path($this->getPath(), $filename);

		// Read the json file
		$jsonString = file_get_contents($filepath);
		$filterSettings = json_decode($jsonString);

		// Get the site settings if defined for this site
		$filterExists = false;
		foreach($filterSettings as $filterEntry)
		{
			// Unable to use the url as some rss feeds don't have it or are shared across many feeds ie twitter
			// Instead use feed id which is unique, whech can be read from url eg f_8
			if (strpos($entry->feed(), $filterEntry->feedId) !== false)
			{
				$filterExists = true;

				$site = $filterEntry->site;
				$default = $filterEntry->default;
				$filters = $filterEntry->filters;
			}
		}

		//Got a filter, so do the processing
		if($filterExists)
		{
			// Combine title and content, so only doing one search
			$titlePlusContent = $entry->content().$entry->title(); 

			// Are any of our keywords in the title or body
			$filterMatch = false;
			foreach( $filters as $filter)
			{
				//Check. Case insensitive
				if ( stripos($titlePlusContent, $filter) !== false)
				{
					$filterMatch = true;
					break;
				}
			}

			// Test for the scenarios where we wish to hide entry:
			// i)  Where default is to hide, and we didn't find one of the filters
			// ii) Where teh default action is to show, but we found one of our filters
			if(($default==="hide" && !$filterMatch) || ($default==="show" && $filterMatch))
			{
				// Don't return entry.  Has effect of hiding.
				// poss could set is_read, but doesn't work for entry_before_display hook
				return;
			}
		}

		return $entry;

	}// End checkForStrings
}//End Class
