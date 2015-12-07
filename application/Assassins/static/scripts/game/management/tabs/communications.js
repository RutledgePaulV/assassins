define([
	'jquery',
	'commands',
	'context',
/**
 * Unreferenced MIDS
 */
	'domReady!',
	'scripts/social/fb'
], function ($, commands, context) {

	var postNotificationButton = $('#post-notification');

	postNotificationButton.click(function () {
		var subject = $('#subject').val();
		var value = $('#notification').val();
		var send_email = $('#send-email').is(':checked');
		var send_text = $('#send-texts').is(':checked');

		commands.POST_NOTIFICATION.fire({
			pk: context.game,
			subject: subject,
			contents: value,
			send_email: send_email,
			send_text: send_text
		});
	});

});