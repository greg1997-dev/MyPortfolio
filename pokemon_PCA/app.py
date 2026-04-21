import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Pokémon PCA Explorer",
    layout="wide"
)


@st.cache_data
def load_data():
    df=pd.read_csv("https://raw.githubusercontent.com/greg1997-dev/MyPortfolio/refs/heads/main/pokemon_PCA/poke_pca.csv")
    df['name']=df['name'].str.title()
    df['generation']=df['generation'].str.title()
    return df

pca_df = load_data()


typeColors = {
    'normal': '#A8A878','fire': '#F08030','water': '#6890F0','electric': '#F8D030',
    'grass': '#78C850','ice': '#98D8D8','fighting': '#C03028','poison': '#A040A0',
    'ground': '#E0C068','flying': '#A890F0','psychic': '#F85888','bug': '#A8B820',
    'rock': '#B8A038','ghost': '#705898','dragon': '#7038F8','dark': '#705848',
    'steel': '#B8B8D0','fairy': '#EE99AC'
}


st.sidebar.title("Controls")

mode = st.sidebar.radio(
    "Visualization Mode",
    ["2D PCA", "3D PCA"]
)

generations = st.sidebar.multiselect(
    "Select Generation",
    sorted(pca_df['generation'].unique()),
    default=sorted(pca_df['generation'].unique())
)

types = st.sidebar.multiselect(
    "Select Type",
    sorted(pca_df['type'].unique()),
    default=sorted(pca_df['type'].unique())
)


filtered_df = pca_df[
    (pca_df['generation'].isin(generations)) &
    (pca_df['type'].isin(types))
]


selected_pokemon = st.sidebar.selectbox(
    "Highlight Pokémon",
    ["None"] + sorted(filtered_df['name'].unique())
)


st.title("Pokémon PCA Explorer")

st.markdown("""
Explore how Pokémon cluster based on their stats using PCA.
Switch between 2D and 3D views, and filter by generation and type.
""")

col_chart, col_card = st.columns([3, 1])


if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()


if mode == "2D PCA":
    fig = px.scatter(
        filtered_df,
        x="PC1",
        y="PC2",
        color="type",
        hover_name="name",
        color_discrete_map=typeColors,
        render_mode="webgl"  # faster
    )

else:
    fig = px.scatter_3d(
        filtered_df,
        x="PC1",
        y="PC2",
        z="PC3",
        color="type",
        hover_name="name",
        color_discrete_map=typeColors
    )

if selected_pokemon != "None":
    highlight_df = filtered_df[filtered_df['name'] == selected_pokemon]

    if mode == "2D PCA":
        fig.add_trace(
            go.Scatter(
                x=highlight_df['PC1'],
                y=highlight_df['PC2'],
                mode='markers+text',
                marker=dict(size=12, color='black'),
                text=highlight_df['name'],
                textposition="top center",
                showlegend=False
            )
        )
    else:
        fig.add_trace(
            go.Scatter3d(
                x=highlight_df['PC1'],
                y=highlight_df['PC2'],
                z=highlight_df['PC3'],
                mode='markers+text',
                marker=dict(size=6, color='black'),
                text=highlight_df['name'],
                textposition="top center",
                showlegend=False
            )
        )

if mode == "2D PCA":
    fig.add_hline(y=0, line=dict(color="black", width=2))
    fig.add_vline(x=0, line=dict(color="black", width=2))


if mode == "3D PCA":
    x_range = [filtered_df['PC1'].min(), filtered_df['PC1'].max()]
    y_range = [filtered_df['PC2'].min(), filtered_df['PC2'].max()]
    z_range = [filtered_df['PC3'].min(), filtered_df['PC3'].max()]

    fig.add_trace(go.Scatter3d(x=x_range, y=[0,0], z=[0,0], mode='lines',
                               line=dict(color='black', width=4), showlegend=False))
    fig.add_trace(go.Scatter3d(x=[0,0], y=y_range, z=[0,0], mode='lines',
                               line=dict(color='black', width=4), showlegend=False))
    fig.add_trace(go.Scatter3d(x=[0,0], y=[0,0], z=z_range, mode='lines',
                               line=dict(color='black', width=4), showlegend=False))


fig.update_layout(
    margin=dict(l=0, r=0, t=40, b=0),
    legend_title="Type"
)


with col_chart:
    st.plotly_chart(fig, use_container_width=True)

with col_card:
    st.subheader("Pokémon Details")

    if selected_pokemon == "None":
        st.info("Select a Pokémon to see details")
    else:
        pokemon = filtered_df[filtered_df['name'] == selected_pokemon].iloc[0]

        st.image(pokemon['sprite_url'], width=120)
        st.markdown(f"### {pokemon['name']}")
        st.write(f"**Type:** {pokemon['type']}")
        st.write(f"**Generation:** {pokemon['generation']}")


st.markdown("""
---
💡 **Tip:** Try filtering by a single type or generation to see how clusters change.
""")