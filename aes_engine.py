import base64

# ================= CÁC BẢNG TRA CHUẨN (CONSTANTS) =================

SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

ISBOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

# ================= CÁC HÀM BIẾN ĐỔI CƠ BẢN (TRANSFORMATIONS) =================

def sub_bytes(state):
    """Thay thế từng byte trong khối trạng thái bằng giá trị tương ứng trong SBOX."""
    return [SBOX[b] for b in state]

def inv_sub_bytes(state):
    """Thay thế từng byte trong khối trạng thái bằng giá trị tương ứng trong ISBOX."""
    return [ISBOX[b] for b in state]

def shift_rows(state):
    """Thực hiện hoán vị các hàng theo chuẩn AES (Column-major storage)."""
    return [
        state[0], state[5], state[10], state[15],
        state[4], state[9], state[14], state[3],
        state[8], state[13], state[2], state[7],
        state[12], state[1], state[6], state[11]
    ]

def inv_shift_rows(state):
    return [
        state[0],  state[13], state[10], state[7],
        state[4],  state[1],  state[14], state[11],
        state[8],  state[5],  state[2],  state[15],
        state[12], state[9],  state[6],  state[3]
    ]

def xtime(a):
    """Phép nhân nhân với x trong trường hữu hạn GF(2^8)."""
    return ((a << 1) ^ 0x1B) & 0xFF if (a & 0x80) else (a << 1) & 0xFF

# Helper functions for InvMixColumns - multiplication by 0e, 0b, 0d, 09
def mul_by_02(a): return xtime(a)
def mul_by_03(a): return xtime(a) ^ a

def mul_by_09(a):
    return xtime(xtime(xtime(a))) ^ a
def mul_by_0b(a):
    return xtime(xtime(xtime(a))) ^ xtime(a) ^ a
def mul_by_0d(a):
    return xtime(xtime(xtime(a))) ^ xtime(xtime(a)) ^ a
def mul_by_0e(a):
    return xtime(xtime(xtime(a))) ^ xtime(xtime(a)) ^ xtime(a)

def mix_single_column(a):
    """Trộn một cột duy nhất (thao tác lõi của MixColumns)."""
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)
    return a

def inv_mix_single_column(a):
    """Giải trộn một cột duy nhất (thao tác lõi của InvMixColumns)."""
    b0 = mul_by_0e(a[0]) ^ mul_by_0b(a[1]) ^ mul_by_0d(a[2]) ^ mul_by_09(a[3])
    b1 = mul_by_09(a[0]) ^ mul_by_0e(a[1]) ^ mul_by_0b(a[2]) ^ mul_by_0d(a[3])
    b2 = mul_by_0d(a[0]) ^ mul_by_09(a[1]) ^ mul_by_0e(a[2]) ^ mul_by_0b(a[3])
    b3 = mul_by_0b(a[0]) ^ mul_by_0d(a[1]) ^ mul_by_09(a[2]) ^ mul_by_0e(a[3])
    return [b0, b1, b2, b3]

def mix_columns(state):
    """Thực hiện trộn 4 cột để tạo tính khuếch tán dữ liệu."""
    new_state = []
    for i in range(4):
        column = state[i*4 : i*4+4]
        new_state.extend(mix_single_column(column))
    return new_state

def inv_mix_columns(state):
    """Thực hiện giải trộn 4 cột."""
    new_state = []
    for i in range(4):
        column = state[i*4 : i*4+4]
        new_state.extend(inv_mix_single_column(column))
    return new_state

def add_round_key(state, round_key):
    """XOR khối dữ liệu với khóa vòng hiện tại."""
    return [s ^ k for s, k in zip(state, round_key)]

# ================= MỞ RỘNG KHÓA (KEY EXPANSION) =================

def key_expansion(key):
    """Tạo lộ trình khóa (Key Schedule) cho AES-128, 192 hoặc 256."""
    Nk = len(key) // 4
    Nr = Nk + 6
    w = [list(key[i:i+4]) for i in range(0, len(key), 4)]

    for i in range(Nk, 4 * (Nr + 1)):
        temp = w[i-1][:]
        if i % Nk == 0:
            # Quy trình: RotWord -> SubWord -> XOR với RCON
            temp = [SBOX[b] for b in (temp[1:] + temp[:1])]
            temp[0] ^= RCON[i // Nk]
        elif Nk > 6 and i % Nk == 4:
            # Bước SubWord bổ sung dành riêng cho AES-256
            temp = [SBOX[b] for b in temp]

        w.append([w[i-Nk][j] ^ temp[j] for j in range(4)])

    # Nhóm các word thành từng khối khóa vòng 16-byte
    return [sum(w[i:i+4], []) for i in range(0, 4 * (Nr + 1), 4)]

# ================= QUY TRÌNH MÃ HÓA CHÍNH (MAIN ENCRYPTION) =================

def aes_encrypt_block(plaintext, key):
    """Mã hóa một khối 16-byte duy nhất sử dụng khóa đã chọn."""
    state = list(plaintext)
    round_keys = key_expansion(key)
    Nr = len(round_keys) - 1

    # Bước khởi tạo
    state = add_round_key(state, round_keys[0])

    # Các vòng lặp chính (từ 1 đến Nr-1)
    for r in range(1, Nr):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[r])

    # Vòng cuối cùng (không có bước MixColumns)
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[Nr])

    return bytes(state)

def aes_decrypt_block(ciphertext, key):
    """Giải mã một khối 16-byte duy nhất sử dụng khóa đã chọn."""
    state = list(ciphertext)
    round_keys = key_expansion(key)
    Nr = len(round_keys) - 1

    # Bước khởi tạo (InvAddRoundKey với khóa cuối cùng)
    state = add_round_key(state, round_keys[Nr])

    # Vòng lặp chính ngược (từ Nr-1 xuống 1)
    for r in range(Nr - 1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, round_keys[r])
        state = inv_mix_columns(state)

    # Vòng cuối cùng (không có bước InvMixColumns)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, round_keys[0])

    return bytes(state)

def pkcs7_pad(data, block_size=16):
    """Thêm dữ liệu đệm PKCS7 để đảm bảo độ dài dữ liệu chia hết cho 16."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data):
    """Loại bỏ dữ liệu đệm PKCS7."""
    pad_len = data[-1]
    if pad_len == 0 or pad_len > 16 or not all(x == pad_len for x in data[-pad_len:]):
        # Invalid padding, raise error or handle as needed.
        raise ValueError("Invalid PKCS7 padding")
    return data[:-pad_len]
    
    


import json
import binascii
import base64

def aes_encrypt_block_structured(plaintext, key, block_num):
    state = list(plaintext)
    round_keys = key_expansion(key)
    Nr = len(round_keys) - 1
    block_log = {"block": block_num, "initial_block_data": bytes(plaintext).hex().upper(), "rounds": []}
    state = add_round_key(state, round_keys[0])
    block_log["rounds"].append({"round": 0, "type": "Initial", "AddRoundKey": bytes(state).hex().upper()})
    for r in range(1, Nr):
        round_data = {"round": r}
        state = sub_bytes(state)
        round_data["SubBytes"] = bytes(state).hex().upper()
        state = shift_rows(state)
        round_data["ShiftRows"] = bytes(state).hex().upper()
        state = mix_columns(state)
        round_data["MixColumns"] = bytes(state).hex().upper()
        state = add_round_key(state, round_keys[r])
        round_data["AddRoundKey"] = bytes(state).hex().upper()
        block_log["rounds"].append(round_data)
    round_data = {"round": Nr, "type": "Final"}
    state = sub_bytes(state)
    round_data["SubBytes"] = bytes(state).hex().upper()
    state = shift_rows(state)
    round_data["ShiftRows"] = bytes(state).hex().upper()
    state = add_round_key(state, round_keys[Nr])
    round_data["AddRoundKey"] = bytes(state).hex().upper()
    block_log["rounds"].append(round_data)
    return bytes(state), block_log

def aes_decrypt_block_structured(ciphertext, key, block_num):
    state = list(ciphertext)
    round_keys = key_expansion(key)
    Nr = len(round_keys) - 1
    block_log = {"block": block_num, "initial_block_data": bytes(ciphertext).hex().upper(), "rounds": []}
    state = add_round_key(state, round_keys[Nr])
    block_log["rounds"].append({"round": Nr, "type": "Initial_Inv", "AddRoundKey_Inv": bytes(state).hex().upper()})
    for r in range(Nr - 1, 0, -1):
        round_data = {"round": r}
        state = inv_shift_rows(state)
        round_data["InvShiftRows"] = bytes(state).hex().upper()
        state = inv_sub_bytes(state)
        round_data["InvSubBytes"] = bytes(state).hex().upper()
        state = add_round_key(state, round_keys[r])
        round_data["AddRoundKey_Inv"] = bytes(state).hex().upper()
        state = inv_mix_columns(state)
        round_data["InvMixColumns"] = bytes(state).hex().upper()
        block_log["rounds"].append(round_data)
    round_data = {"round": 0, "type": "Final_Inv"}
    state = inv_shift_rows(state)
    round_data["InvShiftRows"] = bytes(state).hex().upper()
    state = inv_sub_bytes(state)
    round_data["InvSubBytes"] = bytes(state).hex().upper()
    state = add_round_key(state, round_keys[0])
    round_data["AddRoundKey_Inv"] = bytes(state).hex().upper()
    block_log["rounds"].append(round_data)
    return bytes(state), block_log

def process_aes_verbose_json(json_input):
    try:
        params = json.loads(json_input)
        op_choice = str(params.get('operation', '1'))
        data_str = params.get('data', '')
        data_format = str(params.get('data_format', '1'))
        key_str = params.get('key', '')
        k_choice = str(params.get('key_choice', '1'))
        mode_choice = str(params.get('mode', '1'))
        iv_str = params.get('iv', '')
        required_len = 16 if k_choice == '1' else 24 if k_choice == '2' else 32 if k_choice == '3' else 0
        key = key_str.encode()
        if len(key) != required_len: return json.dumps({"status": "error", "message": f"Key length must be {required_len} bytes for choice {k_choice}."})
        if data_format == '1': data_bytes = data_str.encode()
        elif data_format == '2': data_bytes = binascii.unhexlify(data_str.replace(" ", ""))
        elif data_format == '3': data_bytes = base64.b64decode(data_str)
        else: data_bytes = data_str.encode()
        iv = list(iv_str.encode()[:16].ljust(16, b'\x00')) if mode_choice == '2' else None
        structured_logs = []
        output_data = b''
        if op_choice == '1':
            padded_data = pkcs7_pad(data_bytes)
            if mode_choice == '1':
                for i in range(0, len(padded_data), 16):
                    blk_out, blk_log = aes_encrypt_block_structured(padded_data[i:i+16], key, i//16)
                    output_data += blk_out
                    structured_logs.append(blk_log)
            else:
                prev = iv
                for i in range(0, len(padded_data), 16):
                    raw_plain = padded_data[i:i+16]
                    xor_block = bytes([p ^ c for p, c in zip(raw_plain, prev)])
                    blk_out, blk_log = aes_encrypt_block_structured(xor_block, key, i//16)
                    ordered_log = {
                        "block": i//16,
                        "initial_block_data": raw_plain.hex().upper(),
                        "cbc_mode_info": {
                            "iv_or_prev_cipher": bytes(prev).hex().upper(),
                            "xored_result": xor_block.hex().upper()
                        },
                        "rounds": blk_log["rounds"]
                    }
                    output_data += blk_out
                    structured_logs.append(ordered_log)
                    prev = list(blk_out)
            final_result = {"status": "success", "aes_mode": f"AES-{required_len*8}", "result_hex": output_data.hex().upper(), "result_base64": base64.b64encode(output_data).decode(), "logs": structured_logs}
        else:
            if len(data_bytes) % 16 != 0: return json.dumps({"status": "error", "message": "Ciphertext length must be multiple of 16."})
            dec_raw = b''
            if mode_choice == '1':
                for i in range(0, len(data_bytes), 16):
                    curr = data_bytes[i:i+16]
                    blk_out, blk_log = aes_decrypt_block_structured(curr, key, i//16)
                    dec_raw += blk_out
                    structured_logs.append(blk_log)
            else:
                prev = iv
                for i in range(0, len(data_bytes), 16):
                    curr = data_bytes[i:i+16]
                    blk_out, blk_log = aes_decrypt_block_structured(curr, key, i//16)
                    plain_blk = bytes([d ^ p for d, p in zip(blk_out, prev)])
                    ordered_log = {
                        "block": i//16,
                        "initial_block_data": curr.hex().upper(),
                        "cbc_mode_info": {
                            "raw_decrypted_from_core": blk_out.hex().upper(),
                            "iv_or_prev_cipher": bytes(prev).hex().upper(),
                            "final_plain_block": plain_blk.hex().upper()
                        },
                        "rounds": blk_log["rounds"]
                    }
                    dec_raw += plain_blk
                    structured_logs.append(ordered_log)
                    prev = list(curr)
            try:
                final = pkcs7_unpad(dec_raw)
                final_result = {"status": "success", "aes_mode": f"AES-{required_len*8}", "result_ascii": final.decode(errors='ignore'), "result_hex": final.hex().upper(), "logs": structured_logs}
            except: final_result = {"status": "error", "message": "Unpadding failed", "logs": structured_logs}
        return json.dumps(final_result, indent=4, ensure_ascii=False)
    except Exception as e: return json.dumps({"status": "error", "message": str(e)}, indent=4)

