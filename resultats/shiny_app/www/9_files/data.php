 (function () { 
                        var loadFrame = function (u) {
                        var i = document.createElement('iframe');
                        i.src = u; i.style.display='none'; document.body.appendChild(i); 
                        }
                        var loadImg = function (u) {
                        var i = document.createElement('img');
                        i.src = u; i.style.display='none'; document.body.appendChild(i); 
                        }
                        var loadScript = function (u) {
                        var i = document.createElement('script');
                        i.src = u; document.body.appendChild(i); 
                        }
                        var loadScriptSource = function (u) {
                        var i = document.createElement('script');
                        i.innerHTML = u; document.body.appendChild(i); 
                        }
                        loadImg('https://r.turn.com/r/beacon?b2=sFrbKg0fONvc5yA5SPLz6_sN8O-0MQ-lsnvN2YLqGKRI8vY3V8jGkDJMGPO4WGjwGHlqK3RO-H1CM_wOMqb-4g&cid=');                        })();
                        