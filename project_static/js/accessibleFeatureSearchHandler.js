/* Search and Theme Filtering - Text Only */

/* Prevent the page refreshing when the user presses the enter key */

$("form").on('submit',function(e){
    e.preventDefault();
});

/* Clear the search bar and results on focus */

$('#map_search').focus(function(e) {
	$(this).val('');
	if (MmtFeatureList.allSites == false) {
		$('.feature_list').empty();
		MmtFeatureList.populateList(MmtFeatureList.listUrl, {page: 1});
		$('.results_title').html('Place Index');
		MmtFeatureList.allSites = true;
	}
});

$('#map_search').keyup(function(e) {
	let search_string = $(this)[0].value;
	
	if (search_string == '') {
		// do nothing
	} else if (search_string.length >= 4) {
		let url = MmtFeatureList.searchUrl;
		$('.feature_list').empty();
		MmtFeatureList.populateList(url, {page: 1, q: search_string});
		$('.results_title').html('Search Results for "' + search_string + '"');
		MmtFeatureList.allSites = false;
	}
});


/* Theme filtering */

$('.theme').click(function(e) {
	e.preventDefault();
	themeId = $(this).data('key');
	theme = $(this).html();

	if (themeId == undefined) {
		$('.feature_list').empty();
		MmtFeatureList.populateList(MmtFeatureList.listUrl, {page: 1});
		$('.results_title').html('Place Index');
		MmtFeatureList.allSites = true;
	} else {
		$('.feature_list').empty();
		url = MmtFeatureList.themeUrl;
		MmtFeatureList.populateList(url, {theme: themeId, page: 1});
		$('.results_title').html('Places in Theme ' + theme);
		MmtFeatureList.allSites = false;
	}
});

/* Tag filtering */

$('.tag').click(function(e) {
	e.preventDefault();
	tag = $(this).data('tag');
	if (tag == undefined) {
		$('.feature_list').empty();
		MmtFeatureList.populateList(MmtFeatureList.listUrl, {page: 1});
		$('.results_title').html('Place Index');
		MmtFeatureList.allSites = true;
	} else {
		$('.feature_list').empty();
		url = MmtFeatureList.tagUrl;
		MmtFeatureList.populateList(url, {tags: tag, page: 1});
		$('.results_title').html('Places Tagged "' + tag + '"');
		MmtFeatureList.allSites = false;
	}
});