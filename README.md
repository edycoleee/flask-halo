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

```
📁 Struktur proyek (sederhana tapi scalable)
Kode
belajar-restx/
│
├── app.py
├── extensions.py
├── resources/
│   └── halo.py
└── logs/
    └── api.log



2) 🧩 File extensions.py — setup logger
python
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    handler = RotatingFileHandler(
        "logs/api.log",
        maxBytes=200_000,   # kira-kira ratusan–ribuan baris
        backupCount=1
    )
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)



3) 📦 File resources/halo.py — namespace + endpoint
python
from flask_restx import Namespace, Resource, fields

ns = Namespace("halo", description="Halo operations")

halo_model = ns.model("HaloResponse", {
    "Halo Flask": fields.Boolean(example=True)
})

@ns.route("/")
class HaloResource(Resource):
    @ns.marshal_with(halo_model)
    def get(self):
        """Mengembalikan pesan Halo Flask"""
        return {"Halo Flask": True}


) 🏗️ File app.py — main app + swagger + logging middleware
python
from flask import Flask, request
from flask_restx import Api
from extensions import setup_logger
from resources.halo import ns as halo_ns

app = Flask(__name__)

# Swagger UI otomatis di / (root)
api = Api(
    app,
    version="1.0",
    title="Belajar Flask RESTX",
    description="API sederhana dengan RESTX + Logging",
)

# Register namespace
api.add_namespace(halo_ns, path="/halo")

# Setup logger
setup_logger(app)

# Middleware logging
@app.before_request
def log_request():
    app.logger.info(
        f"REQUEST {request.method} {request.path} "
        f"args={dict(request.args)} "
        f"json={request.get_json(silent=True)}"
    )

@app.after_request
def log_response(response):
    app.logger.info(
        f"RESPONSE {request.method} {request.path} "
        f"status={response.status_code} "
        f"content_type={response.content_type}"
    )
    return response

if __name__ == "__main__":
    app.run(debug=True)


```