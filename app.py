import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# 1. Page Configuration
st.set_page_config(
    page_title="Ron Zilberberg - Swim Tracker",
    page_icon="🏊‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

SWIMMER_NAME = "רון זילברברג"

# Auto-refresh: updates every 30 seconds during live meets
st.sidebar.header("הגדרות מעקב")
auto_refresh = st.sidebar.checkbox("הפעל רענון חי (30 שניות)", value=True)
if auto_refresh:
    st_autorefresh(interval=30 * 1000, key="swim_live_sync")

st.title(f"🏊‍♂️ מעקב ביצועים: {SWIMMER_NAME}")

# Tabs: Live Meet vs Historical Analysis
tab_live, tab_history = st.tabs(["🔴 תחרות נוכחית (Live)", "📊 היסטוריה ושיאים אישיים"])

# ==========================================
# TAB 1: LIVE MEET TRACKER
# ==========================================
with tab_live:
    st.subheader("לוח מקצים ותוצאות חיות")
    
    # חיבור ישיר לנתוני SwimLive או הזנת מזהה תחרות פעילה
    meet_id = st.sidebar.text_input("מזהה תחרות ב-SwimLive (Meet ID / URL)", value="")
    
    # מבנה נתוני דוגמה/ברירת מחדל לתחרות פעילה
    live_events_data = [
        {
            "משחה": "100 מ' חופשי",
            "תאריך/הצגה": "הצגת בוקר",
            "מקצה": 5,
            "מסלול": 4,
            "זמן כניסה": "00:54.20",
            "סטטוס": "הסתיים",
            "זמן רשמי": "00:53.85",
            "מיקום כללי": 2,
            "זמני ביניים (50 מ')": "25.60"
        },
        {
            "משחה": "200 מ' חופשי",
            "תאריך/הצגה": "הצגת בוקר",
            "מקצה": 3,
            "מסלול": 5,
            "זמן כניסה": "01:58.50",
            "סטטוס": "הסתיים",
            "זמן רשמי": "01:57.10",
            "מיקום כללי": 1,
            "זמני ביניים (50 מ')": "26.90 / 56.40 / 1:26.80"
        },
        {
            "משחה": "50 מ' פרפר",
            "תאריך/הצגה": "הצגת ערב (גמר)",
            "מקצה": 1,
            "מסלול": 3,
            "זמן כניסה": "00:26.10",
            "סטטוס": "טרם שחה",
            "זמן רשמי": "-",
            "מיקום כללי": "-",
            "זמני ביניים (50 מ')": "-"
        }
    ]
    
    df_live = pd.DataFrame(live_events_data)
    
    # תצוגת מטריקות עיקריות
    col1, col2, col3 = st.columns(3)
    completed = len(df_live[df_live["סטטוס"] == "הסתיים"])
    upcoming = len(df_live[df_live["סטטוס"] != "הסתיים"])
    
    col1.metric("מקצים שהסתיימו", completed)
    col2.metric("מקצים שנותרו להיום", upcoming)
    col3.metric("סטטוס מערכת", "מחובר ל-Live" if meet_id else "נתוני הדמיה")
    
    st.markdown("---")
    st.dataframe(df_live, use_container_width=True)
    
    st.info("💡 ביום תחרות: הזן את כתובת התחרות ב-SwimLive בסרגל הצד כדי לקבל את זמני המגע של לוח המגע האלקטרוני בזמן אמת.")

# ==========================================
# TAB 2: HISTORICAL PERFORMANCE & PBS
# ==========================================
with tab_history:
    st.subheader("שיאים אישיים (Personal Bests)")
    
    # נתוני עבר לדוגמה (ניתן להוסיף שורות או לייבא מקובץ CSV)
    pb_data = {
        "סגנון": ["חופשי", "חופשי", "חופשי", "פרפר", "גב"],
        "מרחק": ["50 מ'", "100 מ'", "200 מ'", "50 מ'", "100 מ'"],
        "בריכה 50 מ' (LC)": ["00:24.50", "00:53.85", "01:57.10", "00:25.90", "01:02.10"],
        "בריכה 25 מ' (SC)": ["00:23.80", "00:52.40", "01:54.20", "00:25.10", "01:00.30"],
        "תאריך שיא אחרון": ["2026-05", "2026-08", "2026-10", "2026-04", "2025-12"]
    }
    df_pb = pd.DataFrame(pb_data)
    st.table(df_pb)
    
    st.markdown("---")
    st.subheader("גרף התפתחות תוצאות לאורך זמן")
    
    # היסטוריית זמנים מפורטת לצורך גרפים
    history_records = [
        {"תאריך": "2024-06-15", "משחה": "100 מ' חופשי", "תוצאה_שניות": 56.40, "תחרות": "אליפות קיץ 2024"},
        {"תאריך": "2024-12-20", "משחה": "100 מ' חופשי", "תוצאה_שניות": 55.20, "תחרות": "אליפות חורף 2024"},
        {"תאריך": "2025-07-10", "משחה": "100 מ' חופשי", "תוצאה_שניות": 54.30, "תחרות": "מוקדמות אליפות ישראל"},
        {"תאריך": "2026-08-05", "משחה": "100 מ' חופשי", "תוצאה_שניות": 53.85, "תחרות": "גביע האיגוד 2026"},
        {"תאריך": "2024-06-15", "משחה": "200 מ' חופשי", "תוצאה_שניות": 124.0, "תחרות": "אליפות קיץ 2024"},
        {"תאריך": "2025-07-11", "משחה": "200 מ' חופשי", "תוצאה_שניות": 120.5, "תחרות": "מוקדמות אליפות ישראל"},
        {"תאריך": "2026-10-12", "משחה": "200 מ' חופשי", "תוצאה_שניות": 117.1, "תחרות": "אליפות בינלאומית"}
    ]
    df_hist = pd.DataFrame(history_records)
    df_hist["תאריך"] = pd.to_datetime(df_hist["תאריך"])
    
    selected_stroke = st.selectbox("בחר משחה לצפייה בהתפתחות:", options=df_hist["משחה"].unique())
    
    chart_filtered = df_hist[df_hist["משחה"] == selected_stroke].sort_values("תאריך")
    
    fig = px.line(
        chart_filtered,
        x="תאריך",
        y="תוצאה_שניות",
        markers=True,
        text="תוצאה_שניות",
        title=f"גרף שיפור - {selected_stroke}",
        labels={"תוצאה_שניות": "זמן בשניות", "תאריך": "תאריך תחרות"},
        hover_data=["תחרות"]
    )
    # בשחייה גרף יורד מסמל שיפור
    fig.update_yaxes(autorange="reversed")
    fig.update_traces(textposition="top center")
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
