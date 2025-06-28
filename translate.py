import os
import sys
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def read_code(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write_tmp(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def ai_migrate(code):
    prompt = (
        "You are an agent - please keep going until the user’s query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved."
        "If you are not sure about file content or codebase structure pertaining to the user’s request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer."
        "Below is Python 3 code that was translated from Python 2 using 2to3. "
        "Please improve the code to make it more idiomatic and robust in Python 3, but only output the code with nothing else. Remember to remove ``` at the beginning and the end"
        "If any comments are added to explain key changes, include them inline.\n\n"
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


def run_2to3(src_path, dst_path):
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    # Copy src to dst
    with open(src_path, "r", encoding="utf-8") as src_file:
        code = src_file.read()
    with open(dst_path, "w", encoding="utf-8") as dst_file:
        dst_file.write(code)
    # Run 2to3 on dst
    subprocess.run(["2to3", "-w", "-n", dst_path], check=True)


def migrate_file(src_path, dst_path):
    # Step 1: 2to3 conversion (src_path → dst_path)
    run_2to3(src_path, dst_path)
    # Step 2: AI improvement
    code3 = read_code(dst_path)
    code3_improved = ai_migrate(code3)
    write_tmp(dst_path, code3_improved)


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
        print("Usage: python translate.py <python2_src_dir> <python3_dst_dir>")
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    migrate_dir(src, dst)


if __name__ == "__main__":
    main()
