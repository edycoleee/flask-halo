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