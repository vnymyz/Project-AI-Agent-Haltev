# TABLE RENDERER MODULE RINGKAS
def render_summary_table(df):
    if df.empty:
        return "Data tidak ditemukan."

    html = "<table class='employee-table'>"
    html += """
    <tr>
        <th>Nama</th>
        <th>Umur</th>
        <th>Posisi</th>
        <th>Kontrak</th>
        <th>Gaji</th>
        <th>Status</th>
    </tr>
    """

    for _, row in df.iterrows():
        html += f"""
        <tr>
            <td>{row['nama_lengkap'].title()}</td>
            <td>{row['umur']}</td>
            <td>{row['posisi_pekerjaan'].title()}</td>
            <td>{row['tipe_kontrak'].title()}</td>
            <td>Rp {int(row['gaji']):,}</td>
            <td>{row['status_kerja'].title()}</td>
        </tr>
        """

    html += "</table>"
    return html

# DETAIL TABLE RENDERER
def render_detail_table(df):
    if df.empty:
        return "Data tidak ditemukan."

    html = "<table class='employee-table detail'>"

    # header
    html += "<tr>"
    for col in df.columns:
        html += f"<th>{col.replace('_', ' ').title()}</th>"
    html += "</tr>"

    # rows
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            html += f"<td>{row[col]}</td>"
        html += "</tr>"

    html += "</table>"
    return html
