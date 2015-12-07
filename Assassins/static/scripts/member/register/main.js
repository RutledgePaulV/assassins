define([
	'jquery', 'scripts/config/valConfig',

/**
 * Unreferenced MIDS
 */
	'formValidation',
	'domReady!'
], function ($, valConfig) {

	$('#registration-form').formValidation({
		framework: 'bootstrap',
		feedbackIcons: valConfig.ICONS,
		container: valConfig.CONTAINER,
		fields: {
			first_name: valConfig.FIRST_NAME,
			last_name: valConfig.LAST_NAME,
			email: valConfig.EMAIL,
			password1: valConfig.PASSWORD1,
			password2: valConfig.PASSWORD2
		}
	});

});