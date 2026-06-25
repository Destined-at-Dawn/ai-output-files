# Codex University Physics Knowledge Base (Master Index)

> **Role**: This is the master logic base for Codex. Use this index to locate high-fidelity knowledge and exercise files.
> **Constraint**: Always prioritize absolute paths listed here. Follow the "SUEP Exam DNA" for each chapter.

## 1. Unified Navigation & Chapter Matrix

| Chapter | Knowledge Base Path | Exercise Library Path | SUEP Exam DNA (Focus Points) |
| :--- | :--- | :--- | :--- |
| **Ch 01: Kinematics** | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第01章-质点运动学\AI学习\knowledge_base.md` | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第01章-质点运动学\习题\exercise_library.md` | 🔴 Acceleration vector integration ($a \to v \to r$); 🟡 Normal/Tangential acceleration ($a_n, a_\tau$). |
| **Ch 02: Dynamics I** | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第02章-质点动力学\AI学习\summary.md` | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第02章-质点动力学\原来\课堂练习02.md` | 🔴 Newton's 2nd Law in differential form; 🟡 Work-Energy theorem. |
| **Ch 03: Rigid Body** | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第03章-刚体力学基础\知识点\刚体力学基础-核心知识点.md` | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第03章-刚体力学基础\习题\PPT课堂练习-结构化.md` | 🔴 **High Prob**: Moment of Inertia ($J$) calculation; 🔴 Angular Momentum Conservation (Bullet hitting rod). |
| **Ch 06: Electrostatics** | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第06章-静电场\知识点\静电场-核心知识点.md` | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第06章-静电场\习题\PPT课堂练习-结构化.md` | 🔴 Gauss's Law for symmetric distributions; 🟡 Potential ($V$) superposition. |
| **Ch 07: Magnetism I** | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第07章-电流与磁场\AI学习\summary.md` | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第07章-电流与磁场\原来\课堂练习07.md` | 🔴 Biot-Savart Law; 🔴 Ampere's Circuital Law (Infinite solenoid/wire). |
| **Ch 08: Magnetism II** | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第08章-电磁场\AI学习\summary.md` | `E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\第08章-电磁场\原来\课堂练习08.md` | 🔴 Faraday's Law ($ \mathcal{E} = -d\Phi/dt $); 🟡 Motional vs. Induced EMF. |

## 2. Master Formula Matrix (2024 Spring Paper Alignment)

### 🔴 High-Density Mechanics (Rigid Body Focus)
- **Rotational Inertia**: $ J = \int r^2 dm $. Rod (center): $ \frac{1}{12}ML^2 $, Rod (end): $ \frac{1}{3}ML^2 $, Disk: $ \frac{1}{2}MR^2 $.
- **Rotation Law**: $ \sum M = J \alpha $.
- **Angular Momentum**: $ L = J \omega $. Conservation: $ \sum M_{ext} = 0 \implies J_1\omega_1 = J_2\omega_2 $.
- **Energy**: $ E_k = \frac{1}{2}J\omega^2 $.

### 🔴 High-Density Electromagnetism
- **Gauss's Law**: $ \oint_S \vec{E} \cdot d\vec{S} = \frac{\sum q_{in}}{\varepsilon_0} $.
- **Electric Potential**: $ V = \int_P^\infty \vec{E} \cdot d\vec{l} $. Point Charge: $ V = \frac{q}{4\pi\varepsilon_0 r} $.
- **Ampere's Law**: $ \oint_L \vec{B} \cdot d\vec{l} = \mu_0 \sum I_{in} $.
- **Magnetic Force**: $ \vec{F} = q\vec{v} \times \vec{B} $ (Lorentz), $ d\vec{F} = I d\vec{l} \times \vec{B} $ (Ampere).

## 3. Codex Execution Instructions

To generate "Hell-Mode" exam questions for the user, follow these steps:
1. **Context Retrieval**: Read the corresponding `knowledge_base.md` and `exercise_library.md` for the target chapter.
2. **Problem Synthesis**: 
    - Select a 🔴 core concept.
    - Combine it with a 🟡 secondary concept (e.g., rigid body rotation + conservation of energy).
    - Increase difficulty by using variable calculus (e.g., time-dependent torque $M(t)$ or non-uniform charge density $\rho(r)$).
3. **Format Enforcement**: All solutions provided to the user MUST follow **SOP-01 (Eight-Step Physical Problem Solving Format)** defined in `E:\ai产出文件\牛马\日常学习\SOPs\物理电路解题格式SOP.md`.

## 4. Quality Audit Registry
- [x] LaTeX Syntax Rigor Check
- [x] Absolute Path Verification
- [x] SUEP Exam DNA Mapping (Based on 2024 Spring Papers)
- [x] Codex Instruction Clarity

---
*Created by Hermes Agent for University Physics Project.*
