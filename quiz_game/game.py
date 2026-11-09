"""게임 전체 흐름(메뉴 표시, 입력 처리, 기능 실행)을 관리하는 QuizGame 클래스."""

from quiz_game.default_data import create_default_quizzes
from quiz_game.quiz import Quiz
from quiz_game.storage import StateFileError, StateStorage

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """메뉴를 보여 주고, 사용자가 고른 기능을 실행하는 클래스."""

    def __init__(self, storage=None):
        # 파일 저장/불러오기 담당 (기본: 프로젝트 루트의 state.json)
        self.storage = storage or StateStorage()
        # 게임에서 사용할 퀴즈 목록 (Quiz 객체들의 리스트) - load_state()에서 채운다.
        self.quizzes = []
        # 최고 점수 (아직 퀴즈를 푼 적이 없으면 None)
        self.best_score = None

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
        self.load_state()
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
            print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
        if self.save_state():
            print("💾 데이터를 저장했습니다.")
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
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다. 먼저 '2. 퀴즈 추가'에서 퀴즈를 등록해 주세요.")
            return

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

        self.show_result(correct_count, total)

    def show_result(self, correct_count, total):
        """모든 문제를 푼 뒤 결과(맞힌 개수, 100점 만점 점수)를 보여 주고 점수를 돌려준다."""
        score = round(correct_count / total * 100)
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        print(LINE)
        return score

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 등록하고 파일에 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        # 1) 문제 입력 (빈 값, 이미 있는 문제는 다시 입력)
        existing_questions = [quiz.question for quiz in self.quizzes]
        while True:
            question = self.read_text("문제를 입력하세요: ")
            if question in existing_questions:
                print("⚠️ 이미 등록된 문제입니다. 다른 문제를 입력하세요.")
                continue
            break

        # 2) 선택지 4개 입력 (빈 값, 중복된 선택지는 다시 입력)
        choices = []
        for number in range(1, Quiz.CHOICE_COUNT + 1):
            while True:
                choice = self.read_text(f"선택지 {number}: ")
                if choice in choices:
                    print("⚠️ 이미 입력한 선택지입니다. 다른 내용을 입력하세요.")
                    continue
                choices.append(choice)
                break

        # 3) 정답 번호 입력 (1~4)
        answer = self.read_int(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)

        # 4) 퀴즈 등록 후 바로 파일에 저장
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print(f"\n✅ 퀴즈가 추가되었습니다! (총 {len(self.quizzes)}개)")
        else:
            print("\n⚠️ 퀴즈는 추가되었지만 파일 저장에 실패했습니다. 종료할 때 다시 저장을 시도합니다.")

    # ------------------------------------------------------------------
    # 메뉴 기능 (다음 단계에서 구현 예정)
    # ------------------------------------------------------------------

    def show_quizzes(self):
        print("\n🚧 퀴즈 목록 기능은 준비 중입니다.")

    def show_score(self):
        print("\n🚧 점수 확인 기능은 준비 중입니다.")

    # ------------------------------------------------------------------
    # 파일 저장/불러오기 (state.json)
    # ------------------------------------------------------------------
    def load_state(self):
        """state.json에서 퀴즈와 최고 점수를 불러온다.

        - 파일 없음(첫 실행): 기본 퀴즈로 시작
        - 파일 손상: 안내 후 손상된 파일을 보관하고 기본 퀴즈로 복구
        """
        try:
            data = self.storage.load()
        except StateFileError as error:
            print(f"⚠️ 저장 파일을 읽을 수 없습니다: {error}")
            self.recover_with_defaults()
            return

        if data is None:
            self.quizzes = create_default_quizzes()
            self.best_score = None
            print(f"📂 저장된 데이터가 없어 기본 퀴즈 {len(self.quizzes)}개로 시작합니다.")
            return

        try:
            self.apply_state(data)
        except (KeyError, TypeError, ValueError) as error:
            print(f"⚠️ 저장 파일의 내용이 올바르지 않습니다: {error}")
            self.recover_with_defaults()
            return

        best_text = "기록 없음" if self.best_score is None else f"{self.best_score}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best_text})")

    def apply_state(self, data):
        """파일에서 읽은 딕셔너리를 검사해서 게임 속성에 반영한다. 잘못되면 오류를 발생시킨다."""
        quiz_list = data["quizzes"]
        if not isinstance(quiz_list, list):
            raise TypeError("quizzes는 리스트여야 합니다.")
        quizzes = [Quiz.from_dict(item) for item in quiz_list]

        best_score = data.get("best_score")
        if best_score is not None:
            if isinstance(best_score, bool) or not isinstance(best_score, int):
                raise TypeError("best_score는 숫자 또는 null이어야 합니다.")
            if not 0 <= best_score <= 100:
                raise ValueError("best_score는 0~100 사이여야 합니다.")

        # 모든 검사를 통과한 뒤에 한꺼번에 반영한다.
        self.quizzes = quizzes
        self.best_score = best_score

    def recover_with_defaults(self):
        """손상된 파일을 보관하고, 기본 퀴즈로 초기화한 뒤 새로 저장한다."""
        backup_path = self.storage.backup_corrupted()
        if backup_path:
            print(f"   손상된 파일은 '{backup_path.name}'(으)로 보관했습니다.")
        self.quizzes = create_default_quizzes()
        self.best_score = None
        print(f"🔧 기본 퀴즈 {len(self.quizzes)}개로 복구했습니다.")
        self.save_state()

    def save_state(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장한다. 성공하면 True."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            self.storage.save(data)
        except OSError as error:
            print(f"⚠️ 데이터를 저장하지 못했습니다: {error}")
            return False
        return True

    # ------------------------------------------------------------------
    # 입력 처리
    # ------------------------------------------------------------------
    def read_text(self, prompt):
        """비어 있지 않은 글자를 입력받는다. 앞뒤 공백은 제거한다."""
        while True:
            text = input(prompt).strip()
            if text:
                return text
            print("⚠️ 빈 값은 입력할 수 없습니다. 내용을 입력하세요.")

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
