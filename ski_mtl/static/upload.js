$(document).ready(function() {

	drop = document.getElementById('dropzone');

	drop.onclick = function() {
		console.log("test");
		document.getElementById("input").click();
	};
	
	drop.ondragover = function () {
		this.className = 'hover';
		var progress = document.getElementById("progress");
		progress.style.display = "none";
		return false;
	};
	drop.ondragend = function () { this.className = ''; return false; };
	drop.ondragleave = function () { this.className = ''; return false; };

	drop.ondrop = function (e) {
		e.preventDefault();

		this.className = '';
		var progress = document.getElementById("progress");
		progress.innerHTML = "";
		progress.style.width = "0%";
		progress.style.display = "block";

		document.getElementById("drop_text").style.display = "none";

		file = e.dataTransfer.files[0];

		var fd = new FormData();
		fd.append("file", file);

		xhr = new XMLHttpRequest();
		xhr.open("POST", "/upload");

		xhr.upload.addEventListener("progress", function(e) {
				if (e.lengthComputable) {
					var percent = Math.round((e.loaded * 100) / e.total);
					progress.style.width = percent + "%";
					progress.innerHTML = percent + "%";
					console.log(percent);
				}
		}, false);

		xhr.upload.addEventListener("loadend", function(e) {
			progress.style.width = "100%";
			progress.innerHTML = "Done";
		});

		xhr.send(fd);
	}
});
