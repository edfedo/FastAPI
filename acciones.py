from experto_general.engine import Engine  # Importa la clase Engine desde el módulo experto_general.engine


# Motor como variable global
engine = Engine()  # Crea una instancia global de Engine que actuará como el motor de inferencia


def insertar(nombre, prop):  # Define la función insertar con dos parámetros: nombre y prop
    if nombre and prop:  # Verifica que los parámetros no sean valores vacíos
        entry = engine.base.get_or_add_entry(nombre)  # Busca una entrada en la base con el nombre dado; si no existe, la crea
        entry.get_or_add_prop(prop)  # Busca una propiedad en la entrada; si no existe, la agrega
        return f"Entrada agregada: {entry}"  # Devuelve un mensaje de éxito indicando que la entrada se agregó o ya existía
    else:
        return "No se admiten valores vacíos"  # Si falta alguno de los parámetros, devuelve un mensaje de error


def get_base_entries():  # Define la función get_base_entries sin parámetros
    # Devuelve todas las entradas en la base de conocimiento
    return engine.base.entries  # Devuelve una lista de todas las entradas almacenadas en la base de conocimiento de Engine


def guardar(entrada):  # Define la función guardar con el parámetro entrada, que representa el nombre del archivo a guardar
    if entrada:  # Verifica que el parámetro no esté vacío
        engine.base.to_json(entrada.strip())  # Llama a la función to_json del motor para guardar la base de conocimiento en un archivo JSON
        return "El archivo fue guardado con éxito"  # Devuelve un mensaje de éxito si se guardó correctamente
    else:
        return "Elige un nombre para el archivo"  # Si falta el nombre del archivo, devuelve un mensaje de error


def cargar(entrada):  # Define la función cargar con el parámetro entrada, que representa el nombre del archivo a cargar
    if entrada:  # Verifica que el parámetro no esté vacío
        try:
            engine.base.from_json(entrada.strip())  # Llama a la función from_json del motor para cargar la base de conocimiento desde un archivo JSON
            return "El archivo fue cargado con éxito"  # Devuelve un mensaje de éxito si se cargó correctamente
        except KeyError:  # Maneja el caso donde el archivo tiene un formato incorrecto o no se puede cargar
            return "Archivo inválido o con formato incorrecto"  # Devuelve un mensaje de error en caso de excepción
    else:
        return "Elige un nombre del archivo a cargar"  # Si falta el nombre del archivo, devuelve un mensaje de error

