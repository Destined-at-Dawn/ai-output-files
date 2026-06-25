import sqlcipher3, sqlite3, os, sys

key_db = r'E:\ai产出文件\牛马\创作\创作\.tmp\wechat-key-info-20260607-closed\key_info.db'
conn = sqlite3.connect(key_db)
cursor = conn.cursor()
cursor.execute('SELECT key_info_data FROM LoginKeyInfoTable')
rows = cursor.fetchall()
conn.close()
blob = rows[0][0]
inner = blob[3:171]  # 168 bytes

enc_db = r'E:\ai产出文件\牛马\创作\创作\output\databases\latest\message\message_0.db'

best_err = None
for row_idx, (blob,) in enumerate(rows[:3]):
    inner = blob[3:171]
    for offset in [0, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]:
        for key_len in [32, 64]:
            key_bytes = inner[offset:offset+key_len]
            if len(key_bytes) != key_len:
                continue
            for kdf_iter in [4000, 64000, 256000]:
                for page_size in [1024, 4096, 65536]:
                    for hmac in ['HMAC_SHA1', 'HMAC_SHA256', 'HMAC_SHA512']:
                        try:
                            conn2 = sqlcipher3.connect(enc_db)
                            c = conn2.cursor()
                            c.execute(f"PRAGMA key=\"x'{key_bytes.hex()}'\"")
                            c.execute(f'PRAGMA cipher_page_size={page_size}')
                            c.execute(f'PRAGMA kdf_iter={kdf_iter}')
                            c.execute(f'PRAGMA cipher_hmac_algorithm={hmac}')
                            c.execute('PRAGMA cipher_kdf_algorithm=PBKDF2_HMAC_SHA1')
                            c.execute("SELECT COUNT(*) FROM sqlite_master")
                            count = c.fetchone()[0]
                            conn2.close()
                            if count > 0:
                                print(f'SUCCESS! row={row_idx} offset={offset} len={key_len} kdf={kdf_iter} ps={page_size} hmac={hmac}')
                                sys.exit(0)
                        except Exception as e:
                            try: conn2.close()
                            except: pass

print('No combination worked with brute force')
print(f'Tested with keys from {len(rows)} rows')

# Try alternative: maybe the key is the raw key_info_data without protobuf header
print('\nTrying raw key_info_data directly...')
for row_idx, (blob,) in enumerate(rows[:3]):
    for kdf_iter in [4000, 64000]:
        for page_size in [4096]:
            try:
                conn2 = sqlcipher3.connect(enc_db)
                c = conn2.cursor()
                c.execute(f"PRAGMA key=\"x'{blob.hex()}'\"")
                c.execute(f'PRAGMA cipher_page_size={page_size}')
                c.execute(f'PRAGMA kdf_iter={kdf_iter}')
                c.execute('PRAGMA cipher_hmac_algorithm=HMAC_SHA1')
                c.execute('PRAGMA cipher_kdf_algorithm=PBKDF2_HMAC_SHA1')
                c.execute("SELECT COUNT(*) FROM sqlite_master")
                count = c.fetchone()[0]
                conn2.close()
                if count > 0:
                    print(f'SUCCESS raw blob! row={row_idx} kdf={kdf_iter}')
                    sys.exit(0)
            except:
                try: conn2.close()
                except: pass

print('Raw blob also failed')
