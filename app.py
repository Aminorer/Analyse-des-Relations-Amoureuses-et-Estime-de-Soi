"""
Application Streamlit pour l'analyse des relations amoureuses et estime de soi
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import *
from data_processing import *
from visualizations import *

# ============================================================================
# CONFIGURATION DE LA PAGE
# ============================================================================

st.set_page_config(
    page_title="Analyse Relations Amoureuses & Estime de Soi",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CHARGEMENT DES DONNÉES
# ============================================================================

@st.cache_data
def load_and_prepare_data_from_file(uploaded_file):
    """Charge et prépare les données depuis un fichier uploadé"""
    df = load_data(uploaded_file)
    df = apply_labels(df)
    return df

@st.cache_data
def load_and_prepare_data_from_path():
    """Charge et prépare les données depuis un chemin local (fallback)"""
    import os
    possible_paths = [
        './Etudes_relations_amoureuses.xlsx',
        'Etudes_relations_amoureuses.xlsx',
        '../Etudes_relations_amoureuses.xlsx',
        '/mnt/user-data/uploads/Etudes_relations_amoureuses.xlsx',
    ]
    
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
    
    if file_path:
        df = load_data(file_path)
        df = apply_labels(df)
        return df
    return None

# Interface d'upload de fichier
st.markdown("## 📂 Chargement des données")

uploaded_file = st.file_uploader(
    "Téléchargez votre fichier Excel (format attendu : Etudes_relations_amoureuses.xlsx)",
    type=['xlsx', 'xls'],
    help="Le fichier doit contenir 2 lignes d'en-tête et 39 colonnes de données"
)

# Charger les données
df_original = None

if uploaded_file is not None:
    try:
        with st.spinner('📊 Chargement des données en cours...'):
            df_original = load_and_prepare_data_from_file(uploaded_file)
        st.success(f"✅ Fichier chargé avec succès ! ({len(df_original)} participants)")
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier : {e}")
        st.info("""
        **Vérifiez que votre fichier :**
        - Est au format Excel (.xlsx ou .xls)
        - Contient 2 lignes d'en-tête
        - A 39 colonnes (id_participants, Age, Genre, Etude, Items 4-34, Totaux)
        """)
        st.stop()
else:
    # Essayer de charger depuis un fichier local (pour développement)
    df_original = load_and_prepare_data_from_path()
    
    if df_original is None:
        st.info("""
        ### 👋 Bienvenue dans l'application d'analyse !
        
        Pour commencer, veuillez **télécharger votre fichier Excel** en utilisant 
        le bouton ci-dessus.
        
        #### 📋 Format attendu du fichier :
        
        - **Format** : Excel (.xlsx ou .xls)
        - **En-têtes** : 2 lignes (titres des sections + noms des items)
        - **Colonnes** : 39 colonnes au total
        
        #### 📊 Structure des données :
        
        1. **Variables sociodémographiques** (4 colonnes)
           - id_participants, Age, Genre, Etude
        
        2. **Variables relationnelles** (4 colonnes)
           - Item4 (Situation), Item5 (Durée), Item6 (Cohabitation), Item7 (Satisfaction)
        
        3. **Estime de Soi** (10 items + 1 total)
           - Items 8 à 17, Total ES
        
        4. **Valorisation** (5 items + 1 total)
           - Items 18 à 22, Total valo
        
        5. **Manque de Reconnaissance** (6 items + 1 total)
           - Items 23 à 28, Total MR
        
        6. **Gestion des Conflits** (6 items + 1 total)
           - Items 29 à 34, Total GC
        
        ---
        
        **🔒 Confidentialité** : Vos données restent privées et ne sont jamais sauvegardées 
        sur le serveur. Elles sont traitées uniquement dans votre session.
        """)
        st.stop()
    else:
        st.info("ℹ️ Fichier local détecté et chargé. Pour utiliser vos propres données, uploadez un fichier ci-dessus.")

st.markdown("---")

# ============================================================================
# SIDEBAR - FILTRES
# ============================================================================

st.sidebar.title("🎛️ Filtres")
st.sidebar.markdown("---")

# Initialiser les filtres
filters = {}

# Filtre Âge
st.sidebar.subheader("👤 Âge")
age_options = df_original['Age'].unique()
age_selected = st.sidebar.multiselect(
    "Sélectionner les tranches d'âge",
    options=sorted(age_options),
    default=sorted(age_options),
    format_func=lambda x: AGE_LABELS[x]
)
if age_selected:
    filters['Age'] = age_selected

# Filtre Genre
st.sidebar.subheader("⚧️ Genre")
genre_options = df_original['Genre'].unique()
genre_selected = st.sidebar.multiselect(
    "Sélectionner les genres",
    options=sorted(genre_options),
    default=sorted(genre_options),
    format_func=lambda x: GENRE_LABELS[x]
)
if genre_selected:
    filters['Genre'] = genre_selected

# Filtre Niveau d'études
st.sidebar.subheader("🎓 Niveau d'études")
etude_options = df_original['Etude'].unique()
etude_selected = st.sidebar.multiselect(
    "Sélectionner les niveaux",
    options=sorted(etude_options),
    default=sorted(etude_options),
    format_func=lambda x: ETUDE_LABELS[x]
)
if etude_selected:
    filters['Etude'] = etude_selected

# Filtre Cohabitation
st.sidebar.subheader("🏠 Cohabitation")
cohab_options = df_original['Item6'].unique()
cohab_selected = st.sidebar.multiselect(
    "Vit avec le/la partenaire",
    options=sorted(cohab_options),
    default=sorted(cohab_options),
    format_func=lambda x: COHABITATION_LABELS[x]
)
if cohab_selected:
    filters['Item6'] = cohab_selected

# Filtre Satisfaction
st.sidebar.subheader("😊 Satisfaction relationnelle")
satisf_options = df_original['Item7'].unique()
satisf_selected = st.sidebar.multiselect(
    "Niveau de satisfaction",
    options=sorted(satisf_options),
    default=sorted(satisf_options),
    format_func=lambda x: SATISFACTION_LABELS[x]
)
if satisf_selected:
    filters['Item7'] = satisf_selected

# Filtre Durée de relation
st.sidebar.subheader("⏱️ Durée de la relation")
if 'Item5' in df_original.columns:
    duree_min = int(df_original['Item5'].min())
    duree_max = int(df_original['Item5'].max())
    duree_range = st.sidebar.slider(
        "Durée en mois",
        min_value=duree_min,
        max_value=duree_max,
        value=(duree_min, duree_max)
    )

st.sidebar.markdown("---")

# Bouton de réinitialisation
if st.sidebar.button("🔄 Réinitialiser les filtres", use_container_width=True):
    st.rerun()

# ============================================================================
# APPLIQUER LES FILTRES
# ============================================================================

df_filtered = filter_data(df_original, filters)

# Filtre sur la durée si spécifié
if 'Item5' in df_filtered.columns:
    df_filtered = df_filtered[
        (df_filtered['Item5'] >= duree_range[0]) & 
        (df_filtered['Item5'] <= duree_range[1])
    ]

# Afficher le nombre de participants après filtrage
n_filtered = len(df_filtered)
n_total = len(df_original)
st.sidebar.markdown(f"### 📊 Échantillon")
st.sidebar.metric("Participants sélectionnés", f"{n_filtered} / {n_total}")

if n_filtered == 0:
    st.warning("⚠️ Aucun participant ne correspond aux filtres sélectionnés.")
    st.stop()

# ============================================================================
# EN-TÊTE DE L'APPLICATION
# ============================================================================

st.title(APP_TITLE)
st.markdown(f"**{APP_SUBTITLE}**")
st.markdown("---")

# ============================================================================
# NAVIGATION PAR ONGLETS
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏠 Accueil",
    "📊 Analyses Moyennes",
    "💙 Estime de Soi",
    "💎 Valorisation",
    "⚠️ Manque Reconnaissance",
    "🤝 Gestion Conflits",
    "🔗 Analyses Croisées",
    "📈 Statistiques"
])

# ============================================================================
# TAB 1 : ACCUEIL / DASHBOARD
# ============================================================================

with tab1:
    st.header("🏠 Dashboard - Vue d'ensemble")
    
    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("👥 Participants", n_filtered)
    
    with col2:
        st.metric("💙 Estime de Soi", f"{df_filtered['Total ES'].mean():.1f}")
    
    with col3:
        st.metric("💎 Valorisation", f"{df_filtered['Total valo'].mean():.1f}")
    
    with col4:
        st.metric("⚠️ Manque Recon.", f"{df_filtered['Total MR'].mean():.1f}")
    
    with col5:
        st.metric("🤝 Gestion Conflits", f"{df_filtered['Total GC'].mean():.1f}")
    
    st.markdown("---")
    
    # Vue d'ensemble des dimensions
    st.subheader("📊 Scores moyens par dimension")
    fig_overview = create_dimension_overview(df_filtered)
    st.plotly_chart(fig_overview, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Deux colonnes pour les graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Répartition par âge")
        age_dist = df_filtered['Age_label'].value_counts().reset_index()
        age_dist.columns = ['Âge', 'Nombre']
        fig_age = create_pie_chart(age_dist, 'Âge', 'Nombre', 'Distribution par tranche d\'âge')
        st.plotly_chart(fig_age, use_container_width=True, config=PLOTLY_CONFIG)
    
    with col2:
        st.subheader("⚧️ Répartition par genre")
        genre_dist = df_filtered['Genre_label'].value_counts().reset_index()
        genre_dist.columns = ['Genre', 'Nombre']
        fig_genre = create_pie_chart(genre_dist, 'Genre', 'Nombre', 'Distribution par genre')
        st.plotly_chart(fig_genre, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Graphique du niveau d'études
    st.subheader("🎓 Répartition par niveau d'études")
    etude_dist = df_filtered['Etude_label'].value_counts().reset_index()
    etude_dist.columns = ['Niveau', 'Nombre']
    # Trier selon l'ordre logique
    etude_order = ["Lycée", "Licence 1", "Licence 2", "Licence 3", "Master ou plus"]
    etude_dist['Niveau'] = pd.Categorical(etude_dist['Niveau'], categories=etude_order, ordered=True)
    etude_dist = etude_dist.sort_values('Niveau')
    
    fig_etude = create_bar_chart(etude_dist, 'Niveau', 'Nombre', 
                                  'Distribution par niveau d\'études')
    st.plotly_chart(fig_etude, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Matrice de corrélation
    st.subheader("🔗 Corrélations entre les dimensions")
    corr_matrix = get_correlation_matrix(df_filtered)
    fig_corr = create_correlation_heatmap(corr_matrix, 
                                          "Matrice de corrélation entre les scores totaux")
    st.plotly_chart(fig_corr, use_container_width=True, config=PLOTLY_CONFIG)

# ============================================================================
# TAB 2 : ANALYSES MOYENNES
# ============================================================================

with tab2:
    st.header("📊 Analyses des Moyennes par Variable")
    
    st.markdown("""
    Cette page présente les moyennes de chaque variable (items et totaux) pour l'échantillon sélectionné.
    Utilisez les filtres dans la barre latérale pour analyser des sous-groupes spécifiques.
    """)
    
    st.markdown("---")
    
    # Calculer toutes les moyennes
    moyennes_df = calculate_averages_by_filters(df_filtered)
    
    # Afficher les statistiques globales
    st.subheader("📈 Statistiques globales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Estime de Soi (Total ES)",
            f"{moyennes_df.loc['Total ES', 'Moyenne']:.2f}",
            delta=f"σ = {moyennes_df.loc['Total ES', 'Écart-type']:.2f}"
        )
    
    with col2:
        st.metric(
            "Valorisation (Total valo)",
            f"{moyennes_df.loc['Total valo', 'Moyenne']:.2f}",
            delta=f"σ = {moyennes_df.loc['Total valo', 'Écart-type']:.2f}"
        )
    
    with col3:
        st.metric(
            "Manque Recon. (Total MR)",
            f"{moyennes_df.loc['Total MR', 'Moyenne']:.2f}",
            delta=f"σ = {moyennes_df.loc['Total MR', 'Écart-type']:.2f}"
        )
    
    with col4:
        st.metric(
            "Gestion Conflits (Total GC)",
            f"{moyennes_df.loc['Total GC', 'Moyenne']:.2f}",
            delta=f"σ = {moyennes_df.loc['Total GC', 'Écart-type']:.2f}"
        )
    
    st.markdown("---")
    
    # Tableau complet des moyennes par dimension
    st.subheader("📋 Tableau détaillé des moyennes")
    
    # Organiser par dimension
    dimensions_tabs = st.tabs(["Estime de Soi", "Valorisation", "Manque Reconnaissance", "Gestion Conflits", "Variables relationnelles"])
    
    with dimensions_tabs[0]:
        st.markdown("**Items d'Estime de Soi (Échelle de Rosenberg)**")
        es_items = ITEMS_ESTIME_SOI['items'] + [ITEMS_ESTIME_SOI['total']]
        es_data = moyennes_df.loc[moyennes_df.index.isin(es_items)]
        
        # Ajouter les labels
        es_data_display = es_data.copy()
        es_data_display['Label'] = es_data_display.index.map(
            lambda x: ITEMS_ESTIME_SOI_LABELS.get(x, x) if x in ITEMS_ESTIME_SOI_LABELS else "Total Estime de Soi"
        )
        es_data_display = es_data_display[['Label', 'Moyenne', 'Écart-type', 'N']]
        
        st.dataframe(es_data_display, use_container_width=True)
        
        # Graphique des moyennes
        means_es = df_filtered[ITEMS_ESTIME_SOI['items']].mean().sort_values(ascending=True)
        fig_es_means = create_item_means_chart(
            means_es,
            "Moyennes des items d'Estime de Soi",
            ITEMS_ESTIME_SOI_LABELS
        )
        st.plotly_chart(fig_es_means, use_container_width=True, config=PLOTLY_CONFIG)
    
    with dimensions_tabs[1]:
        st.markdown("**Items de Valorisation dans la relation**")
        valo_items = ITEMS_VALORISATION['items'] + [ITEMS_VALORISATION['total']]
        valo_data = moyennes_df.loc[moyennes_df.index.isin(valo_items)]
        
        valo_data_display = valo_data.copy()
        valo_data_display['Label'] = valo_data_display.index.map(
            lambda x: ITEMS_VALORISATION_LABELS.get(x, x) if x in ITEMS_VALORISATION_LABELS else "Total Valorisation"
        )
        valo_data_display = valo_data_display[['Label', 'Moyenne', 'Écart-type', 'N']]
        
        st.dataframe(valo_data_display, use_container_width=True)
        
        means_valo = df_filtered[ITEMS_VALORISATION['items']].mean().sort_values(ascending=True)
        fig_valo_means = create_item_means_chart(
            means_valo,
            "Moyennes des items de Valorisation",
            ITEMS_VALORISATION_LABELS
        )
        st.plotly_chart(fig_valo_means, use_container_width=True, config=PLOTLY_CONFIG)
    
    with dimensions_tabs[2]:
        st.markdown("**Items de Manque de Reconnaissance**")
        mr_items = ITEMS_MANQUE_RECONNAISSANCE['items'] + [ITEMS_MANQUE_RECONNAISSANCE['total']]
        mr_data = moyennes_df.loc[moyennes_df.index.isin(mr_items)]
        
        mr_data_display = mr_data.copy()
        mr_data_display['Label'] = mr_data_display.index.map(
            lambda x: ITEMS_MANQUE_RECONNAISSANCE_LABELS.get(x, x) if x in ITEMS_MANQUE_RECONNAISSANCE_LABELS else "Total Manque Reconnaissance"
        )
        mr_data_display = mr_data_display[['Label', 'Moyenne', 'Écart-type', 'N']]
        
        st.dataframe(mr_data_display, use_container_width=True)
        
        means_mr = df_filtered[ITEMS_MANQUE_RECONNAISSANCE['items']].mean().sort_values(ascending=True)
        fig_mr_means = create_item_means_chart(
            means_mr,
            "Moyennes des items de Manque de Reconnaissance",
            ITEMS_MANQUE_RECONNAISSANCE_LABELS
        )
        st.plotly_chart(fig_mr_means, use_container_width=True, config=PLOTLY_CONFIG)
    
    with dimensions_tabs[3]:
        st.markdown("**Items de Gestion des Conflits**")
        gc_items = ITEMS_GESTION_CONFLITS['items'] + [ITEMS_GESTION_CONFLITS['total']]
        gc_data = moyennes_df.loc[moyennes_df.index.isin(gc_items)]
        
        gc_data_display = gc_data.copy()
        gc_data_display['Label'] = gc_data_display.index.map(
            lambda x: ITEMS_GESTION_CONFLITS_LABELS.get(x, x) if x in ITEMS_GESTION_CONFLITS_LABELS else "Total Gestion Conflits"
        )
        gc_data_display = gc_data_display[['Label', 'Moyenne', 'Écart-type', 'N']]
        
        st.dataframe(gc_data_display, use_container_width=True)
        
        means_gc = df_filtered[ITEMS_GESTION_CONFLITS['items']].mean().sort_values(ascending=True)
        fig_gc_means = create_item_means_chart(
            means_gc,
            "Moyennes des items de Gestion des Conflits",
            ITEMS_GESTION_CONFLITS_LABELS
        )
        st.plotly_chart(fig_gc_means, use_container_width=True, config=PLOTLY_CONFIG)
    
    with dimensions_tabs[4]:
        st.markdown("**Variables relationnelles**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Item5 (Durée relation)' in moyennes_df.index:
                st.metric(
                    "Durée moyenne de relation",
                    f"{moyennes_df.loc['Item5 (Durée relation)', 'Moyenne']:.1f} mois",
                    delta=f"σ = {moyennes_df.loc['Item5 (Durée relation)', 'Écart-type']:.1f}"
                )
        
        with col2:
            satisf_mean = df_filtered['Item7'].mean()
            st.metric(
                "Satisfaction moyenne",
                f"{satisf_mean:.2f} / 4",
                delta=f"σ = {df_filtered['Item7'].std():.2f}"
            )
        
        with col3:
            cohab_pct = (df_filtered['Item6'] == 1).sum() / len(df_filtered) * 100
            st.metric(
                "% Cohabitants",
                f"{cohab_pct:.1f}%"
            )
    
    st.markdown("---")
    
    # Export des données
    st.subheader("💾 Exporter les résultats")
    
    csv = moyennes_df.to_csv(index=True).encode('utf-8')
    st.download_button(
        label="📥 Télécharger le tableau complet (CSV)",
        data=csv,
        file_name=f"moyennes_analyse_{n_filtered}participants.csv",
        mime="text/csv"
    )

# ============================================================================
# TAB 3 : ESTIME DE SOI
# ============================================================================

with tab3:
    st.header("💙 Analyse de l'Estime de Soi")
    
    st.markdown(DESCRIPTION_DIMENSIONS['ES'])
    st.markdown("---")
    
    # Distribution du score total
    st.subheader("📊 Distribution du score total d'Estime de Soi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist_es = create_histogram(
            df_filtered,
            'Total ES',
            'Distribution du score d\'Estime de Soi',
            nbins=15
        )
        st.plotly_chart(fig_hist_es, use_container_width=True, config=PLOTLY_CONFIG)
    
    with col2:
        fig_box_es = create_box_plot(
            df_filtered,
            None,
            'Total ES',
            'Box plot du score d\'Estime de Soi',
            points='all'
        )
        st.plotly_chart(fig_box_es, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Comparaisons par groupes
    st.subheader("📊 Comparaisons par groupes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Par genre**")
        fig_es_genre = create_violin_plot(
            df_filtered,
            'Genre_label',
            'Total ES',
            'Estime de Soi selon le genre'
        )
        st.plotly_chart(fig_es_genre, use_container_width=True, config=PLOTLY_CONFIG)
    
    with col2:
        st.markdown("**Par âge**")
        fig_es_age = create_violin_plot(
            df_filtered,
            'Age_label',
            'Total ES',
            'Estime de Soi selon l\'âge'
        )
        st.plotly_chart(fig_es_age, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Par niveau d'études
    st.markdown("**Par niveau d'études**")
    fig_es_etude = create_box_plot(
        df_filtered,
        'Etude_label',
        'Total ES',
        'Estime de Soi selon le niveau d\'études'
    )
    st.plotly_chart(fig_es_etude, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Analyse item par item
    st.subheader("🔍 Analyse item par item")
    
    means_es = calculate_item_means(df_filtered, ITEMS_ESTIME_SOI)
    fig_items_es = create_item_means_chart(
        means_es,
        "Moyennes des items d'Estime de Soi",
        ITEMS_ESTIME_SOI_LABELS
    )
    st.plotly_chart(fig_items_es, use_container_width=True, config=PLOTLY_CONFIG)

# ============================================================================
# TAB 4 : VALORISATION
# ============================================================================

with tab4:
    st.header("💎 Analyse de la Valorisation dans la relation")
    
    st.markdown(DESCRIPTION_DIMENSIONS['Valorisation'])
    st.markdown("---")
    
    # Distribution
    st.subheader("📊 Distribution du score de Valorisation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist_valo = create_histogram(
            df_filtered,
            'Total valo',
            'Distribution du score de Valorisation',
            nbins=15
        )
        st.plotly_chart(fig_hist_valo, use_container_width=True, config=PLOTLY_CONFIG)
    
    with col2:
        fig_box_valo = create_box_plot(
            df_filtered,
            None,
            'Total valo',
            'Box plot du score de Valorisation',
            points='all'
        )
        st.plotly_chart(fig_box_valo, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Relation avec l'estime de soi
    st.subheader("🔗 Relation entre Valorisation et Estime de Soi")
    
    fig_scatter_valo_es = create_scatter_plot(
        df_filtered,
        'Total valo',
        'Total ES',
        'Corrélation Valorisation vs Estime de Soi',
        color='Satisfaction_label' if 'Satisfaction_label' in df_filtered.columns else None,
        trendline='ols'
    )
    st.plotly_chart(fig_scatter_valo_es, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Par satisfaction relationnelle
    st.subheader("😊 Valorisation selon la satisfaction relationnelle")
    
    fig_valo_satisf = create_violin_plot(
        df_filtered,
        'Item7_label',
        'Total valo',
        'Valorisation selon le niveau de satisfaction'
    )
    st.plotly_chart(fig_valo_satisf, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Analyse item par item
    st.subheader("🔍 Analyse item par item")
    
    means_valo = calculate_item_means(df_filtered, ITEMS_VALORISATION)
    fig_items_valo = create_item_means_chart(
        means_valo,
        "Moyennes des items de Valorisation",
        ITEMS_VALORISATION_LABELS
    )
    st.plotly_chart(fig_items_valo, use_container_width=True, config=PLOTLY_CONFIG)

# ============================================================================
# TAB 5 : MANQUE DE RECONNAISSANCE
# ============================================================================

with tab5:
    st.header("⚠️ Analyse du Manque de Reconnaissance")
    
    st.markdown(DESCRIPTION_DIMENSIONS['MR'])
    st.markdown("---")
    
    # Distribution
    st.subheader("📊 Distribution du score de Manque de Reconnaissance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist_mr = create_histogram(
            df_filtered,
            'Total MR',
            'Distribution du score de Manque de Reconnaissance',
            nbins=15
        )
        st.plotly_chart(fig_hist_mr, use_container_width=True, config=PLOTLY_CONFIG)
    
    with col2:
        fig_box_mr = create_box_plot(
            df_filtered,
            None,
            'Total MR',
            'Box plot du score de Manque de Reconnaissance',
            points='all'
        )
        st.plotly_chart(fig_box_mr, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Relation avec l'estime de soi
    st.subheader("🔗 Relation entre Manque de Reconnaissance et Estime de Soi")
    
    fig_scatter_mr_es = create_scatter_plot(
        df_filtered,
        'Total MR',
        'Total ES',
        'Corrélation Manque de Reconnaissance vs Estime de Soi',
        color='Genre_label',
        trendline='ols'
    )
    st.plotly_chart(fig_scatter_mr_es, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Par cohabitation
    st.subheader("🏠 Manque de Reconnaissance selon la cohabitation")
    
    fig_mr_cohab = create_violin_plot(
        df_filtered,
        'Item6_label',
        'Total MR',
        'Manque de Reconnaissance selon la cohabitation'
    )
    st.plotly_chart(fig_mr_cohab, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Analyse item par item
    st.subheader("🔍 Analyse item par item")
    
    means_mr = calculate_item_means(df_filtered, ITEMS_MANQUE_RECONNAISSANCE)
    fig_items_mr = create_item_means_chart(
        means_mr,
        "Moyennes des items de Manque de Reconnaissance",
        ITEMS_MANQUE_RECONNAISSANCE_LABELS
    )
    st.plotly_chart(fig_items_mr, use_container_width=True, config=PLOTLY_CONFIG)

# ============================================================================
# TAB 6 : GESTION DES CONFLITS
# ============================================================================

with tab6:
    st.header("🤝 Analyse de la Gestion des Conflits")
    
    st.markdown(DESCRIPTION_DIMENSIONS['GC'])
    st.markdown("---")
    
    # Distribution
    st.subheader("📊 Distribution du score de Gestion des Conflits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist_gc = create_histogram(
            df_filtered,
            'Total GC',
            'Distribution du score de Gestion des Conflits',
            nbins=15
        )
        st.plotly_chart(fig_hist_gc, use_container_width=True, config=PLOTLY_CONFIG)
    
    with col2:
        fig_box_gc = create_box_plot(
            df_filtered,
            None,
            'Total GC',
            'Box plot du score de Gestion des Conflits',
            points='all'
        )
        st.plotly_chart(fig_box_gc, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Relation avec l'estime de soi
    st.subheader("🔗 Relation entre Gestion des Conflits et Estime de Soi")
    
    fig_scatter_gc_es = create_scatter_plot(
        df_filtered,
        'Total GC',
        'Total ES',
        'Corrélation Gestion des Conflits vs Estime de Soi',
        color='Item7_label',
        trendline='ols'
    )
    st.plotly_chart(fig_scatter_gc_es, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Par satisfaction
    st.subheader("😊 Gestion des Conflits selon la satisfaction")
    
    fig_gc_satisf = create_violin_plot(
        df_filtered,
        'Item7_label',
        'Total GC',
        'Gestion des Conflits selon la satisfaction relationnelle'
    )
    st.plotly_chart(fig_gc_satisf, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Analyse item par item
    st.subheader("🔍 Analyse item par item")
    
    means_gc = calculate_item_means(df_filtered, ITEMS_GESTION_CONFLITS)
    fig_items_gc = create_item_means_chart(
        means_gc,
        "Moyennes des items de Gestion des Conflits",
        ITEMS_GESTION_CONFLITS_LABELS
    )
    st.plotly_chart(fig_items_gc, use_container_width=True, config=PLOTLY_CONFIG)

# ============================================================================
# TAB 7 : ANALYSES CROISÉES
# ============================================================================

with tab7:
    st.header("🔗 Analyses Croisées et Multivariées")
    
    # Matrice de corrélation détaillée
    st.subheader("📊 Matrice de corrélation complète")
    
    corr_matrix = get_correlation_matrix(df_filtered)
    fig_corr = create_correlation_heatmap(corr_matrix)
    st.plotly_chart(fig_corr, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Scatter matrix
    st.subheader("🎯 Matrice de scatter plots")
    
    fig_scatter_matrix = create_multi_scatter_matrix(
        df_filtered,
        ['Total ES', 'Total valo', 'Total MR', 'Total GC'],
        'Genre_label',
        'Relations entre toutes les dimensions'
    )
    st.plotly_chart(fig_scatter_matrix, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Coordonnées parallèles
    st.subheader("📈 Coordonnées parallèles")
    
    fig_parallel = create_parallel_coordinates(
        df_filtered,
        ['Total ES', 'Total valo', 'Total MR', 'Total GC'],
        'Total ES',
        'Profils multidimensionnels des participants'
    )
    st.plotly_chart(fig_parallel, use_container_width=True, config=PLOTLY_CONFIG)
    
    # Comparaisons par groupes
    st.subheader("👥 Comparaisons par groupes sociodémographiques")
    
    # Choisir la variable de groupement
    group_var = st.selectbox(
        "Sélectionner la variable de groupement",
        options=['Genre_label', 'Age_label', 'Etude_label', 'Item6_label', 'Item7_label'],
        format_func=lambda x: {
            'Genre_label': 'Genre',
            'Age_label': 'Âge',
            'Etude_label': 'Niveau d\'études',
            'Item6_label': 'Cohabitation',
            'Item7_label': 'Satisfaction'
        }[x]
    )
    
    # Calculer les moyennes par groupe
    grouped_means = df_filtered.groupby(group_var)[
        ['Total ES', 'Total valo', 'Total MR', 'Total GC']
    ].mean().reset_index()
    
    # Graphique en barres groupées
    fig_grouped = go.Figure()
    
    dimensions = ['Total ES', 'Total valo', 'Total MR', 'Total GC']
    dim_names = ['Estime de Soi', 'Valorisation', 'Manque Recon.', 'Gestion Conflits']
    
    for dim, name in zip(dimensions, dim_names):
        fig_grouped.add_trace(go.Bar(
            name=name,
            x=grouped_means[group_var],
            y=grouped_means[dim]
        ))
    
    fig_grouped.update_layout(
        title=f"Scores moyens par {group_var.replace('_label', '')}",
        barmode='group',
        template=PLOTLY_LAYOUT_TEMPLATE,
        height=500,
        xaxis_title="",
        yaxis_title="Score moyen"
    )
    
    st.plotly_chart(fig_grouped, use_container_width=True, config=PLOTLY_CONFIG)

# ============================================================================
# TAB 8 : STATISTIQUES
# ============================================================================

with tab8:
    st.header("📈 Statistiques Descriptives Détaillées")
    
    # Statistiques par dimension
    st.subheader("📊 Statistiques par dimension")
    
    dim_stats = calculate_dimension_stats(df_filtered)
    st.dataframe(dim_stats, use_container_width=True)
    
    # Statistiques des items
    st.subheader("🔍 Statistiques des items par dimension")
    
    stat_tabs = st.tabs(["Estime de Soi", "Valorisation", "Manque Reconnaissance", "Gestion Conflits"])
    
    with stat_tabs[0]:
        es_stats = get_item_statistics(df_filtered, ITEMS_ESTIME_SOI['items'])
        st.dataframe(es_stats, use_container_width=True)
    
    with stat_tabs[1]:
        valo_stats = get_item_statistics(df_filtered, ITEMS_VALORISATION['items'])
        st.dataframe(valo_stats, use_container_width=True)
    
    with stat_tabs[2]:
        mr_stats = get_item_statistics(df_filtered, ITEMS_MANQUE_RECONNAISSANCE['items'])
        st.dataframe(mr_stats, use_container_width=True)
    
    with stat_tabs[3]:
        gc_stats = get_item_statistics(df_filtered, ITEMS_GESTION_CONFLITS['items'])
        st.dataframe(gc_stats, use_container_width=True)
    
    # Statistiques groupées
    st.subheader("📊 Comparaisons statistiques par groupes")
    
    compare_var = st.selectbox(
        "Comparer les dimensions selon:",
        options=['Genre', 'Age', 'Etude', 'Item6', 'Item7'],
        format_func=lambda x: {
            'Genre': 'Genre',
            'Age': 'Âge',
            'Etude': 'Niveau d\'études',
            'Item6': 'Cohabitation',
            'Item7': 'Satisfaction'
        }[x],
        key='compare_stat'
    )
    
    grouped_stats = get_grouped_statistics(
        df_filtered,
        compare_var,
        ['Total ES', 'Total valo', 'Total MR', 'Total GC']
    )
    
    st.dataframe(grouped_stats, use_container_width=True)
    
    # Résumé démographique
    st.subheader("👥 Résumé de l'échantillon")
    
    demo_summary = get_demographic_summary(df_filtered)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Répartition par âge**")
        for age, count in demo_summary['age_distribution'].items():
            st.write(f"- {age}: {count} ({count/demo_summary['total_participants']*100:.1f}%)")
    
    with col2:
        st.markdown("**Répartition par genre**")
        for genre, count in demo_summary['genre_distribution'].items():
            st.write(f"- {genre}: {count} ({count/demo_summary['total_participants']*100:.1f}%)")
    
    with col3:
        st.markdown("**Caractéristiques relationnelles**")
        if demo_summary['duree_moyenne']:
            st.write(f"- Durée moyenne: {demo_summary['duree_moyenne']:.1f} mois")
        for sit, count in demo_summary['cohabitation_distribution'].items():
            st.write(f"- {sit}: {count}")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    💕 Application d'analyse - Relations amoureuses et estime de soi<br>
    Mini-mémoire de Licence de Psychologie | 2024-2025
</div>
""", unsafe_allow_html=True)