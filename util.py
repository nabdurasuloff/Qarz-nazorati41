# -*- coding: utf-8 -*-
"""
main.py va importer.py ikkalasida ham kerak bo'ladigan umumiy funksiyalar.
"""
import database as db


def turi_kodidan(mijoz_turi_kodi, mijoz_turi):
    """
    Jismoniy/yuridik ekanini aniqlaydi. Asosiy manba — portfeldagi
    "Мижоз тури" ustuni ('LE' / 'Individual'), bu eng ishonchli maydon.

    Diqqat: "Жис/юр/Ятт коди" raqamli kodi ("mijoz_turi_kodi") mustaqil
    ishonchli belgi EMAS — tekshiruv shuni ko'rsatdiki, kod=8 (asosiy
    jismoniy) va kod=11 (YaTT) Individual'ga, kod=9 esa aslida YURIDIK
    (LE) ga to'g'ri keladi (2, 3, 7, 10, 12 kodlari ham barchasi LE).
    Shu sabab bu yerda faqat 'LE' matn qiymati tekshiriladi.
    """
    turi = str(mijoz_turi or '').strip().upper()
    if turi == 'LE':
        return 'yuridik'
    return 'jismoniy'


def kalit_candidates(portfel_row):
    """Mijozni bog'lash uchun ishlatilishi mumkin bo'lgan ID'lar ro'yxati."""
    return [portfel_row.get('stir'), portfel_row.get('pinfl'), portfel_row.get('unikal')]


def resolve_mijoz(portfel_row):
    """Portfel qatoriga mos mijozni (agar bazada bo'lsa) topadi."""
    turi = turi_kodidan(portfel_row.get('mijoz_turi_kodi'), portfel_row.get('mijoz_turi'))
    for kalit in kalit_candidates(portfel_row):
        if not kalit:
            continue
        kalit = str(kalit).strip()
        m = db.find_mijoz(turi, kalit)
        if m:
            return turi, m
    return turi, None
