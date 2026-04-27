"""Core shape classes wrapping OpenCASCADE topology."""

from typing import Optional, Tuple, Union, List
from OCC.Core.TopoDS import (
    TopoDS_Shape,
    TopoDS_Vertex,
    TopoDS_Edge,
    TopoDS_Wire,
    TopoDS_Face,
    TopoDS_Shell,
    TopoDS_Solid,
    TopoDS_Compound,
)
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeVertex,
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeFace,
)
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeSphere,
    BRepPrimAPI_MakeCylinder,
)
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import (
    TopAbs_VERTEX,
    TopAbs_EDGE,
    TopAbs_FACE,
    TopAbs_SOLID,
)
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib

from .geom import Vector


class Shape:
    """Base class for all CadQuery shapes, wrapping a TopoDS_Shape."""

    def __init__(self, obj: TopoDS_Shape):
        self._shape = obj

    @property
    def wrapped(self) -> TopoDS_Shape:
        """Return the underlying OCC shape."""
        return self._shape

    def bounding_box(self) -> Tuple[Vector, Vector]:
        """Compute the axis-aligned bounding box.

        Returns a tuple of (min_corner, max_corner) as Vectors.
        """
        bbox = Bnd_Box()
        brepbndlib.Add(self._shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        return Vector(xmin, ymin, zmin), Vector(xmax, ymax, zmax)

    def mesh(self, tolerance: float = 0.1, angular_tolerance: float = 0.1) -> None:
        """Tessellate the shape for rendering or export."""
        BRepMesh_IncrementalMesh(self._shape, tolerance, False, angular_tolerance)

    def vertices(self) -> List["Vertex"]:
        """Return all vertices of this shape."""
        explorer = TopExp_Explorer(self._shape, TopAbs_VERTEX)
        result = []
        while explorer.More():
            result.append(Vertex(explorer.Current()))
            explorer.Next()
        return result

    def edges(self) -> List["Edge"]:
        """Return all edges of this shape."""
        explorer = TopExp_Explorer(self._shape, TopAbs_EDGE)
        result = []
        while explorer.More():
            result.append(Edge(explorer.Current()))
            explorer.Next()
        return result

    def faces(self) -> List["Face"]:
        """Return all faces of this shape."""
        explorer = TopExp_Explorer(self._shape, TopAbs_FACE)
        result = []
        while explorer.More():
            result.append(Face(explorer.Current()))
            explorer.Next()
        return result

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._shape})"


class Vertex(Shape):
    """A single point in 3D space."""

    @classmethod
    def make_vertex(cls, x: float, y: float, z: float) -> "Vertex":
        """Create a vertex at the given coordinates."""
        v = BRepBuilderAPI_MakeVertex(gp_Pnt(x, y, z)).Vertex()
        return cls(v)


class Edge(Shape):
    """A curve bounded by two vertices."""

    pass


class Face(Shape):
    """A surface bounded by a wire."""

    pass


class Solid(Shape):
    """A closed volumetric shape."""

    @classmethod
    def make_box(
        cls,
        length: float,
        width: float,
        height: float,
        pnt: Optional[Vector] = None,
    ) -> "Solid":
        """Create a box solid.

        Args:
            length: Size along X axis.
            width: Size along Y axis.
            height: Size along Z axis.
            pnt: Optional origin corner (defaults to origin).
        """
        origin = pnt or Vector(0, 0, 0)
        box = BRepPrimAPI_MakeBox(
            gp_Pnt(origin.x, origin.y, origin.z), length, width, height
        ).Shape()
        return cls(box)

    @classmethod
    def make_sphere(cls, radius: float, center: Optional[Vector] = None) -> "Solid":
        """Create a sphere solid."""
        c = center or Vector(0, 0, 0)
        sphere = BRepPrimAPI_MakeSphere(gp_Pnt(c.x, c.y, c.z), radius).Shape()
        return cls(sphere)

    @classmethod
    def make_cylinder(
        cls,
        radius: float,
        height: float,
        axis: Optional[Vector] = None,
    ) -> "Solid":
        """Create a cylinder solid along the given axis (default Z)."""
        direction = axis or Vector(0, 0, 1)
        ax = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(direction.x, direction.y, direction.z))
        cyl = BRepPrimAPI_MakeCylinder(ax, radius, height).Shape()
        return cls(cyl)
