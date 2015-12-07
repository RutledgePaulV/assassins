define([
	'jquery',
	'hbs!scripts/templates/ConfirmationDialog'
], function ($, template) {

	function ConfirmationDialog() {
		this.isPlaced = false;
		this.hasShown = false;
		this.heading = 'Confirmation Required';
		this.message = 'Are you sure?';
		this.submessage = 'This action is irreversible.';
		this.dom = null;
	}

	ConfirmationDialog.prototype.place = function () {
		$('body').append(this.getDom());
		this.isPlaced = true;
	};

	ConfirmationDialog.prototype.getDom = function () {
		if (this.dom) return this.dom;
		this.dom = $(template(this));
	};

	ConfirmationDialog.prototype.show = function (onSuccess, onFailure) {
		if (!this.isPlaced) this.place();
		if (this.hasShown && arguments.length == 0) return $(this.dom).modal('show');

		var that = this;

		var success = function () {
			if (onSuccess) {
				onSuccess();
			}
			$(that.dom).modal('hide');
		};

		var canceled = function () {
			if (onFailure) {
				onFailure();
			}
			$(that.dom).modal('hide');
		};

		$(this.dom).find('.confirm').click(success);
		$(this.dom).find('.cancel').click(canceled);
		$(this.dom).modal('show');
		this.hasShown = true;
	};


	return ConfirmationDialog;
});