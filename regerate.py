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
plt.title("Canal Haussier de Ryder System, Inc.", color="white")
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

# Ajouter une légende
plt.legend(loc="upper left", fontsize=12)

# Afficher le graphique
plt.grid(visible=False)
plt.show()
