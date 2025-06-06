from dataclasses import dataclass, field as dc_field, replace

def define(_cls=None, **kwargs):
    def wrap(cls):
        return dataclass(cls)
    return wrap(_cls) if _cls is not None else wrap

def evolve(obj, **changes):
    return replace(obj, **changes)

def field(*, default=None, factory=None, **kwargs):
    if default is not None and factory is not None:
        raise ValueError('cannot specify both default and default_factory')
    if factory is not None:
        return dc_field(default_factory=factory)
    return dc_field(default=default)
