import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# Import des nouveaux modules
from src.loader import DataLoader
from src.cleaning import DataCleaner
from src.stats import StatisticsCalculator
from src.generators import GridGenerator
from src.insights import InsightsCalculator
from src.utils import Utils

# Configuration de la page
st.set_page_config(
    page_title="EuroMillions - Analyse statistique",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("EuroMillions - Analyse statistique et exploration")

# ================================
# SECTION À SAVOIR - DISCLAIMER
# ================================
st.header("À savoir avant de commencer")

disclaimer_col1, disclaimer_col2 = st.columns([2, 1])

with disclaimer_col1:
    st.info("""
    **Avertissement important sur les tirages EuroMillions**

    Les tirages EuroMillions sont **indépendants**. Chaque tirage est le résultat d'un processus aléatoire où :
    - Les numéros déjà sortis plus souvent n'ont **pas plus de chances** d'être tirés au prochain tour
    - Les statistiques affichées ici servent uniquement à **analyser l'historique**
    - Elles ne permettent **pas de prédire** de manière fiable les tirages futurs
    - Le générateur pondéré est une **fonctionnalité exploratoire/ludique**, pas un outil d'optimisation

    **Rappel des probabilités théoriques :**
    - Chance de gagner le jackpot : 1 chance sur 139 838 160
    - Chance de gagner un numéro : 5/50 = 10%
    - Chance de gagner une étoile : 2/12 ≈ 16.67%
    """)

with disclaimer_col2:
    st.markdown("""
    **Objectif de cette application**
    - Explorer les données historiques
    - Comprendre les fréquences observées
    - Générer des grilles aléatoirement
    - Apprendre sur les probabilités

    **Méthodologie**
    - Analyse descriptive uniquement
    - Pas de prédiction statistique
    - Focus sur l'observation des patterns
    """)

st.markdown("---")

# ================================
# CHARGEMENT ET PRÉPARATION DES DONNÉES
# ================================
@st.cache_data
def load_and_prepare_data():
    """Charge et prépare les données avec la nouvelle architecture"""
    try:
        # Chargement
        loader = DataLoader("data/resultat_trie.json")
        raw_data = loader.load()

        # Nettoyage
        cleaner = DataCleaner(raw_data)
        df = cleaner.clean_and_normalize()

        # Statistiques
        stats_calc = StatisticsCalculator(df)

        # Insights
        insights_calc = InsightsCalculator(stats_calc)

        # Générateur
        generator = GridGenerator(stats_calc.number_freq, stats_calc.star_freq)

        return {
            'df': df,
            'stats': stats_calc,
            'insights': insights_calc,
            'generator': generator
        }

    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return None

data = load_and_prepare_data()
if data is None:
    st.stop()

df = data['df']
stats_calc = data['stats']
insights_calc = data['insights']
generator = data['generator']

# ================================
# SIDEBAR - FILTRES ET NAVIGATION
# ================================
st.sidebar.title("Contrôles")

# Filtres
st.sidebar.header("📅 Filtres temporels")
years = Utils.get_years_list(df)
selected_year = st.sidebar.selectbox(
    "Filtrer par année",
    ["Toutes les années"] + years,
    help="Sélectionnez une année spécifique ou gardez toutes les années"
)

# Appliquer le filtre
if selected_year != "Toutes les années":
    filtered_df = Utils.filter_by_year(df, selected_year)
    if filtered_df is not None and not filtered_df.empty:
        # Recalculer les stats pour l'année filtrée
        filtered_stats = StatisticsCalculator(filtered_df)
        current_stats = filtered_stats
        current_insights = InsightsCalculator(filtered_stats)
        period_text = f"Année {selected_year}"
    else:
        st.sidebar.warning("Aucune donnée pour cette année sélectionnée.")
        current_stats = stats_calc
        current_insights = insights_calc
        period_text = "Toutes les années"
else:
    current_stats = stats_calc
    current_insights = insights_calc
    period_text = f"{df['date'].min().strftime('%d/%m/%Y')} - {df['date'].max().strftime('%d/%m/%Y')}"

# ================================
# SECTION STATISTIQUES GLOBALES
# ================================
st.header("Statistiques globales")

overview = current_insights.get_overview_insights()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Nombre total de tirages", f"{overview['total_tirages']:,}")

with col2:
    st.metric("Période couverte", period_text)

with col3:
    st.metric("Prix moyen", Utils.format_currency(overview['prix_moyen']))

with col4:
    st.metric("Tirages avec gagnant", f"{overview['tirages_avec_gagnant']:,} ({overview['pourcentage_avec_gagnant']:.1f}%)")

# ================================
# SECTION PRIX DÉTAILLÉS
# ================================
st.subheader("Analyse détaillée des prix")

price_col1, price_col2, price_col3, price_col4 = st.columns(4)

with price_col1:
    st.metric("Prix moyen", Utils.format_currency(overview['prix_moyen']))

with price_col2:
    st.metric("Prix médian", Utils.format_currency(overview['prix_median']))

with price_col3:
    st.metric("Prix minimum", Utils.format_currency(overview['jackpot_min']))

with price_col4:
    st.metric("Prix maximum", Utils.format_currency(overview['jackpot_max']))

# Distribution des prix
prize_stats = current_stats.get_prize_stats()
if not pd.isna(prize_stats['moyen']):
    st.markdown("**Distribution des prix :**")
    prizes = current_stats.df['prize'].dropna()

    col1, col2 = st.columns(2)

    with col1:
        # Histogramme des prix
        fig_prizes = px.histogram(
            prizes,
            nbins=50,
            title=f"Distribution des prix ({period_text})",
            labels={'value': 'Prix (€)', 'count': 'Nombre de tirages'},
            color_discrete_sequence=['green']
        )
        fig_prizes.update_layout(
            xaxis_title="Prix (€)",
            yaxis_title="Nombre de tirages"
        )
        st.plotly_chart(fig_prizes, width='stretch')

    with col2:
        # Box plot des prix
        fig_box = px.box(
            prizes,
            title=f"Boîte à moustaches des prix ({period_text})",
            labels={'y': 'Prix (€)'},
            color_discrete_sequence=['orange']
        )
        st.plotly_chart(fig_box, width='stretch')

# Détails supplémentaires
with st.expander("Voir plus de statistiques"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gagnants")
        st.write(f"**Tirages sans gagnant :** {overview['tirages_sans_gagnant']:,} ({overview['pourcentage_sans_gagnant']:.1f}%)")

    with col2:
        st.subheader("Autres métriques")
        st.write(f"**Écart-type des prix :** {Utils.format_currency(prizes.std()) if len(prizes) > 0 else 'N/A'}")
        st.write(f"**Prix le plus fréquent :** {Utils.format_currency(prizes.mode().iloc[0]) if len(prizes) > 0 else 'N/A'}")

st.markdown("---")

# ================================
# SECTION FRÉQUENCES
# ================================
st.header("Fréquences d'apparition")

freq_insights = current_insights.get_frequency_insights()

tab1, tab2 = st.tabs(["Numéros (1-50)", "Étoiles (1-12)"])

with tab1:
    number_freq_df = current_stats.get_number_frequencies()

    col1, col2 = st.columns(2)

    with col1:
        # Bar chart des fréquences des numéros
        fig_numbers = px.bar(
            number_freq_df,
            x='numero',
            y='frequence',
            title=f'Fréquence d\'apparition des numéros ({period_text})',
            labels={'numero': 'Numéro', 'frequence': 'Fréquence'},
            color='frequence',
            color_continuous_scale='Blues'
        )
        fig_numbers.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=5))
        st.plotly_chart(fig_numbers, width='stretch')

    with col2:
        # Distribution des fréquences
        fig_dist_numbers = px.histogram(
            number_freq_df,
            x='frequence',
            nbins=20,
            title=f'Distribution des fréquences des numéros ({period_text})',
            labels={'frequence': 'Fréquence'},
            color_discrete_sequence=['lightblue']
        )
        st.plotly_chart(fig_dist_numbers, width='stretch')

    # Top/Bottom numéros
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 numéros les plus fréquents")
        for item in freq_insights['top_5_numeros']:
            st.write(f"**{int(item['numero'])}** : {int(item['frequence'])} fois ({item['pourcentage']:.2f}%)")

    with col2:
        st.subheader("Top 5 numéros les moins fréquents")
        for item in freq_insights['bottom_5_numeros']:
            st.write(f"**{int(item['numero'])}** : {int(item['frequence'])} fois ({item['pourcentage']:.2f}%)")

with tab2:
    star_freq_df = current_stats.get_star_frequencies()

    col1, col2 = st.columns(2)

    with col1:
        # Bar chart des fréquences des étoiles
        fig_stars = px.bar(
            star_freq_df,
            x='etoile',
            y='frequence',
            title=f'Fréquence d\'apparition des étoiles ({period_text})',
            labels={'etoile': 'Étoile', 'frequence': 'Fréquence'},
            color='frequence',
            color_continuous_scale='Oranges'
        )
        fig_stars.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))
        st.plotly_chart(fig_stars, width='stretch')

    with col2:
        # Distribution des fréquences des étoiles
        fig_dist_stars = px.histogram(
            star_freq_df,
            x='frequence',
            nbins=10,
            title=f'Distribution des fréquences des étoiles ({period_text})',
            labels={'frequence': 'Fréquence'},
            color_discrete_sequence=['lightsalmon']
        )
        st.plotly_chart(fig_dist_stars, width='stretch')

    # Top/Bottom étoiles
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 étoiles les plus fréquentes")
        for item in freq_insights['top_5_etoiles']:
            st.write(f"**{int(item['etoile'])}** : {int(item['frequence'])} fois ({item['pourcentage']:.2f}%)")

    with col2:
        st.subheader("Top 5 étoiles les moins fréquentes")
        for item in freq_insights['bottom_5_etoiles']:
            st.write(f"**{int(item['etoile'])}** : {int(item['frequence'])} fois ({item['pourcentage']:.2f}%)")

st.markdown("---")

# ================================
# SECTION RÉGULARITÉ ET RETARDS
# ================================
st.header("Régularité et retards")

regularity = current_insights.get_regularity_insights()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Plus grands retards (numéros)")
    st.write("*Nombre de tirages depuis la dernière apparition*")
    for item in regularity['plus_grand_retard_numeros'][:10]:
        st.write(f"**{int(item['numero'])}** : {int(item['retard_max'])} tirages")

with col2:
    st.subheader("Numéros les plus récents")
    for item in regularity['numeros_plus_recents']:
        st.write(f"**{int(item['numero'])}** : {item['derniere_apparition'].strftime('%d/%m/%Y')}")

# Graphique des retards
delay_df = current_stats.get_number_delays()
fig_delays = px.bar(
    delay_df.head(20),
    x='numero',
    y='retard_max',
    title=f'Retards maximums des numéros ({period_text})',
    labels={'numero': 'Numéro', 'retard_max': 'Retard maximum (tirages)'},
    color='retard_max',
    color_continuous_scale='Reds'
)
fig_delays.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=5))
st.plotly_chart(fig_delays, width='stretch')

st.markdown("---")

# ================================
# SECTION GÉNÉRATEUR DE GRILLES
# ================================
st.header("Générateur de grilles EuroMillions")

st.warning("""
**Rappel :** Ce générateur est uniquement à des fins **exploratoires et ludiques**.
Il ne garantit aucunement de meilleures chances de gagner. Chaque tirage est indépendant !
""")

# Contrôles du générateur
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    generator_mode = st.selectbox(
        "Mode de génération",
        ["uniform", "frequent", "rare"],
        format_func=lambda x: {
            "uniform": "Aléatoire uniforme (classique)",
            "frequent": "Pondéré vers les plus fréquents",
            "rare": "Pondéré vers les moins fréquents"
        }[x],
        help="""
        - Uniforme : chaque numéro a la même probabilité
        - Fréquents : favorise les numéros sortis souvent historiquement
        - Rares : favorise les numéros sortis peu souvent historiquement
        """
    )

with col2:
    num_grids = st.selectbox(
        "Nombre de grilles",
        [1, 5],
        help="Générer une ou cinq grilles à la fois"
    )

with col3:
    generate_button = st.button("Générer", type="primary", width='stretch')

# Génération et affichage
if generate_button:
    st.subheader(f"Grilles générées ({generator_mode})")

    if num_grids == 1:
        numbers, stars = generator.generate_weighted_grid(generator_mode) if generator_mode != "uniform" else generator.generate_uniform_grid()

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Numéros :** " + "  ".join(str(n) for n in numbers))
        with col2:
            st.markdown("**Étoiles :** " + "  ".join(str(s) for s in stars))

    else:
        grids = generator.generate_multiple_grids(num_grids, generator_mode)

        for i, (numbers, stars) in enumerate(grids, 1):
            st.markdown(f"**Grille {i} :**")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("Numéros : " + "  ".join(str(n) for n in numbers))
            with col2:
                st.markdown("Étoiles : " + "  ".join(str(s) for s in stars))
            if i < num_grids:
                st.markdown("---")

st.markdown("---")

# ================================
# SECTION INSIGHTS AVANCÉS
# ================================
st.header("🔍 Insights avancés")

with st.expander("Probabilités empiriques vs théoriques"):
    prob_insights = current_insights.get_probability_insights()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Numéros")
        st.write(f"**Probabilité théorique :** {prob_insights['probabilite_theorique_numero']:.3f} (5/50)")
        st.write(f"**Probabilité empirique moyenne :** {prob_insights['probabilite_empirique_moyenne_numero']:.3f}")

    with col2:
        st.subheader("Étoiles")
        st.write(f"**Probabilité théorique :** {prob_insights['probabilite_theorique_etoile']:.3f} (2/12)")
        st.write(f"**Probabilité empirique moyenne :** {prob_insights['probabilite_empirique_moyenne_etoile']:.3f}")

with st.expander("Répartition des numéros"):
    dist_insights = current_insights.get_distribution_insights()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Par dizaines")
        decade_df = pd.DataFrame(dist_insights['distribution_par_dizaines'])
        st.dataframe(decade_df, width='stretch')

        fig_decades = px.bar(
            decade_df,
            x='decade',
            y='frequence',
            title='Répartition par dizaines',
            labels={'decade': 'Dizaine', 'frequence': 'Fréquence'},
            color='pourcentage',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_decades, width='stretch')

    with col2:
        st.subheader("Pairs/Impairs et autres stats")
        parity = dist_insights['statistiques_parite']
        st.write(f"**Pairs :** {parity['pairs']:,} ({parity['pourcentage_pairs']:.1f}%)")
        st.write(f"**Impairs :** {parity['impairs']:,} ({parity['pourcentage_impairs']:.1f}%)")

        sums = dist_insights['statistiques_sommes']
        st.write(f"**Somme moyenne des numéros :** {sums['moyenne']:.1f}")
        st.write(f"**Somme médiane :** {sums['mediane']:.1f}")
        st.write(f"**Somme min/max :** {sums['minimum']:.0f} - {sums['maximum']:.0f}")

# ================================
# FOOTER
# ================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: small;'>
    <p>EuroMillions - Analyse pédagogique des données historiques</p>
    <p><em>"Les tirages passés n'influencent pas les tirages futurs"</em></p>
</div>
""", unsafe_allow_html=True)


