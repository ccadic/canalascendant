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
plt.title("Canal Haussier de Ryder System, Inc. avec Signaux BUY/SELL et Backtest", color="white")
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

# Backtest : Stratégie d'achat et de vente
initial_capital = 10000  # Capital de départ
capital = initial_capital
in_position = False
buy_price = 0

executed_buy_signals = []  # Liste pour les signaux d'achat effectués
executed_sell_signals = []  # Liste pour les signaux de vente effectués

for date, price in zip(data.index, data["Close"]):
    if buy_signals and date == buy_signals[0][0]:  # Signal BUY
        if not in_position:  # Acheter si non investi
            buy_price = price
            in_position = True
            executed_buy_signals.append((date, price))  # Enregistrer le signal BUY effectué
        buy_signals.pop(0)

    elif sell_signals and date == sell_signals[0][0]:  # Signal SELL
        if in_position:  # Vendre si investi
            capital *= price / buy_price  # Calculer le capital après vente
            in_position = False
            executed_sell_signals.append((date, price))  # Enregistrer le signal SELL effectué
        sell_signals.pop(0)

# Si on est en position à la fin de la période, on vend
if in_position:
    capital *= data["Close"][-1] / buy_price  # Vente au dernier prix connu

# Calcul du pourcentage de progression
percentage_increase = ((capital - initial_capital) / initial_capital) * 100

# Afficher les résultats dans un cadre sur le graphique
results_text = f"Invest Depart: {initial_capital} USD\nCapital en sortie: {capital:.2f} USD\nPourcentage de progression: {percentage_increase:.2f} %"
plt.text(data.index[-1], min(data["Close"]), results_text, color="white", ha="right", va="bottom", bbox=dict(facecolor="black", alpha=0.7))

# Ajouter les triangles pour les signaux BUY et SELL exécutés
for buy_signal in executed_buy_signals:
    plt.scatter(buy_signal[0], buy_signal[1], color="green", marker="^", s=100, label="BUY (executed)")

for sell_signal in executed_sell_signals:
    plt.scatter(sell_signal[0], sell_signal[1], color="red", marker="v", s=100, label="SELL (executed)")

# Ajouter une légende sans les éléments en double
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))  # Éviter les doublons dans la légende
plt.legend(by_label.values(), by_label.keys(), loc="upper left", fontsize=12)

# Afficher le graphique
plt.grid(visible=False)
plt.show()
