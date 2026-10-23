"""Regression tests for passing motion component options through to Depthflow."""

import importlib
import sys
import types
import unittest
from enum import Enum
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))


class FakeAnimationComponent:
    """Minimal Depthflow component model; cumulative defaults to False upstream."""

    def __init__(self, **kwargs):
        self.cumulative = kwargs.pop("cumulative", False)
        self.kwargs = kwargs


class FakeAnimation:
    Sine = staticmethod(lambda **kwargs: FakeAnimationComponent(**kwargs))
    Cosine = staticmethod(lambda **kwargs: FakeAnimationComponent(**kwargs))
    Linear = staticmethod(lambda **kwargs: FakeAnimationComponent(**kwargs))
    Triangle = staticmethod(lambda **kwargs: FakeAnimationComponent(**kwargs))


class FakeTarget(Enum):
    Nothing = "nothing"


def load_motion_components_with_stubs():
    """Import the actual node wrappers without loading ComfyUI or GPU libraries."""
    fake_modules = {
        "pydantic": types.SimpleNamespace(Field=lambda default=None, **kwargs: default),
        "broken": types.SimpleNamespace(BrokenEnum=Enum),
        "depthflow": types.ModuleType("depthflow"),
        "depthflow.animation": types.SimpleNamespace(
            Animation=FakeAnimation,
            ComponentBase=FakeAnimationComponent,
            Target=FakeTarget,
        ),
        "comfy": types.ModuleType("comfy"),
        "comfy.utils": types.SimpleNamespace(ProgressBar=object),
    }
    fake_modules["depthflow"].__path__ = []
    fake_modules["comfy"].__path__ = []

    package_modules = (
        "src",
        "src.motion",
        "src.base_flex",
        "src.motion.depthflow_motion_base",
        "src.motion.depthflow_motion_components",
    )
    names = tuple(fake_modules) + package_modules
    missing = object()
    original = {name: sys.modules.get(name, missing) for name in names}
    try:
        sys.modules.update(fake_modules)
        for name in package_modules:
            sys.modules.pop(name, None)
        return importlib.import_module("src.motion.depthflow_motion_components")
    finally:
        for name, module in original.items():
            if module is missing:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


class MotionCumulativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = load_motion_components_with_stubs()

    def assert_cumulative_is_forwarded(self, node_type, **kwargs):
        node = node_type()
        component = node.create_internal(target="Height", cumulative=True, **kwargs)[0]
        self.assertTrue(component.cumulative)

    def test_sine_forwards_cumulative(self):
        self.assert_cumulative_is_forwarded(
            self.nodes.DepthflowMotionSine,
            amplitude=1.0,
            cycles=1.0,
            phase=0.0,
            reverse=False,
            bias=0.0,
        )

    def test_cosine_forwards_cumulative(self):
        self.assert_cumulative_is_forwarded(
            self.nodes.DepthflowMotionCosine,
            amplitude=1.0,
            cycles=1.0,
            phase=0.0,
            reverse=False,
            bias=0.0,
        )

    def test_linear_forwards_cumulative(self):
        self.assert_cumulative_is_forwarded(
            self.nodes.DepthflowMotionLinear,
            start=0.0,
            end=1.0,
            low=0.0,
            high=1.0,
            exponent=1.0,
            reverse=False,
        )

    def test_triangle_forwards_cumulative(self):
        self.assert_cumulative_is_forwarded(
            self.nodes.DepthflowMotionTriangle,
            amplitude=1.0,
            cycles=1.0,
            phase=0.0,
            reverse=False,
            bias=0.0,
        )


if __name__ == "__main__":
    unittest.main()
