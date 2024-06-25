var id;

$(document).ready(
    function(){
        //let params = new URLSearchParams(window.location.search);
        //id = params.get("id");
		id = $("#image_id").val()
        imagecomments ();
		$("#gallery").click(function() {window.location.replace("gallery")});
		$("#upload").click(function() {window.location.replace("upload")});
		$("#about").click(function() {window.location.replace("sobre")});
		$("#ua").click(function() {window.location.replace("ua")});
		$("#process").click(function() {window.location.replace("process")});
		$("#logout").click(function() {$.post("/api/logout"); window.location.replace("login")});
		$("#close").click(function() {window.location.replace("gallery")});
});

function imagecomments()
{
	$.get("/api/comments",
		{ idimg : id },
		function(response){
			showimageandinfo(response);
		});
}

function showimageandinfo(response) {
		// response.image is the image information
		let image = response.image;
		let imageInfo = `

			<div>
				<!-- Button trigger modal -->
				<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal" style="background: grey; border-radius: 20px; margin: 5%; border: none;">
				Click here to see image information...
				</button>

				<!-- Modal -->
				<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
				<div class="modal-dialog">
					<div class="modal-content">
					<div class="modal-header">
						<h1 class="modal-title fs-5" id="exampleModalLabel">Image Information</h1>
						<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
					</div>
					<div class="modal-body">
						<div class="tabelas-cont">
							<table>
							<tr>
								<td><b>ID:</b></td>
								<td>${image.id}</td>
							</tr>
							<tr>
								<td><b>Name:</b></td>
								<td>${image.name}</td>
							</tr>
							<tr>
								<td><b>Author:</b></td>
								<td>${image.author}</td>
							</tr>
							<tr>
								<td><b>Date and Time:</b></td>
								<td>${image.datetime}</td>
							</tr>
							</table>
						</div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
					</div>
					</div>
				</div>
				</div>
			</div>

		
		`;
		let imageHtml = `
			<div>
				<img src= "../${image.path}" alt="${image.name}" width="550px" height="450px" style="box-shadow: #1ca2ff 0px 0px 5px 5px; background-color: white;">
				${imageInfo}
			</div>
		`;
		$("#imageinfo").html(imageHtml);
	
		// response.comments is the image list comments
		let comments = response.comments;
		let commentsHtml = "";
		for (let i = 0; i < comments.length; i++) {
			let comment = comments[i];
			let commentHtml = `
				<p>User: ${comment.user}</p>
				<p>Comment: ${comment.comment}</p>
				<p>Date: ${comment.datetime}</p>
			`;
			commentsHtml += `<div style="box-shadow: #1ca2ff 0px 0px 5px 5px; background-color: white; margin: 20px;">${commentHtml}</div>`;
		}
		$("#comments").html(commentsHtml);
	
		// response.votes is the image votes
		$("#thumbs_up").text(response.votes.thumbs_up);
		$("#thumbs_down").text(response.votes.thumbs_down);

		// Verifica o estado do butão like/dislike:
		var likeStatus = $.get("/api/getUserLike",{ idimg : id },
						function(response)
						{
							//console.log(typeof response);
							if (response === "true") {$("#like").css("filter","saturate(1)");$("#dislike").css("filter","saturate(0.2)");}
							else if (response === "false") {$("#dislike").css("filter","saturate(1)");$("#like").css("filter","saturate(0.2)");}
						});
	}
	// response.votes is the image votes

function newcomment() {
	// obtain the comment from image page
	var comment = $("#comment").val();
	
	if ( comment == "") alert("Missing comment!");
	else {
		$.post("/api/newcomment",
			{ idimg: id, newcomment: comment },
			function() { imagecomments(); });
	}
}

function upvote()
{
	$.post("/api/upvote", { idimg: id}, function() { imagecomments(); });
}

function downvote()
{
	$.post("/api/downvote",{ idimg: id },function() { imagecomments(); });
}

function removeImage()
{
	$.get("/api/removeImage",{idimg : id},function(response){alert(response);window.location.replace("gallery");})
}