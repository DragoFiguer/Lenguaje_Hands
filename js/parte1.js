
var aciertos = 0;
var ind=1,i=0,band=0; 
var banco_imagen = new Array();
var banco_fondo = new Array();
var banco_aleatorio = new Array();
var banco_sonidos= new Array();
//var banco_nombre= new  Array("CERDO"," COCODRILO","DELFIN","CONEJO","ARDILLA","ELEFANTE","LEON","JIRAFA","OSO","PERRO","RANA","OVEJA");
var banco_nombre = new Array("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z");
function genera(){
  //for (let index = 0; index <=12; index++) {
 for (let index = 0; index <=26; index++){
  //banco_imagen[index]= "imagenes/animales/"+ind+".png"; //array donde estan cargados los animales
  banco_imagen[index] = "/senas/senal/"+ind+".jpg";
 //banco_fondo[index]= "imagenes/"+ind+".jpg"; //array donde estan cargados los habitad
 banco_fondo[index] = "senas/ss/"+ind+".jpg";
 banco_sonidos[index]= "sonido/sound_letters/"+ind+".mp3"; //array donde estan cargados los sonidos
 banco_nombre[index];
 ind++;  //Incrementamos la variable
}

i=0; ind=0;
while(band!=1){
   //var aleatorio = Math.floor(Math.random()*12); //Se genera el aleatorio aleatorio entre el 1 y el 12
   var aleatorio = Math.floor(Math.random()*26);
   if( (banco_aleatorio.indexOf(aleatorio)) == (-1) ){ //Comprobamos si el aleatorio aleatorio esta en el array
     banco_aleatorio[i]=aleatorio; ind++; i++;              //En caso de que no este retorna -1 y se agrega al array 
   }
  
   if(ind==3){         //Variable para aciertos=lar cuantos elementos aleatorios se ingresan al array
     band=1; //En caso de llevar 3 elementos se rompe el ciclo
  
}

} 
}
function dibuja(){
genera();
 document.getElementById("ia1").src = banco_imagen[banco_aleatorio[0]];
 document.getElementById("audio1").src = banco_sonidos[banco_aleatorio[0]];
 document.getElementById("ia2").src = banco_imagen[banco_aleatorio[1]];
 document.getElementById("audio2").src = banco_sonidos[banco_aleatorio[1]];
 document.getElementById("ia3").src = banco_imagen[banco_aleatorio[2]];
 document.getElementById("audio3").src = banco_sonidos[banco_aleatorio[2]];

 document.getElementById("habitat1").style.background = "url('"+banco_fondo[banco_aleatorio[0]]+"')";
 document.getElementById("habitat2").style.background = "url('"+banco_fondo[banco_aleatorio[1]]+"')";
 document.getElementById("habitat3").style.background = "url('"+banco_fondo[banco_aleatorio[2]]+"')";

 
 
}
 function allowDrop(ev){
  ev.preventDefault();
  }
  
  function drag(ev) {
  ev.dataTransfer.setData("Text",ev.target.id);
  }
  function drop(ev) {
    ev.preventDefault();
    var audio = document.getElementById("audio");
    var audio1= document.getElementById("audio1");
    var audio2= document.getElementById("audio2");
    var audio3=document.getElementById("audio3");
    var nombre1=banco_nombre[banco_aleatorio[0]];
    var nombre2=banco_nombre[banco_aleatorio[1]];
    var nombre3=banco_nombre[banco_aleatorio[2]];

    if (ev.target.id == "habitat1" && ev.dataTransfer.getData("Text") =="ia1" ){
      var data=ev.dataTransfer.getData("Text");
      ev.target.appendChild(document.getElementById(data));
      document.getElementById("nombre1").innerHTML=nombre1;
      audio1.play();
      aciertos++;

    } 
   if (ev.target.id == "habitat2" && ev.dataTransfer.getData("Text") =="ia2"){
    var data=ev.dataTransfer.getData("Text");
    ev.target.appendChild(document.getElementById(data));
    document.getElementById("nombre2").innerHTML=nombre2;
    audio2.play();   
    aciertos++;
   }
   if( ev.target.id == "habitat3" && ev.dataTransfer.getData("Text") =="ia3"){
    var data=ev.dataTransfer.getData("Text");
    ev.target.appendChild(document.getElementById(data));
   audio3.play();
   document.getElementById("nombre3").innerHTML=nombre3;
    aciertos++;
   }
   
   else if (ev.target.id == "habitat1" && ev.dataTransfer.getData("Text")=="ia1"||  ev.target.id == "habitat2" && ev.dataTransfer.getData("Text") =="ia2"|| ev.target.id == "habitat3" && ev.dataTransfer.getData("Text") =="ia3") {
   
       
    
   } else{
    audio.play();
   }
   console.log(aciertos);// 
    if (aciertos==6){
      setTimeout("redireccionarPagina()",1000);
}
  }
  
  function redireccionarPagina() {
    window.location = 'parte2.html';
  }
  
  



