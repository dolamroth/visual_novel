window.translations_interval = null;
window.statuses_list = null;
window.translators_list = null;


// Get data for dropdown selects
var GetListOfData = function(){
    $.ajax({
        url: '/api/translation/all/selects',
        method: 'GET',
        data: {},
        type: 'json'
    }).always(function(data){
        window.statuses_list = data['statuses'];
        window.translators_list = data['translators'];

        if ((typeof window.statuses_list === undefined) || (typeof window.translators_list === undefined)){
            return false;
        }

        var li_tag_example = $("#translation-statuses-li-example");
        for (i=0; i<(window.statuses_list).length; i++){
            var val = (window.statuses_list)[i];
            (window.statuses_list)[i]['checked'] = val['default'];
            var li_tag = li_tag_example
                .clone(true, true)
                .trigger('create')
                .removeAttr('id');
            li_tag.find('a').attr('data_id', val['key']);
            li_tag.find('span.li-text').html( val['name'] );
            li_tag.find('span.li-text').addClass( 'text-' + val['style'] );
            li_tag.find('input').prop('checked', val['checked']);
            $('#statuses-ul').append( li_tag );
        }

        var li_tag_example = $("#translator-li-example");
        for (i=0; i<(window.translators_list).length; i++){
            var val = (window.translators_list)[i];
            (window.translators_list)[i]['checked'] = true;
            var li_tag = li_tag_example
                .clone(true, true)
                .trigger('create')
                .removeAttr('id');
            li_tag.find('a').attr('data_id', val['id']);
            li_tag.find('span.li-text').html( val['name'] );
            li_tag.find('input').prop('checked', val['checked']);
            $('#translators-ul').append( li_tag );
        }

        bindEventsToDropdownsElements();

        window.translations_interval = setTimeout(function(){ UploadTranslation(); }, 0);
    });
};


// Function binds event listeners for elements of dropdown
var bindEventsToDropdownsElements = function(){
    $( '.dropdown-menu input' ).on( 'click', function(e){
        return false;
    });

    $( '.dropdown-menu#statuses-ul a' ).on( 'click', function( event ) {
        var $target = $( event.currentTarget ),
            val = $target.attr( 'data_id' ),
            $inp = $target.find( 'input' );

        clearInterval(window.translations_interval);

        for (i=0; i<(window.statuses_list).length; i++){
            if( (window.statuses_list)[i]['key'] === val ){
                (window.statuses_list)[i]['checked'] = !($inp.prop( 'checked'));
                $inp.prop('checked', !($inp.prop( 'checked')) );
            }
        }

        window.translations_interval = setTimeout(function(){ UploadTranslation(); }, 0);
        return false;
    });

    $( '.dropdown-menu#translators-ul a' ).on( 'click', function( event ) {
        var $target = $( event.currentTarget ),
            val = $target.attr( 'data_id' ),
            $inp = $target.find( 'input' );

        clearInterval(window.translations_interval);

        for (i=0; i<(window.translators_list).length; i++){
            if( (parseInt(window.translators_list[i]['id']) === parseInt(val) )){
                (window.translators_list)[i]['checked'] = !($inp.prop( 'checked'));
                $inp.prop('checked', !($inp.prop( 'checked')) );
            }
        }

        window.translations_interval = setTimeout(function(){ UploadTranslation(); }, 0);
        return false;
    });
};


var reloadTranslationsOnPage = function(translations){
    var table = $('#all-translations-list');
    var example_row = $("#translation-row-example");

    table.find('tr.translation').remove();
    table.find('tr.no-translation-found').remove();

    for(i=translations.length-1; i>=0; i--){
        var val = translations[i];
        var row = example_row
            .clone(true, true)
            .trigger('create')
            .removeClass('translation-list-hidden')
            .addClass('translation')
            .removeAttr('id');

        row.find('a.link-to-translation').attr('href', val['page_on_site']);
        row.find('span.translation-title').html( val['title'] );
        row.find('span.translation-last-update').html( val['last_update'] );
        row.find('span.translation-status').html( val['status_name'] );
        row.find('span.translation-status').addClass( 'text-' + val['status_style'] );
        row.find('span.translation_total_rows').html( val['total_rows'] );
        row.find('span.translation_translation').html( val['translated'] );
        row.find('span.translation_translation_perc').html( val['translated_perc'] );
        row.find('span.translation_edited_first_pass').html( val['edited_first_pass'] );
        row.find('span.translation_edited_first_pass_perc').html( val['edited_first_pass_perc'] );
        row.find('span.translation_edited_second_pass').html( val['edited_second_pass'] );
        row.find('span.translation_edited_second_pass_perc').html( val['edited_second_pass_perc'] );

        table.prepend(row);
    }

    if (translations.length === 0){
        var example_row = $("#no-translation-found-example");
        var row = example_row
            .clone(true, true)
            .trigger('create')
            .removeClass('translation-list-hidden')
            .addClass('no-translation-found')
            .removeAttr('id');
        table.append(row);
    }
};


var UploadTranslation = function(){
    $.ajax({
        url: '/api/translation/all',
        method: 'GET',
        data: {
            'statuses': JSON.stringify(window.statuses_list),
            'translators': JSON.stringify(window.translators_list)
        },
        type: 'json'
    }).always(function(data){
        if(data['translations']){
            reloadTranslationsOnPage(data['translations']);
        }
    });
};


$(function () {
    window.translations_interval = setTimeout(function(){ GetListOfData(); }, 0);
});
