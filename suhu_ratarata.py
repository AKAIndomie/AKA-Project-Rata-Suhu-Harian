import random
import time
import sys
import csv
import argparse

sys.setrecursionlimit(20000)

# -------------------------
# DATA (Simulasi suhu)
# -------------------------
def generate_suhu(n, low=20.0, high=35.0, seed=123):
    """Menghasilkan list suhu harian acak (float) dengan 1 desimal (reproducible)."""
    rng = random.Random(seed)
    return [round(rng.uniform(low, high), 1) for _ in range(n)]

# =========================================================
# SKEMA ITERATIF
# =========================================================
def avg_iteratif(data):
    total = 0.0
    for x in data:
        total += x
    return total / len(data)

# =========================================================
# SKEMA REKURSIF
# =========================================================
def sum_rekursif(data, n):
    if n == 0:
        return 0.0
    return data[n - 1] + sum_rekursif(data, n - 1)

def avg_rekursif(data):
    return sum_rekursif(data, len(data)) / len(data)

# -------------------------
# UTIL: ukur waktu
# -------------------------
def ukur_waktu(func, *args, repeat=10):
    """Mengukur waktu rata-rata eksekusi fungsi (detik)."""
    times = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        func(*args)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return sum(times) / len(times)

def repeat_adaptif(n):
    if n <= 100:
        return 200
    elif n <= 1000:
        return 50
    return 10

# -------------------------
# BENCHMARK per mode
# -------------------------
def benchmark_iteratif(ukuran_list, seed=123):
    hasil = []
    for n in ukuran_list:
        data = generate_suhu(n, seed=seed + n)
        rep = repeat_adaptif(n)
        t_iter = ukur_waktu(avg_iteratif, data, repeat=rep)
        hasil.append((n, t_iter))
    return hasil

def benchmark_rekursif(ukuran_list, seed=123):
    hasil = []
    for n in ukuran_list:
        data = generate_suhu(n, seed=seed + n)
        rep = repeat_adaptif(n)
        t_rec = ukur_waktu(avg_rekursif, data, repeat=rep)
        hasil.append((n, t_rec))
    return hasil

def benchmark_both(ukuran_list, seed=123):
    hasil = []
    for n in ukuran_list:
        data = generate_suhu(n, seed=seed + n)
        rep = repeat_adaptif(n)
        t_iter = ukur_waktu(avg_iteratif, data, repeat=rep)
        t_rec  = ukur_waktu(avg_rekursif, data, repeat=rep)
        hasil.append((n, t_iter, t_rec))
    return hasil

# -------------------------
# SAVE CSV
# -------------------------
def save_csv_iteratif(hasil, out_csv="runtime_results.csv"):
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["N", "iteratif_s"])
        w.writerows(hasil)

def save_csv_rekursif(hasil, out_csv="runtime_results.csv"):
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["N", "rekursif_s"])
        w.writerows(hasil)

def save_csv_both(hasil, out_csv="runtime_results.csv"):
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["N", "iteratif_s", "rekursif_s"])
        w.writerows(hasil)

# -------------------------
# PLOT 
# -------------------------
def plot_iteratif(hasil, out_png="runtime_plot.png", show=False):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib belum terpasang, grafik tidak dibuat.")
        return

    N  = [x[0] for x in hasil]
    ti = [x[1] for x in hasil]

    plt.figure()
    plt.plot(N, ti, marker="o", label="Iteratif")
    plt.xlabel("Ukuran input (N)")
    plt.ylabel("Waktu eksekusi rata-rata (detik)")
    plt.title("Running Time Iteratif (Rata-rata Suhu)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    if show:
        plt.show()
    else:
        plt.close()

def plot_rekursif(hasil, out_png="runtime_plot.png", show=False):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib belum terpasang, grafik tidak dibuat.")
        return

    N  = [x[0] for x in hasil]
    tr = [x[1] for x in hasil]

    plt.figure()
    plt.plot(N, tr, marker="o", label="Rekursif")
    plt.xlabel("Ukuran input (N)")
    plt.ylabel("Waktu eksekusi rata-rata (detik)")
    plt.title("Running Time Rekursif (Rata-rata Suhu)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    if show:
        plt.show()
    else:
        plt.close()

def plot_both(hasil, out_png="runtime_plot.png", show=False):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib belum terpasang, grafik tidak dibuat.")
        return

    N  = [x[0] for x in hasil]
    ti = [x[1] for x in hasil]
    tr = [x[2] for x in hasil]

    plt.figure()
    plt.plot(N, ti, marker="o", label="Iteratif")
    plt.plot(N, tr, marker="o", label="Rekursif")
    plt.xlabel("Ukuran input (N)")
    plt.ylabel("Waktu eksekusi rata-rata (detik)")
    plt.title("Perbandingan Running Time: Iteratif vs Rekursif (Rata-rata Suhu)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    if show:
        plt.show()
    else:
        plt.close()

# -------------------------
# MAIN
# -------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["iteratif", "rekursif", "both"], default="both",
                        help="Pilih mode: iteratif / rekursif / both")
    parser.add_argument("--show", action="store_true",
                        help="Jika diaktifkan, grafik ditampilkan (pop-up). Default: tidak.")
    args = parser.parse_args()

    ukuran = [10, 100, 500, 1000, 2000, 5000]

    print("=== DEMO HITUNG RATA-RATA SUHU HARIAN ===")
    data7 = generate_suhu(7, seed=130)
    print("Data suhu 7 hari (°C):", data7)

    if args.mode == "iteratif":
        print(f"Rata-rata (Iteratif): {avg_iteratif(data7):.2f} °C")

        print("\n=== BENCHMARK RUNNING TIME (ITERATIF SAJA) ===")
        hasil = benchmark_iteratif(ukuran, seed=123)
        print("N | waktu_iteratif (s)")
        print("----------------------")
        for n, ti in hasil:
            print(f"{n:<4} {ti:<18.8f}")

        save_csv_iteratif(hasil, out_csv="runtime_results.csv")
        plot_iteratif(hasil, out_png="runtime_plot.png", show=args.show)

    elif args.mode == "rekursif":
        print(f"Rata-rata (Rekursif): {avg_rekursif(data7):.2f} °C")

        print("\n=== BENCHMARK RUNNING TIME (REKURSIF SAJA) ===")
        hasil = benchmark_rekursif(ukuran, seed=123)
        print("N | waktu_rekursif (s)")
        print("----------------------")
        for n, tr in hasil:
            print(f"{n:<4} {tr:<18.8f}")

        save_csv_rekursif(hasil, out_csv="runtime_results.csv")
        plot_rekursif(hasil, out_png="runtime_plot.png", show=args.show)

    else:
        print(f"Rata-rata (Iteratif): {avg_iteratif(data7):.2f} °C")
        print(f"Rata-rata (Rekursif): {avg_rekursif(data7):.2f} °C")

        print("\n=== BENCHMARK RUNNING TIME (ITERATIF vs REKURSIF) ===")
        hasil = benchmark_both(ukuran, seed=123)
        print("N | waktu_iteratif (s) | waktu_rekursif (s)")
        print("-------------------------------------------")
        for n, ti, tr in hasil:
            print(f"{n:<4} {ti:<18.8f} {tr:<18.8f}")

        save_csv_both(hasil, out_csv="runtime_results.csv")
        plot_both(hasil, out_png="runtime_plot.png", show=args.show)

    print("\nFile tersimpan:")
    print("- runtime_results.csv")
    print("- runtime_plot.png (jika matplotlib terpasang)")

if __name__ == "__main__":
    main()
