import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. Nastavení ---
headers = {"User-Agent": "Mozilla/5.0"}
url_datart = "https://www.datart.cz/herni-konzole-sony-playstation-5-digital-typ-modelu-slim-ps711000049751-bila"
ted = datetime.now().strftime("%Y-%m-%d %H:%M")

# --- 2. Stáhni stránku ---
r = requests.get(url_datart, headers=headers)
print("Datart:", r.status_code)

# --- 3. Najdi cenu ---
soup = BeautifulSoup(r.text, "html.parser")
cena = soup.find("div", class_="actual")
text = cena.get_text()

cislice = ""
for znak in text:
    if znak.isdigit():
        cislice = cislice + znak

cislo = int(cislice)
print("Aktuální cena:", cislo)

# --- 4. Přečti minulou cenu ---
posledni_cena = None

with open("ceny.csv", encoding="utf-8") as soubor:
    radky = soubor.readlines()

if radky:
    posledni_radek = radky[-1]
    posledni_cena = int(posledni_radek.strip().split(",")[2])

print("Minulá cena:", posledni_cena)

# --- 5. Porovnej ---
if posledni_cena is None:
    print("První měření, není s čím porovnat.")
elif cislo < posledni_cena:
    print(f"Zlevnilo o {posledni_cena-cislo} Kč!")
elif cislo > posledni_cena:
    print(f"Zdražilo o {cislo-posledni_cena} Kč.")
else:
    print("Cena se nezměnila.")

# --- 6. Ulož novou cenu ---
with open("ceny.csv", "a", encoding="utf-8") as soubor:
    soubor.write(f"{ted},Datart,{cislo}\n")