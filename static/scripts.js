function toggle_favourite(item) {

    let product_id = item.data('product_id'),
        heart = item.find('.bi');
    $.get(
        `${location.origin}/${product_id}`
    ).done(function (data) {
        if (data.favourite === true) {
            heart.addClass('bi-heart-fill').removeClass('bi-heart')
        } else {
            heart.addClass('bi-heart').removeClass('bi-heart-fill')
        }
    }).fail(function (error) {
        console.log(error)
    })
}