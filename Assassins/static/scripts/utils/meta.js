/**
 * This module defines the Meta global which includes functions
 * for performing meta-level operations on functions / objects.
 */
define({

	memoize: function (func) {
		var memo = {};
		return function () {
			var args = [].slice.call(arguments);
			if (args in memo) {
				return memo[args];
			} else {
				return (memo[args] = func.apply(this, args));
			}
		};
	},

	getProperty: function (obj, attribute) {
		var attributes = attribute.split('.');
		return attributes.reduce(function (agg, attr) {
			if (agg.hasOwnProperty(attr)) {
				return agg[attr];
			} else {
				return null;
			}
		}, obj);
	}

});