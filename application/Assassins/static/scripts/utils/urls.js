define(['jquery'], function ($) {

	return {
		getQueryParams: function () {
			return (function (a) {
				if (a === '') return {};
				var b = {};
				for (var i = 0; i < a.length; ++i) {
					var p = a[i].split('=');
					if (p.length != 2) continue;
					b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, ' '));
				}
				return b;
			})(window.location.search.substr(1).split('&'));
		},
		setQueryParams: function (params) {
			var queryString = '?' + $.param(params);
			if (queryString !== '?') {
				history.replaceState({}, '', queryString);
			} else {
				history.replaceState({}, '', '//' + location.host + location.pathname);
			}
		},
		deleteQueryParams: function () {
			var current = this.getQueryParams();
			var args = [].slice.call(arguments);
			args.forEach(function (arg) {
				delete current[arg];
			});
			this.setQueryParams(current);
		},
		updateQueryParams: function (overrides) {
			var current = this.getQueryParams();
			var updatedParams = $.extend({}, current, overrides);
			this.setQueryParams(updatedParams);
		}
	}
});