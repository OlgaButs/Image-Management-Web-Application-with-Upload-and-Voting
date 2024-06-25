$(document).ready(function() {
								imageslist("all");// Event handlers to redirect to other pages
								$("#gallery").click(function() {window.location.replace("gallery")});
								$("#upload").click(function() {window.location.replace("upload")});
								$("#about").click(function() {window.location.replace("sobre")});    
								$("#home").click(function(){window.location.replace("index")});
								$("#ua").click(function(){window.location.replace("ua")})
								$("#process").click(function() {window.location.replace("process")});
								$("#logout").click(function() {$.post("/api/logout"); window.location.replace("login")});
							});

function imageslist(id) {
	var author;
	if (id == "all") author = "all";
	else {
			author = $("#authorImg").val();
			if (author == "") author = "all";
	}
	$.get("/api/list",
		{ id : author },
		function(response){
			showimages(response);
		});
}

function showimages(response) {
	// response.images is the list of dictionaries with the images information
	$("#showimages").html("");
	for (var i = 0; i < response.images.length; i++) {
		var image = response.images[i];
		//console.log(image.path)
		var imageHtml = `
			<div class="teste">
				<div class="img_cont" >
					<img src="../${image.path}" alt="${image.name}" width="350px" height="250px" class="image_gall" onclick="showimagecomments('${image.id}')">
					<div class="mensagem" onclick="showimagecomments('${image.id}')">
						Click Here!
					</div>
				</div>
			</div>
		`;
		$("#showimages").append(imageHtml);
		
		
	}
}
// html code for showing the image and allow to click on it and invoke function showimagecomments
function showimagecomments(id)
{
	//window.open("../html/image.html?id=" + id, '_blank');
	//$.get("image",{imgid:id},function(response){window.location.(response);});
	window.location.href = "/image?imgid=" + id;
}