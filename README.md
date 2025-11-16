# 📊 Application d'Analyse : Relations Amoureuses & Estime de Soi

Application Streamlit pour analyser les données d'un questionnaire de psychologie sur l'influence des relations amoureuses sur l'estime de soi chez les jeunes adultes.

## 🎯 Fonctionnalités

### 1. **Dashboard Global** 🏠
- KPIs : Nombre de participants, moyennes par dimension
- Vue d'ensemble des 4 dimensions (ES, Valorisation, MR, GC)
- Distributions sociodémographiques
- Matrice de corrélation

### 2. **Analyses des Moyennes** 📊
- **Page dédiée aux moyennes par variable**
- Calcul des moyennes pour tous les items et totaux
- Filtrage dynamique de la population
- Tableaux détaillés par dimension
- Graphiques des moyennes des items
- Export CSV des résultats

### 3. **Analyses par Dimension**
- **Estime de Soi (ES)** 💙 : 10 items (Échelle de Rosenberg)
- **Valorisation** 💎 : 5 items
- **Manque de Reconnaissance (MR)** ⚠️ : 6 items
- **Gestion des Conflits (GC)** 🤝 : 6 items

Pour chaque dimension :
- Distribution des scores
- Comparaisons par groupes
- Analyse item par item
- Corrélations avec l'estime de soi

### 4. **Analyses Croisées** 🔗
- Matrice de corrélation complète
- Scatter matrix multivariée
- Coordonnées parallèles
- Comparaisons par groupes sociodémographiques

### 5. **Statistiques Détaillées** 📈
- Statistiques descriptives complètes
- Comparaisons par groupes
- Résumé de l'échantillon

## 🎛️ Système de Filtres

Filtres disponibles dans la sidebar :
- 👤 **Âge** : 18-20 ans, 20-25 ans
- ⚧️ **Genre** : Femme, Homme, Autre
- 🎓 **Niveau d'études** : Lycée à Master+
- 🏠 **Cohabitation** : Oui/Non
- 😊 **Satisfaction relationnelle** : 4 niveaux
- ⏱️ **Durée de la relation** : Slider en mois

**→ Les filtres s'appliquent en temps réel sur toutes les analyses !**

## 📁 Structure du Projet

```
.
├── app.py                      # Application principale Streamlit
├── config.py                   # Configuration et mappings
├── data_processing.py          # Traitement des données (avec cache)
├── visualizations.py           # Fonctions de visualisation Plotly
├── requirements.txt            # Dépendances Python
└── README.md                   # Ce fichier
```

## 🚀 Installation et Lancement

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

### 3. Charger vos données

**📤 Upload de fichier (Recommandé)**

L'application utilise un système d'**upload de fichier** pour garantir la confidentialité de vos données :

1. Cliquez sur le bouton "Browse files" dans l'interface
2. Sélectionnez votre fichier Excel (`.xlsx` ou `.xls`)
3. Les données sont chargées et l'analyse commence automatiquement

✅ **Avantages** :
- 🔒 Vos données restent privées (jamais sauvegardées sur le serveur)
- 🌍 Idéal pour le déploiement sur Streamlit Cloud
- 👥 Chaque utilisateur peut analyser ses propres données
- 🔄 Changement de fichier facile

**ℹ️ Mode développement**

Si un fichier `Etudes_relations_amoureuses.xlsx` est présent dans le dossier du projet, il sera chargé automatiquement (pratique pour le développement local).

## 📊 Structure des Données

### Variables Sociodémographiques
- **id_participants** : Identifiant unique
- **Age** : 1 = 18-20 ans, 2 = 20-25 ans
- **Genre** : 1 = Femme, 2 = Homme, 3 = Autre
- **Etude** : 1 = Lycée, 2 = L1, 3 = L2, 4 = L3, 5 = Master+

### Variables Relationnelles (Items 4-7)
- **Item4** : Situation (1 = En couple, 2 = Autre)
- **Item5** : Durée de la relation (en mois)
- **Item6** : Cohabitation (1 = Oui, 2 = Non)
- **Item7** : Satisfaction (1 = Très insatisfaisante → 4 = Très satisfaisante)

### Dimensions Psychométriques

#### 📘 Estime de Soi (Items 8-17) → Total ES
Échelle de Rosenberg : 10 items
- Évalue l'estime de soi globale
- Score de 10 à 40

#### 💚 Valorisation (Items 18-22) → Total valo
5 items sur le sentiment d'être valorisé dans la relation
- Score de 5 à 25

#### ⚠️ Manque de Reconnaissance (Items 23-28) → Total MR
6 items sur les sentiments de négligence
- Score de 6 à 30

#### 🤝 Gestion des Conflits (Items 29-34) → Total GC
6 items sur la qualité de gestion des désaccords
- Score de 6 à 30

**Note importante** : Les colonnes "Total" ne sont PAS des items de questionnaire, ce sont des scores calculés (somme des items de chaque dimension).

## 💡 Utilisation

### Workflow typique

1. **Explorer le Dashboard** pour avoir une vue d'ensemble
2. **Utiliser les filtres** pour sélectionner un sous-groupe
3. **Consulter l'onglet "Analyses Moyennes"** pour voir toutes les moyennes
4. **Explorer chaque dimension** dans son onglet dédié
5. **Analyser les corrélations** dans "Analyses Croisées"
6. **Exporter les résultats** (CSV) depuis l'onglet "Analyses Moyennes"

### Exemples d'analyses possibles

- Comparer l'estime de soi selon le genre
- Voir l'impact de la cohabitation sur le manque de reconnaissance
- Analyser la corrélation valorisation ↔ estime de soi
- Identifier les items les plus discriminants
- Comparer les profils selon la satisfaction relationnelle

## 🎨 Personnalisation

### Modifier les couleurs

Éditez `config.py` → Section `COLORS_DIMENSIONS`

### Ajouter des analyses

1. Créez une nouvelle fonction dans `visualizations.py`
2. Appelez-la dans `app.py` dans l'onglet approprié

### Modifier les filtres

Éditez la section "SIDEBAR - FILTRES" dans `app.py` (lignes 50-120)

## ⚡ Optimisations

- **Cache Streamlit** : `@st.cache_data` sur toutes les fonctions de traitement
- **Lazy Loading** : Les graphiques se chargent uniquement quand l'onglet est sélectionné
- **Filtrage efficace** : Pandas optimisé pour les opérations de filtrage

## 📝 Notes Techniques

- **Plotly** est utilisé pour tous les graphiques (interactifs et exportables)
- **Pandas** pour toutes les manipulations de données
- **Streamlit** pour l'interface utilisateur
- Les données sont rechargées uniquement si le fichier change (cache)

## 🐛 Dépannage

### L'application ne se lance pas
- Vérifiez que Python 3.8+ est installé
- Installez les dépendances : `pip install -r requirements.txt`

### Les graphiques ne s'affichent pas
- Vérifiez que plotly est bien installé
- Essayez de recharger la page (F5)

### Erreur de chargement des données
- Vérifiez le chemin du fichier Excel
- Assurez-vous que le fichier a bien 2 lignes d'en-tête

### Les filtres ne fonctionnent pas
- Cliquez sur "Réinitialiser les filtres" dans la sidebar
- Rafraîchissez la page

## 📧 Support

Pour toute question ou amélioration, n'hésitez pas !

---

**Version** : 1.0  
**Dernière mise à jour** : Novembre 2024  
**Licence** : Projet académique