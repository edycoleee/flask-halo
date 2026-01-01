## FLASK

### 1. Persiapan 

```py
# Update sistem
sudo apt update
sudo apt upgrade -y

# Install python3-venv jika belum ada
sudo apt install python3-venv -y

# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate # Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install package yang diperlukan
pip install flask flask-restx

```


### 2. Hierarki Flask‑RESTX 

```Code
Api
 ├── Namespace "auth"
 │     ├── Resource Login
 │     └── Resource Register
 ├── Namespace "dicom"
 │     ├── Resource Upload
 │     └── Resource Metadata
 └── Namespace "admin"
       └── Resource Dashboard
```
🔹 Api >> Objek utama yang membungkus seluruh REST API.

🔹 Namespace >> Mirip folder atau modul. >> Dipakai untuk memisahkan endpoint berdasarkan domain. >> Contoh: /auth, /dicom, /admin.

🔹 Resource >> Class yang berisi method HTTP: get(), post(), put(), delete(). >> Setiap Resource = satu endpoint.

🔹 Model >> Dipakai untuk dokumentasi dan validasi payload.

### 3. Flask Sederhana

```
# Flask Sederhana
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/halo", methods=["GET"])
def halo():
    return jsonify({"Halo Flask": True})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

```

### 4. Flask Restx Sederhana

```
# Flask Restx Sederhana
from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)  # Membungkus Flask menjadi REST API

# Namespace
halo_ns = api.namespace("halo", description="Contoh endpoint sederhana")

# Resource
@halo_ns.route("/")
class Halo(Resource):
    def get(self):
        return {"Halo Flask-RESTX": True}
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

```
http://192.168.30.14:5000/ >> swagger

http://192.168.30.14:5000/halo/

### 5. Flask Restx Namespace dan Model

```
# Flask Restx Namespace dan Model
from flask import Flask
from flask_restx import Api, Resource, Namespace, fields

app = Flask(__name__)
api = Api(app)

# Namespace
user_ns = Namespace("user", description="User operations")

# Model untuk dokumentasi
user_model = user_ns.model("User", {
    "name": fields.String(required=True),
    "age": fields.Integer(required=True)
})

@user_ns.route("/")
class User(Resource):
    @user_ns.expect(user_model)
    def post(self):
        data = user_ns.payload
        return {"received": data}, 201

api.add_namespace(user_ns)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

```

### 6. CRUD flask-restx

```Code
tbsiswa(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    alamat TEXT
)
```
```py
import sqlite3
from flask import Flask, request
from flask_restx import Api, Resource, Namespace, fields

app = Flask(__name__)
api = Api(app)

# -----------------------------
#  DATABASE HELPER
# -----------------------------
def get_db():
    conn = sqlite3.connect("siswa.db")
    conn.row_factory = sqlite3.Row
    return conn

# Buat tabel jika belum ada
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS tbsiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            alamat TEXT
        )
    """)
    db.commit()

# -----------------------------
#  NAMESPACE & MODEL
# -----------------------------
siswa_ns = Namespace("siswa", description="CRUD data siswa")

siswa_model = siswa_ns.model("Siswa", {
    "nama": fields.String(required=True),
    "alamat": fields.String(required=True)
})

# -----------------------------
#  RESOURCE: READ ALL & CREATE
# -----------------------------
@siswa_ns.route("/")
class SiswaList(Resource):

    def get(self):
        """READ ALL"""
        db = get_db()
        rows = db.execute("SELECT * FROM tbsiswa").fetchall()
        data = [dict(row) for row in rows]
        return data, 200

    @siswa_ns.expect(siswa_model)
    def post(self):
        """CREATE"""
        data = request.get_json()
        db = get_db()
        db.execute(
            "INSERT INTO tbsiswa (nama, alamat) VALUES (?, ?)",
            (data["nama"], data["alamat"])
        )
        db.commit()
        return {"message": "Siswa ditambahkan"}, 201


# -----------------------------
#  RESOURCE: READ ONE, UPDATE, DELETE
# -----------------------------
@siswa_ns.route("/<int:id>")
class Siswa(Resource):

    def get(self, id):
        """READ ONE"""
        db = get_db()
        row = db.execute("SELECT * FROM tbsiswa WHERE id=?", (id,)).fetchone()
        if row:
            return dict(row), 200
        return {"message": "Siswa tidak ditemukan"}, 404

    @siswa_ns.expect(siswa_model)
    def put(self, id):
        """UPDATE"""
        data = request.get_json()
        db = get_db()
        db.execute(
            "UPDATE tbsiswa SET nama=?, alamat=? WHERE id=?",
            (data["nama"], data["alamat"], id)
        )
        db.commit()
        return {"message": "Siswa diperbarui"}, 200

    def delete(self, id):
        """DELETE"""
        db = get_db()
        db.execute("DELETE FROM tbsiswa WHERE id=?", (id,))
        db.commit()
        return {"message": "Siswa dihapus"}, 200


# Tambahkan namespace
api.add_namespace(siswa_ns)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

```

### 7. Struktur folder profesional untuk Flask‑RESTX

```
project/
│
├── app.py
├── database.py
│
├── models/
│   └── siswa_model.py
│
├── services/
│   └── siswa_service.py
│
└── resources/
    └── siswa_resource.py
```

```py
# ========================================
# database.py — Helper SQLite
import sqlite3

def get_db():
    conn = sqlite3.connect("siswa.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS tbsiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            alamat TEXT
        )
    """)
    db.commit()

# ========================================
# models/siswa_model.py — Model Representasi Data
from flask_restx import fields

def get_siswa_model(ns):
    return ns.model("Siswa", {
        "nama": fields.String(required=True),
        "alamat": fields.String(required=True)
    })

# ========================================
# services/siswa_service.py — Logika CRUD
from database import get_db

def get_all_siswa():
    db = get_db()
    rows = db.execute("SELECT * FROM tbsiswa").fetchall()
    return [dict(row) for row in rows]

def get_siswa_by_id(id):
    db = get_db()
    row = db.execute("SELECT * FROM tbsiswa WHERE id=?", (id,)).fetchone()
    return dict(row) if row else None

def create_siswa(data):
    db = get_db()
    db.execute(
        "INSERT INTO tbsiswa (nama, alamat) VALUES (?, ?)",
        (data["nama"], data["alamat"])
    )
    db.commit()

def update_siswa(id, data):
    db = get_db()
    db.execute(
        "UPDATE tbsiswa SET nama=?, alamat=? WHERE id=?",
        (data["nama"], data["alamat"], id)
    )
    db.commit()

def delete_siswa(id):
    db = get_db()
    db.execute("DELETE FROM tbsiswa WHERE id=?", (id,))
    db.commit()

# ========================================
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

# ========================================
# app.py — Entry Point
from flask import Flask
from flask_restx import Api
from resources.siswa_resource import siswa_ns

app = Flask(__name__)
api = Api(app)

api.add_namespace(siswa_ns)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

```
### 8. UI sederhana dengan HTML + Bootstrap

templates/crud.html >> Letakkan file ini di:

```Code
project/
└── templates/
    └── crud.html
```
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CRUD Siswa</title>
    <link rel="stylesheet" 
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>

<body class="bg-light">

    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="#">Manajemen Siswa</a>
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link active" href="#">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="#">About</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">

        <!-- TITLE -->
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h3>Data Siswa</h3>
            <button class="btn btn-primary" onclick="showAddForm()">Tambah Siswa</button>
        </div>

        <!-- TABLE -->
        <table class="table table-bordered table-striped">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Nama</th>
                    <th>Alamat</th>
                    <th width="150">Aksi</th>
                </tr>
            </thead>
            <tbody id="table-body">
                <!-- Data akan di-load via JS -->
            </tbody>
        </table>

        <!-- FORM -->
        <div class="card mt-4" id="form-card" style="display:none;">
            <div class="card-header bg-primary text-white">
                <span id="form-title">Tambah Siswa</span>
            </div>
            <div class="card-body">
                <form id="siswa-form">
                    <input type="hidden" id="form-id">

                    <div class="mb-3">
                        <label>Nama</label>
                        <input type="text" id="form-nama" class="form-control" required>
                    </div>

                    <div class="mb-3">
                        <label>Alamat</label>
                        <input type="text" id="form-alamat" class="form-control" required>
                    </div>

                    <button type="submit" class="btn btn-success">Simpan</button>
                    <button type="button" class="btn btn-secondary" onclick="hideForm()">Batal</button>
                </form>
            </div>
        </div>

    </div>

<script>
const API = "/api/siswa";

// LOAD DATA
function loadData() {
    fetch(API)
        .then(res => res.json())
        .then(data => {
            let rows = "";
            data.forEach(s => {
                rows += `
                    <tr>
                        <td>${s.id}</td>
                        <td>${s.nama}</td>
                        <td>${s.alamat}</td>
                        <td>
                            <button class="btn btn-sm btn-warning" onclick="editData(${s.id})">Edit</button>
                            <button class="btn btn-sm btn-danger" onclick="deleteData(${s.id})">Hapus</button>
                        </td>
                    </tr>
                `;
            });
            document.getElementById("table-body").innerHTML = rows;
        });
}

// SHOW ADD FORM
function showAddForm() {
    document.getElementById("form-card").style.display = "block";
    document.getElementById("form-title").innerText = "Tambah Siswa";
    document.getElementById("form-id").value = "";
    document.getElementById("form-nama").value = "";
    document.getElementById("form-alamat").value = "";
}

// HIDE FORM
function hideForm() {
    document.getElementById("form-card").style.display = "none";
}

// EDIT DATA
function editData(id) {
    fetch(`${API}/${id}`)
        .then(res => res.json())
        .then(s => {
            document.getElementById("form-card").style.display = "block";
            document.getElementById("form-title").innerText = "Edit Siswa";

            document.getElementById("form-id").value = s.id;
            document.getElementById("form-nama").value = s.nama;
            document.getElementById("form-alamat").value = s.alamat;
        });
}

// DELETE DATA
function deleteData(id) {
    if (!confirm("Yakin ingin menghapus?")) return;

    fetch(`${API}/${id}`, { method: "DELETE" })
        .then(() => loadData());
}

// SUBMIT FORM
document.getElementById("siswa-form").addEventListener("submit", function(e) {
    e.preventDefault();

    const id = document.getElementById("form-id").value;
    const data = {
        nama: document.getElementById("form-nama").value,
        alamat: document.getElementById("form-alamat").value
    };

    const method = id ? "PUT" : "POST";
    const url = id ? `${API}/${id}` : API;

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    }).then(() => {
        hideForm();
        loadData();
    });
});

// INITIAL LOAD
loadData();
</script>

</body>
</html>

```
```py
# app.py — Render Template + RESTX API
from flask import Flask, render_template
from flask_restx import Api
from resources.siswa_resource import siswa_ns

app = Flask(__name__)
api = Api(app)

# Tambahkan namespace REST API
api.add_namespace(siswa_ns)

# Route untuk UI
@app.route("/")
def index():
    return render_template("crud.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

Swagger pindah ke /docs, supaya tidak sama dengan UI:

```python
api = Api(app, doc="/docs", prefix="/api")
```

### 9. Docker compose 

```
# Struktur Folder Final

project/
│
├── app.py
├── database.py
├── Dockerfile
├── docker-compose.yml
│
├── templates/
│   └── crud.html
│
├── models/
│   └── siswa_model.py
│
├── services/
│   └── siswa_service.py
│
└── resources/
    └── siswa_resource.py
```



Dockerfile (Flask + Gunicorn)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

requirements.txt
```Code
flask
flask-restx
gunicorn
```

docker-compose.yml

```yaml
version: "3.9"

services:
  flaskapp:
    build: .
    container_name: siswa_api
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    restart: always
```

Cara Menjalankan
- Build
```Code
docker compose build
```
- Run
```Code
docker compose up
```
- Akses

UI CRUD → http://localhost:5000

API → http://localhost:5000/api/siswa

Swagger → http://localhost:5000/docs


### 10. API upload foto siswa

POST api/siswa/<id>/foto → upload foto

Update Database: Tambah Kolom foto

Edit database.py:

```python
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS tbsiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            alamat TEXT,
            foto TEXT
        )
    """)
    db.commit()
```
Hapus tabel lama (cara mudah), Jika tabel sudah ada dan ingin mepertahankan isinya, tambahkan kolom manual:

```sql
ALTER TABLE tbsiswa ADD COLUMN foto TEXT;
```
Buat folder penyimpanan foto >> Di root project:

```Code
mkdir pictures
```

Update Service Layer (services/siswa_service.py) >> Tambahkan fungsi untuk menyimpan nama file foto:

```python

def update_foto(id, filename):
    db = get_db()
    db.execute("UPDATE tbsiswa SET foto=? WHERE id=?", (filename, id))
    db.commit()
```

Tambahkan API Upload Foto (resources/siswa_resource.py) >> Tambahkan import:

```python
import os
from werkzeug.utils import secure_filename
from flask import request, current_app
from services.siswa_service import update_foto
```
Tambahkan Resource baru:

```python
UPLOAD_FOLDER = "pictures"
ALLOWED_EXT = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@siswa_ns.route("/<int:id>/foto")
class UploadFoto(Resource):
    def post(self, id):
        """Upload foto siswa"""
        if "file" not in request.files:
            return {"message": "File tidak ditemukan"}, 400

        file = request.files["file"]

        if file.filename == "":
            return {"message": "Nama file kosong"}, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(f"siswa_{id}_" + file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            file.save(filepath)

            update_foto(id, filename)

            return {"message": "Foto berhasil diupload", "filename": filename}, 201

        return {"message": "Format file tidak diizinkan"}, 400
```
Update app.py agar folder foto bisa diakses >> Tambahkan:

```python
from flask import send_from_directory

@app.route("/pictures/<filename>")
def get_picture(filename):
    return send_from_directory("pictures", filename)
```

Endpoint Baru

Method >>	Endpoint >>	Fungsi
POST >>	api/siswa//foto	>> Upload foto siswa
GET	>> api/pictures/	>> Mengambil foto siswa

Contoh Upload via cURL / Postman
Upload foto:
```Code
POST /siswa/5/foto
Form-Data:
file = (pilih file)
```

templates/crud.html (versi lengkap + upload foto + preview)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CRUD Siswa</title>
    <link rel="stylesheet" 
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>

<body class="bg-light">

    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="#">Manajemen Siswa</a>
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link active" href="#">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="#">About</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">

        <!-- TITLE -->
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h3>Data Siswa</h3>
            <button class="btn btn-primary" onclick="showAddForm()">Tambah Siswa</button>
        </div>

        <!-- TABLE -->
        <table class="table table-bordered table-striped">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Nama</th>
                    <th>Alamat</th>
                    <th>Foto</th>
                    <th width="200">Aksi</th>
                </tr>
            </thead>
            <tbody id="table-body">
                <!-- Data akan di-load via JS -->
            </tbody>
        </table>

        <!-- FORM -->
        <div class="card mt-4" id="form-card" style="display:none;">
            <div class="card-header bg-primary text-white">
                <span id="form-title">Tambah Siswa</span>
            </div>
            <div class="card-body">
                <form id="siswa-form">
                    <input type="hidden" id="form-id">

                    <div class="mb-3">
                        <label>Nama</label>
                        <input type="text" id="form-nama" class="form-control" required>
                    </div>

                    <div class="mb-3">
                        <label>Alamat</label>
                        <input type="text" id="form-alamat" class="form-control" required>
                    </div>

                    <button type="submit" class="btn btn-success">Simpan</button>
                    <button type="button" class="btn btn-secondary" onclick="hideForm()">Batal</button>
                </form>
            </div>
        </div>

    </div>

    <!-- MODAL UPLOAD FOTO -->
    <div class="modal fade" id="uploadModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">

                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title">Upload Foto Siswa</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body">
                    <img id="preview-img" src="" class="img-fluid mb-3 d-none" alt="Preview Foto">

                    <input type="file" id="foto-file" class="form-control" accept="image/*">
                    <input type="hidden" id="foto-id">
                </div>

                <div class="modal-footer">
                    <button class="btn btn-primary" onclick="uploadFoto()">Upload</button>
                    <button class="btn btn-secondary" data-bs-dismiss="modal">Tutup</button>
                </div>

            </div>
        </div>
    </div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<script>
const API = "api/siswa";

// LOAD DATA
function loadData() {
    fetch(API)
        .then(res => res.json())
        .then(data => {
            let rows = "";
            data.forEach(s => {
                const fotoUrl = s.foto ? `/pictures/${s.foto}` : "https://via.placeholder.com/80";

                rows += `
                    <tr>
                        <td>${s.id}</td>
                        <td>${s.nama}</td>
                        <td>${s.alamat}</td>
                        <td><img src="${fotoUrl}" width="80" class="img-thumbnail"></td>
                        <td>
                            <button class="btn btn-sm btn-warning" onclick="editData(${s.id})">Edit</button>
                            <button class="btn btn-sm btn-danger" onclick="deleteData(${s.id})">Hapus</button>
                            <button class="btn btn-sm btn-info" onclick="openUpload(${s.id}, '${s.foto || ''}')">Upload Foto</button>
                        </td>
                    </tr>
                `;
            });
            document.getElementById("table-body").innerHTML = rows;
        });
}

// SHOW ADD FORM
function showAddForm() {
    document.getElementById("form-card").style.display = "block";
    document.getElementById("form-title").innerText = "Tambah Siswa";
    document.getElementById("form-id").value = "";
    document.getElementById("form-nama").value = "";
    document.getElementById("form-alamat").value = "";
}

// HIDE FORM
function hideForm() {
    document.getElementById("form-card").style.display = "none";
}

// EDIT DATA
function editData(id) {
    fetch(`${API}/${id}`)
        .then(res => res.json())
        .then(s => {
            document.getElementById("form-card").style.display = "block";
            document.getElementById("form-title").innerText = "Edit Siswa";

            document.getElementById("form-id").value = s.id;
            document.getElementById("form-nama").value = s.nama;
            document.getElementById("form-alamat").value = s.alamat;
        });
}

// DELETE DATA
function deleteData(id) {
    if (!confirm("Yakin ingin menghapus?")) return;

    fetch(`${API}/${id}`, { method: "DELETE" })
        .then(() => loadData());
}

// OPEN UPLOAD MODAL
function openUpload(id, foto) {
    document.getElementById("foto-id").value = id;

    const preview = document.getElementById("preview-img");
    if (foto) {
        preview.src = `/pictures/${foto}`;
        preview.classList.remove("d-none");
    } else {
        preview.classList.add("d-none");
    }

    const modal = new bootstrap.Modal(document.getElementById("uploadModal"));
    modal.show();
}

// UPLOAD FOTO
function uploadFoto() {
    const id = document.getElementById("foto-id").value;
    const fileInput = document.getElementById("foto-file");

    if (fileInput.files.length === 0) {
        alert("Pilih file terlebih dahulu");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch(`${API}/${id}/foto`, {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(() => {
        loadData();
        document.getElementById("foto-file").value = "";
        const modal = bootstrap.Modal.getInstance(document.getElementById("uploadModal"));
        modal.hide();
    });
}

// SUBMIT FORM
document.getElementById("siswa-form").addEventListener("submit", function(e) {
    e.preventDefault();

    const id = document.getElementById("form-id").value;
    const data = {
        nama: document.getElementById("form-nama").value,
        alamat: document.getElementById("form-alamat").value
    };

    const method = id ? "PUT" : "POST";
    const url = id ? `${API}/${id}` : API;

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    }).then(() => {
        hideForm();
        loadData();
    });
});

// INITIAL LOAD
loadData();
</script>

</body>
</html>
```
### 11. API upload foto siswa (Validasi, Resize, Replace)

Install Pillow `pip install Pillow` >> ambahkan ke requirements.txt:

```Code
Pillow
```

Update API Upload Foto (resources/siswa_resource.py)

```python
import os
from PIL import Image
from werkzeug.utils import secure_filename
from flask import request
from flask_restx import Namespace, Resource

from services.siswa_service import (
    get_siswa_by_id,
    update_foto
)

UPLOAD_FOLDER = "pictures"
ALLOWED_EXT = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def resize_image(path):
    img = Image.open(path)
    img.thumbnail((400, 400))  # Resize max width/height 400px
    img.save(path, optimize=True, quality=85)


@siswa_ns.route("/<int:id>/foto")
class UploadFoto(Resource):
    def post(self, id):
        """Upload foto siswa dengan validasi + resize + hapus lama"""

        siswa = get_siswa_by_id(id)
        if not siswa:
            return {"message": "Siswa tidak ditemukan"}, 404

        if "file" not in request.files:
            return {"message": "File tidak ditemukan"}, 400

        file = request.files["file"]

        if file.filename == "":
            return {"message": "Nama file kosong"}, 400

        if not allowed_file(file.filename):
            return {"message": "Format file tidak diizinkan"}, 400

        # VALIDASI UKURAN FILE
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)

        if file_length > MAX_FILE_SIZE:
            return {"message": "Ukuran file maksimal 2MB"}, 400

        # Nama file aman
        filename = secure_filename(f"siswa_{id}_" + file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # HAPUS FOTO LAMA
        if siswa.get("foto"):
            old_path = os.path.join(UPLOAD_FOLDER, siswa["foto"])
            if os.path.exists(old_path):
                os.remove(old_path)

        # Simpan file
        file.save(filepath)

        # RESIZE FOTO
        resize_image(filepath)

        # Simpan nama file ke DB
        update_foto(id, filename)

        return {"message": "Foto berhasil diupload", "filename": filename}, 201
```

### 12. Logging

Buat folder log >> Di root project:

```Code
mkdir logs
```

Buat file logger.py (global logger) >> Buat file baru:

```Code
project/logger.py
```
Isi:

```python
import logging
import os

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "api.log")

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


Tambahkan middleware logging di app.py
python
from flask import Flask, request
from flask_restx import Api
from resources.siswa_resource import siswa_ns
from logger import logger

app = Flask(__name__)
api = Api(app)

api.add_namespace(siswa_ns)

# -------------------------
# LOGGING REQUEST
# -------------------------
@app.before_request
def log_request():
    logger.info(
        f"REQUEST: {request.method} {request.path} | "
        f"IP={request.remote_addr} | "
        f"ARGS={dict(request.args)} | "
        f"BODY={request.get_json(silent=True)}"
    )

# -------------------------
# LOGGING RESPONSE
# -------------------------
@app.after_request
def log_response(response):
    logger.info(
        f"RESPONSE: {request.method} {request.path} | "
        f"STATUS={response.status_code}"
    )
    return response

# -------------------------
# LOGGING ERROR
# -------------------------
@app.errorhandler(Exception)
def handle_error(e):
    logger.error(f"ERROR: {str(e)}", exc_info=True)
    return {"message": "Internal Server Error"}, 500

@app.route("/")
def index():
    return render_template("crud.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


Tambahkan logging pada service CRUD (services/siswa_service.py)
Tambahkan:

python
from logger import logger
Lalu tambahkan log di setiap fungsi:

python
def get_all_siswa():
    logger.info("SERVICE: get_all_siswa()")
    ...
Contoh lengkap:

python
def create_siswa(data):
    logger.info(f"SERVICE: create_siswa() | DATA={data}")
    db = get_db()
    db.execute(
        "INSERT INTO tbsiswa (nama, alamat) VALUES (?, ?)",
        (data["nama"], data["alamat"])
    )
    db.commit()

```
Lakukan hal yang sama untuk:

get_siswa_by_id

update_siswa

delete_siswa

update_foto

Logging upload foto (resources/siswa_resource.py) >> Tambahkan:

```python
from logger import logger
```

Lalu log aktivitas upload:

```python
logger.info(f"UPLOAD FOTO: siswa_id={id} | filename={filename}")
```

Dan saat menghapus foto lama:

```python
logger.info(f"HAPUS FOTO LAMA: {old_path}")
```

📄 Contoh log yang dihasilkan (logs/api.log)
```Code
2026-01-01 11:05:12,123 - INFO - REQUEST: POST /siswa | IP=192.168.1.10 | ARGS={} | BODY={'nama': 'Budi', 'alamat': 'Semarang'}
2026-01-01 11:05:12,124 - INFO - SERVICE: create_siswa() | DATA={'nama': 'Budi', 'alamat': 'Semarang'}
2026-01-01 11:05:12,130 - INFO - RESPONSE: POST /siswa | STATUS=201
```


Update logger.py → Rotating Log Mingguan

Ganti isi logger.py menjadi:

```python
import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "api.log")

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

# -----------------------------
# ROTATING LOG MINGGUAN
# -----------------------------
handler = TimedRotatingFileHandler(
    LOG_FILE,
    when="W0",          # Rotasi setiap minggu (Senin)
    interval=1,         # Setiap 1 minggu
    backupCount=8,      # Simpan 8 file log (8 minggu)
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

handler.setFormatter(formatter)
logger.addHandler(handler)
```

🧠 Penjelasan Parameter Penting when="W0" >> Rotasi setiap minggu

W0 = Senin

Bisa diganti:

W1 = Selasa

W6 = Minggu

backupCount=8 >> Menyimpan log 8 minggu terakhir

Setelah itu file paling lama otomatis dihapus

Tidak Perlu Mengubah app.py atau service lain >>Karena logger tetap bernama:

```python
logger = logging.getLogger("api_logger")
```



### 13. Pytest


Tambahkan folder:

```Code
project/
│
├── tests/
│   └── test_siswa_api.py
```

🧪 2. Buat file tests/test_siswa_api.py

```python
import os
import io
import pytest
from app import app
from database import get_db

# -----------------------------
# FIXTURE: CLIENT
# -----------------------------
@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    # Reset database sebelum test
    with get_db() as db:
        db.execute("DELETE FROM tbsiswa")
        db.commit()

    return client


# -----------------------------
# TEST: CREATE SISWA
# -----------------------------
def test_create_siswa(client):
    response = client.post("/siswa/", json={
        "nama": "Budi",
        "alamat": "Semarang"
    })
    assert response.status_code == 201


# -----------------------------
# TEST: READ ALL
# -----------------------------
def test_read_all(client):
    # Insert 1 data dulu
    client.post("/siswa/", json={"nama": "Budi", "alamat": "Semarang"})

    response = client.get("/siswa/")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


# -----------------------------
# TEST: READ ONE
# -----------------------------
def test_read_one(client):
    # Insert data
    client.post("/siswa/", json={"nama": "Budi", "alamat": "Semarang"})

    response = client.get("/siswa/1")
    assert response.status_code == 200
    assert response.get_json()["nama"] == "Budi"


# -----------------------------
# TEST: UPDATE SISWA
# -----------------------------
def test_update_siswa(client):
    client.post("/siswa/", json={"nama": "Budi", "alamat": "Semarang"})

    response = client.put("/siswa/1", json={
        "nama": "Budi Update",
        "alamat": "Jakarta"
    })

    assert response.status_code == 200

    # Cek hasil update
    get_res = client.get("/siswa/1")
    assert get_res.get_json()["nama"] == "Budi Update"


# -----------------------------
# TEST: DELETE SISWA
# -----------------------------
def test_delete_siswa(client):
    client.post("/siswa/", json={"nama": "Budi", "alamat": "Semarang"})

    response = client.delete("/siswa/1")
    assert response.status_code == 200

    # Pastikan sudah terhapus
    get_res = client.get("/siswa/1")
    assert get_res.status_code == 404


# -----------------------------
# TEST: UPLOAD FOTO
# -----------------------------
def test_upload_foto(client):
    # Insert data
    client.post("/siswa/", json={"nama": "Budi", "alamat": "Semarang"})

    # Buat file dummy
    dummy_file = (io.BytesIO(b"fake image data"), "foto.jpg")

    response = client.post(
        "/siswa/1/foto",
        content_type="multipart/form-data",
        data={"file": dummy_file}
    )

    assert response.status_code == 201
    assert "filename" in response.get_json()

    # Cek file tersimpan
    filename = response.get_json()["filename"]
    assert os.path.exists(os.path.join("pictures", filename))
```
Cara Menjalankan Test
Pastikan pytest terinstall:

```Code
pip install pytest
```

Lalu jalankan:

```Code
pytest -v
```