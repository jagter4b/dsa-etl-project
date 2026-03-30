import csv
import time
import bisect
import copy
import os
from datetime import datetime


def load_data(filepath):
    records = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['Order ID']      = int(row['Order ID'])
            row['Units Sold']    = int(row['Units Sold'])
            row['Unit Price']    = float(row['Unit Price'])
            row['Unit Cost']     = float(row['Unit Cost'])
            row['Total Revenue'] = float(row['Total Revenue'])
            row['Total Cost']    = float(row['Total Cost'])
            row['Total Profit']  = float(row['Total Profit'])
            records.append(row)
    print(f"[Loader] Loaded {len(records):,} records.")
    return records


#  Sorting Algorithms 

def bubble_sort(data, key):
    arr = copy.deepcopy(data)
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j][key] > arr[j + 1][key]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(data, key):
    arr = copy.deepcopy(data)
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and arr[j][key] > current[key]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr


def selection_sort(data, key):
    arr = copy.deepcopy(data)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j][key] < arr[min_idx][key]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def merge_sort(data, key):
    if len(data) <= 1:
        return data
    mid   = len(data) // 2
    left  = merge_sort(data[:mid], key)
    right = merge_sort(data[mid:], key)
    return _merge(left, right, key)

def _merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(data, key):
    if len(data) <= 1:
        return data
    pivot  = data[len(data) // 2][key]
    left   = [x for x in data if x[key] <  pivot]
    middle = [x for x in data if x[key] == pivot]
    right  = [x for x in data if x[key] >  pivot]
    return quick_sort(left, key) + middle + quick_sort(right, key)


#   benchmark 

def benchmark_sorts(data, key='Total Revenue'):
    algorithms = {
        'Bubble Sort    ': bubble_sort,
        'Insertion Sort ': insertion_sort,
        'Selection Sort ': selection_sort,
        'Merge Sort     ': merge_sort,
        'Quick Sort     ': quick_sort,
    }

    print("\n" + "=" * 50)
    print(f"  SORT BENCHMARK  |  key: '{key}'  |  n={len(data):,}")
    print("=" * 50)

    for name, func in algorithms.items():
        sample  = copy.deepcopy(data)
        start   = time.perf_counter()
        func(sample, key)
        elapsed = time.perf_counter() - start
        print(f"  {name} → {elapsed:.4f}s")

    sample = copy.deepcopy(data)
    start  = time.perf_counter()
    sample.sort(key=lambda x: x[key])
    elapsed = time.perf_counter() - start
    print(f"  Timsort (built-in) → {elapsed:.4f}s")
    print("=" * 50)


#  search algorithms 

def linear_search(data, target_id):
    for record in data:
        if record['Order ID'] == target_id:
            return record
    return None


def binary_search(sorted_data, target_id):
    low, high = 0, len(sorted_data) - 1
    while low <= high:
        mid    = (low + high) // 2
        mid_id = sorted_data[mid]['Order ID']
        if mid_id == target_id:
            return sorted_data[mid]
        elif mid_id < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return None


def benchmark_search(data, target_id):
    print("\n" + "=" * 50)
    print(f"  SEARCH BENCHMARK  |  Target Order ID: {target_id}")
    print("=" * 50)

    start  = time.perf_counter()
    result = linear_search(data, target_id)
    print(f"  Linear Search (unsorted) → {time.perf_counter() - start:.6f}s | Found: {result is not None}")

    sorted_by_id = sorted(data, key=lambda x: x['Order ID'])
    start  = time.perf_counter()
    result = binary_search(sorted_by_id, target_id)
    print(f"  Binary Search (sorted)   → {time.perf_counter() - start:.6f}s | Found: {result is not None}")

    if result:
        print(f"\n  Order ID : {result['Order ID']}")
        print(f"  Country  : {result['Country']}")
        print(f"  Revenue  : {result['Total Revenue']:,.2f}")
        print(f"  Profit   : {result['Total Profit']:,.2f}")
    print("=" * 50)


#  bisect time-series slicer 

def extract_date_range(data, start_date, end_date):
    def parse(d):
        return datetime.strptime(d, '%m/%d/%Y')

    sorted_data = sorted(data, key=lambda x: parse(x['Order Date']))
    dates       = [parse(r['Order Date']) for r in sorted_data]

    left  = bisect.bisect_left(dates,  parse(start_date))
    right = bisect.bisect_right(dates, parse(end_date))

    sliced = sorted_data[left:right]
    print(f"\n[Bisect] {start_date} → {end_date} | {len(sliced):,} transactions found.")
    return sliced


#  phase 1 runner 

def run_phase1(filepath):
    print("\n" + "=" * 50)
    print("  PHASE 1: THE QUERY OPTIMIZER")
    print("=" * 50)

    data = load_data(filepath)

    benchmark_sorts(data, key='Total Revenue')

    target_id = data[10]['Order ID']
    benchmark_search(data, target_id)

    q3 = extract_date_range(data, '7/1/2015', '9/30/2015')
    if q3:
        total = sum(r['Total Revenue'] for r in q3)
        print(f"[Bisect] Total Q3 2015 Revenue: {total:,.2f}\n")



if __name__ == '__main__':
    base     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base, 'data', 'sales_data.csv')
    run_phase1(csv_path)