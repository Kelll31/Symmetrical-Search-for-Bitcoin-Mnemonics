# Symmetrical Search for Bitcoin Mnemonics

This project generates random BIP-39 mnemonic phrases, derives wallet addresses using BIP-32, and checks the balance and transaction history of these addresses. The goal is to search for wallets that have transactions or non-zero balances. This script can be useful for finding active Bitcoin wallets associated with randomly generated seed phrases.

## Features
- **Random Mnemonic Generation**: Generates random BIP-39 mnemonic phrases.
- **Wallet Address Generation**: Derives multiple wallet addresses from a mnemonic phrase using BIP-32.
- **Balance & Transaction Check**: Checks the balance and transaction history of generated wallet addresses via Blockstream's API.
- **Symmetrical Search**: Avoids re-testing previously "not found" seed phrases.
- **Seed Phrase Management**: Stores "not found" seed phrases and those with suspicious transaction histories for future reference.

## Dependencies: 
mnemonic
bip32utils
requests
```console 
pip install mnemonic bip32utils requests
```
## Installation

1. Clone the repository:
   ```console
   git clone https://github.com/NabooJarJar/Symmetrical-Search-for-Bitcoin-Mnemonics.git
   ```
   ```console
   python symmetrical_search.py
   ```

## EXAMPLE SUCCESSFULL OUTPUT
```code
Starting symmetrical search...
Testing mnemonic #1: pie viper depth elderly pigeon flood woman light diamond business wave dawn
Checking address 1/10: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
  - Balance: 0 satoshis, Transactions: 3
--------------------------------------------------
Checking address 2/10: 1J15VeDHFyHrQ9Q1msQ2tD8HLX3ZLnkJh
  - Balance: 0 satoshis, Transactions: 1
--------------------------------------------------
No balance found for mnemonic: pie viper depth elderly pigeon flood woman light diamond business wave dawn. Adding to not_found_seeds.
--------------------------------------------------
Testing mnemonic #2: school universe door closet slice regular hope wheel tax moon hammer
Checking address 1/10: 1LqJ8ZGq9v2k5P3t6hH5vPwnFwUnm5eb9R
  - Balance: 50000 satoshis, Transactions: 2
Address: 1LqJ8ZGq9v2k5P3t6hH5vPwnFwUnm5eb9R, Balance: 50000 satoshis, Transactions: 2
--------------------------------------------------
Address: 1DfFcNz2pkA5JvZB6DhaUHeivVSh3T2q15, Balance: 0 satoshis, Transactions: 0
--------------------------------------------------
Address: 1DdBZ3jkhpvXg7TuV1GyMiW2R61gHj7tV9, Balance: 0 satoshis, Transactions: 0
--------------------------------------------------
No balance found for mnemonic: school universe door closet slice regular hope wheel tax moon hammer. Adding to not_found_seeds.
--------------------------------------------------
...

Seeds with suspected transaction history:
['pie viper depth elderly pigeon flood woman light diamond business wave dawn', 'school universe door closet slice regular hope wheel tax moon hammer', ...]
```

## Feel free to fork my project !
