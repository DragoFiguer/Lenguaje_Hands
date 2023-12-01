function guardarDatos() {
   localStorage.nombre = document.getElementById("nombre").value;
   n = localStorage.nombre;

}

function portada() {// Funcion con uso de canvas
   var img = new Image();// Creamos un objeto de tipo imagen 
   var c = document.getElementById('canvas');// Se declaran  la variable canvas 
   ctx = c.getContext('2d');
   img.src = 'js/win.jpg';
   img.addEventListener('load', function () {
      ctx.drawImage(img, 20, 20, 1005, 660);
      var gradient = ctx.createLinearGradient(0, 0, c.width, 0);
      gradient.addColorStop("0.5", "teal");

      ctx.fillStyle = gradient;  // Uso de texto en canvas 
      ctx.font = '80px Arial Rounded MT Bold';
      ctx.fillText("FELICIDADES", 300, 150);
      var nombre = localStorage.getItem("Nombre");
      ctx.fillText(nombre, 430, 250);
      ctx.fillText("GANASTE", 370, 350);
   }, false);
}


/*font-family: 'Monoton', cursive;*/