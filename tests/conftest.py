import io
import re
import time
import pytest
import matplotlib.pyplot as plt

# Глобальная сводка по результатам тестов
results_summary = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "xfailed": 0,
    "xpassed": 0,
    "errors": 0,
    "total_duration": 0.0
}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для сбора статистики по результатам тестов.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        results_summary["total"] += 1
        results_summary["total_duration"] += getattr(report, "duration", 0)
        if report.passed:
            if hasattr(report, "wasxfail"):
                results_summary["xpassed"] += 1
            else:
                results_summary["passed"] += 1
        elif report.failed:
            if hasattr(report, "wasxfail"):
                results_summary["xfailed"] += 1
            else:
                results_summary["failed"] += 1
        elif report.skipped:
            results_summary["skipped"] += 1
    elif report.failed:
        results_summary["total"] += 1
        results_summary["errors"] += 1


@pytest.hookimpl(trylast=True)
def pytest_html_results_summary(prefix, summary, postfix, session):
    """
    Хук генерации раздела Summary HTML-отчёта pytest-html.
    Вставляет графики, таблицу итогов и README.
    """
    # Чтение покрытия кода из htmlcov/index.html
    cov_percent = None
    cov_covered = None
    cov_missing = None

    try:
        with open("htmlcov/index.html", encoding="utf-8") as f:
            htmlcov = f.read()

        match = re.search(
            r"<tr class=['\"]total['\"].*?<td>(\d+)</td>\s*<td>(\d+)</td>\s*<td>(\d+)%</td>",
            htmlcov, re.DOTALL
        )
        if match:
            total_stmts = int(match.group(1))
            total_missed = int(match.group(2))
            cov_percent = int(match.group(3))
            cov_covered = total_stmts - total_missed
            cov_missing = total_missed
    except Exception:
        cov_percent = None

    # Генерация SVG-графика покрытия
    svg_cov_chart = ""
    if cov_percent is not None and cov_covered is not None:
        labels = [f"Covered ({cov_covered})", f"Missed ({cov_missing})"]
        sizes = [cov_covered, cov_missing]
        colors = ["#4caf50", "#f44336"]

        plt.figure(figsize=(4, 4))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%')
        plt.title(f"Coverage: {cov_percent}%")
        buf = io.StringIO()
        plt.savefig(buf, format='svg')
        plt.close()
        svg_data = buf.getvalue()
        svg_start = svg_data.find("<svg")
        svg_end = svg_data.rfind("</svg>")
        if svg_start != -1 and svg_end != -1:
            svg_cov_chart = svg_data[svg_start:svg_end + 6]

    # Генерация SVG-графика по тестам
    svg_result_chart = ""
    result_labels = []
    sizes = []
    colors = []

    for label, key, color in [
        ("Passed", "passed", "#4caf50"),
        ("Failed", "failed", "#f44336"),
        ("Skipped", "skipped", "#ff9800"),
        ("XFailed", "xfailed", "#9E9E9E"),
        ("XPassed", "xpassed", "#2196F3"),
    ]:
        count = results_summary.get(key, 0)
        if count > 0:
            result_labels.append(f"{label} ({count})")
            sizes.append(count)
            colors.append(color)

    if sizes:
        plt.figure(figsize=(4, 4))
        plt.pie(sizes, labels=result_labels, colors=colors, autopct='%1.0f%%')
        plt.title("Test Results")
        buf = io.StringIO()
        plt.savefig(buf, format='svg')
        plt.close()
        svg_data = buf.getvalue()
        svg_start = svg_data.find("<svg")
        svg_end = svg_data.rfind("</svg>")
        if svg_start != -1 and svg_end != -1:
            svg_result_chart = svg_data[svg_start:svg_end + 6]

    # Таблица итогов
    avg_time_ms = int((results_summary["total_duration"] / results_summary["total"]) * 1000) if results_summary["total"] else 0
    table_html = (
        "<div><h4>Итоги тестов:</h4>"
        "<table style='border-collapse: collapse; text-align: center;'>"
        "<tr style='background: #f2f2f2;'>"
        "<th>Всего</th><th>Пройдено</th><th>Провалено</th>"
        "<th>Пропущено</th><th>Среднее время</th><th>Покрытие</th></tr>"
        f"<tr><td>{results_summary['total']}</td>"
        f"<td style='color:green;'>{results_summary['passed']}</td>"
        f"<td style='color:red;'>{results_summary['failed']}</td>"
        f"<td style='color:orange;'>{results_summary['skipped']}</td>"
        f"<td>{avg_time_ms} ms</td>"
        f"<td>{cov_percent if cov_percent is not None else '-'}</td></tr>"
        "</table></div>"
    )

    # Формируем итоговый HTML
    html_parts = []

    try:
        with open("README.md", encoding="utf-8") as f:
            readme_md = f.read()
        html_parts.append(f"<hr><h2>README</h2><pre>{readme_md}</pre><hr>")
    except Exception as e:
        html_parts.append(f"<p><b>README.md не найден: {e}</b></p>")

    if svg_cov_chart:
        html_parts.append(f"<div>{svg_cov_chart}</div>")

    if svg_result_chart:
        html_parts.append(f"<div>{svg_result_chart}</div>")

    html_parts.append(table_html)

    prefix.extend(html_parts)
