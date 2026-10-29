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
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        nama,
        usia,
        gula,
        bmi,
        riwayat,
        hasil
    ))

    conn.commit()

    messagebox.showinfo(
        "Sukses",
        "Data pasien berhasil disimpan!"
    )

    entry_nama.delete(0, tk.END)
    entry_usia.delete(0, tk.END)
    entry_gula.delete(0, tk.END)
    entry_bmi.delete(0, tk.END)
    combo_riwayat.set("Tidak")


# =========================
# TAMPIL DATA
# =========================
def lihat_data():

    window = tk.Toplevel(root)
    window.title("Riwayat Pasien")
    window.geometry("900x400")

    cols = (
        "ID",
        "Nama",
        "Usia",
        "Gula Darah",
        "BMI",
        "Riwayat Ortu",
        "Prediksi"
    )

    tree = ttk.Treeview(
        window,
        columns=cols,
        show="headings"
    )

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True)

    cursor.execute("SELECT * FROM pasien")

    data = cursor.fetchall()

    for row in data:
        tree.insert("", tk.END, values=row)


# =========================
# GUI TKINTER
# =========================
root = tk.Tk()
root.title("Prediksi Risiko Diabetes")
root.geometry("500x450")
root.resizable(False, False)

judul = tk.Label(
    root,
    text="APLIKASI PREDIKSI RISIKO DIABETES",
    font=("Arial", 14, "bold")
)
judul.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

# Nama
tk.Label(
    frame,
    text="Nama Pasien"
).grid(row=0, column=0, sticky="w", pady=5)

entry_nama = tk.Entry(frame, width=30)
entry_nama.grid(row=0, column=1)

# Usia
tk.Label(
    frame,
    text="Usia"
).grid(row=1, column=0, sticky="w", pady=5)

entry_usia = tk.Entry(frame, width=30)
entry_usia.grid(row=1, column=1)

# Gula Darah
tk.Label(
    frame,
    text="Gula Darah (mg/dL)"
).grid(row=2, column=0, sticky="w", pady=5)

entry_gula = tk.Entry(frame, width=30)
entry_gula.grid(row=2, column=1)

# BMI
tk.Label(
    frame,
    text="BMI"
).grid(row=3, column=0, sticky="w", pady=5)

entry_bmi = tk.Entry(frame, width=30)
entry_bmi.grid(row=3, column=1)

# Riwayat
tk.Label(
    frame,
    text="Riwayat Diabetes Orang Tua"
).grid(row=4, column=0, sticky="w", pady=5)

combo_riwayat = ttk.Combobox(
    frame,
    values=["Ya", "Tidak"],
    state="readonly",
    width=27
)
