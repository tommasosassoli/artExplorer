$(document).ready(function() {
    $(".item").hover(function() {
        $(this).find('.detail-ban').slideToggle("show");
    });
});