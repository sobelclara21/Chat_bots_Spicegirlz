# Spice AI

**Projet :** Application Chatbot avec Snowflake Cortex  
**Team :** SpiceGirlz (Coralie • Hiba • Sophia • Clara • Jade)  
**Date :** Février 2026

---

## Objectif du projet

Concevoir une application web de type ChatGPT avec Streamlit, hébergée via Streamlit in Snowflake, utilisant Snowflake Cortex pour interagir avec un LLM, **sans utiliser de clé OpenAI**.

---

## 1️⃣ Application Streamlit

### Lien vers l'application déployée
```
https://app.snowflake.com/sfvfpfj/nc76900/#/streamlit-apps/CHATBOT_DB.APP.FB8NMSLT10JYN33_/edit
```

### Capture d'écran fonctionnelle
- Vidéo de démonstration disponible

### Description de l'architecture


**Flux de données :**
```
Utilisateur → Interface Streamlit → Python (construction prompt)
    ↓
Snowpark Session → SNOWFLAKE.CORTEX.COMPLETE(model, prompt)
    ↓
Réponse LLM → Affichage dans chat + Sauvegarde en base
```


## 3️⃣ Repository GitHub Public

### URL du repository
**https://github.com/sobelclara21/Chat_bots_Spicegirlz**

**Visibilité :** 🌍 Public


**Sections principales :**

#### Description du projet
Application de chatbot conversationnel utilisant Snowflake Cortex pour fournir une expérience similaire à ChatGPT, avec interface personnalisée, persistance complète et multi-modèles.

#### Étapes de déploiement
1. Configuration environnement Snowflake (setup.sql)
2. Création application Streamlit
3. Déploiement du code Python
4. Tests et validation


#### Instructions d'exécution

1. Accéder à l'app via Snowflake → Streamlit Apps
2. Taper un message dans la zone de saisie
3. Changer de modèle via la sidebar
4. Créer nouvelle conversation avec "🆕 Nouveau chat"
5. Effacer l'historique avec "🗑️ Effacer"

### Arborescence claire

```
Chat_bots_Spicegirlz/
│
├── README.md                    
├── streamlit_app.py             
├── setup.sql   
├──Video_demo               
│
└── Image/
    └── spice_ai_logo.jpeg      
```


### Fonctionnalités complètes

✅ Chat conversationnel temps réel  
✅ Multi-modèles (3 choix)  
✅ Persistance historique  
✅ Gestion sessions  
✅ Design personnalisé  
✅ Avatars custom  
✅ Nouveau chat / Effacer  
✅ Paramètres configurables  

---

## 📞 Informations

**Repository GitHub :** https://github.com/sobelclara21/Chat_bots_Spicegirlz  
**Team :** SpiceGirlz (Coralie • Hiba • Sophia • Clara • Jade)

---
