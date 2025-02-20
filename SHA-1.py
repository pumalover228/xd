import struct
# побитовый сдвиг
def rotate_left(value, shift):
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF


def process_block(block, h):
    # Разбиение блока данных на 16 слов по 32 бита
    w = [0] * 80
    for i in range(16):
        w[i] = struct.unpack('>I', block[i * 4:i * 4 + 4])[0]

    for i in range(16, 80):
        w[i] = rotate_left(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

    a, b, c, d, e = h

    # Основной цикл обработки
    for i in range(80):
        if i < 20:
            f = (b & c) | (~b & d)
            k = 0x5A827999
        elif i < 40:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif i < 60:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        else:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        temp = (rotate_left(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
        e = d
        d = c
        c = rotate_left(b, 30)
        b = a
        a = temp

    return [(x + y) & 0xFFFFFFFF for x, y in zip([a, b, c, d, e], h)]


# Основная функция SHA-1
def sha1(data):
    # Добавляем данные и длину в конец
    data = bytearray(data)
    length = len(data) * 8
    data.append(0x80)  # Добавляем битовый 1
    while len(data) % 64 != 56:
        data.append(0x00)  # Добавляем нули для выравнивания
    data.extend(struct.pack('>Q', length))  # Добавляем длину данных
    # Инициализация хеш-состояния

    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    # Обработка блоков по 512 бит
    for i in range(0, len(data), 64):
        block = data[i:i + 64]
        h = process_block(block, h)

    # Возвращаем хеш в виде строки
    return ''.join(f'{x:08x}' for x in h)


# Пример использования
message = "три дня дождя"
hash_value = sha1(message.encode('utf-8'))
print('Хэш строки <{}>: {}'.format(message, hash_value))


