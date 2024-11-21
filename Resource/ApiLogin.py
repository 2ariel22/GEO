from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

class ApiLogin:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["geo"]
        self.collection = self.db["users"]

    def guardar_usuario(self, nombre_completo, usuario, contrasena):
        if self.collection.find_one({"usuario": usuario}):
            return {"success": False, "message": "Usuario ya registrado"}

        hashed_password = generate_password_hash(contrasena)
        usuario_data = {
            "nombre_completo": nombre_completo,
            "usuario": usuario,
            "contrasena": hashed_password
        }
        self.collection.insert_one(usuario_data)
        return {"success": True, "message": "Usuario registrado exitosamente"}

    def consultar_usuario(self, usuario, contrasena):
        user_data = self.collection.find_one({"usuario": usuario})
        if not user_data:
            return {"success": False, "message": "Usuario no encontrado"}

        if not check_password_hash(user_data["contrasena"], contrasena):
            return {"success": False, "message": "Contraseña incorrecta"}

        return {"success": True, "message": "Usuario autenticado correctamente"}
