#!/usr/bin/env python3
# Logo图片 → RGB888 ROM数据 转换
# 输入: PISAAI Logo图片
# 输出: logo_rom_data.hex / logo_rom_data.coe / logo_preview_173x171.png

from PIL import Image
import os
import sys

TARGET_W = 173
TARGET_H = 171

def rgb_to_packed24(r, g, b):
    return (r << 16) | (g << 8) | b

def main():
    # 从命令行或默认路径读取图片
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    else:
        img_path = "logo.jpg"

    output_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"[1] Reading: {img_path}")
    img = Image.open(img_path)
    print(f"    Size: {img.size[0]}x{img.size[1]}, Mode: {img.mode}")

    print(f"[2] Resizing to {TARGET_W}x{TARGET_H}")
    img_resized = img.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    img_rgb = img_resized.convert("RGB")

    preview_path = os.path.join(output_dir, "logo_preview_173x171.png")
    img_resized.save(preview_path)

    print(f"[3] Converting to RGB888 ({TARGET_W * TARGET_H} pixels)")
    pixels = []
    for y in range(TARGET_H):
        for x in range(TARGET_W):
            r, g, b = img_rgb.getpixel((x, y))
            pixels.append(rgb_to_packed24(r, g, b))

    hex_path = os.path.join(output_dir, "logo_rom_data.hex")
    with open(hex_path, "w") as f:
        for val in pixels:
            f.write(f"{val:06X}\n")
    print(f"    HEX: {hex_path}")

    coe_path = os.path.join(output_dir, "logo_rom_data.coe")
    with open(coe_path, "w") as f:
        f.write("memory_initialization_radix=16;\n")
        f.write("memory_initialization_vector=\n")
        for i, val in enumerate(pixels):
            if i < len(pixels) - 1:
                f.write(f"{val:06X},\n")
            else:
                f.write(f"{val:06X};\n")
    print(f"    COE: {coe_path}")

    total_bits = len(pixels) * 24
    bram_blocks = (total_bits + 16384 - 1) // 16384
    print(f"\n[4] Stats:")
    print(f"    Pixels: {len(pixels)}")
    print(f"    Bits:   {total_bits:,}")
    print(f"    BRAM:   {bram_blocks} x 16Kb ({bram_blocks/100*100:.0f}%)")

if __name__ == "__main__":
    main()
