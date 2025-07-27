import random

def add_token_nominals(input_file="rawuser.txt", output_file="nomuser.txt", integer_part=1):
    added_nominals = set()
    output_lines = []

    try:
        with open(input_file, 'r') as infile:
            wallets = [line.strip() for line in infile if line.strip()]

        if not wallets:
            print(f"File '{input_file}' kosong atau tidak berisi alamat wallet.")
            return

        for wallet in wallets:
            while True:
                decimal_part = ''.join(random.choices('0123456789', k=5))
                nominal_str = f"{integer_part}.{decimal_part}"

                if nominal_str not in added_nominals:
                    added_nominals.add(nominal_str)
                    # Perubahan di sini: menambahkan ", " dan spasi setelah wallet
                    output_lines.append(f"{wallet}, {nominal_str}")
                    break
                else:
                    continue

        with open(output_file, 'a') as outfile:
            for line in output_lines:
                outfile.write(line + '\n')

        print(f"Berhasil menambahkan nominal ke {len(wallets)} wallet dan menyimpannya di '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' tidak ditemukan. Pastikan file berada di direktori yang sama.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    # Contoh penggunaan:
    # Mengatur bagian bulat dari nominal menjadi 10
    add_token_nominals(integer_part=2)