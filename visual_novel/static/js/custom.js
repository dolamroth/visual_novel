window.translation_errors_codes = {
    "translation_item_id": "Уникальный идентификатор перевода",
    "new_parent": "Идентификатор родительского элемента",
    "new_move_to": "Тип перемещения",
    "title": "Пользовательское название",
    "script_title": "Название скрипта",
    "is_chapter": "(Скрытое поле) является ли разделом",
    "timezone": "(Скрытое поле) смещение в минутах от UTC-часового пояса",
    "translation_chapter_id": "Уникальный идентификатор главы перевода",
    "total": "Всего строк",
    "new_translated": "Перевод",
    "new_edited_first_pass": "Редактура 1",
    "new_edited_second_pass": "Редактура 2"
};

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
    },
    showRecalculate: function(){
        var translation_row = $('#translation_total_rows').closest('tr');
        var vn_alias = translation_row.attr('data_alias');
        var translation_item = translation_row.attr('data_translation_item');
        $.ajax({
            url: '/api/translation/'+vn_alias+'/get-statistics',
            method: 'GET',
            data: {'translation_item_id': translation_item},
            type: 'json'
        }).always(function(data){
            if (data['statistics']){
                $('#translation_total_rows').text( data['statistics']['total_rows'] );
                $('#translation_translation').text( data['statistics']['translated'] );
                $('#translation_edited_first_pass').text( data['statistics']['edited_first_pass'] );
                $('#translation_edited_second_pass').text( data['statistics']['edited_second_pass'] );
            }
        });
        return this;
    },
    closeAlertRows: function(){
        $('tr.alert-row').remove();
        return this;
    },
    spawnAlert: function(data){
        var alert_div = this.find('.alert-text-div');
        alert_div
            .text( data['responseJSON']['message'] );
        if (data['responseJSON']['errors']){
            var error_html = "<ul>";
            $.each(data['responseJSON']['errors'], function(key, value){
                error_html += ('<li>Поле "' + (window.translation_errors_codes)[key] + '": ' + value + '</li>');
            });
            error_html += "</ul>";
            alert_div.html( alert_div.html() + error_html);
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

    $('a.close').on('click', function(e){
        var close_link = $( e.currentTarget );
        close_link.closeAlertRows();
    });

    $('.translation-chapter-edit').on('click', function(e){
        var edit_link = $( e.currentTarget );
        edit_link.collapseAll().closeAlertRows();
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
        translation_row_old.collapseTC().closeAlertRows();
        return false;
    });

    $('.btn-save-translation-chapter').on('click', function(e){
        var save_link = $( e.currentTarget );
        var translation_row = save_link.closest('.translation-chapter-expanded');
        translation_row.closeAlertRows();
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
            if (data['movement']){
                location.reload();
            } else {
                if (data['status'] && (data['status'] !== 200)){
                    var alert_example = $('.alert-row-example');
                    translation_row.before( alert_example.clone(true, true) );
                    var alert_row = translation_row.prev();
                    alert_row.spawnAlert(data);
                    alert_row.find('div')
                        .fadeIn();
                    alert_row
                        .removeClass('alert-row-example')
                        .addClass('alert-row')
                        .removeClass('editing-row-hidden');
                } else{
                    var return_data = data['data'];
                    translation_row.attr('data_translated', return_data['new_translated']);
                    translation_row.attr('data_total_rows', return_data['total']);
                    translation_row.attr('data_edited_first_pass', return_data['new_edited_first_pass']);
                    translation_row.attr('data_edited_second_pass', return_data['new_edited_second_pass']);
                    translation_row.attr('data_title', return_data['title']);
                    translation_row.attr('data_script_title', return_data['script_title']);
                    translation_row = translation_row.collapseTC().showRecalculate();
                    translation_row.find('.item_name').find('span').text(return_data['script_title']);
                }
            }
        });

        return false;
    });

    $('.add-chapter').on('click', function(e){
        var add_chapter_link = $( e.currentTarget );
        add_chapter_link.collapseAll().closeAlertRows();
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
        translation_row_add.collapseAC(is_chapter).closeAlertRows();
        return false;
    });

    $('.btn-new-translation-chapter').on('click', function(e){
        var add_chapter_link = $( e.currentTarget );
        var translation_row = add_chapter_link.closest('.add-row-expanded');
        translation_row.closeAlertRows();
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
            url: add_chapter_link.attr('href'),
            method: 'GET',
            data: data,
            type: 'json'
        }).always(function(data){
            if (data['id']){
                location.reload();
            } else {
                if (data['status'] && (data['status'] !== 200)){
                    var alert_example = $('.alert-row-example');
                    translation_row.before( alert_example.clone(true, true) );
                    var alert_row = translation_row.prev();
                    alert_row.spawnAlert(data);
                    alert_row.find('div')
                        .fadeIn();
                    alert_row
                        .removeClass('alert-row-example')
                        .addClass('alert-row')
                        .removeClass('editing-row-hidden');
                }
            }
        });

        return false;
    });

    $('.translation-chapter-delete-popup').on('click', function(e){
        var delete_chapter_link = $( e.currentTarget );
        var translation_row = delete_chapter_link.closest('.translation-chapter-collapsed');
        translation_row.closeAlertRows();
        var item_id = translation_row.attr('data_id');
        var popup_window = $("#delete-chapter-popup");
        popup_window.find('h3').text('Действительно удалить ' + translation_row.attr('data_script_title') + '?');
        popup_window.attr('data_id', item_id);
        var text = $("p#delete-chapter-popup-additional-text");
        text.css('display', 'none');
        text.text('');
        $.ajax({
            url: '/api/translation/'+delete_chapter_link.attr('alias')+'/get-children',
            method: 'GET',
            data: {'translation_chapter_id': item_id},
            type: 'json'
        }).always(function(data){
            if (data['children'] && (data['children'].length > 0)){
                var text = $("p#delete-chapter-popup-additional-text");
                text.append('<p>Это действие удалит следующие главы и разделы:</p>');
                $.each(data['children'], function(idx, val){
                    text.append('<p>' + val['title'] + '</p>');
                });
                text.css('display', 'block');
            }
        });
    });

    $('.translation-chapter-delete-popup').magnificPopup({
        type: 'inline',
        preloader: false,
        modal: true
    });

    $(document).on('click', '.popup-modal-dismiss', function (e){
        $.magnificPopup.close();
        return false;
    });

    $('.delete-chapter-btn').on('click', function(e){
        var block = $("#delete-chapter-popup");
        var data = {};
        data['translation_item_id'] = parseInt(block.attr('data_translation_item'));
        data['translation_chapter_id'] = parseInt(block.attr('data_id'));
        block.closeAlertRows();
        $.ajax({
            url: '/api/translation/'+block.attr('data_alias')+'/delete-chapter',
            method: 'GET',
            data: data,
            type: 'json'
        }).always(function(data){
            if (data['delete_results']){
                location.reload();
            }
        });
        return false;
    });

    $('.edit-comment-send').on('click', function(e){
        var edit_link = $( e.currentTarget );
        var link_id = edit_link.attr('id');
        var type = '';
        switch(link_id){
            case 'save-pictures-description':
                type = 'pictures';
                break;
            case 'save-tech-description':
                type = 'tech';
                break;
            case 'save-comment-description':
                type = 'comment';
                break;
            default:
                return false;
        }

        var data = {};
        var block = $("#delete-chapter-popup");
        data['translation_item_id'] = parseInt(block.attr('data_translation_item'));
        data['description'] = edit_link.prev('textarea').val();
        data['type'] = type;

        $.ajax({
            url: '/api/translation/'+block.attr('data_alias')+'/edit-comment',
            method: 'GET',
            data: data,
            type: 'json'
        }).always(function(data){
            if (data['description']){
                edit_link.prev('textarea').val( data['description'] );
            }
        });

        return false;
    });

    $('.subscription-button').on('click', function (e) {
        var subscription_link = $( e.currentTarget );

        $.ajax({
            url: subscription_link.attr('href'),
            method: 'GET',
            type: 'json'
        }).always(function(data){
            location.reload();
        });

        return false;
    });

});
