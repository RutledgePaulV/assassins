(function () {
	define(function () {

		require.config({
			config: {
				commands: {
					availableUrl: '/commands/available/',
					executionUrl: '/commands/',
					commands: window.__available__.commands
				}
			}
		});

	});

	require(['scripts/config/modules']);
}());