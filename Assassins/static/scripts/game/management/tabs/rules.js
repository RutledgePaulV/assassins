define([
	'jquery',
	'redactor',
	'scripts/plugins/redactor/saveButton',
/**
 * Unreferenced MIDS
 */
	'domReady!'
], function($, saveButton) {

	var redactorContainer = $('#rules-textarea');

	redactorContainer.redactor({
		plugins: [saveButton],
		buttonSource: true
	});

});