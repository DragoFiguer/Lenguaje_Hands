
function alta() {
    
    var nombre = document.getElementById("nombre").value;
    localStorage.setItem("Nombre", nombre);
     //alert("Usuario registrado  ");
    document.getElementById("nombre").value="";
}
function limpiar() {
    document.getElementById("formulario").reset();
  }



