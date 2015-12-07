(function (global) {


	require.config({

		/**
		 * All static files are namespaced under /static/ for our site.
		 */
		baseUrl: '/static/',

		/**
		 * We define custom paths for any bower modules that may be used
		 * or proprietary things like redactor or anything else that we want a shortcut reference.
		 */
		paths: {
			'formatter': 'formatter/dist/formatter.min',
			'context': 'scripts/shims/context',
			'jquery': 'scripts/shims/jquery',
			'facebook': 'scripts/lib/facebook/facebook',
			'knob': 'jquery-knob/dist//jquery.knob.min',
			'hbs': 'require-handlebars-plugin/hbs',
			'domReady': 'requirejs-domready/domReady',
			'moment': 'moment/min/moment.min',
			'commands': 'commands/commands',
			'bootstrap': 'bootstrap/dist/js/bootstrap.min',
			'redactor': 'scripts/lib/redactor/redactor.min',
			'nested': 'nested/jquery.nested',
			'bootstrap-select': 'bootstrap-select/dist/js/bootstrap-select.min',
			'formValidation-base': 'scripts/lib/formvalidation/formValidation.min',
			'formValidation': 'scripts/lib/formvalidation/bootstrap.min',
			'bootstrap-datetimepicker': 'eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min',
			'slick': 'slick-carousel/slick/slick.min',
			'lunr': 'lunr.js/lunr.min'
		},

		config: {
			commands: {
				availableUrl: '/commands/available/',
				executionUrl: '/commands/',
				commands: (global.__available__ || {}).commands
			}
		},

		/**
		 * Configuring handlebars plugin for precompilation
		 */
		hbs: {
			helpers: true,
			i18n: false,
			templateExtension: 'handlebars',
			partialsUrl: '',
			helperPathCallback: function (name) {
				return '/static/scripts/templates/helpers/' + name + '.js';
			}
		},

		/**
		 * Defining shims for any true jquery plugins
		 */
		shim: {

			'jquery-cookie': {
				exports: 'jQuery.cookie'
			},

			'slick': {
				deps: ['jquery'],
				exports: 'jQuery.fn.slick'
			},

			'nested': {
				deps: ['jquery'],
				exports: 'jQuery.fn.nested'
			},

			'bootstrap-select': {
				deps: ['jquery', 'bootstrap'],
				exports: 'jQuery.fn.selectpicker'
			},

			'knob': {
				deps: ['jquery'],
				exports: 'jQuery.fn.knob'
			},

			'facebook': {
				exports: 'FB'
			},

			'formValidation-base': {
				deps: ['jquery'],
				exports: 'FormValidation'
			},

			'formValidation': {
				deps: ['formValidation-base'],
				exports: 'FormValidation'
			},

			'bootstrap-datetimepicker': {
				deps: ['jquery', 'bootstrap', 'moment'],
				exports: 'jQuery.fn.datetimepicker'
			}

		}

	});


}(this || {}));