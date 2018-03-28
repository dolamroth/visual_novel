jQuery.fn.extend({
    collapseTC: function(){
        var example_row = $(".collapsed-row-example");
        var translation_row_old = this;
        this.replaceWith( example_row.clone(true, true) );
        console.log($(".collapsed-row-example"));
        var translation_row = $(".collapsed-row-example").first();
        translation_row.trigger('create');
        $.each(translation_row_old.prop('attributes'), function() {
            translation_row.attr(this.name, this.value);
        });
        translation_row.find('td').first().html( translation_row.attr('data_name') );
        translation_row
            .removeClass('translation-chapter-expanded')
            .addClass('translation-chapter-collapsed')
            .removeClass('editing-row-hidden')
            .removeClass('collapsed-row-example');

        return translation_row;
    }
});

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

    $('.translation-chapter-edit').on('click', function(e){
        var edit_link = $( e.currentTarget );
        var expanded = $('.translation-chapter-expanded');
        if (expanded.length > 0){
            expanded.first().collapseTC();
        }
        var translation_row_old = edit_link.closest('.translation-chapter-collapsed');
        var class_chapter = translation_row_old.attr('data_is_chapter') === "True" ? ".editing-row-example-chapter" : ".editing-row-example";
        var example_row = $(class_chapter);
        translation_row_old.replaceWith( example_row.clone(true, true) );
        var translation_row = $(class_chapter).first();
        translation_row.trigger('create');
        $.each(translation_row_old.prop('attributes'), function() {
            translation_row.attr(this.name, this.value);
        });
        translation_row.find('.input_data_title').val( translation_row.attr('data_title') );
        translation_row.find('.input_data_script_title').val( translation_row.attr('data_script_title') );
        translation_row.find('.input_data_total_rows').val( translation_row.attr('data_total_rows') );
        translation_row.find('.input_data_translation').val( translation_row.attr('data_translated') );
        translation_row.find('.input_data_editing_first_pass').val( translation_row.attr('data_edited_first_pass') );
        translation_row.find('.input_data_editing_second_pass').val( translation_row.attr('data_edited_second_pass') );
        translation_row
            .removeClass('translation-chapter-collapsed')
            .addClass('translation-chapter-expanded')
            .removeClass('editing-row-hidden')
            .removeClass('editing-row-example');
    	return false;
	});

    $('.btn-cancel-translation-chapter').on('click', function(e){
        var cancel_link = $( e.currentTarget );
        var translation_row_old = cancel_link.closest('.translation-chapter-expanded');
        translation_row_old.collapseTC();
        return false;
    });
});

