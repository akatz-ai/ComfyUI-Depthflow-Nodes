from abc import abstractmethod
from DepthFlow.Motion import Preset
from ..base_flex import BaseFlex
from Broken import BrokenEnum
from pydantic import Field
from typing import List

class Target(BrokenEnum):
    Nothing            = "nothing"
    Height             = "height"
    Static             = "static"
    Focus              = "focus"
    Zoom               = "zoom"
    Isometric          = "isometric"
    Dolly              = "dolly"
    CenterX            = "center_x"
    CenterY            = "center_y"
    OriginX            = "origin_x"
    OriginY            = "origin_y"
    OffsetX            = "offset_x"
    OffsetY            = "offset_y"
    
class CombinedPreset(Preset):
    presets: List[Preset] = Field(default_factory=list)

    def animation(self):
        for preset in self.presets:
            yield from preset.animation()


class DepthflowMotion(BaseFlex):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            **super().INPUT_TYPES(),
            "required": {
                **super().INPUT_TYPES()["required"],
            },
            "optional": {
                **super().INPUT_TYPES()["optional"],
                "motion": ("DEPTHFLOW_MOTION",)
            }
        }

    RETURN_TYPES = ("DEPTHFLOW_MOTION",)
    CATEGORY = "🌊 Depthflow/Motion/Components"

    @abstractmethod
    def create_internal(self, **kwargs):
        """
        Implemented by subclasses to create their specific motion preset.
        """
        pass

    def apply(self, strength, feature_threshold, feature_param, feature_mode, motion=None, feature=None, **kwargs):
        # Determine if motion is a list
        motion_is_list = isinstance(motion, list)
        # Determine if we have a feature to modulate over time
        has_feature = feature is not None

        if not motion_is_list and not has_feature:
            # Case 1: Both motion and feature are not lists
            # Create a single motion by combining motion with our motion
            new_motion = self.create(0.0, strength, feature_param, feature_mode, motion=motion, feature=None, **kwargs)
            return (new_motion,)
        elif motion_is_list and not has_feature:
            # Case 2: motion is a list, feature is None
            result = []
            self.start_progress(len(motion), desc=f"Applying {self.__class__.__name__}")
            for i, prev_motion in enumerate(motion):
                kwargs['frame_index'] = i
                new_motion = self.create(0.0, strength, feature_param, feature_mode, motion=prev_motion, feature=None, **kwargs)
                result.append(new_motion)
                self.update_progress()
            self.end_progress()
            return (result,)
        elif not motion_is_list and has_feature:
            # Case 3: motion is not a list, feature is provided
            num_frames = feature.frame_count
            self.start_progress(num_frames, desc=f"Applying {self.__class__.__name__}")
            result = []
            for i in range(num_frames):
                feature_value = feature.get_value_at_frame(i)
                kwargs['frame_index'] = i
                feature_value = feature_value if feature_value >= feature_threshold else 0.0
                new_motion = self.create(feature_value, strength, feature_param, feature_mode, motion=motion, feature=feature, **kwargs)
                result.append(new_motion)
                self.update_progress()
            self.end_progress()
            return (result,)
        elif motion_is_list and has_feature:
            # Case 4: Both motion is a list and feature is provided
            num_frames = feature.frame_count
            if num_frames != len(motion):
                raise ValueError("Number of frames in feature and motion list must be the same")
            self.start_progress(num_frames, desc=f"Applying {self.__class__.__name__}")
            result = []
            for i in range(num_frames):
                feature_value = feature.get_value_at_frame(i)
                kwargs['frame_index'] = i
                feature_value = feature_value if feature_value >= feature_threshold else 0.0
                new_motion = self.create(feature_value, strength, feature_param, feature_mode, motion=motion[i], feature=feature, **kwargs)
                result.append(new_motion)
                self.update_progress()
            self.end_progress()
            return (result,)

    def create(self, feature_value: float, strength: float, feature_param: str, feature_mode: str, motion=None, feature=None, **kwargs):
        # Modulate the selected parameter
        if feature is not None:
            for param_name in self.get_modifiable_params():
                if param_name in kwargs:
                    if param_name == feature_param:
                        kwargs[param_name] = self.modulate_param(param_name, kwargs[param_name],
                                                                 feature_value, strength, feature_mode)

        # Create current motion preset
        current_preset = self.create_internal(**kwargs)[0]

        # Combine with incoming motion
        if motion is None:
            combined_preset = current_preset
        elif isinstance(motion, Preset):
            combined_preset = CombinedPreset(presets=[motion, current_preset])
        elif isinstance(motion, CombinedPreset):
            combined_preset = CombinedPreset(presets=motion.presets + [current_preset])
        else:
            raise ValueError("'motion' should be a Preset or CombinedPreset")

        return combined_preset
