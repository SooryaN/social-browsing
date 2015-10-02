/*
	Background2.js maintains the following state:
		Login state (logged in? access token?)
		Friends List
		Profile data of each friend and self
		Messages
		'timeSpent' for each open page
 */

FB.loadAPI('https://thakkarparth007.github.io/');

window.fbAsyncInit = function() {
	FB.init({
		appId      : '964263926953204',
		xfbml      : true,
		version    : 'v2.4',
		oauth      : true
	});
	syncWithFB();
};

function setPopupPage(changes) {
	if('loggedIn' in changes) {
		var popup_page = "auth.html";
		if(changes.loggedIn.newValue == true)
			popup_page = "popup.html";

		chrome.browserAction.setPopup({
			popup: popup_page
		});
	}
}

// untested!
function getPics(frList) {
	var newFrs = [];
	for(var i in frList) {
		var fr = frList[i];
		if('pic' in fr) continue;

		newFrs.push(frList);
	}

	var jobs_left = newFrs.length;
	for(var i in newFrs) {
		var fr = newFrs[i];
		(function(i, fr) {
			FB.api('/' + fr.id + '/picture', function(pic) {
				jobs_left--;
				fr.pic = pic.data.url;

				if(!jobs_left) {
					chrome.storage.local.set({
						'friendsList': frList
					});
				}
			});
		})(i, fr);
	}
}

function syncWithFB() {
	FB.getLoginStatus(function(response) {
		chrome.storage.local.set({
			loggedIn: "connected" == response.status
		});
		
		chrome.storage.local.get('loggedIn', function(obj) {
			if('loggedIn' in obj) {
				FB.api('/me/friends', function(resp) {
					var data = resp.data;
					chrome.storage.local.set({'friendsList':data});
					getPics(data);
				});
			}
		});
	}, true);
	
}

chrome.storage.onChanged.addListener(setPopupPage);
chrome.alarms.create('fb-status-sync', { periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener(function(alarm) {
	if(alarm.name == 'fb-status-sync')
		syncWithFB();
});

function TimeTracker() {

}





