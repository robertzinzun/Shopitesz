function obtenerID(){
    var combo=document.getElementById("categoria");
    var idCategoria=combo.options[combo.options.selectedIndex].value;
    var ajax=new XMLHttpRequest();
    var url='/productos/categoria/'+idCategoria;
    ajax.open('get',url,true);
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
           llenarTabla(this.responseText);
        }
    };
    ajax.send();
}
function imprimirMsg(){
    alert('Documento cargado');
}
function llenarTabla(datos){
    var tabla=document.getElementById("datos");
    var productos=JSON.parse(datos);
    eliminarTabla();
    for(i=0;i<productos.length;i++){
        var tr=document.createElement("tr");
        var prod=productos[i];
        for (propiedad in prod){
            //alert(propiedad);
            //alert(prod[propiedad]);
            var td=document.createElement("td");
            var texto=document.createTextNode(prod[propiedad]);
            td.appendChild(texto);
            tr.appendChild(td);
        }
        var text=document.createElement("input");
        text.setAttribute("type","number");
        text.setAttribute("min","1");
        text.setAttribute("max",prod.existencia);
        text.setAttribute("value",1);
        text.setAttribute("id","cantidad");
        td=document.createElement("td");
        td.appendChild(text);
        tr.appendChild(td);
        var link=crearLink();
        td=document.createElement("td");
        td.appendChild(link);
        tr.appendChild(td);
        tabla.appendChild(tr);
        var cantidad=document.getElementById("cantidad").value;
        link.setAttribute("href","/carrito/agregar/id="+prod.idProducto+"&cantidad="+cantidad);
        
    }
}
function eliminarTabla(){
    var tabla=document.getElementById("datos");
    //alert(tabla.rows.length);
    for(i=tabla.rows.length-1;i>0;i--){
		tabla.removeChild(tabla.rows[i]);
	}
}
function crearLink(){
    var link=document.createElement("a");
    //alert(producto.idProducto);
    
    link.setAttribute("data-toggle","modal");
    link.setAttribute("data-target","#producto");
    var span=document.createElement("span");
    span.setAttribute("class","glyphicon glyphicon-shopping-cart");
    link.appendChild(span);
    return link;
}
function consultarProducto(id){
    var ajax=new XMLHttpRequest();
    url='/producto/'+id;
    ajax.open('get',url,true);
    ajax.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4){
            var producto=JSON.parse(this.responseText);
            document.getElementById("id").value=producto.idProducto;
        }
    };
    ajax.send();
}