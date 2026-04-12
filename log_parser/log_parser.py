import argparse
import json
import os
import re
from collections import Counter
from heapq import heappush, heappushpop


LOG_PATTERN = re.compile(
    r"^(?P<ip>\S+) - - "
    r"(?P<date>\[[^\]]+\]) "
    r'"(?P<request>[^"]*)" '
    r"(?P<status>\d{3}) "
    r"(?P<bytes>\S+) "
    r'"(?P<referer>[^"]*)" '
    r'"(?P<user_agent>[^"]*)" '
    r"(?P<duration>\d+)$"
)

METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"]


def parse_args():
    parser = argparse.ArgumentParser(description="Log parser")
    parser.add_argument("path")
    return parser.parse_args()


def get_log_files(path):
    if os.path.isfile(path):
        return [path]

    if os.path.isdir(path):
        result = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if os.path.isfile(full_path):
                result.append(full_path)
        return sorted(result)

    raise FileNotFoundError(f"Путь не найден: {path}")


def parse_request(request_line):
    parts = request_line.split()
    if len(parts) < 2:
        return None, None
    return parts[0], parts[1]


def analyze_log_file(file_path):
    total_requests = 0
    total_stat = Counter({method: 0 for method in METHODS})
    ip_counter = Counter()
    top_longest_heap = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.rstrip("\n")
            match = LOG_PATTERN.match(line)
            if not match:
                continue

            total_requests += 1

            ip = match.group("ip")
            date = match.group("date")
            request_line = match.group("request")
            duration = int(match.group("duration"))

            method, url = parse_request(request_line)

            ip_counter[ip] += 1

            if method in METHODS:
                total_stat[method] += 1

            record = {
                "ip": ip,
                "date": date,
                "method": method,
                "url": url if url else "-",
                "duration": duration,
            }

            heap_item = (duration, line_number, record)

            if len(top_longest_heap) < 3:
                heappush(top_longest_heap, heap_item)
            else:
                if duration > top_longest_heap[0][0]:
                    heappushpop(top_longest_heap, heap_item)

    top_ips = dict(ip_counter.most_common(3))
    top_longest = [
        item[2] for item in sorted(top_longest_heap, key=lambda x: (-x[0], x[1]))
    ]

    result = {
        "top_ips": top_ips,
        "top_longest": top_longest,
        "total_stat": {method: total_stat[method] for method in METHODS},
        "total_requests": total_requests,
    }

    return result


def save_result(file_path, result):
    base_name = os.path.basename(file_path)
    name_without_ext, _ = os.path.splitext(base_name)
    output_file = f"{name_without_ext}_result.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    return output_file


def main():
    args = parse_args()
    log_files = get_log_files(args.path)

    if not log_files:
        print("Файлы не найдены")
        return

    for file_path in log_files:
        result = analyze_log_file(file_path)
        output_file = save_result(file_path, result)

        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"JSON сохранён в файл: {output_file}")


if __name__ == "__main__":
    main()
