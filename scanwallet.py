
with open("wallet_999_eoa.txt", "r") as file_all:
    all_wallets = set(line.strip().lower() for line in file_all)


with open("user.txt", "r") as file_ref:
    ref_wallets = set(line.strip().lower() for line in file_ref)


matching_wallets = all_wallets.intersection(ref_wallets)


with open("elig.txt", "w") as output:
    for wallet in matching_wallets:
        output.write(wallet + "\n")

print(f"✅ Ditemukan {len(matching_wallets)} wallet cocok.")
print("📁 Disimpan ke file: elig.txt")
