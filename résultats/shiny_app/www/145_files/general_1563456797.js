$(document).ready(function() {
    switch_to_mobile();
    switch_to_desktop();
    autocompleteGwz(document.getElementById('search'));
    $('[data-toggle="tooltip"]').tooltip();



      
    //Check si on a un hashtag après l'url
    var hashtag = location.hash;
    if (hashtag != '') {
        //Si le hashtag n'est pas vide (ouverture menu sur AMP)
        var strFilter = hashtag.substring(1);
        if (strFilter == 'from_amp=1&show_menu=1') {
            $('#navbarNav').modal('show');
        }
    }
    if (errorConnection == 1) {
        display_connexion();
    }
    // Cookie : close banner
    $('#cookies_banner_close').click(function() {
        $('#cookies_banner_close').parent().addClass('cookies_banner_hidden');
        var expires = new Date();
        expires.setTime(expires.getTime() + 31536000000); // 1 an
        document.cookie = "accepte_cookie" + '=' + "ok" + ';expires=' + expires.toUTCString();
    });
    // Menu : action sur icon plus / moins
    $('.show_submenu2').on('click', function() {
        var id = $(this).attr("data-id");
        $('.layer_menu2').each(function() {
            var select = $(this).attr("id").split('_');
            var reference_id = select[1];
            if ($(this).is(':visible') && reference_id != id) {
                $(this).toggle('blind');
                var el = $("span[data-id='" + reference_id + "']");
                el.toggleClass("fa-plus fa-minus");
            }
        });
        $('#layer_' + id).toggle("blind");
        $(this).toggleClass("fa-plus fa-minus");
    });
    $('.show_submenu3').on('click', function() {
        var id = $(this).attr("data-id");
        $('.categories_n3').each(function() {
            var reference_id = $(this).attr("data-reference-id");
            if ($(this).is(':visible') && reference_id != id) {
                $(this).toggle('blind');
                var el = $("span[data-id='" + reference_id + "']");
                el.toggleClass("fa-plus fa-minus");
            }
        });
        $('#n3_' + id).toggle("blind");
        $(this).toggleClass("fa-plus fa-minus");
    });
    $('#search').on('click', function() {
        $('#search_ok').addClass('fa-close');
    });
    $('#search_ok').on('click', function() {
        $('#search_ok').removeClass('fa-close').addClass('fa-search');
        $('#search').val('');
        // Close the autocomplete search
        //$('.ui-autocomplete').removeClass('open');
        $('#search-ul-id-1').remove();
        $('.container-fluid').show();
        $('#footer').show();
    });
    // Mot de passe oublié
    $('.mdp_oublie').on('click', function() {
        $('#form_connexion_mon_compte').toggleClass('lower_connexion_hide');
        $('.connexion_reset_password').toggleClass('lower_connexion_show');
        $('.mdp_oublie').toggleClass('mdp_oublie_retour');
    });
    $('#formulaire_connexion_mon_compte_modal').on('click', function() {
        modal_forgot_password('');
    });
    $('#responsive_formulaire_connexion_mon_compte_modal').on('click', function() {
        modal_forgot_password('responsive_');
    });
    // Connexion
    $('#formulaire_connexion_mon_compte_responsive').on('click', function() {
        valid_connexion();
    });
    $('.compte_deco_off_responsive').on('click', function() {
        display_connexion();
    });
    $('.redirect_to_connexion').on('click', function(e) {
        e.preventDefault();
        if ($(window).width() < 992) {
            var page = $(this).attr("data-page");
            window.location.href = 'responsive.php?action=connexion&page=' + page;
        } else {
            $('#layer_compte_off').slideToggle();
        }
    });
    $('#btn_connexion_responsive').on('click', function() {
        var my_login = $('#responsive_email').val();
        var my_password = CryptoJS.MD5($('#responsive_password').val()).toString();
        var my_session = 0;
        if ($('#responsive_persist_box').is(':checked')) {
            my_session = 1;
        }
        var provenance_panier_responsive = $('#provenance_panier_responsive').val();
        var url = '';
        var redirection = $('#redirect_page').val();
        if (redirection == '') {
            var url = sessionStorage.getItem('url');
        }
        $.ajax({
            dataType: 'json',
            type: "POST",
            url: './connexion.php',
            data: {
                "action": "process",
                "email_address": my_login,
                "password": my_password,
                "session": my_session,
                "panier": provenance_panier_responsive,
            }
        }).done(function(data) {
            if (data.erreur) {
                $('#responsive_message_alerte_connexion').empty().html(data.erreur_message).show();
            } else {
                if (redirection == 'contact') {
                    window.location.href = '/customer-service';
                } else if (redirection == 'weezlist') {
                    window.location.href = 'list.php';
                } else if (redirection == 'shopping') {
                    window.location.href = 'shopping_cart.php';
                } else if (redirection == '') {
                    window.location.href = url;
                }
            }
        });
    });
    $('#password_visibility').on('click', function(e) {
        e.preventDefault();
        if ($(this).prev('input').attr('type') == 'password') {
            changeType($(this).prev('input'), 'text');
            $(this).removeClass("fa-eye").addClass("fa-eye-slash");
        } else {
            changeType($(this).prev('input'), 'password');
            $(this).removeClass("fa-eye-slash").addClass("fa-eye");
        }
        return false;
    });
    $('#div_deconnexion_mon_compte').on('click', function() {
        $.getJSON("./deconnexion.php", {
            "action": "process"
        }, function(data) {
            if (!data.erreur) {
                if (data.redirection != "") {
                    document.location.href = data.redirection;
                }
            }
        });
    });
    $('#link_monpanier').mouseover(function() {
        $('.layer_header_compte').fadeOut('fast', function() {
            $('#layer_panier').show();
        });
    }).mouseout(function() {
        $('#layer_panier').hide();
    });
    $('#layer_panier').mouseenter(function() {
        $('#layer_panier').show();
    }).mouseleave(function() {
        $('#layer_panier').hide();
    });
    $('#menu_compte').mouseover(function() {
        $('#layer_compte_on').show();
    });
    $('#layer_compte_on').mouseenter(function() {
        $('#layer_compte_on').show();
    }).mouseleave(function() {
        $('#layer_compte_on').fadeOut();
    });
    $('.btn_close_log').click(function() {
        $('#layer_compte_off').slideToggle();
    });
    /*menu hides on mobile when scrolling down*/
    if ($(window).width() < 992) {
        'use strict';
        var c, currentScrollTop = 0,
            navbar = $('header');
        $(window).scroll(function() {
            var a = $(window).scrollTop();
            var b = navbar.height();
            currentScrollTop = a;
            if (c < currentScrollTop && a > b ) {
                navbar.addClass("scrollUp");
            } else if (c > currentScrollTop && !(a <= b)) {
                navbar.removeClass("scrollUp");
            }
            c = currentScrollTop;
        });
        $('.product_to_cart').click(function() {
            navbar.removeClass("scrollUp");
        });
        $("#search").attr("placeholder", "Recherche");
    } else if ($(window).width() > 992) {
        /*footer code promo déplié en desktop*/
        $('#accordion_codepromo_target').addClass('show');
    }

    // asterisque sur menu frais
    var asterisk = document.createElement('div');
    asterisk.setAttribute('class', 'fa fa-asterisk ml-2');
    $(asterisk).appendTo('#lien_4023');

});