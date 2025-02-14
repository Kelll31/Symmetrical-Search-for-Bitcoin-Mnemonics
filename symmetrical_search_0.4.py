import random
import time
import json
import os
import requests
from mnemonic import Mnemonic
import bip32utils
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional

# Глобальная переменная для управления задержкой между запросами
request_delay = 0.5  # Начальная задержка в секундах
error_429_count = 0  # Счетчик ошибок 429
success_count = 0  # Счетчик успешных проверок


# Загрузка списка слов BIP-39
def load_wordlist(filename: str) -> List[str]:
    with open(filename, "r") as f:
        return [line.strip() for line in f]


# Генерация адресов кошельков с использованием BIP-32
def generate_wallet_from_mnemonic(
    mnemonic_phrase: str, num_addresses: int = 10
) -> List[str]:
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic_phrase)
    master_key = bip32utils.BIP32Key.fromEntropy(seed)

    addresses = []
    for i in range(num_addresses):
        child_key = master_key.ChildKey(i)
        addresses.append(child_key.Address())
    return addresses


# Проверка баланса и истории транзакций адреса
def check_balance_and_history(address: str) -> Optional[Tuple[int, int]]:
    global request_delay, error_429_count, success_count
    url = f"https://blockstream.info/api/address/{address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            success_count += 1
            # Увеличиваем скорость (уменьшаем задержку), если 5 успешных запросов подряд
            if success_count >= 5:
                request_delay = max(
                    0.1, request_delay - 0.1
                )  # Минимальная задержка 0.1 сек
                success_count = 0  # Сбрасываем счетчик успешных запросов
            return response.json().get("chain_stats", {}).get(
                "funded_txo_sum", 0
            ), response.json().get("chain_stats", {}).get("tx_count", 0)
        elif response.status_code == 429:
            error_429_count += 1
            print("Превышен лимит запросов. Уменьшаем скорость...")
            request_delay += 0.5  # Увеличиваем задержку на 0.5 сек
            time.sleep(request_delay)  # Ждем перед повторным запросом
            return check_balance_and_history(address)  # Повторяем запрос
        else:
            print(f"Ошибка при запросе данных для {address}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Исключение при проверке адреса {address}: {str(e)}")
        return None


# Сохранение seed-фраз без баланса в файл
def save_not_found_seeds(
    seeds: List[str], filename: str = "not_found_seeds.json"
) -> None:
    if os.path.exists(filename):
        with open(filename, "r") as f:
            existing_seeds = json.load(f)
    else:
        existing_seeds = []

    updated_seeds = list(set(existing_seeds + seeds))  # Убираем дубликаты
    with open(filename, "w") as f:
        json.dump(updated_seeds, f, indent=4, ensure_ascii=False)
    print(f"Сохранено {len(seeds)} seed-фраз в файл {filename}.")


# Загрузка seed-фраз без баланса из файла
def load_not_found_seeds(filename: str = "not_found_seeds.json") -> set:
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return set(json.load(f))
    return set()


# Генерация случайной BIP-39 мнемонической фразы
def generate_random_mnemonic(bip39_wordlist: List[str], num_words: int = 12) -> str:
    return " ".join(random.choices(bip39_wordlist, k=num_words))


# Проверка адресов в многопоточном режиме
def check_addresses_multithreaded(
    addresses: List[str], max_workers: int = 5
) -> List[Tuple[str, int, int]]:
    global request_delay
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_address = {
            executor.submit(check_balance_and_history, address): address
            for address in addresses
        }
        for future in as_completed(future_to_address):
            address = future_to_address[future]
            print(f"Проверяется адрес: {address}")  # Вывод проверяемого адреса
            try:
                result = future.result()
                if result:
                    balance, tx_count = result
                    results.append((address, balance, tx_count))
                # Задержка между запросами
                time.sleep(request_delay)
            except Exception as e:
                print(f"Ошибка при обработке адреса {address}: {str(e)}")
    return results


# Сохранение найденных кошельков с балансом в файл
def save_found_wallet(
    mnemonic_phrase: str,
    address: str,
    balance: int,
    filename: str = "found_wallets.json",
) -> None:
    wallet_data = {
        "mnemonic_phrase": mnemonic_phrase,
        "address": address,
        "balance": balance,
    }
    if os.path.exists(filename):
        with open(filename, "r") as f:
            existing_wallets = json.load(f)
    else:
        existing_wallets = []

    existing_wallets.append(wallet_data)
    with open(filename, "w") as f:
        json.dump(existing_wallets, f, indent=4, ensure_ascii=False)
    print(f"Кошелек с балансом сохранен в файл {filename}.")


# Основная функция симметричного поиска
def symmetrical_search(
    bip39_wordlist: List[str],
    num_addresses: int = 10,
    not_found_file: str = "not_found_seeds.json",
) -> None:
    not_found_seeds = load_not_found_seeds(not_found_file)
    new_not_found_seeds = []

    print("Запуск симметричного поиска...")
    while True:  # Бесконечный цикл
        mnemonic_phrase = generate_random_mnemonic(bip39_wordlist, num_words=12)

        # Пропускаем уже проверенные seed-фразы
        if mnemonic_phrase in not_found_seeds:
            print(f"Пропускаем известную seed-фразу без баланса: {mnemonic_phrase}")
            continue

        print(f"Проверяем мнемоническую фразу: {mnemonic_phrase}")
        try:
            addresses = generate_wallet_from_mnemonic(
                mnemonic_phrase, num_addresses=num_addresses
            )
            results = check_addresses_multithreaded(addresses, max_workers=5)

            for idx, (address, balance, tx_count) in enumerate(results, start=1):
                print(
                    f"Проверен адрес {idx}/{len(addresses)}: {address}"
                )  # Вывод проверенного адреса
                if balance > 0:
                    print(f"Найден кошелек с балансом!")
                    print(f"Мнемоническая фраза: {mnemonic_phrase}")
                    print(
                        f"Адрес: {address}, Баланс: {balance} сатоши, Транзакции: {tx_count}"
                    )

                    # Сохранение найденного кошелька
                    save_found_wallet(mnemonic_phrase, address, balance)

                    return  # Завершаем поиск
                elif tx_count > 0:
                    print(f"Адрес: {address} имеет транзакции, но баланс равен 0.")

            print(
                f"Баланс не найден для мнемонической фразы: {mnemonic_phrase}. Добавляем в список not_found_seeds."
            )
            new_not_found_seeds.append(mnemonic_phrase)
            not_found_seeds.add(mnemonic_phrase)  # Добавляем в проверенные

            print("-" * 50)

        except Exception as e:
            print(
                f"Ошибка при обработке мнемонической фразы: {mnemonic_phrase} | {str(e)}"
            )
            continue

        # Сохраняем новые seed-фразы без баланса
        save_not_found_seeds(new_not_found_seeds, not_found_file)


if __name__ == "__main__":
    # Загрузка списка слов BIP-39
    bip39_wordlist = load_wordlist("english.txt")

    # Запуск симметричного поиска
    symmetrical_search(bip39_wordlist, num_addresses=10)
