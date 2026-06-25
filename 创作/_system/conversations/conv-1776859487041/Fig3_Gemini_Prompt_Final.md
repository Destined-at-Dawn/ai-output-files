# Figure 3: Main Controller State Machine Diagram - Gemini Prompt
# For: "Secure Communication System Based on iCE40 FPGA with ECDH-AES"
# Target: Academic paper figure, teacher demonstration standard
# Language: English ONLY (absolutely NO Chinese characters anywhere)
# Resolution: Minimum 2048×1400px, vector-style, zero ghosting/double-rendering

---

## Prompt

**IMPORTANT**: Render all text as a single clean layer. Do NOT duplicate any text element. Zero ghosting / double-rendering. Minimum resolution 2048×1400px.

Draw a Moore finite state machine (FSM) transition diagram for academic paper publication. This is the main controller state machine of an FPGA-based secure communication system.

### **Figure Title & Style**
- Top center: **"Fig. 3: Main Controller State Machine Diagram"** in bold, 14pt Arial/Times New Roman
- Background: Pure white (#FFFFFF)
- Line style: Sharp, no anti-aliasing (vector-style)
- Color scheme: Blue-gray primary (#2E5AAC for states), red only for error paths (#D32F2F)
- NO 3D effects, NO gradients, NO shadows, NO decorative borders
- All text must be crisp and readable when printed on A4 paper at 600 DPI

### **State Nodes (6 states, rounded rectangles)**
Arrange horizontally as main flow: **IDLE → RECV → DECODE → CRYPTO → SEND**
Place **ERROR** state below the main flow, connected from RECV and back to IDLE.

1. **IDLE** (Initial state - draw with double circle outline)
   - Inside rectangle: **"IDLE"** (bold, 12pt)
   - Below state name: **"Wait for reception"** (10pt, italic)

2. **RECV** (Receive state)
   - Inside rectangle: **"RECV"** (bold, 12pt)
   - Below state name: **"Latch frame data"** (10pt, italic)

3. **DECODE** (Decode state)
   - Inside rectangle: **"DECODE"** (bold, 12pt)
   - Below state name: **"Parse frame type"** (10pt, italic)

4. **CRYPTO** (Cryptographic operation state)
   - Inside rectangle: **"CRYPTO"** (bold, 12pt)
   - Below state name: **"Start enc/dec/key exchange"** (10pt, italic)

5. **SEND** (Transmit state)
   - Inside rectangle: **"SEND"** (bold, 12pt)
   - Below state name: **"Assemble & send frame"** (10pt, italic)

6. **ERROR** (Error handling state - use red border #D32F2F)
   - Inside rectangle: **"ERROR"** (bold, 12pt, red text #D32F2F)
   - Below state name: **"Light error LED"** (10pt, italic, red #D32F2F)

### **Transition Arrows & Conditions**
Draw black solid arrows (1.5pt width) with transition conditions in 9pt font near arrow midpoint.

**Main flow (blue arrows #2E5AAC):**
1. **IDLE → RECV**: Label **"rx_done = 1"** (complete frame received)
2. **RECV → DECODE**: Label **"CRC check PASS"** (frame CRC verification passed)
3. **DECODE → CRYPTO**: Label **"frame_type decoded"** (frame type identified, start crypto op)
4. **CRYPTO → SEND**: Label **"crypto_done = 1"** (cryptographic operation completed)
5. **SEND → IDLE**: Label **"tx_done = 1"** (transmission completed)

**Error paths (red arrows #D32F2F):**
6. **RECV → ERROR**: Label **"CRC check FAIL"** (frame CRC verification failed)
7. **ERROR → IDLE**: Label **"timeout OR manual reset"** (error recovery)

### **Layout Specifications**
- **Horizontal spacing**: Equal distance between IDLE, RECV, DECODE, CRYPTO, SEND (approx 150px each)
- **Vertical placement**: ERROR state centered below RECV-DECODE-CRYPTO line
- **Arrow curvature**: Minimal, straight lines preferred, slight curves only where needed
- **Text alignment**: State names centered, transition labels positioned to avoid overlap
- **State size**: Rounded rectangles 120×80px, corner radius 10px
- **Double circle**: IDLE state outer circle 140×100px, inner rectangle as above

### **Technical Accuracy Notes**
- This FSM controls the secure_comm_top module in iCE40 FPGA system
- State transitions synchronized to 12MHz system clock
- CRC check refers to CRC-16-CCITT polynomial 0x1021
- Crypto operations include: AES-128 encryption/decryption, SHA-256 hash, ECDH P-256 key exchange
- Frame format: [Magic 2B][Length 2B][Type 1B][Payload NB][CRC16 2B]

### **Output Requirements**
- Format: SVG (vector) preferred, or PNG with lossless compression
- Resolution: ≥2048×1400px (scales to A4 paper width ~170mm)
- Text clarity: All text must remain sharp when printed at 600 DPI
- Color profile: sRGB
- File: No watermarks, no "AI generated" labels

**CRITICAL**: Render all text cleanly with zero duplication/ghosting. Each character must appear exactly once, perfectly aligned.