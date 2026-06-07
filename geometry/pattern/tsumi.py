from typing import List, Union

from geometry.pattern.pattern import Pattern
from geometry.primitives import Line, Arc, QuadraticBezier


class TsumiPattern(Pattern):
    def get_material_cost(self) -> float:
        return 2.5

    def _get_geometry(self, a, b, c) -> List[Union[Line, Arc, QuadraticBezier]]:
        ax, ay = a
        bx, by = b
        cx, cy = c

        # Centroid (center of triangle)
        centroid_x = (ax + bx + cx) / 3
        centroid_y = (ay + by + cy) / 3

        # Midpoints of each edge
        mid_ab = ((ax + bx) / 2, (ay + by) / 2)
        mid_bc = ((bx + cx) / 2, (by + cy) / 2)
        mid_ca = ((cx + ax) / 2, (cy + ay) / 2)

        return  [
            Line((centroid_x, centroid_y), (mid_ab[0], mid_ab[1])),
            Line((centroid_x, centroid_y), (mid_bc[0], mid_bc[1])),
            Line((centroid_x, centroid_y), (mid_ca[0], mid_ca[1]))
        ]
