import streamlit as st

# Define the pages
main_page = st.Page("main_page.py", title="Main Page", icon="🎈")
page_2 = st.Page("boss_ask.py", title="老板问数助手", icon="❄️")
page_3 = st.Page("ask_excel.py", title="EXCEL数据分析助手", icon="🎉")
page_4 = st.Page("ask_indices.py", title="指标问答助手", icon="🎉")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3, page_4])

# Run the selected page
pg.run()