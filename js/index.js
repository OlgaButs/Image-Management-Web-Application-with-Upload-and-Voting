const btnAside = document.querySelector('.aside-ua button');
const asideContent = document.querySelector('.aside-ua__content');
const modalUa = document.querySelector('.modal-ua');

$(document).ready(function () {
  $("#gallery").click(function () { window.location.replace("gallery"); });
  $("#upload").click(function () { window.location.replace("upload"); });
  $("#about").click(function () { window.location.replace("sobre"); });
  $("#ua").click(function () { window.location.replace("ua"); });
  $("#process").click(function () { window.location.replace("process"); });
  $("#changePassword").click(function () { window.location.replace("changePassword"); });
  $("#logout").click(function () { $.post("/api/logout"); window.location.replace("login"); });
  loadTopImages();
});

function loadTopImages() {
  $.getJSON("/api/topimage", function (response) {
    const topImages = response.top_images;
    $("#image1").attr("src", "../" + topImages.image1);
    $("#image2").attr("src", "../" + topImages.image2);
    $("#image3").attr("src", "../" + topImages.image3);
  });
}
const myCarouselElement = document.querySelector('#carouselExampleAutoplaying')
const carousel = new bootstrap.Carousel(myCarouselElement, {
  interval: 2000,
  touch: false
})