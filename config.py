"""
Configuration et mappings pour l'application d'analyse des relations amoureuses
"""

# ============================================================================
# MAPPINGS DES VARIABLES CATÉGORIELLES
# ============================================================================

AGE_LABELS = {
    1: "18-20 ans",
    2: "20-25 ans"
}

GENRE_LABELS = {
    1: "Femme",
    2: "Homme",
    3: "Autre"
}

ETUDE_LABELS = {
    1: "Lycée",
    2: "Licence 1",
    3: "Licence 2",
    4: "Licence 3",
    5: "Master ou plus"
}

SITUATION_LABELS = {
    1: "En couple",
    2: "Autre"
}

COHABITATION_LABELS = {
    1: "Oui",
    2: "Non"
}

SATISFACTION_LABELS = {
    1: "Très insatisfaisante",
    2: "Plutôt insatisfaisante",
    3: "Plutôt satisfaisante",
    4: "Très satisfaisante"
}

# Échelle de Likert 5 points (pour Items 8-17 et autres items psychométriques)
LIKERT_5_LABELS = {
    1: "Pas du tout d'accord",
    2: "Plutôt pas d'accord",
    3: "Ni d'accord ni en désaccord",
    4: "Plutôt d'accord",
    5: "Tout à fait d'accord"
}

# Échelle de Likert 4 points (pour Item 7 - Satisfaction)
LIKERT_4_LABELS = {
    1: "Tout à fait en désaccord",
    2: "Plutôt en désaccord",
    3: "Plutôt en accord",
    4: "Tout à fait en accord"
}

# ============================================================================
# STRUCTURE DES ITEMS PAR DIMENSION
# ============================================================================

# Estime de Soi (Échelle de Rosenberg)
ITEMS_ESTIME_SOI = {
    'items': ['Item 8', 'Item 9', 'Item 10', 'Item 11', 'Item 12', 
              'Item 13', 'Item 14', 'Item 15', 'Item 16', 'Item 17'],
    'total': 'Total ES',
    'description': 'Estime de Soi (Rosenberg)',
    'short_name': 'ES'
}

ITEMS_ESTIME_SOI_LABELS = {
    'Item 8': "Je pense que je suis une personne de valeur",
    'Item 9': "Je possède un certain nombre de belles qualités",
    'Item 10': "Je me considère comme un(e) raté(e) (inversé)",
    'Item 11': "Je suis capable de faire les choses aussi bien que les autres",
    'Item 12': "Peu de raisons d'être fier(ère) de moi (inversé)",
    'Item 13': "J'ai une attitude positive vis-à-vis de moi-même",
    'Item 14': "Je suis satisfait(e) de moi",
    'Item 15': "J'aimerais avoir plus de respect pour moi-même (inversé)",
    'Item 16': "Je me sens vraiment inutile (inversé)",
    'Item 17': "Je suis un(e) bon(ne) à rien (inversé)"
}

# Valorisation dans la relation
ITEMS_VALORISATION = {
    'items': ['Item 18', 'Item 19', 'Item 20', 'Item21', 'Item 22'],
    'total': 'Total valo',
    'description': 'Valorisation dans la relation',
    'short_name': 'Valorisation'
}

ITEMS_VALORISATION_LABELS = {
    'Item 18': "Mon/ma partenaire me fait sentir que j'ai de la valeur",
    'Item 19': "Je me sens apprécié(e) pour ce que je suis",
    'Item 20': "Mon/ma partenaire reconnaît mes efforts et qualités",
    'Item21': "Mon/ma partenaire m'encourage à être moi-même",
    'Item 22': "Être avec mon/ma partenaire renforce ma confiance"
}

# Manque de Reconnaissance
ITEMS_MANQUE_RECONNAISSANCE = {
    'items': ['Item 23', 'Item 24', 'Item 25', 'Item 26', 'Item 27', 'Item 28'],
    'total': 'Total MR',
    'description': 'Manque de Reconnaissance',
    'short_name': 'MR'
}

ITEMS_MANQUE_RECONNAISSANCE_LABELS = {
    'Item 23': "Je me sens parfois mis(e) de côté ou peu écouté(e)",
    'Item 24': "Mon/ma partenaire ne remarque pas ce que je fais",
    'Item 25': "Je me sens parfois négligé(e) ou peu considéré(e)",
    'Item 26': "Mon/ma partenaire me critique plus qu'il/elle ne me valorise",
    'Item 27': "Le comportement de mon/ma partenaire me fait douter",
    'Item 28': "Je ressens un déséquilibre entre ce que je donne et reçois"
}

# Gestion des Conflits
ITEMS_GESTION_CONFLITS = {
    'items': ['Item 29', 'Item 30', 'Item 31', 'Item 32', 'Item 33', 'Item 34'],
    'total': 'Total GC',
    'description': 'Gestion des Conflits',
    'short_name': 'GC'
}

ITEMS_GESTION_CONFLITS_LABELS = {
    'Item 29': "Lors de nos désaccords, nous communiquons sans nous blesser",
    'Item 30': "Après un conflit, je me sens respecté(e) et compris(e)",
    'Item 31': "Les disputes me font parfois douter de moi-même (inversé)",
    'Item 32': "Nos désaccords nous aident à mieux nous comprendre",
    'Item 33': "Mon/ma partenaire cherche plus à avoir raison (inversé)",
    'Item 34': "Nos désaccords me donnent le sentiment d'être incompris(e) (inversé)"
}

# Variables relationnelles (Items 4-7)
ITEMS_RELATIONNELS = {
    'Item4': 'Situation actuelle',
    'Item5': 'Durée de la relation (mois)',
    'Item6': 'Cohabitation',
    'Item7': 'Satisfaction relationnelle'
}

# ============================================================================
# VARIABLES POUR FILTRES
# ============================================================================

VARIABLES_SOCIODEMOGRAPHIQUES = {
    'Age': {'label': 'Âge', 'mapping': AGE_LABELS},
    'Genre': {'label': 'Genre', 'mapping': GENRE_LABELS},
    'Etude': {'label': 'Niveau d\'études', 'mapping': ETUDE_LABELS}
}

VARIABLES_RELATIONNELLES_FILTRES = {
    'Item4': {'label': 'Situation actuelle', 'mapping': SITUATION_LABELS},
    'Item6': {'label': 'Cohabitation', 'mapping': COHABITATION_LABELS},
    'Item7': {'label': 'Satisfaction relationnelle', 'mapping': SATISFACTION_LABELS}
}

# ============================================================================
# COULEURS ET STYLE
# ============================================================================

COLOR_PALETTE = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff9800',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

COLORS_DIMENSIONS = {
    'ES': '#1f77b4',      # Bleu
    'Valorisation': '#2ca02c',  # Vert
    'MR': '#d62728',      # Rouge
    'GC': '#ff7f0e'       # Orange
}

COLORS_GENRE = {
    'Femme': '#e377c2',
    'Homme': '#17becf',
    'Autre': '#bcbd22'
}

COLORS_AGE = {
    '18-20 ans': '#9467bd',
    '20-25 ans': '#8c564b'
}

# ============================================================================
# PARAMÈTRES PLOTLY
# ============================================================================

PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'graph',
        'height': 800,
        'width': 1200,
        'scale': 2
    }
}

PLOTLY_LAYOUT_TEMPLATE = 'plotly_white'

# ============================================================================
# TEXTES ET DESCRIPTIONS
# ============================================================================

APP_TITLE = "📊 Analyse des Relations Amoureuses et Estime de Soi"
APP_SUBTITLE = "Mini-mémoire de Licence de Psychologie"

DESCRIPTION_DIMENSIONS = {
    'ES': """
    **Échelle d'Estime de Soi de Rosenberg**
    
    Mesure l'évaluation globale qu'une personne fait d'elle-même.
    Score de 10 à 40 (10 items). Plus le score est élevé, plus l'estime de soi est positive.
    """,
    
    'Valorisation': """
    **Valorisation dans la relation**
    
    Évalue dans quelle mesure la personne se sent valorisée et appréciée par son/sa partenaire.
    Score de 5 à 25 (5 items). Plus le score est élevé, plus la valorisation est forte.
    """,
    
    'MR': """
    **Manque de Reconnaissance**
    
    Mesure les sentiments de négligence ou de manque de considération dans la relation.
    Score de 6 à 30 (6 items). Plus le score est élevé, plus le manque de reconnaissance est important.
    """,
    
    'GC': """
    **Gestion des Conflits**
    
    Évalue la qualité de la communication et de la résolution des désaccords dans le couple.
    Score de 6 à 30 (6 items). Plus le score est élevé, meilleure est la gestion des conflits.
    """
}