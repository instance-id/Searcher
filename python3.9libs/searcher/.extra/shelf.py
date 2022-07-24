import hou


def create_shelf_current_desktop(shelf_obj):
    # Add the shelf to the current desktop.
    desktop = hou.ui.curDesktop()
    dock = desktop.shelfDock()
    shelfSets = dock.shelfSets()
    shelfSet = shelfSets[0]
    if shelf_obj not in shelfSet.shelves():
        shelfSet.setShelves(shelfSet.shelves() + (shelf_obj, ))
    return shelf_obj

def is_shelf_created(shelf_name, shelf_tab="shelf_set_1"):
    try:
        shelf_set = hou.shelves.shelfSets()[shelf_tab]
    except KeyError:
        print("Key not Found! for shelf.")
        return False
    return shelf_name in shelf_set.shelves()

def create_shelf_under_tab(shelf_name, shelf_tab="shelf_set_1"):
    shelves = hou.shelves.shelves()
    _shelf = shelves.get(shelf_name)
    if not _shelf:
        _shelf = hou.shelves.newShelf(name=shelf_name, label=shelf_name)
    try:
        shelf_set = hou.shelves.shelfSets()[shelf_tab]
    except KeyError:
        print("Key not Found! for shelf.")
        return 0
    shelf_set.setShelves(shelf_set.shelves() + (_shelf, ))
    return _shelf

def create_tool_under_shelf(shelf_obj, tool_name):
    # Clear the existing tools
    shelf_obj.setTools(())

    tools = hou.shelves.tools()
    tool = tools.get(tool_name)
    if not tool:
        tool = hou.shelves.newTool(name=tool_name)

    # Set up the tool.
    tool.setLabel(tool_name)
    # tool.setScript('from houtools.shelf import dispatch; dispatch(%r)' % spec['entrypoint'])
    shelf_obj.setTools(shelf_obj.tools() + (tool, ))

def run_shelf_creation():
    print("Trying to create the shelf.")
    if is_shelf_created("BpCustom"):
        print("Not running shelf creation as its present.")
        return 1
    shelf_obj = create_shelf_under_tab("BpCustom")
    create_tool_under_shelf(shelf_obj, "BpTool1")