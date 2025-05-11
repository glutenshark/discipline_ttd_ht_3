# Универсальный скрипт запуска pytest с HTML-отчётом и покрытием кода
# Работает на Windows, Linux, macOS
import os
import subprocess
import sys
import webbrowser

LOG = "report_log.txt"
VENV_DIR = "venv"
REQ_FILE = "requirements.txt"
REPORT_FILE = "report.html"


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)


def run(cmd, shell=False):
    result = subprocess.run(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log(result.stdout)
    return result.returncode


def create_venv():
    log("Создание виртуального окружения...")
    return run([sys.executable, "-m", "venv", VENV_DIR]) == 0


def install_requirements(pip_cmd):
    log("Установка зависимостей...")
    return run([pip_cmd, "install", "-r", REQ_FILE]) == 0


def run_pytest(python_cmd):
    log("Запуск тестов и генерация отчёта...")
    return run([
        python_cmd, "-m", "pytest",
        "--html=" + REPORT_FILE,
        "--self-contained-html",
        "--cov=.", "--cov-report=json:coverage.json"
    ]) == 0


def main():
    if os.path.exists(LOG):
        os.remove(LOG)

    log("Запуск сборки отчёта PyTest")

    venv_bin = os.path.join(VENV_DIR, "Scripts" if os.name == "nt" else "bin")
    python_cmd = os.path.join(venv_bin, "python")
    pip_cmd = os.path.join(venv_bin, "pip")

    if not os.path.exists(python_cmd):
        if not create_venv():
            log("Ошибка при создании venv.")
            return

    if not install_requirements(pip_cmd):
        log("Ошибка при установке зависимостей.")
        return

    if run_pytest(python_cmd):
        log("Все тесты выполнены.")
    else:
        log("Некоторые тесты завершились с ошибками.")

    if os.path.exists(REPORT_FILE):
        log("Открытие итогового отчёта...")
        webbrowser.open(os.path.abspath(REPORT_FILE))
    else:
        log("Файл отчёта не найден.")


if __name__ == "__main__":
    main()
