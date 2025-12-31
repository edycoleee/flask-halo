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