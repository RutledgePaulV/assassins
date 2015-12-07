define([
	'jquery',
/**
 * Unreferenced MIDS
 */
	'bootstrap-datetimepicker'
], function ($) {

	$('#start_date').datetimepicker({date: new Date($('#original_start_date').val())});
	$('#end_date').datetimepicker({date: new Date($('#original_end_date').val())});

});