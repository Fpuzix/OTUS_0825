import subprocess
from collections import Counter
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


console = Console()


def get_ps_output():
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True)
    return result.stdout


def parse_ps(ps_text):
    lines = ps_text.strip().split("\n")
    process_lines = lines[1:]

    users = []
    total_cpu = 0.0
    total_mem = 0.0

    max_cpu = {"value": -1.0, "command": ""}
    max_mem = {"value": -1.0, "command": ""}

    for line in process_lines:
        parts = line.split(None, 10)
        if len(parts) < 11:
            continue

        user = parts[0]
        cpu = float(parts[2])
        mem = float(parts[3])
        command = parts[10]

        users.append(user)
        total_cpu += cpu
        total_mem += mem

        if cpu > max_cpu["value"]:
            max_cpu["value"] = cpu
            max_cpu["command"] = command[:20]

        if mem > max_mem["value"]:
            max_mem["value"] = mem
            max_mem["command"] = command[:20]

    user_counts = Counter(users)
    unique_users = sorted(user_counts.keys())

    return {
        "users": unique_users,
        "total_processes": len(process_lines),
        "user_counts": user_counts,
        "total_mem": total_mem,
        "total_cpu": total_cpu,
        "max_mem_command": max_mem["command"],
        "max_cpu_command": max_cpu["command"],
    }


def build_report_text(data):
    lines = [
        "Отчёт о состоянии системы:",
        f"Пользователи системы: {', '.join(repr(user) for user in data['users'])}",
        f"Процессов запущено: {data['total_processes']}",
        "",
        "Пользовательских процессов:",
    ]

    for user, count in sorted(data["user_counts"].items()):
        lines.append(f"{user}: {count}")

    lines.extend(
        [
            "",
            f"Всего памяти используется: {data['total_mem']:.1f}%",
            f"Всего CPU используется: {data['total_cpu']:.1f}%",
            f"Больше всего памяти использует: {data['max_mem_command']}",
            f"Больше всего CPU использует: {data['max_cpu_command']}",
        ]
    )

    return "\n".join(lines)


def print_rich_report(data):
    console.print("\n[bold cyan]Отчёт о состоянии системы[/bold cyan]\n")

    users_str = ", ".join(f"'{user}'" for user in data["users"])
    console.print(f"[bold]Пользователи системы:[/bold] {users_str}")
    console.print(f"[bold]Процессов запущено:[/bold] {data['total_processes']}\n")

    table = Table(title="Пользовательские процессы")
    table.add_column("Пользователь", style="green")
    table.add_column("Количество процессов", justify="right", style="yellow")

    for user, count in sorted(data["user_counts"].items()):
        table.add_row(user, str(count))

    console.print(table)

    summary = (
        f"[bold]Всего памяти используется:[/bold] {data['total_mem']:.1f}%\n"
        f"[bold]Всего CPU используется:[/bold] {data['total_cpu']:.1f}%\n"
        f"[bold]Больше всего памяти использует:[/bold] {data['max_mem_command']}\n"
        f"[bold]Больше всего CPU использует:[/bold] {data['max_cpu_command']}"
    )

    console.print(Panel(summary, title="Сводка", expand=False))


def save_report(report_text):
    filename = datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report_text)
    return filename


def main():
    ps_text = get_ps_output()
    data = parse_ps(ps_text)

    print_rich_report(data)

    report_text = build_report_text(data)
    filename = save_report(report_text)

    console.print(f"\n[bold green]Отчёт тут -->:[/bold green] {filename}")


if __name__ == "__main__":
    main()
