from Resource.ApiEquipo import ApiEquipo

def main():
    # Crear instancia de la API
    api = ApiEquipo()
    
    # Solicitar ID del equipo
    equipo_id = input("Ingrese el ID del equipo que desea actualizar: ")
    
    # Verificar si el equipo existe
    equipo = api.obtener_equipo_por_id(equipo_id)
    if not equipo:
        print("No se encontró ningún equipo con ese ID")
        return
    
    # Mostrar ubicación actual
    print(f"Ubicación actual: {equipo['location']}")
    
    # Solicitar nueva ubicación
    nueva_ubicacion = input("Ingrese la nueva ubicación: ")
    
    # Actualizar la ubicación
    actualizado = api.actualizar_equipo(equipo_id, {"location": nueva_ubicacion})
    
    # Mostrar resultado
    if actualizado:
        print("Ubicación actualizada exitosamente")
    else:
        print("No se pudo actualizar la ubicación")

if __name__ == "__main__":
    main()