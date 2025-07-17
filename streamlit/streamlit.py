import streamlit as st
import pandas as pd
from core.settings import settings
from core.db import PostActions

# Function to load posts from the database into a DataFrame
def load_data():
    db = PostActions(settings.DB_URL)
    posts = db.get_posts()
    data = [PostActions.object_as_dict(post) for post in posts]
    df = pd.DataFrame(data)
    return df

def main():
    st.set_page_config(page_title="📰 News Bot Dashboard", layout="wide", page_icon="📰")

    # Sidebar
    st.sidebar.image("https://img.icons8.com/color/96/news.png", width=64)
    st.sidebar.title("News Bot Dashboard")
    st.sidebar.markdown("Monitor and analyze your news posts in real time.")
    st.sidebar.markdown("---")
    st.sidebar.info("Dashboard")

    st.title("📰 News Bot Dashboard")
    st.markdown("Welcome to your news analytics dashboard. Here you can view metrics, trends, and details about your posts.")

    df = load_data()
    if df.empty:
        st.info("No posts found in the database.")
        return

    # Ensure created_at is datetime
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'])
    else:
        st.warning("`created_at` field not found; time-based charts will be disabled.")

    # Overview metrics in columns
    st.header("Overview")
    col1, col2, col3 = st.columns(3)
    total_posts = len(df)
    col1.metric(label="📝 Total Posts", value=total_posts)

    if 'created_at' in df.columns and not df['created_at'].empty:
        date_range = df['created_at'].max() - df['created_at'].min()
        days = date_range.days + 1
        avg_per_day = total_posts / days if days > 0 else total_posts
        col2.metric(label="📅 Avg Posts/Day", value=f"{avg_per_day:.2f}")
        first_date = df['created_at'].min().strftime("%Y-%m-%d")
        last_date = df['created_at'].max().strftime("%Y-%m-%d")
        col3.metric(label="🕒 Date Range", value=f"{first_date} → {last_date}")
    else:
        col2.metric(label="Avg Posts/Day", value="N/A")
        col3.metric(label="Date Range", value="N/A")

    # Latest posts table in expander
    with st.expander("📋 Latest Posts", expanded=True):
        display_cols = ['id', 'title', 'news_url', 'ai_title']
        if 'created_at' in df.columns:
            display_cols.append('created_at')
        st.dataframe(
            df.sort_values(by='created_at', ascending=False)[display_cols],
            use_container_width=True,
            height=350
        )

    # Charts in columns
    st.header("Trends & Distributions")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Posts Over Time")
        if 'created_at' in df.columns:
            posts_by_date = df.groupby(df['created_at'].dt.date).size()
            st.line_chart(posts_by_date, height=250)
        else:
            st.write("Created_at field missing: cannot render time-series chart.")

    with chart_col2:
        st.subheader("Title Length Distribution")
        df['title_length'] = df['title'].str.len()
        st.bar_chart(df['title_length'].value_counts().sort_index(), height=250)

    # Footer
    st.markdown("---")
    st.caption("© 2024 News Bot Dashboard | Built with Streamlit")

if __name__ == "__main__":
    main()
