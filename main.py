"""퀴즈 게임 실행 파일.

실행 방법: python main.py
"""

import sys

from quiz_game.game import QuizGame


def configure_console():
    """한글과 이모지가 깨지지 않도록 출력 인코딩을 UTF-8로 맞춘다."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass  # 인코딩을 바꿀 수 없는 환경이면 기본값 그대로 사용


def main():
    configure_console()
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
