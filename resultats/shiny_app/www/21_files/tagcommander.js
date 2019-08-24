function loadScript(file, position) {
  var eventName = 'tagCoReady'
  if (typeof(Event) === 'function') {
    var domEvent = new Event(eventName);
  } else {
    var domEvent = document.createEvent('Event');
    domEvent.initEvent(eventName, false, false);
  }

  var script  = document.createElement('script');
  script.addEventListener("load", function(event) {
    if (position === 'head') {
      document.dispatchEvent(domEvent)
    }
  });
  script.src  = file;
  script.type = 'text/javascript';
  if (position !== 'head') {
    script.defer = true;
  }
  document.getElementsByTagName(position).item(0).appendChild(script);
}

loadScript('https://cdn.tagcommander.com/3969/tc_CarrefourONE_20.js?rn=201907190028', 'head');
