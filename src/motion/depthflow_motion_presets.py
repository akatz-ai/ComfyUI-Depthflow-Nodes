from DepthFlow.Motion import Presets
from ..base_flex import BaseFlex

class DepthflowMotionPreset(BaseFlex):
    CATEGORY = "🌊 Depthflow/Motion/Presets"
    RETURN_TYPES = ("DEPTHFLOW_MOTION",)

class DepthflowMotionPresetCircle(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "intensity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01}),
                "reverse": ("BOOLEAN", {"default": False}),
                "smooth": ("BOOLEAN", {"default": True}),
                "phase_x": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.01}),
                "phase_y": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.01}),
                "phase_z": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.01}),
                "amplitude_x": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "amplitude_y": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "amplitude_z": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "static_value": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }
        
    DESCRIPTION = """
    Depthflow Motion Preset Circle Node:
    This node allows the user to configure the circle motion preset.
    - intensity: Intensity of the circle motion
    - reverse: Reverse the circle motion
    - smooth: Smooth the circle motion
    - phase_x: X phase of the circle motion
    - phase_y: Y phase of the circle motion
    - phase_z: Z phase of the circle motion
    - amplitude_x: X amplitude of the circle motion
    - amplitude_y: Y amplitude of the circle motion
    - amplitude_z: Z amplitude of the circle motion
    - static_value: Static value of the circle motion
    """
        
    @classmethod
    def get_modifiable_params(cls):
        return ["intensity", "phase_x", "phase_y", "phase_z", "amplitude_x", "amplitude_y", "amplitude_z", "static_value", "None"]

    def create_internal(self, intensity, reverse, smooth, phase_x, phase_y, phase_z, amplitude_x, amplitude_y, amplitude_z, static_value, **kwargs):
        # Create the Circle preset object with the provided parameters
        preset = Presets.Circle(
            intensity=intensity,
            reverse=reverse,
            smooth=smooth,
            phase=(phase_x, phase_y, phase_z),
            amplitude=(amplitude_x, amplitude_y, amplitude_z),
            static=static_value,
        )
        return (preset,)
      
      
class DepthflowMotionPresetZoom(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "intensity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1}),
                "reverse": ("BOOLEAN", {"default": False}),
                "smooth": ("BOOLEAN", {"default": True}),
                "phase": ("FLOAT", {"default": 0.0}),
                "loop": ("BOOLEAN", {"default": False}),
            }
        }
        
    DESCRIPTION = """
    Depthflow Motion Preset Zoom Node:
    This node allows the user to configure the zoom motion preset.
    - intensity: Intensity of the zoom motion
    - reverse: Reverse the zoom motion
    - smooth: Smooth the zoom motion
    - phase: Phase of the zoom motion
    - loop: Loop the zoom motion
    """
    
    @classmethod
    def get_modifiable_params(cls):
        return ["intensity", "phase", "None"]

    def create_internal(self, intensity, reverse, smooth, phase, loop, **kwargs):
        # Create the Zoom preset object with the provided parameters
        preset = Presets.Zoom(
            intensity=intensity,
            reverse=reverse,
            smooth=smooth,
            phase=phase,
            loop=loop,
        )
        return (preset,)


class DepthflowMotionPresetDolly(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "intensity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1}),
                "reverse": ("BOOLEAN", {"default": False}),
                "smooth": ("BOOLEAN", {"default": True}),
                "loop": ("BOOLEAN", {"default": True}),
                "depth": ("FLOAT", {"default": 0.5}),
            }
        }
        
    DESCRIPTION = """
    Depthflow Motion Preset Dolly Node:
    This node allows the user to configure the dolly motion preset.
    - intensity: Intensity of the dolly motion
    - reverse: Reverse the dolly motion
    - smooth: Smooth the dolly motion
    - loop: Loop the dolly motion
    """
    
    @classmethod
    def get_modifiable_params(cls):
        return ["intensity", "depth", "None"]

    def create_internal(self, intensity, reverse, smooth, loop, depth, **kwargs):
        # Create the Dolly preset object with the provided parameters
        preset = Presets.Dolly(
            intensity=intensity,
            reverse=reverse,
            smooth=smooth,
            loop=loop,
            depth=depth,
        )
        return (preset,)


class DepthflowMotionPresetVertical(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "intensity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1}),
                "reverse": ("BOOLEAN", {"default": False}),
                "smooth": ("BOOLEAN", {"default": True}),
                "loop": ("BOOLEAN", {"default": True}),
                "phase": ("FLOAT", {"default": 0.0}),
                "static_value": ("FLOAT", {"default": 0.3}),
            }
        }
        
    DESCRIPTION = """
    Depthflow Motion Preset Vertical Node:
    This node allows the user to configure the vertical motion preset.
    - intensity: Intensity of the vertical motion
    - reverse: Reverse the vertical motion
    - smooth: Smooth the vertical motion
    - loop: Loop the vertical motion
    """
    
    @classmethod
    def get_modifiable_params(cls):
        return ["intensity", "phase", "static_value", "None"]

    def create_internal(self, intensity, reverse, smooth, loop, phase, static_value, **kwargs):
        # Create the Vertical preset object with the provided parameters
        preset = Presets.Vertical(
            intensity=intensity,
            reverse=reverse,
            smooth=smooth,
            loop=loop,
            phase=phase,
            static=static_value,
        )
        return (preset,)


class DepthflowMotionPresetHorizontal(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "intensity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1}),
                "reverse": ("BOOLEAN", {"default": False}),
                "smooth": ("BOOLEAN", {"default": True}),
                "loop": ("BOOLEAN", {"default": True}),
                "phase": ("FLOAT", {"default": 0.0}),
                "static_value": ("FLOAT", {"default": 0.3}),
            }
        }
        
    DESCRIPTION = """
    Depthflow Motion Preset Horizontal Node:
    This node allows the user to configure the horizontal motion preset.
    - intensity: Intensity of the horizontal motion
    - reverse: Reverse the horizontal motion
    - smooth: Smooth the horizontal motion
    - loop: Loop the horizontal motion
    """
    
    
    @classmethod
    def get_modifiable_params(cls):
        return ["intensity", "phase", "static_value", "None"]

    def create_internal(self, intensity, reverse, smooth, loop, phase, static_value, **kwargs):
        # Create the Horizontal preset object with the provided parameters
        preset = Presets.Horizontal(
            intensity=intensity,
            reverse=reverse,
            smooth=smooth,
            loop=loop,
            phase=phase,
            static=static_value,
        )
        return (preset,)
    
class DepthflowMotionPresetOrbital(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "intensity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1}),
                "depth": ("FLOAT", {"default": 0.5}),
                "reverse": ("BOOLEAN", {"default": False}),
            }
        }
        
    DESCRIPTION = """
    Depthflow Motion Preset Orbital Node:
    This node allows the user to configure the orbital motion preset.
    - intensity: Intensity of the orbital motion
    - depth: Depth of the orbital motion
    - reverse: Reverse the orbital motion
    """
    
    @classmethod
    def get_modifiable_params(cls):
        return ["intensity", "depth", "None"]

    def create_internal(self, intensity, depth, reverse, **kwargs):
        # Create the Orbital preset object with the provided parameters
        preset = Presets.Orbital(
            intensity=intensity,
            depth=depth,
            reverse=reverse
        )
        return (preset,)
    