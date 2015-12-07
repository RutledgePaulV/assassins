(function (context) {

	var heap = window.heap = [];

	heap.load = function (e, t) {
		window.heap.appid = e;
		window.heap.config = t = t || {};
		var n = t.forceSSL || "https:" === document.location.protocol, a = document.createElement("script");
		a.type = "text/javascript";
		a.async = !0;
		a.src = (n ? "https:" : "http:") + "//cdn.heapanalytics.com/js/heap-" + e + ".js";
		var o = document.getElementsByTagName("script")[0];
		o.parentNode.insertBefore(a, o);
		for (var r = function (e) {
			return function () {
				heap.push([e].concat(Array.prototype.slice.call(arguments, 0)))
			}
		}, p = ["clearEventProperties", "identify", "setEventProperties", "track", "unsetEventProperty"], c = 0; c < p.length; c++) {
			heap[p[c]] = r(p[c])
		}
	};

	if (context.token) {
		heap.load(context.token);
	}

	if (context.user) {
		heap.identify(context.user);
	}

}((window || {}).__context__ || {}));
