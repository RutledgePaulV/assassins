define([
	'jquery', 'scripts/config/valConfig',

/**
 * Unreferenced MIDS
 */
	'formValidation',
	'domReady!'
], function($, valConfig){

	$('#login-form').formValidation({
		framework: 'bootstrap',
		icons: valConfig.ICONS,
		container: valConfig.CONTAINER,
		fields: {
			login: valConfig.LOGIN_EMAIL,
			password: valConfig.LOGIN_PASSWORD
		}
	});

});