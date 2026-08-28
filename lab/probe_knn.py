"""Does exact kNN stay affordable at our scale, or do we need an ANN index (faiss)?

Matters because neighborhood-stability is a candidate faithfulness probe, and an ANN
index's own recall error would contaminate the measurement it is being used to take.
"""
import time
import torch

d = torch.device("cuda")
DIM = 128
K = 20

def timed(fn, warmup=1, reps=3):
    for _ in range(warmup):
        fn()
    torch.cuda.synchronize()          # without this we time queue submission, not compute
    t0 = time.perf_counter()
    for _ in range(reps):
        fn()
    torch.cuda.synchronize()
    return (time.perf_counter() - t0) / reps

print(f"{'N':>9} {'exact kNN (s)':>14} {'peak VRAM MiB':>14}  {'chunked':>8}")
for n in (10_000, 50_000, 100_000, 250_000):
    torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    x = torch.randn(n, DIM, device=d)
    x = torch.nn.functional.normalize(x, dim=1)
    # Chunk the query side so the N*N similarity matrix never materializes at once.
    chunk = max(1, min(n, int(2e8 // n)))
    def run():
        for i in range(0, n, chunk):
            sim = x[i : i + chunk] @ x.T
            sim.topk(K, dim=1)
    try:
        secs = timed(run)
        print(f"{n:>9,} {secs:>14.3f} {torch.cuda.max_memory_allocated()/2**20:>14.1f}  {chunk:>8,}")
    except torch.cuda.OutOfMemoryError:
        print(f"{n:>9,} {'OOM':>14}")
    del x

# The async trap, demonstrated rather than asserted.
x = torch.nn.functional.normalize(torch.randn(50_000, DIM, device=d), dim=1)
torch.cuda.synchronize()
t0 = time.perf_counter(); (x @ x[:20_000].T).topk(K, dim=1); naive = time.perf_counter() - t0
torch.cuda.synchronize(); honest = time.perf_counter() - t0
print(f"\nunsynchronized timing: {naive*1000:.1f} ms   |   synchronized: {honest*1000:.1f} ms"
      f"   -> understates by {honest/naive:.1f}x")
