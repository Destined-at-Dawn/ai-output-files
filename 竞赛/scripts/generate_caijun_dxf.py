import ezdxf
import os
import math

# 输出目录
OUT_DIR = r"${WORKSPACE_ROOT}/projects/跨校协作/outputs/蔡俊-CAD设计"
os.makedirs(OUT_DIR, exist_ok=True)

def create_base_dxf():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    doc.layers.add("CUT-OUTER", color=1)
    doc.layers.add("ENGRAVE-INNER", color=4)
    doc.layers.add("HOLE", color=3)
    doc.layers.add("BEND", color=6)
    doc.layers.add("DIM", color=7)
    return doc, msp

def save_dxf(doc, name):
    path = os.path.join(OUT_DIR, name)
    doc.saveas(path)
    size = os.path.getsize(path)
    print(f"  OK {name} - {size} bytes")
    return path

# ========== 零件01：头颈件 ==========
print("Part 01...")
doc, msp = create_base_dxf()

head_pts = [
    (0, 10), (6, 10.5), (10, 8), (12, 5), (13, 3),
    (13.5, 1.5), (12.5, 0), (11, -1), (11.5, -2.5),
    (10, -4), (8, -5.5), (5, -6.5), (2, -7),
    (-2, -7), (-5, -6), (-8, -3), (-10, 2), (-10, 6),
    (-7, 9), (-3, 10.2), (0, 10),
]
msp.add_lwpolyline(head_pts, dxfattribs={"layer": "CUT-OUTER", "const_width": 0.2})

ear_pts = [(-7, 3), (-9, 4.5), (-10, 3), (-9, 1.5), (-7, 3)]
msp.add_lwpolyline(ear_pts, dxfattribs={"layer": "CUT-OUTER"})

eye_center = (3, 4.5)
msp.add_circle(eye_center, 1.2, dxfattribs={"layer": "ENGRAVE-INNER"})
msp.add_arc(eye_center, 1.2, 30, 150, dxfattribs={"layer": "ENGRAVE-INNER"})

mouth_center = (11, -1.5)
msp.add_arc(mouth_center, 0.8, 200, 340, dxfattribs={"layer": "ENGRAVE-INNER"})

for i in range(3):
    y = 8 - i * 1.5
    pts = [(-5+i*2, y+2), (-2+i*3, y+1.5), (2+i*2, y)]
    msp.add_lwpolyline(pts, dxfattribs={"layer": "ENGRAVE-INNER"})

collar_pts = [(1, -7), (3, -9), (5, -9), (7, -7)]
msp.add_lwpolyline(collar_pts, dxfattribs={"layer": "ENGRAVE-INNER"})
collar_inner = [(2, -7.5), (3.5, -8.5), (5, -8.5), (6, -7.5)]
msp.add_lwpolyline(collar_inner, dxfattribs={"layer": "ENGRAVE-INNER"})

msp.add_circle((-2, -7), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((-2, -7), 4, dxfattribs={"layer": "CUT-OUTER"})

save_dxf(doc, "零件01-头颈件.dxf")

# ========== 零件02：上躯干件 ==========
print("Part 02...")
doc, msp = create_base_dxf()

torso_pts = [
    (-20, 25), (-15, 30), (-5, 32), (0, 33), (5, 32),
    (15, 30), (20, 25), (18, 10), (15, 0), (12, -5),
    (5, -8), (0, -8), (-5, -8), (-12, -5), (-15, 0),
    (-18, 10), (-20, 25),
]
msp.add_lwpolyline(torso_pts, dxfattribs={"layer": "CUT-OUTER", "const_width": 0.2})

msp.add_line((0, 30), (0, -5), dxfattribs={"layer": "ENGRAVE-INNER"})
for y in range(25, 0, -5):
    msp.add_circle((0, y), 0.8, dxfattribs={"layer": "ENGRAVE-INNER"})
for y in range(22, 5, -4):
    msp.add_lwpolyline([(-2, y), (2, y), (2, y-2), (-2, y-2), (-2, y)],
                        dxfattribs={"layer": "ENGRAVE-INNER"})

plane_pts = [(-3, 18), (0, 20), (3, 18), (2, 17), (-2, 17), (-3, 18)]
msp.add_lwpolyline(plane_pts, dxfattribs={"layer": "ENGRAVE-INNER"})

msp.add_circle((-17, 27), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((17, 27), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((-17, 27), 4, dxfattribs={"layer": "CUT-OUTER"})
msp.add_circle((17, 27), 4, dxfattribs={"layer": "CUT-OUTER"})
msp.add_circle((0, -5), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, -5), 4, dxfattribs={"layer": "CUT-OUTER"})

save_dxf(doc, "零件02-上躯干件.dxf")

# ========== 零件03：下躯干件 ==========
print("Part 03...")
doc, msp = create_base_dxf()

lower_torso = [
    (-12, 15), (-15, 12), (-16, 8), (-15, 3), (-14, 0),
    (-12, -5), (-10, -10), (-5, -12), (0, -12.5),
    (5, -12), (10, -10), (12, -5), (14, 0),
    (15, 3), (16, 8), (15, 12), (12, 15),
    (5, 16), (0, 16), (-5, 16), (-12, 15),
]
msp.add_lwpolyline(lower_torso, dxfattribs={"layer": "CUT-OUTER", "const_width": 0.2})

msp.add_line((-14, 3), (14, 3), dxfattribs={"layer": "ENGRAVE-INNER"})
msp.add_line((-14, 1), (14, 1), dxfattribs={"layer": "ENGRAVE-INNER"})
msp.add_lwpolyline([(-2, 4), (2, 4), (2, 0), (-2, 0), (-2, 4)],
                    dxfattribs={"layer": "ENGRAVE-INNER"})

msp.add_circle((-13, -2), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((13, -2), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((-13, -2), 4, dxfattribs={"layer": "CUT-OUTER"})
msp.add_circle((13, -2), 4, dxfattribs={"layer": "CUT-OUTER"})
msp.add_circle((0, 13), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, 13), 4, dxfattribs={"layer": "CUT-OUTER"})

save_dxf(doc, "零件03-下躯干件.dxf")

# ========== 零件04：左上臂件 ==========
print("Part 04...")
doc, msp = create_base_dxf()

arm_pts = [
    (-5, 25), (5, 25), (6, 20), (6, 5),
    (5, 0), (-5, 0), (-6, 5), (-6, 20), (-5, 25),
]
msp.add_lwpolyline(arm_pts, dxfattribs={"layer": "CUT-OUTER", "const_width": 0.2})

for y in [22, 20, 5, 3]:
    msp.add_lwpolyline([(-4, y), (4, y), (4, y-1), (-4, y-1), (-4, y)],
                        dxfattribs={"layer": "ENGRAVE-INNER"})

msp.add_circle((0, 22), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, 22), 4, dxfattribs={"layer": "CUT-OUTER"})
msp.add_circle((0, 3), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, 3), 4, dxfattribs={"layer": "CUT-OUTER"})

save_dxf(doc, "零件04-左上臂件.dxf")

# ========== 零件05：右上臂件 ==========
print("Part 05...")
doc, msp = create_base_dxf()

msp.add_lwpolyline(arm_pts, dxfattribs={"layer": "CUT-OUTER", "const_width": 0.2})
for y in [22, 20, 5, 3]:
    msp.add_lwpolyline([(-4, y), (4, y), (4, y-1), (-4, y-1), (-4, y)],
                        dxfattribs={"layer": "ENGRAVE-INNER"})
msp.add_circle((0, 22), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, 22), 4, dxfattribs={"layer": "CUT-OUTER"})
msp.add_circle((0, 3), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, 3), 4, dxfattribs={"layer": "CUT-OUTER"})

save_dxf(doc, "零件05-右上臂件.dxf")

# ========== 零件06：左前臂连手件 ==========
print("Part 06...")
doc, msp = create_base_dxf()

forearm = [
    (-4, 28), (4, 28), (5, 24), (5, 8),
    (4, 4), (-4, 4), (-5, 8), (-5, 24), (-4, 28),
]
msp.add_lwpolyline(forearm, dxfattribs={"layer": "CUT-OUTER", "const_width": 0.2})

palm = [
    (-5, 4), (-5, 0), (-8, -4), (-6, -2), (-4, -6),
    (-1, -7), (1, -7), (3, -6), (5, -2), (6, 0), (5, 4),
]
msp.add_lwpolyline(palm, dxfattribs={"layer": "CUT-OUTER"})

for y in [26, 24]:
    msp.add_lwpolyline([(-3, y), (3, y), (3, y-1), (-3, y-1), (-3, y)],
                        dxfattribs={"layer": "ENGRAVE-INNER"})

msp.add_circle((0, 26), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, 26), 4, dxfattribs={"layer": "CUT-OUTER"})
msp.add_circle((0, 2), 0.75, dxfattribs={"layer": "HOLE"})

save_dxf(doc, "零件06-左前臂连手件.dxf")

# ========== 零件07：右前臂连手件 ==========
print("Part 07...")
doc, msp = create_base_dxf()

msp.add_lwpolyline(forearm, dxfattribs={"layer": "CUT-OUTER", "const_width": 0.2})

fist_center = (0, 1)
msp.add_circle(fist_center, 4, dxfattribs={"layer": "CUT-OUTER"})
for angle in [30, 60, 90, 120, 150]:
    x1 = fist_center[0] + 2.5 * math.cos(math.radians(angle))
    y1 = fist_center[1] + 2.5 * math.sin(math.radians(angle))
    x2 = fist_center[0] + 4 * math.cos(math.radians(angle))
    y2 = fist_center[1] + 4 * math.sin(math.radians(angle))
    msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": "ENGRAVE-INNER"})

slot_pts = [(-2, 4), (-2, 6), (2, 6), (2, 4)]
msp.add_lwpolyline(slot_pts, dxfattribs={"layer": "CUT-OUTER"})

for y in [26, 24]:
    msp.add_lwpolyline([(-3, y), (3, y), (3, y-1), (-3, y-1), (-3, y)],
                        dxfattribs={"layer": "ENGRAVE-INNER"})

msp.add_circle((0, 26), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, 26), 4, dxfattribs={"layer": "CUT-OUTER"})
msp.add_circle((0, 5), 0.75, dxfattribs={"layer": "HOLE"})

save_dxf(doc, "零件07-右前臂连手件.dxf")

# ========== 零件08：左大腿件 ==========
print("Part 08...")
doc, msp = create_base_dxf()

thigh = [
    (-5, 25), (5, 25), (6, 20), (6, 5),
    (5, 0), (-5, 0), (-6, 5), (-6, 20), (-5, 25),
]
msp.add_lwpolyline(thigh, dxfattribs={"layer": "CUT-OUTER", "const_width": 0.2})
msp.add_line((0, 24), (0, 1), dxfattribs={"layer": "ENGRAVE-INNER"})

msp.add_circle((0, 22), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, 22), 4, dxfattribs={"layer": "CUT-OUTER"})
msp.add_circle((0, 3), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, 3), 4, dxfattribs={"layer": "CUT-OUTER"})

save_dxf(doc, "零件08-左大腿件.dxf")

# ========== 零件09：右小腿连脚件 ==========
print("Part 09...")
doc, msp = create_base_dxf()

calf = [
    (-4, 30), (4, 30), (5, 25), (5, 8),
    (4, 4), (-4, 4), (-5, 8), (-5, 25), (-4, 30),
]
msp.add_lwpolyline(calf, dxfattribs={"layer": "CUT-OUTER", "const_width": 0.2})

shoe = [
    (-5, 4), (-5, 0), (-4, -2), (0, -6),
    (4, -2), (5, 0), (5, 4),
]
msp.add_lwpolyline(shoe, dxfattribs={"layer": "CUT-OUTER"})

msp.add_line((-3, 0), (3, 0), dxfattribs={"layer": "ENGRAVE-INNER"})
msp.add_line((-2, -2), (2, -2), dxfattribs={"layer": "ENGRAVE-INNER"})
msp.add_line((0, 28), (0, 8), dxfattribs={"layer": "ENGRAVE-INNER"})

msp.add_circle((0, 27), 0.75, dxfattribs={"layer": "HOLE"})
msp.add_circle((0, 27), 4, dxfattribs={"layer": "CUT-OUTER"})

save_dxf(doc, "零件09-右小腿连脚件.dxf")

# ========== 零件10：书籍道具 ==========
print("Part 10...")
doc, msp = create_base_dxf()

book = [
    (-10, 13), (10, 13), (10, -13), (-10, -13), (-10, 13),
]
msp.add_lwpolyline(book, dxfattribs={"layer": "CUT-OUTER", "const_width": 0.2})
msp.add_line((-7, 13), (-7, -13), dxfattribs={"layer": "ENGRAVE-INNER"})

plane = [
    (-3, 5), (0, 8), (5, 6), (3, 5), (6, 3),
    (3, 2), (5, 0), (0, -2), (-3, 0), (-3, 5),
]
msp.add_lwpolyline(plane, dxfattribs={"layer": "ENGRAVE-INNER"})

msp.add_lwpolyline([(-5, -5), (5, -5), (5, -10), (-5, -10), (-5, -5)],
                    dxfattribs={"layer": "ENGRAVE-INNER"})

msp.add_circle((-3, 12), 1, dxfattribs={"layer": "HOLE"})
msp.add_circle((3, 12), 1, dxfattribs={"layer": "HOLE"})

save_dxf(doc, "零件10-书籍道具.dxf")

# ========== 平铺布局总览 ==========
print("Layout...")
doc, msp = create_base_dxf()

parts_offsets = [
    ("零件01-头颈件", 0, 0),
    ("零件02-上躯干件", 60, 0),
    ("零件03-下躯干件", 120, 0),
    ("零件04-左上臂件", 170, 0),
    ("零件05-右上臂件", 170, -40),
    ("零件06-左前臂连手件", 0, -80),
    ("零件07-右前臂连手件", 70, -80),
    ("零件08-左大腿件", 140, -80),
    ("零件09-右小腿连脚件", 200, -80),
    ("零件10-书籍道具", 270, -40),
]

for part_name, ox, oy in parts_offsets:
    dxf_path = os.path.join(OUT_DIR, f"{part_name}.dxf")
    if os.path.exists(dxf_path):
        src = ezdxf.readfile(dxf_path)
        for entity in src.modelspace():
            dxftype = entity.dxftype()
            attribs = dict(entity.dxfattribs())
            # Remove handle/owner keys
            for k in ['handle', 'owner']:
                attribs.pop(k, None)
            if dxftype == 'LWPOLYLINE':
                pts = [(p[0]+ox, p[1]+oy) for p in entity.get_points()]
                msp.add_lwpolyline(pts, dxfattribs=attribs)
            elif dxftype == 'CIRCLE':
                c = entity.dxf.center
                msp.add_circle((c[0]+ox, c[1]+oy), entity.dxf.radius, dxfattribs=attribs)
            elif dxftype == 'LINE':
                s = entity.dxf.start
                e = entity.dxf.end
                msp.add_line((s[0]+ox, s[1]+oy), (e[0]+ox, e[1]+oy), dxfattribs=attribs)
            elif dxftype == 'ARC':
                c = entity.dxf.center
                msp.add_arc((c[0]+ox, c[1]+oy), entity.dxf.radius,
                           entity.dxf.start_angle, entity.dxf.end_angle, dxfattribs=attribs)
        # Label
        msp.add_text(part_name, dxfattribs={"layer": "DIM", "height": 3, "insert": (ox-10, oy-20)})

save_dxf(doc, "平铺布局总览.dxf")

print("\n=== DONE ===")
for f in sorted(os.listdir(OUT_DIR)):
    if f.endswith('.dxf'):
        full = os.path.join(OUT_DIR, f)
        print(f"  {os.path.getsize(full):>8}B  {f}")
