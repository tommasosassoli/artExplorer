let actualPage = 0;

function insertItem(img_url, title, year) {
    let item = $('.item.to-clone').clone().removeClass('to-clone')
    item.find('img').attr('src', img_url)
    item.find('.title-ban p').text(title)
    item.find('.year').text(year)
    item.on('click', function (event) {
        event.preventDefault()
        window.location = '/' + encodeURI(title)
    })
    item.hover(function() {
        $(this).find('.detail-ban').slideToggle("show");
    });

    $('.art-container').append(item)
}

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
                    insertItem(res.img_url, res.title, res.year)
                });
            },
            error: function () {
                console.error('error on search artworks ajax')
            }
        });
    }
}

function nextPage() {
    actualPage += 1
    $.ajax({
        url: '/api/page/' + actualPage,
        datatype: 'json',
        success: function (result) {
            console.log(result)
            $('.item:not(.to-clone)').remove()
            result.forEach((res) => {
                insertItem(res.img_url, res.title, res.year)
            });
        },
        error: function () {
            actualPage -= 1
            console.error('error on page artworks ajax')
        }
    });
}

function previousPage() {
    if (actualPage > 0) {
        actualPage -= 1
        $.ajax({
            url: '/api/page/' + actualPage,
            datatype: 'json',
            success: function (result) {
                console.log(result)
                $('.item:not(.to-clone)').remove()
                result.forEach((res) => {
                    insertItem(res.img_url, res.title, res.year)
                });
            },
            error: function () {
                actualPage += 1
                console.error('error on page artworks ajax')
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