define([
	'jquery', 'commands',
	'scripts/utils/store'
], function ($, commands, Store) {

	var Wizard = {};

	var store = new Store('createWizard', {overwritesAllowed: false});

	var getWizardField = function (fieldName) {
		return $('input[name=' + fieldName + ']').val();
	};

	var submitPanel = function (fields, mixins) {
		for (var index in fields) {
			if (fields.hasOwnProperty(index)) {
				var field = fields[index];
				store.put(field, getWizardField(field));
			}
		}

		for (var key in mixins) {
			if (mixins.hasOwnProperty(key)) {
				store.put(key, mixins[key]);
			}
		}
	};

	Wizard.submitFirstPanel = function () {
		var fields = ['title', 'address', 'city', 'zip'];
		submitPanel(fields, {
			intro: $('#intro').val(),
			state: $('#state').val()
		});
	};

	Wizard.submitSecondPanel = function () {
		var fields = ['max_players'];
		submitPanel(fields, {
			start_date: (new Date($('#start_date').val()).toISOString())
		});
	};

	Wizard.submit = function (pk) {

		// get the pk from the rule set submit
		store.put('rules_pk', pk);

		var payload = store.payload();

		commands.CREATE_GAME.fire(payload, function (response) {
			// awesome, they successfully created a game.
			console.log(response);
		}, function (response) {
			// uh-oh. something failed
			var errors = response.errors;
		});
	};


	return Wizard;

});