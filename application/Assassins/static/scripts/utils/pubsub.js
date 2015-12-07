/**
 * This jQuery plugin provides a basic implementation of the publish / subscribe event model. This
 * allows us to take advantage of the event system within jQuery without being directly tied to DOM
 * elements, and so we can use it for driving any custom events for plain JS.
 *
 *
 */

define(['jquery'], function ($) {

	var queue = $({});

	return {
		pub: function (topic, args) {
			queue.trigger.apply(queue, arguments);
		},
		sub: function (topic, callback) {
			queue.on(topic, callback);
		},
		unsub: function (topic) {
			queue.off(topic);
		}
	};

});