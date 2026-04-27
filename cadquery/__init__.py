"""CadQuery - A parametric 3D CAD scripting framework built on top of OCCT.

CadQuery is a Python library that allows you to build 3D models using a
fluent, chainable API. It wraps OpenCASCADE Technology (OCCT) to provide
a high-level interface for solid modeling.

Basic usage::

    import cadquery as cq

    result = cq.Workplane("XY").box(1, 2, 3)
    cq.exporters.export(result, "box.step")
"""

from .cq import (
    CQContext,
    CQObject,
    Workplane,
)
from .occ_impl.geom import (
    Vector,
    Matrix,
    Plane,
    Location,
)
from .occ_impl.shapes import (
    Shape,
    Vertex,
    Edge,
    Wire,
    Face,
    Shell,
    Solid,
    Compound,
)
from .occ_impl.assembly import (
    Assembly,
    Constraint,
)
from .selectors import (
    Selector,
    NearestToPointSelector,
    ParallelDirSelector,
    DirectionSelector,
    PerpendicularDirSelector,
    TypeSelector,
    DirectionMinMaxSelector,
    CenterNthSelector,
    RadiusNthSelector,
    LengthNthSelector,
    SumSelector,
    SubtractSelector,
    AndSelector,
    InverseSelector,
    StringSyntaxSelector,
)
from . import exporters
from . import importers
from . import selectors
from . import occ_impl

# Package metadata
__version__ = "2.4.0"
__author__ = "CadQuery Contributors"
__license__ = "Apache-2.0"
__url__ = "https://github.com/CadQuery/cadquery"

__all__ = [
    # Core workplane
    "CQContext",
    "CQObject",
    "Workplane",
    # Geometry primitives
    "Vector",
    "Matrix",
    "Plane",
    "Location",
    # Shape types
    "Shape",
    "Vertex",
    "Edge",
    "Wire",
    "Face",
    "Shell",
    "Solid",
    "Compound",
    # Assembly
    "Assembly",
    "Constraint",
    # Selectors
    "Selector",
    "NearestToPointSelector",
    "ParallelDirSelector",
    "DirectionSelector",
    "PerpendicularDirSelector",
    "TypeSelector",
    "DirectionMinMaxSelector",
    "CenterNthSelector",
    "RadiusNthSelector",
    "LengthNthSelector",
    "SumSelector",
    "SubtractSelector",
    "AndSelector",
    "InverseSelector",
    "StringSyntaxSelector",
    # Submodules
    "exporters",
    "importers",
    "selectors",
    "occ_impl",
]
