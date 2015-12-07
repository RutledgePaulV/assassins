define([
	'jquery',
	'commands',
	'scripts/game/management/section',
/**
 * Unreferenced MIDS
 */
	'domReady!'
], function($, commands, Section) {

	$('#complete-tabs').find('a').click(function (e) {
		e.preventDefault();
		$(this).tab('show');
	});

	var reviewSection = new Section('#review', 'review');
	var pendingSection = new Section('#pending', 'pending');
	var incompleteSection = new Section('#incomplete', 'incomplete');
	var completeSection = new Section('#complete', 'complete');

	var updateSections = function () {
		reviewSection.update();
		completeSection.update();
	};

	reviewSection.registerHandlers(function (section) {

		$(section.domNode).find('button[name="success"]').click(function () {
			var pk = $(this).data('assignment');
			var payload = {assignment: pk, verdict: true};
			commands.ASSIGNMENT_REPORT_STATUS.fire(payload, updateSections);
		});

		$(section.domNode).find('button[name="failure"]').click(function () {
			var pk = $(this).data('assignment');
			var payload = {assignment: pk, verdict: false};
			commands.ASSIGNMENT_REPORT_STATUS.fire(payload, updateSections);
		});

	});


});
