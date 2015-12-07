define([
	'jquery',
	'hbs!scripts/components/visualizations/templates/Concentric',
	'hbs!scripts/components/visualizations/templates/Legend',

/**
 * Unreferenced MIDS
 */
	'knob',
	'domReady!'
], function ($, ConcentricTemplate, LegendTemplate) {

	var defaults = {
		readOnly: true
	};

	var getPercentage = function (circle) {
		return circle.percentage;
	};

	var Concentric = function (options) {
		this.circles = [];
		this.settings = $.extend({}, defaults, options);
	};

	Concentric.prototype.sort = function () {
		this.circles = this.circles.sort(function (a, b) {
			var percentA = getPercentage(a);
			var percentB = getPercentage(b);
			return percentA > percentB ? -1 : percentA === percentB ? 0 : 1;
		});
	};

	Concentric.prototype.add = function (percent, diameter, color, label) {
		this.circles.push({
			percentage: percent,
			diameter: diameter,
			color: color,
			label: label
		});
	};

	Concentric.prototype.prepareData = function () {
		var globalThickness = this.settings.thickness || 0.2;
		this.sort();
		this.circles.forEach(function (circle, index, circles) {
			circle.margin = circle.margin || 0;
			circle.thickness = globalThickness;
			circle.angleOffset = circle.AngleOffset || 90;

			circle.ringWidth = circle.diameter * circle.thickness * 0.5;

			if (index > 0) {
				var containingCircle = circles[index - 1];
				var containingDiameter = containingCircle.diameter;
				var containingRingWidth = containingCircle.ringWidth;
				var innerDiameter = containingDiameter - containingRingWidth * 2;
				var extraMargin = (innerDiameter - circle.diameter) / 2 + containingRingWidth;

				var ratio = containingDiameter / circle.diameter;
				circle.margin = extraMargin + containingCircle.margin;
				circle.angleOffset = containingCircle.angleOffset + (360 * containingCircle.percentage / 100.0)
			}
		});
	};

	Concentric.prototype.build = function () {
		this.prepareData();
		return $(ConcentricTemplate(this));
	};

	Concentric.prototype.buildLegend = function () {
		this.prepareData();
		return $(LegendTemplate(this));
	};

	Concentric.prototype.place = function (domNode) {
		var node = this.build();
		$(domNode).append(node);
		$(node).find('input[type="text"]').knob(this.settings);
	};

	Concentric.prototype.placeLegend = function (domNode) {
		var node = this.buildLegend();
		$(domNode).append(node);
	};

	return Concentric;

});