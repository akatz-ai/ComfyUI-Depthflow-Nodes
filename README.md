# 🌊 Depthflow Node Pack for ComfyUI 🌊

**Turn your 2D images into stunning 2.5D parallax animations using Depthflow in ComfyUI.**

⚡ **Extends RyanOnTheInside's Flex System** for additional motion control and dynamic features!

## 🚀 Showcase

![](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3ExZHZ1NzN0MW1tbHMydHE1ZXJqeXFrcDQxYndvMGJ3d25yNzRibiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hsD6dpQuIeu9h7t8b1/giphy.webp)

*Example: Watch a static 2D image transform into a motion-filled scene with depth.*

---

## 📦 What's Included

This Depthflow Node Pack includes everything you need to create complex parallax animations. From basic motion presets to fine-tuned motion components, here's a breakdown of what you can expect:

### **1. Base Node: Depthflow**

The heart of the node pack. The **Depthflow** node takes a 2D image and its corresponding depth map and applies various types of motion animation (Zoom, Dolly, Circle, etc.) to generate a parallax effect. This node outputs a batch of images to be rendered as a video.

**Parameters:**
- `image`: Input image.
- `depth_map`: Depthmap corresponding to the image.
- `options`: DepthState object for customizable depth rendering.
- `motion`: Depthflow motion object for configuring animation.
- `input_fps`: Frames per second for the input.
- `output_fps`: Frames per second for the output video.
- `num_frames`: Number of frames in the animation.
- `quality`: Output quality.
- `ssaa`: Super sampling anti-aliasing samples.
- `invert`: Invert the depthmap.
- `tiling_mode`: Control for tiling the image.

![Depthflow Core Demo](./path/to/depthflow_core_demo.gif)

---

### **2. Depthflow Effects**

Enhance the parallax animation with customizable effects such as Depth of Field and Vignette. These effects can be configured to interact with the depth information for a more immersive experience.

#### **Depth of Field (DOF) Effect**

The **DOF** node lets you apply depth-aware blur to simulate focus and bokeh, giving your animations a cinematic feel.

**Parameters:**
- `strength`, `feature_threshold`, `feature_param`, `dof_start`, `dof_end`, etc., for controlling focus zones, intensity, and quality.

![DOF Effect Demo](./path/to/dof_effect_demo.gif)

---

### **3. Depthflow Motion**

Take control of your animations with pre-configured **motion presets** or dive deep with granular **motion components** to create exactly the movement you want.

#### **Motion Presets**
Simplify your workflow with ready-to-use presets for common animations. Nodes like **Zoom**, **Dolly**, and **Circle** abstract away complex parameters so you can focus on creative output.

- **Zoom Motion Preset**: Configure zoom intensity, direction, and looping behavior.
- **Circle Motion Preset**: Creates smooth circular motion around a point of focus.

**Example**:
- `intensity`, `reverse`, `smooth`, `loop`, etc.

![Zoom Motion Preset Demo](./path/to/zoom_motion_demo.gif)

#### **Motion Components**
If you want finer control, the **motion components** offer modular building blocks to animate individual parameters like height, zoom, and center of rotation. Mix and match different functions like Sine, Cosine, Linear, and more for highly customized motion paths.

- **Sine Motion Component**: Applies a sine wave modulation to any target parameter for smooth, oscillating motion.

**Parameters:**
- `target`: The parameter to modulate (Zoom, Height, Focus, etc.).
- `amplitude`, `cycles`, `phase`, and more for custom wave behavior.

![Sine Motion Component Demo](./path/to/sine_motion_demo.gif)

---

### **4. Dynamic Features**

For even more control, the motion nodes accept an optional **"feature"** input, which allows the animation to be influenced by external factors like audio or masks. This adds new layers of creativity and flexibility to your animations.

---

## 🎨 Extending RyanOnTheInside's Flex System

Depthflow is one of the first custom node packs to extend the **Flex System**, a versatile system developed by RyanOnTheInside. By building on Flex, Depthflow opens up a range of possibilities for dynamically adjusting motion parameters based on user-defined features like sound, colors, or masks. This integration pushes the boundaries of what's possible in ComfyUI animations.

---

## 🔧 Installation and Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/depthflow-nodepack.git
```
