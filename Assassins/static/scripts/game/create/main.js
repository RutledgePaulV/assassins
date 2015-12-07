define([
	'jquery', 'commands', 'formatter', 'scripts/config/valConfig',
	'scripts/config/imagePickerOptions',
	'scripts/game/create/wizard',
	'hbs!scripts/game/templates/image',

/**
 * Unreferenced MIDS
 */
	'formValidation',
	'bootstrap-datetimepicker',
	'bootstrap-select',
	'nested',
	'domReady!'
], function ($, commands, Formatter, valConfig,
             imagePickerOptions,
             wizard, imageTemplate) {


	var gridOptions = {
		minWidth: 160,
		gutter: 10,
		resizeToFit: true,
		resizeToFitOptions: {
			resizeAny: true
		}
	};


	var carousel, imageContainer;

	var advanceCarousel = function () {
		if (carousel) {
			carousel.carousel('next');
		}
	};

	var initPanel2 = function () {

		var formatted = new Formatter($('#zip')[0], {
			pattern: '{{99999}}',
			persistent: true
		});

		commands.QUERY_IMAGES.fire({size: 24}, function (data) {
			var imageMarkup = imageTemplate(data.result);
			imageContainer.html(imageMarkup);
		});

		$('#pane2').formValidation({
			framework: 'bootstrap',
			feedbackIcons: valConfig.ICONS,
			container: valConfig.CONTAINER,
			fields: {
				title: valConfig.GAME_TITLE,
				intro: valConfig.GAME_INTRO,
				address: valConfig.ADDRESS,
				state: valConfig.STATE,
				city: valConfig.CITY,
				zip: valConfig.ZIP
			},
			button: {
				selector: 'button.btn-next',
				disabled: 'disabled'
			}
		});

		$('.selectpicker').selectpicker();

	};

	var initPanel3 = function () {

		$('#config-form').formValidation({
			framework: 'bootstrap',
			feedbackIcons: valConfig.ICONS,
			container: valConfig.CONTAINER,
			fields: {
				startdate: valConfig.DATE_TIME_PICKER,
				maxplayers: valConfig.INTEGER
			},
			button: {
				selector: 'button.btn-next',
				disabled: 'disabled'
			}
		});

		var start = $('#start_date');
		var end = $("#end_date");

		var startDate = new Date();
		startDate.setMinutes(0);
		startDate.setHours(startDate.getHours() + 24);

		start.datetimepicker({useCurrent: false, minDate: startDate});

		end.datetimepicker({useCurrent: false});

		// start date should set the minimum date on the end date
		start.on("dp.change", function (e) {
			end.data("DateTimePicker").minDate(e.date);
		});

		// end date should set the maximum date on the start date
		end.on("dp.change", function (e) {
			start.data("DateTimePicker").maxDate(e.date);
		});

		start.on('dp.change dp.show', function (e) {
			$('#config-form').formValidation('revalidateField', 'startdate');
		});

		end.on('dp.change dp.show', function (e) {
			$('#config-form').formValidation('revalidateField', 'enddate');
		});

	};

	var initPanel4 = function () {
		$('button[data-pk]').click(function () {
			var pk = parseInt($(this).data('pk'));
			wizard.submit(pk);
		});

		$('button[data-target]').click(function() {
			var target = $(this).data('target');
			$(target).modal('show');
		});
	};


	// get a handle on the carousel div and instantiate the carousel
	carousel = $('#carousel');
	carousel.carousel('pause');

	// get a handle on the image container
	imageContainer = $('#image-container');

	initPanel2();
	initPanel3();
	initPanel4();

	$('#pane1-next').click(function () {
		advanceCarousel();
		imageContainer.nested(gridOptions);
	});

	$('#pane2-next').click(function () {
		wizard.submitFirstPanel();
		advanceCarousel();
	});

	$('#pane3-next').click(function () {
		wizard.submitSecondPanel();
		advanceCarousel();
	});


});