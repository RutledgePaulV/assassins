/**
 * This module is a FormValidation custom validator that validates that
 * at least one of a set of inputs has a value.
 */
define([
	'formValidation'
], function (FormValidation) {

	FormValidation.Validator.linked = {

		otherFields: [],
		validatorInstance: null,

		init: function (thisArg, $field, options) {

			for (var field in options.fields) {
				if (options.fields.hasOwnProperty(field)) {
					this.otherFields.push({field: field, validators: options.fields[field]})
				}
			}

		},

		validate: function (validator, $field) {

			if ($field.is(":checked")) {
				return this.otherFields.every(function (fieldDescriptor) {

					var fieldName = fieldDescriptor.field;
					var allValidatorsAreValid = true;

					for (var key in fieldDescriptor.validators) {

						if(fieldDescriptor.validators.hasOwnProperty(key)) {

							var validatorName = fieldDescriptor.validators[key];

							var isEnabled = validator.getOptions(fieldName, validatorName, 'enabled');

							if (!isEnabled) {
								validator.enableFieldValidators(fieldName, true, validatorName);
							}

							var isValid = validator.isValidField(fieldName);

							if(isValid === null) {
								validator.validateField(fieldName);
								isValid = validator.isValidField(fieldName);
							}

							allValidatorsAreValid = allValidatorsAreValid && isValid;

							validator.enableFieldValidators(fieldName, isEnabled, validatorName);
						}
					}

					return allValidatorsAreValid;
				});
			}

			return true;
		}

	};

});