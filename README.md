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
const API = "/siswa";

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
api = Api(app, doc="/docs")
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

API → http://localhost:5000/siswa

Swagger → http://localhost:5000/docs