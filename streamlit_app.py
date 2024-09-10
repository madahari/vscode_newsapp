import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import time

# OpenAI API 키 설정
openai_api_key = st.secrets["openai"]["api_key"]
openai.api_key = openai_api_key

# Streamlit 앱 레이아웃
st.title("뉴스 요약 및 알림 앱")
st.write("주로 보는 뉴스 사이트와 관심 주제를 등록하세요.")

# 뉴스 사이트 입력
news_site = st.text_input("뉴스 사이트 URL을 입력하세요:", key="news_site")

# 관심 주제 입력
interest_topic = st.text_input("관심 주제를 입력하세요:", key="interest_topic")

# 뉴스 요약 함수
def summarize_news(content):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"다음 뉴스 내용을 요약해 주세요:\n\n{content}\n\n요약:",
        max_tokens=150
    )
    summary = response.choices[0].text.strip()
    return summary

# 뉴스 크롤링 함수
def fetch_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('h2')  # 뉴스 사이트에 따라 태그가 다를 수 있음
    return [headline.text for headline in headlines]

# 알림 함수
def notify(summary):
    st.write(f"새로운 뉴스 요약: {summary}")

# 주기적으로 뉴스 확인 및 요약
if st.button("뉴스 확인 시작"):
    if news_site and interest_topic:
        while True:
            news_headlines = fetch_news(news_site)
            for headline in news_headlines:
                if interest_topic in headline:
                    summary = summarize_news(headline)
                    notify(summary)
            time.sleep(60)  # 1분마다 뉴스 확인
    else:
        st.warning("뉴스 사이트와 관심 주제를 모두 입력하세요.")
