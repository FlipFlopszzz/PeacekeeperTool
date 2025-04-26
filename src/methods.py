# 银牌点灯
import difflib


def compute_candles(iterations):
    r = [0] * 7
    a = [[0] * 7 for _ in range(7)]
    e = [[0] * 7 for _ in range(7)]
    n = "无结果"

    for t in range(7):
        r[t] = iterations[t].replace(" ", "").replace("，", ",")
        i = r[t].split(",")
        for o in range(7):
            e[t][o] = 0
        for o in range(len(i)):
            e[t][int(i[o]) - 1] = 1
        if r[t] == "":
            return n

    a[0] = e[0]
    for t in range(1, 7):
        for o in range(7):
            a[t][o] = 1 if e[t-1][o] != e[t][o] else 0

    l = 0
    f = [
        [0], [1], [2], [3], [4], [5], [6],
        [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
        [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [2, 3], [2, 4], [2, 5], [2, 6],
        [3, 4], [3, 5], [3, 6], [4, 5], [4, 6], [5, 6], [
            0, 1, 2], [0, 1, 3], [0, 1, 4], [0, 1, 5], [0, 1, 6],
        [0, 2, 3], [0, 2, 4], [0, 2, 5], [0, 2, 6], [0, 3, 4], [
            0, 3, 5], [0, 3, 6], [0, 4, 5], [0, 4, 6], [0, 5, 6],
        [1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 2, 6], [1, 3, 4], [
            1, 3, 5], [1, 3, 6], [1, 4, 5], [1, 4, 6], [1, 5, 6],
        [2, 3, 4], [2, 3, 5], [2, 3, 6], [2, 4, 5], [2, 4, 6], [
            2, 5, 6], [3, 4, 5], [3, 4, 6], [3, 5, 6], [4, 5, 6],
        [0, 1, 2, 3], [0, 1, 2, 4], [0, 1, 2, 5], [0, 1, 2, 6], [
            0, 1, 3, 4], [0, 1, 3, 5], [0, 1, 3, 6], [0, 1, 4, 5],
        [0, 1, 4, 6], [0, 1, 5, 6], [0, 2, 3, 4], [0, 2, 3, 5], [
            0, 2, 3, 6], [0, 2, 4, 5], [0, 2, 4, 6], [0, 2, 5, 6],
        [0, 3, 4, 5], [0, 3, 4, 6], [0, 3, 5, 6], [0, 4, 5, 6], [
            1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 3, 6], [1, 2, 4, 5],
        [1, 2, 4, 6], [1, 2, 5, 6], [1, 3, 4, 5], [1, 3, 4, 6], [
            1, 3, 5, 6], [1, 4, 5, 6], [2, 3, 4, 5], [2, 3, 4, 6],
        [2, 3, 5, 6], [2, 4, 5, 6], [3, 4, 5, 6], [0, 1, 2, 3, 4], [
            0, 1, 2, 3, 5], [0, 1, 2, 3, 6], [0, 1, 2, 4, 5],
        [0, 1, 2, 4, 6], [0, 1, 2, 5, 6], [0, 1, 3, 4, 5], [0, 1, 3, 4, 6], [
            0, 1, 3, 5, 6], [0, 1, 4, 5, 6], [0, 2, 3, 4, 5],
        [0, 2, 3, 4, 6], [0, 2, 3, 5, 6], [0, 2, 4, 5, 6], [0, 3, 4, 5, 6], [
            1, 2, 3, 4, 5], [1, 2, 3, 4, 6], [1, 2, 3, 5, 6],
        [1, 2, 4, 5, 6], [1, 3, 4, 5, 6], [2, 3, 4, 5, 6], [
            0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 5, 6],
        [0, 1, 2, 4, 5, 6], [0, 1, 3, 4, 5, 6], [0, 2, 3, 4, 5, 6], [
            1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6]
    ]

    for t in range(len(f)):
        v = e[6][:]
        w = f[t][:]
        for y in range(len(w)):
            if w[y] - y + 1 <= 0:
                w[y] = w[y] - y + 8
            else:
                w[y] = w[y] - y + 1
        for A in range(len(f[t])):
            for o in range(7):
                u = v[o] + a[f[t][A]][o]
                v[o] = 0 if u == 2 else u
            c = sum(v)
            if c == 7:
                n = "结果为：" + str(w)
                l = -1
                break
            if l == -1:
                break
        if l == -1:
            break
        l += 1

    return n


def find_missing_letters(input_str: str):
    # 目标字符串
    target_str = "DULCEETDECORUMESTPROPATRIAMORI"

    # 预处理输入文本：转大写并移除空格
    processed_input = "".join(input_str.upper().split())

    # 验证输入长度
    if len(processed_input) != 22:
        return ['error:输入字符数不是22个']

    # 验证输入是否都是字母
    if not processed_input.isalpha():
        return ['error:输入的字符中含有不是字母的字符']

    results = []
    input_len = len(processed_input)
    target_len = len(target_str)

    def backtrack(target_index, input_index, current_missing):
        if target_index == target_len:
            if len(current_missing) == target_len - input_len:
                results.append(''.join(current_missing))
            return
        if input_index < input_len and processed_input[input_index] == target_str[target_index]:
            backtrack(target_index + 1, input_index + 1, current_missing)
        new_missing = current_missing + [target_str[target_index]]
        backtrack(target_index + 1, input_index, new_missing)

    backtrack(0, 0, [])
    return results


# # 测试代码
# if __name__ == "__main__":
#     # 测试用例
#     test_cases = [
#         "DULCEETDECRUMESTPRPAIA",
#         "ULCEETDECORUMESTPROPOR",
#         "DULCEETDECRUMESTPARIMO",
#         "DULCEETDECOESTPROPATRI",
#         "abcdefghijklmnopqrstuv"
#         # "DULCEETDECRUMESTRIOI",
#         # "DULCEETDECORMESPROP"
#     ]
#     for index, test_case in enumerate(test_cases, start=1):
#         missing_letters = find_missing_letters(test_case)
#         print(f"测试用例 {index}: 输入字符串 '{test_case}'，缺失的字母是: {missing_letters}")


def find_missing_numbers(letters: str) -> str:
    # 字母到数字的映射表
    letter_to_num = {
        'C': '1', 'D': '2', 'A': '3', 'R': '4', 'B': '5',
        'N': '6', 'E': '7', 'G': '8', 'M': '9', 'P': '0',
        'F': '1', 'O': '2', 'U': '3', 'Z': '4', 'I': '5',
        'X': '6', 'L': '7', 'K': '8', 'S': '9', 'T': '0'
    }

    # 验证输入长度
    if len(letters) != 8:
        return 'error'

    # 验证所有字母都在映射表中
    for letter in letters:
        if letter not in letter_to_num:
            return 'error'

    # 转换字母为数字
    result = ''.join(letter_to_num[letter] for letter in letters)

    return result


def find_missing_lights(numbers: str) -> list[str]:
    # 数字到灯光状态的映射表
    num_to_lights = {
        '0': '灭灭灭灭灭',
        '1': '亮灭灭灭灭',
        '2': '亮亮灭灭灭',
        '3': '亮亮亮灭灭',
        '4': '亮亮亮亮灭',
        '5': '亮亮亮亮亮',
        '6': '灭亮亮亮亮',
        '7': '灭灭亮亮亮',
        '8': '灭灭灭亮亮',
        '9': '灭灭灭灭亮'
    }

    # 验证输入长度
    if len(numbers) != 8:
        return ['error']

    # 验证所有字符都是数字
    if not numbers.isdigit():
        return ['error']

    # 转换数字为灯光状态
    result = [num_to_lights[num] for num in numbers]

    return result


def get_last_gold_text(letters: str):
    nums = find_missing_numbers(letters)
    lights = find_missing_lights(nums)
    light_str = "\n".join(lights)
    return "缺少的字母为:"+letters+"\n对应数字为:"+nums+"\n灯的开关序列(1-8号):\n"+light_str


def format_with_letters(letters: str) -> str:
    """
    将5个字母插入到指定格式的字符串中

    Args:
        letters (str): 5个字母组成的字符串

    Returns:
        str: 格式化后的字符串 'CAEEB XXXXX FEAADDAD' 其中 XXXXX 被替换为输入的字母
    """
    # 验证输入长度
    if len(letters) != 5:
        raise ValueError(
            f"Input must be exactly 5 letters, got {len(letters)}")

    # 验证输入是否都是字母
    if not letters.isalpha():
        raise ValueError("Input must contain only letters")

    # 转换为大写并格式化字符串
    return f"CAEEB {letters.upper()} FEAADDAD"

# 以下为解密器


def decode_morse(morse_code):
    # 定义摩斯密码到字母的映射
    MORSE_CODE_DICT = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
        '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
        '----.': '9', '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'",
        '-.-.--': '!', '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&',
        '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-',
        '..--.-': '_', '.-..-.': '"', '...-..-': '$', '.--.-.': '@'
    }

    # 去除首尾空格
    morse_code = morse_code.strip().replace('_', '-')
    # 按空格分割摩斯密码字符串
    words = morse_code.split('  ')
    decoded_text = []

    for word in words:
        letters = word.split(' ')
        decoded_word = ''.join([MORSE_CODE_DICT.get(letter, '')
                               for letter in letters])
        decoded_text.append(decoded_word)

    # 将解码后的单词用空格连接起来
    return ' '.join(decoded_text)


def decrypt_reverse(ciphertext):
    return ciphertext[::-1]


def decrypt_atbash(ciphertext):
    plaintext = ""
    for char in ciphertext:
        if 'A' <= char <= 'Z':
            # 处理大写字母
            new_char = chr(ord('A') + ord('Z') - ord(char))
        elif 'a' <= char <= 'z':
            # 处理小写字母
            new_char = chr(ord('a') + ord('z') - ord(char))
        else:
            # 非字母字符保持不变
            new_char = char
        plaintext += new_char
    return plaintext


def decrypt_rot(ciphertext, n=7):
    plaintext = ""
    for char in ciphertext:
        if 'A' <= char <= 'Z':
            # 处理大写字母
            shifted = ord(char) - n
            if shifted < ord('A'):
                shifted += 26
            plaintext += chr(shifted)
        elif 'a' <= char <= 'z':
            # 处理小写字母
            shifted = ord(char) - n
            if shifted < ord('a'):
                shifted += 26
            plaintext += chr(shifted)
        else:
            # 非字母字符保持不变
            plaintext += char
    return plaintext


def decrypt_rail_fence(ciphertext, needToReverse=False, rails=5, offset=0):
    process_input = decrypt_reverse(
        ciphertext) if needToReverse else ciphertext
    length = len(process_input)
    # 初始化一个二维列表来模拟栅栏，用于存储字符位置信息
    fence = [['\n' for _ in range(length)] for _ in range(rails)]
    # 标记当前是向下还是向上移动
    going_down = False
    row, col = 0, 0

    # 第一步：确定每个位置在栅栏中的轨迹
    for i in range(length):
        if row == 0:
            going_down = True
        elif row == rails - 1:
            going_down = False
        # 记录当前位置
        fence[row][col] = i
        col += 1
        row += 1 if going_down else -1

    # 第二步：根据栅栏轨迹将密文填充到对应位置
    index = 0
    result = [''] * length
    for i in range(rails):
        for j in range(length):
            if fence[i][j] != '\n':
                # 考虑偏移量
                adjusted_index = (fence[i][j] + offset) % length
                result[adjusted_index] = process_input[index]
                index += 1

    # 第三步：将结果列表组合成字符串
    return ''.join(result)


def decrypt_baconian(ciphertext):
    # 定义培根密码表，将 5 位的 A 和 B 序列映射到对应的字母
    baconian_dict = {
        'aaaaa': 'A', 'aaaab': 'B', 'aaaba': 'C', 'aaabb': 'D',
        'aabaa': 'E', 'aabab': 'F', 'aabba': 'G', 'aabbb': 'H',
        'abaaa': 'I', 'abaab': 'J', 'ababa': 'K', 'ababb': 'L',
        'abbaa': 'M', 'abbab': 'N', 'abbba': 'O', 'abbbb': 'P',
        'baaaa': 'Q', 'baaab': 'R', 'baaba': 'S', 'baabb': 'T',
        'babaa': 'U', 'babab': 'V', 'babba': 'W', 'babbb': 'X',
        'bbaaa': 'Y', 'bbaab': 'Z'
    }

    # 去除密文中可能存在的非 A 和 B 的字符，并将其转换为小写
    clean_ciphertext = ''.join(
        filter(lambda x: x in 'ABab', ciphertext)).lower()

    plaintext = ''
    # 以 5 个字符为一组进行分割
    for i in range(0, len(clean_ciphertext), 5):
        code = clean_ciphertext[i:i + 5]
        if code in baconian_dict:
            plaintext += baconian_dict[code]
    return plaintext


def decrypt_vigenere(ciphertext, key='Edward'):
    plaintext = ""
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            # 确定密钥字符
            key_char = key[key_index % len(key)].upper()
            key_shift = ord(key_char) - ord('A')

            if char.isupper():
                # 解密大写字母
                new_char = chr((ord(char) - ord('A') - key_shift) %
                               26 + ord('A'))
            else:
                # 解密小写字母
                new_char = chr((ord(char) - ord('a') - key_shift) %
                               26 + ord('a'))
            key_index += 1
        else:
            # 非字母字符保持不变
            new_char = char
        plaintext += new_char
    return plaintext


def decrypt_autokey(ciphertext, key="George", alphabet="zabcdefghijklmnopqrstuvwxy"):
    # 确保密钥和密文为大写形式
    key = key.upper()
    ciphertext = ciphertext.upper()
    plaintext = ""
    key_index = 0

    # 遍历密文中的每个字符
    for i, char in enumerate(ciphertext):
        if char in alphabet.upper():
            if i < len(key):
                # 前几个字符使用初始密钥解密
                current_key_char = key[key_index]
                key_index = (key_index + 1) % len(key)
            else:
                # 后续字符使用之前解密出的明文作为密钥
                current_key_char = plaintext[i - len(key)]

            # 获取密文字符和密钥字符在字母表中的索引
            cipher_index = alphabet.upper().index(char)
            key_index_in_alphabet = alphabet.upper().index(current_key_char)

            # 计算解密后的字符索引
            plain_index = (
                cipher_index - key_index_in_alphabet) % len(alphabet)

            # 获取解密后的字符
            plain_char = alphabet.upper()[plain_index]
            plaintext += plain_char
        else:
            # 非字母字符保持不变
            plaintext += char

    return plaintext


candidate_strings = [
    "AMIENS NEUF FURNITURE",
    "CHURCH RUINS AMIENS",
    "LONGUEVILLE STATUE AMIENS",
    "BALLROOM MAP VARENNES",
    "STATUES GARDEN VARENNES",
    "VARENNES SERVANT BED",
    "BUCKET MARSHLANDS FAW",
    "OUTPOST BARREL FAW",
    "TREE FORTRESS FAW",
    "CANAL KANTARA VASES",
    "CRATE TRENCH CANAL",
    "HILL TOWER CANAL",
    "CASTELLO ISLE ADRIATIC",
    "COASTAL FORTRESS ADRIATIC",
    "HILL BARN ADRIATIC",
    "CRATE JABAL JIFAR",
    "PILLAR OUTSKIRTS JIFAR",
    "PILLOW MAZAR JIFAR",
    "CRATE SEREN VENETIAN",
    "FERRO FIRE VENETIAN",
    "STOVE TURRET VENETIAN",
    "HOTEL CHECK PERONNE",
    "RUIN VENTURE PERONNE",
    "TRAVECY ATTIC PERONNE",
    "LUGGAGE BASEMENT APREMONT",
    "PANEL WATER APREMONT",
    "TREE TRAIN APREMONT"
]


def find_closest_string(target, candidates=candidate_strings, threshold=0.6):
    best_match = difflib.get_close_matches(
        target, candidates, n=1, cutoff=threshold)
    return best_match[0] if best_match else "无结果"


# if __name__ == "__main__":
    # print(find_missing_letters("DULCEETDECORUESTPRPTRM"))
    # iterations = ["1，2", "2,7", "2,3,6,7",
    #               "2,3,4,5,6，7", "2,3,4,5,6", "2,3,4", "4"]
    # result = compute_candles(iterations)
    # print(result)
