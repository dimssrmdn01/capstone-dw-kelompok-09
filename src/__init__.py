def validasi_silver(df):
    hasil = {}

    # 1. Validasi rentang persen
    persen = df[
        df["seri_kode"].isin(
            ["var1447", "var1451", "var1221"]
        )
    ]

    hasil["rentang_persen"] = (
        persen["nilai"].between(0, 100).all()
    )

    # 2. Validasi APK PAUD
    apk = df[df["seri_kode"] == "var1439"]

    hasil["rentang_apk"] = (
        (apk["nilai"] >= 0).all()
    )

    # 3. Validasi keunikan Silver
    kunci = [
        "sumber",
        "seri_kode",
        "wilayah_kode",
        "periode",
        "jenis_periode",
        "rincian",
        "_berkas_raw"
    ]

    hasil["keunikan_silver"] = (
        ~df.duplicated(subset=kunci).any()
    )

    # 4. Validasi konsistensi satuan
    hasil["konsistensi_satuan"] = (
        df.groupby("seri_kode")["satuan"]
        .nunique().le(1).all()
    )

    return hasil