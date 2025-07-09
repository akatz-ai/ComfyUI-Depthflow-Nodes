def parse_color_string(color_str):
    """
    Parse a color string in various formats and return RGBA values (0-1 range).
    
    Supported formats:
    - HEX: #RGB, #RGBA, #RRGGBB, #RRGGBBAA
    - RGB: "r,g,b" or "r,g,b,a" where values are 0-255
    
    Returns tuple (r, g, b, a) with values in 0-1 range
    """
    if not isinstance(color_str, str):
        raise ValueError("Color must be a string")
    
    color_str = color_str.strip()
    
    # Handle HEX format
    if color_str.startswith('#'):
        hex_str = color_str[1:]
        
        # Validate hex characters
        if not all(c in '0123456789ABCDEFabcdef' for c in hex_str):
            raise ValueError(f"Invalid hex color: {color_str}")
        
        # Handle different hex formats
        if len(hex_str) == 3:  # #RGB
            r = int(hex_str[0] * 2, 16) / 255.0
            g = int(hex_str[1] * 2, 16) / 255.0
            b = int(hex_str[2] * 2, 16) / 255.0
            a = 1.0
        elif len(hex_str) == 4:  # #RGBA
            r = int(hex_str[0] * 2, 16) / 255.0
            g = int(hex_str[1] * 2, 16) / 255.0
            b = int(hex_str[2] * 2, 16) / 255.0
            a = int(hex_str[3] * 2, 16) / 255.0
        elif len(hex_str) == 6:  # #RRGGBB
            r = int(hex_str[0:2], 16) / 255.0
            g = int(hex_str[2:4], 16) / 255.0
            b = int(hex_str[4:6], 16) / 255.0
            a = 1.0
        elif len(hex_str) == 8:  # #RRGGBBAA
            r = int(hex_str[0:2], 16) / 255.0
            g = int(hex_str[2:4], 16) / 255.0
            b = int(hex_str[4:6], 16) / 255.0
            a = int(hex_str[6:8], 16) / 255.0
        else:
            raise ValueError(f"Invalid hex color length: {color_str}")
    
    # Handle RGB/RGBA comma-separated format
    elif ',' in color_str:
        parts = [p.strip() for p in color_str.split(',')]
        
        if len(parts) not in (3, 4):
            raise ValueError(f"RGB format must have 3 or 4 values: {color_str}")
        
        try:
            values = [float(p) for p in parts]
        except ValueError:
            raise ValueError(f"Invalid RGB values: {color_str}")
        
        # Validate range
        for v in values:
            if v < 0 or v > 255:
                raise ValueError(f"RGB values must be between 0-255: {color_str}")
        
        r = values[0] / 255.0
        g = values[1] / 255.0
        b = values[2] / 255.0
        a = values[3] / 255.0 if len(values) == 4 else 1.0
    
    else:
        raise ValueError(f"Unsupported color format: {color_str}")
    
    return (r, g, b, a)