from pymongo import MongoClient
from bson.objectid import ObjectId

class ApiEquipo:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["geo"]
        self.collection = self.db["equipos"]

    def agregar_equipo(self, nombre, ubicacion, serial, modelo, imagen):
        nuevo_equipo = {
            "name": nombre,
            "location": ubicacion,
            "serial": serial,
            "model": modelo,
            "img": imagen
        }
        result = self.collection.insert_one(nuevo_equipo)
        return str(result.inserted_id)

    def eliminar_equipo(self, equipo_id):
        result = self.collection.delete_one({"_id": ObjectId(equipo_id)})
        return result.deleted_count > 0

    def obtener_equipos(self):
        equipos = list(self.collection.find())
        for equipo in equipos:
            equipo["_id"] = str(equipo["_id"])  # Convertimos ObjectId a string
        return equipos

    def obtener_equipo_por_id(self, equipo_id):
        equipo = self.collection.find_one({"_id": ObjectId(equipo_id)})
        if equipo:
            equipo["_id"] = str(equipo["_id"])  # Convertimos ObjectId a string
        return equipo

    def actualizar_equipo(self, equipo_id, datos_actualizados):
        result = self.collection.update_one(
            {"_id": ObjectId(equipo_id)},
            {"$set": datos_actualizados}
        )
        return result.modified_count > 0
