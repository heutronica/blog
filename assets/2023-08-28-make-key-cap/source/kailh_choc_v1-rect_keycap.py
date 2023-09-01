import cadquery as cq

# ------------------ #
# SETTINGS scale: mm #
# ------------------ #

# keycap settings
keycap = {"width": 17, "height": 4, "fillet": 2, "taper": 2}

# 3D printer settings
printer = {
    "DIA": 0.36,
    # 'layerThickness': 0.2
}

# export settings
fileName = "kailh_choc_v1-{0}mm".format(keycap["width"])
outputDir = "/"

# -------- #
# MODELING #
# -------- #

keycap.update({"thickness": printer["DIA"] * 3, "top_thickness": printer["DIA"] * 2})

# keytop

fill_bottom = (
    cq.Sketch()
    .rect(keycap["width"], keycap["width"])
    .vertices()
    .fillet(keycap["fillet"])
)
fill_top = (
    cq.Sketch()
    .rect(keycap["width"] - keycap["taper"], keycap["width"] - keycap["taper"])
    .vertices()
    .fillet(keycap["fillet"])
)
fill = (
    cq.Workplane()
    .placeSketch(
        fill_top.moved(cq.Location(cq.Vector(0, 0, keycap["height"]))), fill_bottom
    )
    .loft()
)

# keytop inside

infill_width = keycap["width"] - keycap["thickness"] * 2
infill_fillet = max(0.01, keycap["fillet"] - keycap["thickness"] / 2)
# TODO: 内側のfilletの算出をもう少しいい感じにする
# TODO: filletの値がwidthに対して逸脱していないかをチェックする必要がある

infill_bottom = (
    cq.Sketch()
    .rect(
        infill_width,
        infill_width,
    )
    .vertices()
    .fillet(infill_fillet)
)
infill_top = (
    cq.Sketch()
    .rect(
        infill_width - keycap["taper"],
        infill_width - keycap["taper"],
    )
    .vertices()
    .fillet(infill_fillet)
)
infill = (
    cq.Workplane()
    .placeSketch(
        infill_bottom,
        infill_top.moved(
            cq.Location(cq.Vector(0, 0, keycap["height"] - keycap["top_thickness"]))
        ),
    )
    .loft()
)

keytop = fill.cut(infill)

# keycap STEM

clearance = printer["DIA"]

stem_plate = (
    cq.Workplane()
    .box(
        infill_width - keycap["taper"] - clearance,
        infill_width - keycap["taper"] - clearance,
        keycap["top_thickness"],
    )
    .edges("|Z")
    .fillet(infill_fillet)
)

stems = stem_plate.pushPoints([(3, 0), (-3, 0)]).eachpoint(
    lambda loc: cq.Workplane().rect(1.28, 4).extrude(-3).val().located(loc)
)

stem_plate = stem_plate.union(stems)

# ------ #
# EXPORT #
# ------ #

cq.exporters.export(keytop, "{0}/{1}.stl".format(outputDir, fileName))
cq.exporters.export(stem_plate, "{0}/{1}_stem.stl".format(outputDir, fileName))
