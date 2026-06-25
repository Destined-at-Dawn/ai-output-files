#!/usr/bin/env python3
"""
hex_to_coe.py
Convert $readmemh HEX file to Vivado BMG IP .coe format.
Usage: python hex_to_coe.py logo_rom_data.hex logo_rom_data.coe

HEX format (one value per line, 24-bit RGB888):
  FF0000
  00FF00
  ...

COE format:
  memory_initialization_radix=16;
  memory_initialization_vector=
  FF0000,
  00FF00,
  ...
  0000FF;
"""

import sys
import os

def hex_to_coe(hex_path, coe_path=None):
    if coe_path is None:
        coe_path = os.path.splitext(hex_path)[0] + '.coe'

    # Read hex file
    with open(hex_path, 'r') as f:
        lines = f.readlines()

    # Parse hex values (skip empty lines and comments)
    values = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('#'):
            continue
        # Handle Verilog-style comments at end of line
        if '//' in line:
            line = line[:line.index('//')].strip()
        if line:
            values.append(line.upper())

    if not values:
        print(f"ERROR: No data found in {hex_path}")
        return False

    # Write COE file
    with open(coe_path, 'w') as f:
        f.write("memory_initialization_radix=16;\n")
        f.write("memory_initialization_vector=\n")
        for i, val in enumerate(values):
            if i < len(values) - 1:
                f.write(f"{val},\n")
            else:
                f.write(f"{val};\n")  # Last value ends with semicolon

    print(f"Converted {len(values)} entries")
    print(f"  Input:  {hex_path}")
    print(f"  Output: {coe_path}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python hex_to_coe.py <input.hex> [output.coe]")
        sys.exit(1)
    hex_path = sys.argv[1]
    coe_path = sys.argv[2] if len(sys.argv) > 2 else None
    hex_to_coe(hex_path, coe_path)
