"""Minimal stub of the plotly package for offline tests."""

import sys

class FakeBar:
    def __init__(self, *args, **kwargs):
        pass

class FakeFigure:
    def __init__(self, data=None):
        self.data = data or []

    def update_layout(self, *args, **kwargs):
        pass

    def update_xaxes(self, *args, **kwargs):
        pass

    def update_yaxes(self, *args, **kwargs):
        pass

    def to_image(self, format="png", width=800, height=500, scale=2):
        # Return enough bytes to satisfy tests checking image size
        return b"\x89PNG\r\n\x1a\n" + b"0" * 60000

# Expose submodules
module_name = __name__ + ".graph_objects"
graph_objects = sys.modules.setdefault(module_name, type(sys)(module_name))
graph_objects.Figure = FakeFigure
graph_objects.Bar = FakeBar

module_name = __name__ + ".express"
express = sys.modules.setdefault(module_name, type(sys)(module_name))

module_name = __name__ + ".subplots"
subplots = sys.modules.setdefault(module_name, type(sys)(module_name))

def make_subplots(*args, **kwargs):
    return FakeFigure()

subplots.make_subplots = make_subplots

__all__ = ["graph_objects", "express", "subplots"]
