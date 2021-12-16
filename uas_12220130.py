#Nama : Jasmine Christiana Manihuruk
#NIM  : 12220130
#Deskripsi Program : Aplikasi web-based sebagai alat untuk mengecek data produksi minyak, menggunakan GUI berbasis
#streamlit, dilengkapi fitur2 seperti yang ada di dalam file panduan UAS IF2112

import pandas as pd
import streamlit as st
import altair as alt
import json

# Data load
df = pd.read_csv('produksi_minyak_mentah.csv', index_col="kode_negara")
dfListNeg = pd.read_json("kode_negara_lengkap.json")
nd_al3 = {negara['alpha-3']:negara for negara in json.loads(open("kode_negara_lengkap.json").read())}
nd_name = {negara['name']:negara for negara in json.loads(open("kode_negara_lengkap.json").read())}

for al3code in df.index.unique().tolist():
    if al3code not in dfListNeg['alpha-3'].tolist():
        df.drop([al3code], inplace=True)
df.reset_index(inplace=True)

# Fungsi yang diperlukan
def show_altair_bar(df, x, y):
    st.altair_chart(alt.Chart(df[[x, y]]).mark_bar().encode(
        x=alt.X(x, sort=None),
        y=y
        ), use_container_width=True)

# Container
navbar = st.container()
judul = st.container()
graphminsemua = st.container()
grafmintahunan = st.container()
grafminterbesar = st.container()
infonegara = st.container()

# Fitur tambahan navbar( menu navigasi)
with navbar:
    st.sidebar.markdown("# Menu Navigasi")
    st.sidebar.markdown("#### Pergi ke:")
    st.sidebar.markdown("[Grafik produksi tiap negara](#produksi-per-negara)")
    st.sidebar.markdown("[Grafik produsen terbesar tahunan](#produksi-minyak-terbesar-tahunan)")
    st.sidebar.markdown("[Grafik produsen minyak terbesar](#produsen-minyak-terbesar)")
    st.sidebar.markdown("[Filter dan info negara](#filter-dan-info-negara)")

with judul:
    st.title("DATA PRODUKSI MINYAK BERBAGAI NEGARA")
    st.write('Lihat semua data produksi minyak di semua negara!')
    st.markdown("***")
    st.info('Untuk melakukan navigasi ke fitur-fitur yang ada, tekan tanda panah di pojok kiri atas!')

# Interface tambahan yaitu gambar
st.markdown(
        """
        <style>
        .reportview-container {
            background: url("https://photoeverywhere.co.uk/west/usa/california/sunset_oil_rigDSC_4701.jpg")
        }
    .sidebar .sidebar-content {
            background: url("https://wallpaperaccess.com/full/2959083.jpg")
        }
        </style>
        """,
        unsafe_allow_html=True
    )
  
# Soal A produksi per negara
with graphminsemua:
    st.markdown('***')
    st.title("Produksi per negara")
    
    lnegara = [nd_al3[kode]['name'] for kode in df['kode_negara'].unique().tolist()]
    lnegara.insert(0, 'Pilih negara...')
    # User input
    sel_negara = st.selectbox("Pilih negara", lnegara)
    if sel_negara != 'Pilih negara...':
        code = nd_name[sel_negara]['alpha-3']
        disp_data = df[df["kode_negara"] == code][['tahun', 'produksi']]
        disp_data = disp_data.set_index('tahun')
        st.line_chart(disp_data)
        with st.expander('Lihat tabel'):
            st.write(disp_data)
    else:
        st.info('Pilih negara yang ingin anda cek!')
    st.markdown('***')
    
# Soal B produksi minyak negara tahunan
with grafmintahunan:
    st.markdown("***")
    st.title('Produksi minyak terbesar tahunan')
    year = df["tahun"]
    # User input
    y = st.slider('Tahun', min(year), max(year))
    n = st.number_input('Jumlah peringkat', value=5, step=1)

    prod_minyak_thn_ke_n = df.loc[df["tahun"] == y].sort_values('produksi', ascending=False)[:int(n)] 
    prod_minyak_thn_ke_n = prod_minyak_thn_ke_n.reset_index(drop=True)
    prod_minyak_thn_ke_n.index = prod_minyak_thn_ke_n.index + 1
    show_altair_bar(prod_minyak_thn_ke_n, 'kode_negara', 'produksi')
    with st.expander('Lihat tabel'):
        st.dataframe(prod_minyak_thn_ke_n)
        
# Soal C produksi minyak negara total
with grafminterbesar:
    st.markdown('***')
    st.title('Produsen minyak terbesar')
    input_rank = st.number_input('Jumlah negara', value=10, step=1)#user input
    sum_prod = (df[['kode_negara', 'produksi']].groupby('kode_negara', as_index=False).sum().sort_values(['produksi'], ascending=[0])).reset_index(drop=True)
    sum_prod = sum_prod[:int(input_rank)].reset_index(drop=True)
    sum_prod_disp = sum_prod[['kode_negara', 'produksi']]
    sum_prod_disp.index = sum_prod_disp.index + 1
    show_altair_bar(sum_prod_disp, 'kode_negara', 'produksi')
    with st.expander('Lihat tabel'):
        st.write(sum_prod_disp)
    st.markdown('***')

# Fungsi untuk menampilkan tabel untuk infonegara
def show_table_filter(df, dfid):
    row = df[dfid:dfid+1]
    kode_negara = row['kode_negara'].values[0]
    nama_negara = dfListNeg[dfListNeg["alpha-3"] == kode_negara]["name"].values[0]
    region_negara = dfListNeg[dfListNeg["name"] == nama_negara]["region"].values[0]
    sub_ = dfListNeg[dfListNeg["name"] == nama_negara]["sub-region"].values[0]
    nMaxProduksi = row['produksi'].values[0]
    out = pd.DataFrame()
    out['Nama'] = out.append({'Nama':nama_negara}, ignore_index=True)
    out['Kode'] = kode_negara
    out['Region'] = region_negara
    out['Sub-region'] = sub_
    out['Produksi'] = nMaxProduksi
    st.dataframe(out)

# Soal D info negara berdasarkan produksi dan waktu
with infonegara:
    st.markdown('***')
    st.title('Filter dan info negara')
    # User input
    filt1 = st.selectbox('Jumlah produksi', ['Terbanyak', 'Paling sedikit', 'Tidak ada produksi'])
    filt2 = st.selectbox('Jangka waktu', ['Keseluruhan', 'Tahun spesifik'])
    if filt1 == 'Terbanyak': # alur terbanyak
        if filt2 == 'Tahun spesifik': # alur tahun
            input_thn = st.slider('Tahun yang akan dicek untuk produksi maksimum', min_value=1971, max_value=2020)
            if input_thn == 0:
                st.info('Masukkan tahun yang valid!')
            dfMaxID = df[df['tahun'] == int(input_thn)]['produksi'].idxmax()
            show_table_filter(df, dfMaxID) # show tabel dari dataframe global dan index
        elif filt2 == 'Keseluruhan': # alur keseluruhan
            dfMaxID = df['produksi'].idxmax()
            show_table_filter(df, dfMaxID) # show tabel dari dataframe global dan index
    elif filt1 == 'Paling sedikit': # alur sedikit bukan 0 
        if filt2 == 'Tahun spesifik':
            userTahunInputMin = st.slider('Tahun yang akan dicek untuk produksi minimum', min_value=1971, max_value=2020)
            if userTahunInputMin == 0:
                st.info('Masukkan tahun yang valid!')
            dfMinF = df[df['tahun'] == int(userTahunInputMin)]
            dfMinF = dfMinF[dfMinF['produksi'] != 0]
            dfMinID = dfMinF['produksi'].idxmin()
            show_table_filter(dfMinF, dfMinID) # show tabel dari dataframe lokal dfMinF dan index        
        elif filt2 == 'Keseluruhan':
            dfMinF = df[df['produksi'] > 0]
            dfMinF.reset_index(inplace=True)
            dfMinID = dfMinF['produksi'].idxmin()
            show_table_filter(dfMinF, dfMinID) # show tabel dari dataframe lokal dfMinF dan index    
    elif filt1 == 'Tidak ada produksi': # alur nol tidak produksi
        df_no_prod= df[df['produksi'] == 0]
        df_no_prod.reset_index(inplace=True)
        #buat list kosong
        nama = []
        region = []
        subregion = []
        for _, row in df_no_prod.iterrows():# iterate through rows, tambah ke list sesuai nama
            kode = row['kode_negara']
            nama.append(dfListNeg[dfListNeg['alpha-3'] == kode]['name'].values[0])
            region.append(dfListNeg[dfListNeg['alpha-3'] == kode]['region'].values[0])
            subregion.append(dfListNeg[dfListNeg['alpha-3'] == kode]['sub-region'].values[0])
        # Tambah kolom baru
        df_no_prod['Nama'] = nama
        df_no_prod['Region'] = region
        df_no_prod['Subregion'] = subregion
        if filt2 == 'Tahun spesifik':
            # User input
            input_thn = st.slider('Tahun yang akan dicek untuk produksi kosong', min_value=1971, max_value=2020, value=1972)
            disp_df_no_prod = df_no_prod[df_no_prod['tahun'] == int(input_thn)] # ambil row dengan tahun sekian
            disp_df_no_prod.reset_index(inplace=True)
            # Show bagian yang di filter
            st.dataframe(disp_df_no_prod.filter(items=['Nama', 'kode_negara', 'Region', 'Subregion']))
        elif filt2 == 'Keseluruhan':
            # Show dataframe tanpa duplikat dan index
            st.dataframe(df_no_prod.filter(items=['Nama', 'kode_negara', 'Region', 'Subregion']).drop_duplicates().drop(index=0).reset_index(drop=True))
            
st.write('Jasmine Christiana Manihuruk | 12220130@mahasiswa.itb.ac.id') 
    
