import gc
from collections import deque
import copy
from pathlib import Path

import cv2
import numpy as np
import torch
from broken.core.extra.loaders import LoadImage
from comfy.utils import ProgressBar

from depthflow.scene import DepthScene
from depthflow.animation import DepthAnimation
from depthflow.state import DepthState

from .custom_state import CustomInpaintState

DEPTH_SHADER = Path(__file__).parent / "shaders" / "depthflow.glsl"


class CustomDepthflowScene(DepthScene):
    def __init__(
        self,
        state=None,
        effects=None,
        progress_callback=None,
        num_frames=30,
        input_fps=30.0,
        output_fps=30.0,
        animation_speed=1.0,
        **kwargs,
    ):
        DepthScene.__init__(self, **kwargs)
        self.frames = deque()
        self.progress_callback = progress_callback
        self.custom_animation_frames = deque()
        self._set_effects(effects)
        # Override state with keywords in state
        self.override_state = state
        self.time = 0.00001
        # Initialize images and depth_maps
        self.images = None
        self.depth_maps = None
        self.input_fps = input_fps
        self.output_fps = output_fps
        self.animation_speed = animation_speed
        self.num_frames = num_frames
        self.video_time = 0.0
        self.frame_index = 0
        # Initialize animation with empty DepthAnimation
        self.config.animation = DepthAnimation()
        self.state.inpaint = CustomInpaintState()
        
    def build(self):
        DepthScene.build(self)
        self.shader.fragment = DEPTH_SHADER

    def input(self, image, depth):
        # TODO: maybe put this somewhere else?
        # self.shader.fragment = DEPTH_SHADER
        # Store the images and depth maps
        self.images = image  # Should be numpy arrays of shape [num_frames, H, W, C]
        self.depth_maps = depth
        # For initial setup, use the first frame
        initial_image = image[0]
        initial_depth = depth[0]
        DepthScene.input(self, initial_image, initial_depth)
        
    def _load_inputs(self, echo: bool=True) -> None:
        """Load inputs: single or batch exporting"""

        # Batch exporting implementation
        image = self._get_batch_input(self.config.image)
        depth = self._get_batch_input(self.config.depth)

        if (image is None):
            self.log_info("DEBUG: image is None")
            return
            # raise super().ShaderBatchStop()

        # self.log_info(f"Loading image: {image}", echo=echo)
        # self.log_info(f"Loading depth: {depth or 'Estimating from image'}", echo=echo)

        # Load, estimate, upscale input image
        image = self.config.upscaler.upscale(LoadImage(image))
        depth = LoadImage(depth) or self.config.estimator.estimate(image)

        # Match rendering resolution to image
        self.resolution   = (image.width,image.height)
        self.aspect_ratio = (image.width/image.height)
        self.image.from_image(image)
        self.depth.from_image(depth)

    def _set_effects(self, effects):
        if effects is None:
            self.effects = None
            return
        # If effects is a list or deque, convert it to a deque
        if isinstance(effects, (list, deque)):
            self.effects = deque(effects)
        else:
            self.effects = effects

    def custom_animation(self, motion):
        # check if motion is a list, otherwise add it directly with config.animation.add
        if isinstance(motion, list):
            for m in motion:
                self.custom_animation_frames.append(m)
        elif hasattr(motion, 'presets'):  # CombinedPreset
            for preset in motion.presets:
                self.config.animation.add(preset)
        else:
            self.config.animation.add(motion)

    def update(self):
        frame_duration = 1.0 / self.input_fps

        while self.time > self.video_time:
            self.video_time += frame_duration
            self.frame_index += 1

        # Set the current image and depth map based on self.frame
        if self.images is not None and self.depth_maps is not None:
            frame_index = min(self.frame_index, len(self.images) - 1)
            current_image = self.images[frame_index]
            current_depth = self.depth_maps[frame_index]

            # Convert to appropriate format if necessary
            image = LoadImage(current_image) #self.upscayl(LoadImage(current_image))
            depth = LoadImage(current_depth)

            # Set the current image and depth map
            self.image.from_image(image)
            self.depth.from_image(depth)

        # If there are custom animation frames present, use them instead of the normal animation frames
        if self.custom_animation_frames:
            # Clear current animation and add the new frame
            self.config.animation.clear()
            frame = self.custom_animation_frames.popleft()
            if hasattr(frame, 'presets'):  # CombinedPreset
                for preset in frame.presets:
                    self.config.animation.add(preset)
            else:
                self.config.animation.add(frame)

        DepthScene.update(self)

        def set_effects_helper(effects):
            # Map old effect keys to new state structure
            effect_mapping = {
                # Vignette
                'vignette_enable': ('vignette', 'enable'),
                'vignette_intensity': ('vignette', 'intensity'),
                'vignette_decay': ('vignette', 'decay'),
                # DOF (Blur)
                'dof_enable': ('blur', 'enable'),
                'dof_start': ('blur', 'start'),
                'dof_end': ('blur', 'end'),
                'dof_exponent': ('blur', 'exponent'),
                'dof_intensity': ('blur', 'intensity'),
                'dof_quality': ('blur', 'quality'),
                'dof_directions': ('blur', 'directions'),
                # Inpaint
                'inpaint_enable': ('inpaint', 'enable'),
                'inpaint_black': ('inpaint', 'black'),
                'inpaint_limit': ('inpaint', 'limit'),
                'inpaint_color_r': ('inpaint', 'color_r'),
                'inpaint_color_g': ('inpaint', 'color_g'),
                'inpaint_color_b': ('inpaint', 'color_b'),
                'inpaint_color_a': ('inpaint', 'color_a'),
                # Colors
                'color_enable': ('colors', 'enable'),
                'color_saturation': ('colors', 'saturation'),
                'color_contrast': ('colors', 'contrast'),
                'color_brightness': ('colors', 'brightness'),
                'color_gamma': ('colors', 'gamma'),
                'color_grayscale': ('colors', 'grayscale'),
                'color_sepia': ('colors', 'sepia'),
            }
            
            for key, value in effects.items():
                if key in effect_mapping:
                    state_obj, attr = effect_mapping[key]
                    if hasattr(self.state, state_obj):
                        setattr(getattr(self.state, state_obj), attr, value)
                elif hasattr(self.state, key):
                    setattr(self.state, key, value)

        if self.effects:
            if isinstance(self.effects, deque):
                set_effects_helper(self.effects.popleft())
            else:
                set_effects_helper(self.effects)

        if self.override_state:
            for key, value in self.override_state.items():
                if hasattr(self.state, key):
                    setattr(self.state, key, value)

            if "tiling_mode" in self.override_state:
                if self.override_state["tiling_mode"] == "repeat":
                    self.image.repeat(True)
                    self.depth.repeat(True)
                    self.state.mirror = False
                elif self.override_state["tiling_mode"] == "mirror":
                    self.image.repeat(False)
                    self.depth.repeat(False)
                    self.state.mirror = True
                else:
                    self.image.repeat(False)
                    self.depth.repeat(False)
                    self.state.mirror = False

    @property
    def tau(self) -> float:
        return super().tau * self.animation_speed

    def next(self, dt):
        DepthScene.next(self, dt)
        tensor = torch.from_numpy(self.screenshot().copy())

        # Accumulate the frame
        self.frames.append(tensor)

        if self.progress_callback:
            self.progress_callback()

        return self

    def get_accumulated_frames(self):
        # Convert the deque of frames to a tensor
        return torch.stack(list(self.frames))

    def clear_frames(self):
        self.frames.clear()
        gc.collect()


class Depthflow:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # Input image
                "depth_map": ("IMAGE",),  # Depthmap input
                "motion": ("DEPTHFLOW_MOTION",),  # Motion object
                "animation_speed": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.01, "step": 0.01},
                ),
                "input_fps": ("FLOAT", {"default": 30.0, "min": 1.0, "step": 1.0}),
                "output_fps": ("FLOAT", {"default": 30.0, "min": 1.0, "step": 1.0}),
                "num_frames": ("INT", {"default": 30, "min": 1, "step": 1}),
                "quality": ("INT", {"default": 50, "min": 1, "max": 100, "step": 1}),
                "ssaa": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.0, "max": 4.0, "step": 0.1},
                ),
                "invert": (
                    "FLOAT",
                    {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
                "tiling_mode": (["mirror", "repeat", "none"], {"default": "mirror"}),
                "edge_fix": ("INT", {"default": 5, "min": 0, "max": 50, "step": 1}),
            },
            "optional": {
                "effects": ("DEPTHFLOW_EFFECTS",),  # DepthState object
            },
        }

    RETURN_TYPES = (
        "IMAGE",
    )  # Output is a batch of images (torch.Tensor with shape [B,H,W,C])
    FUNCTION = "apply_depthflow"
    CATEGORY = "🌊 Depthflow"
    DESCRIPTION = """
    Depthflow Node:
    This node applies a motion animation (Zoom, Dolly, Circle, Horizontal, Vertical) to an image
    using a depthmap and outputs an image batch as a tensor.
    - image: The input image.
    - depth_map: Depthmap corresponding to the image.
    - options: DepthState object.
    - motion: Depthflow motion object.
    - input_fps: Frames per second for the input video.
    - output_fps: Frames per second for the output video.
    - num_frames: Number of frames for the output video.
    - quality: Quality of the output video.
    - ssaa: Super sampling anti-aliasing samples.
    - invert: Invert the depthmap.
    - tiling_mode: Tiling mode for the image.
    """

    def __init__(self):
        self.progress_bar = None

    def start_progress(self, total_steps, desc="Processing"):
        self.progress_bar = ProgressBar(total_steps)

    def update_progress(self):
        if self.progress_bar:
            self.progress_bar.update(1)

    def end_progress(self):
        self.progress_bar = None

    def apply_depthflow(
        self,
        image,
        depth_map,
        motion,
        animation_speed,
        input_fps,
        output_fps,
        num_frames,
        quality,
        ssaa,
        invert,
        tiling_mode,
        edge_fix,
        effects=None,
    ):
        # Create the scene
        state = {"invert": invert, "tiling_mode": tiling_mode}
        scene = CustomDepthflowScene(
            state=state,
            effects=effects,
            progress_callback=self.update_progress,
            num_frames=num_frames,
            input_fps=input_fps,
            output_fps=output_fps,
            animation_speed=animation_speed,
            backend="headless",
        )

        # Fix: Disable upscaler to prevent incorrect resolution doubling
        # The pypi depthflow package incorrectly defaults upscaler.scale to 2
        scene.config.upscaler.scale = 1

        # Convert image and depthmap to numpy arrays
        if image.is_cuda:
            image = image.cpu().numpy()
        else:
            image = image.numpy()
        if depth_map.is_cuda:
            depth_map = depth_map.cpu().numpy()
        else:
            depth_map = depth_map.numpy()

        # Ensure the arrays have the correct shape and data type
        if image.ndim == 3:
            image = np.expand_dims(image, axis=0)
        elif image.ndim != 4:
            raise ValueError(f"Unsupported image shape: {image.shape}")

        if depth_map.ndim == 3:
            depth_map = np.expand_dims(depth_map, axis=0)
        elif depth_map.ndim != 4:
            raise ValueError(f"Unsupported depth_map shape: {depth_map.shape}")

        if image.dtype != np.uint8:
            image = (image * 255).astype(np.uint8)
        if depth_map.dtype != np.uint8:
            depth_map = (depth_map * 255).astype(np.uint8)

        # Apply edge fix (dilation) to depth maps if edge_fix > 0
        if edge_fix > 0:
            # Create circular kernel for dilation
            kernel_size = edge_fix * 2 + 1
            kernel = np.zeros((kernel_size, kernel_size), np.uint8)
            kernel = cv2.circle(kernel, (edge_fix, edge_fix), edge_fix, 1, -1)
            
            # Apply dilation to each depth map frame
            dilated_depth_maps = []
            for i in range(depth_map.shape[0]):
                # Get the current depth map frame
                current_depth = depth_map[i]
                
                # If depth map has multiple channels, process each channel
                if current_depth.shape[2] > 1:
                    channels = []
                    for c in range(current_depth.shape[2]):
                        dilated_channel = cv2.dilate(current_depth[:, :, c], kernel, iterations=1)
                        channels.append(dilated_channel)
                    dilated_frame = np.stack(channels, axis=2)
                else:
                    # Single channel depth map
                    dilated_frame = cv2.dilate(current_depth[:, :, 0], kernel, iterations=1)
                    dilated_frame = np.expand_dims(dilated_frame, axis=2)
                
                dilated_depth_maps.append(dilated_frame)
            
            # Convert back to numpy array
            depth_map = np.array(dilated_depth_maps)

        # Determine the number of frames
        num_image_frames = image.shape[0]
        num_depth_frames = depth_map.shape[0]
        num_render_frames = max(num_frames, num_image_frames, num_depth_frames)

        # Expand images and depth maps to match num_render_frames
        def expand_frames(array, num_frames):
            if array.shape[0] == num_frames:
                return array
            elif array.shape[0] == 1:
                return np.broadcast_to(array, (num_frames,) + array.shape[1:])
            else:
                raise ValueError(
                    f"Cannot expand array with shape {array.shape} to {num_frames} frames"
                )

        image = expand_frames(image, num_render_frames)
        depth_map = expand_frames(depth_map, num_render_frames)

        # Get width and height of images
        height, width = image.shape[1], image.shape[2]

        # Validate image dimensions against OpenGL texture limits
        # Most OpenGL contexts have a maximum texture size of 16384
        MAX_TEXTURE_SIZE = 16384
        if width > MAX_TEXTURE_SIZE or height > MAX_TEXTURE_SIZE:
            raise ValueError(
                f"Image dimensions ({width}x{height}) exceed OpenGL maximum texture size ({MAX_TEXTURE_SIZE}). "
                f"Please resize your input image to be at most {MAX_TEXTURE_SIZE}x{MAX_TEXTURE_SIZE} pixels."
            )

        # Input the image and depthmap into the scene
        # Store the image and depth sequences in the scene for frame-by-frame processing
        print(f"DEBUG: depth_map shape: {depth_map.shape}, dtype: {depth_map.dtype}")
        print(f"DEBUG: image shape: {image.shape}, dtype: {image.dtype}")
        
        # Store the arrays in the scene for update() to use
        # scene.images = image
        # scene.depth_maps = depth_map
        
        # Don't call scene.input or set config.image/depth directly
        # The scene's update() method will handle loading frames dynamically
        # This avoids the boolean evaluation issue in depthflow's _load_inputs
        scene.input(image, depth=depth_map)
        
        # Instead, we'll set up the scene resolution based on the input
        # scene.resolution = (width, height)
        # scene.aspect_ratio = width / height

        scene.custom_animation(motion)

        # Calculate the duration based on fps and num_frames
        if num_frames <= 0:
            raise ValueError("FPS and number of frames must be greater than 0")
        duration = float(num_frames) / input_fps
        total_frames = duration * output_fps

        self.start_progress(total_frames, desc="Depthflow Rendering")

        # Render the output video
        scene.main(
            render=False,
            output=None,
            fps=output_fps,
            time=duration,
            speed=1.0,
            quality=quality,
            ssaa=ssaa,
            scale=1.0,
            width=width,
            height=height,
            ratio=None,
            freewheel=True,
        )

        video = scene.get_accumulated_frames()
        scene.clear_frames()
        self.end_progress()

        # Normalize the video frames to [0, 1]
        video = video.float() / 255.0

        return (video,)
