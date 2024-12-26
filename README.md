# 🌊 Depthflow Node Pack for ComfyUI 🌊

**Turn your 2D images into stunning 2.5D parallax animations using Depthflow in ComfyUI. An open source Immersity alternative.**

🙌 **An implementation of the Depthflow library in ComfyUI originally created by [Tremeschin](https://github.com/Tremeschin)!** 
- Check out the [Depthflow github page](https://github.com/BrokenSource/DepthFlow)!
- Also see his [Awesome Website](https://brokensrc.dev/depthflow/) for more info!

⚡ **Extends [RyanOnTheInside's Flex System](https://github.com/ryanontheinside/ComfyUI_RyanOnTheInside)** for additional motion control and dynamic features!

## 🚀 Showcase

<div style="display: inline-block;">
    <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3ExZHZ1NzN0MW1tbHMydHE1ZXJqeXFrcDQxYndvMGJ3d25yNzRibiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hsD6dpQuIeu9h7t8b1/giphy.webp" alt="Description" width="250"/>
    <img src="https://media3.giphy.com/media/EFPKZv80znaW1xHh1M/giphy.webp" alt="Description" width="250"/>
    <img src="https://media0.giphy.com/media/JO0JR2MbaBprvzg41M/giphy.gif" alt="Description" width="250"/>
</div>

## 🖥️ Custom Environment
I created a custom ComfyUI environment for testing out Depthflow nodes:

**akatzai/comfy-env-depthflow:latest**

Create a new environment and copy and paste the link above into the "Custom Image" field in my Environment Manager tool:
https://github.com/akatz-ai/ComfyUI-Environment-Manager

Make sure to select the **Basic** environment type to access the included workflow!

## 📦 What's Included

(For a full breakdown of all nodes and their parameters, [check out the Depthflow Nodes Docs](https://cyber-damselfly-b6c.notion.site/Depthflow-Nodes-11dfd5b1ca3b8007ae9dc0bd0c65690a))

This Depthflow Node Pack includes everything you need to create complex parallax animations. From basic motion presets to fine-tuned motion components, here's a breakdown of what you can expect:

### **1. Base Node: Depthflow**

<img src="https://i.imgur.com/GmemdKs.png" alt="Description" width="400"/>

The heart of the node pack. The **Depthflow** node takes an image (or video) and its corresponding depth map and applies various types of motion animation (Zoom, Dolly, Circle, etc.) to generate a parallax effect. This node outputs a batch of images to be rendered as a video.

**Parameters:**
- `image`: Input image or image batch.
- `depth_map`: Depthmap image or image batch corresponding to the input image.
- `motion`: Depthflow motion object(s) for configuring animation.
- `effects`: (Optional) Depthflow Effects including DOF and Vignette that can be stacked.
- `num_frames`: Number of frames in the animation.
- `input_fps`: Frames per second for the input.
- `output_fps`: Frames per second for the output video.
- `quality`: Output quality (1-100)
- `ssaa`: Super sampling anti-aliasing samples (0.0-2.0)
- `invert`: Invert the depthmap.
- `tiling_mode`: Control for tiling the image.

![Depthflow Core Demo](./path/to/depthflow_core_demo.gif)

---

### **2. Depthflow Effects**

<img src="https://i.imgur.com/SGPWerb.png" alt="Description" width="800"/>

Enhance the parallax animation with customizable effects such as Depth of Field and Vignette. These effects can be configured to interact with the depth information for a more immersive experience.

- **DOF Effect**: A depth-aware blur effect to simulate focus and bokeh, giving your animations a cinematic feel.
- **Vignette Effect**: A vignette effect that darkens the edges of the frame.

**Examples:**

![](https://media1.giphy.com/media/nBiAFUBE4BSm87CcQm/giphy.webp)

*(Depth of Field effect modulated over time by a feature to more clearly demonstrate the effect)*

---

### **3. Depthflow Motion**

Take control of your animations with pre-configured **motion presets** or dive deep with granular **motion components** to create exactly the movement you want.

#### **Motion Presets**

![](https://i.imgur.com/8BamKev.png)

Simplify your workflow with ready-to-use presets for common animations. Nodes like **Zoom**, **Dolly**, and **Circle** abstract away complex parameters so you can focus on creative output.

- **Orbital Motion Preset**: Creates an orbital motion around a focal point, giving a 3D rotational effect.
- **Dolly Motion Preset**: Simulates a dolly camera motion, moving toward or away from the subject for a dynamic depth effect.
- **Circle Motion Preset**: Creates smooth circular motion around a point of focus, simulating rotational camera movement.
- **Vertical Motion Preset**: Applies vertical panning motion to the scene, moving the view up or down.
- **Horizontal Motion Preset**: Moves the scene horizontally, simulating a side-to-side panning motion.
- **Zoom Motion Preset**: Configure zoom intensity, direction (inward or outward), and looping behavior for dramatic zoom effects.

**Examples**:

![](https://media2.giphy.com/media/C69HgFr9C2b2pdlYF9/giphy.webp)
<img src="https://media2.giphy.com/media/h5Lh02liQQlXe2FcAl/giphy.webp" alt="Description" width="238"/>

#### **Motion Components**

![](https://i.imgur.com/6JBOVfa.png)

If you want finer control, the **motion components** offer modular building blocks to animate individual parameters like height, zoom, and center of rotation. Mix and match different functions like Sine, Cosine, Linear, and more for highly customized motion paths.

- **Linear Motion Component**: Applies a linear motion to the specified target, creating a steady and consistent movement.
- **Exponential Motion Component**: Generates motion with an exponential curve, starting slow and accelerating over time.
- **Sine Motion Component**: Applies a sine wave modulation to any target parameter, creating a smooth, oscillating motion.
- **Cosine Motion Component**: Similar to the sine component, but starts at a different phase, useful for wave-like motion with a different timing.
- **Arc Motion Component**: Moves the target parameter along a smooth arc, perfect for rotational or sweeping motion.
- **Set Target Motion Component**: Explicitly sets the value of a specified target parameter, overriding other motion inputs.

See the official [Depthflow Parameters page](https://brokensrc.dev/depthflow/learn/parameters/) to see how each target parameter affects the output.

## 🎨 Extending RyanOnTheInside's Flex System

Depthflow is one of the first custom node packs to extend the **Flex System**, a versatile system developed by [RyanOnTheInside](https://github.com/ryanontheinside). By building on Flex, Depthflow opens up a range of possibilities for dynamically adjusting motion parameters based on user-defined features like sound, colors, or masks. Check out [RyanOnTheInside's Github Page](https://github.com/ryanontheinside/ComfyUI_RyanOnTheInside) for more details on how to set up and use the Flex system.

## 🔧 Installation and Usage

1. ComfyUI Manager:

- This node pack is available to install via the [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager). You can find it in the Custom Nodes section by searching for "Depthflow" and clicking on the entry called "🌊 Depthflow Nodes".

2. Clone the repository:
- Navigate to ComfyUI/custom_nodes folder in terminal or command prompt.
- Clone the repo using the following command:
```bash
git clone https://github.com/akatz-ai/ComfyUI-Depthflow-Nodes.git
```
- Restart ComfyUI
