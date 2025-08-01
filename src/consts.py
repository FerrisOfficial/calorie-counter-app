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
    LIGHT_GRAY = get_color_from_hex('#CCCCCC')
    LIGHT_GRAY_HEX = '#CCCCCC'
    GRAYER = get_color_from_hex('#333333')
    GRAYER_HEX = '#333333'
    WHITE = get_color_from_hex('#FFFFFF')
    WHITE_HEX = '#FFFFFF'
    
    # Background colors for progress indicators
    LIGHT_GREEN = get_color_from_hex('#E8F5E8')
    LIGHT_GREEN_HEX = '#E8F5E8'
    LIGHT_ORANGE = get_color_from_hex('#FFF3E0')
    LIGHT_ORANGE_HEX = '#FFF3E0'
    LIGHT_RED = get_color_from_hex('#FFEBEE')
    LIGHT_RED_HEX = '#FFEBEE'
    
    # Text colors for input fields
    # Note: Due to Kivy TextInput limitations, foreground_color may not be visually effective
    # but the functionality is implemented and ready for future Kivy versions
    INPUT_TEXT_ACTIVE = get_color_from_hex('#000000')  # Black for active text
    INPUT_TEXT_ACTIVE_HEX = '#000000'

    TRANSPARENT = get_color_from_hex('#00000000')  # Fully transparent
    TRANSPARENT_HEX = '#00000000'

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
            tuple(Colors.LIGHT_GRAY): Colors.LIGHT_GRAY_HEX,
            tuple(Colors.GRAYER): Colors.GRAYER_HEX,
            tuple(Colors.WHITE): Colors.WHITE_HEX,
            tuple(Colors.INPUT_TEXT_ACTIVE): Colors.INPUT_TEXT_ACTIVE_HEX,
            tuple(Colors.LIGHT_GREEN): Colors.LIGHT_GREEN_HEX,
            tuple(Colors.LIGHT_ORANGE): Colors.LIGHT_ORANGE_HEX,
            tuple(Colors.LIGHT_RED): Colors.LIGHT_RED_HEX
        }
        return dict_color.get(tuple(color), "#000000")