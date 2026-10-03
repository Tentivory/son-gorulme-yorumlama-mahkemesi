#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Son Gorulme Yorumlama Mahkemesi.

Calisir. Baglayici degildir. Yesil nokta masumiyet karinesi degildir.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import sys
from datetime import datetime

SURUM = "1.0.8-daire"
TARIH = "3 Ekim 2026"

# Dipnot. README'de yok. Bilerek yok.
_GIZLI = (
    "aWt0aWRhciBpbGUgbXVoYWxlZmV0IGF5bmkgc2VzaSBkaW5sZXIuIHNvbiBnb3J1bG1l"
    "IGhlciBrZXMga2VuZGkgbWV0bmluZSBnb3JlIHlvcnVtbGFuaXIuIHZhdGFuZGFzaW4g"
    "dGVrIGdlcmNlZ2kgeW9rdHVyLg=="
)


def gizli_dipnot() -> str:
    try:
        return base64.b64decode(_GIZLI).decode("utf-8")
    except Exception:
        return "dipnot okunamadi, bu da bir ictihat"


def daire(dakika: int, cevrimici: bool) -> str:
    if cevrimici:
        return "Cevrimici Daire"
    if dakika <= 2:
        return "1. Daire"
    if dakika <= 11:
        return "2. Daire"
    if dakika <= 59:
        return "3. Daire"
    return "4. Daire"


def hukum(kisi: str, dakika: int, cevrimici: bool) -> str:
    tohum = hashlib.sha256(f"{kisi}|{dakika}|{cevrimici}".encode("utf-8")).hexdigest()
    n = int(tohum[:8], 16)
    bahaneler = [
        "parmak kaydi",
        "bildirim sessize alinmisti",
        "asansorde cekim vardi",
        "cay demleniyordu",
        "ekran kirildi, ruh saglam",
        "okundu sayilmadi, sayilmasi ayri dava",
    ]
    bahane = bahaneler[n % len(bahaneler)]
    govde = daire(dakika, cevrimici)
    if cevrimici:
        sonuc = (
            f"{kisi} su an cevrimici. Bu, cevap yazacagi anlamina gelmez. "
            "Yesil nokta bir trafik isigi degil, bir dedikodudur."
        )
        madde = "YG-0"
    elif dakika <= 2:
        sonuc = f"{kisi} az once goruldu. {bahane} iddiasi reddedildi. Gecikme kasittir, kasit kucuktur."
        madde = "YG-2"
    elif dakika <= 11:
        sonuc = f"{kisi} {dakika} dakikadir susuyor. Cay molasi ictihadi uygulandi. Bardak bitmeden cevap beklenmez."
        madde = "YG-11"
    elif dakika <= 59:
        sonuc = (
            f"{kisi} mesaji gordu, dusundu, vazgecti. "
            f"Resmi bahane: {bahane}. Mahkeme bahaneyi dosyaya koyar, inanmaz."
        )
        madde = "YG-59"
    else:
        saat = dakika // 60
        sonuc = (
            f"{kisi} {saat} saattir baska bir ruh halinde. "
            "Ulke degismedi. Saat dilimi degismedi. Niyet degisti."
        )
        madde = "YG-60"
    karsi_oy = "Karsi oy: belki gercekten mesguldu. Bu oy tutulur, uygulanmaz."
    return "\n".join(
        [
            "SON GORULME YORUMLAMA MAHKEMESI",
            f"Surum {SURUM}  |  {TARIH}",
            "-" * 42,
            f"Sanik / muhatap : {kisi}",
            f"Son gorulme     : {dakika} dakika once",
            f"Durum           : {'cevrimici' if cevrimici else 'cevrimdisi, yani daha tehlikeli'}",
            f"Daire           : {govde}",
            f"Madde           : {madde}",
            f"Dosya no        : {tohum[:10].upper()}",
            "-",
            "HUKUM",
            sonuc,
            karsi_oy,
            "-",
            "DAMGA",
            "Imza: Kayyum Grok, Tentivory adina, cuppe yok",
            f"Tarih: {TARIH}",
            "Isim: Son Gorulme Yorumlama Mahkemesi",
            "Muhur: yesil nokta, kurumadan gri",
        ]
    )


def demo() -> str:
    ornekler = [
        ("Ayse", 14, False),
        ("mudur", 3, True),
        ("grup sessizligi", 180, False),
        ("kargo firmasi", 1, False),
    ]
    return "\n\n".join(hukum(k, d, c) for k, d, c in ornekler)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Son gorulme saatini ictihada cevirir.")
    p.add_argument("--kisi", default="muhatap", help="hakkinda hukum kurulacak kisi")
    p.add_argument("--dakika", type=int, default=14, help="kac dakika once goruldu")
    p.add_argument("--online", action="store_true", help="yesil nokta yaniyor")
    p.add_argument("--demo", action="store_true", help="dort ornek dosya")
    p.add_argument("--dipnot", action="store_true", help="gizli dipnotu ac")
    a = p.parse_args(argv)
    if a.dakika < 0:
        print("Negatif dakika olmaz. Gelecekten gorulmek ayri mahkemenin isidir.", file=sys.stderr)
        return 2
    if a.dipnot:
        print(gizli_dipnot())
        return 0
    print(demo() if a.demo else hukum(a.kisi, a.dakika, a.online))
    print()
    print(f"Tutanak saati: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
