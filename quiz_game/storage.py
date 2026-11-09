"""state.json 파일 읽기/쓰기를 담당하는 StateStorage 클래스."""

import json
import os
from pathlib import Path

# 프로젝트 루트(main.py가 있는 폴더)의 state.json
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE_PATH = PROJECT_ROOT / "state.json"


class StateFileError(Exception):
    """state.json을 읽을 수 없거나 내용이 손상된 경우 발생시키는 오류."""


class StateStorage:
    """게임 데이터(퀴즈 목록, 최고 점수)를 JSON 파일로 저장하고 불러온다."""

    def __init__(self, path=DEFAULT_STATE_PATH):
        self.path = Path(path)

    def load(self):
        """파일을 읽어 딕셔너리로 돌려준다.

        - 파일이 없으면 None을 돌려준다. (첫 실행)
        - 파일이 손상되었거나 읽을 수 없으면 StateFileError를 발생시킨다.
        """
        if not self.path.exists():
            return None
        try:
            # utf-8-sig: 메모장 등에서 저장해 BOM이 붙은 UTF-8 파일도 읽을 수 있다.
            with open(self.path, "r", encoding="utf-8-sig") as file:
                data = json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise StateFileError("JSON 형식이 올바르지 않습니다.") from error
        except OSError as error:
            raise StateFileError(f"파일을 읽을 수 없습니다. ({error})") from error

        if not isinstance(data, dict):
            raise StateFileError("데이터의 최상위 구조가 객체({ })가 아닙니다.")
        return data

    def save(self, data):
        """딕셔너리를 UTF-8 JSON 파일로 저장한다. 실패하면 OSError가 발생한다.

        임시 파일에 먼저 쓴 뒤 바꿔치기해서, 저장 도중 문제가 생겨도
        기존 파일이 반쯤 쓰인 상태로 망가지지 않게 한다.
        """
        temp_path = self.path.with_name(self.path.name + ".tmp")
        with open(temp_path, "w", encoding="utf-8") as file:
            # ensure_ascii=False: 한글을 \uXXXX가 아닌 글자 그대로 저장
            json.dump(data, file, ensure_ascii=False, indent=4)
        os.replace(temp_path, self.path)

    def backup_corrupted(self):
        """손상된 파일을 state.json.corrupted로 옮겨 보관한다. 보관한 경로를 돌려준다."""
        backup_path = self.path.with_name(self.path.name + ".corrupted")
        try:
            os.replace(self.path, backup_path)
        except OSError:
            return None
        return backup_path
