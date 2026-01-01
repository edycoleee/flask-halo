# resources/siswa_resource.py — Endpoint RESTX
from flask import request
from flask_restx import Namespace, Resource
from models.siswa_model import get_siswa_model
from services.siswa_service import (
    get_all_siswa,
    get_siswa_by_id,
    create_siswa,
    update_siswa,
    delete_siswa
)

siswa_ns = Namespace("siswa", description="CRUD data siswa")

siswa_model = get_siswa_model(siswa_ns)

@siswa_ns.route("/")
class SiswaList(Resource):
    def get(self):
        return get_all_siswa(), 200

    @siswa_ns.expect(siswa_model)
    def post(self):
        data = request.get_json()
        create_siswa(data)
        return {"message": "Siswa ditambahkan"}, 201


@siswa_ns.route("/<int:id>")
class Siswa(Resource):
    def get(self, id):
        siswa = get_siswa_by_id(id)
        if siswa:
            return siswa, 200
        return {"message": "Siswa tidak ditemukan"}, 404

    @siswa_ns.expect(siswa_model)
    def put(self, id):
        data = request.get_json()
        update_siswa(id, data)
        return {"message": "Siswa diperbarui"}, 200

    def delete(self, id):
        delete_siswa(id)
        return {"message": "Siswa dihapus"}, 200
