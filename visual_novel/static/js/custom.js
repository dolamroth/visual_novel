$('.vn-desc-unwrap').click(function(){
	$(this).toggleClass('hidden-option').next().toggleClass('hidden-option').next().toggleClass('hidden-option');
	return false;
});

$('.vn-desc-wrap').click(function(){
	$(this).toggleClass('hidden-option').prev().toggleClass('hidden-option').prev().toggleClass('hidden-option');
	return false;
});

$(function () {
	$('.popup-modal').magnificPopup({
		type: 'inline',
		preloader: false,
		focus: '#username',
		modal: true
	});
	$(document).on('click', '.popup-modal-dismiss', function (e) {
		e.preventDefault();
		$.magnificPopup.close();
	});
});

$(document).ready(function() {
	$('.gallery').magnificPopup({
		delegate: 'a',
		type: 'image',
		gallery: {
			enabled:true,
			tCounter: '<span class="mfp-counter">%curr% из %total%</span>'
		}
	});
});
