from hutil.Qt import QtCore, QtUiTools, QtWidgets, QtGui





window = ViewTree({"Pipe 1": {'1.Name': 'ABC', '2.Outside diameter': '10', '3.Wall thickness': '5', '4.Density': '7850', '5.Liner layers': {1: {'1.Liner name': 'SAD', '2.Liner thickness': '5', '3.Liner density': '900'}}, '6.Coating layers': {1: {'1.Coating name': 'TWR', '2.Coating thickness': '50', '3.Coating density': '3000', '4.Coating cutback': '0.7', '5.Coating absorption': '4'}}}})

class ViewTree(QtWidgets.QTreeWidget):
    def __init__(self, value):
        super().__init__()
        def fill_item(item, value):
            def new_item(parent, text, val=None):
                child = QtWidgets.QTreeWidgetItem([text])
                fill_item(child, val)
                parent.addChild(child)
                child.setExpanded(True)
            if value is None: return
            elif isinstance(value, dict):
                for key, val in sorted(value.items()):
                    new_item(item, str(key), val)
            elif isinstance(value, (list, tuple)):
                for val in value:
                    text = (str(val) if not isinstance(val, (dict, list, tuple))
                            else '[%s]' % type(val).__name__)
                    new_item(item, text, val)
            else:
                new_item(item, str(value))

        fill_item(self.invisibleRootItem(), value)

if __name__ == '__main__':
    app = QApplication([])
    window = ViewTree({"Pipe 1": {'1.Name': 'ABC', '2.Outside diameter': '10', '3.Wall thickness': '5', '4.Density': '7850', '5.Liner layers': {1: {'1.Liner name': 'SAD', '2.Liner thickness': '5', '3.Liner density': '900'}}, '6.Coating layers': {1: {'1.Coating name': 'TWR', '2.Coating thickness': '50', '3.Coating density': '3000', '4.Coating cutback': '0.7', '5.Coating absorption': '4'}}}})
    window.show()
    app.exec_()
