document.addEventListener('Loaded', function() {
	chrome.runtime.onMessage.addListener(function(req, sender, cb) {
		if(req.event == 'numViewsSent') {
			document.getElementById("num_views").innerHTML = req['num_views'];
		}
	});
});