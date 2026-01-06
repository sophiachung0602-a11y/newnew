import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="24H 全球財經即時監控", layout="wide")

def get_google_news(search_query):
    # 優化搜尋語法：移除過多的 OR，確保搜尋結果精準
    encoded_query = urllib.parse.quote(search_query)
    # 增加時區設定與排序邏輯
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}+when:1d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    
    feed = feedparser.parse(rss_url)
    return feed.entries[:10]

st.title("📊 24H 財經新聞即時監控")
st.write(f"最後更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 精簡關鍵字，增加搜尋命中率
categories = {
    "🌍 總體經濟": "總體經濟 OR 通膨 OR 聯準會",
    "🇺🇸 美股重大新聞": "美股 OR 標普500 OR Nvidia",
    "🇹🇼 台股重大新聞": "台股 OR 台積電",
    "🇯🇵 日股重大新聞": "日股 OR 日經225 OR 日圓"
}

tabs = st.tabs(list(categories.keys()))

for i, (name, query) in enumerate(categories.items()):
    with tabs[i]:
        articles = get_google_news(query)
        if not articles:
            # 如果 24 小時內沒新聞，嘗試擴大到 2 天 (when:2d)
            st.info(f"🔍 正在嘗試擴大搜尋範圍...")
            alt_query = urllib.parse.quote(query)
            articles = feedparser.parse(f"https://news.google.com/rss/search?q={alt_query}+when:2d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant").entries[:5]
        
        if articles:
            for entry in articles:
                with st.container():
                    st.markdown(f"### [{entry.title}]({entry.link})")
                    st.caption(f"📅 {entry.published}  |  來源：{getattr(entry, 'source', {'title': 'Google News'}).get('title')}")
                    st.divider()
        else:
            st.warning(f"目前暫無 {name} 的相關新聞，請稍後再試。")
