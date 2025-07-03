from depthflow.animation import Animation

from ..base_flex import BaseFlex


class DepthflowMotionPreset(BaseFlex):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "intensity": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01},
                ),
                "reverse": ("BOOLEAN", {"default": False}),
            },
        }

    CATEGORY = "🌊 Depthflow/Motion/Presets"
    RETURN_TYPES = ("DEPTHFLOW_MOTION",)


class DepthflowMotionPresetCircle(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "smooth": ("BOOLEAN", {"default": True}),
                "phase_x": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "phase_y": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "phase_z": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "amplitude_x": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "amplitude_y": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "amplitude_z": (
                    "FLOAT",
                    {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "static_value": (
                    "FLOAT",
                    {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
            },
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
        return [
            "intensity",
            "phase_x",
            "phase_y",
            "phase_z",
            "amplitude_x",
            "amplitude_y",
            "amplitude_z",
            "static_value",
            "None",
        ]

    def create_internal(
        self,
        intensity,
        reverse,
        smooth,
        phase_x,
        phase_y,
        phase_z,
        amplitude_x,
        amplitude_y,
        amplitude_z,
        static_value,
        **kwargs,
    ):
        # Create the Circle preset object with the provided parameters
        preset = Animation.Circle(
            intensity=intensity,
            reverse=reverse,
            phase=(phase_x, phase_y, phase_z),
            amplitude=(amplitude_x, amplitude_y, amplitude_z),
            steady=static_value,
            isometric=0.6,  # Default value from new API
        )
        return (preset,)


class DepthflowMotionPresetZoom(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "smooth": ("BOOLEAN", {"default": True}),
                "phase": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "loop": ("BOOLEAN", {"default": False}),
            },
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
        preset = Animation.Zoom(
            intensity=intensity,
            reverse=reverse,
            smooth=smooth,
            phase=phase,
            loop=loop,
            isometric=0.8,  # Default value from new API
        )
        return (preset,)


class DepthflowMotionPresetDolly(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "smooth": ("BOOLEAN", {"default": True}),
                "loop": ("BOOLEAN", {"default": True}),
                "depth": (
                    "FLOAT",
                    {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
            },
        }

    DESCRIPTION = """
    Depthflow Motion Preset Dolly Node:
    This node allows the user to configure the dolly motion preset.
    - intensity: Intensity of the dolly motion
    - reverse: Reverse the dolly motion
    - smooth: Smooth the dolly motion
    - loop: Loop the dolly motion
    - depth: Depth of the dolly motion
    """

    @classmethod
    def get_modifiable_params(cls):
        return ["intensity", "depth", "None"]

    def create_internal(self, intensity, reverse, smooth, loop, depth, **kwargs):
        # Create the Dolly preset object with the provided parameters
        preset = Animation.Dolly(
            intensity=intensity,
            reverse=reverse,
            smooth=smooth,
            loop=loop,
            focus=depth,  # Changed from 'depth' to 'focus' in new API
            phase=0.0,  # Default value from new API
        )
        return (preset,)


class DepthflowMotionPresetVertical(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "loop": ("BOOLEAN", {"default": True}),
                "smooth": ("BOOLEAN", {"default": True}),
                "phase": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "steady_value": (
                    "FLOAT",
                    {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
            },
        }

    DESCRIPTION = """
    Depthflow Motion Preset Vertical Node:
    This node allows the user to configure the vertical motion preset.
    - intensity: Intensity of the vertical motion
    - reverse: Reverse the vertical motion
    - smooth: Smooth the vertical motion
    - loop: Loop the vertical motion
    - steady_value: Static value of the vertical motion
    """

    @classmethod
    def get_modifiable_params(cls):
        return ["intensity", "phase", "steady_value", "None"]

    def create_internal(
        self, intensity, reverse, smooth, loop, phase, steady_value, **kwargs
    ):
        # Create the Vertical preset object with the provided parameters
        preset = Animation.Vertical(
            intensity=intensity,
            reverse=reverse,
            smooth=smooth,
            loop=loop,
            phase=phase,
            steady=steady_value,
            isometric=0.6,  # Default value from new API
        )
        return (preset,)


class DepthflowMotionPresetHorizontal(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "loop": ("BOOLEAN", {"default": True}),
                "smooth": ("BOOLEAN", {"default": True}),
                "phase": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "steady_value": (
                    "FLOAT",
                    {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
            },
        }

    DESCRIPTION = """
    Depthflow Motion Preset Horizontal Node:
    This node allows the user to configure the horizontal motion preset.
    - intensity: Intensity of the horizontal motion
    - reverse: Reverse the horizontal motion
    - smooth: Smooth the horizontal motion
    - loop: Loop the horizontal motion
    - steady_value: Static value of the horizontal motion
    """

    @classmethod
    def get_modifiable_params(cls):
        return ["intensity", "phase", "steady_value", "None"]

    def create_internal(
        self, intensity, reverse, smooth, loop, phase, steady_value, **kwargs
    ):
        # Create the Horizontal preset object with the provided parameters
        preset = Animation.Horizontal(
            intensity=intensity,
            reverse=reverse,
            smooth=smooth,
            loop=loop,
            phase=phase,
            steady=steady_value,
            isometric=0.6,  # Default value from new API
        )
        return (preset,)


class DepthflowMotionPresetOrbital(DepthflowMotionPreset):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "depth": (
                    "FLOAT",
                    {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
            },
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
        preset = Animation.Orbital(
            intensity=intensity, 
            steady=depth,  # Changed from 'depth' to 'steady' in new API
            reverse=reverse,
            zoom=0.98,  # Default value from new API
        )
        return (preset,)
