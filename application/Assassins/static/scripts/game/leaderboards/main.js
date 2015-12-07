define([
	'jquery',

/**
 * Unreferenced MIDS
 */
	'nested',
	'scripts/game/shared/affix',
	'domReady!'
], function ($) {


	var gridOptions = {
		animate: true,
		minWidth: 160,
		gutter: 10,
		resizeToFit: true,
		resizeToFitOptions: {
			resizeAny: true
		}
	};

	var playerResultsContainer = $('#player-results');

	playerResultsContainer.nested(gridOptions);


});
