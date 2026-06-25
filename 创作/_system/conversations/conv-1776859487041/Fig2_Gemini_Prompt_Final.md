# Fig. 2 — Final Prompt for Gemini (English Only, High Clarity)

Copy everything below the line and paste it into Gemini as a single prompt.

---

## Prompt

Generate a high-resolution, publication-quality technical block diagram for an academic paper. The diagram illustrates the four-layer hierarchical architecture of an FPGA-based secure communication system.

**Overall style requirements (CRITICAL — follow exactly):**

- Pure white background (#FFFFFF), no gradients, no shadows, no 3D effects, no decorative borders
- Clean vector-style flat illustration, extremely sharp lines and text
- All text in English only — absolutely NO Chinese characters anywhere
- Font: Arial or Helvetica, crisp and legible at print size
- Title/label font size: 10–12 pt equivalent; annotation font size: 8–9 pt equivalent
- Color palette: four shades of blue for the four layers (darkest at bottom, lightest at top): Layer 1 #1A3A6B, Layer 2 #2E5AAC, Layer 3 #4A6FA5, Layer 4 #7B9BC2. Module boxes inside each layer: white fill with thin border matching the layer color. Text: black (#000000)
- Line weight: 1.5 pt for main connections, 1 pt for internal module borders
- Arrow style: solid filled triangular arrowheads, consistent size throughout
- Output: high resolution, minimum 2048 × 1400 pixels, crisp text with no blur or ghosting
- NO watermarks, NO signatures, NO decorative elements

**Layout — four horizontal layers stacked vertically, bottom to top:**

Each layer is a wide rounded rectangle spanning the full diagram width. Layers are stacked with ~15px vertical gap between them. Inside each layer, module boxes are arranged horizontally. Vertical arrows between layers show data flow direction.

**LAYER 1 (bottom) — Transport Layer:**

- Background: rounded rectangle filled with #1A3A6B (darkest blue), ~20% opacity fill so internal modules are visible
- Layer label on the left edge (vertical text, white): "Transport Layer"
- Three module boxes inside, arranged left to right:
  - Box 1: "uart_rx" — subtitle below: "16× Oversampling + Majority Vote"
  - Box 2: "uart_tx" — subtitle below: "8N1 Frame Generator"
  - Box 3: "crc16" — subtitle below: "CRC-16-CCITT (poly 0x1021)"
- Below Layer 1, a thin annotation line: "UART Physical Interface: RX / TX (125 kbps, 8N1)"
- Each module box: white fill, thin border in #1A3A6B, rounded corners

**LAYER 2 — Crypto Layer:**

- Background: rounded rectangle filled with #2E5AAC, ~20% opacity
- Layer label on the left edge (vertical text, white): "Crypto Layer"
- One large module box in the center: "crypto_top" — subtitle: "Crypto Arbiter (3-bit Opcode Select)"
- Inside crypto_top, three sub-module boxes arranged horizontally, separated by thin dashed lines:
  - Sub-box 1: "aes_core" — subtitle: "AES-128 (10 rounds, FIPS-197)"
  - Sub-box 2: "sha256" — subtitle: "SHA-256 (FIPS-180-4)"
  - Sub-box 3: "ecdh" — subtitle: "ECDH P-256 (secp256r1)"
- To the right of crypto_top, a small annotation table (compact, no heavy borders):
  ```
  Opcode | Operation
  000    | ECDH Key Pair Gen
  001    | ECDH Shared Key
  010    | AES Encrypt
  011    | AES Decrypt
  100    | SHA-256 Hash
  ```
- Sub-module boxes: white fill, thin dashed border in #2E5AAC

**LAYER 3 — Protocol Layer:**

- Background: rounded rectangle filled with #4A6FA5, ~20% opacity
- Layer label on the left edge (vertical text, white): "Protocol Layer"
- Two module boxes inside, arranged left and right with a double-headed arrow between them:
  - Box 1 (left): "frame_parser" — subtitle: "Frame Disassembly"
  - Box 2 (right): "frame_builder" — subtitle: "Frame Assembly"
- Between the two boxes: a horizontal double-headed arrow labeled "Bidirectional"
- To the right, a compact frame format annotation:
"[Magic 2B] [Length 2B] [Type 1B] [Payload NB] [CRC16 2B]"
Below it: "Magic = 0xAA55 | Type: 0x01 Data, 0x02 KeyExch, 0x03 Handshake, 0xFF Heartbeat"

**LAYER 4 (top) — Application Layer:**

- Background: rounded rectangle filled with #7B9BC2 (lightest blue), ~20% opacity
- Layer label on the left edge (vertical text, white): "Application Layer"
- One module box in the center: "secure_comm_top" — subtitle: "Main Controller"
- Inside this box, two sub-sections side by side:
  - Left sub-section: a compact state machine flow (horizontal):
  "IDLE → DECODE → CRYPTO → SEND" with a branch arrow from any state down to "ERROR", and "ERROR → IDLE" return arrow
  Use small rounded rectangles for each state, connected by thin arrows
  - Right sub-section: "Key Storage" box containing three items listed vertically:
    - "Private Key (local)"
    - "Public Key (remote)"
    - "Shared Key (negotiated)"

**VERTICAL ARROWS between layers (data flow):**

- Left side: a large upward arrow spanning all four layers, labeled "RX Path (Receive)"
  - Arrow color: #2E5AAC
  - Flow: UART_RX → comm_top → frame_parser → secure_comm_top → crypto_top
- Right side: a large downward arrow spanning all four layers, labeled "TX Path (Transmit)"
  - Arrow color: #D32F2F (red, to distinguish from RX)
  - Flow: crypto_top → secure_comm_top → frame_builder → comm_top → UART_TX

**Between each adjacent layer pair:**

- Small vertical arrows (1.5 pt, black) connecting the module boxes to show data flow
- Arrow labels in 7 pt font: "raw bytes", "parsed frame", "plaintext / ciphertext", "control signals"

**Bottom of diagram:**

- Centered caption: "Fig. 2. Four-layer hierarchical architecture of the iCE40 FPGA-based secure communication system"
- Caption font: Times New Roman italic, 9 pt equivalent

**Quality checklist (re-read before generating):**

- Every single character must be sharp, with zero ghosting or double-rendering
- No overlapping text anywhere
- All four layers must be clearly distinguishable by color shade (darkest at bottom, lightest at top)
- Module boxes must be neatly aligned within each layer
- The opcode table must be legible and properly formatted
- The state machine inside Layer 4 must show clear transitions with arrows
- The frame format annotation must be compact but fully readable
- The entire diagram must look like it belongs in an IEEE Transactions journal paper
- All layer labels, module names, and annotations must be perfectly horizontal (not rotated or skewed), except the vertical layer labels on the left edge

&nbsp;