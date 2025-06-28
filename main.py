from fastapi import FastAPI, Query
import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search

app = FastAPI()

def ambil_id_facebook(url):
    match = re.search(r'facebook\.com/profile\.php\?id=(\d+)', url)
    if match:
        return match.group(1)
    return None

def ambil_nama_dari_facebook(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else ""
        nama = title.split('|')[0].strip()
        return nama
    except:
        return "Nama tidak diketahui"

@app.get("/get_facebook_id")
def get_facebook_id(
    nama: str = Query(..., description="Nama target Facebook"),
    jumlah: int = Query(5, description="Jumlah hasil yang diambil"),
    jeda: int = Query(2, description="Jeda antar pencarian (detik)")
):
    hasil = []
    dork = f'site:facebook.com/profile.php?id= "{nama}"'
    try:
        for url in search(dork, num_results=jumlah, sleep_interval=jeda):
            profile_id = ambil_id_facebook(url)
            nama_fb = ambil_nama_dari_facebook(url)
            if profile_id:
                hasil.append({
                    "url": url,
                    "profile_id": profile_id,
                    "nama": nama_fb
                })
    except Exception as e:
        return {"error": str(e)}
    return {"results": hasil}
