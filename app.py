# # Flask Restx
# from flask import Flask
# from flask_restx import Api, Resource

# app = Flask(__name__)
# api = Api(app)  # Membungkus Flask menjadi REST API

# # Namespace
# halo_ns = api.namespace("halo", description="Contoh endpoint sederhana")

# # Resource
# @halo_ns.route("/")
# class Halo(Resource):
#     def get(self):
#         return {"Halo Flask-RESTX": True}
    
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

## ==================================================

# from flask import Flask
# from flask_restx import Api, Resource, Namespace, fields

# app = Flask(__name__)
# api = Api(app)

# # Namespace
# user_ns = Namespace("user", description="User operations")

# # Model untuk dokumentasi
# user_model = user_ns.model("User", {
#     "name": fields.String(required=True),
#     "age": fields.Integer(required=True)
# })

# @user_ns.route("/")
# class User(Resource):
#     @user_ns.expect(user_model)
#     def post(self):
#         data = user_ns.payload
#         return {"received": data}, 201

# api.add_namespace(user_ns)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

# # =========================================================

# import sqlite3
# from flask import Flask, request
# from flask_restx import Api, Resource, Namespace, fields

# app = Flask(__name__)
# api = Api(app)

# # -----------------------------
# #  DATABASE HELPER
# # -----------------------------
# def get_db():
#     conn = sqlite3.connect("siswa.db")
#     conn.row_factory = sqlite3.Row
#     return conn

# # Buat tabel jika belum ada
# with get_db() as db:
#     db.execute("""
#         CREATE TABLE IF NOT EXISTS tbsiswa (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             nama TEXT,
#             alamat TEXT
#         )
#     """)
#     db.commit()

# # -----------------------------
# #  NAMESPACE & MODEL
# # -----------------------------
# siswa_ns = Namespace("siswa", description="CRUD data siswa")

# siswa_model = siswa_ns.model("Siswa", {
#     "nama": fields.String(required=True),
#     "alamat": fields.String(required=True)
# })

# # -----------------------------
# #  RESOURCE: READ ALL & CREATE
# # -----------------------------
# @siswa_ns.route("/")
# class SiswaList(Resource):

#     def get(self):
#         """READ ALL"""
#         db = get_db()
#         rows = db.execute("SELECT * FROM tbsiswa").fetchall()
#         data = [dict(row) for row in rows]
#         return data, 200

#     @siswa_ns.expect(siswa_model)
#     def post(self):
#         """CREATE"""
#         data = request.get_json()
#         db = get_db()
#         db.execute(
#             "INSERT INTO tbsiswa (nama, alamat) VALUES (?, ?)",
#             (data["nama"], data["alamat"])
#         )
#         db.commit()
#         return {"message": "Siswa ditambahkan"}, 201


# # -----------------------------
# #  RESOURCE: READ ONE, UPDATE, DELETE
# # -----------------------------
# @siswa_ns.route("/<int:id>")
# class Siswa(Resource):

#     def get(self, id):
#         """READ ONE"""
#         db = get_db()
#         row = db.execute("SELECT * FROM tbsiswa WHERE id=?", (id,)).fetchone()
#         if row:
#             return dict(row), 200
#         return {"message": "Siswa tidak ditemukan"}, 404

#     @siswa_ns.expect(siswa_model)
#     def put(self, id):
#         """UPDATE"""
#         data = request.get_json()
#         db = get_db()
#         db.execute(
#             "UPDATE tbsiswa SET nama=?, alamat=? WHERE id=?",
#             (data["nama"], data["alamat"], id)
#         )
#         db.commit()
#         return {"message": "Siswa diperbarui"}, 200

#     def delete(self, id):
#         """DELETE"""
#         db = get_db()
#         db.execute("DELETE FROM tbsiswa WHERE id=?", (id,))
#         db.commit()
#         return {"message": "Siswa dihapus"}, 200


# # Tambahkan namespace
# api.add_namespace(siswa_ns)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

# # =========================================================
# ### 7. Struktur folder profesional untuk Flask‑RESTX
# # app.py — Entry Point
# from flask import Flask
# from flask_restx import Api
# from resources.siswa_resource import siswa_ns

# app = Flask(__name__)
# api = Api(app)

# api.add_namespace(siswa_ns)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

# # =========================================================
# ### 8. UI sederhana dengan HTML + Bootstrap
# app.py — Render Template + RESTX API
from flask import Flask, render_template
from flask_restx import Api
from resources.siswa_resource import siswa_ns

app = Flask(__name__)
#api = Api(app, doc="/docs")
api = Api(app, doc="/docs", prefix="/api")

# Tambahkan namespace REST API
api.add_namespace(siswa_ns)

# Route untuk UI
@app.route("/")
def index():
    return render_template("crud.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)