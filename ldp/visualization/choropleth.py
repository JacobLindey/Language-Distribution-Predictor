"""
    Generates choropleth charts that are displayed in a web browser.

    Takes data from simulation and displays a single language distribution across a
    global map. Uses plotly's gapminder dataset as a base for world data.

    For more information on choropleth charts see https://en.wikipedia.org/wiki/Choropleth_map

    ldp.visualization.choropleth
    ./visualization/choropleth.py

    author: Jacob Lindey
    created: 7-22-2019
    update: 7-22-2019
"""
import plotly.express as px
import pandas as pd


def show_choropleth(sim_dataframe: pd.DataFrame, language: str) -> None:
    """
        Shows a choropleth chart of the language distribution from sim_dataframe.

        Args:
            sim_dataframe (pandas.DataFrame): A DataFrame containing the output from
                the ldp simulation.
            language (str): The name of a language distribution to display. Must be
                a column header in sim_dataframe.

        Raises:
            ValueError: if language is not a column header in sim_dataframe.
    """
    if language not in sim_dataframe.columns:
        raise ValueError(f"ValueError: Invalid language '{language}'.")

    # merge plotly.gapminder dataset with our data on iso_alpha
    df_map = sim_dataframe.rename(columns={'regions':'iso_alpha'}, inplace=False)
    gapminder = px.data.gapminder().query("year==2007")
    df_all = pd.merge(gapminder, df_map, on="iso_alpha")

    # generate figure
    fig = px.choropleth(df_all, locations="iso_alpha",
                        color=language, # life Exp is a column of gapminder
                        hover_name="country", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.show(renderer="browser")
