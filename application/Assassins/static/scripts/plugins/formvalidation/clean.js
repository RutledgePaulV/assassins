define([
	'scripts/config/forbiddenWords',
	'formValidation'
], function(forbiddenWords, FormValidation){

	FormValidation.Validator.cleanLanguage = {
		validate: function (validator, $field) {
			var val = $field.val();
			return !forbiddenWords.test(val);
		}
	};

});