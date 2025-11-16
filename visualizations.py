"""
Module de visualisations avec Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from config import *


def create_bar_chart(data, x, y, title, color=None, labels=None, orientation='v'):
    """
    Crée un graphique en barres
    """
    fig = px.bar(
        data, 
        x=x, 
        y=y, 
        title=title,
        color=color,
        labels=labels,
        orientation=orientation,
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_layout(
        showlegend=True if color else False,
        height=400
    )
    
    return fig


def create_histogram(data, column, title, nbins=20, color=None):
    """
    Crée un histogramme
    """
    fig = px.histogram(
        data,
        x=column,
        title=title,
        nbins=nbins,
        color=color,
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_layout(
        showlegend=True if color else False,
        height=400
    )
    
    return fig


def create_box_plot(data, x, y, title, color=None, points='all'):
    """
    Crée un box plot
    """
    fig = px.box(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        points=points,
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_layout(
        height=450
    )
    
    return fig


def create_violin_plot(data, x, y, title, color=None, box=True):
    """
    Crée un violin plot
    """
    fig = px.violin(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        box=box,
        points='all',
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_layout(
        height=450
    )
    
    return fig


def create_scatter_plot(data, x, y, title, color=None, size=None, hover_data=None, trendline=None):
    """
    Crée un scatter plot
    """
    fig = px.scatter(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        size=size,
        hover_data=hover_data,
        trendline=trendline,
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_layout(
        height=500
    )
    
    return fig


def create_correlation_heatmap(corr_matrix, title="Matrice de Corrélation"):
    """
    Crée une heatmap de corrélation
    """
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title="Corrélation")
    ))
    
    fig.update_layout(
        title=title,
        template=PLOTLY_LAYOUT_TEMPLATE,
        height=500,
        xaxis_title="",
        yaxis_title=""
    )
    
    return fig


def create_grouped_bar_chart(data, x, y_cols, title, labels=None):
    """
    Crée un graphique en barres groupées
    """
    fig = go.Figure()
    
    for col in y_cols:
        fig.add_trace(go.Bar(
            x=data[x],
            y=data[col],
            name=col
        ))
    
    fig.update_layout(
        title=title,
        barmode='group',
        template=PLOTLY_LAYOUT_TEMPLATE,
        height=450,
        xaxis_title=labels.get(x, x) if labels else x,
        yaxis_title="Score moyen"
    )
    
    return fig


def create_radar_chart(data, categories, values, title, name="Score"):
    """
    Crée un radar chart
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=name
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.1]
            )
        ),
        title=title,
        template=PLOTLY_LAYOUT_TEMPLATE,
        height=500
    )
    
    return fig


def create_sunburst(data, path, values, title):
    """
    Crée un sunburst chart
    """
    fig = px.sunburst(
        data,
        path=path,
        values=values,
        title=title,
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_layout(
        height=550
    )
    
    return fig


def create_distribution_comparison(data, column, group_by, title):
    """
    Compare les distributions d'une variable selon un groupement
    """
    fig = px.histogram(
        data,
        x=column,
        color=group_by,
        barmode='overlay',
        title=title,
        opacity=0.7,
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_layout(
        height=450
    )
    
    return fig


def create_item_means_chart(means_series, title, item_labels=None):
    """
    Crée un graphique des moyennes des items
    """
    if item_labels:
        labels = [item_labels.get(item, item) for item in means_series.index]
    else:
        labels = means_series.index
    
    fig = go.Figure(go.Bar(
        x=means_series.values,
        y=labels,
        orientation='h',
        marker=dict(
            color=means_series.values,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Moyenne")
        ),
        text=means_series.values.round(2),
        textposition='auto'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Moyenne",
        yaxis_title="",
        template=PLOTLY_LAYOUT_TEMPLATE,
        height=max(400, len(means_series) * 40)
    )
    
    return fig


def create_kpi_cards_data(df):
    """
    Prépare les données pour les KPI cards
    """
    kpis = {
        'N Participants': len(df),
        'Estime de Soi (moy)': df['Total ES'].mean(),
        'Valorisation (moy)': df['Total valo'].mean(),
        'Manque Reconnaissance (moy)': df['Total MR'].mean(),
        'Gestion Conflits (moy)': df['Total GC'].mean(),
        'Durée relation (moy)': df['Item5'].mean() if 'Item5' in df.columns else None
    }
    
    return kpis


def create_parallel_coordinates(data, dimensions, color_col, title):
    """
    Crée un graphique de coordonnées parallèles
    """
    fig = px.parallel_coordinates(
        data,
        dimensions=dimensions,
        color=color_col,
        title=title,
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_layout(
        height=500
    )
    
    return fig


def create_line_chart(data, x, y, title, markers=True, color=None):
    """
    Crée un graphique en ligne
    """
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        markers=markers,
        color=color,
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_layout(
        height=400
    )
    
    return fig


def create_stacked_bar(data, x, y_cols, title):
    """
    Crée un graphique en barres empilées
    """
    fig = go.Figure()
    
    for col in y_cols:
        fig.add_trace(go.Bar(
            name=col,
            x=data[x],
            y=data[col]
        ))
    
    fig.update_layout(
        title=title,
        barmode='stack',
        template=PLOTLY_LAYOUT_TEMPLATE,
        height=450
    )
    
    return fig


def create_pie_chart(data, names, values, title):
    """
    Crée un graphique en camembert
    """
    fig = px.pie(
        data,
        names=names,
        values=values,
        title=title,
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )
    
    fig.update_layout(
        height=400
    )
    
    return fig


def create_multi_scatter_matrix(data, dimensions, color, title):
    """
    Crée une matrice de scatter plots
    """
    fig = px.scatter_matrix(
        data,
        dimensions=dimensions,
        color=color,
        title=title,
        template=PLOTLY_LAYOUT_TEMPLATE
    )
    
    fig.update_layout(
        height=800
    )
    
    return fig


def create_comparison_table_figure(grouped_stats, title):
    """
    Crée un tableau de comparaison sous forme de figure Plotly
    """
    # Réinitialiser l'index pour avoir les groupes en colonne
    table_data = grouped_stats.reset_index()
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(table_data.columns),
            fill_color='paleturquoise',
            align='left',
            font=dict(size=12, color='black')
        ),
        cells=dict(
            values=[table_data[col] for col in table_data.columns],
            fill_color='lavender',
            align='left',
            font=dict(size=11)
        )
    )])
    
    fig.update_layout(
        title=title,
        height=min(400, 100 + len(table_data) * 30)
    )
    
    return fig


def create_dimension_overview(df):
    """
    Crée un graphique de vue d'ensemble des 4 dimensions
    """
    dimensions = ['Estime de Soi', 'Valorisation', 'Manque Reconnaissance', 'Gestion Conflits']
    totals = ['Total ES', 'Total valo', 'Total MR', 'Total GC']
    colors_list = [COLORS_DIMENSIONS['ES'], COLORS_DIMENSIONS['Valorisation'], 
                   COLORS_DIMENSIONS['MR'], COLORS_DIMENSIONS['GC']]
    
    means = [df[col].mean() for col in totals]
    stds = [df[col].std() for col in totals]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=dimensions,
        y=means,
        error_y=dict(type='data', array=stds),
        marker=dict(color=colors_list),
        text=[f"{m:.1f}" for m in means],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Vue d'ensemble des scores moyens par dimension",
        xaxis_title="Dimension",
        yaxis_title="Score moyen",
        template=PLOTLY_LAYOUT_TEMPLATE,
        height=450,
        showlegend=False
    )
    
    return fig