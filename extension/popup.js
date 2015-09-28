function work() {
	document.getElemenyById("box").addEventListener('click',function(){
		document.getElemenyById("box").innerHTML = "black";
	});
}

window.addEventListener('DOMContentLoaded', function() {
    work();
});