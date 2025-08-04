import os
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

# Load 12-word phrase from env variable
mnemonic_phrase = os.environ.get("MNEMONIC_12")

def is_valid_mnemonic(mnemonic_phrase):
    mnemo = Mnemonic("english")
    return mnemo.check(mnemonic_phrase)

def derive_eth_address(mnemonic_phrase):
    seed_bytes = Bip39SeedGenerator(mnemonic_phrase).Generate()
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    return bip44_mst.PublicKey().ToAddress()

if not mnemonic_phrase:
    print("No mnemonic phrase provided in MNEMONIC_12 env variable.")
elif not is_valid_mnemonic(mnemonic_phrase):
    print("❌ Invalid BIP39 mnemonic.")
else:
    eth_address = derive_eth_address(mnemonic_phrase)
    print(f"✅ Valid mnemonic. Derived Ethereum address: {eth_address}")
