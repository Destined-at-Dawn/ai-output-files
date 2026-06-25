# Fig. 1 — Final Prompt for Gemini (English Only, High Clarity)

Copy everything below the line and paste it into Gemini as a single prompt.

---

## Prompt

Generate a high-resolution, publication-quality technical diagram for an academic paper. The diagram illustrates security threats to plaintext UART communication in three embedded system scenarios.

**Overall style requirements (CRITICAL — follow exactly):**

- Pure white background (#FFFFFF), no gradients, no shadows, no 3D effects, no decorative borders
- Clean vector-style flat illustration, extremely sharp lines and text
- All text in English only — absolutely NO Chinese characters anywhere
- Font: Arial or Helvetica, crisp and legible at print size
- Title/label font size: 10–12 pt equivalent; annotation font size: 8–9 pt equivalent
- Color palette: primary blue #2E5AAC, secondary blue #4A6FA5, light blue #7B9BC2, danger red #D32F2F, light gray background for threat box #F0F0F0
- Line weight: 1.5 pt for main connections, 1 pt for secondary lines
- Arrow style: solid filled triangular arrowheads, consistent size throughout
- Output: high resolution, minimum 2048 × 1200 pixels, crisp text with no blur or ghosting
- NO watermarks, NO signatures, NO decorative elements

**Layout — three zones:**

**TOP ZONE — Three application scenarios arranged left to right, evenly spaced:**

Left panel — "Smart Door Lock System":

- Simple flat icon: a door lock outline + a small MCU chip icon
- Below the icons, two lines of text:
Line 1: "Card Reader ↔ Main Controller"
Line 2: "UART (125 kbps, 8N1)"
- Small annotation below: "STM32F103C8T6, 72 MHz"
- Panel border: thin rounded rectangle in #4A6FA5

Center panel — "Industrial PLC System":

- Simple flat icon: a PLC rack outline + a sensor icon
- Below the icons, two lines of text:
Line 1: "PLC ↔ Sensor / Actuator"
Line 2: "RS-485 Serial Bus (Modbus RTU)"
- Small annotation below: "S7-1200, 24 VDC"
- Panel border: thin rounded rectangle in #4A6FA5

Right panel — "UAV Flight Control System":

- Simple flat icon: a quadcopter top-view outline + a ground station laptop icon
- Below the icons, two lines of text:
Line 1: "Flight Controller ↔ Ground Station"
Line 2: "UART Telemetry Link (MAVLink)"
- Small annotation below: "Pixhawk, 400 Hz Control Loop"
- Panel border: thin rounded rectangle in #4A6FA5

**MIDDLE ZONE — Central communication link:**

- A prominent horizontal red dashed line (#D32F2F, 2 pt weight) spanning the full width of the diagram
- Centered label on the red dashed line: "UART / TTL Serial Link — Plaintext Transmission"
- The label should have a small white background pad so it is clearly readable over the dashed line
- Three thin blue arrows drop down from each of the three panels above to connect to this red dashed line

**BOTTOM ZONE — Attacker and threat classification:**

Left side of bottom zone — Attacker:

- A simple human silhouette icon in red outline (#D32F2F)
- Label below: "Attacker"
- A red upward arrow from the attacker to the red dashed line
- Arrow label: "Physical Access / Logic Analyzer Capture"
- Next to the attacker: a small flat icon of a logic analyzer device

Right side of bottom zone — Threat classification box:

- A rounded rectangle with light gray fill (#F0F0F0) and thin border
- Title inside the box: "Security Threats" (bold, 10 pt)
- Three items listed vertically, each preceded by a small red triangle warning icon:
  1. Eavesdropping (Passive)
  2. Tampering (Active)
  3. Replay Attack (Active)

**Bottom of diagram:**

- Centered caption: "Fig. 1. Application scenarios and security threats of plaintext UART communication in embedded systems"
- Caption font: Times New Roman italic, 9 pt equivalent

**Quality checklist (re-read before generating):**

- Every single character must be sharp, with zero ghosting or double-rendering
- No overlapping text anywhere
- All three panels must be exactly the same size and evenly spaced
- The red dashed line must be perfectly horizontal
- All icons must be consistent flat style — no photorealistic elements
- The entire diagram must look like it belongs in an IEEE Transactions journal paper

&nbsp;