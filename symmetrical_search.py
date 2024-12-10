import random
import time
import json
import os
import requests
from mnemonic import Mnemonic
import bip32utils

# Load BIP-39 wordlist
def load_wordlist(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f]

# Generate wallet address using BIP-32 from mnemonic
def generate_wallet_from_mnemonic(mnemonic_phrase, num_addresses=10):
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic_phrase)
    master_key = bip32utils.BIP32Key.fromEntropy(seed)
    
    addresses = []
    for i in range(num_addresses):
        child_key = master_key.ChildKey(i)
        addresses.append(child_key.Address())
    return addresses

# Check balance and transaction history of an address using an API
def check_balance_and_history(address):
    try:
        # Blockstream API for Bitcoin balances
        url = f"https://blockstream.info/api/address/{address}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            confirmed = data.get("chain_stats", {}).get("funded_txo_sum", 0)
            spent = data.get("chain_stats", {}).get("spent_txo_sum", 0)
            tx_count = data.get("chain_stats", {}).get("tx_count", 0)
            balance = confirmed - spent
            return balance, tx_count
        else:
            print(f"Error fetching data for {address}: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return None, None

# Save not_found_seeds to a JSON file
def save_not_found_seeds(seeds, filename="not_found_seeds.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            existing_seeds = json.load(f)
    else:
        existing_seeds = []

    updated_seeds = list(set(existing_seeds + seeds))  # Avoid duplicates
    with open(filename, "w") as f:
        json.dump(updated_seeds, f, indent=4)
    print(f"Saved {len(seeds)} seeds to {filename}.")

# Load not_found_seeds from a JSON file
def load_not_found_seeds(filename="not_found_seeds.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return set(json.load(f))
    return set()

# Generate a random BIP-39 mnemonic phrase
def generate_random_mnemonic(bip39_wordlist, num_words=12):
    return " ".join(random.choices(bip39_wordlist, k=num_words))

# Symmetrical search function
def symmetrical_search(bip39_wordlist, attempts=10, num_addresses=10, not_found_file="not_found_seeds.json"):
    not_found_seeds = load_not_found_seeds(not_found_file)
    new_not_found_seeds = []
    suspected_tx_seeds = []

    print("Starting symmetrical search...")
    for attempt in range(attempts):
        mnemonic_phrase = generate_random_mnemonic(bip39_wordlist, num_words=12)
        
        # Skip testing if mnemonic is already marked as "not found"
        if mnemonic_phrase in not_found_seeds:
            print(f"Skipping known not_found seed: {mnemonic_phrase}")
            continue

        print(f"Testing mnemonic #{attempt + 1}: {mnemonic_phrase}")
        try:
            addresses = generate_wallet_from_mnemonic(mnemonic_phrase, num_addresses=num_addresses)
            balance_found = False

            for idx, address in enumerate(addresses):
                print(f"Checking address {idx+1}/{len(addresses)}: {address}")
                balance, tx_count = check_balance_and_history(address)

                if balance is not None:
                    if balance > 0:
                        print(f"Address: {address}, Balance: {balance} satoshis, Transactions: {tx_count}")
                        balance_found = True
                    elif tx_count > 0:
                        print(f"Address: {address} has transactions but no balance. Storing seed for variations.")
                        suspected_tx_seeds.append(mnemonic_phrase)
                
                time.sleep(1)  # Respect API rate limits

            if not balance_found:
                print(f"No balance found for mnemonic: {mnemonic_phrase}. Adding to not_found_seeds.")
                new_not_found_seeds.append(mnemonic_phrase)
            
            print("-" * 50)
        
        except Exception as e:
            print(f"Error with mnemonic: {mnemonic_phrase} | {str(e)}")
            continue

    # Save new not_found_seeds to file
    save_not_found_seeds(new_not_found_seeds, not_found_file)

    return suspected_tx_seeds

if __name__ == "__main__":
    # Load BIP-39 wordlist
    bip39_wordlist = load_wordlist("english.txt")

    # Run symmetrical search
    suspected_tx_seeds = symmetrical_search(bip39_wordlist, attempts=10, num_addresses=10)

    print("\nSeeds with suspected transaction history:")
    print(suspected_tx_seeds)
