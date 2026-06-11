"""Parametric sensor-mount bracket — change a parameter, open a PR, watch
argus-diff comment the geometric change.

    python make_bracket.py --thickness 8 --hole 6 --boss-od 24
"""

from __future__ import annotations

import argparse

import cadquery as cq


def build(thickness: float, hole: float, boss_od: float, boss_x: float,
          gusset: bool, locating_pin: bool, gusset_offset: float = 10.0) -> cq.Assembly:
    plate = (
        cq.Workplane("XY")
        .box(90, 60, thickness, centered=(True, True, False))
        .faces(">Z").workplane()
        .rect(74, 44, forConstruction=True).vertices().hole(hole)
        .edges("|Z").fillet(6)
    )
    boss = (
        cq.Workplane("XY", origin=(boss_x, 0, thickness))
        .circle(boss_od / 2).extrude(14)
        .faces(">Z").workplane().hole(8)
    )
    asm = cq.Assembly(name="bracket")
    asm.add(plate, name="plate")
    asm.add(boss, name="boss")
    if gusset:
        g = (
            cq.Workplane("XZ", origin=(boss_x + gusset_offset, 2.5, thickness))
            .polyline([(0, 0), (18, 0), (0, 12)]).close().extrude(5)
        )
        asm.add(g, name="gusset")
    if locating_pin:
        asm.add(cq.Workplane("XY", origin=(-30, 15, 0)).circle(2).extrude(-8),
                name="locating_pin")
    asm.add(cq.Workplane("XY", origin=(30, -15, 0)).circle(2).extrude(-8), name="dowel")
    return asm


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--thickness", type=float, default=6.0)
    ap.add_argument("--hole", type=float, default=5.0)
    ap.add_argument("--boss-od", type=float, default=20.0)
    ap.add_argument("--boss-x", type=float, default=0.0)
    ap.add_argument("--gusset", action="store_true")
    ap.add_argument("--gusset-offset", type=float, default=10.0,
                    help="gusset root distance from boss center (mm)")
    ap.add_argument("--no-locating-pin", action="store_true")
    ap.add_argument("--out", default="cad/bracket.step")
    args = ap.parse_args()
    build(args.thickness, args.hole, args.boss_od, args.boss_x,
          args.gusset, not args.no_locating_pin, args.gusset_offset).export(args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
