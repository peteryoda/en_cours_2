var _BaseClassName="nolink";
var startTime = new Date().getTime();  
var elapsedTime = 0;

jsli = {
	getElementsByClassName:function (className) {
		if (!document.getElementsByClassName) {
			var retour=new Array();
			var dc=document.getElementsByTagName("span");
			for(i=0;i<dc.length;i++)
			{
				var cln=dc[i].className.split(" ")
				for(j=0;j<cln.length;j++)
				{
					if (cln[j]==className)
						retour[retour.length]=dc[i];
				}
			}
			return retour;
		} else {
			return document.getElementsByClassName(className);
		}
	},

	LocalIterations:0,
	SpansTransform:0,
	IterationsVides:0,
	IsRunning:false,
	
	Transformation:function ()
	{	
		jsli.IsRunning=true;
		try  {
			var spanstotos=this.getElementsByClassName(_BaseClassName);
			var nbspanstotos=spanstotos.length;
			var _base16="0A12B34C56D78E9F";	
			var _tproperties="charset,name,rel,rev,target,accesskey,id,style,tabindex,title".split(',');
			var _tmethods="blur,click,dblclick,focus,mousedown,mousemove,mouseover,mouseup,keydown,keyppress,keyup".split(',');
			var str, rurl=""
			var curSpan, rclassn, ln =null;
			var ch, cl, j, p,d=0;	
			var i=nbspanstotos;while(i--)
			{	
				curSpan=spanstotos[i];
				p=curSpan.className.indexOf(' ');
				d=curSpan.className.indexOf(' ',p+1);
				if (d == -1)
					d=curSpan.className.length;
				rurl="";
				if (p>0)
				{	
					str=curSpan.className.substr(p+1,d-p-1);
					for(j=0;j<str.length;j+=2)			
					{
						ch=_base16.indexOf(str.charAt(j));
						cl=_base16.indexOf(str.charAt(j+1));
						rurl+=String.fromCharCode((ch*16)+cl);
					}
				}
				rclassn=curSpan.className.substr(d+1,curSpan.className.length-d-1);
				ln=document.createElement("a");
				ln.href=rurl;	
			
				j=_tproperties.length;while(j--)
				{
					try {
						p=_tproperties[j];
						if (d=curSpan.getAttribute(p))
							ln[p]=d;
					} catch (e) {}
				}
			
				j=_tmethods.length;while(j--)
				{
					try {
						p=_tmethods[j];
						if (d=curSpan["on"+p]) {
							if (ln.addEventListener){
								ln.addEventListener(p, d, false);
							} else if (ln.attachEvent) {
								ln.attachEvent('on'+p, d);
							}
						}
					} catch (e) {}
				}
			
				ln.className=rclassn;
				j=curSpan.childNodes.length;while(j--)
					ln.appendChild(curSpan.childNodes[0]);			
				curSpan.parentNode.insertBefore(ln, curSpan);
				curSpan.parentNode.removeChild(curSpan);
			}
		} catch (e)  {}
		jsli.LocalIterations++;
		jsli.SpansTransform+=nbspanstotos;
		if ((jsli.SpansTransform > 0) && ((nbspanstotos == 0) && (document.body))) {	
			jsli.IterationsVides++;
		}
		if (jsli.IterationsVides < 5 ) {
			setTimeout("jsli.Transformation()", 200);
		} else jsli.IsRunning=false;

		elapsedTime = new Date().getTime() - startTime;
		//console.log((elapsedTime/1000)+' secondes ');
	}
}

jsli.Transformation();

