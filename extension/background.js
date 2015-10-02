var viewTime;
var url;
var endViewTime;
var elapsedTime;
//HOST URL
var hosturl = "";
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
/*
    	$.ajax({
    		type: "POST",
    		url: hosturl + "/visited",
    		async: true,
    		processData: true,
    		data: {
    			'url' : String(url),
    			'userid': String("HFDJKOWHFDOKJW"),
    			'viewTime': String(viewTime),
    			'endViewTime':String(endViewTime),
    			'timespent': String(elapsedTime),
    			'host': String(host)
    		},
    		success: function(data) {
    			console.log("HIHIH");
    		},
    		error: function(jqxhr, status, message) {
    			console.log("Yep...it failed :");
    		}
    	});*/
}

function getViews(userid, url, hosturl) {
	var received_views = 0;
	alert("K");

	var xhr = new XMLHttpRequest();
	xhr.open('GET', hosturl + '/visited', true);
	xhr.onload = function() {
		received_views = responseText;
	}
	xhr.send("url="+String(url)+"&userid="+String(userid));

/*	$.ajax({
		type: "GET",
		url: hosturl + "/visited",
		async: true,
		processData: true,
		data: {
			'url': String(url),
			'userid': String(userid),
		},
		success: function(data) {
			received_views = data['content'];
		},
		error: function(jqxhr, status, message) {
			alert("Failed");
		}
	}); */

	return received_views;
}

window.addEventListener('Loaded', function() {
	getPageData();
});

function getPageData() {

    //get the time of view
	viewTime = Date.now();
	//When the tab has completed loading
    chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
    	if(changeInfo.status == 'complete' && tab.active) {
    		
    		//When the tab is active and the most recently focused window
    		chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function(tabs) {
		    	
		    	//get the URL
		    	url = tabs[0].url;
		    	document.getElementById("box").innerHTML = url;

		    	views = getViews(userid, url,hosturl);
		    	alert("K");
		    	document.getElementById("num_views").innerHTML = views;

		    	host = window.location.hostname;
		    });
    		

    	}
    	
    });

    //When the tab is closed to find the closing time
	    chrome.tabs.onRemoved.addListener( function (tabId, removeInfo) {
	    	endViewTime = Date.now();
	    	elapsedTime = endViewTime - viewTime;

	    	informVisited(url, viewTime, endViewTime, hosturl, elapsedTime, host);
	    });

}


window.addEventListener("hashchange", function() {
	//informVisited(url, viewTime, endViewTime, host, elapsedTime, hosturl);
	alert("HIHIIIII");
;});