## FLASK


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
pip install flask flask-restx sqlite3

```


2. Hierarki Flask‑RESTX 

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

```
# Flask Restx
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

```
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
    app.run(debug=True)

```