from pydantic import Field
from depthflow.animation import Animation, ComponentBase

from .depthflow_motion_base import DepthflowMotion, Target

TARGETS = [target.name for target in Target]


class DepthflowMotionSine(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "amplitude": (
                    "FLOAT",
                    {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "cycles": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01},
                ),
                "phase": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "reverse": ("BOOLEAN", {"default": False}),
                "bias": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
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

    def create_internal(
        self, target, amplitude, cycles, phase, reverse, bias, cumulative, **kwargs
    ):
        # Create the Sine component
        return (
            Animation.Sine(
                target=Target[target].value,
                amplitude=amplitude,
                cycles=cycles,
                phase=phase,
                reverse=reverse,
                bias=bias,
            ),
        )


class DepthflowMotionCosine(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "amplitude": (
                    "FLOAT",
                    {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "cycles": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01},
                ),
                "phase": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "reverse": ("BOOLEAN", {"default": False}),
                "bias": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
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

    def create_internal(
        self, target, amplitude, cycles, phase, reverse, bias, cumulative, **kwargs
    ):
        # Create the Cosine component
        return (
            Animation.Cosine(
                target=Target[target].value,
                amplitude=amplitude,
                cycles=cycles,
                phase=phase,
                reverse=reverse,
                bias=bias,
            ),
        )


class DepthflowMotionLinear(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "start": (
                    "FLOAT",
                    {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "end": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "low": (
                    "FLOAT",
                    {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.01},
                ),
                "high": (
                    "FLOAT",
                    {"default": 1.0, "min": -9999.0, "max": 9999.0, "step": 0.01},
                ),
                "exponent": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 9999.0, "step": 0.01},
                ),
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

    def create_internal(
        self, target, start, end, low, high, exponent, reverse, cumulative, **kwargs
    ):
        # Create the Linear component
        return (
            Animation.Linear(
                target=Target[target].value,
                start=start,
                end=end,
                low=low,
                hight=high,
                exponent=exponent,
                reverse=reverse,
            ),
        )


class DepthflowMotionTriangle(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "amplitude": (
                    "FLOAT",
                    {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "cycles": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01},
                ),
                "phase": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "reverse": ("BOOLEAN", {"default": False}),
                "bias": (
                    "FLOAT",
                    {"default": 0.0, "min": -10.0, "max": 10.0, "step": 0.01},
                ),
                "cumulative": ("BOOLEAN", {"default": False}),
            },
        }

    DESCRIPTION = """
    Depthflow Motion Triangle Node:
    This node applies a triangle wave motion to a specified target parameter.
    - target: Parameter to apply the motion to.
    - amplitude: Amplitude of the triangle wave.
    - cycles: Number of cycles over the duration.
    - phase: Phase shift of the triangle wave.
    - reverse: Reverse the time direction.
    - bias: Constant offset added to the motion.
    - cumulative: Whether to add to the previous frame's value.
    """

    @classmethod
    def get_modifiable_params(cls):
        return ["amplitude", "phase", "cycles", "None"]

    def create_internal(
        self, target, amplitude, cycles, phase, reverse, bias, cumulative, **kwargs
    ):
        # Create the Triangle component
        return (
            Animation.Triangle(
                target=Target[target].value,
                amplitude=amplitude,
                cycles=cycles,
                phase=phase,
                reverse=reverse,
                bias=bias,
            ),
        )



class DepthflowMotionSetTarget(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "value": (
                    "FLOAT",
                    {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.001},
                ),
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
        return (
            Animation.Set(
                target=Target[target].value,
                value=value,
            ),
        )


class DepthflowMotionArc(DepthflowMotion):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
                "target": (TARGETS, {"default": TARGETS[0]}),
                "start": (
                    "FLOAT",
                    {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.01},
                ),
                "middle": (
                    "FLOAT",
                    {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.01},
                ),
                "end": (
                    "FLOAT",
                    {"default": 0.0, "min": -9999.0, "max": 9999.0, "step": 0.01},
                ),
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

    def create_internal(
        self, target, start, middle, end, reverse, cumulative, **kwargs
    ):
        # Create a custom Arc animation component
        class Arc(ComponentBase):
            start_val: float = Field(default=0.0)
            middle_val: float = Field(default=0.0)
            end_val: float = Field(default=0.0)
            reverse: bool = Field(default=False)
            
            def compute(self, scene, tau, cycle):
                # Note: tau and cycle are already processed by get_time() in the base class
                # when apply() calls compute(), so reverse is already handled
                
                # Use quadratic Bézier curve for smooth arc motion
                # To make the curve pass through all 3 points, we need to calculate the control point
                # For a quadratic Bézier to pass through (0,start), (0.5,middle), (1,end):
                # The control point P1 = 2*middle - 0.5*(start + end)
                control_point = 2.0 * self.middle_val - 0.5 * (self.start_val + self.end_val)
                
                # Quadratic Bézier formula: B(t) = (1-t)²*P0 + 2*(1-t)*t*P1 + t²*P2
                # where P0 = start, P1 = control_point, P2 = end
                t = tau
                one_minus_t = 1.0 - t
                
                return (one_minus_t * one_minus_t * self.start_val + 
                        2.0 * one_minus_t * t * control_point + 
                        t * t * self.end_val)
        
        arc_component = Arc(
            target=Target[target].value,
            start_val=start,
            middle_val=middle,
            end_val=end,
            reverse=reverse,
            cumulative=cumulative
        )
        
        return (arc_component,)
