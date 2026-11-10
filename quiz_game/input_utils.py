"""사용자 입력을 안전하게 받는 함수 모음.

모든 입력은 앞뒤 공백을 제거한 뒤 검사하고,
잘못된 값이면 안내 메시지를 보여 준 다음 다시 입력받는다.
"""


def read_text(prompt):
    """비어 있지 않은 글자를 입력받아 돌려준다."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("⚠️ 빈 값은 입력할 수 없습니다. 내용을 입력하세요.")


def parse_int(raw, minimum, maximum):
    """입력 문자열을 검사해서 (숫자, None) 또는 (None, 오류 메시지)를 돌려준다."""
    guide = f"{minimum}-{maximum} 사이의 숫자를 입력하세요."
    raw = raw.strip()
    if not raw:
        return None, f"⚠️ 입력값이 없습니다. {guide}"
    try:
        number = int(raw)
    except ValueError:
        return None, f"⚠️ 잘못된 입력입니다. {guide}"
    if not minimum <= number <= maximum:
        return None, f"⚠️ 범위를 벗어난 숫자입니다. {guide}"
    return number, None


def read_int(prompt, minimum, maximum):
    """minimum~maximum 범위의 정수를 입력받는다. 올바른 값이 들어올 때까지 반복한다."""
    while True:
        number, error = parse_int(input(prompt), minimum, maximum)
        if error is None:
            return number
        print(error)
