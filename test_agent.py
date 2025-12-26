from agent.agent import ai_agent

tests = [
    "berapa lama Andi bekerja",
    "gaji Budi berapa",
    "izin sakit Rizky",
    "izin tanpa keterangan Agus",
    "cuti Siti",
    "posisi pekerjaan Dewi",
    "status kerja Eko",
    "data lengkap Maya",
    "berapa gaji Lina",
    "berapa lama Ilham bekerja",
    "data lengkap karyawan fiktif"
]

for t in tests:
    print("Q:", t)
    print("A:", ai_agent(t))
    print("-" * 50)
