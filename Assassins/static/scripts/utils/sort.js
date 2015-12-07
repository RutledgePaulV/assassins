define([
	'scripts/utils/meta'
], function (meta) {

	return function (array, property, ascending) {

		ascending = ascending || true;
		var sortOrder = ascending ? 1 : -1;
		var properties = property.split(',');

		for (var i in properties) {
			property = properties[i];
			var customSort = function (a, b) {
				var aValue = meta.getProperty(a, property) || '';
				var bValue = meta.getProperty(b, property) || '';
				var result = (aValue < bValue) ? -1 : (aValue > bValue) ? 1 : 0;
				return result * sortOrder;
			};

			array = array.sort(customSort);
		}

		return array;
	};

});