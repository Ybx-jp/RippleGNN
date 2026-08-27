"""The environment claims are machine-checked, because a scaffold that has not resolved
is a claim rather than an environment.

The CUDA assertions skip rather than fail when no device is present: this suite should be
honest on a CPU box, not red. On the development box (RTX 3060, sm_86) the skip not
firing is itself the check.
"""

import pytest
import torch

import ripple_gnn


def test_package_imports():
    assert ripple_gnn.__version__ == "0.1.0"


def test_torch_is_a_cuda_build():
    assert torch.version.cuda is not None, "resolved a CPU-only torch; check tool.uv.sources"


@pytest.mark.skipif(not torch.cuda.is_available(), reason="no CUDA device on this box")
def test_message_passing_runs_on_device():
    from torch_geometric.nn import SAGEConv

    device = torch.device("cuda")
    generator = torch.Generator(device=device).manual_seed(20260826)
    x = torch.randn(512, 32, device=device, generator=generator)
    edge_index = torch.randint(0, 512, (2, 4096), device=device, generator=generator)

    out = SAGEConv(32, 16).to(device)(x, edge_index)

    assert out.shape == (512, 16)
    assert torch.isfinite(out).all()
