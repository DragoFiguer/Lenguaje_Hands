const array = [
    {
        'case': ' ',
        'imagen': 'senas/senal/0.png'
    },
    {
        'case': 'A',
        'imagen': 'senas/senal/1.jpg'
    },
    {
        'case': 'B',
        'imagen': 'senas/senal/2.jpg'
    },
    {
        'case': 'C',
        'imagen': 'senas/senal/3.jpg'
    },
    {
        'case': 'D',
        'imagen': 'senas/senal/4.jpg'
    },
    {
        'case': 'E',
        'imagen': 'senas/senal/5.jpg'
    },
    {
        'case': 'F',
        'imagen': 'senas/senal/6.jpg'
    },
    {
        'case': 'G',
        'imagen': 'senas/senal/7.jpg'
    },
    {
        'case': 'H',
        'imagen': 'senas/senal/8.jpg'
    },
    {
        'case': 'I',
        'imagen': 'senas/senal/9.jpg'
    },
    {
        'case': 'J',
        'imagen': 'senas/senal/10.jpg'
    },
    {
        'case': 'K',
        'imagen': 'senas/senal/11.jpg'
    },
    {
        'case': 'L',
        'imagen': 'senas/senal/12.jpg'
    },
    {
        'case': 'M',
        'imagen': 'senas/senal/13.jpg'
    },
    {
        'case': 'N',
        'imagen': 'senas/senal/14.jpg'
    },
    {
        'case': 'O',
        'imagen': 'senas/senal/15.jpg'
    },
    {
        'case': 'P',
        'imagen': 'senas/senal/16.jpg'
    },
    {
        'case': 'Q',
        'imagen': 'senas/senal/17.jpg'
    },
    {
        'case': 'R',
        'imagen': 'senas/senal/18.jpg'
    },
    {
        'case': 'S',
        'imagen': 'senas/senal/19.jpg'
    },
    {
        'case': 'T',
        'imagen': 'senas/senal/20.jpg'
    },
    {
        'case': 'U',
        'imagen': 'senas/senal/21.jpg'
    },
    {
        'case': 'V',
        'imagen': 'senas/senal/22.jpg'
    },
    {
        'case': 'W',
        'imagen': 'senas/senal/23.jpg'
    },
    {
        'case': 'X',
        'imagen': 'senas/senal/24.jpg'
    },
    {
        'case': 'Y',
        'imagen': 'senas/senal/25.jpg'
    },
    {
        'case': 'Z',
        'imagen': 'senas/senal/26.jpg'
    }
];

//Variables y contantes globales

const seccionTraducir = document.getElementById('sec-traducir');
const seccionAcerca = document.getElementById('sec-acerca-de');
const btnTraducir = document.getElementById('btn-traducir');
const btnAcerca = document.getElementById('btn-acerca');
const btnTraducirName = document.getElementById('btn-traducir-ya');
const contenedorTraslate = document.getElementById('contenedor-traslate');
const InputAccion = document.getElementById('input-traducir');
const btnReset = document.getElementById('btn-reset');


let nombre;
let opcionImagen;
let remover;



//ESCUCHAMOS EN QUE MOMENTO SE DA CLICK PARA TRADUCIR
btnTraducirName.addEventListener('click', traduccion);

//FUNCION TRADUCCION
function traduccion(){
    //Aqui obtenemos el valor de input y lo guardamo en la variable nombre
    nombre = document.getElementById('input-traducir').value;

    if(nombre == ""){
        alert("Ingresa tu nombre!")
    }else{
        //AQUI DESCONPONE EL NOMBRE POR LETRA
        for(let i=0;i<nombre.length;i++){
            let descomposicion = nombre[i];
            //AQUI RECORRE EL ARREGLO PARA HACER LA VALIDACION
            for(let j=0;j<array.length;j++){
                //AQUI COMPARA LETRA DEL COMBRE CON CASO DEL ARREGLO
                if(descomposicion.toUpperCase() == array[j].case){
                    //AQUI CREAMOS LA ETIQUETA DE LA IMAGEN CORRESPONDIENTE
                    opcionImagen =  `
                        <img class="remove" src="${array[j].imagen}" alt="${array[j].name}">
                    `;

                    contenedorTraslate.innerHTML += opcionImagen;
                    btnTraducirName.disabled = true;
                    InputAccion.disabled = true;
                    btnReset.style.display = 'flex';
                }
            }
        }
    }

    btnReset.addEventListener('click', reseteo);
    //console.log(nombre.toUpperCase());
};


function reseteo(){
    location.reload();
}


//CUANDO RECIEN CARGA LA PAGINA
function inicar(){
    seccionAcerca.style.display = 'none';
    btnTraducir.classList.add('is-active');
    btnReset.style.display = 'none';
};

//INTERACCION BOTON TRADUCIR
btnTraducir.addEventListener('click', function(){
    seccionAcerca.style.display = 'none';
    btnAcerca.classList.remove('is-active');
    seccionTraducir.style.display = 'flex';
    btnTraducir.classList.add('is-active');
})

//INTERACCION BOTON ACERCA DE
btnAcerca.addEventListener('click', function(){
    seccionAcerca.style.display = 'flex';
    btnAcerca.classList.add('is-active');
    seccionTraducir.style.display = 'none';
    btnTraducir.classList.remove('is-active');
})





//Escuchamos si carga el contenido y llamamos funcion iniciar
window.addEventListener('load', inicar);