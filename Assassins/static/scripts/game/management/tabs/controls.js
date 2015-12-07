define([
	'jquery',
	'commands',
	'context',
	'scripts/utils/redirect',
	'scripts/dialogs/ConfirmationDialog',
	'scripts/dialogs/ListAndDetailDialog',
	'hbs!scripts/templates/PlayerResults',
	'hbs!scripts/templates/KickPlayerDetails',
	'hbs!scripts/templates/MakeReviewerDetails',
	'hbs!scripts/templates/ReviewerResults',
	'hbs!scripts/templates/KickReviewerDetails',
	'hbs!scripts/templates/MakeOwnerDetails',
	'hbs!scripts/templates/ErrorResult',
/**
 *
 */
	'domReady!'
], function ($, commands, context, redirect,
             ConfirmationDialog, ListAndDetailDialog,
             playerTemplate, kickPlayerDetailTemplate, makeReviewerDetailTemplate,
             reviewerTemplate, kickReviewerDetailTemplate, makeOwnerDetailTemplate,
             errorTemplate) {


	var setupRow1 = function () {
		// row 1, delete button
		var confirmationDialog = new ConfirmationDialog();
		confirmationDialog.message = "Are you sure you want to delete this game?";
		confirmationDialog.submessage = "This is not reversible and will affect every player and host in the game.";

		var deleteButton = $('#delete-game');
		deleteButton.click(function () {
			confirmationDialog.show(function () {
				commands.DELETE_GAME.fire({
					game: context.game
				}, function () {
					redirect('/');
				}, function () {
					alert('Could not delete the game!');
				});
			});
		});
	};


	var setupRow2 = function () {
		// row 2, enable registration
		var openButton = $('#open-registration');
		var closeButton = $('#close-registration');

		openButton.click(function () {
			var payload = {game: context.game, open: true};
			commands.TOGGLE_REGISTRATION.fire(payload, function () {
				openButton.prop('disabled', true);
				closeButton.prop('disabled', false);
			});
		});

		closeButton.click(function () {
			var payload = {game: context.game, open: false};
			commands.TOGGLE_REGISTRATION.fire(payload, function () {
				openButton.prop('disabled', false);
				closeButton.prop('disabled', true);
			});
		});

	};

	var getQueryForPlayerType = function (type) {
		return function (success, failure) {
			var filters = {pk: context.game, type: type, query: ''};
			commands.LIST_USERS_FOR_GAME.fire(filters, function (data) {
				success(data.results);
			}, failure);
		}
	};

	var setupRow3 = function () {
		var hostButton = $('#manage-reviewers');
		var query = getQueryForPlayerType('reviewers');
		var hostManager = new ListAndDetailDialog(reviewerTemplate, errorTemplate, query);
		hostManager.context.title = 'Reviewers';

		var kickReviewerCallback = function (data, success, failure) {
			var payload = {game: context.game, player_pk: data.pk};
			commands.KICK_FROM_GAME.fire(payload, success, failure);
		};

		var makeOwnerCallback = function (data, success, failure) {
			var payload = {game: context.game, player_pk: data.pk};
			commands.MAKE_OWNER.fire(payload, function () {
				redirect('games:manage', {pk: context.game});
				// no callback since we're redirecting anyway
			}, failure);
		};

		hostManager.listViewClickEvents = {
			'.kick-reviewer-button': kickReviewerDetailTemplate,
			'.make-owner-button': makeOwnerDetailTemplate
		};

		hostManager.detailViewClickEvents = {
			'.make-owner-confirm': {
				callback: makeOwnerCallback
			},
			'.kick-reviewer-confirm': {
				callback: kickReviewerCallback,
				shouldRemove: true,
				shouldRefresh: false
			},
			'.cancel': {
				shouldRemove: false,
				shouldRefresh: false
			}
		};

		hostButton.click(function () {
			hostManager.show();
		});
	};


	var setupRow4 = function () {
		// row 4, player management
		var playerButton = $('#manage-players');
		var query = getQueryForPlayerType('players');
		var playerManager = new ListAndDetailDialog(playerTemplate, errorTemplate, query);
		playerManager.context.title = 'Players';


		var kickPlayerCallback = function (data, success, failure) {
			var payload = {game: context.game, player_pk: data.pk};
			commands.KICK_FROM_GAME.fire(payload, success, failure);
		};

		var makeReviewerCallback = function (data, success, failure) {
			var payload = {game: context.game, player_pk: data.pk};
			commands.MAKE_REVIEWER.fire(payload, success, failure);
		};

		playerManager.listViewClickEvents = {
			'.kick-player-button': kickPlayerDetailTemplate,
			'.make-reviewer-button': makeReviewerDetailTemplate
		};

		playerManager.detailViewClickEvents = {
			'.make-reviewer-confirm': {
				callback: makeReviewerCallback,
				shouldRemove: true,
				shouldRefresh: false
			},
			'.kick-player-confirm': {
				callback: kickPlayerCallback,
				shouldRemove: true,
				shouldRefresh: false
			},
			'.cancel': {
				shouldRemove: false,
				shouldRefresh: false
			}
		};

		playerButton.click(function () {
			playerManager.show();
		});
	};


	var setupRow5 = function () {
		var subscriptionButton = $('#manage-subscription');
		subscriptionButton.click(function () {
			alert('Subscriptions aren\'t actually a thing yet!');
		});
	};


	// setup everything.
	setupRow1();
	setupRow2();
	setupRow3();
	setupRow4();
	setupRow5();

});