(function () {
	return {
		wrapShim: true,
		optimizeCss: "none",
		optimize: "uglify2",
		skipDirOptimize: false,
		preserveLicenseComments: false,
		mainConfigFile: 'config/require.js',
		// this piece embeds a define and require of the module configuration
		// just prior to the require() call provided by the insertRequire (which
		// is used to load the main for a given page. This is necessary because
		// commands depends on module configuration
		include: ['scripts/config/modules']
	}
}());