function obtenerID(){
    var combo=document.getElementById("categoria");
    var valor=combo.options[combo.options.selectedIndex].value;
    alert(valor);
}