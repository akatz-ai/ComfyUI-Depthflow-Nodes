"""
@author: akatz
@title: Depthflow Nodes
@nickname: Depthflow Nodes
@description: Custom nodes for use with Tremeschin's Depthflow library.
"""

from .src.motion.depthflow_motion_components import DepthflowMotionSine, DepthflowMotionCosine, DepthflowMotionLinear, DepthflowMotionExponential, DepthflowMotionArc, DepthflowMotionSetTarget
from .src.motion.depthflow_motion_presets import DepthflowMotionPresetCircle, DepthflowMotionPresetZoom, DepthflowMotionPresetDolly, DepthflowMotionPresetVertical, DepthflowMotionPresetHorizontal, DepthflowMotionPresetOrbital
from .src.depthflow import Depthflow
from .src.effects.depthflow_effects import DepthflowEffectVignette, DepthflowEffectDOF

NODE_CONFIG = {
  "DepthflowMotionPresetCircle": {"class": DepthflowMotionPresetCircle, "name": "🌊 Depthflow Motion Preset Circle"},
  "DepthflowMotionPresetZoom": {"class": DepthflowMotionPresetZoom, "name": "🌊 Depthflow Motion Preset Zoom"},
  "DepthflowMotionPresetDolly": {"class": DepthflowMotionPresetDolly, "name": "🌊 Depthflow Motion Preset Dolly"},
  "DepthflowMotionPresetVertical": {"class": DepthflowMotionPresetVertical, "name": "🌊 Depthflow Motion Preset Vertical"},
  "DepthflowMotionPresetHorizontal": {"class": DepthflowMotionPresetHorizontal, "name": "🌊 Depthflow Motion Preset Horizontal"},
  "DepthflowMotionPresetOrbital": {"class": DepthflowMotionPresetOrbital, "name": "🌊 Depthflow Motion Preset Orbital"},
  "Depthflow": {"class": Depthflow, "name": "🌊 Depthflow"},
  "DepthflowEffectVignette": {"class": DepthflowEffectVignette, "name": "🌊 Depthflow Effect Vignette"},
  "DepthflowEffectDOF": {"class": DepthflowEffectDOF, "name": "🌊 Depthflow Effect DOF"},
  "DepthflowMotionSine": {"class": DepthflowMotionSine, "name": "🌊 Depthflow Motion Sine"},
  "DepthflowMotionCosine": {"class": DepthflowMotionCosine, "name": "🌊 Depthflow Motion Cosine"},
  "DepthflowMotionLinear": {"class": DepthflowMotionLinear, "name": "🌊 Depthflow Motion Linear"},
  "DepthflowMotionExponential": {"class": DepthflowMotionExponential, "name": "🌊 Depthflow Motion Exponential"},
  "DepthflowMotionArc": {"class": DepthflowMotionArc, "name": "🌊 Depthflow Motion Arc"},
  "DepthflowMotionSetTarget": {"class": DepthflowMotionSetTarget, "name": "🌊 Depthflow Motion Set Target"},
}


def generate_node_mappings(node_config):
    node_class_mappings = {}
    node_display_name_mappings = {}

    for node_name, node_info in node_config.items():
        node_class_mappings[node_name] = node_info["class"]
        node_display_name_mappings[node_name] = node_info.get("name", node_info["class"].__name__)

    return node_class_mappings, node_display_name_mappings

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = generate_node_mappings(NODE_CONFIG)

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', "WEB_DIRECTORY"]

ascii_art = """
🌊 DEPTHFLOW NODES 🌊
"""
print(ascii_art)