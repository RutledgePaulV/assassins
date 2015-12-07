define([
	'jquery',
	'commands',
	'context',
	'hbs!scripts/game/templates/in_review',
	'hbs!scripts/game/templates/in_progress',
	'hbs!scripts/game/templates/complete',
	'hbs!scripts/game/templates/incomplete'
/**
 * unreferenced MIDS
 */

], function ($, commands, context, inReviewTemplate,
             inProgressTemplate, completeTemplate, incompleteTemplate) {

	var Section = function (identifier, type) {
		this.type = type;
		this.domNode = $(identifier);
		this.countNode = this.domNode.find('.count').next();
		this.resultsNode = this.domNode.find('.results').next();
		this.init();
	};

	Section.prototype = {
		constructor: Section,
		init: function () {
			switch (this.type) {
				case 'review':
					this.template = inReviewTemplate;
					break;
				case 'pending':
					this.template = inProgressTemplate;
					break;
				case 'incomplete':
					this.template = incompleteTemplate;
					break;
				case 'complete':
					this.template = completeTemplate;
					break;
				default:
					throw new Error('Provided type was not expected.');
			}
		},
		_updateCount: function (count) {
			this.countNode.text(count);
		},
		_rebuildResults: function (results) {
			var template = this.template;
			var resultsNode = this.resultsNode;

			resultsNode.empty();

			if (!results || results.length === 0) {
				resultsNode.append('<p>Nothing to see here!</p>');
			}

			results.forEach(function (result) {
				var markup = template(result);
				resultsNode.append(markup);
			});
		},
		_buildPayload: function () {
			return {
				game: context.game,
				type: this.type
			}
		},
		update: function () {
			var self = this;
			var payload = this._buildPayload();
			commands.GET_MANAGEMENT_SECTION.fire(payload, function (data) {
				self._updateCount(data.count);
				self._rebuildResults(data.results);
			});
		},
		registerHandlers: function (callback) {
			callback(this);
		}
	};


	return Section;
});