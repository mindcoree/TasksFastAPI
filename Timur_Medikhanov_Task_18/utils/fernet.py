import hashlib
import asyncio
from cryptography.fernet import Fernet
from core.config import settings

# Получаем объект Fernet синхронно (быстрая операция)
fernet = Fernet(settings.fernet_key.encode())


async def encrypt_card_number(card_number: str) -> str:
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Invalid card number format")

    bytes_card_number = card_number.encode()
    encrypt_bytes = await asyncio.to_thread(fernet.encrypt, bytes_card_number)
    return encrypt_bytes.decode()


# Асинхронно расшифровываем
async def decrypt_card_number(encrypted_str: str) -> str:
    encrypted_bytes = encrypted_str.encode()
    decrypted_bytes = await asyncio.to_thread(fernet.decrypt, encrypted_bytes)
    return decrypted_bytes.decode()


# Маскируем номер карты
async def mask_card_number(card_number: str) -> str:
    return f"**** **** **** {card_number[-4:]}"


def _hash_card_number_sync(card_number: str) -> str:
    return hashlib.sha256(card_number.encode()).hexdigest()


async def hash_card_number(card_number: str) -> str:
    return await asyncio.to_thread(_hash_card_number_sync, card_number)
