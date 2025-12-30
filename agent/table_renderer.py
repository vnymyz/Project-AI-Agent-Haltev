def render_table(df):
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
