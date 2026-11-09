"""퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제(question), 선택지(choices), 정답 번호(answer)를 가진 퀴즈 한 개."""

    CHOICE_COUNT = 4  # 선택지는 항상 4개

    def __init__(self, question, choices, answer):
        # 잘못된 값으로 퀴즈가 만들어지지 않도록 먼저 검사한다.
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(choices, list) or len(choices) != self.CHOICE_COUNT:
            raise ValueError(f"선택지는 {self.CHOICE_COUNT}개여야 합니다.")
        for choice in choices:
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")
        # bool은 int의 한 종류(True == 1)이므로 따로 걸러 낸다.
        if isinstance(answer, bool) or not isinstance(answer, int):
            raise ValueError("정답은 숫자(1~4)여야 합니다.")
        if not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(f"정답은 1~{self.CHOICE_COUNT} 사이여야 합니다.")

        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer  # 정답은 1~4 번호로 관리

    @property
    def correct_choice(self):
        """정답 번호에 해당하는 선택지 내용 (예: 3번 → '6개')."""
        return self.choices[self.answer - 1]

    def display(self, number):
        """문제 번호, 문제, 선택지를 화면에 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, answer_number):
        """사용자가 고른 번호가 정답이면 True, 아니면 False를 돌려준다."""
        return answer_number == self.answer

    def to_dict(self):
        """파일(JSON)에 저장할 수 있도록 딕셔너리로 바꾼다."""
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """파일에서 읽은 딕셔너리로 Quiz 객체를 만든다."""
        if not isinstance(data, dict):
            raise TypeError("퀴즈 데이터는 딕셔너리여야 합니다.")
        return cls(data["question"], data["choices"], data["answer"])
