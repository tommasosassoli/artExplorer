function searchArtworks() {
    let title = $('#search-input').val()
    if (title !== "") {
        $.ajax({
            url: '/api/search/' + encodeURI(title),
            datatype: 'json',
            success: function (result) {
                console.log(result)
                $('.item:not(.to-clone)').remove()
                result.forEach((res) => {
                    let item = $('.item.to-clone').clone().removeClass('to-clone')
                    item.find('img').attr('src', res.img_url)
                    item.find('.title-ban p').text(res.title)
                    item.find('.year').text(res.year)
                    item.on('click', function (event) {
                        event.preventDefault()
                        window.location = '/' + encodeURI(res.title)
                    })
                    item.hover(function() {
                        $(this).find('.detail-ban').slideToggle("show");
                    });

                    $('.container').append(item)
                });
            },
            error: function () {
                console.error('error on search artworks ajax')
            }
        });
    }
}

$(document).ready(function() {
    $(".item").hover(function() {
        $(this).find('.detail-ban').slideToggle("show");
    });

    $('#search-input').keypress(function (event) {
      if (event.keyCode === 13) {
        event.preventDefault();
        searchArtworks();
      }
    })
});