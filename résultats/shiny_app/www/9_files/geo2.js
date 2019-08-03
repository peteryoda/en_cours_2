(function(){
	function e(e, t, n) {
	  var i = new Date;
	  i.setTime(i.getTime() + 24 * n * 60 * 60 * 1e3);
	  var o = "expires=" + i.toGMTString();
	  document.cookie = e + "=" + t + "; " + o + "; path=/;domain="+window.location.hostname.replace('www','')+";"
    }
    var xhr = new XMLHttpRequest();

xhr.open('GET', 'https://pro.ip-api.com/json/?key=jAoQ8GLYRzcAChw');
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
xhr.onload = function() {
    if (xhr.status === 200 ) {
        var  dd_cc=(JSON.parse(xhr.responseText, null, 2));
        var itemsArray = localStorage.getItem('us_dt') ? JSON.parse(localStorage.getItem('us_dt')) : {};
		var date_day = Math.round(+new Date()/1000+3600);
		itemsArray["ctr"]={"ctr" : dd_cc.country,"d":date_day};
		localStorage.setItem('us_dt', JSON.stringify(itemsArray));
	  	// e("us_dt", JSON.stringify(itemsArray), 365);
    }

};
xhr.send(encodeURI());
})();