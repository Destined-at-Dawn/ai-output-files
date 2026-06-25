import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else "logo_rom_data.coe"
output_file = sys.argv[2] if len(sys.argv) > 2 else "logo_rom_data_rgb565.coe"

with open(input_file, 'r') as f:
    lines = f.readlines()

header = "memory_initialization_radix=16;\nmemory_initialization_vector=\n"
data_lines = []

for line in lines:
    line = line.strip().rstrip(',').rstrip(';')
    if not line or line.startswith('memory_'):
        continue
    val = int(line, 16)
    r = (val >> 16) & 0xFF
    g = (val >> 8) & 0xFF
    b = val & 0xFF
    rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
    data_lines.append(format(rgb565, '04X'))

with open(output_file, 'w') as f:
    f.write(header)
    for i, d in enumerate(data_lines):
        if i == len(data_lines) - 1:
            f.write(d + ";\n")
        else:
            f.write(d + ",\n")

print(f"Done: {len(data_lines)} pixels converted")
print(f"Sample: first={data_lines[0]}, last={data_lines[-1]}")
