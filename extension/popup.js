var wait = 2;

function work() {
	//chrome.runtime.sendMessage({directive: "popup-click"}, function(response) {
	//	console.log("Lulllllllz");
	//});
	document.getElementById("box").addEventListener('click',function(){
		document.getElementById("box").innerHTML = "black";
	//	chrome.runtime.sendMessage({directive: "popup-click"}, function(response) {
	//		//this.close(); // close the popup when the background finishes processing request
	//	});

		FB.getLoginStatus(function(response) {
			if (response.status === 'connected') {
				alert('Logged in.');
			}
			else {
				alert("not logged in");
				FB.login(function(){
				  // Note: The call will only work if you accept the permission request
				  FB.api('/me/feed', 'post', {message: 'Hello, world!'});
				}, {scope: 'public_profile,email,user_friends'});
			}
		});
	});
}

window.addEventListener('DOMContentLoaded', function() {
	wait--;
	if(!wait) work();
});

FB.loadAPI('https://thakkarparth007.github.io/');

window.fbAsyncInit = function() {
	FB.init({
		appId      : '964263926953204',
		xfbml      : true,
		version    : 'v2.4',
		oauth      : true
	});

	wait--;
	if(!wait) work();
};

