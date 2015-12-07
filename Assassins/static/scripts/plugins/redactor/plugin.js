/**
 * This module just provides a wrapper around redactor's plugin registry method.
 * We create the global if it doesn't exist yet, and we expose a constructor
 * function for use when defining new plugins.
 *
 *
 */
define(function(){

	if(!window.RedactorPlugins){
		window.RedactorPlugins = {};
	}

	return function(name, prototype){
		window.RedactorPlugins[name] = function(){
			return prototype;
		};

		return name;
	};

});