define([
	'jquery', 'context',
	'scripts/plugins/redactor/plugin',
	'commands'
], function ($, context, RegisterPlugin, commands) {

	return RegisterPlugin('save', {

		init: function () {
			var button = this.button.add('save-button', 'Save');
			this.button.addCallback(button, this.save.save);
		},

		save: function () {
			var html = this.code.get();
			commands.UPDATE_GAME_RULES.fire({
				pk: context.game,
				html: html
			});
		}

	});
	
});