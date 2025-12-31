#/app.py
# python app.py
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
