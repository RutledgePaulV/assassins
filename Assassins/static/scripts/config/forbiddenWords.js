define([], function () {

	var words = [
		'\u0061\u0073\u0073',
		'\u0066\u0075\u0063\u006b',
		'\u0066\u0075\u006b',
		'\u0066\u0075\u0063',
		'\u0064\u0061\u006d\u006e',
		'\u0063\u0075\u006e\u0074',
		'\u0062\u0069\u0074\u0063\u0068',
		'\u0077\u0068\u006f\u0072\u0065',
		'\u0074\u0069\u0074',
		'\u0070\u0075\u0073\u0073\u0079',
		'\u0076\u0061\u0067\u0069\u006e\u0061',
		'\u0070\u0065\u006e\u0069\u0073',
		'\u0073\u0068\u0069\u0074',
		'\u0073\u0063\u0072\u006f\u0074\u0075\u006d',
		'\u0070\u006f\u0072\u006e',
		'\u0062\u006c\u006f\u0077\u006a\u006f\u0062',
		'\u0073\u0065\u006d\u0065\u006e',
		'\u0063\u0075\u006d'
	];

	return new RegExp(words.join('|'), 'i')

});