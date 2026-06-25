#!/usr/bin/env python3
"""
Image → ROM COE file converter
Supports RGB888 (24-bit) and RGB565 (16-bit) output.

Usage:
    python logo_to_rom.py logo.png                          # RGB888 (default)
    python logo_to_rom.py logo.png --rgb565                 # RGB565 for ST7796S etc
    python logo_to_rom.py logo.png --width 200 --height 150 # custom size

Output:
    logo_rom_data.hex    Verilog $readmemh format
    logo_rom_data.coe    Vivado BMG IP format
    logo_preview_WxH.png Resized preview

Dependencies: pip install pillow
"""

import argparse
from PIL import Image
import os

TARGET_W = 173
TARGET_H = 171


def rgb888_to_rgb565(r, g, b):
    """RGB888 (3x8-bit) -> RGB565 (16-bit): RRRRRGGGGGGBBBBB"""
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)


def rgb888_to_packed24(r, g, b):
    """RGB888 -> 24-bit: RRRRRRRRGGGGGGGGBBBBBBBB"""
    return (r << 16) | (g << 8) | b


def main():
    parser = argparse.ArgumentParser(description="Image -> FPGA ROM COE/HEX")
    parser.add_argument("image", help="Input image path (PNG/JPG/BMP)")
    parser.add_argument("--rgb565", action="store_true",
                        help="Output 16-bit RGB565 instead of 24-bit RGB888")
    parser.add_argument("--width", type=int, default=TARGET_W,
                        help=f"Target pixel width (default: {TARGET_W})")
    parser.add_argument("--height", type=int, default=TARGET_H,
                        help=f"Target pixel height (default: {TARGET_H})")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Output directory (default: same as script)")
    args = parser.parse_args()

    w, h = args.width, args.height
    out_dir = args.output_dir or os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    bit_mode = "RGB565" if args.rgb565 else "RGB888"
    bits_per_pixel = 16 if args.rgb565 else 24

    # Step 1: Load and resize
    print(f"[1] Reading: {args.image}")
    img = Image.open(args.image)
    print(f"    Original size: {img.size[0]}x{img.size[1]}, Mode: {img.mode}")

    print(f"[2] Resizing to {w}x{h}")
    img_resized = img.resize((w, h), Image.LANCZOS)
    img_rgb = img_resized.convert("RGB")

    # Save preview
    preview_path = os.path.join(out_dir, f"logo_preview_{w}x{h}.png")
    img_resized.save(preview_path)
    print(f"    Preview saved: {preview_path}")

    # Step 2: Convert pixels
    total = w * h
    print(f"[3] Converting {total} pixels to {bit_mode}")
    pixels = []
    for y in range(h):
        for x in range(w):
            r, g, b = img_rgb.getpixel((x, y))
            if args.rgb565:
                pixels.append(rgb888_to_rgb565(r, g, b))
            else:
                pixels.append(rgb888_to_packed24(r, g, b))

    # Step 3: Write HEX file
    hex_path = os.path.join(out_dir, "logo_rom_data.hex")
    hex_width = 4 if args.rgb565 else 6
    with open(hex_path, "w") as f:
        for val in pixels:
            f.write(f"{val:0{hex_width}X}\n")
    print(f"    HEX: {hex_path}")

    # Step 4: Write COE file
    coe_path = os.path.join(out_dir, "logo_rom_data.coe")
    with open(coe_path, "w") as f:
        f.write("memory_initialization_radix=16;\n")
        f.write("memory_initialization_vector=\n")
        for i, val in enumerate(pixels):
            comma = ",\n" if i < len(pixels) - 1 else ";\n"
            f.write(f"{val:0{hex_width}X}{comma}")
    print(f"    COE: {coe_path}")

    # Step 5: Stats
    total_bits = total * bits_per_pixel
    bram_blocks = (total_bits + 16384 - 1) // 16384
    print(f"\n[4] Summary:")
    print(f"    Pixels:  {total} ({w}x{h})")
    print(f"    Format:  {bit_mode} ({bits_per_pixel} bit/pixel)")
    print(f"    Bits:    {total_bits:,}")
    print(f"    BRAM:    ~{bram_blocks} x 16Kb blocks")
    print(f"    BMG IP:  Port A Width={bits_per_pixel}, Depth={total}")


if __name__ == "__main__":
    main()
