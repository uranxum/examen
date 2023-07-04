function validar() {
    let resp;
    resp = validarPassword();
    if(resp = false){
        return false;
    }
 
 }

 //validar que las contraseñas sean iguales con javascript
function validarPassword() {
    let pass1 = document.getElementById('pwdPass1').value;
    let pass2 = document.getElementById('pwdPass2').value;

    if(pass1 == ''){
        alert('Debe ingresar una contraseña')
        return false;
    }else if(pass1 != pass2){
        alert('Las contraseñas deben ser iguales');
        return false;
    }else{
        return true;
        
   }
}
//validar el rut ccon jquery
$(document).ready(function() {
    $("#Enviar").click(function() {
    var rut = $("#txtRut").val();
      
    // Eliminar puntos y guión del Rut
    rut = rut.replace(/\./g,'');
    rut = rut.replace(/\-/g,'');
      
      // Validar formato del Rut
    if (!/^[0-9]{7,8}[kK0-9]$/.test(rut)) {
        alert("El Rut no tiene el formato correcto");
        return false;
       }
      
      // Validar dígito verificador
      var dv = rut.charAt(rut.length - 1);
      var rutSinDV = rut.substring(0, rut.length - 1);
      var suma = 0;
      var factor = 2;
      for (var i = rutSinDV.length - 1; i >= 0; i--) {
        suma += factor * rutSinDV.charAt(i);
         factor = factor === 7 ? 2 : factor + 1;
      }
      var dvCalculado = 11 - (suma % 11);
      if (dvCalculado === 11) {
        dvCalculado = "0";
      } else if (dvCalculado === 10) {
        dvCalculado = "K";
      }
      if (dv.toUpperCase() !== dvCalculado.toString()) {
        alert("El Rut no es válido");
        return false;
      }
    });
  });

  //validar el formato del correo con jquery
$(document).ready(function() {
  $("#Enviar").click(function() {
    var correo = $("#txtEmail").val();
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]{2,3}$/;
    if (!re.test(correo)) {
      alert("El correo electrónico no es válido");
      return false;
    }
    return true;
  });
});