import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# =========================
# DATABASE SQLITE
# =========================
conn = sqlite3.connect("prediksi_diabetes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pasien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pasien TEXT NOT NULL,
    usia INTEGER NOT NULL,
    gula_darah REAL NOT NULL,
    bmi REAL NOT NULL,
    riwayat_ortu TEXT NOT NULL,
    hasil_prediksi TEXT NOT NULL
)
""")

conn.commit()

# =========================
# FUNGSI PREDIKSI
# =========================
def prediksi_diabetes(gula_darah, bmi, riwayat_ortu):

    if gula_darah >= 200:
        if bmi >= 30 or riwayat_ortu == "Ya":
            return "Sangat Tinggi", "red"
        else:
            return "Tinggi", "orange"

    elif 140 <= gula_darah <= 199:
        if bmi >= 30 and riwayat_ortu == "Ya":
            return "Tinggi", "orange"
        else:
            return "Sedang", "gold"

    else:
        if bmi >= 30:
            if riwayat_ortu == "Ya":
                return "Sedang", "gold"
            else:
                return "Waspada", "blue"

        elif bmi < 30 and riwayat_ortu == "Ya":
            return "Waspada", "blue"

        else:
            return "Rendah", "green"


# =========================
# VALIDASI DAN SIMPAN
# =========================
def simpan_data():

    nama = entry_nama.get().strip()
    usia = entry_usia.get().strip()
    gula = entry_gula.get().strip()
    bmi = entry_bmi.get().strip()
    riwayat = combo_riwayat.get()

    if nama == "":
        messagebox.showerror(
            "Validasi",
            "Nama pasien tidak boleh kosong!"
        )
        return

    try:
        usia = int(usia)
        gula = float(gula)
        bmi = float(bmi)
    except:
        messagebox.showerror(
            "Validasi",
            "Usia, gula darah, dan BMI harus berupa angka!"
        )
        return

    if usia <= 0:
        messagebox.showerror(
            "Validasi",
            "Usia harus lebih dari 0."
        )
        return

    if gula <= 0:
        messagebox.showerror(
            "Validasi",
            "Gula darah harus lebih dari 0."
        )
        return

    if bmi <= 0:
        messagebox.showerror(
            "Validasi",
            "BMI harus lebih dari 0."
        )
        return

    hasil, warna = prediksi_diabetes(
        gula,
        bmi,
        riwayat
    )

    lbl_hasil.config(
        text=f"Risiko Diabetes : {hasil}",
        fg=warna
    )

    cursor.execute("""
    INSERT INTO pasien
    (
        nama_pasien,
        usia,
        gula_darah,
        bmi,
        riwayat_ortu,
        hasil_prediksi
    )