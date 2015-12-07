define([
	'jquery',
	'commands',
	'formatter',
	'scripts/config/valConfig',

/**
 * Unreferenced MIDS
 */
	'formValidation',
	'domReady!'
], function ($, commands, Formatter, valConfig) {

	var formatted = new Formatter($('#phone')[0], {
		pattern: '{{999}}-{{999}}-{{9999}}',
		persistent: true
	});


	var phonePreferenceValidator = function (e, data) {
		var otherField = 'phone';
		var toggleValidator = 'notEmpty';
		var enableOrDisable = $(data.element).is(':checked');

		data.fv.enableFieldValidators(otherField, enableOrDisable, toggleValidator);
		if (!data.fv.isValidField(otherField)) {
			data.fv.revalidateField(otherField);
		}
	};

	$('#account-form').formValidation({
		framework: 'bootstrap',
		feedbackIcons: valConfig.ICONS,
		container: valConfig.CONTAINER,
		fields: {
			first_name: valConfig.FIRST_NAME,
			last_name: valConfig.LAST_NAME,
			email: valConfig.EMAIL
		}
	});

	$('#profile-form').formValidation({
		framework: 'bootstrap',
		feedbackIcons: valConfig.ICONS,
		container: valConfig.CONTAINER,
		fields: {
			phone: valConfig.PHONE,
			slogan: valConfig.SLOGAN,
			biography: valConfig.BIOGRAPHY,
			'phone-preference': {
				onSuccess: phonePreferenceValidator
			}
		}
	});

	$('#password-form').formValidation({
		framework: 'bootstrap',
		feedbackIcons: valConfig.ICONS,
		container: valConfig.CONTAINER,
		fields: {
			password: valConfig.CURRENT_PASSWORD,
			password1: valConfig.PASSWORD1,
			password2: valConfig.PASSWORD2
		}
	});

	function getAccountInfo() {
		return {
			first_name: $('#first_name').val(),
			last_name: $('#last_name').val(),
			email: $('#email').val()
		}
	}

	$('#submit-account').click(function () {
		var data = getAccountInfo();
		commands.UPDATE_MEMBER_INFO.fire(data, function (data) {
			// show some green for success
			alert(data.message);
		}, function (data) {
			// show some red for errors
			alert(data.errors);
		});
	});

	function getProfileInfo() {
		return {
			phone: $('#phone').val(),
			slogan: $('#slogan').val(),
			biography: $('#biography').val(),
			image: $('#image')[0].files[0],
			should_email: '' + $('#email-preference').is(':checked'),
			should_text: '' + $('#phone-preference').is(':checked')
		}
	}

	$('#submit-profile').click(function () {
		var data = getProfileInfo();
		commands.UPDATE_MEMBER_PROFILE.fire(data, function (data) {
			// show some green for success
			alert(data.message);
		}, function (data) {
			// show some red for failure
			alert(data.error);
		});
	});

	function getPasswordInfo() {
		return {
			password: $('#password').val(),
			password1: $('#password1').val(),
			password2: $('#password2').val()
		};
	}

	$('#submit-password').click(function () {
		var data = getPasswordInfo();
		commands.CHANGE_MEMBER_PASSWORD.fire(data, function (data) {
			alert(data.message);
		}, function (data) {
			alert(data.error);
		});
	});

});
