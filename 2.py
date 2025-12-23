import streamlit as st
import pandas as pd

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Social Media Analytics Pro",
    page_icon="🚀",
    layout="wide"
)

# =================================================
# CSS
# =================================================
st.markdown("""
<style>
.main { background: linear-gradient(to right, #141E30, #243B55); }
.gradient-text {
    background: linear-gradient(90deg,#00c6ff,#0072ff,#7f00ff,#e100ff);
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-card {
    padding: 20px; border-radius: 18px; color: white;
    text-align: center; box-shadow: 0px 6px 25px rgba(0,0,0,0.4);
}
.blue { background: linear-gradient(135deg,#396afc,#2948ff); }
.green { background: linear-gradient(135deg,#11998e,#38ef7d); }
.orange { background: linear-gradient(135deg,#f7971e,#ffd200); }
.red { background: linear-gradient(135deg,#ff416c,#ff4b2b); }
.purple { background: linear-gradient(135deg,#667eea,#764ba2); }
</style>
""", unsafe_allow_html=True)

# =================================================
# LOAD DATA
# =================================================
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_engagement_enhanced.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# =================================================
# DERIVED METRICS
# =================================================
df["revenue_generated"] = df["ad_spend"] * (1 + df["roi"])

# =================================================
# SIDEBAR FILTERS
# =================================================
st.sidebar.markdown("## 🎛️ Dashboard Controls")

platform_filter = st.sidebar.multiselect("📱 Platform", df["platform"].unique(), df["platform"].unique())
content_filter = st.sidebar.multiselect("🖼️ Content Type", df["content_type"].unique(), df["content_type"].unique())
year_filter = st.sidebar.multiselect("📅 Year", df["year"].unique(), df["year"].unique())

filtered_df = df[
    (df["platform"].isin(platform_filter)) &
    (df["content_type"].isin(content_filter)) &
    (df["year"].isin(year_filter))
]

# =================================================
# HEADER
# =================================================
st.markdown("""
<h1 class="gradient-text" style="text-align:center;">
🚀 Social Media Analytics Pro Dashboard
</h1>
<p style="text-align:center;color:#dcdcdc;">
Engagement • Content • Campaign ROI • Strategy
</p>
""", unsafe_allow_html=True)

# =================================================
# KPI CARDS
# =================================================
c1, c2, c3, c4, c5 = st.columns(5)

c1.markdown(f"<div class='metric-card blue'><h3>Total Engagement</h3><h2>{int(filtered_df['engagement'].sum())}</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card green'><h3>Avg Engagement Rate</h3><h2>{round(filtered_df['engagement_rate'].mean(),2)}%</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card orange'><h3>Ad Spend</h3><h2>₹ {int(filtered_df['ad_spend'].sum())}</h2></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card red'><h3>Revenue</h3><h2>₹ {int(filtered_df['revenue_generated'].sum())}</h2></div>", unsafe_allow_html=True)
c5.markdown(f"<div class='metric-card purple'><h3>Avg ROI</h3><h2>{round(filtered_df['roi'].mean(),2)}</h2></div>", unsafe_allow_html=True)

# =================================================
# COMMON INSIGHTS
# =================================================
best_platform = filtered_df.groupby("platform")["engagement_rate"].mean().idxmax()
best_content = filtered_df.groupby("content_type")["engagement_rate"].mean().idxmax()
best_hour = filtered_df.groupby("post_hour")["engagement"].mean().idxmax()
best_month = filtered_df.groupby("month")["engagement"].mean().idxmax()

# =================================================
# TABS (CREATIVE SET)
# =================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ["📱 Engagement", "🖼️ Content", "💰 Campaign ROI", "⏰ Best Time",
     "📈 Trends", "🧭 Strategy Advisor", "🏆 Scorecard"]
)

# ---------------- TAB 1 ----------------
with tab1:
    plat = filtered_df.groupby("platform")["engagement_rate"].mean().reset_index()
    st.bar_chart(plat, x="platform", y="engagement_rate")
    st.info(f"Best platform: **{best_platform}**")

# ---------------- TAB 2 ----------------
with tab2:
    cont = filtered_df.groupby("content_type")["engagement"].mean().reset_index()
    st.bar_chart(cont, x="content_type", y="engagement")

# ---------------- TAB 3 ----------------
with tab3:
    camp = filtered_df.groupby("campaign_name")[["ad_spend","roi"]].mean().reset_index()
    st.dataframe(camp)

# ---------------- TAB 4 ----------------
with tab4:
    hour = filtered_df.groupby("post_hour")["engagement"].mean().reset_index()
    st.line_chart(hour, x="post_hour", y="engagement")
    st.success(f"Best posting time: **{best_hour}:00 hrs**")

# ---------------- TAB 5 ----------------
with tab5:
    trend = filtered_df.groupby(["year","month"])["engagement"].mean().reset_index()
    st.line_chart(trend, x="month", y="engagement")
    st.info(f"Highest engagement in Month **{best_month}**")

# ---------------- TAB 6 : STRATEGY ADVISOR ----------------
with tab6:
    st.success("📌 **Smart Strategy Recommendation**")
    st.write(f"""
    • Focus on **{best_platform}** platform  
    • Use **{best_content}** content  
    • Post around **{best_hour}:00 hrs**  
    • Peak engagement in **Month {best_month}**
    """)

# ---------------- TAB 7 : PERFORMANCE SCORECARD ----------------
with tab7:
    score_df = filtered_df.groupby("platform")[["engagement_rate","roi","reach"]].mean().reset_index()

    score_df["score"] = (
        score_df["engagement_rate"] * 40 +
        score_df["roi"] * 40 +
        (score_df["reach"] / score_df["reach"].max()) * 20
    )

    score_df["score"] = score_df["score"].round(1)
    st.dataframe(score_df[["platform","score"]])
    st.bar_chart(score_df, x="platform", y="score")

# =================================================
# INSIGHTS TAB (TEXT-BASED, VERY CREATIVE)
# =================================================
st.markdown("## 💡 Key Insights")
st.markdown(f"""
- **{best_content}** content performs better than other formats  
- Evening posting hours show higher engagement  
- Higher ad spend does not always guarantee higher ROI  
- **{best_platform}** is the most effective platform overall
""")

# =================================================
# DOWNLOAD
# =================================================
st.download_button(
    "⬇️ Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_social_media_data.csv",
    "text/csv"
)

# =================================================
# FOOTER
# =================================================
st.markdown("""
<hr>
<p style="text-align:center;color:#bbbbbb;">
Social Media Engagement Analytics • Expo Project
</p>
""", unsafe_allow_html=True)
