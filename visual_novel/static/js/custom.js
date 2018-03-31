jQuery.fn.extend({
    collapseTC: function(){
        var example_row = $(".collapsed-row-example");
        var translation_row_old = this;
        this.replaceWith( example_row.clone(true, true) );
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
    },
    collapseAC: function(is_chapter){
        var className = (is_chapter === "True") ? ".add-section-text-example" : ".add-chapter-text-example";
        var example_row = $(className);
        var translation_row_old = this;
        this.replaceWith( example_row.clone(true, true) );
        var translation_row_add = $(className).first();
        translation_row_add.trigger('create');
        $.each(translation_row_old.prop('attributes'), function() {
            translation_row_add.attr(this.name, this.value);
        });
        translation_row_add
            .removeClass('add-row-expanded')
            .addClass('add-row-collapsed');
        return translation_row_add;
    },
    collapseAll: function(){
        var expanded = $('.translation-chapter-expanded');
        if (expanded.length > 0){
            expanded.first().collapseTC();
        }
        expanded = $('.add-row-expanded');
        if (expanded.length > 0){
            expanded.first().collapseAC();
        }
        return this;
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
        edit_link.collapseAll();
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

    $('.btn-save-translation-chapter').on('click', function(e){
        var save_link = $( e.currentTarget );
        var translation_row = save_link.closest('.translation-chapter-expanded');
        var data = {};
        data['translation_item_id'] = parseInt(translation_row.attr('data_translation_item'));
        data['translation_chapter_id'] = parseInt(translation_row.attr('data_id'));
        data['total'] = translation_row.find('.input_data_total_rows').val();
        data['translated'] = translation_row.find('.input_data_translation').val();
        data['edited_first_pass'] = translation_row.find('.input_data_editing_first_pass').val();
        data['edited_second_pass'] = translation_row.find('.input_data_editing_second_pass').val();
        data['parent'] = parseInt(translation_row.find('.input_data_parent').find(":selected").val());
        data['move_to'] = translation_row.find('.input_data_position').find(":selected").val();
        data['is_chapter'] = (translation_row.attr('data_is_chapter') === 'True');
        data['title'] = translation_row.find('.input_data_title').val();
        data['script_title'] = translation_row.find('.input_data_script_title').val();

        $.ajax({
            url: save_link.attr('href'),
            method: 'GET',
            data: data,
            type: 'json'
        }).always(function(data){
            console.log(data);
            if (data['movement']){
                location.reload();
            } else {
                if (data['status'] && (data['status'] !== 200)){
                    /* TODO: alert */
                } else{
                    var return_data = data['data'];
                    translation_row.attr('data_translated', return_data['new_translated']);
                    translation_row.attr('data_total_rows', return_data['total']);
                    translation_row.attr('data_edited_first_pass', return_data['new_edited_first_pass']);
                    translation_row.attr('data_edited_second_pass', return_data['new_edited_second_pass']);
                    translation_row.attr('data_title', return_data['title']);
                    translation_row.attr('data_script_title', return_data['script_title']);
                    translation_row = translation_row.collapseTC();
                    translation_row.find('.item_name').find('span').text(return_data['script_title']);
                }
            }
        });

        return false;
    });

    $('.add-chapter').on('click', function(e){
        var add_chapter_link = $( e.currentTarget );
        add_chapter_link.collapseAll();
        var translation_row_old = add_chapter_link.closest('.add-row-collapsed');
        var class_chapter = translation_row_old.attr('data_is_chapter') === "True" ? ".add-section-example" : ".add-chapter-example";
        var example_row = $(class_chapter);
        translation_row_old.replaceWith( example_row.clone(true, true) );
        var translation_row = $(class_chapter).first();
        translation_row.trigger('create');
        $.each(translation_row_old.prop('attributes'), function() {
            translation_row.attr(this.name, this.value);
        });
        translation_row
            .removeClass('add-row-collapsed')
            .addClass('add-row-expanded')
            .removeClass('editing-row-hidden');
        return false;
    });

    $('.btn-cancel-new-translation-chapter').on('click', function(e){
        var cancel_add_chapter_link = $( e.currentTarget );
        var translation_row_add = cancel_add_chapter_link.closest('.add-row-expanded');
        var is_chapter = translation_row_add.attr('data_is_chapter');
        translation_row_add.collapseAC(is_chapter);
        return false;
    });
});

