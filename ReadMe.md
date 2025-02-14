Вот обновленный `README.md` с русской и английской версиями:

---

# Symmetrical Search for Bitcoin Mnemonics

[![Kelll31 profile views](https://u8views.com/api/v1/github/profiles/46720761/views/day-week-month-total-count.svg)](https://u8views.com/github/Kelll31)

This project generates random BIP-39 mnemonic phrases, derives wallet addresses using BIP-32, and checks the balance and transaction history of these addresses. The goal is to search for wallets that have transactions or non-zero balances. This script can be useful for finding active Bitcoin wallets associated with randomly generated seed phrases.

---

# Симметричный поиск Bitcoin мнемоник

[![Kelll31 profile views](https://u8views.com/api/v1/github/profiles/46720761/views/day-week-month-total-count.svg)](https://u8views.com/github/Kelll31)

Этот проект генерирует случайные мнемонические фразы BIP-39, создает адреса кошельков с использованием BIP-32 и проверяет баланс и историю транзакций этих адресов. Цель — найти кошельки с транзакциями или ненулевым балансом. Этот скрипт может быть полезен для поиска активных Bitcoin-кошельков, связанных со случайно сгенерированными seed-фразами.

---

## Features / Возможности

- **Random Mnemonic Generation / Генерация случайных мнемоник**: Generates random BIP-39 mnemonic phrases. / Генерация случайных мнемонических фраз BIP-39.
- **Wallet Address Generation / Генерация адресов кошельков**: Derives multiple wallet addresses from a mnemonic phrase using BIP-32. / Создание нескольких адресов кошельков из мнемонической фразы с использованием BIP-32.
- **Balance & Transaction Check / Проверка баланса и транзакций**: Checks the balance and transaction history of generated wallet addresses via Blockstream's API. / Проверка баланса и истории транзакций сгенерированных адресов через API Blockstream.
- **Symmetrical Search / Симметричный поиск**: Avoids re-testing previously "not found" seed phrases. / Исключает повторную проверку ранее найденных seed-фраз без баланса.
- **Seed Phrase Management / Управление seed-фразами**: Stores "not found" seed phrases and those with suspicious transaction histories for future reference. / Сохраняет seed-фразы без баланса и с подозрительной историей транзакций для дальнейшего анализа.

---

## Dependencies / Зависимости

- `mnemonic`
- `bip32utils`
- `requests`

Install dependencies: / Установите зависимости:
```console
pip install mnemonic bip32utils requests
```

---

## Installation / Установка

1. Clone the repository: / Клонируйте репозиторий:
   ```console
   git clone https://github.com/NabooJarJar/Symmetrical-Search-for-Bitcoin-Mnemonics.git
   ```

2. Run the script: / Запустите скрипт:
   ```console
   python symmetrical_search.py
   ```

---

## Example Successful Output / Пример успешного вывода

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

---

## Notes / Примечания

- **API Rate Limiting / Ограничения API**: The script dynamically adjusts the request delay to avoid hitting API rate limits. / Скрипт динамически регулирует задержку между запросами, чтобы избежать превышения лимитов API.
- **Threading / Многопоточность**: The script uses multithreading to speed up address checks. / Скрипт использует многопоточность для ускорения проверки адресов.

---

## Feel free to fork my project! / Не стесняйтесь форкать мой проект!

---

Теперь `README.md` содержит как английскую, так и русскую версии, что делает его удобным для пользователей из разных стран.
