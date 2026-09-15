# 修正例1: 正しい型の引数を渡す
result = add_numbers(10, 20)

# 修正例2: 文字列を扱う場合は関数の型ヒントを変更
def concatenate_strings(a: str, b: str) -> str:
    return a + b
