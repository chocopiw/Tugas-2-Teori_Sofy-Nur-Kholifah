from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

# Fungsi untuk simulasi Monte Carlo
def monte_carlo_simulation(data, num_simulations=1000):
    # Hitung rata-rata dan standar deviasi dari data
    mean = data.mean()
    std_dev = data.std()

    # Lakukan simulasi Monte Carlo
    simulations = np.random.normal(mean, std_dev, num_simulations)

    # Mengembalikan rata-rata simulasi, interval bawah, dan interval atas
    return np.mean(simulations), np.percentile(simulations, 5), np.percentile(simulations, 95)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Ambil input tahun dari form
            year = int(request.form['tahun'])

            # Baca file CSV
            data = pd.read_csv('angka_kematian_balita.csv')

            # Jika tahun ada di data, gunakan data tersebut
            if year in data['tahun'].values:
                data_filtered = data[data['tahun'] == year]
                mean_pred, lower_bound, upper_bound = monte_carlo_simulation(data_filtered['jumlah_kematian'])
            else:
                # Prediksi untuk tahun di luar data menggunakan rata-rata historis
                mean_pred, lower_bound, upper_bound = monte_carlo_simulation(data['jumlah_kematian'])

            # Tampilkan hasil ke HTML
            return render_template('index.html', prediction=mean_pred, lower_bound=lower_bound, upper_bound=upper_bound, year=year)
        
        except Exception as e:
            return render_template('index.html', error=f"Terjadi kesalahan: {str(e)}")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
