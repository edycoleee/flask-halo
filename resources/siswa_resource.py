# resources/siswa_resource.py — Endpoint RESTX
from flask import request
from flask_restx import Namespace, Resource, reqparse
from models.siswa_model import get_siswa_model
from services.siswa_service import (
    get_all_siswa,
    get_siswa_by_id,
    create_siswa,
    update_siswa,
    delete_siswa
)
import os
from werkzeug.utils import secure_filename
from flask import request, current_app
from services.siswa_service import update_foto
from werkzeug.datastructures import FileStorage

siswa_ns = Namespace("siswa", description="CRUD data siswa")

siswa_model = get_siswa_model(siswa_ns)

UPLOAD_FOLDER = "pictures"
ALLOWED_EXT = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 2 * 1024 * 1024 # 2MB

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

# PARSER UNTUK SWAGGER
upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    "file",
    location="files",
    type=FileStorage,
    required=True,
    help="Upload foto siswa"
)


@siswa_ns.route("/")
class SiswaList(Resource):
    def get(self):
        return get_all_siswa(), 200

    @siswa_ns.expect(siswa_model)
    def post(self):
        data = request.get_json()
        new_id = create_siswa(data)
        # create_siswa(data)
        return {"message": "Siswa ditambahkan","id": new_id}, 201


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

@siswa_ns.route("/<int:id>/foto")
class UploadFoto(Resource):

    @siswa_ns.expect(upload_parser)
    def post(self, id):
        """Upload foto siswa"""

        args = upload_parser.parse_args()
        file = args["file"]

        siswa = get_siswa_by_id(id)
        if not siswa:
            return {"message": "Siswa tidak ditemukan"}, 404

        if file is None or file.filename == "":
            return {"message": "File tidak ditemukan"}, 400

        if not allowed_file(file.filename):
            return {"message": "Format file tidak diizinkan"}, 400

        # Pastikan folder upload ada
        upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
        os.makedirs(upload_path, exist_ok=True)

        filename = secure_filename(f"siswa_{id}_{file.filename}")
        filepath = os.path.join(upload_path, filename)

        file.save(filepath)

        update_foto(id, filename)

        return {
            "message": "Foto berhasil diupload",
            "filename": filename
        }, 201
