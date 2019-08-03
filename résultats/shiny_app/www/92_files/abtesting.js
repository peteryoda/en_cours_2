// AB testing Early Birds (used in shopping cart and product info)
$(function() {
    if (window.eb.profile.id != null) {
        var isEB = parseInt(window.eb.profile.id.replace('-', ''), 16) % 2 ? true : false;
        Cookies.remove('eb-ab');
        Cookies.set('eb-ab', isEB, {
            expires: 365
        });
        if (isEB) {
            ga('set', 'dimension15', 'earlyBirdsSliders');
            ga('send', 'event', 'sliders', 'abtest', 'earlyBirdsSliders', {
                'nonInteraction': 1
            });
        } else {
            ga('set', 'dimension15', 'greenweezSliders');
            ga('send', 'event', 'sliders', 'abtest', 'greenweezSliders', {
                'nonInteraction': 1
            });
        }
    }
});