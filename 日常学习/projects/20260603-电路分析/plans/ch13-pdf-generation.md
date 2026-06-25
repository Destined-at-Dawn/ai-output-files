# Chapter 13 Circuit Analysis PDF Generation Plan

## Context
The user wants to generate a Chapter 13 review PDF for the "Circuit Analysis" course based on **SOP-06**. 
Chapter 13 covers "Non-sinusoidal Periodic Current Circuits" (非正弦周期电流电路). 
A previous version of the PDF (v3) exists, but SOP-06 requires a "source-first" approach, focusing on original materials (教材, PPT, 习题) and providing visual evidence (screenshots) rather than just source references.

## Requirements
1. Follow **SOP-06** pipeline: P0 (Resources) -> P1 (Database) -> P2 (Templates) -> P3 (PDF Generation).
2. Use **Source-First Exam Mode**: 
   - Extract original question snippets from PDFs.
   - Embed screenshots of original problems/formulas into the PDF.
   - Use `image2` for high-quality page generation.
   - Use LaTeX for final PDF composition.
3. Ensure accuracy: No fabricated page numbers, handle different frequencies correctly (prohibited to add phasers of different frequencies directly), and follow SOP-01 for problem solving format.

## Critical Files & Resources
- **SOP**: `SOPs/06_复习PDF制作SOP.md`
- **Resource Index**: `outputs/00_资料索引.md`
- **Question Database**: `outputs/05_教材原题与习题原题索引.md`
- **Key Source Materials**:
    - PPT: `shared\学校资料\第13章  非正弦周期电流电路和信号的频谱.pdf`
    - Exercises: `shared\学校资料\第13章  非正弦周期电流电路-学生作业修改.pdf`
    - Answer Key: `shared\学校资料\第十三章习题答案-有删减.pdf`
    - Textbook: `shared\教材\电路_邱关源_内嵌教材.pdf`

## Implementation Plan

### Phase 1: Resource Preparation & Snippet Extraction (P0)
1.  **Initialize Directory**: Create `outputs/第13章_非正弦周期电流电路_复习PDF_v4/source_snippets/`.
2.  **Extract Snippets**: Use `pdf` tool to extract images/regions of the core questions identified in `05_教材原题与习题原题索引.md` (CH13-TB-13-1 to 13-11, CH13-SCH-J1 to B1).
3.  **Update Resource Index**: Ensure `outputs/chapter_resource_index.md` is updated with specific page numbers and screenshot links.

### Phase 2: Refine Question Database & Templates (P1 & P2)
1.  **Verify Database**: Check `05_教材原题与习题原题索引.md` for completeness.
2.  **Generate Trap/Template Table**: Create `outputs/第13章_易错陷阱与题型模板.md`.
    - Content: Waveform symmetry, RMS calculation for different frequencies, Average power, Filter design.

### Phase 3: Page Generation (P3 - Draft)
1.  **Design Layout**: Plan ~6-8 pages following the existing visual style (purple blocks, red reminders) but with embedded original snippets.
2.  **Generate Pages (image2)**:
    - Page 1: Concepts, Fourier Series, Symmetry.
    - Page 2: RMS, Average Power formulas with original examples.
    - Page 3-5: Step-by-step solutions for calculation types (CH13-TB-13-4, 13-6, 13-10).
    - Page 6: School-specific typical problems (SCH-B1).
3.  **User Review**: Present generated `.png` pages for user feedback.

### Phase 4: Final PDF Composition
1.  **LaTeX Script**: Write/Update `scripts/build_ch13_latex_v4.py` to synthesize the `.png` pages into a final PDF.
2.  **Verification**: Render and check for formula accuracy, image clarity, and layout issues.

## Verification Section
1.  **Visual Check**: Verify that `source_snippets/` contains clear images of original book/PPT problems.
2.  **Accuracy Check**: Ensure no "adding phasers of different frequencies" occurs in the explanations.
3.  **Formatting Check**: Confirm solving steps follow SOP-01 (Answer first -> Given -> Formula -> Calculation -> Result).
4.  **End-to-End**: Run LaTeX compilation and open the final PDF to verify page order and quality.
