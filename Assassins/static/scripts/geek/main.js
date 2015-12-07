define([
	'jquery',
	'scripts/components/visualizations/concentric',
/**
 * Unreferenced MIDS
 */
	'domReady!'
], function ($, Concentric) {

	var concentric = new Concentric({
		bgColor: 'white'
	});

	concentric.add(37, 400, 'lightgreen', 'python');
	concentric.add(30, 280, 'pink', 'html');
	concentric.add(18, 160, 'orange', 'css');
	concentric.add(15, 70, 'lightblue', 'javascript');

	var concentricContainer = $('#concentric');
	var legendContainer = $('#legend');

	concentric.place(concentricContainer);
	concentric.placeLegend(legendContainer);

});