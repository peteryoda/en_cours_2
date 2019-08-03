var switch_to_mobile = function() {
    //Menu desktop qui passe en modal mobile
    if ($(window).width() < 992) {
        $("#responsive-menu-container").appendTo($("#mobile_navbar_services"));
        $('#navbarNav').addClass('modal left fade');
        $('#responsive-modal-dialog').addClass('modal-dialog');
        $('#responsive-modal-dialog').removeClass('mx-auto');
        $('#responsive-modal-content').addClass('modal-content');
        $('#responsive-modal-body').addClass('modal-body');
        $('#responsive-menu-container').addClass('container');
        $("#link_monpanier").prop('id', 'link_monpanier_mobile');
        /*landscape mobile listing en long*/
        if (window.matchMedia("(orientation: portrait)").matches) {
            $("#page_list_content").removeClass("landscape_mobile_listing");
        }
    }
}
var switch_to_desktop = function() {
    //Menu mobile qui repasse en desktop
    if ($(window).width() > 992) {
        $("#responsive-menu-container").appendTo($("#navbar_services"));
        $('#navbarNav').removeClass('modal left fade');
        $('#responsive-modal-dialog').removeClass('modal-dialog');
        $('#responsive-modal-dialog').addClass('mx-auto');
        $('#responsive-modal-content').removeClass('modal-content');
        $('#responsive-modal-body').removeClass('modal-body');
        $('#responsive-menu-container').removeClass('container');
        $("#link_monpanier_mobile").prop('id', 'link_monpanier');
        if (document.body.classList.contains('modal-open')) {
            $(document.body).removeClass('modal-open');
            $('.modal-backdrop').removeClass('show');
        }
    }
    if ($(window).width() < 992) {
        /*landscape mobile listing en long*/
        if (window.matchMedia("(orientation: landscape)").matches) {
            $("#page_list_content").addClass("landscape_mobile_listing");
        }
    }
}
$(window).scroll(function() {
    if ($(window).width() < 992) {
        if ($(window).scrollTop() > 70) {
            $('#main_search_form').addClass('responsive_search_form');
            $('#navbar_secondary').addClass('responsive_nav_bar');
            $('#responsive-modal-dialog').addClass('responsive_modal_menu');
            $('#listing_filtres_modal').addClass('listing_filtres_modal_scroll');
            $('#selected_filters').fadeOut('slow');
            if (nompage_tunnel_js != 'panier' && nompage_tunnel_js != 'recap_commande' && nompage_tunnel_js != 'livraison_commande' && nompage_tunnel_js != 'confirme_commande' && nompage_tunnel_js != 'confirme_commande_cheque' && nompage_tunnel_js != 'succes_commande') {
                $('.logo_principal svg').fadeOut('fast');
                $('#logo_abeille').fadeIn();
            }
        } else if ($(window).scrollTop() < 180) {
            $('#main_search_form').removeClass('responsive_search_form');
            $('#navbar_secondary').removeClass('responsive_nav_bar');
            $('#listing_filtres_modal').removeClass('listing_filtres_modal_scroll');
            $('#selected_filters').fadeIn('slow');
            if (nompage_tunnel_js != 'panier' && nompage_tunnel_js != 'recap_commande' && nompage_tunnel_js != 'livraison_commande' && nompage_tunnel_js != 'confirme_commande' && nompage_tunnel_js != 'confirme_commande_cheque' && nompage_tunnel_js != 'succes_commande') {
                $('.logo_principal svg').fadeIn('slow');
                $('#logo_abeille').fadeOut();
            }
        }
    }
});
window.addEventListener("resize", function() {
    switch_to_mobile();
    switch_to_desktop();
}, false);
window.addEventListener("orientationchange", function() {
    var angle = window.orientation;
    if (angle == 90) {
        switch_to_desktop();
    } else if (angle == 0) {
        switch_to_mobile();
    }
}, false);
window.addEventListener('scroll', function(event) {
    if (event.target.id == 'search-ul-id-1') {
        if ($('#search-ul-id-1').scrollTop() + $('#search-ul-id-1').innerHeight() == $('#search-ul-id-1')[0].scrollHeight) {
            if ($('#page').val() <= $('#total_page').val()) {
                paginationScrollAutocomplete();
            }
        }
    }
}, true);
var valid_connexion = function() {
    var my_login = $('#email_address_responsive').val();
    var my_password = CryptoJS.MD5($('#password_responsive').val()).toString();
    var my_session = 0;
    var url = $('#returnUrl').val();
    var panier = $('#panier_finish_order').val();
    if (typeof(url) == 'undefined' || url == '') {
        url = document.location.href;
    }
    if ($('#persist_box').is(':checked')) {
        my_session = 1;
    }
    $('#message_alerte_connexion').hide().empty();
    $.ajax({
        type: "POST",
        url: 'connexion.php',
        dataType: 'json',
        async: false,
        data: {
            "action": "process",
            "email_address": my_login,
            "password": my_password,
            "session": my_session,
            "url": url,
            "panier": panier
        },
        success: function(data) {
            if (data.erreur) {
                $('#message_alerte_connexion').text(data.erreur_message).show();
            } else {
                if (data.redirection != "") {
                    document.location.href = data.redirection;
                }
            }
        }
    });
}
var disableEnterKey = function(e) {
    var key;
    if (window.event) key = window.event.keyCode; //IE
    else key = e.which; //firefox
    return (key != 13);
}
var modal_forgot_password = function(id) {
    var div_message = '#' + id + 'mdp_ctn_error_txt';
    var input_login = '#' + id + 'email_address';
    $(div_message).hide().empty().removeClass('resetmdp_confirmation');
    var my_login = $(input_login).val();
    $.getJSON("./forgot_password.php", {
        "action": "process",
        "email_address": my_login
    }, function(data) {
        if (!data.erreur) {
            $(div_message).addClass('resetmdp_confirmation');
        }
        $(div_message).text(data.erreur_message).show();
        $(input_login).val('');
    });
}
var autocompleteGwz = function(input) {
    var timer = null;
    input.addEventListener("input", function(event) {
        var el, val = this.value,
            id = this.id;
        if (!val || val.length < 3) {
            return false;
        }
        if (timer !== null) {
            clearTimeout(timer);
        }
        timer = setTimeout(function() {
            if (!document.getElementById(id + '-ul-id-1')) {
                el = document.createElement("ul");
                el.setAttribute('id', id + '-ul-id-1');
                el.setAttribute('class', 'ui-autocomplete ui-front ui-menu ui-widget ui-widget-content open');
                el.setAttribute('style', 'display: none; position: relative;');
                document.getElementById('results_search').appendChild(el);
            }
            var element_search = document.getElementById(id + '-ul-id-1');
            var element_contener = document.getElementsByClassName('container-fluid')[1];
            var element_footer = document.getElementById('footer');
            element_contener.style.display = 'none';
            element_footer.style.display = 'none';
            $.ajax({
                type: 'GET',
                cache: false,
                url: 'autocomplete_search.php',
                dataType: 'json',
                data: {
                    'term': val
                }
            }).done(function(data) {
                element_search.innerHTML = data.content;
                element_search.style.display = 'block';
                $('#results_search .json_facets_autocomplete').each(function() {
                    elementSelectedAutocomplete(this);
                });
            });
        }, 300);
    });
    // Send searched terms to Google Analytics (GA site search requires pageview hits)
    input.addEventListener("blur", function(event) {
        var searchedTerms = this.value.replace(/\s/g, "+");
        searchedTerms = accentsTidy(searchedTerms);
        ga('send', 'pageview', "autocomplete_search.php?keywords=" + searchedTerms);
    });
}
var display_connexion = function() {
    if ($(window).width() < 992) {
        var url = document.location.href;
        sessionStorage.setItem('url', url);
        window.location.href = 'responsive.php?action=connexion';
    } else {
        $('#layer_compte_off').slideToggle();
    }
}
var accentsTidy = function(string) {
    var returnString = string.toLowerCase();
    returnString = returnString.replace(new RegExp("\\s", 'g'), "");
    returnString = returnString.replace(new RegExp("[àáâãäå]", 'g'), "a");
    returnString = returnString.replace(new RegExp("æ", 'g'), "ae");
    returnString = returnString.replace(new RegExp("ç", 'g'), "c");
    returnString = returnString.replace(new RegExp("[èéêë]", 'g'), "e");
    returnString = returnString.replace(new RegExp("[ìíîï]", 'g'), "i");
    returnString = returnString.replace(new RegExp("ñ", 'g'), "n");
    returnString = returnString.replace(new RegExp("[òóôõö]", 'g'), "o");
    returnString = returnString.replace(new RegExp("œ", 'g'), "oe");
    returnString = returnString.replace(new RegExp("[ùúûü]", 'g'), "u");
    returnString = returnString.replace(new RegExp("[ýÿ]", 'g'), "y");
    //returnString = returnString.replace(new RegExp("\\W", 'g'), "");
    return returnString;
};