import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="TARDIS - SNCF", layout="wide")

st.title("TARDIS : Prédire l'imprévisible (Retards SNCF)")
st.markdown("Bienvenue sur le tableau de bord de prédiction des retards. Entrez les paramètres de votre trajet pour estimer votre retard à l'arrivée !")

st.divider()

@st.cache_resource
def load_model():
    return joblib.load('model.pkl')

modele = load_model()

st.success("Le modèle d'Intelligence Artificielle est chargé et prêt à prédire !")

st.subheader("Entrez les paramètres de votre trajet")

col1, col2, col3 = st.columns(3)

with col1:
    duree = st.number_input("Durée moyenne du trajet (min)", min_value=30, max_value=300, value=120)
    nb_trains = st.number_input("Nombre de trains prévus", min_value=1, max_value=20, value=5)

with col2:
    is_weekend = st.selectbox("Période du trajet", options=["Semaine", "Week-end"])
    is_weekend_encoded = 1 if is_weekend == "Week-end" else 0
    retard_depart = st.number_input("Retard moyen estimé au départ (min)", min_value=0, max_value=120, value=5)

with col3:
    cause_externe = st.slider("% Retard dû à des causes externes (ex: météo)", 0, 100, 0)
    cause_infra = st.slider("% Retard dû aux infrastructures", 0, 100, 0)

st.divider()

if st.button("Estimer mon retard à l'arrivée"):
    
    colonnes_du_modele = [
        'Average journey time', 
        'Number of scheduled trains', 
        'Number of cancelled trains', 
        'Number of trains delayed at departure',
        'Average delay of late trains at departure',
        'Average delay of all trains at departure',
        'Number of trains delayed at arrival',           
        'Average delay of late trains at arrival',       
        'Number of trains delayed > 15min',
        'Average delay of trains > 15min (if competing with flights)',
        'Number of trains delayed > 30min',
        'Number of trains delayed > 60min',
        'Pct delay due to external causes',
        'Pct delay due to infrastructure',
        'Pct delay due to traffic management',
        'Pct delay due to rolling stock',
        'Pct delay due to station management and equipment reuse', 
        'Pct delay due to passenger handling (crowding, disabled persons, connections)',
        'year',
        'month',
        'weekday',
        'is_weekend'
    ]

    donnees_utilisateur = pd.DataFrame(0, index=[0], columns=colonnes_du_modele)

    donnees_utilisateur['Average journey time'] = duree
    donnees_utilisateur['Number of scheduled trains'] = nb_trains
    donnees_utilisateur['is_weekend'] = is_weekend_encoded
    
    donnees_utilisateur['Average delay of late trains at departure'] = retard_depart
    
    donnees_utilisateur['Number of trains delayed at departure'] = nb_trains / 2
    donnees_utilisateur['Number of trains delayed at arrival'] = nb_trains / 2
    
    donnees_utilisateur['Average delay of late trains at arrival'] = retard_depart
    
    donnees_utilisateur['Pct delay due to external causes'] = cause_externe / 100.0
    donnees_utilisateur['Pct delay due to infrastructure'] = cause_infra / 100.0
    
    prediction = modele.predict(donnees_utilisateur)
    retard_estime = prediction[0]
    
    if retard_estime <= 5:
        st.success(f"Bon voyage ! Le retard estimé est minime : **{retard_estime:.0f} minutes**.")
    elif retard_estime <= 15:
        st.warning(f"Attention, un léger retard est estimé à : **{retard_estime:.0f} minutes**.")
    else:
        st.error(f"Prévoyez de la marge ! Le retard estimé est de : **{retard_estime:.0f} minutes**.")
