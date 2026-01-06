import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import urllib.parse

# 頁面設定
st.set_page_config(page_title="24H 全球財經免API監控", layout="wide")

def get_google_news(search_query):
    # 將關鍵字進行 URL 編碼
    encoded_query = urllib.parse.quote(search_query)
    # 使用 Google News RSS 連結 (hl=zh-TW 為繁體中文, gl=TW 為台灣區域)
    # when:1d 代表過去 24 小時
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}+when:1d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    
    feed = feedparser.parse(rss_url)
    articles = []
    
    for entry in feed.entries[:10]: # 每個分類取前 10 則
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "source": entry.source.title if hasattr(entry, 'source') else "Google News"
        })
    return articles

st.title("📊 24H 財經新聞即時監控 (RSS 版)")
st.caption("使用 Google News 資源，無需 API Key，自動抓取過去 24 小時新聞。")

# 定義分類與搜尋關鍵字
categories = {
    "🌍 總體經濟": "總體經濟 OR 通膨 OR 聯準會 OR 降息",
    "🇺🇸 美股重大新聞": "美股 OR 標普500 OR 納斯達克 OR NVIDIA OR 蘋果股價",
    "🇹🇼 台股重大新聞": "台股 OR 積體電路 OR 台積電 OR 鴻海 OR 加權指數",
    "🇯🇵 日股重大新聞": "日股 OR 日經225 OR 日本銀行 OR 日圓匯率"
}

tabs = st.tabs(list(categories.keys()))

for i, (name, query) in enumerate(categories.items()):
    with tabs[i]:
        with st.spinner(f'正在讀取 {name}...'):
            news_items = get_google_news(query)
            
            if not news_items:
                st.warning(f"⚠️ 過去 24 小時內暫無 {name} 相關新聞，請嘗試點選側邊欄更新。")
            else:
                for item in news_items:
                    with st.expander(f"📌 {item['title']}"):
                        st.write(f"**來源：** {item['source']}")
                        st.write(f"**發布時間：** {item['published']}")
                        st.markdown(f"[🔗 點擊閱讀新聞全文]({item['link']})")

# 側邊欄重新整理按鈕
if st.sidebar.button("🔄 立即重新整理"):
    st.rerun()
