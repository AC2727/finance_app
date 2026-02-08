import streamlit as st
from service import add_transaction, get_transactions, get_summary, get_monthly_report

st.set_page_config(page_title="Kişisel Finans", layout="centered")
st.title("Kişisel Finans Takibi")

income, expense = get_summary()
balance = income - expense

col1, col2, col3 = st.columns(3)

col1.metric("Toplam Gelir", f"{income:.2f} ₺")
col2.metric("Toplam Gider", f"{expense:.2f} ₺")
col3.metric("Bakiye", f"{balance:.2f} ₺")

with st.form("transaction_form"):
    amount = st.number_input("Tutar", min_value=0.0, step=1.0)
    category = st.text_input("Kategori")
    tx_type = st.selectbox("Tür", ["income", "expense"])
    description = st.text_input("Açıklama")

    submitted = st.form_submit_button("Kaydet")

    if submitted:
        add_transaction(amount, category, tx_type, description)
        st.success("Kayıt eklendi!")

st.divider()
st.subheader("Kayıtlar")

transactions = get_transactions()

if transactions:
    for t in transactions:
        amount, category, tx_type, description, created_at = t
        st.write(
            f"{created_at} | {tx_type.upper()} | {category} | {amount} ₺ | {description}"
        )
else:
    st.info("Henüz kayıt yok.")

import pandas as pd

st.divider()
st.subheader("Gelir / Gider Grafiği")

if transactions:
    df = pd.DataFrame(
        transactions,
        columns=["amount", "category", "type", "description", "created_at"]
    )

    summary_df = (
        df.groupby("type", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total"})
    )

    st.bar_chart(summary_df.set_index("type"))
else:
    st.info("Grafik için henüz veri yok.")

import datetime as dt

st.divider()
st.subheader("Aylık Rapor")

today = dt.date.today()

col1, col2 = st.columns(2)
year = col1.selectbox("Yıl", range(today.year - 5, today.year + 1), index=5)
month = col2.selectbox("Ay", range(1, 13), index=today.month - 1)

report = get_monthly_report(year, month)

monthly_income = report["income"]
monthly_expense = report["expense"]
monthly_balance = monthly_income - monthly_expense

c1, c2, c3 = st.columns(3)
c1.metric("Aylık Gelir", f"{monthly_income:.2f} ₺")
c2.metric("Aylık Gider", f"{monthly_expense:.2f} ₺")
c3.metric("Aylık Bakiye", f"{monthly_balance:.2f} ₺")

