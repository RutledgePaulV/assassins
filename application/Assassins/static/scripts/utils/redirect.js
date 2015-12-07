/**
 * Redirect offers a cached method for redirecting users based on django view names,
 * or if the url begins with / it will be relative to the base url. If it begins with
 * ./ it will be relative to the current page.
 */
define([
	'commands'
], function (commands) {

	var join = function() {
		return [].prototype.splice(arguments).join('/').replace(/\/+/g, '/');
	};

	var redirect = function(replacement) {
		window.location.replace(replacement);
	};

	var refresh = function () {
		window.location.reload(true);
	};

	var cache = {
		get: function (key) {
			return sessionStorage.getItem(key);
		},
		put: function (key, value) {
			sessionStorage.setItem(key, value);
		}
	};

	var reverse = function (view_name, kwargs) {
		var args = JSON.stringify(arguments);

		var cachedValue = cache.get(args);

		if (cachedValue) {
			redirect(join(window.location.origin, cachedValue));
		} else {
			commands.REVERSE_URL.fire({
				view_name: view_name,
				kwargs: kwargs || {}
			}, function (data) {
				var uri = data.result;
				cache.put(args, uri);
				redirect(join(window.location.origin ,uri));
			});
		}
	};

	return function (path, kwargs) {

		if (!path) {
			refresh();
		}

		var piece = path.length >= 2 ? path.substr(0, 2) : '/';

		switch (piece) {
			case '/':
				redirect(join(window.location.origin, path));
				break;
			case './':
				redirect(join(window.location.href, path.substring(1)));
				break;
			default:
				reverse(path, kwargs);
				break;
		}

	};


});