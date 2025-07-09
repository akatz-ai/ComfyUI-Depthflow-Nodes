import unittest
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.color_utils import parse_color_string


class TestColorUtils(unittest.TestCase):
    
    def test_hex_color_formats(self):
        """Test various HEX color formats."""
        # Test #RGB format
        r, g, b, a = parse_color_string("#F00")
        self.assertAlmostEqual(r, 1.0, places=2)
        self.assertAlmostEqual(g, 0.0, places=2)
        self.assertAlmostEqual(b, 0.0, places=2)
        self.assertAlmostEqual(a, 1.0, places=2)
        
        # Test #RGBA format
        r, g, b, a = parse_color_string("#0F08")
        self.assertAlmostEqual(r, 0.0, places=2)
        self.assertAlmostEqual(g, 1.0, places=2)
        self.assertAlmostEqual(b, 0.0, places=2)
        self.assertAlmostEqual(a, 0.533, places=2)  # 8/15 ≈ 0.533
        
        # Test #RRGGBB format
        r, g, b, a = parse_color_string("#FF0000")
        self.assertAlmostEqual(r, 1.0, places=2)
        self.assertAlmostEqual(g, 0.0, places=2)
        self.assertAlmostEqual(b, 0.0, places=2)
        self.assertAlmostEqual(a, 1.0, places=2)
        
        # Test #RRGGBBAA format
        r, g, b, a = parse_color_string("#00FF00FF")
        self.assertAlmostEqual(r, 0.0, places=2)
        self.assertAlmostEqual(g, 1.0, places=2)
        self.assertAlmostEqual(b, 0.0, places=2)
        self.assertAlmostEqual(a, 1.0, places=2)
        
        # Test with lowercase hex
        r, g, b, a = parse_color_string("#00ff00")
        self.assertAlmostEqual(r, 0.0, places=2)
        self.assertAlmostEqual(g, 1.0, places=2)
        self.assertAlmostEqual(b, 0.0, places=2)
        self.assertAlmostEqual(a, 1.0, places=2)
    
    def test_rgb_color_formats(self):
        """Test RGB comma-separated formats."""
        # Test RGB format
        r, g, b, a = parse_color_string("255,0,0")
        self.assertAlmostEqual(r, 1.0, places=2)
        self.assertAlmostEqual(g, 0.0, places=2)
        self.assertAlmostEqual(b, 0.0, places=2)
        self.assertAlmostEqual(a, 1.0, places=2)
        
        # Test RGBA format
        r, g, b, a = parse_color_string("0,255,0,128")
        self.assertAlmostEqual(r, 0.0, places=2)
        self.assertAlmostEqual(g, 1.0, places=2)
        self.assertAlmostEqual(b, 0.0, places=2)
        self.assertAlmostEqual(a, 0.502, places=2)  # 128/255 ≈ 0.502
        
        # Test with spaces
        r, g, b, a = parse_color_string("255, 128, 64")
        self.assertAlmostEqual(r, 1.0, places=2)
        self.assertAlmostEqual(g, 0.502, places=2)
        self.assertAlmostEqual(b, 0.251, places=2)
        self.assertAlmostEqual(a, 1.0, places=2)
    
    def test_edge_cases(self):
        """Test edge cases and boundary values."""
        # Test black
        r, g, b, a = parse_color_string("#000000")
        self.assertAlmostEqual(r, 0.0, places=2)
        self.assertAlmostEqual(g, 0.0, places=2)
        self.assertAlmostEqual(b, 0.0, places=2)
        self.assertAlmostEqual(a, 1.0, places=2)
        
        # Test white
        r, g, b, a = parse_color_string("255,255,255")
        self.assertAlmostEqual(r, 1.0, places=2)
        self.assertAlmostEqual(g, 1.0, places=2)
        self.assertAlmostEqual(b, 1.0, places=2)
        self.assertAlmostEqual(a, 1.0, places=2)
        
        # Test transparent
        r, g, b, a = parse_color_string("#00000000")
        self.assertAlmostEqual(r, 0.0, places=2)
        self.assertAlmostEqual(g, 0.0, places=2)
        self.assertAlmostEqual(b, 0.0, places=2)
        self.assertAlmostEqual(a, 0.0, places=2)
    
    def test_invalid_color_strings(self):
        """Test that invalid color strings raise appropriate errors."""
        # Test invalid hex characters
        with self.assertRaises(ValueError) as cm:
            parse_color_string("#GGGGGG")
        self.assertIn("Invalid hex color", str(cm.exception))
        
        # Test invalid hex length
        with self.assertRaises(ValueError) as cm:
            parse_color_string("#FF")
        self.assertIn("Invalid hex color length", str(cm.exception))
        
        # Test invalid RGB values (out of range)
        with self.assertRaises(ValueError) as cm:
            parse_color_string("256,0,0")
        self.assertIn("RGB values must be between 0-255", str(cm.exception))
        
        # Test invalid RGB values (negative)
        with self.assertRaises(ValueError) as cm:
            parse_color_string("-1,0,0")
        self.assertIn("RGB values must be between 0-255", str(cm.exception))
        
        # Test invalid RGB format (too few values)
        with self.assertRaises(ValueError) as cm:
            parse_color_string("255,0")
        self.assertIn("RGB format must have 3 or 4 values", str(cm.exception))
        
        # Test invalid RGB format (too many values)
        with self.assertRaises(ValueError) as cm:
            parse_color_string("255,0,0,128,255")
        self.assertIn("RGB format must have 3 or 4 values", str(cm.exception))
        
        # Test non-numeric RGB values
        with self.assertRaises(ValueError) as cm:
            parse_color_string("red,green,blue")
        self.assertIn("Invalid RGB values", str(cm.exception))
        
        # Test unsupported format
        with self.assertRaises(ValueError) as cm:
            parse_color_string("rgb(255,0,0)")
        self.assertIn("Unsupported color format", str(cm.exception))
        
        # Test non-string input
        with self.assertRaises(ValueError) as cm:
            parse_color_string(12345)
        self.assertIn("Color must be a string", str(cm.exception))
    
    def test_whitespace_handling(self):
        """Test that whitespace is properly handled."""
        # Test with leading/trailing spaces
        r, g, b, a = parse_color_string("  #FF0000  ")
        self.assertAlmostEqual(r, 1.0, places=2)
        self.assertAlmostEqual(g, 0.0, places=2)
        self.assertAlmostEqual(b, 0.0, places=2)
        self.assertAlmostEqual(a, 1.0, places=2)
        
        # Test RGB with extra spaces
        r, g, b, a = parse_color_string("  128  ,  64  ,  32  ")
        self.assertAlmostEqual(r, 0.502, places=2)
        self.assertAlmostEqual(g, 0.251, places=2)
        self.assertAlmostEqual(b, 0.125, places=2)
        self.assertAlmostEqual(a, 1.0, places=2)


if __name__ == "__main__":
    unittest.main()