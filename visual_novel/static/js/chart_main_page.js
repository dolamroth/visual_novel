$(function () {
    $("img.poster-img").each(function(idx){
        var $this = $(this);
        $this.attr('src', $this.attr('data_url'));
    });
});
