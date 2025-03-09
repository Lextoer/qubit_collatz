import sys
import os
import matplotlib.pyplot as plt
from qiskit import Aer, transpile, assemble, execute
from src.grover import create_grover_circuit
from src.collatz_oracle import collatz_oracle
import math

# === DEBUG MODU ===
DEBUG_MODE = True

# ✅ Çıkış dosya yolu ayarları
output_dir = os.path.join(os.path.dirname(__file__), 'out')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ✅ İlk ve son durum için dosya adı ayarları
MIN_FILENAME = os.path.join(output_dir, "min.png")
MAX_FILENAME = os.path.join(output_dir, "max.png")
MAX_DIST_FILENAME = os.path.join(output_dir, "max_dist.png")

# ✅ Başarı ve hata log dosyaları
SUCCESS_LOG = os.path.join(output_dir, "success_log.txt")
FAILURE_LOG = os.path.join(output_dir, "failure_log.txt")

def run_grover(start_num, iterations=2):
    num_qubits = int(math.ceil(math.log2(start_num + 1)))
    
    print(f"\nBaşlangıç Sayısı: {start_num}, Qubit Sayısı: {num_qubits}")

    # ✅ Devreyi oluşturuyoruz
    circuit = create_grover_circuit(num_qubits)

    # ✅ Başlangıç durumunu ayarlıyoruz
    start_state = f"{start_num:0{num_qubits}b}" 
    for i, bit in enumerate(start_state):
        if bit == '1' and i < num_qubits:
            circuit.x(i)

    # ✅ Grover iterasyonları → İşaretleme için çalıştırıyoruz
    for _ in range(iterations):
        collatz_oracle(circuit, list(range(num_qubits)))

    # ✅ Simülatörü tanımlıyoruz
    simulator = Aer.get_backend('aer_simulator')
    compiled_circuit = transpile(circuit, simulator)
    qobj = assemble(compiled_circuit)

    # ✅ Simülasyonu çalıştırıyoruz
    result = execute(circuit, simulator).result()
    counts = result.get_counts()

    # ✅ Sonuçları yazdırıyoruz
    print("\n==== Sonuçlar ====")
    print(counts)
    
    return counts, circuit

def plot_results(counts, filename):
    labels = counts.keys()
    values = counts.values()

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='royalblue')
    plt.xlabel('Durumlar', fontsize=14)
    plt.ylabel('Ölçüm Sayısı', fontsize=14)
    plt.title('Collatz Problemi Olasılık Dağılımı', fontsize=16)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(filename)
    plt.close()
    print(f"✅ Olasılık dağılımı kaydedildi → {filename}")

def log_result(start_num, is_success):
    log_file = SUCCESS_LOG if is_success else FAILURE_LOG
    with open(log_file, 'a') as file:
        file.write(f"Test Edilen Sayı: {start_num}\n")

def test_collatz(max_test=100):
    iterations = 2

    for start_num in range(2, max_test + 1):
        print(f"\n=== {start_num} Sayısını Test Ediyoruz ===")

        try:
            counts, circuit = run_grover(start_num, iterations)

            # ✅ Hedef durumu dinamik olarak ayarlıyoruz
            target_state = f"{1:0{int(math.ceil(math.log2(start_num + 1)))}b}"
            
            if target_state not in counts:
                print(f"\n🚨 **Collatz Hipotezi Geçersiz! {start_num} sayısı 1'e ulaşmıyor.** 🚨")
                plot_results(counts, os.path.join(output_dir, f"failure_{start_num}.png"))
                log_result(start_num, is_success=False)
                break
            else:
                print(f"✅ {start_num} sayısı Collatz zincirine uygun.")
                log_result(start_num, is_success=True)

            # ✅ İlk sayı için devreyi kaydet → "min.png"
            if start_num == 2 and DEBUG_MODE:
                circuit.draw(output='mpl', filename=MIN_FILENAME)
                print(f"✅ Başlangıç devresi kaydedildi → {MIN_FILENAME}")

            # ✅ Son sayı için devreyi kaydet → "max.png"
            if start_num == max_test and DEBUG_MODE:
                circuit.draw(output='mpl', filename=MAX_FILENAME)
                print(f"✅ Sonuç devresi kaydedildi → {MAX_FILENAME}")

            # ✅ Max test sayısına ulaşıldığında olasılık tablosunu kaydet
            if start_num == max_test:
                plot_results(counts, MAX_DIST_FILENAME)

        except Exception as e:
            print(f"\n❌ Hata Oluştu: {e}")

if __name__ == "__main__":
    max_test = 100
    test_collatz(max_test)
