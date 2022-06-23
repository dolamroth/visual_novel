window.news_page = 1;
window.total_pages = 1;
window.pagination_current_page = 0;
window.pagination_total_pages = 0;
window.news_interval = null;


var UpdatePagination = function(pagination){
    var list = $("#ul-pagination");
    list.find('li').remove();
    $.each(pagination, function(idx, val){
        if (!val['link']){
            list.append( "<li class=\"page-item disabled\"><a class=\"page-link\" href=\"#\" tabindex=\"-1\">...</a></li>" )
        } else {
            if (val['active']){
                list.append( "<li class=\"page-item active\"><a class=\"page-link\" href=\"#\" data-link='"+ val['page'] +"'>"+ val['page'] +"</a></li>" )
            } else {
                list.append( "<li class=\"page-item\"><a class=\"page-link\" href=\"#\" data-link='"+ val['page'] +"'>"+ val['page'] +"</a></li>" )
            }
        }
    });
    $("li.page-item").not(".disabled").find('a').on('click', function(e){
        var page_link = $( e.currentTarget );
        var page_n = parseInt(page_link.attr('data-link'));
        clearInterval(window.news_interval);
        window.news_page = page_n;
        window.news_interval = setTimeout(function(){ UploadNews(true); }, 0);
        return false;
    });
    $("li.disabled").find('a').on('click', function(){
        return false;
    });
    window.pagination_current_page = window.news_page;
    window.pagination_total_pages = window.total_pages;
};


var reloadNewsOnPage = function(news){
    var table = $('#news-list-table');
    var current_rows_count = table.find('tr.news').length;
    var example_row = $(".hidden-news");
    table.find('tr.news').remove();
    for(i=news.length-1; i>=0; i--){
        var val = news[i];
        var row = example_row
            .clone(true, true)
            .trigger('create')
            .removeClass('hidden-news')
            .addClass('news');
        row.find('div.title').html( '<a href="/news/' + val['alias'] + '">' + val['title'] + '</a>');
        row.find('div.short_description').html( val['short_description'] );
        row.find('div.poster').html( '<img src="'+val['poster_url']+'" style="height: 350px; width: auto; max-width: 730px;">' );
        row.find('div.author').html( 'Дата добавления: ' + val['created_at'] + '; автор: ' + val['author'] );
        table.prepend(row);
    }
};


var UploadNews = function(){
    $.ajax({
        url: '/api/news/all',
        method: 'GET',
        data: {
            'start_page': window.news_page
        },
        type: 'json'
    }).always(function(data){
        if (data['total_news']){
            reloadNewsOnPage(data['news']);
            window.news_page = data['current_page'];
            window.total_pages = data['total_pages'];
            if ((window.pagination_current_page !== window.news_page) || (window.pagination_total_pages !== window.total_pages)){
                UpdatePagination(data['pagination']);
            }
        }
    });
};


$(function () {
    window.news_interval = setTimeout(function(){ UploadNews(); }, 0);
});
