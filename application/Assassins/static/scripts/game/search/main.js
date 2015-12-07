define([
	'jquery', 'commands', 'scripts/utils/urls', 'scripts/config/valConfig',
	'hbs!scripts/game/templates/result',

/**
 * Unreferenced MID
 */
	'formValidation',
	'domReady!'
], function ($, commands, urls, valConfig, resultTemplate) {

	var resultContainer = $('#results');
	var searchContainer = $('#search');

	/**
	 * What should we do with the results after a query to the server?
	 *
	 * @param data
	 */
	var searchResultHandler = function (data) {
		resultContainer.html('');

		if (data.results && data.results.length > 0) {
			// building results in a loop and displaying as we go.
			for (var index in data.results) {
				if (data.results.hasOwnProperty(index)) {
					var result = data.results[index];
					var markup = resultTemplate(result);
					resultContainer.append(markup);
				}
			}

		} else {
			resultContainer.html('<h3>No results found!</h3>');
		}

	};

	/**
	 * What should we do if something went wrong when querying the server?
	 * @param data
	 */
	var searchResultFailure = function (data) {
		alert('Oops! Something went wrong with your search. Are you connected to the internet?');
	};

	/**
	 * Actually performs the query for a given term and page.
	 *
	 * @param queryTerm
	 * @param page
	 */
	var query = function (queryTerm, page) {

		var modifier = buildHistoryModifierCallback(queryTerm, page);

		var callback = function (data) {
			searchResultHandler(data);
			modifier(data);
		};

		var payload = {query: queryTerm, page: page};

		commands.SEARCH_GAMES.fire(payload, callback, searchResultFailure);
	};

	var buildHistoryModifierCallback = function () {
		var currentParams = urls.getQueryParams();
		var currentQuery = currentParams.query;
		var currentPage = currentParams.page || 1;

		return function (data) {
			if (currentQuery !== data.query && data.query !== '') {
				urls.deleteQueryParams('page');
				urls.updateQueryParams({query: data.query});
			}

			if (data.query === '') {
				urls.deleteQueryParams('query');
			}

			if (currentPage !== data.page && data.page > 1) {
				urls.updateQueryParams({page: data.page});
			} else if (data.page === 1) {
				urls.deleteQueryParams('page');
			}
		}
	};

	/**
	 * Perform a search on enter.
	 */
	searchContainer.keypress(function (e) {
		if (e.which === 13) {
			query($(this).val(), 1);
		}
	});

	/**
	 * Prevent empty queries from being searched.
	 */
	searchContainer.formValidation({
		framework: 'bootstrap',
		container: valConfig.CONTAINER,
		feedbackIcons: valConfig.ICONS,
		fields: {
			search: valConfig.SEARCH
		}
	});


	/**
	 * Perform a search when the page first loads.
	 */
	query(searchContainer.val(), searchContainer.data('page') || 1);

});