import json
import os
import threading
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def compute_task(n: int) -> int:
    return sum(i * i for i in range(n))

def io_task(filepath: str) -> str:
    with open(filepath, 'w') as f:
        f.write('benchmark io test')
    with open(filepath, 'r') as f:
        return f.read()

def benchmark():
    results = {'timestamp': datetime.utcnow().isoformat(), 'io_ms': 0, 'compute_ms': 0, 'thread_ms': 0}

    tmp = '/tmp/bench_io_test.txt'

    start = time.monotonic()
    io_task(tmp)
    os.remove(tmp)
    results['io_ms'] = round((time.monotonic() - start) * 1000, 3)

    start = time.monotonic()
    compute_task(100000)
    results['compute_ms'] = round((time.monotonic() - start) * 1000, 3)

    start = time.monotonic()
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = [ex.submit(compute_task, 50000) for _ in range(4)]
        [f.result() for f in futures]
    results['thread_ms'] = round((time.monotonic() - start) * 1000, 3)

    return results

def main():
    res = benchmark()
    header = 'timestamp\tio_ms\tcompute_ms\tthread_ms'
    row = f"{res['timestamp']}\t{res['io_ms']}\t{res['compute_ms']}\t{res['thread_ms']}"
    if not os.path.exists('data.tsv'):
        with open('data.tsv', 'w') as f:
            f.write(header + '\n')
    with open('data.tsv', 'a') as f:
        f.write(row + '\n')
    print(row)

if __name__ == '__main__':
    main()
