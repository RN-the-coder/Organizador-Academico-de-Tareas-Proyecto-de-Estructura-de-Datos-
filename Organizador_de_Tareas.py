
import pandas as pd
import os
from collections import deque

# Archivos donde se guardarán las tareas
ARCHIVO_TAREAS = 'tareas_pendientes.csv'
ARCHIVO_HISTORIAL = 'historial_completadas.csv'

def cargar_datos():
    """
    Carga las tareas pendientes y el historial desde archivos CSV.
    Si los archivos no existen, crea DataFrames y listas vacías.
    """
    # Cargar tareas pendientes
    if os.path.exists(ARCHIVO_TAREAS):
        tareas_df = pd.read_csv(ARCHIVO_TAREAS)
    else:
        tareas_df = pd.DataFrame(columns=['Materia', 'Descripcion', 'Fecha de Entrega', 'Estado'])

    # Cargar historial
    if os.path.exists(ARCHIVO_HISTORIAL):
        historial_df = pd.read_csv(ARCHIVO_HISTORIAL)
        historial_pila = deque(historial_df.to_dict('records'))
    else:
        historial_pila = deque()

    return tareas_df, historial_pila


def guardar_datos(tareas_df, historial_pila):
    """Guarda el DataFrame de tareas pendientes y el historial en archivos CSV."""
    tareas_df.to_csv(ARCHIVO_TAREAS, index=False)

    historial_df = pd.DataFrame(list(historial_pila))
    historial_df.to_csv(ARCHIVO_HISTORIAL, index=False)

    print("\n¡Datos guardados exitosamente!")



def agregar_tarea(tareas_df):
    """Solicita al usuario los datos de una nueva tarea y la añade al DataFrame."""
    print("\n--- Agregar Nueva Tarea ---")
    materia = input("Materia: ")
    descripcion = input("Descripción: ")
    fecha_entrega = input("Fecha de Entrega (YYYY-MM-DD): ")

    nueva_tarea = pd.DataFrame({
        'Materia': [materia],
        'Descripcion': [descripcion],
        'Fecha de Entrega': [fecha_entrega],
        'Estado': ['Pendiente']
    })

    tareas_df = pd.concat([tareas_df, nueva_tarea], ignore_index=True)

    print("\n¡Tarea agregada correctamente!")
    return tareas_df


def mostrar_tareas_pendientes(tareas_df):
    """Organiza y muestra las tareas pendientes."""
    print("\n--- Tareas Pendientes ---")
    if tareas_df.empty:
        print("¡No tienes tareas pendientes! ¡Excelente!")
    else:
        tareas_organizadas = tareas_df.sort_values(by=['Fecha de Entrega', 'Materia'])
        print(tareas_organizadas.reset_index(drop=True).rename(index=lambda x: x + 1))



def marcar_tarea_completada(tareas_df, historial_pila):
    """Marca una tarea como completada y la mueve al historial."""
    mostrar_tareas_pendientes(tareas_df)

    if tareas_df.empty:
        return tareas_df, historial_pila

    try:
        num_tarea = int(input("\nIngresa el número de la tarea que quieres marcar como completada (0 para cancelar): "))

        if num_tarea == 0:
            return tareas_df, historial_pila

        indice_real = tareas_df.sort_values(by=['Fecha de Entrega', 'Materia']).index[num_tarea - 1]

        tarea_completada = tareas_df.loc[indice_real].to_dict()
        tarea_completada['Estado'] = 'Completada'

        historial_pila.appendleft(tarea_completada)

        tareas_df = tareas_df.drop(indice_real)

        print(f"\n¡Tarea '{tarea_completada['Descripcion']}' marcada como completada!")

    except (ValueError, IndexError):
        print("\nError: Número de tarea no válido. Inténtalo de nuevo.")

    return tareas_df, historial_pila


def mostrar_historial(historial_pila):
    """Muestra el historial de tareas completadas."""
    print("\n--- Historial de Tareas Completadas ---")
    if not historial_pila:
        print("Aún no has completado ninguna tarea.")
    else:
        for i, tarea in enumerate(historial_pila, 1):
            print(f"{i}. Materia: {tarea['Materia']}, Descripción: {tarea['Descripcion']}, Fecha: {tarea['Fecha de Entrega']}")



def main():
    """Función principal que ejecuta el menú del programa."""
    tareas_df, historial_pila = cargar_datos()

    while True:
        print("\n===== Gestor de Tareas Escolares =====")
        print("1. Agregar nueva tarea")
        print("2. Ver tareas pendientes (organizadas)")
        print("3. Marcar tarea como completada")
        print("4. Ver historial de tareas completadas")
        print("5. Guardar y Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            tareas_df = agregar_tarea(tareas_df)
        elif opcion == '2':
            mostrar_tareas_pendientes(tareas_df)
        elif opcion == '3':
            tareas_df, historial_pila = marcar_tarea_completada(tareas_df, historial_pila)
        elif opcion == '4':
            mostrar_historial(historial_pila)
        elif opcion == '5':
            guardar_datos(tareas_df, historial_pila)
            break
        else:
            print("\nOpción no válida. Por favor, elige de nuevo.")


# Punto de entrada
if __name__ == "__main__":
    main()
