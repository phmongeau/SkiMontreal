$(document).ready(function() {

	drop = document.getElementById('dropzone');
	files = [];
	file_names = [];

	//drop.onclick = function() {
		//console.log("test");
		//document.getElementById("input").click();
	//};
	
	drop.ondragover = function () {
		this.className = 'hover';
		document.getElementById("input").style.display = "none";
		var progress = document.getElementById("progress");
		progress.style.display = "none";
		document.getElementById("drop_text").style.display = "block";
		return false;
	};
	drop.ondragend = function () {
		document.getElementById("input").style.display = "";
		document.getElementById("drop_text").style.display = "none";
		this.className = ''; return false; 
	};
	drop.ondragleave = function () {
		document.getElementById("input").style.display = "";
		document.getElementById("drop_text").style.display = "none";
		this.className = ''; return false;
	};

	drop.ondrop = function (e) {
		e.preventDefault();

		document.getElementById("input").style.display = "";
		document.getElementById("drop_text").style.display = "none";

		addFiles(e.dataTransfer.files);

		this.className = ''; return false;
	}

	addFiles = function(input_files) {

		for (var i = 0; i < input_files.length; ++i)
		{
			var f = input_files.item(i);
			if (f.name.split(".").reverse()[0] === "gpx" && file_names.indexOf(f.name) == -1)
				files.push(f);
				file_names.push(f.name);
		}
		$("#file_list ul").html('');
		for (var i in files)
		{
			var file = files[i];
			
			$("#file_list ul").append("<li>" + file.name + "</li>");
		}

	}

	handleFiles = function(f)
	{
		addFiles(f);
	}

	sendFiles = function()
	{
		var form = document.getElementById("uploadForm");


		for (var i in files)
		{
			var fd = new FormData();
			fd.append("file", files[i]);

			var xhr = new XMLHttpRequest();
			xhr.open("POST", "/upload");
			xhr.send(fd);
		}
	}

	$("#send_form").click(function() {
		sendFiles();
	});
});
