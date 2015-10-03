var viewTime = new Date();
var url;
var endViewTime;
var elapsedTime;
//HOST URL
var hosturl = "127.0.0.1:5000";
var host;
var views;
var userid = "";



function informVisited(url, viewTime, endViewTime, host, elapsedTime, hosturl) {

	var xhr = new XMLHttpRequest();
	xhr.open('POST', hosturl + '/visited', true);
	xhr.onload = function() {
		console.log("HIIHI");
	};
	xhr.send("url ="+String(url)+"&userid="+String("HFDJKOWHFDOKJW")+"&viewTime="+String(viewTime)+"&endViewTime="+String(endViewTime)+"&timespent="+String(elapsedTime)+"&host="+String(host));
}

function getViews(userid, url, hosturl) {
	var received_views = 0;
	alert("K");

	var xhr = new XMLHttpRequest();
	xhr.open('GET', hosturl + '/visited', true);
	xhr.onload = function() {
		received_views = responseText;
		chrome.storage.local.get(key, function(obj){
			friendListFunction();
		});
	}
	xhr.send("url="+String(url)+"&userid="+String(userid));

	return received_views;
}


function getPageData() {
	alert("O");
	var d = new Date();
	var viewTime = d.getTime()
    //get the time of view
	//viewTime = Date.now();
	//When the tab has completed loading
    chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
    	if(changeInfo.status == 'complete' && tab.active) {
    		alert("HI");
    		//When the tab is active and the most recently focused window
    		chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function(tabs) {
		    	
		    	//get the URL
		    	url = tabs[0].url;
		    	//document.getElementById("box").innerHTML = url;

		    	views = getViews(userid, url,hosturl);
		    	alert("K");
		    	document.getElementById("num_views").innerHTML = String(views);

		    	host = window.location.hostname;
		    });
    		

    	}
    	
    });

    //When the tab is closed to find the closing time
	    chrome.tabs.onRemoved.addListener( function (tabId, removeInfo) {
	    	endViewTime = Date.now();
	    	elapsedTime = endViewTime - viewTime;
	    	alert("HIHIHHIIH");
	    	informVisited(url, viewTime, endViewTime, hosturl, elapsedTime, host);
	    });

}

window.addEventListener('Loaded', function() {
	alert("Loaded");
	getPageData();
});



window.addEventListener("hashchange", function() {
	informVisited(url, viewTime, endViewTime, host, elapsedTime, hosturl);
	alert("HIHIIIII");
;});