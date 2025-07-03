from abc import ABC, abstractmethod

from comfy.utils import ProgressBar


class BaseFlex(ABC):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "strength": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01},
                ),
                "feature_threshold": (
                    "FLOAT",
                    {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "feature_param": (
                    cls.get_modifiable_params(),
                    {"default": cls.get_modifiable_params()[0]},
                ),
                "feature_mode": (["relative", "absolute"], {"default": "relative"}),
            },
            "optional": {"feature": ("FEATURE", {"default": None})},
        }

    CATEGORY = "🌊 Depthflow"
    FUNCTION = "apply"

    def __init__(self):
        self.progress_bar = None

    def start_progress(self, total_steps, desc="Processing"):
        self.progress_bar = ProgressBar(total_steps)

    def update_progress(self):
        if self.progress_bar:
            self.progress_bar.update(1)

    def end_progress(self):
        self.progress_bar = None

    @classmethod
    @abstractmethod
    def get_modifiable_params(cls):
        """Return a list of parameter names that can be modulated."""
        return []

    def modulate_param(self, param_name, param_value, feature_value, strength, mode):
        if mode == "relative":
            return param_value * (1 + (feature_value - 0.5) * strength)
        else:  # absolute
            return param_value * feature_value * strength

    def apply(
        self,
        strength,
        feature_threshold,
        feature_param,
        feature_mode,
        feature=None,
        **kwargs,
    ):
        # If feature is not provided, simply return a single preset
        if feature is None:
            return (
                self.create(
                    0.0, strength, feature_param, feature_mode, feature, **kwargs
                ),
            )

        num_frames = feature.frame_count

        self.start_progress(num_frames, desc=f"Applying {self.__class__.__name__}")

        result = []
        for i in range(num_frames):
            feature_value = feature.get_value_at_frame(i)
            kwargs["frame_index"] = i
            feature_value = feature_value if feature_value >= feature_threshold else 0.0
            processed_preset = self.create(
                feature_value, strength, feature_param, feature_mode, feature, **kwargs
            )

            result.append(processed_preset)
            self.update_progress()

        self.end_progress()

        return (result,)

    def create(
        self,
        feature_value: float,
        strength: float,
        feature_param: str,
        feature_mode: str,
        feature=None,
        **kwargs,
    ):
        # Modulate the selected parameter
        if feature is not None:
            for param_name in self.get_modifiable_params():
                if param_name in kwargs:
                    if param_name == feature_param:
                        kwargs[param_name] = self.modulate_param(
                            param_name,
                            kwargs[param_name],
                            feature_value,
                            strength,
                            feature_mode,
                        )

        motion = self.create_internal(**kwargs)[0]
        return motion

    @abstractmethod
    def create_internal(self, **kwargs):
        """Implemented by subclasses to create the object based on the provided parameters."""
        pass
