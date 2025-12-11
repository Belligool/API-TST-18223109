![F1 API CI](https://github.com/Belligool/API-TST-18223109/actions/workflows/ci.yml/badge.svg)

# API-TST-18223109

Proyek ini adalah implementasi **Domain-Driven Design (DDD)** untuk Sistem Manajemen Tim Formula 1. Sistem ini mencakup Backend berbasis **FastAPI**, Frontend menggunakan **Streamlit**, serta penerapan standar **Test Driven Development (TDD)** dengan coverage tinggi dan integrasi **CI/CD** menggunakan GitHub Actions.

Dibuat untuk memenuhi Tugas Besar **II3160 Teknologi Sistem Terintegrasi**

## Daftar Isi
- [Fitur Utama](#-fitur-utama)
- [Arsitektur & Struktur Proyek](#-arsitektur--struktur-proyek)
- [Tech Stack](#-tech-stack)
- [Instalasi & Konfigurasi](#-instalasi--konfigurasi)
- [Cara Menjalankan Aplikasi](#-cara-menjalankan-aplikasi)
- [Pengujian (Unit Testing & TDD)](#-pengujian-unit-testing--tdd)
- [CI/CD Workflow](#-cicd-workflow)
- [How I'm Feeling](#-How-I'm-Feeling)

---

# Fitur Utama
### 1. Core Domain (Inti Bisnis)
- **Race Strategy Management:** Merencanakan strategi pit stop, pemilihan ban, dan bahan bakar.
- **Driver Performance Analysis:** Memantau telemetri (speed, RPM) dan waktu putaran (lap time) pembalap.
- **Automated Report System:** (Fitur Baru) Menghasilkan laporan balapan otomatis berisi ringkasan, analisis performa tim, dan insiden kunci.

### 2. Supporting Domain (Pendukung)
- **Team Management:** CRUD lengkap untuk entitas Tim, termasuk manajemen Driver, Sponsor, Inventory, dan Engineers.
- **Engineer Management:** (Fitur Baru) Penjadwalan tugas spesifik untuk mekanik dan teknisi di garasi/pit lane.

### 3. Generic Domain (Umum)
- **Authentication & Authorization:** Sistem login aman menggunakan JWT (JSON Web Token).
- **Frontend Dashboard:** Antarmuka visual untuk mengelola seluruh data tanpa coding.

---

# Arsitektur & Struktur Proyek

```text
API-TST-18223109/
├── .github/workflows/      # Konfigurasi CI/CD (GitHub Actions)
├── tests/                  # Unit Tests (TDD)
├──── conftest.py
├──── test_main.py
├──── __init__.py
├── main.py                 # Entry point Backend (FastAPI)
├── app.py                  # Entry point Frontend (Streamlit)
├── models.py               # Definisi Pydantic Models (Entities/Value Objects)
├── dependencies.py         # Database In-Memory & Auth Dependencies
├── auth.py                 # Utilitas Keamanan (Hash Password & JWT)
├── teams_controller.py     # Logic Manajemen Tim
├── report_system.py        # Logic Generator Laporan
├── engineer_management.py  # Logic Penjadwalan Teknisi
├── requirements.txt        # Daftar Library Python
└── .env                    # Environment Variables (Rahasia)
```
---

# Tech Stack
- **Language**: Python 3.10+
- **Backend Framework**: FastAPI
- **Frontend Framework**: Streamlit
- **Server**: Uvicorn
- **Security**: OAuth2 dengan JWT (python-jose, passlib)
- **Testing**: Pytest, Pytest-Cov (Coverage >95%)
- **CI/CD**: GitHub Actions, Flake8 (Linting)

---

# Instalasi & Konfigurasi

Ikuti langkah ini untuk menjalankan proyek di komputer lokal
### 1. Clone Repository
```
git clone [https://github.com/Belligool/API-TST-18223109.git](https://github.com/Belligool/API-TST-18223109.git)
cd API-TST-18223109
```

### 2. Setup Virtual Environment
```
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```
atau
```
pip install fastapi "uvicorn[standard]" python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv streamlit pandas requests pytest pytest-cov httpx flake8
```

### 4. Konfigurasi Environment (.env)
```
SECRET_KEY=masukkan_secret_key_yang_panjang_dan_rahasia_disini
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Akun Admin Default (Bebas. Dibawah ini hanyalah contoh)
ADMIN_USERNAME=jbenham
ADMIN_PASSWORD=opmeersucks
ADMIN_EMAIL=jakebenham@f1system.com
ADMIN_FULL_NAME="Jake Benham"
```
---

# Cara Menjalankan Aplikasi
Jalankan dua terminal secara bersamaan (satu untuk Backend, satu untuk Frontend).

### Terminal 1: Backend
```
uvicorn main:app --reload
```

### Terminal 2: Frontend
```
streamlit run app.py
```
Dashboard akan otomatis terbuka di browser (http://localhost:8501).

**Login Default:**   
**Username: jbenham**   
**Password: opmeersucks**

---

# Pengujian (Unit Testing & TDD)
Pengujian dapat digunakan menggunakan Pytest dengan target Code Coverage > 95% untuk seluruh logic backend. **Cara menjalankannya adalah:**

**Gantilah ke root folder dan type kode berikut ke terminal:**
```
pytest --cov=. --cov-report=term-missing
```

---

# CI/CD Workflow
Repositori ini terintegrasi dengan GitHub Actions untuk Continuous Integration. Setiap kali ada push atau pull request ke branch main, pipeline otomatis akan berjalan.   

**Tahapan Pipeline (.github/workflows/ci.yml):**   
1. Checkout Code: Mengambil kode terbaru.
2. Setup Python: Menyiapkan environment Python.
3. Install Dependencies: Menginstall library yang dibutuhkan.
4. Linting (Flake8): Mengecek kualitas kode dan error sintaks.
5. Testing (Pytest): Menjalankan seluruh unit test dan memastikan coverage terpenuhi.   

Badge di bagian atas README akan berwarna Hijau (Passing) ketika pipeline sukses.

---


# How I'm Feeling  
![leclerc](https://i.ibb.co.com/20nJHSPP/tgwgw.png)  

***"This is so incredibly frustrating, We've lost all competitiveness. You just have to listen to me, I would have found a different way of managing those issues. Now it's just undriveble. Undriveable. It's a miracle if we finish on the podium."***  
-- Charles Leclerc, Hungary 2025.
  

  
© All trademarks, logos, and team or driver information belong to their respective owners. This API is a fan-made, educational project and isn’t affiliated with Formula 1, the FIA, or any teams.