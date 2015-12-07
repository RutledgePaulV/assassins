define(['jquery'], function ($) {

	var defaults = {
		overwritesAllowed: false
	};

	/**
	 *
	 * @param {string} name A name for the store.
	 * @param {object} options A set of options to override the defaults with
	 * @constructor Store
	 * @class Store
	 */
	var Store = function (name, options) {
		this.data = {};
		this.name = name;
		this.options = $.extend({}, defaults, options);
	};

	Store.prototype = {
		constructor: Store,
		put: function (key, value) {
			if (!this.options.overwritesAllowed && this.data.hasOwnProperty(key))
				throw new Error('You may not write to a key which has already been written to.');
			this.data[key] = value;
		},
		payload: function (converter) {
			var result = $.extend(true, {}, this.data);
			return converter ? converter(result) : result;
		}
	};

	return Store;
});