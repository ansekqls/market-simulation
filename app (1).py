import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="시장 시뮬레이터", layout="wide")
st.title("🧠 시장 변동 시뮬레이터 기반 투자 전략 분석")

# 🔧 시장 변수
st.sidebar.header("🔧 시장 변수 조정")
rate = st.sidebar.slider("기준금리 변화 (%)", -2.0, 2.0, 0.0, 0.25)
oil = st.sidebar.slider("국제유가 변화율 (%)", -20.0, 20.0, 0.0, 1.0)
fx = st.sidebar.slider("환율 변화율 (%)", -10.0, 10.0, 0.0, 0.5)
consumer_index = st.sidebar.slider("소비심리지수 변화", -5.0, 5.0, 0.0, 1.0)
investor_sentiment = st.sidebar.slider("투자심리지수 변화", -5.0, 5.0, 0.0, 1.0)

sector_data = {
    '은행': rate * 1.5 + fx * 0.5,
    '건설': -rate * 1.2 - oil * 0.3,
    '에너지': oil * 1.0,
    'IT': -rate * 0.5 + fx * 0.8,
    '소비재': consumer_index * 1.2,
    '반도체': fx * 1.5 - rate * 0.4
}

st.subheader("📊 산업별 영향 예측")
sector_df = pd.DataFrame.from_dict(sector_data, orient='index', columns=['영향도'])
sector_df['영향도'] = sector_df['영향도'].round(2)
st.bar_chart(sector_df)

st.subheader("📈 추천 투자 전략")
if sector_df['영향도'].max() > 0:
    best_sector = sector_df['영향도'].idxmax()
    st.success(f"✅ 유리한 산업: {best_sector} → 관련 ETF/테마주에 주목")
else:
    st.warning("📉 모든 산업이 부정적 영향을 받는 상황입니다.")

st.subheader("📝 요약 리포트")
best_sector = best_sector if sector_df['영향도'].max() > 0 else "없음"
st.markdown(f"""
- **기준금리 변화**: `{rate}`%
- **유가 변화**: `{oil}`%
- **환율 변화**: `{fx}`%
- **소비심리 변화**: `{consumer_index}`
- **투자심리 변화**: `{investor_sentiment}`

**예상 유리 산업**: `{best_sector}`

👉 관련 ETF: KODEX {best_sector}, TIGER {best_sector}
""")

# 🔔 삼성전자 & SK하이닉스 주요 지표 (하드코딩된 값 사용)
st.header("📋 삼성전자 & SK하이닉스 주요 지표 (고정값)")

samsung_df = pd.DataFrame({
    '지표': ['PER', 'PBR'],
    'Samsung Electronics': [12.1, 1.1]
})

skhynix_df = pd.DataFrame({
    '지표': ['PER', 'PBR'],
    'SK hynix': [8.3, 2.5]
})

col1, col2 = st.columns(2)
with col1:
    st.subheader("Samsung Electronics")
    st.dataframe(samsung_df)

with col2:
    st.subheader("SK hynix")
    st.dataframe(skhynix_df)

# 🔔 주가 데이터 다운로드
samsung = yf.Ticker("005930.KS")
skhynix = yf.Ticker("000660.KS")
samsung_hist = samsung.history(period="1y")
skhynix_hist = skhynix.history(period="1y")

# 📈 최근 1년 주가 그래프 → 2-column
st.header("📈 삼성전자 & SK하이닉스 최근 1년 주가 그래프")

col3, col4 = st.columns(2)
with col3:
    fig_samsung, ax_samsung = plt.subplots(figsize=(6,4))
    ax_samsung.plot(samsung_hist.index, samsung_hist['Close'], color='blue')
    ax_samsung.set_title("Samsung Electronics")
    ax_samsung.set_xlabel("Date")
    ax_samsung.set_ylabel("Close Price (KRW)")
    ax_samsung.grid(True)
    st.pyplot(fig_samsung)

with col4:
    fig_skhynix, ax_skhynix = plt.subplots(figsize=(6,4))
    ax_skhynix.plot(skhynix_hist.index, skhynix_hist['Close'], color='orange')
    ax_skhynix.set_title("SK hynix")
    ax_skhynix.set_xlabel("Date")
    ax_skhynix.set_ylabel("Close Price (KRW)")
    ax_skhynix.grid(True)
    st.pyplot(fig_skhynix)

# 📊 월간 수익률 그래프 → 2-column
st.header("📊 삼성전자 & SK하이닉스 월간 수익률")

samsung_month = samsung_hist['Close'].resample('M').last()
skhynix_month = skhynix_hist['Close'].resample('M').last()

samsung_return = samsung_month.pct_change().dropna() * 100
skhynix_return = skhynix_month.pct_change().dropna() * 100

samsung_dates = samsung_return.index.strftime('%Y-%m')
skhynix_dates = skhynix_return.index.strftime('%Y-%m')

col5, col6 = st.columns(2)
with col5:
    fig4, ax4 = plt.subplots(figsize=(6,4))
    ax4.bar(samsung_dates, samsung_return.values, color='skyblue')
    ax4.set_title("Samsung Electronics Monthly Return (%)")
    ax4.set_xlabel("Month")
    ax4.set_ylabel("Return (%)")
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(axis='y')
    st.pyplot(fig4)

with col6:
    fig5, ax5 = plt.subplots(figsize=(6,4))
    ax5.bar(skhynix_dates, skhynix_return.values, color='orange')
    ax5.set_title("SK hynix Monthly Return (%)")
    ax5.set_xlabel("Month")
    ax5.set_ylabel("Return (%)")
    ax5.tick_params(axis='x', rotation=45)
    ax5.grid(axis='y')
    st.pyplot(fig5)
