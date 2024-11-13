import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Définir la période d'affichage
start_date = "2024-03-01"
end_date = "2024-11-12"

# Télécharger les données de l'action Ryder System, Inc.
symbol = "R"
data = yf.download(symbol, start=start_date, end=end_date, interval="1d")

# Paramètres pour l'affichage
plt.style.use("dark_background")
plt.figure(figsize=(14, 8))
plt.title("Canal Haussier de Ryder System, Inc. avec Signaux BUY/SELL", color="white")
plt.xlabel("Date", color="white")
plt.ylabel("Prix de l'action", color="white")

# Définir les équations du canal
x_dates = np.arange(np.datetime64("2024-03-01"), np.datetime64("2024-11-13"))
x_days = (x_dates - np.datetime64("2024-01-01")).astype(int)

# Équation de la ligne supérieure et inférieure
y_upper = 0.1649 * x_days + 104.99
y_lower = 0.1665 * x_days + 89.23

# Tracer les lignes du canal
plt.plot(x_dates, y_upper, color="violet", linestyle="--", label="Canal Supérieur")
plt.plot(x_dates, y_lower, color="green", linestyle="--", label="Canal Inférieur")

# Tracer le cours de l'action
plt.plot(data.index, data["Close"], color="white", label="Cours de l'Action Ryder System, Inc.")

# Calcul des signaux BUY et SELL avec une tolérance de 98%
buy_signals = []
sell_signals = []
previous_position = None  # Utilisé pour éviter la répétition de signaux consécutifs

for i, (date, price) in enumerate(zip(data.index, data["Close"])):
    day_from_start = (date - np.datetime64("2024-01-01")).days
    upper_bound = 0.1649 * day_from_start + 104.99
    lower_bound = 0.1665 * day_from_start + 89.23

    # Déterminer la position actuelle par rapport aux bornes avec une tolérance de 98%
    if price <= lower_bound * 1.02:  # En dessous de la limite inférieure ou à 98% de celle-ci
        current_position = "below_lower"
        if current_position != previous_position:  # Éviter les signaux consécutifs
            buy_signals.append((date, price))
    elif price >= upper_bound * 0.98:  # Au-dessus de la limite supérieure ou à 98% de celle-ci
        current_position = "above_upper"
        if current_position != previous_position:
            sell_signals.append((date, price))
    else:
        current_position = "inside"  # Dans le canal

    previous_position = current_position

# Ajouter les triangles pour les signaux sans dupliquer la légende
buy_plotted = sell_plotted = False
for buy_signal in buy_signals:
    if not buy_plotted:
        plt.scatter(buy_signal[0], buy_signal[1], color="green", marker="^", s=100, label="BUY")
        buy_plotted = True
    else:
        plt.scatter(buy_signal[0], buy_signal[1], color="green", marker="^", s=100)

for sell_signal in sell_signals:
    if not sell_plotted:
        plt.scatter(sell_signal[0], sell_signal[1], color="red", marker="v", s=100, label="SELL")
        sell_plotted = True
    else:
        plt.scatter(sell_signal[0], sell_signal[1], color="red", marker="v", s=100)

# Ajouter une légende sans les éléments en double
plt.legend(loc="upper left", fontsize=12)

# Afficher le graphique
plt.grid(visible=False)
plt.show()
