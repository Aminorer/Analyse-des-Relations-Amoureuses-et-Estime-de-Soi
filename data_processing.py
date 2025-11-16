"""
Module de chargement et traitement des données
"""

import pandas as pd
import streamlit as st
from config import *

@st.cache_data
def load_data(file_path):
    """
    Charge les données depuis le fichier Excel avec mise en cache
    
    Args:
        file_path: Chemin vers le fichier Excel
        
    Returns:
        DataFrame pandas avec les données nettoyées
    """
    # Charger avec la deuxième ligne comme header
    df = pd.read_excel(file_path, header=1)
    
    # Nettoyer les noms de colonnes (enlever les espaces superflus)
    df.columns = df.columns.str.strip()
    
    return df


@st.cache_data
def apply_labels(df):
    """
    Applique les labels textuels aux variables catégorielles
    
    Args:
        df: DataFrame original
        
    Returns:
        DataFrame avec colonnes labellisées ajoutées
    """
    df_labeled = df.copy()
    
    # Appliquer les mappings
    df_labeled['Age_label'] = df_labeled['Age'].map(AGE_LABELS)
    df_labeled['Genre_label'] = df_labeled['Genre'].map(GENRE_LABELS)
    df_labeled['Etude_label'] = df_labeled['Etude'].map(ETUDE_LABELS)
    df_labeled['Item4_label'] = df_labeled['Item4'].map(SITUATION_LABELS)
    df_labeled['Item6_label'] = df_labeled['Item6'].map(COHABITATION_LABELS)
    df_labeled['Item7_label'] = df_labeled['Item7'].map(SATISFACTION_LABELS)
    
    return df_labeled


def filter_data(df, filters):
    """
    Applique les filtres sélectionnés par l'utilisateur
    
    Args:
        df: DataFrame à filtrer
        filters: Dictionnaire de filtres {colonne: [valeurs]}
        
    Returns:
        DataFrame filtré
    """
    df_filtered = df.copy()
    
    for col, values in filters.items():
        if values and len(values) > 0:
            df_filtered = df_filtered[df_filtered[col].isin(values)]
    
    return df_filtered


@st.cache_data
def get_item_statistics(df, items_list):
    """
    Calcule les statistiques descriptives pour une liste d'items
    
    Args:
        df: DataFrame
        items_list: Liste des noms de colonnes (items)
        
    Returns:
        DataFrame avec statistiques
    """
    stats = df[items_list].describe().T
    stats['median'] = df[items_list].median()
    stats = stats[['mean', 'median', 'std', 'min', 'max', 'count']]
    stats.columns = ['Moyenne', 'Médiane', 'Écart-type', 'Min', 'Max', 'N']
    
    return stats


@st.cache_data
def calculate_dimension_stats(df):
    """
    Calcule les statistiques pour toutes les dimensions (ES, Valorisation, MR, GC)
    
    Args:
        df: DataFrame
        
    Returns:
        DataFrame avec statistiques par dimension
    """
    dimensions = {
        'Estime de Soi': ITEMS_ESTIME_SOI,
        'Valorisation': ITEMS_VALORISATION,
        'Manque de Reconnaissance': ITEMS_MANQUE_RECONNAISSANCE,
        'Gestion des Conflits': ITEMS_GESTION_CONFLITS
    }
    
    results = []
    
    for dim_name, dim_config in dimensions.items():
        total_col = dim_config['total']
        items_cols = dim_config['items']
        
        # Stats du total
        total_stats = {
            'Dimension': dim_name,
            'Type': 'Score Total',
            'Moyenne': df[total_col].mean(),
            'Médiane': df[total_col].median(),
            'Écart-type': df[total_col].std(),
            'Min': df[total_col].min(),
            'Max': df[total_col].max(),
            'N': df[total_col].count()
        }
        results.append(total_stats)
        
        # Stats moyennes des items
        item_means = df[items_cols].mean(axis=1).mean()
        item_std = df[items_cols].mean(axis=1).std()
        
        item_stats = {
            'Dimension': dim_name,
            'Type': 'Moyenne des Items',
            'Moyenne': item_means,
            'Médiane': df[items_cols].mean(axis=1).median(),
            'Écart-type': item_std,
            'Min': df[items_cols].mean(axis=1).min(),
            'Max': df[items_cols].mean(axis=1).max(),
            'N': df[items_cols].count().min()
        }
        results.append(item_stats)
    
    return pd.DataFrame(results)


@st.cache_data
def get_correlation_matrix(df):
    """
    Calcule la matrice de corrélation entre les scores totaux
    
    Args:
        df: DataFrame
        
    Returns:
        Matrice de corrélation
    """
    total_cols = ['Total ES', 'Total valo', 'Total MR', 'Total GC']
    corr_matrix = df[total_cols].corr()
    
    # Renommer pour plus de clarté
    corr_matrix.columns = ['Estime de Soi', 'Valorisation', 'Manque Reconnaissance', 'Gestion Conflits']
    corr_matrix.index = ['Estime de Soi', 'Valorisation', 'Manque Reconnaissance', 'Gestion Conflits']
    
    return corr_matrix


def get_grouped_statistics(df, group_by_col, value_cols):
    """
    Calcule les statistiques groupées par une variable catégorielle
    
    Args:
        df: DataFrame
        group_by_col: Colonne de regroupement
        value_cols: Colonnes de valeurs à analyser
        
    Returns:
        DataFrame avec statistiques groupées
    """
    # Grouper et calculer les moyennes
    grouped = df.groupby(group_by_col)[value_cols].agg(['mean', 'std', 'count']).round(2)
    
    return grouped


@st.cache_data
def calculate_item_means(df, items_config):
    """
    Calcule la moyenne de chaque item d'une dimension
    
    Args:
        df: DataFrame
        items_config: Configuration de la dimension (dict avec 'items' et 'total')
        
    Returns:
        Series avec les moyennes
    """
    items = items_config['items']
    means = df[items].mean().sort_values(ascending=False)
    
    return means


def get_demographic_summary(df):
    """
    Résumé des caractéristiques démographiques
    
    Args:
        df: DataFrame
        
    Returns:
        Dict avec les résumés
    """
    summary = {
        'total_participants': len(df),
        'age_distribution': df['Age_label'].value_counts().to_dict(),
        'genre_distribution': df['Genre_label'].value_counts().to_dict(),
        'etude_distribution': df['Etude_label'].value_counts().to_dict(),
        'situation_distribution': df['Item4_label'].value_counts().to_dict(),
        'cohabitation_distribution': df['Item6_label'].value_counts().to_dict(),
        'duree_moyenne': df['Item5'].mean() if 'Item5' in df.columns else None
    }
    
    return summary


@st.cache_data  
def get_satisfaction_groups(df):
    """
    Groupe les participants selon leur niveau de satisfaction relationnelle
    
    Args:
        df: DataFrame
        
    Returns:
        DataFrame avec groupes de satisfaction
    """
    # Créer des groupes de satisfaction
    df_copy = df.copy()
    df_copy['Satisfaction_group'] = df_copy['Item7'].map({
        1: 'Insatisfait',
        2: 'Insatisfait', 
        3: 'Satisfait',
        4: 'Satisfait'
    })
    
    return df_copy


def calculate_averages_by_filters(df):
    """
    Calcule les moyennes de tous les items et totaux pour l'ensemble filtré
    
    Args:
        df: DataFrame (potentiellement filtré)
        
    Returns:
        DataFrame avec toutes les moyennes
    """
    # Colonnes à calculer
    all_items = (
        ITEMS_ESTIME_SOI['items'] + 
        ITEMS_VALORISATION['items'] + 
        ITEMS_MANQUE_RECONNAISSANCE['items'] + 
        ITEMS_GESTION_CONFLITS['items']
    )
    
    totals = ['Total ES', 'Total valo', 'Total MR', 'Total GC']
    
    # Calculer les moyennes
    means_dict = {}
    
    # Items individuels
    for item in all_items:
        if item in df.columns:
            means_dict[item] = {
                'Moyenne': df[item].mean(),
                'Écart-type': df[item].std(),
                'N': df[item].count()
            }
    
    # Totaux
    for total in totals:
        if total in df.columns:
            means_dict[total] = {
                'Moyenne': df[total].mean(),
                'Écart-type': df[total].std(),
                'N': df[total].count()
            }
    
    # Variables relationnelles numériques
    if 'Item5' in df.columns:  # Durée de relation
        means_dict['Item5 (Durée relation)'] = {
            'Moyenne': df['Item5'].mean(),
            'Écart-type': df['Item5'].std(),
            'N': df['Item5'].count()
        }
    
    # Convertir en DataFrame
    results_df = pd.DataFrame(means_dict).T
    results_df = results_df.round(2)
    results_df.index.name = 'Variable'
    
    return results_df