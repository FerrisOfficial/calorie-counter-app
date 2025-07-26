"""
Constants for the Calorie Counter app
"""

from kivy.utils import get_color_from_hex

class Colors:
    """Centralized color constants using get_color_from_hex"""
    BLACK = get_color_from_hex("#000000")
    BLACK_HEX = '#000000'
    BLUE = get_color_from_hex('#2196F3')
    BLUE_HEX = '#2196F3'
    GREEN = get_color_from_hex('#4CAF50')
    GREEN_HEX = '#4CAF50'
    RED = get_color_from_hex('#F44336')
    RED_HEX = '#F44336'
    ORANGE = get_color_from_hex('#FF9800')
    ORANGE_HEX = '#FF9800'
    GRAY = get_color_from_hex('#666666')
    GRAY_HEX = '#666666'
    GRAYER = get_color_from_hex('#333333')
    GRAYER_HEX = '#333333'
    WHITE = get_color_from_hex('#FFFFFF')
    WHITE_HEX = '#FFFFFF'

    @staticmethod
    def to_hex(color):
        """Converts a Kivy color to hex string"""
        dict_color = {
            tuple(Colors.BLACK): Colors.BLACK_HEX,
            tuple(Colors.BLUE): Colors.BLUE_HEX,
            tuple(Colors.GREEN): Colors.GREEN_HEX,
            tuple(Colors.RED): Colors.RED_HEX,
            tuple(Colors.ORANGE): Colors.ORANGE_HEX,
            tuple(Colors.GRAY): Colors.GRAY_HEX,
            tuple(Colors.GRAYER): Colors.GRAYER_HEX,
            tuple(Colors.WHITE): Colors.WHITE_HEX
        }
        return dict_color.get(tuple(color), "#000000")