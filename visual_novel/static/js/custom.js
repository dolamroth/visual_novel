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

window.betalink_errors_codes = {
    "translation_item_id": "Уникальный идентификатор перевода",
    "title": "Пользовательское название",
    "url": "URL",
    "comment": "Комментарий"
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
    spawnAlert: function(data, error_codes){
        var alert_div = this.find('.alert-text-div');
        alert_div
            .text( data['responseJSON']['message'] );
        if (data['responseJSON']['errors']){
            var error_html = "<ul>";
            $.each(data['responseJSON']['errors'], function(key, value){
                error_html += ('<li>Поле "' + error_codes[key] + '": ' + value + '</li>');
            });
            error_html += "</ul>";
            alert_div.html( alert_div.html() + error_html);
        }
        return this;
    },
    spawnAlertBottom: function(data){
        var alert_example = $('.alert-row-example');
        var block = $('#delete-betalink-popup');
        var translation_row = $('tr[data_alias='+block.attr('data_alias')+']').last().next().next();
        translation_row.after( alert_example.clone(true, true) );
        var alert_row = translation_row.next();
        alert_row.spawnAlert(data, window.translation_errors_codes);
        alert_row.find('div')
            .fadeIn();
        alert_row
            .removeClass('alert-row-example')
            .addClass('alert-row')
            .removeClass('editing-row-hidden');
    },
    collapseBetaLinkEdit: function(){
        var betalink_expanded_row = this;
        var example_row = $(".betallink-collapsed-edit-row-example");
        this.replaceWith( example_row.clone(true, true) );
        var translation_row = $(".betallink-collapsed-edit-row-example").first();
        translation_row.trigger('create');
        $.each(betalink_expanded_row.prop('attributes'), function() {
            translation_row.attr(this.name, this.value);
        });
        var new_html = "";
        new_html += "<strong>" + translation_row.attr('betalink_title') + "</strong><br />";
        new_html += "<a href="+translation_row.attr('betalink_url')+" target='_blank'>"+translation_row.attr('betalink_url')+"</a><br />";
        new_html += translation_row.attr('betalink_comment') + "<br />";
        var approved = (translation_row.attr('betalink_approved') === "True");
        var rejected = (translation_row.attr('betalink_rejected') === "True");
        if (approved){
            new_html += "<span style=\"color:#118339\">Подтвержденная ссылка</span>";
        } else {
            if (rejected){
                new_html += "<span style=\"color:#dc301f\">Ссылка отклонена</span>";
            } else {
                new_html += "<span style=\"color:#ffa121\">Ссылка не подтверждена</span>";
            }
        }
        translation_row.find('td').first().html( new_html );
        translation_row
            .removeClass('betallink-collapsed-edit-row-example')
            .removeClass('betalink-row-expanded')
            .addClass('betalink-row-collapsed')
            .removeClass('editing-row-hidden');
        return translation_row;
    },
    collapseBetaLinkAdd: function(){
        var betalink_add_row = this;
        var example_row = $(".betallink-collapsed-add-row-example");
        this.replaceWith( example_row.clone(true, true) );
        var translation_row = $(".betallink-collapsed-add-row-example").first();
        translation_row.trigger('create');
        translation_row
            .removeClass('betallink-collapsed-add-row-example')
            .addClass('betalink-row-add-collapsed')
            .removeClass("betalink-row-add-expanded")
            .removeClass('editing-row-hidden');
        return translation_row;
    },
    collapseBetaLinkAll: function(){
        var expanded = $('.betalink-row-expanded');
        if (expanded.length > 0){
            expanded.first().collapseBetaLinkEdit();
        }
        expanded = $('.betalink-row-add-expanded');
        if (expanded.length > 0){
            expanded.first().collapseBetaLinkAdd();
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
                    alert_row.spawnAlert(data, window.translation_errors_codes);
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
                    alert_row.spawnAlert(data, window.translation_errors_codes);
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
            url: '/api/translation/'+translation_row.attr('data_alias')+'/get-children',
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
        var tci = data['translation_chapter_id'];
        block.closeAlertRows();
        $.ajax({
            url: '/api/translation/'+block.attr('data_alias')+'/delete-chapter',
            method: 'GET',
            data: data,
            type: 'json'
        }).always(function(data){
            if (data['delete_results']){
                location.reload();
            } else {
                $.magnificPopup.close();
                var alert_example = $('.alert-row-example');
                var translation_row = $('tr[data_id='+tci+']');
                translation_row.before( alert_example.clone(true, true) );
                var alert_row = translation_row.prev();
                alert_row.spawnAlert(data, window.translation_errors_codes);
                alert_row.find('div')
                    .fadeIn();
                alert_row
                    .removeClass('alert-row-example')
                    .addClass('alert-row')
                    .removeClass('editing-row-hidden');
            }
        });
        return false;
    });

    $('.edit-comment-send').on('click', function(e){
        var edit_link = $( e.currentTarget );
        var link_id = edit_link.attr('id');
        var type = '';
        var old_text = edit_link.attr('data_text');
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
            } else {
                edit_link.spawnAlertBottom(data);
                $('#'+link_id).prev('textarea').val( old_text );
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
            /* TODO: Rewrite without reload */
            location.reload();
        });

        return false;
    });

    $('.translation-betalink-edit').on('click', function(e){
        var edit_link = $( e.currentTarget );
        edit_link.collapseBetaLinkAll().closeAlertRows();
        var edit_row = edit_link.closest('.betalink-row-collapsed');
        var approved = edit_row.attr("betalink_approved");
        var rejected = edit_row.attr("betalink_rejected");
        var title = edit_row.attr("betalink_title");
        var url = edit_row.attr("betalink_url");
        var comment = edit_row.attr("betalink_comment");
        var example_row = $(".edit-betalink-example");
        edit_row.replaceWith( example_row.clone(true, true) );
        var betalink_row_add = $(".edit-betalink-example").first();
        betalink_row_add.trigger('create');
        $.each(edit_row.prop('attributes'), function() {
            betalink_row_add.attr(this.name, this.value);
        });
        betalink_row_add.find('.input_betalink_title').val( title );
        betalink_row_add.find('.input_betalink_url').val( url );
        betalink_row_add.find('.input_betalink_comment').val( comment );
        betalink_row_add
            .removeClass("edit-betalink-example")
            .removeClass("editing-row-hidden")
            .removeClass("betalink-row-collapsed")
            .addClass("betalink-row-expanded");
        return false;
    });

    $('.add-betalink-link').on('click', function(e){
        var add_link = $( e.currentTarget );
        var add_row = add_link.closest('tr.add-betalink-row');
        add_row.collapseBetaLinkAll().closeAlertRows();
        var example_row = $(".add-betalink-example");
        add_row.replaceWith( example_row.clone(true, true) );
        var betalink_row_add = $(".add-betalink-row").first();
        betalink_row_add
            .removeClass("add-betalink-example")
            .removeClass("editing-row-hidden")
            .removeClass("betalink-row-add-collapsed")
            .addClass("betalink-row-add-expanded");
        return false;
    });

    $(".btn-cancel-betalink").on('click', function(e){
        var cancel_link = $( e.currentTarget );
        var edit_row = cancel_link.closest(".betalink-row-expanded");
        edit_row.collapseBetaLinkEdit().closeAlertRows();
        return false;
    });

    $(".btn-cancel-add-betalink").on("click", function(e){
        var cancel_link = $( e.currentTarget );
        var add_row = cancel_link.closest(".betalink-row-add-expanded");
        add_row.collapseBetaLinkAdd().closeAlertRows();
        return false;
    });

    $(".btn-save-add-betalink").on('click', function(e){
        var add_link = $( e.currentTarget );
        var add_row = add_link.closest(".betalink-row-add-expanded");
        add_row.closeAlertRows();
        var data = {};
        data['data_translation_item'] = parseInt(add_row.attr('data_translation_item'));
        data['title'] = add_row.find('.input_betalink_title').val();
        data['url'] = add_row.find('.input_betalink_url').val();
        data['comment'] = add_row.find('.input_betalink_comment').val();

        $.ajax({
            url: add_link.attr('href'),
            method: 'GET',
            type: 'json',
            data: data
        }).always(function(data){
            if (data['status'] && (data['status'] !== 200)){
                var alert_example = $('.betalink-alert-row-example');
                add_row.before( alert_example.clone(true, true) );
                var alert_row = add_row.prev();
                alert_row.spawnAlert(data, window.betalink_errors_codes);
                alert_row.find('div')
                    .fadeIn();
                alert_row
                    .removeClass('betalink-alert-row-example')
                    .addClass('alert-row')
                    .removeClass('editing-row-hidden');
            } else {
                var return_data = data['data'];
                var example_row = $(".edit-betalink-example");
                add_row.before( example_row.clone(true, true) );
                var new_added_row = add_row.prev();
                new_added_row.trigger('create');
                new_added_row.attr('betalink_title', return_data['title']);
                new_added_row.attr('betalink_url', return_data['url']);
                new_added_row.attr('betalink_comment', return_data['comment']);
                new_added_row.attr('betalink_approved', return_data['approved']);
                new_added_row.attr('betalink_rejected', return_data['rejected']);
                new_added_row.attr('data_translation_item', return_data['translation_item_id']);
                new_added_row.attr('betalink_id', return_data['betalink_id']);
                new_added_row = new_added_row.collapseBetaLinkEdit().closeAlertRows();
                add_row.collapseBetaLinkAdd();
            }
        });

        return false;
    });

    $(".btn-save-betalink").on('click', function(e){
        var edit_link = $( e.currentTarget );
        var edit_row = edit_link.closest(".betalink-row-expanded");
        edit_row.closeAlertRows();
        var data = {};
        data['data_translation_item'] = parseInt(edit_row.attr('data_translation_item'));
        data['title'] = edit_row.find('.input_betalink_title').val();
        data['url'] = edit_row.find('.input_betalink_url').val();
        data['comment'] = edit_row.find('.input_betalink_comment').val();
        data['betalink_id'] = parseInt(edit_row.attr('betalink_id'));
        $.ajax({
            url: edit_link.attr('href'),
            method: 'GET',
            type: 'json',
            data: data
        }).always(function(data){
            if (data['status'] && (data['status'] !== 200)){
                var alert_example = $('.betalink-alert-row-example');
                edit_row.before( alert_example.clone(true, true) );
                var alert_row = edit_row.prev();
                alert_row.spawnAlert(data, window.betalink_errors_codes);
                alert_row.find('div')
                    .fadeIn();
                alert_row
                    .removeClass('betalink-alert-row-example')
                    .addClass('alert-row')
                    .removeClass('editing-row-hidden');
            } else {
                var return_data = data['data'];
                edit_row.attr('betalink_title', return_data['title']);
                edit_row.attr('betalink_url', return_data['url']);
                edit_row.attr('betalink_comment', return_data['comment']);
                edit_row.attr('betalink_approved', return_data['approved']);
                edit_row.attr('betalink_rejected', return_data['rejected']);
                edit_row.attr('data_translation_item', return_data['translation_item_id']);
                edit_row = edit_row.collapseBetaLinkEdit().closeAlertRows();
            }
        });
        return false;
    });

    $('.translation-betalink-delete-popup').on('click', function(e){
        var delete_chapter_link = $( e.currentTarget );
        var betalink_row = delete_chapter_link.closest('.betalink-row-collapsed');
        betalink_row.closeAlertRows();
        var item_id = betalink_row.attr('betalink_id');
        var popup_window = $("#delete-betalink-popup");
        popup_window.attr('data_id', item_id);
    });

    $('.translation-betalink-delete-popup').magnificPopup({
        type: 'inline',
        preloader: false,
        modal: true
    });

    $('.delete-betalink-btn').on('click', function(e){
        var block = $("#delete-betalink-popup");
        var data = {};
        data['betalink_id'] = parseInt(block.attr('data_id'));
        console.log(data);
        block.closeAlertRows();
        $.ajax({
            url: '/api/translation/'+block.attr('data_alias')+'/deletebetalink',
            method: 'GET',
            data: data,
            type: 'json'
        }).always(function(data){
            if (data['delete_results']){
                /* TODO: Manually remove betalink from page, without reload */
                location.reload();
            }
        });
        return false;
    });

    $('.update-user-subscription-settings').on('click', function(e){
        var submit_link = $( e.currentTarget );
        var weekdays = 0;
        $.each( $(".weekday-checkbox:checked"), function(idx, val){ weekdays += parseInt(val.value) }  );
        var is_subscribed = $('#distribution-check').prop('checked');
        var time = $('#distribution-time').val();
        var vk_link = $('#vk-link').val();
        var data = {
            'weekmap': weekdays,
            'is_subscribed': is_subscribed,
            'time': time,
            'vk_link': vk_link
        };
        $.ajax({
            url: '/api/core/'+submit_link.attr('username')+'/subscriptions_edit',
            method: 'GET',
            data: data,
            type: 'json'
        }).always(function(data){
            /* TODO: manually change button and data on page, without reload */
            location.reload();
        });
        return false;
    });

    $('.select-translation-status-popup').on('click', function(e){
        var status_link = $( e.currentTarget );
        var popup_window = $('#change-translation-status-popup');
        var current_status = $('#current-translation-status').attr('data-status');
        var new_status = status_link.attr('data-key');

        var text = $("p#change-status-popup-additional-text");
        text.css('display', 'none');
        text.text('');

        if (current_status === new_status){
            $('#translation-statuses').dropdown('toggle');
            $(e).preventDefault();
            return false;
        }
        popup_window.attr('data_status', new_status);

        var status_span = status_link.find('span');
        popup_window.attr('data_status_name', status_span.text() );
        popup_window.attr('data_status_style', status_span.attr('class') );

        text.text( status_link.attr('data-description') );
        text.css('display', 'block');
    });

    $('.select-translation-status-popup').magnificPopup({
        type: 'inline',
        preloader: false,
        modal: true
    });

    $('.change-status-btn').on('click', function(e){
        var popup_window = $('#change-translation-status-popup');
        var data = {
            'status': popup_window.attr('data_status'),
            'translation_item_id': popup_window.attr('data_translation_item')
        };
        $.ajax({
            url: '/api/translation/'+popup_window.attr('data_alias')+'/change-status',
            method: 'GET',
            data: data,
            type: 'json'
        }).always(function(data){
            $.magnificPopup.close();
            var current_status = $('#current-translation-status');
            if(data['status'] && data['status'] !== 200){
                current_status.spawnAlertBottom(data);
            } else {
                current_status.removeClass();
                current_status.text( popup_window.attr('data_status_name') );
                current_status.addClass( popup_window.attr('data_status_style') );
                current_status.attr('data-status', popup_window.attr('data_status'));
            }
        });
        return false;
    });

});
