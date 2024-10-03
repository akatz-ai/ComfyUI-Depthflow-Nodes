from .depthflow_motion_base import DepthflowMotion, Target
from DepthFlow.Motion import Components, Preset

TARGETS = [target.name for target in Target]

class DepthflowMotionSine(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "amplitude": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "cycles": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                "phase": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "reverse": ("BOOLEAN", {"default": False}),
                "bias": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "cumulative": ("BOOLEAN", {"default": False}),
            },
        }

    DESCRIPTION = """
    Depthflow Motion Sine Node:
    This node applies a sine wave motion to a specified target parameter.
    - target: Parameter to apply the motion to.
    - amplitude: Amplitude of the sine wave.
    - cycles: Number of cycles over the duration.
    - phase: Phase shift of the sine wave.
    - reverse: Reverse the time direction.
    - bias: Constant offset added to the motion.
    - cumulative: Whether to add to the previous frame's value.
    """

    @classmethod
    def get_modifiable_params(cls):
        return ["amplitude", "phase", "cycles", "None"]

    def create_internal(self, target, amplitude, cycles, phase, reverse, bias, cumulative, **kwargs):
        # Create the Sine component
        animation = Components.Sine(
            target=Target[target].value,
            amplitude=amplitude,
            cycles=cycles,
            phase=phase,
            reverse=reverse,
            bias=bias,
            cumulative=cumulative,
        )
        # Create a Preset that yields this animation
        class SingleAnimationPreset(Preset):
            def animation(self):
                yield animation

        preset = SingleAnimationPreset()
        return (preset,)
      
class DepthflowMotionCosine(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "amplitude": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "cycles": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                "phase": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "reverse": ("BOOLEAN", {"default": False}),
                "bias": ("FLOAT", {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                "cumulative": ("BOOLEAN", {"default": False}),
            },
        }
        
    DESCRIPTION = """
    Depthflow Motion Cosine Node:
    This node applies a cosine wave motion to a specified target parameter.
    - target: Parameter to apply the motion to.
    - amplitude: Amplitude of the cosine wave.
    - cycles: Number of cycles over the duration.
    - phase: Phase shift of the cosine wave.
    - reverse: Reverse the time direction.
    - bias: Constant offset added to the motion.
    - cumulative: Whether to add to the previous frame's value.
    """

    @classmethod
    def get_modifiable_params(cls):
        return ["amplitude", "phase", "cycles", "None"]

    def create_internal(self, target, amplitude, cycles, phase, reverse, bias, cumulative, **kwargs):
        # Create the Cosine component
        animation = Components.Cosine(
            target=Target[target].value,
            amplitude=amplitude,
            cycles=cycles,
            phase=phase,
            reverse=reverse,
            bias=bias,
            cumulative=cumulative,
        )
        # Create a Preset that yields this animation
        class SingleAnimationPreset(Preset):
            def animation(self):
                yield animation

        preset = SingleAnimationPreset()
        return (preset,)
    
class DepthflowMotionLinear(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "start": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "end": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "low": ("FLOAT", {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.01}),
                "high": ("FLOAT", {"default": 1.0, "min": -9999.0, "max": 9999.0, "step": 0.01}),
                "exponent": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 0.01}),
                "reverse": ("BOOLEAN", {"default": False}),
                "cumulative": ("BOOLEAN", {"default": False}),
            },
        }
        
    DESCRIPTION = """
    Depthflow Motion Linear Node:
    This node applies a linear motion to a specified target parameter.
    - target: Parameter to apply the motion to.
    - start: Starting value of the linear motion.
    - end: Ending value of the linear motion.
    - low: Lower bound of the linear motion.
    - high: Upper bound of the linear motion.
    - exponent: Exponent of the linear motion.
    - reverse: Reverse the time direction.
    - cumulative: Whether to add to the previous frame's value.
    """

    @classmethod
    def get_modifiable_params(cls):
        return ["start", "end", "low", "high", "exponent", "None"]

    def create_internal(self, target, start, end, low, high, exponent, reverse, cumulative, **kwargs):
        # Create the Linear component
        animation = Components.Linear(
            target=Target[target].value,
            start=start,
            end=end,
            low=low,
            hight=high,
            exponent=exponent,
            reverse=reverse,
            cumulative=cumulative,
        )
        # Create a Preset that yields this animation
        class SingleAnimationPreset(Preset):
            def animation(self):
                yield animation

        preset = SingleAnimationPreset()
        return (preset,)
    
class DepthflowMotionExponential(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "base": ("FLOAT", {"default": 2.0, "step": 0.01}),
                "scale": ("FLOAT", {"default": 1.0, "step": 0.01}),
                "reverse": ("BOOLEAN", {"default": False}),
                "cumulative": ("BOOLEAN", {"default": False}),
            },
        }
        
    DESCRIPTION = """
    Depthflow Motion Exponential Node:
    This node applies an exponential motion to a specified target parameter.
    - target: Parameter to apply the motion to.
    - base: Base of the exponential motion.
    - scale: Scale of the exponential motion.
    - reverse: Reverse the time direction.
    - cumulative: Whether to add to the previous frame's value.
    """

    @classmethod
    def get_modifiable_params(cls):
        return ["base", "scale", "None"]

    def create_internal(self, target, base, scale, reverse, cumulative, **kwargs):
        # Create the Exponential component
        animation = Components.Exponential(
            target=Target[target].value,
            base=base,
            scale=scale,
            reverse=reverse,
            cumulative=cumulative,
        )
        # Create a Preset that yields this animation
        class SingleAnimationPreset(Preset):
            def animation(self):
                yield animation

        preset = SingleAnimationPreset()
        return (preset,)
    

class DepthflowMotionArc(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "start": ("FLOAT", {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.01}),
                "middle": ("FLOAT", {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.01}),
                "end": ("FLOAT", {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.01}),
                "reverse": ("BOOLEAN", {"default": False}),
                "cumulative": ("BOOLEAN", {"default": False}),
            },
        }
        
    DESCRIPTION = """
    Depthflow Motion Arc Node: 
    This node applies an arc motion to a specified target parameter.
    - target: Parameter to apply the motion to.
    - start: Starting value of the arc motion.
    - middle: Middle value of the arc motion.
    - end: Ending value of the arc motion.
    - reverse: Reverse the time direction.
    - cumulative: Whether to add to the previous frame's value.
    """

    @classmethod
    def get_modifiable_params(cls):
        return ["start", "middle", "end", "None"]

    def create_internal(self, target, start, middle, end, reverse, cumulative, **kwargs):
        # Create the Arc component
        animation = Components.Arc(
            target=Target[target].value,
            points=(start, middle, end),
            reverse=reverse,
            cumulative=cumulative,
        )
        # Create a Preset that yields this animation
        class SingleAnimationPreset(Preset):
            def animation(self):
                yield animation

        preset = SingleAnimationPreset()
        return (preset,)
    
    
class DepthflowMotionSetTarget(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "value": ("FLOAT", {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.001}),
            },
        }

    DESCRIPTION = """
    Depthflow Motion Set Target Node:
    This node sets a target parameter to a specified value.
    - target: Parameter to set (e.g., Height, OffsetX, OffsetY).
    - value: Value to set the parameter to.
    - reverse: Reverse the time direction (for compatibility).
    - bias: Constant offset added to the value.
    - cumulative: Whether to add to the previous frame's value.
    """

    @classmethod
    def get_modifiable_params(cls):
        return ["value", "None"]

    def create_internal(self, target, value, **kwargs):
        # Create the Set component
        animation = Components.Set(
            target=Target[target].value,
            value=value,
            reverse=False,
            bias=0.0,
            cumulative=False,
        )

        # Create a Preset that yields this animation
        class SingleAnimationPreset(Preset):
            def animation(self):
                yield animation

        preset = SingleAnimationPreset()
        return (preset,)