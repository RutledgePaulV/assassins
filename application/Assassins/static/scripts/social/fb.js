define(['facebook'], function (FB) {

	FB.init({
		appId: '664656580346919',
		cookie: true,
		xfbml: true,
		version: 'v2.3'
	});

	return FB;
});