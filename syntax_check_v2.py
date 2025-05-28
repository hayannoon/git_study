import os
import subprocess
import ast
import json
import xml.etree.ElementTree as ET
from pathlib import Path

LOG_FILE = "syntax_check_result.log"
errors = []
log_lines = []

SUPPORTED_EXTENSIONS = {".py", ".json", ".xml", ".c", ".cpp", ".cc", ".cxx", ".java"}

def log(msg, is_error=False):
    print(msg)
    log_lines.append(msg)
    if is_error:
        errors.append(msg)

def check_python(path):
    try:
        ast.parse(Path(path).read_text(encoding="utf-8"))
        log(f"✅ PYTHON OK: {path}")
    except SyntaxError as e:
        log(f"❌ PYTHON ERROR in {path}:\n   {e}", is_error=True)

def check_json(path):
    try:
        json.loads(Path(path).read_text(encoding="utf-8"))
        log(f"✅ JSON OK: {path}")
    except json.JSONDecodeError as e:
        log(f"❌ JSON ERROR in {path}:\n   {e}", is_error=True)

def check_xml(path):
    try:
        ET.parse(path)
        log(f"✅ XML OK: {path}")
    except ET.ParseError as e:
        log(f"❌ XML ERROR in {path}:\n   {e}", is_error=True)

def check_cpp(path):
    result = subprocess.run(
        ["cppcheck", "--force", "--template=gcc", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    combined_output = (result.stdout + result.stderr).strip()
    lower_output = combined_output.lower()

    if (
        result.returncode != 0 or
        "error:" in lower_output or
        "syntaxerror" in lower_output or
        "parseerror" in lower_output
    ):
        log(f"❌ CPP SYNTAX ERROR in {path}:\n{combined_output}", is_error=True)
    else:
        log(f"✅ CPP OK: {path}")

def check_java(path):
    result = subprocess.run([
        "pmd/bin/run.sh", "check", "-d", str(path),
        "-f", "text", "-R", "rulesets/java/quickstart.xml"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    combined_output = (result.stdout + result.stderr).strip()
    lower_output = combined_output.lower()

    if "syntax error" in lower_output or "parseexception" in lower_output:
        log(f"❌ JAVA SYNTAX ERROR in {path}:\n{combined_output}", is_error=True)
    else:
        log(f"✅ JAVA OK: {path}")

def main():
    for file in Path(".").rglob("*"):
        if not file.is_file():
            continue
        if file.suffix not in SUPPORTED_EXTENSIONS:
            continue

        suffix = file.suffix

        if suffix == ".py":
            check_python(file)
        elif suffix == ".json":
            check_json(file)
        elif suffix == ".xml":
            check_xml(file)
        elif suffix in [".c", ".cpp", ".cc", ".cxx"]:
            check_cpp(file)
        elif suffix == ".java":
            check_java(file)

    # 로그 파일 저장
    header = "PASS" if not errors else "FAIL"
    log_lines.insert(0, header)
    Path(LOG_FILE).write_text("\n".join(log_lines), encoding="utf-8")

    if errors:
        print(f"\n❌ Syntax errors found. See {LOG_FILE} for details.")
        exit(1)
    else:
        print(f"\n✅ All files passed. See {LOG_FILE} for details.")

if __name__ == "__main__":
    main()