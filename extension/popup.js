function work() {
	chrome.runtime.sendMessage({directive: "popup-click"}, function(response) {
	    console.log("Lulllllllz");
	});
	document.getElementById("box").addEventListener('click',function(){
		document.getElementById("box").innerHTML = "black";
		chrome.runtime.sendMessage({directive: "popup-click"}, function(response) {
	        //this.close(); // close the popup when the background finishes processing request
	    });
	});
}

window.addEventListener('DOMContentLoaded', function() {
    work();
});