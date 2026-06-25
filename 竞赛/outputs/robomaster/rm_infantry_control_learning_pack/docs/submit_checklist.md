# 提交检查清单

## 结论

提交前要让评审一眼看出三件事：结构清楚、功能有边界、作者真的理解。

## 必交内容

- STM32 工程源码
- `README.md`
- `docs/design.md`
- `docs/test_plan.md`
- `docs/reflection.md`
- Git 仓库链接
- 压缩包兜底

## README 必写

- 项目目标
- 功能完成度
- 文件结构
- 按键说明
- 安全保护说明
- 硬件接入说明
- 未完成/待实车验证项

## Git 提交建议

不要一次性提交全部代码。建议提交记录：

```text
init stm32 hal project
add pid module
add remote key state machine
add chassis kinematics and speed pid
add gimbal angle control and pitch limit
add robot mode and safety stop
add docs and test record
```

## 压缩包命名

按题目要求命名为：

```text
25+学院简称+姓名.zip
```

例如：

```text
25电科张三.zip
```

Source: `C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:86`
