import streamlit as st
import pandas as pd
import altair as alt


def load_data(file_path):
    """Load and preprocess the dataset."""
    data = pd.read_csv(file_path, encoding="latin")
    data["Spotify Streams"] = preprocess_column(data["Spotify Streams"])
    data["Spotify Playlist Count"] = preprocess_column(data["Spotify Playlist Count"])
    return data


def preprocess_column(column):
    """Convert a string column with commas to integers, handling NaN values."""
    column = column.str.replace(",", "")
    column = pd.to_numeric(column, errors="coerce").fillna(0).astype(int)
    return column


def show_raw_data(data):
    """Display the raw dataset if the checkbox is selected."""
    if st.sidebar.checkbox("Show raw data"):
        st.subheader("Spotify Songs Dataset")
        st.write(data)


def show_top_10_songs(data):
    """Display the top 10 most streamed songs."""
    st.subheader("Top 10 Most Streamed Songs")
    top_10_songs = data.nlargest(10, "Spotify Streams")[
        ["Track", "Artist", "Spotify Streams"]
    ]
    st.write(top_10_songs)
    return top_10_songs


def search_feature(data):
    """Provide a search feature to find specific tracks or artists."""
    st.subheader("Search for a Track or Artist")
    search_query = st.text_input("Enter a track or artist name")
    if search_query:
        search_results = data[
            data.apply(
                lambda row: search_query.lower() in row["Track"].lower()
                or search_query.lower() in row["Artist"].lower(),
                axis=1,
            )
        ]
        st.write(search_results)


def visualize_top_10_songs(top_10_songs):
    """Visualize the top 10 songs by Spotify Streams."""
    st.subheader("Top 10 Songs by Spotify Streams")
    top_10_chart = (
        alt.Chart(top_10_songs)
        .mark_bar()
        .encode(
            x=alt.X("Spotify Streams", title="Spotify Streams"),
            y=alt.Y("Track", sort="-x", title="Track"),
            color="Artist",
        )
        .properties(width=700, height=400)
    )
    st.altair_chart(top_10_chart)


def visualize_top_10_artists(data):
    """Visualize the top 10 artists by Spotify Playlist Count."""
    st.subheader("Top 10 Artists by Spotify Playlist Count")
    top_10_artists = (
        data.groupby("Artist")
        .agg({"Spotify Playlist Count": "sum"})
        .reset_index()
        .nlargest(10, "Spotify Playlist Count")
    )
    top_10_artists_chart = (
        alt.Chart(top_10_artists)
        .mark_bar()
        .encode(
            x=alt.X("Spotify Playlist Count", title="Spotify Playlist Count"),
            y=alt.Y("Artist", sort="-x", title="Artist"),
            color="Artist",
        )
        .properties(width=700, height=400)
    )
    st.altair_chart(top_10_artists_chart)


st.sidebar.title("Spotify Songs Dashboard")
st.sidebar.markdown("Analyze the most streamed Spotify songs of 2024")

data = load_data("spotify_songs_2024.csv")

show_raw_data(data)
top_10_songs = show_top_10_songs(data)
search_feature(data)
visualize_top_10_songs(top_10_songs)
visualize_top_10_artists(data)
