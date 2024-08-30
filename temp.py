def extract_chars(word: str) -> str:
    result = temp = ""
    for char in f"{word}#":
        if char.isalpha():
            temp += char
        elif not result:
            result = temp
        else:
            result = min(result, temp) if temp else result
            temp = ""

    return result


def compare_min_word(word: str, compare_word: str) -> str:
    if len(word) >= 2:
        if not compare_word:
            return word

        return min(word, compare_word)

    return compare_word


def main() -> None:
    row, col = map(int, input().split())
    min_word = ""

    words = [input() for _ in range(row)]

    for row_idx in range(row):
        horizontal_word = extract_chars(words[row_idx])
        min_word = compare_min_word(horizontal_word, min_word)

    for chars in zip(*words, strict=False):
        vertical_word = extract_chars("".join(chars))
        min_word = compare_min_word(vertical_word, min_word)

    print(min_word)


if __name__ == "__main__":
    main()
