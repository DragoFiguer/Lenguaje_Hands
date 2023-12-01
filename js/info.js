var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

// Define la posición inicial de las imágenes
var imageX = 100;
var imageY = 100;

// Carga las imágenes
var images = [];
var imageSources = ["senas/1.jpg", "senas/2.jpg", "senas/3.jpg", "senas/4.jpg",
                    "senas/5.jpg", "senas/6.jpg", "senas/7.jpg", "senas/8.jpg",
                    "senas/9.jpg", "senas/10.jpg", "senas/11.jpg", "senas/12.jpg",
                    "senas/13.jpg", "senas/14.jpg", "senas/15.jpg", "senas/16.jpg",
                    "senas/17.jpg", "senas/18.jpg", "senas/19.jpg", "senas/20.jpg",
                    "senas/21.jpg", "senas/22.jpg", "senas/23.jpg", "senas/24.jpg",
                    "senas/25.jpg", "senas/26.jpg"];

// Dibuja las imágenes en el lienzo
function drawImages() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  images.forEach(function(image) {
    ctx.drawImage(image, imageX, imageY);
  });
}

// Crea una función para cargar las imágenes
function loadImages(callback) {
  var loadedImages = 0;

  imageSources.forEach(function(src) {
    var image = new Image();
    image.onload = function() {
      loadedImages++;
      if (loadedImages === imageSources.length) {
        callback();
      }
    };
    image.src = src;
    images.push(image);
  });
}

// Actualiza la posición de las imágenes cuando se mueve el cursor
canvas.addEventListener("mousemove", function(event) {
  // Actualiza la posición de las imágenes según la posición del cursor
  imageX = event.clientX - canvas.offsetLeft;
  imageY = event.clientY - canvas.offsetTop;

  // Vuelve a dibujar las imágenes
  drawImages();
});

// Carga las imágenes y dibújalas inicialmente en el lienzo
loadImages(function() {
  drawImages();
});