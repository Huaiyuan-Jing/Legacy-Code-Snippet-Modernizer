import os
import sys
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def read_code(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def ai_migrate(code):
    prompt = (
        "Below is Python 2 code. Convert it to semantically equivalent Python 3 code. Make sure only output raw code with nothing extra infomation."
        "Include comments explaining key changes.\n\n"
        f"{code}"
    )
    resp = client.responses.create(
        model="gpt-4.1",
        input=prompt,
    )
    return resp.output_text


def write_tmp(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def run_2to3(path):
    subprocess.run(["2to3", "-w", "-n", path], check=True)


def migrate_file(src_path, dst_path):
    code2 = read_code(src_path)
    code3 = ai_migrate(code2)
    write_tmp(dst_path, code3)
    run_2to3(dst_path)


def migrate_dir(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for fname in os.listdir(src_dir):
        if not fname.endswith(".py"):
            continue
        migrate_file(
            os.path.join(src_dir, fname),
            os.path.join(dst_dir, fname),
        )


def main():
    if len(sys.argv) != 3:
        print("Usage: python migrate.py <python2_src_dir> <python3_dst_dir>")
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    migrate_dir(src, dst)


if __name__ == "__main__":
    main()
