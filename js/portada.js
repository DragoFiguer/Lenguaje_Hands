
function portada() {// Funcion con uso de canvas
   var img= new Image();// Creamos un objeto de tipo imagen 
   var c = document.getElementById('canvas');// Se declaran  la variable canvas 
   ctx = c.getContext('2d');
    img.src = 'js/ff.jpg'; //Mandamos llamar nuestra imagen 
    img.addEventListener('load', function() { 
   ctx.drawImage(img,20,20,1005,660);//Declaramos  el tamaño de la imagen 
   var gradient = ctx.createLinearGradient(0, 0, c.width, 0);
    gradient.addColorStop("0.3", "black");
    gradient.addColorStop("0.5", "purple");

    ctx.fillStyle = gradient;  // Uso de texto en canvas 
    ctx.font='90px Amasis MT Pro Black';// Uso de font 
    ctx.fillText("APRENDAMOS ", 230, 300);//Texto que queremos imprimir 
    //ctx.fillText("CON ", 400, 400);
    ctx.fillText("JUGANDO ", 310, 480);
         }, false);
}



/*font-family: 'Monoton', cursive;*/