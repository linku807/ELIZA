CHO = [0, 2, 3, 5, 6, 7, 9, 11]
JUNG = [0, 2, 4, 6, 8, 12, 13, 17]
JONG = [0, 1, 4, 7, 8, 16, 17, 19]

CHO_REV = {val: idx for idx, val in enumerate(CHO)}
JUNG_REV = {val: idx for idx, val in enumerate(JUNG)}
JONG_REV = {val: idx for idx, val in enumerate(JONG)}


def encode(num: int) -> str:
    result = []
    for shift in range(21, -1, -3):
        c = (num >> (shift * 3 + 6)) & 7
        u = (num >> (shift * 3 + 3)) & 7
        j = (num >> (shift * 3)) & 7

        code = ((CHO[c] * 21) + JUNG[u]) * 28 + JONG[j] + 0xAC00
        result.append(chr(code))

    return "".join(result)


def decode(enc: str) -> int:
    num = 0
    for char in enc:
        code = ord(char) - 0xAC00

        # 한글 자음/모음/받침 인덱스 분리
        jong_val = code % 28
        code //= 28
        jung_val = code % 21
        cho_val = code // 21

        # 역매핑 테이블로 8진수 값 복원 후 비트 연산으로 합침
        triple = (
            (CHO_REV[cho_val] << 6)
            | (JUNG_REV[jung_val] << 3)
            | JONG_REV[jong_val]
        )
        num = (num << 9) | triple

    return num