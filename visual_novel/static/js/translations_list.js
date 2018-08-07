window.translations_interval = null;
window.statuses_list = null;


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
            'statuses': JSON.stringify(window.statuses_list)
        },
        type: 'json'
    }).always(function(data){
        if(data['translations']){
            reloadTranslationsOnPage(data['translations']);
        }
    });
};


$(function () {
    window.translations_interval = setTimeout(function(){ UploadTranslation(); }, 0);
});
