define([
	'jquery',
/**
 * Unreferenced MIDS
 */
	'bootstrap',
	'domReady!'
], function ($) {


	var affix = $('#game-menu').affix({
		offset: {

			// we need to set the boundary for where the transition between affixed-top and affixed occurs.
			// we choose to values such that the transition appears seamless to the user
			top: function () {
				var selector = $('#cover-photo');
				if(selector.length){
					this.top = selector.outerHeight(true) - selector.offset().top;
				} else {
					this.top = 0;
				}
				return this.top;
			},

			// theoretically, we should never hit this if content is longer than the menu.
			bottom: function () {
				return (this.bottom = $('#footer').outerHeight(true));
			}
		}
	}).on('affix.bs.affix', function (e) {

		// once we drop far enough we need to shift the main contents over
		var oneSixth = 1 / 6.0 * 100;
		$('#content-section').css({'margin-left': oneSixth + "%"});


	}).on('affix-top.bs.affix', function (e) {

		// if we go back up into the affixed-top section, we need to remove the margin again
		$('#content-section').css({'margin-left': 0});

	});

});