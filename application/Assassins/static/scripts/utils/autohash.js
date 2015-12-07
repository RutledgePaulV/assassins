define([
	'jquery',

/**
 * Unreferenced MIDS
 */
	'domReady!'
], function ($) {

	/**
	 * Initiate any tabs on the page
	 */
	$('.tab-nav').find('a').click(function (e) {
		e.preventDefault();
		$(this).tab('show');
		location.hash = $(this).attr('href');
	});


	/**
	 * Try to switch to a tab represented by the hash on the url
	 */
	if (window && window.location && window.location.hash) {
		var activeTab = $('a[href=' + window.location.hash + ']');
		if (activeTab) {
			activeTab.tab('show');
		}
	}

});