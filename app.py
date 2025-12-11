import streamlit as st
import requests
import pandas as pd
from datetime import datetime, time

st.set_page_config(page_title="F1 Team Management", layout="wide", page_icon="🏎️")

API_URL = "http://127.0.0.1:8000"

def login(username, password):
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.ConnectionError:
        st.error("Gagal terhubung ke server API. Pastikan backend berjalan!")
        return None

def authenticated_request(method, endpoint, data=None, params=None):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    url = f"{API_URL}{endpoint}"

    if method=="GET":
        response = requests.get(url, headers=headers, params=params)
    elif method=="POST":
        response = requests.post(url, headers=headers, json=data)
    elif method=="PUT":
        response = requests.put(url, headers=headers, json=data)
    
    return response

if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

def show_login_page():
    st.title("🏎️ F1 Management System Login 🏎️")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            token_data = login(username, password)
            if token_data:
                st.session_state['token'] = token_data['access_token']
                st.session_state['username'] = username
                st.success("Login Berhasil!")
                st.rerun()
            else:
                st.error("Username atau Password salah")

def show_dashboard():
    st.title(f"Selamat Datang, {st.session_state['username']}! 👋")
    st.info("Gunakan sidebar di sebelah kiri untuk navigasi antar fitur.")
    
    st.subheader("Status Sistem")
    col1, col2, col3 = st.columns(3)
    col1.metric("API Status", "Online", "200 OK")
    col2.metric("Role", "API Manager", "Verified")
    col3.metric("Season", "2025", "Current")

def show_team_management():
    st.header("🛡️ Manajemen Tim 🛡️")

    if 'draft_team' not in st.session_state:
        st.session_state['draft_team'] = {
            'members': [],
            'inventory': [],
            'sponsors': [],
            'engineers': [],
            'drivers': []
        }
    
    tab1, tab2 = st.tabs(["Buat Tim Baru", "Lihat Data Tim"])
    
    with tab1:
        st.subheader("Informasi Utama Tim")
        # Input Utama
        t_id = st.number_input("Team ID", min_value=1, step=1)
        t_name = st.text_input("Nama Tim")

        st.divider()

        with st.expander("+ Tambah Drivers"):
            c1, c2, c3 = st.columns(3)
            d_id = c1.number_input("Driver ID", min_value=1, key="d_id")
            d_name = c2.text_input("Nama Driver", key="d_name")
            d_abb = c3.text_input("Singkatan (3 Huruf)", max_chars=3, key="d_abb").upper()
            
            c4, c5 = st.columns(2)
            d_nat = c4.text_input("Kebangsaan", key="d_nat")
            d_cond = c5.selectbox("Kondisi Fisik", ["Fit", "Injured", "Recovering"], key="d_cond")
            
            if st.button("Tambah Driver ke List"):
                new_driver = {
                    "driverID": d_id,
                    "name": d_name,
                    "driverAbb": d_abb,
                    "nationality": d_nat,
                    "physicalCondition": d_cond
                }
                st.session_state['draft_team']['drivers'].append(new_driver)
                st.success(f"Driver {d_name} ditambahkan!")

            if st.session_state['draft_team']['drivers']:
                st.dataframe(pd.DataFrame(st.session_state['draft_team']['drivers']))
                if st.button("Hapus Semua Driver", key="del_drv"):
                    st.session_state['draft_team']['drivers'] = []
                    st.rerun()

        with st.expander("+ Tambah Engineers"):
            ec1, ec2, ec3 = st.columns(3)
            e_id = ec1.number_input("Engineer ID", min_value=1, key="e_id")
            e_name = ec2.text_input("Nama Engineer", key="e_name")
            e_role = ec3.text_input("Role (e.g., Race Engineer)", key="e_role")

            if st.button("Tambah Engineer ke List"):
                new_eng = {"engineerID": e_id, "name": e_name, "role": e_role}
                st.session_state['draft_team']['engineers'].append(new_eng)
                st.success(f"Engineer {e_name} ditambahkan!")
            
            if st.session_state['draft_team']['engineers']:
                st.dataframe(pd.DataFrame(st.session_state['draft_team']['engineers']))

        with st.expander("+ Tambah Inventory"):
            ic1, ic2 = st.columns(2)
            i_id = ic1.number_input("Item ID", min_value=1, key="i_id")
            i_name = ic2.text_input("Nama Part", key="i_name")
            
            ic3, ic4 = st.columns(2)
            i_qty = ic3.number_input("Quantity", min_value=0, key="i_qty")
            i_stat = ic4.selectbox("Status", ["Ready", "Damaged", "In Use"], key="i_stat")

            if st.button("Tambah Item ke List"):
                new_item = {
                    "itemID": i_id,
                    "partName": i_name,
                    "quantity": i_qty,
                    "status": i_stat
                }
                st.session_state['draft_team']['inventory'].append(new_item)
                st.success(f"Item {i_name} ditambahkan!")
            
            if st.session_state['draft_team']['inventory']:
                st.dataframe(pd.DataFrame(st.session_state['draft_team']['inventory']))

        with st.expander("+ Tambah Sponsors"):
            sc1, sc2, sc3 = st.columns(3)
            s_id = sc1.number_input("Sponsor ID", min_value=1, key="s_id")
            s_name = sc2.text_input("Nama Sponsor", key="s_name")
            s_val = sc3.number_input("Nilai Kontrak ($)", min_value=0.0, step=1000.0, key="s_val")

            if st.button("Tambah Sponsor ke List"):
                new_sponsor = {
                    "sponsorID": s_id,
                    "sponsorName": s_name,
                    "contractValue": s_val
                }
                st.session_state['draft_team']['sponsors'].append(new_sponsor)
                st.success(f"Sponsor {s_name} ditambahkan!")

            if st.session_state['draft_team']['sponsors']:
                st.dataframe(pd.DataFrame(st.session_state['draft_team']['sponsors']))

        with st.expander("+ Tambah Members (Staff Umum)"):
            m_name = st.text_input("Nama Staff", key="m_name")
            if st.button("Tambah Member"):
                if m_name:
                    st.session_state['draft_team']['members'].append(m_name)
                    st.success(f"Member {m_name} ditambahkan!")
            
            if st.session_state['draft_team']['members']:
                st.write(st.session_state['draft_team']['members'])

        st.divider()
        
        if st.button("SIMPAN DATA TIM KE DATABASE"):
            final_payload = {
                "teamID": t_id,
                "name": t_name,
                "members": st.session_state['draft_team']['members'],
                "inventory": st.session_state['draft_team']['inventory'],
                "sponsors": st.session_state['draft_team']['sponsors'],
                "engineers": st.session_state['draft_team']['engineers'],
                "drivers": st.session_state['draft_team']['drivers']
            }

            with st.spinner("Mengirim data ke API..."):
                res = authenticated_request("POST", "/teams/", data=final_payload)
                
                if res.status_code == 200:
                    st.success(f"Tim **{t_name}** beserta seluruh detailnya berhasil disimpan!")
                    # Reset Draft setelah sukses
                    st.session_state['draft_team'] = {
                        'members': [], 'inventory': [], 'sponsors': [], 
                        'engineers': [], 'drivers': []
                    }
                else:
                    st.error(f"Gagal menyimpan tim. Error: {res.text}")

    with tab2:
        search_id = st.number_input("Cari berdasarkan Team ID", min_value=1, step=1, key="search_team")
        if st.button("Cari Tim"):
            res = authenticated_request("GET", f"/teams/{search_id}")
            if res.status_code == 200:
                team_data = res.json()
                st.success(f"Tim Ditemukan: {team_data['name']}")
                st.json(team_data)
            else:
                st.warning("Tim tidak ditemukan.")

def show_engineer_management():
    st.header("🔧 Engineer Management 🔧")
    st.caption("Penjadwalan tugas untuk mekanik dan teknisi.")

    tab1, tab2 = st.tabs(["Buat Jadwal Baru", "Lihat Semua Jadwal"])

    with tab1:
        with st.form("schedule_form"):
            col1, col2 = st.columns(2)
            eng_id = col1.number_input("Engineer ID", min_value=1)
            race_id = col2.number_input("Race ID", min_value=1)
            
            task = st.text_input("Deskripsi Tugas")
            loc = st.text_input("Lokasi")
            
            d_col, t1_col, t2_col = st.columns(3)
            s_date = d_col.date_input("Tanggal")
            s_time = t1_col.time_input("Waktu Mulai")
            e_time = t2_col.time_input("Waktu Selesai")

            if st.form_submit_button("Konfirmasi Jadwal"):
                payload = {
                    "engineerID": eng_id,
                    "taskDescription": task,
                    "date": str(s_date),
                    "startTime": str(s_time),
                    "endTime": str(e_time),
                    "location": loc,
                    "raceID": race_id
                }
                res = authenticated_request("POST", "/engineer_management/schedules/", data=payload)
                if res.status_code == 201:
                    st.success("Jadwal Berhasil Dibuat!")
                else:
                    st.error(f"Error: {res.text}")

    with tab2:
        if st.button("Refresh Jadwal"):
            res = authenticated_request("GET", "/engineer_management/schedules/")
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                else:
                    st.info("Belum ada jadwal.")
            else:
                st.error("Gagal mengambil data.")
def show_report_system():
    st.header("📄 Report System 📄")
    st.caption("Generate laporan otomatis hasil balapan.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Generate Report")
        race_id_input = st.number_input("Masukkan Race ID", min_value=1)
        if st.button("Generate Laporan"):
            with st.spinner("Menganalisis data balapan..."):
                res = authenticated_request("POST", f"/report_system/generate/{race_id_input}")
                if res.status_code == 201:
                    st.success("Laporan berhasil dibuat!")
                    st.session_state['last_report'] = res.json()
                elif res.status_code == 404:
                    st.error("Data balapan (Race Strategy) tidak ditemukan. Buat Race Strategy dulu.")
                elif res.status_code == 400:
                    st.warning("Laporan untuk Race ID ini sudah ada.")
                else:
                    st.error(f"Error: {res.text}")

    with col2:
        st.subheader("View Report")
        report_id = st.number_input("Cari Report ID", min_value=1)
        if st.button("Lihat Laporan"):
             res = authenticated_request("GET", f"/report_system/{report_id}")
             if res.status_code == 200:
                 st.session_state['last_report'] = res.json()
             else:
                 st.error("Laporan tidak ditemukan.")
        
        if 'last_report' in st.session_state:
            report = st.session_state['last_report']
            st.divider()
            st.markdown(f"### Report #{report['reportID']} (Race #{report['raceID']})")
            st.info(report['raceSummary'])
            
            st.markdown("#### 🚨 Key Incidents 🚨")
            for incident in report['keyIncidents']:
                st.write(f"- {incident}")
            
            st.markdown("#### 📊 Team Performance Analysis 📊")
            for team, analysis in report['teamPerformanceAnalysis'].items():
                with st.expander(f"Analisis: {team}"):
                    st.write(analysis)


def show_race_strategy_simple():
    st.header("🏎️ Race Strategy (Simple) 🏎️")
    st.warning("Pastikan data ini dibuat SEBELUM generate report.")
    
    with st.form("simple_race_strat"):
        rid = st.number_input("Race ID", min_value=1)
        circuit = st.text_input("Circuit Name")
        res_str = st.text_area("Race Result (Format: P1: Name (Team))")
        
        if st.form_submit_button("Buat Data Dummy Balapan"):
            results = [x.strip() for x in res_str.split('\n') if x.strip()]
            
            payload = {
                "race": {
                    "raceID": rid,
                    "circuitName": circuit,
                    "date": str(datetime.now().date()),
                    "weather": "Sunny",
                    "result": results
                },
                "strategyPlan": {
                    "pitStopSchedule": [20],
                    "tyreStrategy": ["Soft", "Hard"],
                    "fuelPlan": "Push"
                },
                "liveTelemetry": {"speed": 0, "rpm": 0, "temperature": 0}
            }
            
            res = authenticated_request("POST", "/race_strategy/", data=payload)
            if res.status_code == 200:
                st.success("Data Race Strategy tersimpan! Sekarang Anda bisa generate report.")
            else:
                st.error(f"Gagal: {res.text}")


if st.session_state['token'] is None:
    show_login_page()
else:
    with st.sidebar:
        st.title("F1 API Manager")
        st.write(f"User: *{st.session_state['username']}*")
        menu = st.radio(
            "Menu", 
            ["Dashboard", "Teams", "Engineer Schedule", "Race Strategy (Input)", "Report System"]
        )
        
        st.divider()
        if st.button("Logout"):
            st.session_state['token'] = None
            st.session_state['username'] = None
            st.rerun()

    if menu == "Dashboard":
        show_dashboard()
    elif menu == "Teams":
        show_team_management()
    elif menu == "Engineer Schedule":
        show_engineer_management()
    elif menu == "Race Strategy (Input)":
        show_race_strategy_simple()
    elif menu == "Report System":
        show_report_system()