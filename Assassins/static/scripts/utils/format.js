define([], function () {

	var manageArguments = function (args) {
		if (args.length > 1) {
			return [].slice.call(args, 0);
		} else if (args.length === 1 && args[0] instanceof Array) {
			return args[0];
		} else if (args.length === 1 && args[0] !== null && typeof args[0] === 'object') {
			return args[0];
		} else if (args.length === 1) {
			return [args[0]];
		} else {
			throw new Error("Received unexpected type of input for string formatter.");
		}
	};

	return function (input) {
		var args = manageArguments([].slice.call(arguments, 1));
		for (var key in args) {
			if (args.hasOwnProperty(key)) {
				var replace = new RegExp("{" + key + "}", "g");
				input = input.replace(replace, args[key]);
			}
		}
		return input;
	}
});