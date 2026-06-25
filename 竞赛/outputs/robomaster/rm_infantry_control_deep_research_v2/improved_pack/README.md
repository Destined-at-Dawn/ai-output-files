# 简易步兵机器人电控系统学习包

## 结论

这是一份面向 STM32 HAL 工程的 RoboMaster 简易步兵电控参考实现。它不是直接绑定某块板子的完整 CubeMX 工程，而是一个清晰的应用层框架：硬件相关内容集中在 `bsp_port.c`，控制逻辑按底盘、云台、遥控、PID、任务调度拆开。

最适合的使用方式：

1. 先读 `docs/tutorial_step_by_step.md`，理解每个模块为什么存在。
2. 把 `Core/Inc` 和 `Core/Src` 复制进自己的 STM32Cube 工程。
3. 按自己的板子改 `bsp_port.c`，接上按键、PWM/CAN、编码器、IMU。
4. 按 `docs/test_plan.md` 一项一项验证。
5. 最后改 README 和心得，把自己的调试过程写进去。

## 文件结构

```text
Core/
  Inc/
    app.h
    bsp_port.h
    c620_can.h
    chassis.h
    gimbal.h
    pid.h
    remote.h
    robot_def.h
    safety.h
  Src/
    app.c
    bsp_port.c
    c620_can.c
    chassis.c
    gimbal.c
    pid.c
    remote.c
    safety.c
docs/
  technical_report.md
  design.md
  code_walkthrough.md
  tutorial_step_by_step.md
  test_plan.md
  reflection.md
  submit_checklist.md
main_integration_example.c
```

## 已覆盖功能

- 分层架构：`app / remote / chassis / gimbal / pid / bsp_port`
- 循环任务调度：`App_Loop()` 内部按周期调用控制任务
- 整车模式：`ROBOT_STOP`、`ROBOT_NORMAL`
- 底盘模式：独立模式、小陀螺模式、跟随云台模式
- X 型四轮全向底盘运动学
- 电机速度 PID 接口
- 云台 yaw/pitch 目标角控制
- Pitch 角度限位
- 急停、输出限幅、遥控超时保护接口
- 默认平移速度为 0，不会在解除急停后自动前进
- 按键短按、长按、长按连发
- 串口协议解析函数框架
- C620/M3508 CAN 电调协议打包与反馈解析模块
- 独立 `safety` 安全状态机
- L1 呼吸灯、L2 模式灯接口

## 需要自己接入的硬件

`Core/Src/bsp_port.c` 里所有函数都是硬件适配层：

- `BSP_GetTickMs()`
- `BSP_ReadKey()`
- `BSP_SetMotorOutput()`
- `BSP_GetMotorSpeed()`
- `BSP_GetYawAngleDeg()`
- `BSP_GetPitchAngleDeg()`
- `BSP_SetLedL1()`
- `BSP_SetLedL2()`

如果暂时没有实车，可以先用串口打印或调试变量观察目标速度、目标角度和输出值。

## v2 调研迭代新增点

- 参考 RoboMaster 官方 C 型开发板资料，保留 IMU、CAN、UART、PWM、DBUS 等硬件接入位置。
- 参考 RoboMaster C620 官方用户手册，新增 0x200/0x1FF 电流控制帧打包和 0x201-0x208 反馈帧解析。
- 将安全逻辑从 `app.c` 中抽出为 `safety.c`，便于后续增加遥控丢失、堵转、过温、过流等保护。
- 文档新增 `research_report.md`，说明调研来源、设计取舍和 v1 到 v2 的迭代原因。

## 提交建议

提交时不要声称“所有硬件已经实测”，除非确实接过电机和 IMU。更稳妥的表达：

- 已完成软件架构、运动学、状态机、PID 接口、安全保护。
- 已预留编码器和 IMU 反馈接口。
- 当前硬件适配层需要根据实际开发板引脚和电机驱动方式配置。

Source: `C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:11`
