"""처음 실행할 때(또는 저장 파일이 손상되었을 때) 사용하는 기본 퀴즈 데이터.

주제: Python & Git 기초
"""

from quiz_game.quiz import Quiz


def create_default_quizzes():
    """기본 퀴즈 8개를 Quiz 객체 리스트로 만들어 돌려준다."""
    return [
        Quiz(
            "Python을 만든 사람은 누구일까요?",
            ["귀도 반 로섬", "리누스 토르발스", "비야네 스트롭스트룹", "제임스 고슬링"],
            1,
        ),
        Quiz(
            "type(3.14)를 실행하면 어떤 자료형이 나올까요?",
            ["int", "str", "float", "bool"],
            3,
        ),
        Quiz(
            "리스트 [10, 20, 30]의 길이(요소 개수)를 구하는 함수는?",
            ["size()", "len()", "count()", "length()"],
            2,
        ),
        Quiz(
            "반복 횟수를 미리 알 수 없을 때, 조건이 참인 동안 계속 반복하는 문은?",
            ["for", "while", "if", "def"],
            2,
        ),
        Quiz(
            "딕셔너리에서 키가 없어도 오류 대신 기본값을 돌려주는 메서드는?",
            ["get()", "pop()", "keys()", "items()"],
            1,
        ),
        Quiz(
            "클래스 안의 메서드에서 '객체 자기 자신'을 가리키는 첫 번째 매개변수 이름은?",
            ["this", "me", "self", "it"],
            3,
        ),
        Quiz(
            "실행 중 발생한 오류(예외)를 잡아서 처리할 때 사용하는 구문은?",
            ["try / except", "if / else", "for / in", "def / return"],
            1,
        ),
        Quiz(
            "GitHub(원격 저장소)의 최신 변경 사항을 내 컴퓨터로 가져와 합치는 Git 명령어는?",
            ["git push", "git pull", "git commit", "git init"],
            2,
        ),
    ]
