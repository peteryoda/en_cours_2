var OS11012104 = cibleclic_pt['OS11012104'];
OS11012104.functions.cp = function(n) {
    var t = JSON.parse(JSON.stringify(n)),
        o = 0;
    for (var r in n) t[r] = o + "-" + (parseInt(o) + parseInt(n[r].split("/")[0])), o = parseInt(o) + parseInt(n[r].split("/")[0]);
    var e = parseInt(n[r].split("/")[1]);
    OS11012104.pop = t, OS11012104.den = e
}, OS11012104.functions.a_R = function(n) {
    var t = Math.random() * OS11012104.den | 0;
    for (var o in n) {
        if (t >= n[o].split("-")[0] && t < n[o].split("-")[1]) return o;
        if (t >= n[o].split(";")[0] && t < n[o].split(";")[1]) return o
    }
}, OS11012104.functions.getCookie = function(n,a) {
    var sp =  !JSON.parse(localStorage.getItem('n')) ? '' :JSON.parse(localStorage.getItem('n'))[a] ? JSON.parse(localStorage.getItem('n'))[a][a] : '';
    return sp
}, OS11012104.functions.updateCookie = function(n, a, t, o) {
    if (o) {
        var r = new Date;
        r.setTime(r.getTime() + 24 * o * 60 * 60 * 1e3);
        var e = "; expires=" + r.toGMTString()
    } else e = "";
    var i = localStorage.getItem("us_dt") ? JSON.parse(localStorage.getItem("us_dt")) : {},
        s = Math.round(+new Date / 1e3 + 3600);
    i[a] = {
        [a]: t,
        d: s
    }, localStorage.setItem("us_dt", JSON.stringify(i))
    // , document.cookie = n + "=" + JSON.stringify(i) + e + "; path=/;domain=" + window.location.hostname.replace('www', '')
}, OS11012104.functions.testSplit = function(n) {
    var t = JSON.parse(JSON.stringify(OS11012104.pop));
    for (var o in t) t[o] = 0;
    for (var r = 0; r < n; r++)
        for (var o in test = OS11012104.functions.a_R(OS11012104.pop), OS11012104.pop) test == o && (t[o] = t[o] + 1);
    for (var o in OS11012104.pop) console.log("% in group " + o + " = " + t[o] / n * 100)
}, OS11012104.functions.t_s = function(n) {
    var t = JSON.parse(JSON.stringify(OS11012104.pop));
    for (var o in t) t[o] = 0;
    for (var r = 0; n > r; r++)
        for (var o in test = OS11012104.functions.a_R(OS11012104.pop), OS11012104.pop) test == o && (t[o] = t[o] + 1);
    for (var o in OS11012104.pop) console.log("% in grps " + o + " = " + t[o] / n * 100)
}, OS11012104.functions.cp(OS11012104.sr), OS11012104.grps = OS11012104.functions.getCookie(OS11012104.cn,OS11012104.cn2), "" == OS11012104.grps && (OS11012104.grps = OS11012104.functions.a_R(OS11012104.pop)), OS11012104.functions.updateCookie(OS11012104.cn, OS11012104.cn2, OS11012104.grps, 365);

