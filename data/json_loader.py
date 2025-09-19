import os
import json

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

def load_json(file_name: str) -> dict:
    file_path = os.path.join(DATA_DIR, file_name)
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] {file_path} 파일을 찾을 수 없습니다.")
        return {}
    except json.JSONDecodeError:
        print(f"[ERROR] {file_path} 파일을 JSON으로 파싱할 수 없습니다.")
        return {}
