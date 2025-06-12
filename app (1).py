import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="시장 시뮬레이터", layout="wide")
st.title("🧠 시장 변동 시뮬레이터 기반 투자 전략 분석")

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
    st.warning("📉 모든 산업이 부정적 영향을 받는 상황입니다. 방어적 포트폴리오를 고려하세요.")

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
