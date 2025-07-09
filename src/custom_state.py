from typing import Annotated, Iterable, Tuple

from pydantic import Field
from shaderflow.variable import ShaderVariable, Uniform
from typer import Option

from depthflow.state import InpaintState as BaseInpaintState

# ------------------------------------------------------------------------------------------------ #

class CustomInpaintState(BaseInpaintState):
    """Extended InpaintState with color support"""
    
    color_r: Annotated[float, Option("--color-r", min=0, max=1)] = Field(0.0)
    """Red component of the inpaint color"""
    
    color_g: Annotated[float, Option("--color-g", min=0, max=1)] = Field(1.0)
    """Green component of the inpaint color"""
    
    color_b: Annotated[float, Option("--color-b", min=0, max=1)] = Field(0.0)
    """Blue component of the inpaint color"""
    
    color_a: Annotated[float, Option("--color-a", min=0, max=1)] = Field(1.0)
    """Alpha component of the inpaint color"""

    def pipeline(self) -> Iterable[ShaderVariable]:
        # First yield all the base uniforms
        yield from super().pipeline()
        # Then add our color uniform
        yield Uniform("vec4", "iInpaintColor", (self.color_r, self.color_g, self.color_b, self.color_a))