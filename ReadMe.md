# Symmetrical Search for Bitcoin Mnemonics

This project generates random BIP-39 mnemonic phrases, derives wallet addresses using BIP-32, and checks the balance and transaction history of these addresses. The goal is to search for wallets that have transactions or non-zero balances. This script can be useful for finding active Bitcoin wallets associated with randomly generated seed phrases.

## Features
- **Random Mnemonic Generation**: Generates random BIP-39 mnemonic phrases.
- **Wallet Address Generation**: Derives multiple wallet addresses from a mnemonic phrase using BIP-32.
- **Balance & Transaction Check**: Checks the balance and transaction history of generated wallet addresses via Blockstream's API.
- **Symmetrical Search**: Avoids re-testing previously "not found" seed phrases.
- **Seed Phrase Management**: Stores "not found" seed phrases and those with suspicious transaction histories for future reference.

## Installation

1. Clone the repository:
   ```bash
