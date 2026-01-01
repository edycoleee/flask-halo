## FLASK


```py
# Update sistem
sudo apt update && sudo apt upgrade -y

# Install python3-venv jika belum ada
sudo apt install python3-venv -y

# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate # Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

pip install flask


#=========================================
#app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/halo", methods=["GET"])
def halo():
    return jsonify({"Halo Flask": True})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)


# python app.py
# curl http://127.0.0.1:5000/halo

```

Tambah Swagger (OpenAPI) dengan Flasgger

```py
pip install flasgger


from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)  # Swagger UI default di /apidocs

@app.route("/halo", methods=["GET"])
def halo():
    """
    Halo endpoint
    ---
    get:
      description: Mengembalikan pesan Halo Flask
      responses:
        200:
          description: Berhasil
          content:
            application/json:
              schema:
                type: object
                properties:
                  Halo Flask:
                    type: boolean
                    example: true
    """
    return jsonify({"Halo Flask": True})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)


```
