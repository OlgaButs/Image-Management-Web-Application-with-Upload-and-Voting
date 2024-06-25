var originalImage;

function loadImage() {
    console.log("loadImage() called");
    originalImage = $("#original-image").val();
    if ($.isNumeric(originalImage)) {
        $.get("/api/comments", { idimg: originalImage }, function(response) {
            showImage(response);
        });
    } else {
        alert("It must be an integer, try again");
    }
}

function showImage(response) {
    let image = response.image;
    if (image.path !== undefined) {
        let imageHtml = `
            <div>
                <img src="../${image.path}" alt="${image.name}" width="550px" height="450px">
            </div>
        `;
        $("#originalimage").html(imageHtml);
    } else {
        alert("No image exists with that id");
    }
}

function processedImage(selected) {
    console.log("processedImage() called");
    if (originalImage === "") {
        alert("Missing image id");
    } else {
        $.getJSON("/api/imageproc", { id: originalImage, select: selected }, function(response) {
            console.log("Image received");
            var imageProcessed = response.processedImagePath;
            if (imageProcessed !== undefined) {
                // Adiciona um carimbo de data/hora ao final do URL da imagem processada
                var timestamp = new Date().getTime();
                imageProcessed += "?timestamp=" + timestamp;

                let imageHtml = `
                    <div>
                        <img src="${imageProcessed}" alt="processed" width="550px" height="450px">
                    </div>
                `;
                $("#processedImage").html(imageHtml);
            }
            console.log(imageProcessed);
        })
        .fail(function() {
            alert("Error in processing image");
        });
    }
}
function deleteProcessedImages() {
    $.get("/api/deleteProcessedImages", function(response) {});
}

$(document).ready(function() {
    // Event handlers to redirect to other pages
    $("#gallery").click(function() {deleteProcessedImages();window.location.replace("gallery");});
    $("#upload").click(function() {deleteProcessedImages();window.location.replace("upload");});
    $("#about").click(function() {deleteProcessedImages();window.location.replace("sobre");});
    $("#home").click(function() { deleteProcessedImages();window.location.replace("index");});
    $("#ua").click(function() { deleteProcessedImages();window.location.replace("ua");});
    $("#process").click(function() { deleteProcessedImages();window.location.replace("process");});
    $("#logout").click(function() {$.post("/api/logout"); window.location.replace("login")});

    $("select.mySelect").change(function() {
        console.log("Select value changed");
        var selected = $(this).children("option:selected").val();
        if (originalImage !== "") {
            if (selected != "0") {
                processedImage(selected);
                alert("It will take a little time, please wait.");
            }
        } else {
            alert("Missing image!");
        }
    });
});
