var select = [];
var agg = [];

function toggleFilters(state) {
    if (state == 'visible') {
        $('#search_brand_cat_bloc').fadeOut();
        $('#search_filter').fadeIn();
        $('#search_filter').addClass('search_filter_translate');
    } else {
        $('#search_brand_cat_bloc').fadeIn();
        $('#search_filter').fadeOut();
        $('#search_filter').removeClass('search_filter_translate');
    }
}

function elementSelectedAutocomplete(element) {
    var key = $(element).attr('rel');
    select[key] = [];
    agg.push(key);
    $('.json_' + key + ':checked').each(function() {
        var value = $(element).val();
        select[key].push(value);
    });
}

function filterAutocomplete(element) {
    var key = $(element).attr('rel');
    var value = $(element).val();
    var sort = $('#sort_by_autocomplete').attr('data-sort');
    var sort_txt = $.trim($('#sort_by_autocomplete').text());
    var term = $('#search').val();
    if (element.is(':checked')) {
        select[key].push(value);
    } else {
        select[key].splice($.inArray(value, select[key]), 1);
    }
    sendFacetsAutocomplete(agg, select, sort, sort_txt, term, 'visible');
}

function sortAutocomplete(sort, sort_txt, term) {
    sendFacetsAutocomplete(agg, select, sort, sort_txt, term, 'visible');
}

function paginationScrollAutocomplete() {
    var sort = $('#sort_by_autocomplete').attr('data-sort');
    var sort_txt = null;
    var term = $('#search').val();
    var page = ($('#page').val() * 1) + 1;
    sendFacetPagination(agg, select, sort, sort_txt, term, page);
}

function sendFacetsAutocomplete(aggs, selects, sort, sort_txt, term, display) {
    $.ajax({
        dataType: 'json',
        method: 'GET',
        url: './autocomplete_search.php',
        data: {
            'term': term,
            'sort': sort,
            'aggs[]': aggs,
            'brands': selects['brands'],
            'labels': selects['labels'],
            'tags': selects['tags'],
            'status': selects['status'],
            'capacities': selects['capacities'],
            'origins': selects['origins']
        }
    }).done(function(data) {
        $('ul.ui-autocomplete').empty().html(data.content);
        if (sort_txt != null) {
            $('#sort_by_autocomplete .btn-dropdown-title').text(sort_txt);
            $('#sort_by_autocomplete').attr('data-sort', sort);
        }
        toggleFilters(display);
    });
}

function sendFacetPagination(aggs, selects, sort, sort_txt, term, page) {
    $.ajax({
        dataType: 'json',
        method: 'GET',
        url: './ajax/autocomplete/autocomplete_pagination.php',
        data: {
            'term': term,
            'page': page,
            'sort': sort,
            'aggs[]': aggs,
            'brands': selects['brands'],
            'labels': selects['labels'],
            'tags': selects['tags'],
            'status': selects['status'],
            'capacities': selects['capacities'],
            'origins': selects['origins']
        }
    }).done(function(data) {
        $('#ui-autocomplete-category-products').append(data.html);
        $('#page').val(data.page);
    });
}

function listenerViewAll(id) {
    $('#results_search').on('click', '#' + id + '_view_all', function() {
        $(this).fadeOut('fast', function() {
            $('#' + id + '_all').slideDown('fast', function() {
                $('#' + id + '_hide_all').fadeIn('fast');
            });
        });
    });
    $('#results_search').on('click', '#' + id + '_hide_all', function() {
        $(this).fadeOut('fast', function() {
            $('#' + id + '_all').slideUp('fast', function() {
                $('#' + id + '_view_all').fadeIn('fast');
            });
        });
    });
}

function animate_cart() {
    $('#mon_panier').addClass('bounce_animation').delay(1000).queue(function(next) {
        $(this).removeClass('bounce_animation');
        next();
    });
}

function displayLogin(){
    if ($(window).width() < 992) {
        var url = document.location.href;
        sessionStorage.setItem('url', url);

        window.location.href = 'responsive.php?action=connexion';
    } else {
        $('#layer_compte_off').slideToggle();
    }
}

// Au chargement de la page
$(document).ready(function() {
    $('input[errormessage]').each(function(i, input) {
        if (input.setCustomValidity !== undefined) {
            var check = function(event) {
                var els = this.type === 'radio' ? $('input[type=radio][name=' + this.name + ']') : $(this),
                    ok = false;
                els.each(function(i, el) {
                    if (el.checked) {
                        ok = true;
                    }
                });
                var message = ok ? '' : els.attr('errormessage');
                els.each(function(i, el) {
                    el.setCustomValidity(message);
                });
            };
            $(input).change(check);
            check.apply(input);
        }
    });
    $('div.liste_pl').click(function() {
        if ($(this).next().is(":hidden")) {
            $(this).next().css('display', 'block');
        } else {
            $(this).next().hide();
        }
    });
    $(".infos").mouseout(function() {
        matooltip = this.id;
        $("#tooltip" + matooltip).hide();
    });
    $(".infos").mouseover(function() {
        matooltip = this.id;
        $("#tooltip" + matooltip).show();
    });
    if ($(".select_fp").length > 0) {
        $(".select_fp").uniform({
            selectClass: 'selector s180'
        });
    }
    if ($(".select_fp2").length > 0) {
        $(".select_fp2").uniform({
            selectClass: 'selector s182'
        });
    }
    if ($(".select_ad").length > 0) {
        $(".select_ad").uniform({
            selectClass: 'selector s190'
        });
    }
    if ($(".select_ad_cp").length > 0) {
        $(".select_ad_cp").uniform({
            selectClass: 'selector s190b'
        });
    }
    if ($(".select_jour").length > 0) {
        $(".select_jour").uniform({
            selectClass: 'selector s200'
        });
    }
    if ($(".select_mois").length > 0) {
        $(".select_mois").uniform({
            selectClass: 'selector s205'
        });
    }
    if ($(".annee").length > 0) {
        $(".annee").uniform({
            selectClass: 'selector s210'
        });
    }
    //initialisation des fonctions
    init_onglets();
});
//Gestion des onglets
var init_onglets = function() {
    //On masque tout les onglets
    $("#conteneur #contenu #categories .desc_txt").hide();
    //On affiche le premier
    $("#conteneur #contenu #categories .desc_txt:eq(0)").show();
    $("#conteneur #contenu #categories .description .desc_det").addClass("on");
    //On va associer les clicks
    $("#conteneur #contenu #categories .description .desc_det").click(function() {
        $("#conteneur #contenu #categories .description .avis").removeClass("on");
        $("#conteneur #contenu #categories .description .desc_det").addClass("on");
        $("#conteneur #contenu #categories .desc_txt:eq(1)").hide();
        $("#conteneur #contenu #categories .desc_txt:eq(0)").show();
    });
    $("#conteneur #contenu #categories .description .avis").click(function() {
        $("#conteneur #contenu #categories .description .avis").addClass("on");
        $("#conteneur #contenu #categories .description .desc_det").removeClass("on");
        $("#conteneur #contenu #categories .desc_txt:eq(1)").show();
        $("#conteneur #contenu #categories .desc_txt:eq(0)").hide();
    });
}
/* ---------------------- FUNCTIONS CPE ---------------------- */
var delayMenuIn = null;
var delayMenuOut = null;
var nbstring = 0;
/* MENU */
if ($(window).width() > 992) {
    $('.header_menu').mouseover(function() {
        var selected = $(this).attr("rel").split("_");
        var id = selected[1];
        delayMenuIn = setTimeout(function() {
            $('#layer_' + id).css('display', 'flex');
        }, 50);
    }).mouseout(function() {
        var selected = $(this).attr("rel").split("_");
        var id = selected[1];
        if (delayMenuIn) {
            clearTimeout(delayMenuIn);
        }
        $('#layer_' + id).css('display', 'none');
    });
    /* MENU LAYER */
    $('.layer_menu2').mouseenter(function() {
        var selected = $(this).attr('id').split("_");
        var id = selected[1];
        //if (id != category_selected) {
        $('#lien_' + id).addClass('active_menu');
        //}
        $(this).css('display', 'flex');
    }).mouseleave(function() {
        var selected = $(this).attr('id').split("_");
        var id = selected[1];
        //if (id != category_selected) {
        $('#lien_' + id).removeClass('active_menu');
        //}
        $(this).css('display', 'none');
        $('.menu_reponsive').each(function() {
            $(this).height(28);
            $(this).attr('class', 'menu_reponsive');
        });
        $('.layer_menu2').appendTo($('#header'));
    });
}
$(function() {
    more_infos();

    // QUICK WINS
    $(".linkwins").mousedown(function(event) {
        var selected = $(this).attr("rel");
        if (selected !== undefined) {
            var url = document.location.href;
            var path = url.substring(0, url.lastIndexOf("/"));
            document.location.href = path + '/' + selected;
            return false;
        }
    });
    /*
     **********  Autocomplete : Moteur de recherche  ****************************************************************************************************************************************************
     */
    // tri dans autocomplete   
    $('#results_search').on('click', '#sort_by_autocomplete', function(e) {
        e.preventDefault();
        $('#sort_items_autocomplete').show();
    });

    $('#results_search').on('click', 'button.dropdown-item', function() {
        var sort = $(this).val();
        var sort_txt = $.trim($(this).html());
        var term = $('#search').val();
        sortAutocomplete(sort, sort_txt, term);
    });

    $('#results_search').on('click', '#launch_filter_sidebar', function() {
        toggleFilters('visible');
    });

    $('#results_search').on('click', '.autocomplete_checkbox', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var input = $(this).parent().find('.json_filters_autocomplete');
        if (input.is(':checked')) {
            input.removeAttr('checked');
        } else {
            input.attr('checked', 'checked');
        }
        filterAutocomplete(input);
    });

    listenerViewAll('autocomplete_labels');
    listenerViewAll('autocomplete_tags');
    listenerViewAll('autocomplete_brands');

    $('#results_search').on('click', '#autocomplete_close_filter', function() {
        toggleFilters('hidden');
    });

    $('#results_search').on('click', '#autocomplete_cancel_filters', function() {
        var term = $('#search').val();
        select = [];
        $('#results_search .json_facets_autocomplete').each(function() {
            $(this).prop('checked', false);
            elementSelectedAutocomplete(this);
        });
        sendFacetsAutocomplete(agg, select, 'default', 'Tri par défaut', term, 'hidden');
    });
    /*
     **********  Weezlist ****************************************************************************************************************************************************************************************
     */
    // Ajout du produit à la weezlist
    $('body').on('click', '.weezlist', function() {
        var div = $(this);
        var button = $(this).find('button');

        button.tooltip('hide');

        var products_id = button.attr("data-products-id");
        var variantes_id = 0;

        //if(div.hasClass('connected')) {
        var is_favorite = false;
        if(div.hasClass('favorite')) {
            is_favorite = true;
        }

        $.ajax({
            dataType : 'json',
            method   : 'POST',
            url      : './ajax/weezlist/weezlist.php',
            data     : {
                action       : 'add_to_list',
                products_id  : products_id,
                variantes_id : variantes_id,
                is_favorite  : is_favorite
            }
        }).done(function(data){
            if(!data.error) {
                if(is_favorite){
                    div.removeClass('favorite');
                    button.removeClass('bounce_animation');
                    button.attr('data-original-title', 'Ajouter à ma weezlist');
                } else {
                    div.addClass('favorite');
                    button.addClass('bounce_animation');
                    button.attr('data-original-title', 'Supprimer de ma weezlist');
                }
            } else {
                displayLogin();
            }
        });
        //} else {
        //    
        //}
    });
    
    /*
     ******************************************************************************************************************************************************************************
     */
    if (category_selected != 0) {
        $('#menu_' + category_selected).children('a').attr('style', 'background-color:#afcb09;');
    }
    $('.contImgDroite').click(function(event) {
        event.preventDefault();
        var type = $(this).data('type');
        var href = $(this).find('a:first').attr('href');
        href = decodeURIComponent(href);
        var aHref = decodeURIComponent(href).split('/');
        var path = aHref[aHref.length - 1];
        var pattern = /([a-zA-Z0-9-]+)-(p|m|c)([0-9]+)/;
        path = path.match(pattern);
        if (path != null) {
            ga('send', {
                hitType: 'event',
                eventCategory: 'TG - Clicks Merch',
                eventAction: 'Menu_Deroulant',
                eventLabel: $.trim(path[1])
            });
        } else {
            path = aHref[aHref.length - 1];
            pattern = /([a-zA-Z0-9-]+)\.php/;
            path = path.match(pattern);
            if (path != null) {
                ga('send', {
                    hitType: 'event',
                    eventCategory: 'TG - Clicks Merch',
                    eventAction: 'Menu_Deroulant',
                    eventLabel: $.trim(path[1])
                });
            }
        }
        document.location.href = href;
    });
    $('.link_menu_haut').click(function() {
        var url = $(this).attr("rel");
        ga('send', 'event', 'Clic_Navigation', 'Menu_Deroulant', '' + url + '');
    });
    $('.link_menu_left').click(function() {
        var url = $(this).attr("rel");
        ga('send', 'event', 'Clic_Navigation', 'Menu_Gauche', '' + url + '');
    });
    $('.link_slider_hp').click(function() {
        var img = $(this).attr("rel");
        ga('send', 'event', 'Clic_Navigation', 'Slider', '' + img + '');
    });
    $('.link_encart_hp').click(function() {
        var img = $(this).attr("rel");
        ga('send', 'event', 'Clic_Navigation', 'Bons_Plans', '' + img + '');
    });
    $('body').on('click', '.product_to_cart', function() {
        $('#mon_panier').addClass('bounce_animation').delay(1000).queue(function(next) {
            $(this).removeClass('bounce_animation');
            next();
        });
        var selected = $(this).attr("rel").split("_");
        var id = selected[1];
        var crosssell = selected[2];
        var page = selected[3].replace('-', '_');
        var price = Math.round(selected[4]); // price sans chiffre apres la virgule pour simplifier Google Analytics
        var quantity = 1;
        var variante_id = 0;
        var isVariante = $(this).data('isvariante');
        var refinterne = $(this).data('refinterne');
        var fpcrosssell = $(this).data('crosssell');
        var parent = $(this).parent().parent('.prod_list');
        var brand = $(this).attr("data-brand");
        var name = $(this).attr("data-name");
        var category = $(this).attr("data-category");
        var position = $(this).attr("data-position");
        var cat_id = $(this).attr("data-categories-id");
        var origin = $(this).attr("data-origin");
        var csPosition = $(this).attr("data-crosssell-position");
        var cartLocation = {
            'Listing_Page': 'liste',
            'Fiche_Produit': 'produit',
            'Autocomplete': 'recherche'
        }
        if ($('#quantity').length && fpcrosssell === undefined) {
            quantity = parseInt($("#quantity").val());
        }
        if ($("#variante").length && fpcrosssell === undefined) {
            var variante = $("#variante").val().split("|");
            variante_id = variante[0];
            if (variante_id == 'none') {
                alert(message);
                return false;
            }
        }
        // If click occured on a crosssell slider we send data to early birds
        if (origin == 'product_info_crosssell_early_birds_similar_products' || origin == 'product_info_crosssell_early_birds_complementary_products') {
            var eb_container = $(this).closest('div.eb-container');
            var widget_id = eb_container.attr('data-widget-id');
            var recommendation_id = eb_container.attr('data-recommendation-id');
            var products_id = $(this).closest('.carousel_object').attr('data-products-id');
            window._ebq.push(['trackActivity', {
                original_id: products_id,
                recommendationId: recommendation_id,
                verb: 'click-on-reco',
                type: 'product',
                widget: widget_id
            }]);
        }
        // Enhanced Ecommerce
        ga('ec:addProduct', {
            'id': id,
            'name': name,
            'category': category,
            'brand': brand,
            'price': price,
            'quantity': quantity,
            'position': position
        });
        ga('ec:setAction', 'add', {
            list: 'Listing Produit - cat c' + cat_id
        });
        ga('send', {
            hitType: 'event',
            eventCategory: 'Add to Cart',
            eventAction: cartLocation[page],
            eventLabel: id
        });
        // DataLayer (Google Tag Manager)
        dataLayer.push({
            'event': 'addToCart',
        });
        if (fPixel) {
            fbq('track', 'AddToCart', {
                content_ids: [id],
                content_type: 'product',
                value: price,
                currency: 'EUR'
            });
        }
        /* Ajout au panier sans popup */
        var url = $(this).attr('data-productsurl');
        if (isVariante == 1) {
            document.location.href = url;
        } else {
            add_product_to_cart(id, quantity, variante_id, parent, true, url, origin, csPosition);
            // On log également un autocomplete_click
            if (origin == 'autocomplete') {
                var search_term = $('#search').val();
                var first_manufacturer = ($('.first_manufacturer').attr('data-url') != undefined) ? $('.first_manufacturer').attr('data-url') : '';
                var first_categorie = ($('.first_categorie').attr('data-url') != undefined) ? $('.first_categorie').attr('data-url') : '';
                var first_product = ($('.first_product').attr('data-url') != undefined) ? $('.first_product').attr('data-url') : '';
                var second_product = ($('.second_product').attr('data-url') != undefined) ? $('.second_product').attr('data-url') : '';
                var device_type = $('#deviceType').val();
                var quicklist = ($('#has_quicklist').val() != undefined ? $('#has_quicklist').val() : 0);
                $.ajax({
                    type: 'POST',
                    url: 'ajax/autocomplete/log.php',
                    dataType: 'json',
                    data: {
                        action: 'click',
                        url: url,
                        search_term: search_term,
                        position: position,
                        first_manufacturer: first_manufacturer,
                        first_categorie: first_categorie,
                        first_product: first_product,
                        second_product: second_product,
                        origin: origin,
                        device_type: device_type,
                        quicklist: quicklist
                    }
                });
            }
        }
    });
    // Ajout au panier depuis crosssell
    $('#guide_crossell').on('click', '.product_to_cart_panier', function() {
        var products_id = $(this).attr('data-products-id');
        var products_variantes_id = 0;
        var quantity = 1;
        var products_url = $(this).attr("data-productsurl");
        var origin = $(this).attr("data-origin");
        var csPosition = $(this).attr("data-crosssell-position");
        // Annimation du panier
        animate_cart();
        // Ajout le produit au panier
        //add_product_to_cart(products_id, quantity, products_variantes_id, null, true, url, origin, csPosition);
        $.ajax({
            dataType: 'json',
            type: "GET",
            url: "./ajout_produit_panier.php",
            data: {
                products_id: products_id,
                variante: products_variantes_id,
                quantity: quantity
            },
            cache: false
        }).done(function(data) {
            ga('send', 'event', 'panier', 'slider_produit_oublie', '' + data.customers_id + '_' + products_id + '');
            // DataLayer (Google Tag Manager)
            dataLayer.push({
                'event': 'addToCart',
            });
            // layer détail panier
            $('#header_panier_articles').empty().text(data.nbr_articles);
            $('#header_show_total').empty().html(data.show_total);
            $('#layer_cart_header').html(data.layer);
            // Mise à jour des blocks
            // reload_crosssell(csPosition);
        });
    });

    // Ajout au panier en utilisant les boutons quantités + / -
    $('body').on('click', '.change_quantity_to_basket', function() {
        var id = $(this).parent().data('productsId');

        $('#mon_panier').addClass('bounce_animation').delay(1000).queue(function(next) {
            $(this).removeClass('bounce_animation');
            next();
        });

        $('#add_product_to_basket_' + id).addClass('flash_animation').delay(300).queue(function(next) {
            $('#add_product_to_basket_' + id).removeClass('flash_animation');
            next();
        });

        var products_id     = $(this).parent().attr('data-products-id');
        var variante_id     = 0;
        var isVariante      = $(this).parent().attr('data-isvariante');
        var way             = $(this).attr('data-mode');
        var divQuantity     = $(this).closest('div').find('.nb_products_cart');
        var quantityDisplay = divQuantity.text();
        var nbrProductMax   = $(this).parent().attr('data-products-stock');
        
        if ($("#variante").length) {
            var variante = $("#variante").val().split("|");
            variante_id = variante[0];
            nbrProductMax = variante[8];
        }

        if (way == 'up') {
            quantity = (quantityDisplay * 1) + 1;
        } else {
            quantity = (quantityDisplay * 1) - 1;
        }

        quantity = parseInt(quantity);

        if (quantity >= 0) {
            $.ajax({
                dataType : 'json',
                type     : 'POST',
                url      : '/ajax/panier/update_quantity.php',
                data     : {
                    products_id           : products_id,
                    products_variantes_id : variante_id,
                    quantity              : quantity
                }
            }).done(function(data) {
                if (!data.error) {
                    if (quantityDisplay == 1 && way == "down") {
                        divQuantity.text("0");

                        $('#add_product_to_basket').removeClass('added_to_cart');
                        $('#add_product_to_basket').addClass('product_to_cart');
                    } else {
                        if (nbrProductMax < quantity) {
                            quantity = nbrProductMax;
                        }

                        divQuantity.text(quantity);
                    }
                    // layer détail panier
                    $('#header_panier_articles').empty().html(data.values.nb_articles);
                    $('#header_show_total').empty().html(data.values.show_total);
                    $('#layer_cart_header').html(data.values.layer);
                }
            });
        }
        if (quantityDisplay == 1 && way == "down") {
            $('#add_product_to_basket_' + id).removeClass('added_to_cart');
            $('#add_product_to_basket_' + id).addClass('product_to_cart');
            return false;
        }
    });

    /* MOD_4739 : Suppression modal */
    $('#formulaire_newsletter_footer').click(function(e) {
        e.preventDefault();
        var email = $('#email_address_newsletter').val();
        var inscription = $(this).parents().find('.btn_c_email');
        var div = $(this).parents().find('.add_email');
        div.append('<div id="retour"></div>');
        if (email != "Votre adresse email") {
            $.getJSON("./newsletter.php", {
                "action": "process",
                "email_address": email,
                "abo_newsletter": "1"
            }, function(data) {
                if (!data.erreur) {
                    inscription.remove();
                    $("#retour").empty();
                    $("#retour").append('<small class="newsletter_inscription_response">Votre inscription a bien été prise en compte</small>');
                } else {
                    $("#retour").empty();
                    $("#retour").append('<small class="newsletter_inscription_response_error font-color-danger">' + data.erreur_message + '</small>');
                }
            });
        }
    });
    $('#submit_deconnexion_mon_compte_reponsive').click(function() {
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
    $('#formulaire_newsletter').click(function(e) {
        e.preventDefault();
        var email = $('#newsletter_reinscription').val();
        if (email != "Votre adresse email") {
            $.getJSON("./newsletter.php", {
                "action": "process",
                "email_address": email,
                "abo_newsletter": "1"
            }, function(data) {
                if (!data.erreur) {
                    $("#retour").empty();
                    $("#retour").append('<div class="alert alert-success">Votre inscription a bien été prise en compte</div>');
                    $("#icon").removeClass("is-invalid");
                    $("#newsletter_reinscription").removeClass("is-invalid");
                } else {
                    $("#retour").empty();
                    $("#retour").append('<div class="alert alert-danger">' + data.erreur_message + '</div>');
                    $("#icon").addClass("is-invalid");
                    $("#newsletter_reinscription").addClass("is-invalid");
                }
            });
        }
    });
    /*$('#email_address_newsletter').focus(function() {
        if ($('#email_address_newsletter').val() == _('Votre adresse e-mail')) {
            $('#email_address_newsletter').val('');
        }
    }).blur(function() {
        if ($('#email_address_newsletter').val() == '') {
            $('#email_address_newsletter').val(_('Votre adresse e-mail'));
        }
    });*/
    $('.ga_link_menu').click(function(event) {
        event.preventDefault();
        var string = $(this).text();
        var href = $(this).attr('href');
        var pathname = window.location.pathname;
        if (pathname == '/') {
            ga('send', {
                hitType: 'event',
                eventCategory: 'Homepage - Clicks Merch',
                eventAction: 'menu',
                eventLabel: $.trim(string)
            });
        }
        document.location.href = href;
    });
    $('.categorie_bloc').click(function(event) {
        event.preventDefault();
        var string = $(this).find('span:first').text().split('\n');
        var href = $(this).find('a:first').attr('href');
        ga('send', {
            hitType: 'event',
            eventCategory: 'Page Categorie - Clicks Merch',
            eventAction: 'sous-categorie',
            eventLabel: $.trim(string[1])
        });
        // Clicks on magazeen blocks should open new tabs
        if (href.indexOf("magazine") >= 0) {
            window.open(href, '_blank')
        } else {
            document.location.href = href;
        }
    });
    $('.manufacturer_bloc').click(function(event) {
        event.preventDefault();
        var href = $(this).find('a:first').attr('href');
        var aHref = decodeURIComponent(href).split('/');
        var path = aHref[aHref.length - 1];
        var pattern = /([a-zA-Z0-9-]+)-(p|m|c)([0-9]+)/;
        path = path.match(pattern);
        if (path != null) {
            ga('send', {
                hitType: 'event',
                eventCategory: 'Page Categorie - Clicks Merch',
                eventAction: 'promo',
                eventLabel: $.trim(path[1])
            });
        }
        document.location.href = href;
    });
    $('#cat_promo_include div#encart div.encart_1, #cat_promo_include div#encart div.encart_2, #cat_promo_include div#encart div.encart_3').click(function(event) {
        event.preventDefault();
        var href = $(this).find('a:first').attr('href');
        var aHref = decodeURIComponent(href).split('/');
        var path = aHref[aHref.length - 1];
        var pattern = /([a-zA-Z0-9-]+)-(p|m|c)([0-9]+)/;
        path = path.match(pattern);
        if (path != null) {
            ga('send', {
                hitType: 'event',
                eventCategory: 'Page Categorie - Clicks Merch',
                eventAction: 'promo',
                eventLabel: $.trim(path[1])
            });
        }
        document.location.href = href;
    });
    // Envois events GA clicks blocks merche HP (Attention hp_block_3 a un comportement spécifique. Voire ci-dessous)
    $('#hp_contenu section.hp_block_1, #hp_contenu figure.hp_block_2, #hp_contenu figure.hp_block_4, #hp_contenu figure.hp_block_5 ,#categories_niveau2 figure.hp_block_2').on('click', function(event) {
        event.preventDefault();
        var type = $(this).data('type');
        var originId = $(this).parent().parent().attr('id');
        // Does the user come from hp or category page ? 
        if (originId != 'small_visio_home' && type == 'hp_block_2') {
            origin = "Categories - Clicks Merch";
        } else {
            origin = "Homepage - Clicks Merch";
        }
        var href = $(this).find('a:first').attr('href');
        href = decodeURIComponent(href);
        var aHref = decodeURIComponent(href).split('/');
        var path = aHref[aHref.length - 1];
        var pattern = /([a-zA-Z0-9-]+)-(p|m|c|l|g)([0-9]+)/;
        label = path.split('?')[0];
        path = path.match(pattern);
        if (path != null) {
            path = aHref[aHref.length - 1];
            label = path.split('?')[0];
            ga('send', {
                hitType: 'event',
                eventCategory: origin,
                eventAction: type,
                eventLabel: label
            });
        } else {
            path = aHref[aHref.length - 1];
            pattern = /([a-zA-Z0-9-]+)\.php/;
            path = path.match(pattern);
            if (path != null) {
                ga('send', {
                    hitType: 'event',
                    eventCategory: origin,
                    eventAction: type,
                    eventLabel: $.trim(path[1])
                });
            }
        }
        document.location.href = href;
    });
    // Listener spécifique à hp_block_3 pour permettre un ajout au panier sans redirection
    $(' #hp_contenu div.hp_block_3 a, #categories_niveau2 div.hp_block_3 a').on('click', function(event) {
        event.preventDefault();
        var hp_block_3 = $(this).closest('div.hp_block_3');
        var originId = hp_block_3.parent().attr('id');
        // Does the user come from hp or category page ? 
        if (originId == 'categories_nouveautes') {
            origin = "Categories - Clicks Merch";
        } else {
            origin = "Homepage - Clicks Merch";
        }
        var type = hp_block_3.data('type');
        var href = hp_block_3.find('a:first').attr('href');
        href = decodeURIComponent(href);
        var aHref = decodeURIComponent(href).split('/');
        var path = aHref[aHref.length - 1];
        var pattern = /([a-zA-Z0-9-]+)-(p|m|c)([0-9]+)/;
        path = path.match(pattern);
        if (path != null) {
            ga('send', {
                hitType: 'event',
                eventCategory: origin,
                eventAction: type,
                eventLabel: $.trim(path[1])
            });
        } else {
            path = aHref[aHref.length - 1];
            pattern = /([a-zA-Z0-9-]+)\.php/;
            path = path.match(pattern);
            if (path != null) {
                ga('send', {
                    hitType: 'event',
                    eventCategory: origin,
                    eventAction: type,
                    eventLabel: $.trim(path[1])
                });
            }
        }
        // Si on clique sur l'ajout au panier alors on ne redirige pas vers la fiche produit
        if ($(this).attr('name') != 'Ajout_Panier') {
            document.location.href = href;
        }
    });
    $('.header_menu_responsive').click(function() {
        var selected = $(this).attr("rel").split("_");
        var id = selected[1];
        var num = $('#layer_' + id + ' .bloc_cat').length;
        $('.layer_menu_reponsive').hide();
        $('.menu_nav_reponsive_li .menu_reponsive').height(28);
        $('.menu_nav_reponsive_li #responsive_' + id).height(num * 34);
        $('.menu_nav_reponsive_li #responsive_' + id).attr('class', 'menu_reponsive fleche_responsive');
        $('#layer_responsive_' + id).appendTo($('#responsive_' + id));
        $('#layer_responsive_' + id).show();
    });
    $('.header_ss_menu_responsive').click(function() {
        var selected = $(this).attr("rel").split("_");
        var id = selected[2];
        var num = $('#layer_responsive_' + id + ' li').length;
        $('.layer_ss_cat').hide();
        $('#layer_responsive_' + id).height(num * 15);
        $('#layer_responsive_' + id + ' li').show();
        $('#layer_responsive_' + id).show();
    });
    /* LANGUE */
    $('#layer_langue').mouseenter(function() {
        $('#layer_langue').show();
    }).mouseleave(function() {
        $('#layer_langue').slideUp();
    });
    /* MON COMPTE // CONNECTER */
    $('.panier_responsive').click(function() {
        $('#layer_responsive_panier').slideToggle();
    });
    $('#menu_haut_responsive').click(function() {
        $.scrollTo($('#menu_responsive'), 800);
    });
    $('#navigation_menu_responsive').click(function() {
        $.scrollTo($('#navigation_responsive'), 800);
    });
    /* SOCIETE */
    $('.no_societe').click(function() {
        if ($('#ouvre_societe').css('display') == 'block') {
            $('#ouvre_societe').slideUp();
            $('#show_datenaissance').show();
            $('#show_pseudo').show();
        }
    });
    $('.open_societe').click(function() {
        $('#ouvre_societe').slideDown();
        $('#show_datenaissance').hide();
        $('#show_pseudo').hide();
    });
    $('.no_societe_2').click(function() {
        if ($('#ouvre_societe_2').css('display') == 'block') {
            $('#ouvre_societe_2').slideUp();
        }
    });
    $('.open_societe_2').click(function() {
        $('#ouvre_societe_2').slideDown();
    });
    /* ADRESSE DE FACTURATION */
    $('#adresse_facturation_open').click(function() {
        $('#div_adresse_facturation').slideDown();
    });
    $('#adresse_facturation_closed').click(function() {
        if ($('#div_adresse_facturation').css('display') == 'block') {
            $('#div_adresse_facturation').slideUp();
        }
    });
    $('.create_my_account').click(function() {
        var url = '';
        if (uri != '') {
            var parser = document.createElement('a');
            parser.href = uri;
            var pathname = parser.pathname.substring(1);
            if (pathname != '') {
                url = '?returnUrl=' + pathname;
            }
        }
        document.location.href = './create_account.php' + url;
    });
    /* INFOS BULLE */
    $('.infos_bulle').mousemove(function(event) {
        var infos = $(this).attr('rel');
        if ($('#curseur').css('display') == 'block') {
            //$('#curseur').hide();
        }
        $('#curseur').css('left', event.pageX + 10).css('top', event.pageY + 10);
        $('#curseur').html(infos);
        $('#curseur').show();
    }).mouseleave(function() {
        $('#curseur').fadeOut('fast');
        $('#curseur').empty();
        $('#curseur').css('left', 0).css('top', 0);
    });
    /* FAVORITES */
    $('.delete').click(function() {
        var selected = $(this).attr("rel").split("_");
        var id = selected[1];
        delete_favorites(id);
    });
    /* CODE PROMOTIONNEL */
    $('#code_promotionnel').click(function() {
        if ($('#code_promotionnel_info').css('display') == 'none') {
            $('#code_promotionnel_info').show(300);
            $('#total_info_table').addClass('sunken_div');
            $('#bouton_simulation_info').hide(300);
            $('.panier_simulation').removeClass('sunken_div');
        } else {
            $('#code_promotionnel_info').hide(300);
            $('#total_info_table').removeClass('sunken_div');
        }
    });
    /* SIMULATION FRAIS DE PORT */
    $('#bouton_simulation').click(function() {
        if ($('#bouton_simulation_info').css('display') == 'none') {
            $('#bouton_simulation_info').show(300);
            $('.panier_simulation').addClass('sunken_div');
            $('#code_promotionnel_info').hide(300);
            $('#total_info_table').removeClass('sunken_div');
        } else {
            $('#bouton_simulation_info').hide(300);
            $('.panier_simulation').removeClass('sunken_div');
        }
    });
    /* BLOC FIXED */
    $('#inscription_news_off_fr').hover(function() {
        $('#inscription_news_off_fr').hide();
        $('#inscription_news_on_fr').show();
    });
    $('#inscription_news_on_fr').mouseleave(function() {
        $('#inscription_news_on_fr').hide();
        $('#inscription_news_off_fr').show();
    });
    $('#formulaire_inscription_newsletter_fixed').click(function() {
        valid_inscription_newsletter();
        return false;
    });
    $('.idz_background').click(function() {
        document.location.href = $('#button_offline a')[0].href;
    });
    $('.version_bureau').click(function() {
        ga('send', 'event', 'Responsive', 'Changement_Version', 'Version_Complete');
        setCookie('GW_VERSION_BUREAU', 1);
        location.reload();
    });
    $('.version_mobile').click(function() {
        ga('send', 'event', 'Responsive', 'Changement_Version', 'Version_Responsive');
        setCookie('GW_VERSION_BUREAU', 0);
        location.reload();
    });
    // Code Promo GWZ
    $('#footer_overlay_close').click(function() {
        $('#code').hide('slow');
        $.ajax({
            url: './ajax/footer/footer_hide.php',
            method: 'POST',
            data: {
                bloc: 'footer_GWZ'
            }
        });
    });
});
var setCookie = function(name, value) {
    var nbrDay = 1;
    var expire = '';
    var path = '/';
    var date = new Date();
    if (value == 1) {
        /* Validité du cookie à 1 jour */
        date.setTime(date.getTime() + (nbrDay * (24 * ((60 * 60) * 1000))));
        expire = date.toGMTString();
    } else if (value == 0) {
        date.setTime(date.getTime() - 1);
        expire = date.toGMTString();
    }
    document.cookie = '' + name + '=' + escape(value) + '; expires=' + expire + '; path=' + path + '';
}
var display_box_youtube = function(id) {
    var href = 'https://www.youtube.com/watch?v=' + id;
    $.fancybox({
        'padding': 0,
        'autoScale': false,
        'transitionIn': 'none',
        'transitionOut': 'none',
        'width': 680,
        'height': 495,
        'href': href.replace(new RegExp("watch\\?v=", "i"), 'v/'),
        'type': 'swf',
        'swf': {
            'wmode': 'transparent',
            'allowfullscreen': 'true'
        }
    });
}
var add_product_to_cart = function(id, quantity, variante, idparent, log_autocomplete, url, origin, csPosition) {
    idparent = idparent || null;
    log_autocomplete = log_autocomplete || false;
    url = url || '';
    origin = origin || '';
    csPosition = csPosition || '';
    if (id != null) {
        $.ajax({
            type: "GET",
            url: "./ajout_produit_panier.php",
            data: "products_id=" + id + "&variante=" + variante + "&quantity=" + quantity,
            cache: false,
            dataType: 'json',
            success: function(data) {
                if (!data.error) {
                    // Animaton panier
                    $('#add_product_to_basket_' + id).addClass('bounce_animation').delay(1000).queue(function(next) {
                        $(this).removeClass('bounce_animation');
                        next();
                    });
                    // Gestion du bouton Ajouter (+ / -)
                    $('#basket_addons_' + id).fadeIn();
                    // Empêcher le comportement habituel quand on est sur la fiche produit
                    if (origin != 'product_info_crosssell_gwz_similar_products' && origin != 'product_info_crosssell_greenweez' && origin != 'categorie_special_guide_regular_slider' && origin != 'product_info_crosssell_early_birds_similar_products' && origin != 'product_info_crosssell_early_birds_complementary_products') {
                        $('#add_product_to_basket_' + id).removeClass('product_to_cart');
                        $('#add_product_to_basket_' + id).addClass('added_to_cart');
                        // fiche produit
                        $('#add_product_to_basket').removeClass('product_to_cart');
                        $('#add_product_to_basket').addClass('added_to_cart');
                        $('#add_product_to_basket').addClass('bounce_animation').delay(1000).queue(function(next) {
                            $(this).removeClass('bounce_animation');
                            next();
                        });
                    }
                    // layer détail panier
                    $('#header_panier_articles').empty().text(data.nbr_articles);
                    $('#header_show_total').empty().html(data.show_total);
                    $('#layer_cart_header').html(data.layer);
                    if (origin == '7' || origin == '3') {
                        //origin = slider_produit_oublie = 7
                        //origin = page_produit_oublie = 3
                        ga('send', 'event', 'panier', 'slider_produit_oublie', '' + data.customers_id + '_' + id + '');
                    } else if (origin == 'product_info_crosssell_greenweez') {
                        ga('send', 'event', 'fiche_produit', 'product_info_crosssell_greenweez', '' + data.customers_id + '_' + id + '');
                    } else if (origin == 'product_info_crosssell_gwz_similar_products') {
                        ga('send', 'event', 'fiche_produit', 'product_info_crosssell_gwz_similar_products', '' + data.customers_id + '_' + id + '');
                    }
                    /* Mise à jour de la quantité de produit déjà au panier quand on ajoute un produit pour la première fois depuis une div_box
                    de la home_page ou div_box des listing_produits */
                    if (origin == '1') {
                        var divQuantity = $('#add_product_to_basket_' + id).closest('div').find('.nb_products_cart');
                        var nbrProductMax = $('#add_product_to_basket_' + id).closest('div').find('.nb_products_cart').attr('data-products-stock');
                        var quantityDisplay = divQuantity.text();
                        quantity = (quantityDisplay * 1) + 1;
                        quantity = parseInt(quantity);
                        divQuantity.text(quantity);
                        // Il faut gérer la MAJ du panier dans la barre de navigation
                        if (quantity >= 0) {
                            $.ajax({
                                dataType: 'json',
                                type: 'POST',
                                url: '/ajax/panier/update_quantity.php',
                                data: {
                                    products_id: id,
                                    products_variantes_id: variante,
                                    quantity: quantity
                                }
                            }).done(function(data) {
                                if (!data.error) {
                                    if (quantityDisplay == 1) {
                                        divQuantity.text("0");
                                        $('#add_product_to_basket').removeClass('added_to_cart');
                                        $('#add_product_to_basket').addClass('product_to_cart');
                                        return false;
                                    } else {
                                        if (nbrProductMax < quantity) {
                                            quantity = nbrProductMax;
                                        }
                                        divQuantity.text(quantity);
                                    }
                                    // layer détail panier
                                    $('#header_panier_articles').empty().html(data.values.nb_articles);
                                    $('#header_show_total').empty().html(data.values.show_total);
                                    $('#layer_cart_header').html(data.values.layer);
                                }
                            });
                        }
                    }
                    // Mise à jour de la quantité de produit déjà au panier pour le bouton "Ajouter au panier de la fiche produit"
                    if (origin == '6') {
                        var divQuantity = $('#add_product_to_basket').closest('div').find('.nb_products_cart');
                        var nbrProductMax = $('#add_product_to_basket').closest('div').find('.nb_products_cart').attr('data-products-stock');
                        var quantityDisplay = divQuantity.text();
                        quantity = (quantityDisplay * 1) + 1;
                        quantity = parseInt(quantity);
                        divQuantity.text(quantity);
                        // Il faut gérer la MAJ du panier dans la barre de navigation
                        if (quantity >= 0) {
                            $.ajax({
                                dataType: 'json',
                                type: 'POST',
                                url: '/ajax/panier/update_quantity.php',
                                data: {
                                    products_id: id,
                                    products_variantes_id: variante,
                                    quantity: quantity
                                }
                            }).done(function(data) {
                                if (!data.error) {
                                    if (quantityDisplay == 1) {
                                        divQuantity.text("0");
                                        $('#add_product_to_basket').removeClass('added_to_cart');
                                        $('#add_product_to_basket').addClass('product_to_cart');
                                        return false;
                                    } else {
                                        if (nbrProductMax < quantity) {
                                            quantity = nbrProductMax;
                                        }
                                        divQuantity.text(quantity);
                                    }
                                    // layer détail panier
                                    $('#header_panier_articles').empty().html(data.values.nb_articles);
                                    $('#header_show_total').empty().html(data.values.show_total);
                                    $('#layer_cart_header').html(data.values.layer);
                                }
                            });
                        }
                    }
                } else {
                    if (idparent != null) {
                        $(idparent).addClass('inactive');
                        $(idparent).children().children().children().children('.lazyloaded').attr('style', 'opacity:0.4');
                        $(idparent).children().children().children('.stock').addClass('inactive').html('Stock épuisé !');
                    }
                }
            }
        });
    }
}
var more_infos = function() {
    $(".btn_ql").hide();
    $(".prod_list").mouseenter(function() {
        $(".btn_ql", this).show();
    }).mouseleave(function() {
        $(".btn_ql", this).hide();
    });
    /*--------- layer de l'espace noel ---------*/
    $(".noel_image_frame .produits_layer").hide();
    $(".noel_image_frame").mouseenter(function() {
        $(".produits_layer", this).show();
    }).mouseleave(function() {
        $(".produits_layer", this).hide();
    });
    $(".noel_image_frame .produits_layer_2").hide();
    $(".noel_image_frame").mouseenter(function() {
        $(".produits_layer_2", this).show();
    }).mouseleave(function() {
        $(".produits_layer_2", this).hide();
    });
}
var delete_favorites = function(id) {
    if (id != null) {
        $.getJSON("./delete_favorites.php", {
            "action": "process",
            "id": id
        }, function(data) {
            if (data.erreur == false) {
                $('#favorites_' + id).fadeOut('slow', function() {
                    $('#favorites_' + id).empty();
                })
                $('#favorites_number_articles').fadeOut('fast', function() {
                    $('#favorites_number_articles').empty().text(data.nbr_favorites).fadeIn();
                });
            }
        });
    }
}
/* ---------------------- FIN FUNCTIONS CPE ---------------------- */
/* ---------------------- FUNCTION SPEC SAFARI ---------------------- */
var checkFormSafariSpec = function(message) {
    var is_chrome = navigator.userAgent.indexOf('Chrome') > -1;
    var is_explorer = navigator.userAgent.indexOf('MSIE') > -1;
    var is_firefox = navigator.userAgent.indexOf('Firefox') > -1;
    var is_safari = navigator.userAgent.indexOf("Safari") > -1;
    var is_opera = navigator.userAgent.toLowerCase().indexOf("op") > -1;
    if ((is_chrome) && (is_safari)) {
        is_safari = false;
    }
    if ((is_chrome) && (is_opera)) {
        is_chrome = false;
    }
    if (is_safari) {
        var forms = document.getElementsByTagName('form');
        for (var i = 0; i < forms.length; i++) {
            forms[i].noValidate = true;
            forms[i].addEventListener('submit', function(event) {
                //Prevent submission if checkValidity on the form returns false.
                if (!event.target.checkValidity()) {
                    event.preventDefault();
                    //Implement you own means of displaying error messages to the user here.
                    alert(message);
                }
            }, false);
        }
    }
}
/* ---------------------- FIN FUNCTION SPEC SAFARI ---------------------- */
var checkPasswordRules = function(pwd) {
    var rules = 0
    /*Validation des règles*/
    // rule [minLength8]
    if (pwd.length < 8) {
        $('[data-requirement="minLength8"]').removeClass('valide').addClass('invalid');
    } else {
        rules += 1;
        $('[data-requirement="minLength8"]').removeClass('invalid').addClass('valide');
    }
    // rule [number]
    if (pwd.match(/([0-9])/)) {
        rules += 1;
        $('[data-requirement="number"]').removeClass('invalid').addClass('valide');
    } else {
        $('[data-requirement="number"]').removeClass('valide').addClass('invalid');
    }
    // rule [lowercase]
    if (pwd.match(/([a-z])/)) {
        rules += 1;
        $('[data-requirement="lowercase"]').removeClass('invalid').addClass('valide');
    } else {
        $('[data-requirement="lowercase"]').removeClass('valide').addClass('invalid');
    }
    // rule [uppercase]
    if (pwd.match(/([A-Z])/)) {
        rules += 1;
        $('[data-requirement="uppercase"]').removeClass('invalid').addClass('valide');
    } else {
        $('[data-requirement="uppercase"]').removeClass('valide').addClass('invalid');
    }
    // rule []
    /*if(pwd.match(/[\W_]/)) {
        rules += 1;
        $('[data-requirement="specialChar"]').removeClass('invalid').addClass('valide');
    }
    else {
        $('[data-requirement="specialChar"]').removeClass('valide').addClass('invalid');
    }*/
    return rules;
}
var checkPasswordFormat = function(password, nom, prenom, email) {
    var valid = false;
    var msg = 'Votre mot de passe ne doit pas contenir ';
    var forbidden = '';
    var display = false;
    // Validation [nom]
    if (nom != "") {
        var regNom = new RegExp(nom, 'i');
        if (password.search(regNom) != -1) {
            forbidden += 'votre nom;';
            display = true;
        }
    }
    // Validation [prenom]
    if (prenom != '') {
        var regPrenom = new RegExp(prenom, 'i');
        if (password.search(regPrenom) != -1) {
            forbidden += 'votre prénom;';
            display = true;
        }
    }
    // Validation [email]
    if (email != '') {
        mail = email.split('@');
        mail = mail[0];
        var regMail = new RegExp(mail, 'i');
        if (password.search(regMail) != -1) {
            forbidden += 'votre email;';
            display = true;
        }
    }
    temp = forbidden.split(";");
    $.each(temp, function(key, value) {
        msg += value;
        if (key != temp.length - 1) {
            msg += ", ";
        }
    });
    msg = msg.substring(0, msg.length - 2);
    $('#pass-val-msg').empty();
    if (display) {
        $('#pass-val-msg').append(msg);
    } else {
        valid = true;
    }
    return valid;
}
var changeType = function(elem, type) {
    if (elem.prop('type') == type) {
        return elem; // ça serait facile.
    }
    try {
        // Une sécurité d'IE empêche ceci
        return elem.prop('type', type);
    } catch (e) {
        // On tente de recréer l'élément
        // En créant d'abord une div
        var html = $("<div>").append(elem.clone()).html();
        var regex = /type=(\")?([^\"\s]+)(\")?/;
        // la regex trouve type=text ou type="text"
        // si on ne trouve rien, on ajoute le type à la fin, sinon on le remplace
        var tmp = $(html.match(regex) == null ? html.replace(">", ' type="' + type + '">') : html.replace(regex, 'type="' + type + '"'));
        // on rajoute les vieilles données de l'élément
        tmp.data('type', elem.data('type'));
        var events = elem.data('events');
        var cb = function(events) {
            return function() {
                //Bind all prior events
                for (i in events) {
                    var y = events[i];
                    for (j in y) tmp.bind(i, y[j].handler);
                }
            }
        }(events);
        elem.replaceWith(tmp);
        setTimeout(cb, 10); // On attend un peu avant d'appeler la fonction
        return tmp;
    }
}
//Fonctions d'ajout / suppression de produits dans les listes de courses
var add_products_to_list = function(item, action, formData, urlAjax) {
    $.ajax({
        url: urlAjax,
        type: 'POST',
        dataType: 'json',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            var label = item.parent().find('label');
            var list_nbr = item.next().find('.list_nbr');
            var list_info = item.next().find('.list_info');
            if (action == 'add') {
                label.removeClass("ajout_liste_supprime").addClass("ajout_liste_ajoute");
                list_info.css('display', 'block');
                list_info.empty();
                list_info.append(data.message).delay(3000).fadeOut(function() {
                    label.removeClass("ajout_liste_ajoute");
                });
            } else {
                label.removeClass("ajout_liste_ajoute").addClass("ajout_liste_supprime");
                list_info.css('display', 'block');
                list_info.empty();
                list_info.append(data.message).delay(3000).fadeOut(function() {
                    label.removeClass("ajout_liste_supprime");
                });
            }
            list_nbr.html('(' + data.nbr_products + ') ');
        }
    });
}
var add_products_to_new_list = function(list_name, formData2, urlAjax) {
    var formData = new FormData();
    formData.append('action', 'create_new_list');
    formData.append('list_name', list_name);
    $.ajax({
        url: './customer_favorites.php',
        type: 'POST',
        dataType: 'json',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            if (data.error) {
                $('#creation_liste_hidden .msg_error').html('La liste existe déjà').css("display", "block");
            } else {
                formData2.append('action', 'add_products_to_list');
                formData2.append('list_id', data.list_id);
                $.ajax({
                    url: urlAjax,
                    type: 'POST',
                    dataType: 'json',
                    data: formData2,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function(data) {
                        var index = ($('#nb_liste').val() * 1) + 1;
                        var html = '<div class="ajout_liste_selection">' + '   <input type="checkbox" id="ajout_liste_selection_' + index + '" class="ajout_liste_checkbox" data-list-id="' + data.list_id + '" checked="checked"/>' + '   <label for="ajout_liste_selection_' + index + '" class="ajout_liste_ajoute">' + '       <span></span>' + '       <div>' + '           <p class="list_title">' + list_name + '</p>' + '           <p class="list_nbr">(' + data.nbr_products + ')</p>' + '           <p class="list_info"> ' + data.message + '</p>' + '       </div>' + '   </label>' + '   <div class="ajout_liste_voir_liste">' + '       <a href="my-account/wishlist">> Voir</a>' + '   </div>' + '</div>';
                        $('#nb_liste').val(index);
                        $('.ajout_liste_contenu').append(html);
                        $('#creation_liste_hidden').toggle();
                    }
                });
            }
        }
    });
}
//-- Fin fonction pour les listes de courses