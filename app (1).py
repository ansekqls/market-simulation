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

# 🔔 추가: 삼성전자 & SK하이닉스 주요 지표
st.header("📋 삼성전자 & SK하이닉스 주요 지표")

samsung = yf.Ticker("005930.KS")
skhynix = yf.Ticker("000660.KS")

samsung_info = samsung.info
skhynix_info = skhynix.info

def get_value(info, key):
    return info[key] if key in info and info[key] is not None else 'N/A'

samsung_df = pd.DataFrame({
    '지표': ['PER', 'PBR', 'Dividend Yield (%)', 'Market Cap'],
    'Samsung': [
        get_value(samsung_info, 'trailingPE'),
        get_value(samsung_info, 'priceToBook'),
        round(get_value(samsung_info, 'dividendYield')*100, 2) if samsung_info.get('dividendYield') else 0,
        get_value(samsung_info, 'marketCap')
    ]
})

skhynix_df = pd.DataFrame({
    '지표': ['PER', 'PBR', 'Dividend Yield (%)', 'Market Cap'],
    'SK hynix': [
        get_value(skhynix_info, 'trailingPE'),
        get_value(skhynix_info, 'priceToBook'),
        round(get_value(skhynix_info, 'dividendYield')*100, 2) if skhynix_info.get('dividendYield') else 0,
        get_value(skhynix_info, 'marketCap')
    ]
})

st.subheader("Samsung Electronics")
st.dataframe(samsung_df)

st.subheader("SK hynix")
st.dataframe(skhynix_df)

# 🔔 추가: 3개월 단위 수익률 그래프
st.header("📊 삼성전자 & SK하이닉스 3개월(분기) 수익률")

samsung_hist = samsung.history(period="1y")
skhynix_hist = skhynix.history(period="1y")

samsung_quarter = samsung_hist['Close'].resample('Q').last()
skhynix_quarter = skhynix_hist['Close'].resample('Q').last()

samsung_return = samsung_quarter.pct_change().dropna() * 100
skhynix_return = skhynix_quarter.pct_change().dropna() * 100

samsung_dates = samsung_return.index.strftime('%Y-Q%q')
skhynix_dates = skhynix_return.index.strftime('%Y-Q%q')

fig, ax = plt.subplots(figsize=(10,4))
ax.bar(samsung_dates, samsung_return.values, color='skyblue')
ax.set_title("Samsung
fig, ax = plt.subplots(figsize=(10,4)")
ax.bar(samsung_dates, samsung_return.values, color='skyblue')
ax.set_title("Samsung Electronics Quarterly Return (%)")
ax.set_xlabel("Quarter")
ax.set_ylabel("Return (%)")
ax.grid(axis='y')
st.pyplot(fig)

fig2, ax2 = plt.subplots(figsize=(10,4))
ax2.bar(skhynix_dates, skhynix_return.values, color='orange')
ax2.set_title("SK hynix Quarterly Return (%)")
ax2.set_xlabel("Quarter")
ax2.set_ylabel("Return (%)")
ax2.grid(axis='y')
st.pyplot(fig2)
