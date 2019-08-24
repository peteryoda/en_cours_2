$(document).ready(function() {
    $('#footer_close_facebook').click(function() {
        EA_button('fermer-footer-spreadbutton');
        $('#footer_facebook').slideUp('slow');
    });
    $('#footer_close_overlay').click(function() {
        EA_button('fermer-footer-spreadbutton');
        $('#footer_overlay').slideUp('slow');
    });
    $('#footer_close_overlay_2').click(function() {
        EA_button('fermer-footer-spreadbutton');
        $('#footer_overlay_2').slideUp('slow');
    });
    $('#footer_close_overlay_3').click(function() {
        EA_button('fermer-footer-spreadbutton');
        $('#footer_overlay_3').slideUp('slow');
    });
    $('#footer_close_overlay_4').click(function() {
        EA_button('fermer-footer-spreadbutton');
        $('#footer_overlay_4').slideUp('slow');
    });
    $('#footerEs1_close').click(function() {
        EA_button('fermer-footer-spreadbutton');
        $('#footerEs1').slideUp('slow');
    });
    $('#linkid_overlay3').click(function() {
        popupOptinisation('optionnel');
    });
});
var footerTags = function() {
    var footertags = document.getElementById("footer_facebook");
    if ($('#footer_facebook').css('display') == 'none') {
        $('#footer_facebook').delay(4000).slideDown('slow');
    }
}
var footerTags2 = function() {
    var footertags2 = document.getElementById("footer_overlay");
    if ($('#footer_overlay').css('display') == 'none') {
        $('#footer_overlay').delay(4000).slideDown('slow');
    }
}
var footerTags3 = function() {
    var footertags3 = document.getElementById("footer_overlay_2");
    if ($('#footer_overlay_2').css('display') == 'none') {
        $('#footer_overlay_2').delay(4000).slideDown('slow');
    }
}
var footerTags4 = function() {
    var footertags4 = document.getElementById("footer_overlay_3");
    if ($('#footer_overlay_3').css('display') == 'none') {
        $('#footer_overlay_3').delay(4000).slideDown('slow');
    }
}
var footerTags5 = function() {
    var footertags5 = document.getElementById("footer_overlay_4");
    if ($('#footer_overlay_4').css('display') == 'none') {
        $('#footer_overlay_4').delay(4000).slideDown('slow');
    }
}
var footerEs1 = function() {
    var footerEs1 = document.getElementById("footerEs1");
    if ($('#footerEs1').css('display') == 'none') {
        $('#footerEs1').delay(4000).slideDown('slow');
    }
}
var popupOptinisation = function(type) {
    display_box_createaccount(type);
}