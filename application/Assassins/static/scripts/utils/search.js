define(['lunr'], function (lunr) {


	var SearchableStore = function (data, indexedFields) {

		var index = lunr(function () {
			for (var key in indexedFields) {
				if (indexedFields.hasOwnProperty(key)) {
					var field = indexedFields[key];
					this.field(field);
				}
			}

			this.ref('id');
		});

		for (var key in data) {
			if (data.hasOwnProperty(key)) {
				var doc = data[key];
				if (!doc.id) {
					doc.id = key;
				}
				index.add(doc);
			}
		}

		this.data = data;
		this.index = index;
	};

	SearchableStore.prototype.remove = function (ref) {
		this.index.remove(ref);
		delete this.data[ref.id];
	};

	SearchableStore.prototype.search = function (term) {

		if (!term) {
			return this.data;
		}

		var refsAndScores = this.index.search(term);
		var results = [];

		var that = this;
		refsAndScores.forEach(function (result) {
			results.push(that.data[result.ref]);
		});

		return results;
	};

	return SearchableStore;
});