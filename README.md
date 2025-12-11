![F1 API CI](https://github.com/Belligool/API-TST-18223109/actions/workflows/ci.yml/badge.svg)](https://github.com/Belligool/API-TST-18223109/actions/workflows/ci.yml))

# API-TST-18223109

API dibuat untuk tugas besar II3160	Teknologi Sistem Terintegrasi. 

Untuk simpliity, langkah-langkah ini akan diterapkan untuk OS Windows.

# 1.	Setup Environment dan Dependencies  
Langkah ini dilakukan dengan menjalankan kode dibawah ini di terminal
```
python -m venv venv  
venv\Scripts\activate  
pip install fastapi "uvicorn[standard]" python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv
```


# 2.	Konfigurasi Environment Variable  
Buatlah file .env di folder yang sama dengan isi  
```
SECRET_KEY= # apa aja yg penting panjang  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30  
ADMIN_USERNAME=jbenham # contoh  
ADMIN_PASSWORD=opmeersucks # contoh  
ADMIN_EMAIL=jakebenham@f1system.com # contoh  
```

# 3.	Menjalankan Server  
Jalankan server dengan cara menjalankan di terminal  

```
uvicorn main:app --reload
```

# 4.	Charles Leclerc Image  
yea why not  
![leclerc](https://media.discordapp.net/attachments/1035492827972501514/1444910544367784036/tgwgw.png?ex=692e6d4e&is=692d1bce&hm=8606c2ee54e82334442b5df66530ae2d597f1278bef2210f0f452ffd1e44e69c&=&format=webp&quality=lossless&width=298&height=930)  

***"This is so incredibly frustrating, We've lost all competitiveness. You just have to listen to me, I would have found a different way of managing those issues. Now it's just undriveble. Undriveable. It's a miracle if we finish on the podium."***  
-- Charles Leclerc, Hungary 2025.
  

  
© All trademarks, logos, and team or driver information belong to their respective owners. This API is a fan-made, educational project and isn’t affiliated with Formula 1, the FIA, or any teams.