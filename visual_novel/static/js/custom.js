$(function () {

    // Handling events with popup windows and galleries throughout the project
    // Documentation available at: http://dimsemenov.com/plugins/magnific-popup/
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

	$('.gallery').magnificPopup({
		delegate: 'a',
		type: 'image',
		gallery: {
			enabled:true,
			tCounter: '<span class="mfp-counter">%curr% из %total%</span>'
		}
	});

	// Handling events with tooltip events on hover
    // Documentation available at: http://iamceege.github.io/tooltipster/
	$('.tooltip').tooltipster({
        theme: 'tooltipster-shadow',
        contentAsHTML: true,
		interactive: true,
        maxWidth: 1000
    });

    // Custom functions for chart main page, to hide and open visual novel description
	$('.vn-desc-unwrap').click(function(){
        $(this).toggleClass('hidden-option').next().toggleClass('hidden-option').next().toggleClass('hidden-option');
        return false;
    });

    $('.vn-desc-wrap').click(function(){
        $(this).toggleClass('hidden-option').prev().toggleClass('hidden-option').prev().toggleClass('hidden-option');
        return false;
    });

    setTimeout(function(){
		$('.alert').fadeOut();
	}, 1000);
});

