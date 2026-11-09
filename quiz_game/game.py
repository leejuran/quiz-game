"""게임 전체 흐름(메뉴 표시, 입력 처리, 기능 실행)을 관리하는 QuizGame 클래스."""

from quiz_game.default_data import create_default_quizzes
from quiz_game.quiz import Quiz

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """메뉴를 보여 주고, 사용자가 고른 기능을 실행하는 클래스."""

    def __init__(self):
        # 게임에서 사용할 퀴즈 목록 (Quiz 객체들의 리스트)
        self.quizzes = create_default_quizzes()

        # (메뉴 이름, 실행할 메서드) 목록. 실행할 메서드가 None이면 종료를 뜻한다.
        self.menu_items = [
            ("퀴즈 풀기", self.play_quiz),
            ("퀴즈 추가", self.add_quiz),
            ("퀴즈 목록", self.show_quizzes),
            ("점수 확인", self.show_score),
            ("종료", None),
        ]

    # ------------------------------------------------------------------
    # 실행 흐름
    # ------------------------------------------------------------------
    def run(self):
        """게임을 시작하고, 종료를 고를 때까지 메뉴를 반복한다."""
        self.print_title()
        try:
            while True:
                self.show_menu()
                choice = self.read_int("선택: ", 1, len(self.menu_items))
                _, action = self.menu_items[choice - 1]
                if action is None:
                    break
                action()
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C 또는 입력 스트림 종료 시 오류 화면 없이 안전하게 종료
            print("\n\n⚠️ 입력이 중단되었습니다. 프로그램을 안전하게 종료합니다.")
        print("👋 게임을 종료합니다. 다음에 또 만나요!")

    def print_title(self):
        """프로그램 시작 시 제목을 출력한다."""
        print(LINE)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print(LINE)

    def show_menu(self):
        """메뉴 목록을 출력한다."""
        print()
        print(LINE)
        for number, (name, _) in enumerate(self.menu_items, start=1):
            print(f"{number}. {name}")
        print(LINE)

    # ------------------------------------------------------------------
    # 메뉴 기능
    # ------------------------------------------------------------------
    def play_quiz(self):
        """저장된 퀴즈를 차례대로 출제하고, 문제마다 정답 여부를 알려 준다."""
        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        correct_count = 0  # 맞힌 문제 수
        for number, quiz in enumerate(self.quizzes, start=1):
            print(THIN_LINE)
            quiz.display(number)
            answer = self.read_int("정답 입력: ", 1, Quiz.CHOICE_COUNT)
            if quiz.is_correct(answer):
                correct_count += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice}'입니다.")
            print()

    # ------------------------------------------------------------------
    # 메뉴 기능 (다음 단계에서 구현 예정)
    # ------------------------------------------------------------------

    def add_quiz(self):
        print("\n🚧 퀴즈 추가 기능은 준비 중입니다.")

    def show_quizzes(self):
        print("\n🚧 퀴즈 목록 기능은 준비 중입니다.")

    def show_score(self):
        print("\n🚧 점수 확인 기능은 준비 중입니다.")

    # ------------------------------------------------------------------
    # 입력 처리
    # ------------------------------------------------------------------
    def read_int(self, prompt, minimum, maximum):
        """minimum~maximum 범위의 정수를 입력받는다. 올바른 값이 들어올 때까지 반복한다."""
        guide = f"{minimum}-{maximum} 사이의 숫자를 입력하세요."
        while True:
            raw = input(prompt).strip()  # 앞뒤 공백 제거
            if not raw:
                print(f"⚠️ 입력값이 없습니다. {guide}")
                continue
            try:
                number = int(raw)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {guide}")
                continue
            if not minimum <= number <= maximum:
                print(f"⚠️ 범위를 벗어난 숫자입니다. {guide}")
                continue
            return number
