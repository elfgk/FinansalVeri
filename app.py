from csv import excel
import pandas as pd
import yfinance as yf
from datetime import date
from io import BytesIO
import streamlit as st

st.set_page_config(page_title='Hisse Senedi Grafiği')

# Hisse senetleri listesi


# CSV dosyasını okuma
df = pd.read_csv(r'C:\Users\LENOVO\PycharmProjects\finansalveri\name.csv',encoding='windows-1254',delimiter=';')


# Şirketler ve Kodlar ile bir sözlük oluşturma
stocks = dict(zip(df['sembol'], df['sembol_kodu']))


# Kullanıcının hisse senedi seçmesi için selectbox
sembol = st.sidebar.selectbox("Hisse Senedi Seçiniz", options=list(stocks.keys()))
sembol_kodu = stocks[sembol]
st.title(f"{sembol} ({sembol_kodu}) Hisse Senedi Grafiği")

start_date = st.sidebar.date_input('Başlangıç Tarihi', value=date(2023, 1, 1))
end_date = st.sidebar.date_input('Bitiş Tarihi', value=date.today())

# Tarih kontrolü
if start_date > end_date:
    st.error('Başlangıç tarihi bitiş tarihinden sonra olamaz.')
else:
    # Veri çekme işlemi
    df = yf.download(sembol_kodu, start=start_date, end=end_date)

    if df.empty:
        st.warning('Seçilen sembol ve tarih aralığı için veri bulunamadı.')
    else:
        # Zaman dilimi bilgisini kaldırma
        df.index = df.index.tz_localize(None)

        # Veri çerçevesini gösterme
        st.subheader('Hisse Senedi Verileri')
        st.write(df)

        # Grafik çizme
        st.subheader('Kapanış Fiyatı Grafiği')
        st.line_chart(df['Close'])

        # Excel dosyasını indirme
        st.subheader('Hisse Senedi Verileri Excel Dosyası')

        def to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=True, sheet_name='Sheet1')
            writer.close()
            processed_data = output.getvalue()
            return processed_data

        excel_data = to_excel(df)
        st.download_button(
            label='Excel olarak indir',
            data=excel_data,
            file_name=f'{sembol_kodu}_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )