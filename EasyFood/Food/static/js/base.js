

let phone = document.getElementById('id_phone')
if(phone){
      phone.addEventListener('input', function(e) {
            const input = e.target;
            const value = input.value.replace(/\D/g, ''); // Elimina todos los caracteres no numéricos
      
            if (value.length <= 3) {
                  value = `(${value}`;
            } else if (value.length <= 6) {
                  value = `(${value.substring(0, 3)}) ${value.substring(3)}`;
            } else if (value.length <= 10) {
                  value = `(${value.substring(0, 3)}) ${value.substring(3, 6)}-${value.substring(6)}`;
            } else {
                  value = `(${value.substring(0, 3)}) ${value.substring(3, 6)}-${value.substring(6, 10)}`;
            }
            input.value = value;
      });
}


// Agregar animación al botón de carga masiva
function LoadMasiveImport() {
      const element = document.querySelector('.sec-top');
      if (element) {
            element.classList.toggle('d-none');
            element.classList.add('flip-up-ai')
      }
}


// Carga los usuarios desde un archivo Excel
function Load_Masive_Excel_Users() {
        var formData = new FormData();
        var fileInput = document.getElementById('file');
    
        // Asegurarse de que se haya seleccionado un archivo
        if (fileInput.files.length > 0) {
            formData.append('file', fileInput.files[0]);  
            
            // Agregar el archivo al FormData
            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajax({
                  url: '/company/upload-masive-user',
                  type: 'POST',
                  data: formData,
                  processData: false, // No procesar los datos
                  contentType: false, // No establecer tipo de contenido
                  headers: {
                        'X-CSRFToken': csrfToken, // Enviar el token CSRF con la solicitud
                  },
                  success: function(response) {
                        alert("Usuarios cargados exitosamente");
                  },
                  error: function(xhr, status, error) {
                        alert('Error al cargar el archivo');
                  }
            });
      }
}
