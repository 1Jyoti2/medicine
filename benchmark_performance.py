"""
Performance Benchmark Suite for Medicine Application.
Measures:
1. API Startup & Warmup Time
2. Leaf Inference Time
3. Pill Inference Time
4. Prescription OCR Processing Time
5. End-to-End API Round-Trip Latency
"""

import time
import requests
from pathlib import Path
import numpy as np

BASE_URL = "http://127.0.0.1:8000"
PROJECT_ROOT = Path(__file__).resolve().parent


def benchmark_flow(name: str, endpoint: str, file_path: Path, n_runs: int = 5):
    print(f"\n--- Benchmarking {name} ({n_runs} runs) ---")
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return None

    with open(file_path, "rb") as f:
        img_bytes = f.read()

    latencies = []
    server_inference_times = []

    for i in range(n_runs):
        start = time.perf_counter()
        r = requests.post(
            f"{BASE_URL}{endpoint}",
            files={"file": (file_path.name, img_bytes, "image/jpeg")},
            timeout=30
        )
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        
        if r.status_code == 200:
            data = r.json().get("data", {})
            srv_time = data.get("inferenceTimeMs") or data.get("processingTimeMs") or 0.0
            latencies.append(elapsed_ms)
            server_inference_times.append(srv_time)
            print(f"  Run {i+1}: API Round-Trip = {elapsed_ms:.1f}ms | Server ML Time = {srv_time:.1f}ms")
        else:
            print(f"  Run {i+1}: FAILED (status {r.status_code})")

    if latencies:
        avg_rt = np.mean(latencies)
        p50_rt = np.median(latencies)
        p95_rt = np.percentile(latencies, 95)
        avg_srv = np.mean(server_inference_times)
        print(f"  => Results for {name}:")
        print(f"     Average Round-Trip: {avg_rt:.2f} ms (p50: {p50_rt:.2f} ms, p95: {p95_rt:.2f} ms)")
        print(f"     Average Server ML Time: {avg_srv:.2f} ms")
        return {"avg_rt": avg_rt, "p50_rt": p50_rt, "p95_rt": p95_rt, "avg_srv": avg_srv}
    return None


def main():
    print("=" * 80)
    print("STARTING PERFORMANCE BENCHMARK")
    print("=" * 80)

    # 1. Health check
    t0 = time.perf_counter()
    r = requests.get(f"{BASE_URL}/health")
    health_latency = (time.perf_counter() - t0) * 1000.0
    print(f"Health Check Latency: {health_latency:.2f} ms")

    # Locate test images
    leaf_samples = list((PROJECT_ROOT / "ml_training" / "data" / "leaf_processed").rglob("*.jpg"))
    rx_samples = list((PROJECT_ROOT / "datasets" / "handwritten_pages_jpg").glob("*.jpg"))
    pill_samples = list((PROJECT_ROOT / "datasets" / "small_dataset_20_images").rglob("*.jpg"))

    results = {}

    if leaf_samples:
        results["leaf"] = benchmark_flow("Leaf Classification", "/predict/leaf", leaf_samples[0], n_runs=5)

    if pill_samples:
        results["pill"] = benchmark_flow("Pill Identification", "/predict/pill", pill_samples[0], n_runs=5)

    if rx_samples:
        results["ocr"] = benchmark_flow("Prescription OCR", "/predict/prescription", rx_samples[0], n_runs=3)

    print("\n" + "=" * 80)
    print("BENCHMARK SUMMARY")
    print("=" * 80)
    for flow, res in results.items():
        if res:
            print(f"{flow.upper():<15}: Server ML = {res['avg_srv']:.1f}ms | Total API = {res['avg_rt']:.1f}ms")
    print("=" * 80)


if __name__ == "__main__":
    main()
