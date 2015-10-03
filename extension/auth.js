var wait = 2;

function work() {
	document.getElementById("box").addEventListener('click',function(e) {
		document.getElementById("box").innerHTML = "black";
		
		FB.login(function(response){
			if(response.status == 'connected') {
				var accessToken = response.authResponse.accessToken;
				var userid = response.authResponse.userID;
				chrome.storage.local.set({
					loggedIn: true,
					accessToken: accessToken,
					userid: userid
				});
			}
			//
			// else ???
		}, {scope: 'public_profile,email,user_friends'});

		return false;
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
