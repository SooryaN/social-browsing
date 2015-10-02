var wait = 2;

function work() {
	chrome.runtime.sendMessage({directive: "popup-click"}, function(response) {
		console.log("Lulllllllz");
	});
	document.getElementById("box").addEventListener('click',function(){
		document.getElementById("box").innerHTML = "black";
		chrome.runtime.sendMessage({directive: "popup-click"}, function(response) {
			//this.close(); // close the popup when the background finishes processing request
		});

		FB.getLoginStatus(function(response) {
			if (response.status === 'connected') {
				console.log('Logged in.');
			}
			else {
				FB.login(function(){
			  // Note: The call will only work if you accept the permission request
			  FB.api('/me/feed', 'post', {message: 'Hello, world!'});
			}, {scope: 'publish_actions'});
			}
		});
	});
}

window.addEventListener('DOMContentLoaded', function() {
	wait--;
	if(!wait) work();
});

window.fbAsyncInit = function() {
	FB.init({
		appId      : '964263926953204',
		xfbml      : false,
		version    : 'v2.4'
	});

	wait--;
	if(!wait) work();
};

(function(d, s, id){
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) {return;}
	js = d.createElement(s); js.id = id;
	js.src = "https://connect.facebook.net/en_US/sdk.js";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));