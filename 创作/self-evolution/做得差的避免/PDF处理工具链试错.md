# 做得差：PDF处理工具链反复试错（2026-05-27）

> 一个扫描型PDF的任务，花了两轮对话、10+次工具切换才完成。
> 这不是"最终完成了"的问题，是"过程完全失控"的问题。

---

## 错误路径（已验证的死路）

```
pdfplumber提取 → 空（图片型PDF）
→ Read工具视觉识别 → 不支持
→ PDF转图片 + easyocr → easyocr全局包损坏
→ pip install easyocr → pip 24.0 metadata损坏
→ pip install paddleocr → 同上
→ pip install tesseract → 未安装且无法安装
→ markitdown MCP → pip安装失败
→ pip install --upgrade pip → 成功但easyocr仍装不上
→ 清理缓存重装 → 成功
→ venv安装easyocr → 成功
→ 最终OCR识别 → 成功
```

**总耗时**：两轮对话，中间断开重来。

---

## 正确路径（应该从一开始就走的）

```
pdfplumber提取 → 空 → 判断为图片型PDF
→ python -c "import easyocr" → 失败
→ python -m venv .venv && .venv\Scripts\pip install easyocr
→ 渲染PDF为图片（PyMuPDF 250 DPI）
→ OCR识别 → 统计
```

**预期耗时**：单轮对话 5 分钟内完成。

---

## 三条通用避坑规则

### 1. 环境损坏一票否决
发现 `pip metadata missing` 或 `ImportError: cannot import name` → **立即切换 venv**。
不要在损坏的全局环境上尝试修复，那是无底洞。

### 2. 先检查再动手
任何工具调用前，花 10 秒验证可用性：
```bash
python -c "import easyocr; print('OK')"
```
不可用 → 立即安装到 venv → 不可用 → 换方案。≤3 次。

### 3. 退出判据必须预设
开始前说清楚：「如果 X 不行，我就走 Y 路径」。
不要"试试看"心态——每个"试试"都是在浪费用户的信任。

---

## 关联

- 教训编号：lessons.md#教训004
- 模式编号：patterns.md#Pattern-004
- 负结果日志：项目 negative-results.md
- 跨工作区知识库：knowledge/knowledge.md（PDF处理决策树）
