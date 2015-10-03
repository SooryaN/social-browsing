/*
	Background2.js maintains the following state:
		Login state (logged in? access token?)
		Friends List
		Profile data of each friend and self
		Messages
		'timeSpent' for each open page
 */

var url;
//HOST URL
var hosturl = "127.0.0.1:5000";
var host;
var views;
var userid = "";


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
// NOTE: The first part of the method is noobish.
// One should check the chrome.store for the pic
// attribute. Too complicated for now. :P
function getPics(frList) {
	var newFrs = [];
	var jobs_left1 = 0;
	for(var i in frList) {
		var fr = frList[i];
		if('pic' in fr) continue;

		newFrs.push(fr);
	}

	var jobs_left2 = newFrs.length;
	for(var i in newFrs) {
		var fr = newFrs[i];
		(function(i, fr) {
			FB.api('/' + fr.id + '/picture', function(pic) {
				jobs_left2--;
				fr.pic = pic.data.url;

				if(!jobs_left2) {
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

				FB.api('/me/', function(resp) {
					chrome.storage.local.set({'me': resp.data});
					FB.api('/me/picture', function(pic_resp) {
						chrome.storage.local.set({
							'me': {
								id: resp.data.id,
								name: resp.data.name,
								pic: pic_resp.data.url
							}
						});
					});
				});


				FB.api('/me/friends', function(resp) {
					var data = resp.data;
					chrome.storage.local.set({'friendsList':data});

					chrome.storage.local.get(
						['me','friendsList'], 
						function(obj) {
							var friends = [];
							for(var i in obj.friendsList)
								friends.push(obj.friendsList[i].id);
							
							$.ajax({
								url: hosturl + '/user',
								method: 'POST',
								data: {
									name: obj.me.name, 
									fbuserid: obj.me.id, 
									friends: friends, 
									token: response.authResponse.accessToken
								}
							});
						}
					);
					
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

function getViews(url) {
	$.ajax({
		url: hosturl + "/visited/history",
		method: "POST",
		data: {
			url: url
		},
		success: function(data, status) {
			alert("Yolo");
			console.log()
		},
		error: function() {
			alert("Error occurred");
			console.log("Error");
		}
	});
}

function sendTimeSpent(url, timeSpent) {
	$.ajax({
		url: hosturl + "/visited/",
		method: "POST",
		data: {
			'url': url,
			'timespent': timeSpent
		},
		success: function(data, status) {
			alert("Yolo");
			console.log()
		},
		error: function() {
			alert("Error occurred");
			console.log("Error");
		}
	});
}

chrome.runtime.onMessage.addListener(function(req, sender, cb) {
	if(req.event == 'timeTrackStart') {
		getViews(req.url);
	}
	if(req.event == 'timeTrackEnd') {
		sendTimeSpent(req.url, req.timeSpent);
	}
});