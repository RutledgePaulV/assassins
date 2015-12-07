define([
	'jquery', 'commands',
	'scripts/utils/meta',
	'formValidation'
], function ($, commands, MetaUtils, FormValidation) {

	var timerKey = 'bv.command.timer';

	FormValidation.Validator.command = {

		commandQuery: null,

		init: function(thisArg, $field, options){
			this.commandQuery = MetaUtils.memoize(function(value){
				return options.query(value, commands);
			});
		},

		destroy: function (validator, $field, options) {
			var timer = $field.data(timerKey);
			if (timer) {
				clearTimeout(timer);
				$field.removeData(timerKey);
			}
		},

		validate: function (validator, $field, options) {
			var value = $field.val();
			var dfd = new $.Deferred();

			if (value === '') {
				dfd.resolve($field, 'command', {valid: true});
				return dfd;
			}

			var that = this;

			function runQuery() {
				var xhr = that.commandQuery(value);

				xhr.then(function (response) {
					var valid = response.result.valid;
					var message = response.result.message;
					dfd.resolve($field, 'command', {valid: valid, message: message});
				});

				dfd.fail(function () {
					xhr.abort();
				});

				return dfd;
			}

			if (options.delay) {
				this.destroy(null, $field, options);
				$field.data(timerKey, setTimeout(runQuery, options.delay));
				return dfd;
			} else {
				return runQuery();
			}
		}
	};

	return $;
});