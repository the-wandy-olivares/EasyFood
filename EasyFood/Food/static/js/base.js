

let phone = document.getElementById('id_phone');

if (phone) {
    phone.addEventListener('input', function (e) {
        const input = e.target;
        const rawValue = input.value.replace(/\D/g, ''); // Elimina caracteres no numéricos
        let formattedValue = ''; // Nueva variable para el valor formateado

        if (rawValue.length <= 3) {
            formattedValue = `(${rawValue}`;
        } else if (rawValue.length <= 6) {
            formattedValue = `(${rawValue.substring(0, 3)}) ${rawValue.substring(3)}`;
        } else {
            formattedValue = `(${rawValue.substring(0, 3)}) ${rawValue.substring(3, 6)}-${rawValue.substring(6, 10)}`;
        }

        input.value = formattedValue;
    });
}


let contact_representant = document.getElementById('id_contact_representante');

if (contact_representant) {
    contact_representant.addEventListener('input', function (e) {
        const input = e.target;
        const rawValue = input.value.replace(/\D/g, ''); // Elimina caracteres no numéricos
        let formattedValue = ''; // Nueva variable para el valor formateado

        if (rawValue.length <= 3) {
            formattedValue = `(${rawValue}`;
        } else if (rawValue.length <= 6) {
            formattedValue = `(${rawValue.substring(0, 3)}) ${rawValue.substring(3)}`;
        } else {
            formattedValue = `(${rawValue.substring(0, 3)}) ${rawValue.substring(3, 6)}-${rawValue.substring(6, 10)}`;
        }

        input.value = formattedValue;
    });
}

const dniInput = document.getElementById('id_dni');
if (dniInput) {
    dniInput.addEventListener('input', () => {
        // Obtener solo los números
        let dni = dniInput.value.replace(/\D/g, "");

        // Aplicar formato
        if (dni.length > 3 && dni.length <= 10) {
            dni = `${dni.slice(0, 3)}-${dni.slice(3)}`;
        } else if (dni.length > 10) {
            dni = `${dni.slice(0, 3)}-${dni.slice(3, 10)}-${dni.slice(10)}`;
        }

        // Actualizar el valor del campo de entrada
        dniInput.value = dni;
    });
}

// Agregar animación al botón de carga masiva
function LoadMasiveImport() {
      const element = document.querySelector('.sec-top');
      if (element) {
            element.classList.toggle('d-none');
            element.classList.add('flip-down-ai')
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
