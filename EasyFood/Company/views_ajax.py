from django.http import JsonResponse
from django.contrib.auth.models import User
from . import models


import openpyxl
from django.contrib import messages
def Verify_Username_Ajax(request):
    username = request.GET.get('username', '').strip()
    if username:
        user_exists = User.objects.filter(username__iexact=username, is_active=True).exists()
        return JsonResponse({'exists': user_exists})
    return JsonResponse({'error': 'No username provided'}, status=400)


def Upload_Masive_User(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        try:
            # Cargar el archivo Excel usando openpyxl
            wb = openpyxl.load_workbook(file)
            sheet = wb.active  # Selecciona la primera hoja

            # Iterar sobre las filas del archivo Excel (comienza desde la fila 2 para saltar los encabezados)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if len(row) == 5:  # Asegúrate de que haya exactamente 5 valores
                    Usuario, Correo, Nombre, Apellidos, Contraseña = row  # Desempaqueta correctamente
                else:
                    continue 
                
                print(f"Usuario: {Usuario}, Correo: {Correo}, Nombre: {Nombre}, Apellidos: {Apellidos}, Contraseña: {Contraseña}")
                # Validar los datos del usuario (si es necesario agregar validaciones)
                if not Usuario or not Correo or not Contraseña:
                    continue  # Ignorar filas con datos faltantes (puedes personalizar esto)

                # Convertir Nombre y Apellidos a minúsculas
                Nombre = Nombre.lower() if Nombre else ''
                Apellidos = Apellidos.lower() if Apellidos else ''

                # Crear usuario
                user, created = User.objects.get_or_create(
                    username=str(Usuario),
                    defaults={
                        'email': str(Correo),
                        'first_name': str(Nombre),
                        'last_name': str(Apellidos),
                    }
                )
              # Crear empleado asociado
                try:
                    employe = models.Employee(
                        company =  request.user.employee_profile.company,  # Asignar la compañía del empleado logueado
                        user=user,
                        first_name=str(Nombre),
                        last_name=str(Apellidos),
                        email=str(Correo),
                    )
                    employe.save()
                except Exception as e:
                    # Si ocurre un error, capturamos la excepción y mostramos el mensaje
                    print(f"Error al crear el empleado: {e}")
                    return JsonResponse({'ok': False, 'message': f"Error al crear el empleado: {e}"}, status=400)

                # Si todo salió bien, puedes continuar con el flujo
                messages.success(request, "Empleado creado exitosamente.")
                if created:
                    user.set_password(Contraseña)
                    user.save()

                # Crear empleado asociado
            messages.success(request, "Usuarios cargados exitosamente.")
            ok = True
        except Exception as e:
            ok = False
            messages.error(request, f"Error al procesar el archivo: {e}")



    return JsonResponse({'ok': ok},  safe=False)