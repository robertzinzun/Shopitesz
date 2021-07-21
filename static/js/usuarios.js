function imprimirMsg(){
    alert('Se hizo click');
}
function validar(form){
    var cad=validarPassword(form.password.value);
    cad+=validarPasswords(form.password.value,form.passwordConfirmacion.value);
    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}
function validarPassword(pwd){
    if(pwd.length<8){
        return 'El password debe ser de al menos 8 caracteres<br>';
    }
    else{
        return '';
    }
}
function validarPasswords(pwd1,pwd2){
    if(pwd1!=pwd2){
        return 'Los password no coinciden<br>';
    }
    else{
        return '';
    }
}
function verPasswords(){
    var check=document.getElementById("verPassword");
    if(check.checked){
        document.getElementById("password").setAttribute('type','text')
        document.getElementById("passwordConfirmacion").setAttribute('type','text')
    }
    else{
        document.getElementById("password").setAttribute('type','password')
        document.getElementById("passwordConfirmacion").setAttribute('type','password')
    }
}