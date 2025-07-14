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

# 📋 삼성전자 & SK하이닉스 주요 지표 (PER/PBR: 고정, 배당수익률/시가총액: 실시간)
st.header("📋 삼성전자 & SK하이닉스 주요 지표")

samsung = yf.Ticker("005930.KS")
skhynix = yf.Ticker("000660.KS")
samsung_info = samsung.info
skhynix_info = skhynix.info

# 고정값
samsung_per, samsung_pbr = 12.1, 1.1
skhynix_per, skhynix_pbr = 8.3, 2.5

# 실시간 값
samsung_div = round(samsung_info.get('dividendYield', 0) * 100, 2) if samsung_info.get('dividendYield') else 0
skhynix_div = round(skhynix_info.get('dividendYield', 0) * 100, 2) if skhynix_info.get('dividendYield') else 0
samsung_mcap = samsung_info.get('marketCap', 'N/A')
skhynix_mcap = skhynix_info.get('marketCap', 'N/A')

samsung_df = pd.DataFrame({
    '지표': ['PER', 'PBR', '배당수익률 (%)', '시가총액'],
    'Samsung Electronics': [samsung_per, samsung_pbr, samsung_div, samsung_mcap]
})

skhynix_df = pd.DataFrame({
    '지표': ['PER', 'PBR', '배당수익률 (%)', '시가총액'],
    'SK hynix': [skhynix_per, skhynix_pbr, skhynix_div, skhynix_mcap]
})

col1, col2 = st.columns(2)
with col1:
    st.subheader("Samsung Electronics")
    st.dataframe(samsung_df)

with col2:
    st.subheader("SK hynix")
    st.dataframe(skhynix_df)

# 📈 최근 1년 주가 그래프 (2-column)
st.header("📈 삼성전자 & SK하이닉스 최근 1년 주가 그래프")

samsung_hist = samsung.history(period="1y")
skhynix_hist = skhynix.history(period="1y")

col3, col4 = st.columns(2)
with col3:
    fig_samsung, ax_samsung = plt.subplots(figsize=(6,4))
    ax_samsung.plot(samsung_hist.index, samsung_hist['Close'], color='blue')
    ax_samsung.set_title("Samsung Electronics")
    ax_samsung.grid(True)
    st.pyplot(fig_samsung)

with col4:
    fig_skhynix, ax_skhynix = plt.subplots(figsize=(6,4))
    ax_skhynix.plot(skhynix_hist.index, skhynix_hist['Close'], color='orange')
    ax_skhynix.set_title("SK hynix")
    ax_skhynix.grid(True)
    st.pyplot(fig_skhynix)

# 📊 월간 수익률 그래프 (2-column)
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
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(axis='y')
    st.pyplot(fig4)

with col6:
    fig5, ax5 = plt.subplots(figsize=(6,4))
    ax5.bar(skhynix_dates, skhynix_return.values, color='orange')
    ax5.set_title("SK hynix Monthly Return (%)")
    ax5.tick_params(axis='x', rotation=45)
    ax5.grid(axis='y')
    st.pyplot(fig5)

st.header("🔧 삼성전자 & SK 하이닉스 안정성/예상 수익률 비교 시뮬레이션")

base_stability, base_return = 50, 5.0

samsung_stability = base_stability + rate * 10 - investor_sentiment * 5
samsung_return_sim = base_return + fx * 2 + investor_sentiment * 1.5

skhynix_stability = base_stability + rate * 5 - investor_sentiment * 3
skhynix_return_sim = base_return + fx * 3 + investor_sentiment * 2.0

labels = ['Samsung Electronics', 'SK hynix']

# 📊 Stability - 하나의 그래프
st.subheader("📊 안정성 점수")

fig_stab, ax_stab = plt.subplots(figsize=(6,4))
ax_stab.bar(labels, [samsung_stability, skhynix_stability], color=['blue', 'orange'], width=0.4)
ax_stab.set_ylim(0, 100)
ax_stab.set_ylabel("Stability Score (0~100)")
for i, v in enumerate([samsung_stability, skhynix_stability]):
    ax_stab.text(i, v + 2, f"{v:.1f}", ha='center')
st.pyplot(fig_stab)

# 📊 Expected Return - 하나의 그래프
st.subheader("📊 예상 수익률")

fig_ret, ax_ret = plt.subplots(figsize=(6,4))
ax_ret.bar(labels, [samsung_return_sim, skhynix_return_sim], color=['blue', 'orange'], width=0.4)
ax_ret.set_ylabel("Expected Return (%)")
for i, v in enumerate([samsung_return_sim, skhynix_return_sim]):
    ax_ret.text(i, v + 0.5, f"{v:.1f}%", ha='center')
st.pyplot(fig_ret)
