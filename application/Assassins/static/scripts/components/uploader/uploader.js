define([
	'scripts/utils/format',
	'hbs!scripts/components/uploader/templates/Uploader'
], function (format, UploaderTemplate) {

	var index = 0;

	var updateImage = function (imageNode, source) {
		$(imageNode).attr('src', source);
	};

	var getPreviewCallback = function (imageNode) {
		return function (inputNode) {
			if (inputNode && inputNode.files && input.files[0]) {
				var reader = new FileReader();
				reader.onload = function (e) {
					updateImage(imageNode, e.target.result);
				};
				reader.readAsDataURL(inputNode.files[0]);
			}
		}
	};

	var Uploader = function (emptyImage, defaultImage, inputNode) {
		this.emptyImage = emptyImage;
		this.defaultImage = defaultImage;
		this.input = inputNode;
		this.init();
	};

	Uploader.prototype.init = function () {
		var id = 'image-preview-' + index++;
		$(this.input).before(format('<img id="{0}" height="200" width="200"/>', id));
		this.image = $('#' + id);
		updateImage(this.image, this.defaultImage ? this.defaultImage : this.emptyImage);
		$(this.input).change(getPreviewCallback(this.image));
	};

	Uploader.prototype.get = function () {
		return $(this.input)[0].files[0];
	};

	Uploader.prototype.remove = function () {
		this.input.value = null;
		updateImage(this.image, this.defaultImage);
	};

	return Uploader;
});