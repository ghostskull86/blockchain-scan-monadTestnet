blacklist = {
    "0x92c2a6a52b7bb3d4bb71c8e0568aea0d388298c7"
}

# Baca isi file user.txt
with open("user.txt", "r") as file:
    wallets = set(line.strip().lower() for line in file)

# Buang wallet yang diblacklist
wallets = wallets - blacklist

# Tulis kembali ke user.txt tanpa wallet yang diblacklist dan duplikat
with open("user.txt", "w") as file:
    for wallet in wallets:
        file.write(wallet + "\n")

print(f"✅ user.txt telah dibersihkan dari duplikat dan wallet blacklist.")
print(f"📌 Total wallet unik (non-blacklist): {len(wallets)}")
