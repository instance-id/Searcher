import hou

from hutil.Qt import QtCore
from hutil.Qt import QtGui
from hutil.Qt import QtWidgets

_MIN_RGB_VALUE = 0
_MAX_RGB_VALUE = 255

class ColorFieldSelector(QtWidgets.QWidget):
    """
hou.qt.ColorField

A widget for color input.

The widget contains a color swatch button and an input field for RGBA
values.

This class inherits from Qt's QtWidgets.QWidget class.

"""
    def __init__(self, label="", include_alpha=False):
        """
__init__(self, label=\"\", include_alpha=False)

    Create and return a new ColorField object.


    label
        If set to a non-empty string then a label is added to the color
        field.

    include_alpha
        If True, then an alpha component is added to the color field.

"""
        QtWidgets.QWidget.__init__(self)

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(hou.ui.scaledSize(2))
        layout.setContentsMargins(0, 0, 0, 0)

        self.colorSwatchButton = hou.qt.ColorSwatchButton(include_alpha)

        # Use the color swatch button's colorChanged signal as our own.
        self.colorChanged = self.colorSwatchButton.colorChanged

        self.inputField = hou.qt.InputField(
            hou.qt.InputField.FloatType,
            4 if include_alpha else 3)

        if label is not None and label != "":
            layout.addWidget(hou.qt.FieldLabel(label))

        layout.addWidget(self.colorSwatchButton)
        layout.addSpacing(hou.ui.scaledSize(5))
        layout.addWidget(self.inputField)

        # Connect color swatch button to field so their values
        # are always in-sync.
        self.colorSwatchButton.colorChanged.connect(
            self._updateFieldFromColorSwatch)
        self.inputField.valueChanged.connect(
            self._updateColorSwatchFromField)

        # Sync input field with color swatch.
        self._updateFieldFromColorSwatch(self.colorSwatchButton.color())

        self.setLayout(layout)

    def color(self):
        """
color() -> QtGui.QColor

    Return the field's current color.

"""
        return self.colorSwatchButton.color()

    def setColor(self, color):
        """
setColor(color)

    Set the field's current color. color must be a QtGui.QColor object.

"""
        self.colorSwatchButton.setColor(color)

        # Update the input field with the new color.
        self._updateFieldFromColorSwatch(color)

    def _updateFieldFromColorSwatch(self, color):
        if self.colorSwatchButton.hasAlpha():
            self.inputField.setValues([
                color.redF(), color.greenF(), color.blueF(), color.alphaF()])
        else:
            self.inputField.setValues([
                color.redF(), color.greenF(), color.blueF()]) 

    def _updateColorSwatchFromField(self):
        values = list(self.inputField.values())

        color = QtGui.QColor()
        color.setRedF(self._clampRGBValue(values[0]))
        color.setGreenF(self._clampRGBValue(values[1]))
        color.setBlueF(self._clampRGBValue(values[2]))

        if self.colorSwatchButton.hasAlpha():
            color.setAlphaF(self._clampRGBValue(values[3]))

        self.colorSwatchButton.setColor(color)

    def _clampRGBValue(self, val):
        if val > 1.0:
            return 1.0

        if val < 0.0:
            return 0.0

        return val

