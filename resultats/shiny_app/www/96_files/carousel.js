if (typeof slideTo == 'undefined') {
    var slideTo = null;
}
window.onload = function() {
    // Envoie event à Google quand on clique sur ajout au panier depuis le crosssell produits du même rayon sur fiche produit
    $('.ga_side_products').click(function(event) {
        event.preventDefault();
        var productid = $(this).data('productId');
        var productid_dest = $(this).data('productIdDestination');
        var url = $(this).attr("href");
        ga('send', 'event', 'fiche_produit', 'slider_produits', '' + productid + '_' + productid_dest + '');
        document.location.href = url;
    });
    /*
    Slider : FP - produits du meme rayon
    */
    $('#slider_fp_cat').on('init', function(event, slick) {
        $('#slider_fp_cat_container').css('height', '220px');
        $('#slider_fp_cat_container').css('visibility', 'visible');
    });
    $('#slider_fp_cat').slick({
        dots: false,
        slickGoTo: 10,
        slidesToShow: 3,
        slidesToScroll: 2,
        centerMode: false,
        infinite: false,
        // initialSlide: slideTo,
        responsive: [{
            breakpoint: 992,
            settings: "unslick"
        }]
    });
    // init greenweez in-house crosssell slider on product page
    $('#product_info_crosssell_greenweez').on('init', function(event, slick) {
        $('#product_info_crosssell_greenweez_container').css('height', '220px');
        $('#product_info_crosssell_greenweez_container').css('visibility', 'visible');
    });
    $('#product_info_crosssell_greenweez').slick({
        dots: false,
        slickGoTo: 10,
        slidesToShow: 3,
        slidesToScroll: 2,
        centerMode: false,
        infinite: false,
        // initialSlide: slideTo,
        responsive: [{
            breakpoint: 992,
            settings: "unslick"
        }]
    });
    // init greenweez in-house crosssell slider on product page
    $('#product_info_crosssell_gwz_similar_products').on('init', function(event, slick) {
        $('#product_info_crosssell_gwz_similar_products_container').css('height', '220px');
        $('#product_info_crosssell_gwz_similar_products_container').css('visibility', 'visible');
    });
    $('#product_info_crosssell_gwz_similar_products').slick({
        dots: false,
        slickGoTo: 10,
        slidesToShow: 3,
        slidesToScroll: 2,
        centerMode: false,
        infinite: false,
        // initialSlide: slideTo,
        responsive: [{
            breakpoint: 992,
            settings: "unslick"
        }]
    })
    /*
    Slider : Guide d'achat
    */
    $('.slider_guide').on('init', function(event, slick) {
        $('.carousel_guide').css('visibility', 'visible');
    });
    $('.slider_guide').slick({
        dots: false,
        slidesToShow: 4,
        slidesToScroll: 3,
        initialSlide: 1,
        centerMode: false,
        infinite: true,
        responsive: [{
            breakpoint: 992,
            settings: "unslick"
        }]
    });
    /*
    Slider : Panier - produits oubliés
    */
    /*$('.slider_panier_oubli').on('init', function(event, slick) {
        console.log("test");
        $('#produits_oublies').css('visibility', 'visible');
    });

    if ( deviceType == "isTablet") {
        console.log("sldier !");
        $('.slider_panier_oubli').slick({
            dots          : false,
            slidesToShow  : 4,
            slidesToScroll: 4,
            centerMode    : false,
            infinite      : false,
        });
    }else{
        console.log("init slider");

        $('.slider_panier_oubli').slick({
            dots: false,
            slidesToShow: 4,
            slidesToScroll: 3,
            centerMode: false,
            infinite: false,
            responsive: [{
                breakpoint: 989,
                settings  : "unslick"
            }]
        });
    }*/
}