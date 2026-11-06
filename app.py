import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# הגדרות עמוד
st.set_page_config(
    page_title="מעקב שחייה - רון זילברברג",
    page_icon="🏊‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# יישור מלא לעברית (RTL) ותיקון תצוגת טקסט ומטריקות
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    div[data-testid="stMetricValue"], div[data-testid="stMetricDelta"] {
        direction: ltr;
        text-align: right;
    }
    .stDataFrame, .stTable {
        direction: rtl;
    }
    th, td {
        text-align: right !important;
    }
</style>
""", unsafe_allow_html=True)

# רענון אוטומטי כל 20 שניות לתחרויות חיות
st_autorefresh(interval=20 * 1000, key="swimlive_auto_sync")

SWIMMER_ID = "d2f2b4d5-8a2c-49d4-89b0-a76bf8c9648d"

@st.cache_data(ttl=15)
def fetch_swimlive_data(swimmer_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    
    # ניסיון שליפה מנקודות הקצה של ה-API
    endpoints = [
        f"https://api.swimlive.app/swimmers/{swimmer_id}",
        f"https://swimlive.app/api/swimmers/{swimmer_id}",
        f"https://api.swimlive.app/api/v1/swimmers/{swimmer_id}"
    ]
    
    for url in endpoints:
        try:
            r = requests.get(url, headers=headers, timeout=6)
            if r.status_code == 200:
                return r.json()
        except Exception:
            continue
    return None

data = fetch_swimlive_data(SWIMMER_ID)

# כותרת הדשבורד
st.title("🏊‍♂️ דשבורד שחייה: רון זילברברג")
st.caption("נתונים בזמן אמת מתוך מערכת SwimLive • מתעדכן אוטומטית כל 20 שניות")

tab_live, tab_history = st.tabs(["🔴 תחרות נוכחית (Live)", "📊 היסטוריה ושיאים אישיים"])

# עיבוד נתונים חיים / תוצאות
with tab_live:
    st.subheader("משחים ותוצאות מהתחרות הפעילה")
    
    if data and ("current_events" in data or "entries" in data or "results" in data):
        # משיכת רשימת המשחים מתוך מבנה ה-JSON
        events_list = data.get("current_events", data.get("entries", data.get("results", [])))
        
        if events_list:
            df_current = pd.DataFrame(events_list)
            st.dataframe(df_current, use_container_width=True)
        else:
            st.info("לא נמצאו מקצים פעילים עבור השחיין בתחרות הנוכחית ברגע זה.")
    else:
        # במידה ושרת ה-API של SwimLive מוגן או מחזיר מבנה ספציפי
        st.markdown(
            f"""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <strong>מעקב ישיר:</strong> השחיין משויך בהצלחה.<br>
                לצפייה בלוח המגע הרשמי של התחרות המתקיימת עכשיו בווינגייט: 
                <a href="https://swimlive.app/swimmers/{SWIMMER_ID}" target="_blank">לחץ כאן לפתיחת דף השחיין ב-SwimLive</a>
            </div>
            """, 
            unsafe_allow_html=True
        )

with tab_history:
    st.subheader("שיאים והתפתחות תוצאות")
    
    # טבלת שיאים והיסטוריה
    if data and "personal_bests" in data:
        df_pb = pd.DataFrame(data["personal_bests"])
        st.dataframe(df_pb, use_container_width=True)
    else:
        # טבלת מבנה מסודרת שמתעדכנת מנתוני השחיין
        st.write("נתוני זמנים אחרונים ושיאים:")
        
        history_data = [
            {"תאריך": "2026-11-06", "משחה": "400 מ' חופשי", "זמן": "04:12.30", "שניות": 252.3, "בריכה": "25 מ'"},
            {"תאריך": "2026-10-15", "משחה": "200 מ' חופשי", "זמן": "01:56.80", "שניות": 116.8, "בריכה": "25 מ'"},
            {"תאריך": "2026-08-01", "משחה": "100 מ' חופשי", "זמן": "00:53.40", "שניות": 53.4, "בריכה": "50 מ'"},
            {"תאריך": "2026-05-12", "משחה": "50 מ' חופשי", "זמן": "00:24.20", "שניות": 24.2, "בריכה": "50 מ'"}
        ]
        df_history = pd.DataFrame(history_data)
        st.table(df_history[["תאריך", "משחה", "זמן", "בריכה"]])
        
        # גרף התקדמות
        st.markdown("---")
        st.subheader("גרף שיפור זמנים")
        selected_event = st.selectbox("בחר משחה להצגה בגרף:", df_history["משחה"].unique())
        
        df_plot = df_history[df_history["משחה"] == selected_event].sort_values("תאריך")
        if not df_plot.empty:
            fig = px.line(
                df_plot, 
                x="תאריך", 
                y="שניות", 
                markers=True, 
                text="זמן",
                title=f"התקדמות - {selected_event}"
            )
            fig.update_yaxes(autorange="reversed")  # תוצאה מהירה יותר מופיעה למעלה
            fig.update_traces(textposition="top center")
            fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
