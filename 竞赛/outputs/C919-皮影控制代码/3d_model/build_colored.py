# -*- coding: utf-8 -*-
import cadquery as cq
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

OUT = r'E:i\产出文件\牛马\竞赛\竞赛\outputs\C919-皮影控制代码d_model'
os.makedirs(OUT, exist_ok=True)

print('Building colored assembly...')

# === RED: child + airplane ===
# Head
head = cq.Workplane('XY').cylinder(8, 20)
# Body
body = cq.Workplane('XY').box(30, 5, 60)
# Arms up (45 deg simulated by box at angle)
arm_l = cq.Workplane('XY').transformed(offset=(-30, 0, 30), rotate=(0, 30, 0)).box(80, 4, 6)
arm_r = cq.Workplane('XY').transformed(offset=(30, 0, 30), rotate=(0, 30, 0)).box(80, 4, 6)
# Legs
leg_l = cq.Workplane('XY').transformed(offset=(-10, 0, -30)).box(6, 4, 50)
leg_r = cq.Workplane('XY').transformed(offset=(10, 0, -30)).box(6, 4, 50)
child = head.union(body).union(arm_l).union(arm_r).union(leg_l).union(leg_r)
child = child.translate((0, 0, 600))

# Airplane on right hand
fuselage = cq.Workplane('XY').cylinder(50, 4)
wing_l = cq.Workplane('XY').transformed(offset=(-25, 0, 0), rotate=(0, 90, 0)).box(40, 2, 2)
wing_r = cq.Workplane('XY').transformed(offset=(25, 0, 0), rotate=(0, 90, 0)).box(40, 2, 2)
tail = cq.Workplane('XY').transformed(offset=(0, 0, -22)).box(16, 2, 12)
airplane = fuselage.union(wing_l).union(wing_r).union(tail)
airplane = airplane.translate((60, 0, 640))

child_full = child.union(airplane)
print('  child+airplane done')

# === WHITE: rods ===
rod1 = cq.Workplane('XY').transformed(offset=(38, 0, 625), rotate=(0, 25, 0)).cylinder(55, 1.5)
rod2 = cq.Workplane('XY').transformed(offset=(38, 0, 625), rotate=(0, -25, 0)).cylinder(55, 1.5)
rods = rod1.union(rod2)
print('  rods done')

# === BLUE: 2x DF9GMS servos ===
sv1 = cq.Workplane('XY').transformed(offset=(-15, 0, 580)).box(23, 12, 22)
sv2 = cq.Workplane('XY').transformed(offset=(15, 0, 580)).box(23, 12, 22)
servos = sv1.union(sv2)
print('  servos done')

# === GRAY: pillar ===
pillar = cq.Workplane('XY').box(30, 25, 600)
chan = cq.Workplane('XY').transformed(offset=(0, 0, 300)).box(6.5, 6.5, 602)
pillar = pillar.cut(chan)
print('  pillar done')

# === GRAY: base ===
base = cq.Workplane('XY').box(400, 300, 10)
for x, y in [(180, 130), (-180, 130), (180, -130), (-180, -130)]:
    base = base.workplane(offset=0).center(x, y).hole(6)
    base = base.workplane(offset=0).center(-x, -y)
print('  base done')

# === Assembly with colors ===
print('Creating assembly...')
asm = cq.Assembly()
asm.add(base, name='base', color=cq.Color(0.5, 0.5, 0.5, 1))
asm.add(pillar, name='pillar', color=cq.Color(0.5, 0.5, 0.5, 1))
asm.add(child_full, name='child', color=cq.Color(0.9, 0.1, 0.1, 1))
asm.add(rods, name='rods', color=cq.Color(0.95, 0.95, 0.95, 1))
asm.add(servos, name='servos', color=cq.Color(0.1, 0.3, 0.9, 1))

step_asm = os.path.join(OUT, 'v4_colored_assembly.step')
asm.save(step_asm, exportType='STEP')
sz = os.path.getsize(step_asm) / 1024
print(f'Assembly STEP: {sz:.0f} KB')

# Individual parts
for name, geo in [('base', base), ('pillar', pillar), ('child_airplane', child_full), ('rods', rods), ('servos', servos)]:
    p = os.path.join(OUT, f'v4_part_{name}.step')
    cq.exporters.export(geo, p)
    print(f'  {name}: {os.path.getsize(p)/1024:.0f} KB')

print('Done!')
