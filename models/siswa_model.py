# models/siswa_model.py — Model Representasi Data
from flask_restx import fields

def get_siswa_model(ns):
    return ns.model("Siswa", {
        "nama": fields.String(required=True),
        "alamat": fields.String(required=True)
    })
