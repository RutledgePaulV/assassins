define([
	'jquery',
	'commands',
/**
 * Unreferenced MIDS
 */
	'slick',
	'domReady!'
], function ($, commands) {

	$('.rotator').slick({
		centerMode: true,
		centerPadding: '60px',
		slidesToShow: 3,
		dots: true,
		adaptiveHeight: true,
		infinite: true
	});


	$('.js-complete').click(function () {
		var button = $(this);
		var pk = $(this).data('assignment');
		var payload = {assignment: pk, verdict: true};

		commands.ASSIGNMENT_REPORT_STATUS.fire(payload, function () {
			button.replaceWith('<span class="alert alert-info">Verdict Submitted!</span>');
		}, function () {
			alert('Something went wrong!');
		});
	});

});