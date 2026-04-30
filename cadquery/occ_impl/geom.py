"""Geometry primitives and transformations for CadQuery.

This module provides Vector, Matrix, and Plane classes used throughout
the CadQuery modeling pipeline.
"""

import math
from typing import Optional, Tuple, Union, overload

from OCC.Core.gp import (
    gp_Vec,
    gp_Pnt,
    gp_Dir,
    gp_Ax1,
    gp_Ax3,
    gp_Trsf,
    gp_GTrsf,
    gp_XYZ,
)


class Vector:
    """A 3D vector with common math operations.

    Wraps OCC gp_Vec / gp_Pnt to provide a convenient interface.
    """

    def __init__(self, *args):
        if len(args) == 3:
            self._wrapped = gp_Vec(args[0], args[1], args[2])
        elif len(args) == 1:
            if isinstance(args[0], gp_Vec):
                self._wrapped = args[0]
            elif isinstance(args[0], gp_Pnt):
                self._wrapped = gp_Vec(args[0].X(), args[0].Y(), args[0].Z())
            elif isinstance(args[0], gp_Dir):
                self._wrapped = gp_Vec(args[0])
            elif isinstance(args[0], (list, tuple)) and len(args[0]) == 3:
                self._wrapped = gp_Vec(*args[0])
            else:
                raise TypeError(f"Cannot construct Vector from {type(args[0])}")
        elif len(args) == 2:
            self._wrapped = gp_Vec(args[0], args[1], 0.0)
        else:
            raise TypeError(f"Vector requires 1, 2, or 3 arguments, got {len(args)}")

    @property
    def x(self) -> float:
        return self._wrapped.X()

    @property
    def y(self) -> float:
        return self._wrapped.Y()

    @property
    def z(self) -> float:
        return self._wrapped.Z()

    def to_pnt(self) -> gp_Pnt:
        return gp_Pnt(self._wrapped.XYZ())

    def to_dir(self) -> gp_Dir:
        return gp_Dir(self._wrapped)

    def length(self) -> float:
        return self._wrapped.Magnitude()

    def normalized(self) -> "Vector":
        """Return a unit vector in the same direction."""
        return Vector(self._wrapped.Normalized())

    def dot(self, other: "Vector") -> float:
        return self._wrapped.Dot(other._wrapped)

    def cross(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Crossed(other._wrapped))

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Added(other._wrapped))

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Subtracted(other._wrapped))

    def __mul__(self, scale: float) -> "Vector":
        return Vector(self._wrapped.Multiplied(scale))

    def __rmul__(self, scale: float) -> "Vector":
        return self.__mul__(scale)

    def __neg__(self) -> "Vector":
        return Vector(self._wrapped.Reversed())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self._wrapped.IsEqual(other._wrapped, 1e-9, 1e-9)

    def __repr__(self) -> str:
        return f"Vector({self.x:.6g}, {self.y:.6g}, {self.z:.6g})"

    def angle_between(self, other: "Vector") -> float:
        """Return the angle in degrees between this vector and another.

        Returns a value in [0, 180]. I find degrees more intuitive than
        radians for most CAD work, so converting here instead of returning
        raw radians like the OCC method does.
        """
        return math.degrees(self._wrapped.Angle(other._wrapped))
