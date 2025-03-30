# Ce bot envoie une alerte mail via le processus SMTP. K=Le bot ci dessous n'est
# configuré que pour des adresses mail receveur Gmail. Pour toute autre adresse mail
# se referer au protocole SMTP de l'adresse mail specifique


import numpy as np
import pandas as pd
import yfinance as yf
import smtplib
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

STOCK_SYMBOL = "AAPL"
START_DATE = "2023-01-01"
END_DATE = "2024-01-01"
THRESHOLD = -0.05  # Seuil de détection des anomalies (-5%)
EMAIL_SENDER = "maxence.delehelle@edu.esiee.fr"
EMAIL_RECEIVER = "votre_adresse_mail@gmail.com"
EMAIL_PASSWORD = "votre_mdp_de_mail" # Remarque : l'authentification à deux étapes doit être
                                     #activée pour que Gmail autorise l'utilisation de STMP


print("Téléchargement des données...")
data = yf.download(STOCK_SYMBOL, start=START_DATE, end=END_DATE)
data['Returns'] = data['Close'].pct_change()
data = data.dropna()

print("Détection des anomalies...")
model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
data['Anomaly'] = model.fit_predict(data[['Returns']])
data['Anomaly'] = data['Anomaly'].apply(lambda x: 1 if x == -1 else 0)


anomalies = data[data['Anomaly'] == 1]
anomalies = anomalies[anomalies['Returns'] < THRESHOLD]


if not anomalies.empty:
    print("Anomalies détectées ! Envoi de l'email...")
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = f"ALERTE : Anomalies détectées sur {STOCK_SYMBOL}"
    
    body = f"Les anomalies suivantes ont été détectées :\n\n{anomalies[['Returns']].to_string()}"
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    print("Email envoyé !")


plt.figure(figsize=(12,6))
plt.plot(data.index, data['Close'], label='Prix de clôture', color='blue')
plt.scatter(anomalies.index, anomalies['Close'], color='red', label='Anomalies', marker='o')
plt.title(f"Anomalies sur {STOCK_SYMBOL}")
plt.legend()
plt.show()

print("Analyse terminée.")
