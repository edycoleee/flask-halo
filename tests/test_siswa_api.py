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

    # Hanya kosongkan tabel, tidak reset autoincrement
    with get_db() as db:
        db.execute("DELETE FROM tbsiswa")
        db.commit()

    return client


# -----------------------------
# HELPER: INSERT SISWA & RETURN ID
# -----------------------------
def create_siswa(client, nama="Budi", alamat="Semarang"):
    res = client.post("/api/siswa/", json={"nama": nama, "alamat": alamat})
    assert res.status_code == 201
    return res.get_json()["id"]


# -----------------------------
# TEST: CREATE SISWA
# -----------------------------
def test_create_siswa(client):
    sid = create_siswa(client)
    assert isinstance(sid, int)


# -----------------------------
# TEST: READ ALL
# -----------------------------
def test_read_all(client):
    create_siswa(client)

    response = client.get("/api/siswa/")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


# -----------------------------
# TEST: READ ONE
# -----------------------------
def test_read_one(client):
    sid = create_siswa(client)

    response = client.get(f"/api/siswa/{sid}")
    assert response.status_code == 200
    assert response.get_json()["nama"] == "Budi"


# -----------------------------
# TEST: UPDATE SISWA
# -----------------------------
def test_update_siswa(client):
    sid = create_siswa(client)

    response = client.put(f"/api/siswa/{sid}", json={
        "nama": "Budi Update",
        "alamat": "Jakarta"
    })
    assert response.status_code == 200

    get_res = client.get(f"/api/siswa/{sid}")
    assert get_res.get_json()["nama"] == "Budi Update"


# -----------------------------
# TEST: DELETE SISWA
# -----------------------------
def test_delete_siswa(client):
    sid = create_siswa(client)

    response = client.delete(f"/api/siswa/{sid}")
    assert response.status_code == 200

    get_res = client.get(f"/api/siswa/{sid}")
    assert get_res.status_code == 404


# -----------------------------
# TEST: UPLOAD FOTO
# -----------------------------
def test_upload_foto(client):
    sid = create_siswa(client)

    dummy_file = (io.BytesIO(b"fake image data"), "foto.jpg")

    response = client.post(
        f"/api/siswa/{sid}/foto",
        content_type="multipart/form-data",
        data={"file": dummy_file}
    )

    assert response.status_code == 201
    filename = response.get_json()["filename"]
    assert os.path.exists(os.path.join("pictures", filename))
