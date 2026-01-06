import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# 頁面設定
st.set_page_config(page_title="24H 全球財經新聞儀表板", layout="wide")

# 從 Streamlit Secrets 讀取 API Key (部署後在 Streamlit Cloud 設定)
API_KEY = st.secrets["NEWS_API_KEY"]

def fetch_news(query):
    # 設定搜尋 24 小時內的新聞
    from_date = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S')
    url = f"https://newsapi.org/v2/everything?q={query}&from={from_date}&sortBy=publishedAt&language=zh&apiKey={API_KEY}"
    
    # NewsAPI 的中文支援有時有限，若無結果則嘗試英文搜尋
    response = requests.get(url)
    data = response.json()
    
    if data.get("status") == "ok":
        return data.get("articles", [])
    return []

# --- 側邊欄設定 ---
st.sidebar.title("🔍 新聞追蹤設定")
update_interval = st.sidebar.selectbox("自動重新整理頻率", ["手動", "15分鐘", "1小時"])
if st.sidebar.button("立即更新數據"):
    st.rerun()

st.title("📊 24H 財經新聞即時監控")
st.write(f"最後更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- 分類邏輯 ---
categories = {
    "🌍 總體經濟": "Macroeconomics OR Inflation OR Fed OR Central Bank",
    "🇺🇸 美股重大新聞": "US Stock Market OR S&P500 OR Nasdaq OR Nvidia OR Apple",
    "🇹🇼 台股重大新聞": "Taiwan Stock OR TSMC OR 台股 OR 半導體",
    "🇯🇵 日股重大新聞": "Japan Stock OR Nikkei 225 OR Yen OR Tokyo Stock Exchange"
}

# 建立分頁
tabs = st.tabs(list(categories.keys()))

for i, (name, query) in enumerate(categories.items()):
    with tabs[i]:
        articles = fetch_news(query)
        if not articles:
            st.info(f"目前暫無 {name} 的相關新聞。")
        else:
            for art in articles[:10]:  # 顯示前10則
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if art.get("urlToImage"):
                            st.image(art["urlToImage"])
                    with col2:
                        st.subheader(art["title"])
                        st.caption(f"來源: {art['source']['name']} | 發布時間: {art['publishedAt']}")
                        st.write(art["description"])
                        st.markdown(f"[閱讀全文]({art['url']})")
                    st.divider()