// Image UpLoad Javascript
var file;
								// Event handlers to redirect to other pages
$(document).ready(function() {
								$("#home").click(function() {window.location.replace("index")});
								$("#gallery").click(function() {window.location.replace("gallery")});
								$("#upload").click(function() {window.location.replace("upload")});
								$("#about").click(function() {window.location.replace("sobre")});
								$("#ua").click(function() {window.location.replace("ua")});
								$("#process").click(function() {window.location.replace("process")});
								$("#logout").click(function() {$.post("/api/logout"); window.location.replace("login")});
							});

function updatePhoto(event) {
	var reader = new FileReader();
	reader.onload = function(event) {
		//Create an imagem
		var img = new Image();
		img.onload = function() {
			//Put imagen on screen
			const canvas = $("#photo")[0];
			const ctx = canvas.getContext("2d");
			ctx.drawImage(img,0,0,img.width,img.height,0,0,550, 450);
		}
		img.src = event.target.result;
	}

	file = event.target.files[0];
	//Obtain the file
	reader.readAsDataURL(file);
}

function uploadImage() {
    if(file != null) {
        sendFile(file);
		window.URL.revokeObjectURL(picURL);
    }
    else alert("Missing image!");
}

function sendFile(file)
{
	var data = new FormData();
	//data.setRequestHeader("Content-type", "multipart/form-data");
	data.append("myFile", file);

	//Obtain nameImg and authorImg and fill the form
	var name = $("#nameImg").val();
	data.append("nameImg", name);
	var author = $("#authorImg").val();
	data.append("authorImg", author);

	if (name == "" || author == "") alert("Missing name and/or author!");
	else
	{
		var xhr = new XMLHttpRequest();
		xhr.open("POST", "/api/upload");
		xhr.upload.addEventListener("progress", updateProgress(this), false);
		xhr.send(data);
	}
}

function updateProgress(evt){
	if(evt.loaded == evt.total) alert("Okay");
}