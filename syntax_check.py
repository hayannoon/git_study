import os
import json
import ast
import subprocess
import xml.etree.ElementTree as ET

def check_python_syntax(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            ast.parse(f.read(), filename=file_path)
        return True, None
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}, column {e.offset}: {e.msg}"

def check_json_format(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"JSONDecodeError at line {e.lineno}, column {e.colno}: {e.msg}"

def check_xml_format(file_path):
    try:
        ET.parse(file_path)
        return True, None
    except ET.ParseError as e:
        return False, f"XML ParseError at line {e.position[0]}, column {e.position[1]}: {e.msg}"

def check_cpp_syntax(file_path):
    try:
        result = subprocess.run(["clang++", "-fsyntax-only", file_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if result.returncode == 0:
            return True, None
        return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def check_java_syntax(file_path):
    try:
        result = subprocess.run(["javac", "-Xlint", "-d", "/tmp", file_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if result.returncode == 0:
            return True, None
        return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def check_kotlin_syntax(file_path):
    try:
        result = subprocess.run(
            ["kotlinc", "-Xuse-ir", "-d", "/tmp", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return True, None
        return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def check_files_in_directory(directory):
    results = []
    for root, _, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            ext = os.path.splitext(name.lower())[1]

            if ext == ".py":
                valid, msg = check_python_syntax(file_path)
                file_type = "Python"
            elif ext == ".json":
                valid, msg = check_json_format(file_path)
                file_type = "JSON"
            elif ext == ".xml":
                valid, msg = check_xml_format(file_path)
                file_type = "XML"
            elif ext == ".cpp":
                valid, msg = check_cpp_syntax(file_path)
                file_type = "C++"
            elif ext == ".java":
                valid, msg = check_java_syntax(file_path)
                file_type = "Java"
            elif ext == ".kt":
                valid, msg = check_kotlin_syntax(file_path)
                file_type = "Kotlin"
            else:
                continue

            results.append({
                "file": file_path,
                "type": file_type,
                "valid": valid,
                "message": msg
            })

    return results

def summarize_and_print_results(results):
    total = len(results)
    errors = [r for r in results if not r["valid"]]
    valid_count = total - len(errors)

    print("\n====================== 검사 결과 요약 ======================")
    print(f"총 검사 파일 수    : {total}")
    print(f"정상 파일 수      : {valid_count}")
    print(f"문법 오류 파일 수  : {len(errors)}")

    if total > 0:
        print("\n📊 형식별 요약:")
        type_counts = {}
        for r in results:
            t = r["type"]
            if t not in type_counts:
                type_counts[t] = {"total": 0, "errors": 0}
            type_counts[t]["total"] += 1
            if not r["valid"]:
                type_counts[t]["errors"] += 1

        for t, stats in type_counts.items():
            print(f" - {t:<6}: 총 {stats['total']}개 중 오류 {stats['errors']}개")

    if errors:
        print("\n🔴 Syntax Error details:")
        for r in errors:
            print("------------------------------------------------------")
            print(f"파일명    : {r['file']}")
            print(f"파일 형식 : {r['type']}")
            print(f"오류 내용 : {r['message']}")
    print("==========================================================\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("사용법: python syntax_check.py <디렉토리 경로>")
        sys.exit(1)

    path_to_check = sys.argv[1]
    result_data = check_files_in_directory(path_to_check)
    summarize_and_print_results(result_data)

    # 결과를 result.json 파일로 저장
    # 결과를 result 파일로 저장
    has_error = any(not r["valid"] for r in result_data)
    status = "fail" if has_error else "pass"

    # summarize_and_print_results의 출력을 문자열로 저장
    import io
    import contextlib

    summary_output = io.StringIO()
    with contextlib.redirect_stdout(summary_output):
        summarize_and_print_results(result_data)
    summary_text = summary_output.getvalue()

    with open("result", "w", encoding="utf-8") as f:
        f.write(f"{status}\n")
        f.write(summary_text)
        
    # GitHub Actions에서 실패 처리하도록 오류가 있으면 exit(1)
    if any(not r["valid"] for r in result_data):
        sys.exit(1)
