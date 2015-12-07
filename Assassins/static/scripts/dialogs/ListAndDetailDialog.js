/**
 * Defines a generic popup dialog designed for a purpose like the following:
 *
 *  Some initial view is a list of things. These things have one or more actions that can be performed on each.
 *  Once an action is chosen, the dialog view changes to display the details of that particular action. Usually
 *  some sort of confirmation and final action. Once the action is chosen or cancelled, it reverts again to the
 *  list view.
 *
 *  The backing data store can optionally be indexed and provides a free-text search on the bottom of the modal.
 *
 *  The modal is lazily instantiated and added to the dom on first show. The backing data store is simply a function
 *  that somehow produces results and then calls the success / failure callback. In many cases it will probably be
 *  driven by ajax requests.
 *
 */
define([
	'jquery', 'scripts/utils/search',
	'hbs!scripts/templates/ListAndDetailDialog'
], function ($, SearchableStore, dialogTemplate) {

	/**
	 * The constructor for a ListAndDetailDialog.
	 *
	 *
	 * @param listTemplate The template for list view. Each item in the list must contain the class 'result'
	 * @param errorTemplate The template for an error that occurs.
	 * @param dataQuery The function that can be called to populate the instance copy of the data to display.
	 * @constructor
	 */
	var ListAndDetailDialog = function (listTemplate, errorTemplate, dataQuery) {
		this.domNode = null;
		this.searchNode = null;

		this.dialogTemplate = dialogTemplate;
		this.listTemplate = listTemplate;
		this.errorTemplate = errorTemplate;
		this.dataQuery = dataQuery;

		this.data = [];
		this.error = {};
		this.context = {};
		this.store = null;
		this.indexedFields = [];

		this.showSearch = true;
		this.listViewClickEvents = {};
		this.detailViewClickEvents = {};
	};

	/**
	 * Clears all the results on the modal. Would clear either list view
	 * or detail view.
	 */
	ListAndDetailDialog.prototype.clearResult = function () {
		var resultsRoot = $(this.domNode).find('.results');
		resultsRoot.empty();
	};

	/**
	 * Sets a single result. Generally used for detail view.
	 *
	 * @param node
	 */
	ListAndDetailDialog.prototype.setResult = function (node) {
		var resultsRoot = $(this.domNode).find('.results');
		resultsRoot.html(node);
	};

	/**
	 * Adds a result to the current set of results. Generally used for building the list view.
	 *
	 * @param node
	 */
	ListAndDetailDialog.prototype.addResult = function (node) {
		var resultsRoot = $(this.domNode).find('.results');
		resultsRoot.append(node);
	};

	/**
	 * Function which generates the dom node and places it into the body. If it already
	 * exists, then nothing will happen. Additionally, if the modal is supposed to support
	 * search, then the keypress handlers will be bound to the search input by this method.
	 */
	ListAndDetailDialog.prototype.place = function () {
		var that = this;
		if (!this.domNode) {
			if (this.showSearch) {
				this.context.showSearch = true;
			}
			this.domNode = $(this.dialogTemplate(this.context));
			$('body').append($(this.domNode));
			if (this.showSearch) {
				this.searchNode = $(this.domNode).find('.search');
				this.searchNode.keypress(function (e) {
					if (e.which === 13) {
						that.renderListTemplate();
					}
				});
			}
		}
	};


	/**
	 * For applying any click handlers whenever the detail view is displayed. This
	 * provides a callback to any of the handlers that have been defined that when
	 * called will automatically return the modal to the list view.
	 *
	 */
	ListAndDetailDialog.prototype.applyDetailViewClickEvents = function () {
		var that = this;
		var resultsRoot = $(this.domNode).find('.results');

		for (var selector in this.detailViewClickEvents) {
			if (this.detailViewClickEvents.hasOwnProperty(selector)) {

				var callback = function (selector) {

					return function () {
						var detailOptions = that.detailViewClickEvents[selector] || {};

						var resultNode = $(this).closest('.result');
						var context = resultNode.data('context');
						var index = resultNode.data('index');

						var success = function () {
							if (detailOptions.shouldRefresh) {
								that.query();
							}

							if (detailOptions.shouldRemove) {
								delete that.data[index];
								if(that.showSearch) {
									that.store.remove({id: index});
									that.searchNode.val('');
								}
							}

							that.renderListTemplate();
						};

						var failure = function (error) {
							that.error = error;
							that.data = null;
							that.renderErrorTemplate();
						};

						if (detailOptions.callback) {
							detailOptions.callback(context, success, failure);
						} else {
							success();
						}
					}
				};

				resultsRoot.find(selector).click(callback(selector));
			}
		}
	};

	/**
	 * For applying any click handlers whenever the list view is displayed.
	 *
	 */
	ListAndDetailDialog.prototype.applyListViewClickEvents = function () {
		var that = this;
		var resultsRoot = $(this.domNode).find('.results');

		for (var selector in this.listViewClickEvents) {
			if (this.listViewClickEvents.hasOwnProperty(selector)) {

				var callback = function (selector) {
					return function () {
						var detailTemplate = that.listViewClickEvents[selector];
						var node = $(this).closest('.result');
						var index = $(node).data('index');
						var context = $(node).data('context');
						that.renderDetailTemplate(index, context, detailTemplate);
					}
				};

				resultsRoot.find(selector).click(callback(selector));
			}
		}
	};

	/**
	 * Renders the detail view given a particular node. The index and context
	 * are used to set the corresponding data attributes on the node so that
	 * any handlers can gain easy access to the data associated with the particular
	 * item. The template is determined by which detailTemplates were registered to
	 * correspond to which selectors for clickHandlers.
	 *
	 * @param index
	 * @param context
	 * @param detailTemplate
	 */
	ListAndDetailDialog.prototype.renderDetailTemplate = function (index, context, detailTemplate) {
		var data = this.data;
		if (this.showSearch) {
			$(this.searchNode).hide();
		}
		if (data.hasOwnProperty(index)) {
			var node = $(detailTemplate(context));
			$(node).data('index', index);
			$(node).data('context', context);
			this.setResult(node);
		}
		this.applyDetailViewClickEvents();
	};

	/**
	 * Renders the list view based on the currently held data store.
	 * If search is enabled then the contents of the search bar will
	 * be used to determine the result set to display.
	 *
	 */
	ListAndDetailDialog.prototype.renderListTemplate = function () {
		var data = this.data;
		this.clearResult();

		if (this.showSearch) {
			data = this.store.search($(this.searchNode).val());
			$(this.searchNode).show();
		}

		for (var key in data) {
			if (data.hasOwnProperty(key)) {
				var context = data[key];
				var node = $(this.listTemplate(context));
				$(node).data('index', key);
				$(node).data('context', context);
				this.addResult(node);
			}
		}
		this.applyListViewClickEvents();
	};

	/**
	 * Renders an error template. For calling when something went wrong
	 * fetching data from the store or in one of the event handlers.
	 *
	 */
	ListAndDetailDialog.prototype.renderErrorTemplate = function () {
		this.setResult($(this.errorTemplate(this.error)));
	};

	/**
	 * Prompts a new fetch from the store to repopulate the instance's
	 * copy of the data for displaying. After a successful load of data
	 * the list view will be rendered, and then if a callback was provided
	 * it will be called with the ListAndDetailDialog instance as an argument.
	 *
	 *
	 * @param callback
	 */
	ListAndDetailDialog.prototype.query = function (callback) {
		var that = this;
		if (this.dataQuery) {
			this.dataQuery(function (data) {
				that.load(data);
				that.error = null;
				that.renderListTemplate();
				if (callback) {
					callback(that);
				}
			}, function (error) {
				that.data = null;
				that.error = error;
				that.renderErrorTemplate();
				if (callback) {
					callback(that);
				}
			});
		}
	};

	/**
	 * Used for loading an array of data into the instance. If search
	 * is enabled then it will also redefine the search index with the
	 * new data.
	 *
	 * @param data
	 */
	ListAndDetailDialog.prototype.load = function (data) {

		this.indexedFields = [];
		this.store = null;

		this.data = data;

		if (this.showSearch) {
			if (data.length > 0) {
				for (var key in data[0]) {
					if(data[0].hasOwnProperty(key)) {
						this.indexedFields.push(key);
					}
				}
			}
			this.store = new SearchableStore(this.data, this.indexedFields);
		}

	};

	/**
	 * Displays the modal with a fresh call to populate the data.
	 * On the first call this will result in the relevant dom nodes
	 * being constructed and put into the body.
	 *
	 */
	ListAndDetailDialog.prototype.show = function () {
		this.place();
		this.query();
		$(this.domNode).modal('show');
	};

	/**
	 * Hides the modal. If called before show, then this will construct
	 * the modal and put it into the dom but not show it.
	 *
	 */
	ListAndDetailDialog.prototype.hide = function () {
		this.place();
		$(this.domNode).modal('hide');
	};

	return ListAndDetailDialog;

});