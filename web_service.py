from flask import Flask, render_template_string, request, redirect
import requests

# Flask uygulamasını başlat
app = Flask(__name__)

# Arka uç API'sinin URL'si
# Lütfen bu URL'nin doğru çalıştığından emin olun.
API_URL = "https://hello-cloud3.onrender.com"

# Ön yüz HTML içeriği
HTML = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mikro Hizmetli Selam!</title>
<style>
body { 
    font-family: Arial, sans-serif; 
    text-align: center; 
    padding: 50px; 
    background: #eef2f3; 
    margin: 0;
}
h1 { 
    color: #333; 
    margin-bottom: 20px;
}
p {
    margin-bottom: 25px;
    color: #555;
}
form {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 40px;
}
input[type="text"] { 
    padding: 12px; 
    font-size: 16px; 
    border: 1px solid #ccc;
    border-radius: 6px; 
    width: 250px;
    max-width: 70%;
}
button { 
    padding: 12px 20px; 
    background: #007bff; /* Mavi tonu */
    color: white; 
    border: none; 
    border-radius: 6px; 
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s ease;
}
button:hover {
    background: #0056b3;
}
h3 {
    color: #4CAF50; /* Yeşil tonu */
    margin-bottom: 15px;
}
ul {
    list-style: none;
    padding: 0;
}
li { 
    background: white; 
    margin: 8px auto; 
    width: 90%;
    max-width: 300px; 
    padding: 10px; 
    border-radius: 6px; 
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
li:hover {
    transform: translateY(-2px);
}
</style>
</head>
<body>
    <h1>Mikro Hizmetli Selam!</h1>
    <p>Adınızı yazarak ziyaretçi listesine ekleyin.</p>
    
    <form method="POST">
        <input type="text" name="isim" placeholder="Adınızı yazın" required>
        <button type="submit">Gönder</button>
    </form>
    
    <h3>Son Ziyaretçiler:</h3>
    <ul>
        {% for ad in isimler %}
        <li>{{ ad }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    """Ana sayfa rotası: Ziyaretçi ekler ve listeler."""
    if request.method == "POST":
        # Yeni ziyaretçiyi arka uç API'sine POST et
        isim = request.form.get("isim")
        try:
            requests.post(API_URL + "/ziyaretciler", json={"isim": isim}, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"Hata: Ziyaretçi eklenemedi: {e}")
            # Hata durumunda bile kullanıcıyı ana sayfaya yönlendir
        
        return redirect("/")

    # Ziyaretçi listesini arka uç API'sinden GET et
    isimler = []
    try:
        resp = requests.get(API_URL + "/ziyaretciler", timeout=5)
        if resp.status_code == 200:
            isimler = resp.json()
        else:
            print(f"Hata: API'den ziyaretçi listesi alınamadı. Durum kodu: {resp.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Hata: API bağlantı hatası: {e}")

    # HTML şablonunu ziyaretçi listesiyle birlikte render et
    return render_template_string(HTML, isimler=isimler)


if __name__ == "__main__":
    # Uygulamayı 0.0.0.0 adresi ve 5000 portu üzerinden çalıştır
    app.run(host="0.0.0.0", port=5000)
