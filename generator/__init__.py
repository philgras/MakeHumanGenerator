from .makehuman_generator import GeneratorTaskView

"""
makehuman plugin: must be imported via makehuman application
"""


def load(app):
    category = app.getCategory('Utilities')
    category.addTask(GeneratorTaskView(category))


def unload(app):
    pass
