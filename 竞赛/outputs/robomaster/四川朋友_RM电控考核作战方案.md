# 四川朋友 RM 电控软件组考核作战方案

## 结论

这份作业不适合追求“大而全”，最优策略是做一个能跑通、结构清楚、能解释清楚的最小电控工程，然后用 README、Git 提交记录和演示材料证明自己有工程习惯。

优先级：

1. 必须完成：模块化工程、任务调度、底盘运动学、云台目标角控制、按键模拟输入、STOP/NORMAL 模式、安全保护。
2. 尽量完成：PID 模块、电机编码器速度闭环、L1 呼吸灯、L2 模式灯、Pitch 限位。
3. 加分完成：Git 仓库提交、跟随模式、小陀螺模式、串口目标角输入、陀螺仪角度反馈说明或实测。

原因：题目明确“不要求全部做完”，但强调“代码中会体现个人的思想”。所以评审最可能看的是架构意识、控制闭环意识、安全意识、学习过程，而不是堆一堆不可验证功能。

## 任务拆解

### 1. 工程结构

建议文件结构：

```text
Core/
  Inc/
    app.h
    chassis.h
    gimbal.h
    remote.h
    pid.h
    robot_def.h
  Src/
    app.c
    chassis.c
    gimbal.c
    remote.c
    pid.c
    main.c
README.md
docs/
  architecture.md
  test_record.md
```

最关键原则：

- `main.c` 只做 HAL 初始化和调用 `App_Init()`、`App_Loop()`。
- 控制逻辑放到 `app.c` 的 `Control_Task()`，内部调用 `Remote_Update()`、`Chassis_Control()`、`Gimbal_Control()`。
- 每个模块暴露少量接口，不互相乱改全局变量。

### 2. 模式状态机

至少实现两个整车模式：

- `ROBOT_STOP`：所有电机输出为 0。
- `ROBOT_NORMAL`：底盘和云台正常响应按键。

建议额外做两个底盘模式：

- `CHASSIS_INDEPENDENT`：底盘方向就是车体正方向。
- `CHASSIS_SPIN`：按下 `key1` 后底盘保持固定角速度旋转。

如果时间足够，再做：

- `CHASSIS_FOLLOW_GIMBAL`：长按 `key1`，用 yaw 角误差给底盘角速度，让底盘正方向追云台朝向。

### 3. 底盘控制

四轮全向轮 X 型底盘可以先抽象为速度分配：

```text
w1 = +vx - vy - wz * K
w2 = +vx + vy + wz * K
w3 = -vx + vy - wz * K
w4 = -vx - vy + wz * K
```

提交时要说明：

- `vx`：车体前后速度。
- `vy`：车体左右速度。
- `wz`：车体旋转角速度。
- `K`：底盘半径/几何系数，先用宏定义，后续实车标定。

如果没有实车，也要保留“目标轮速”和“反馈轮速”的接口，体现后续接编码器闭环的设计。

### 4. PID 闭环

建议写通用 `pid.c/pid.h`：

- `PID_Init()`
- `PID_Calc()`
- `PID_Reset()`
- 输出限幅
- 积分限幅

底盘电机速度闭环：

```text
target_speed -> PID -> pwm_output
encoder_speed -> feedback
```

云台角度闭环：

```text
target_angle -> PID -> motor_output
gyro_angle -> feedback
```

注意：题目要求云台角度反馈用陀螺仪，不要用电机编码器替代。没有硬件时，可以把 `Gimbal_GetYawAngle()`、`Gimbal_GetPitchAngle()` 写成接口，并在 README 说明当前用模拟值/占位值，真实上车时替换为 IMU 数据。

### 5. 遥控输入

按键设计：

- `key1`：短按切换小陀螺模式，长按进入跟随模式。
- `key2`：短按 yaw 目标角加一次，长按连续增加。
- `key3`：短按 pitch 目标角加一次，长按连续增加。
- `key_stop`：急停/解除急停。

必须做按键消抖和短按/长按识别。这个点很容易体现“个人思想”，比单纯写 if 判断更像工程代码。

进阶串口协议可以作为加分项处理，不建议第一版就卡在这里：

- 控制信息数据包：包头 `0x0a 0x05`，字段 `Vx=0x01`、`Vy=0x02`、云台转速 `0x03`、校验位 `0x06`，包尾 `0x05 0x0a`。
- 云台电机反馈数据包：包头 `0x0a`，字段为电机实际速度、电机实际角度，包尾 `0x05`。
- 云台电机控制数据包：包头 `0x0a`，字段为电机转速控制量，包尾 `0x05`。
- 实现方式：先写 `Remote_ParseUartFrame()`，校验包头/包尾/校验位，再把解析结果写入 `remote_cmd_t`，不要让串口中断直接改底盘和云台输出。

### 6. 安全保护

优先实现三件事：

- 电机输出限幅：所有 PWM/CAN 电流输出都经过 `Limit()`。
- Pitch 角度限位：目标角先限到 `[-20, 30]`。
- 急停模式：任何状态下触发后立即进入 `ROBOT_STOP`。

如果要更进一步：

- 遥控超时保护：超过指定时间没有输入，自动停机。
- 堵转保护：目标输出很大但编码器速度长期接近 0，降低输出或停机。

## 7 天冲刺安排

第 1 天：

- 建 STM32 HAL 工程或整理已有模板。
- 建好 `chassis/gimbal/remote/pid/app` 文件。
- 写 README 的任务理解和模块图。

第 2 天：

- 完成按键输入、短按/长按、模式状态机。
- 完成 L1/L2 指示灯逻辑。

第 3 天：

- 写底盘正逆运动学。
- 做目标轮速限幅。
- 在串口或调试变量里打印/观察轮速。

第 4 天：

- 写 PID 模块。
- 把底盘速度闭环接口接起来，即使暂时用模拟反馈，也要结构完整。

第 5 天：

- 写云台 yaw/pitch 目标角控制。
- 做 Pitch 限位。
- 预留 IMU 角度反馈接口。

第 6 天：

- 加急停、输出限幅、遥控超时。
- 补注释，清理 `main.c`，避免逻辑堆积。

第 7 天：

- 写 README、测试记录、功能完成表。
- 用 Git 提交，发仓库链接；同时准备压缩包兜底。

## 提交物清单

必须有：

- STM32 HAL 工程源码。
- `README.md`：功能说明、模块结构、按键说明、完成度说明。
- `docs/architecture.md`：控制流程和状态机说明。
- `docs/test_record.md`：每个功能怎么测、测到什么现象。
- Git 仓库链接，争取加 10 分。

README 建议写清楚：

- 已完成：模块调度、底盘运动学、按键输入、STOP/NORMAL、安全保护等。
- 部分完成：PID 接口完成，真实编码器/IMU 需接硬件验证。
- 未完成但已预留：串口视觉数据、跟随模式参数实车整定。

## 面试/答辩表达

可以这样说：

> 我没有把所有逻辑堆在 main.c，而是按底盘、云台、遥控、PID、任务调度拆开。因为 RM 电控后期一定会多人协作和频繁调参，如果架构不清楚，功能越多越难维护。

> 我优先做了 STOP、输出限幅、Pitch 限位，是因为机器人电控不是先追求能动，而是先保证失控时能停。这个也是比赛现场最重要的底线。

> 底盘我先用 X 型全向轮运动学把 vx、vy、wz 转成四轮目标速度，再通过 PID 接编码器反馈。这样即使现在没有完整硬件，也能保证控制链路是可扩展的。

## 风险提醒

- 不要直接复制网上完整 RM 工程，风格和硬件依赖会露馅。
- 不要承诺已经实测真实电机/IMU，除非确实测过。
- 不要只交压缩包，Git 链接明确加分。
- 不要把完成度写满，诚实写“已完成/待实车验证/后续扩展”，反而更可信。

## 下一步

如果要继续推进，下一步应该直接建工程骨架或审查他现有代码。优先看三个文件：`main.c`、`chassis.c`、`gimbal.c`。如果现在还没有代码，就先用 CubeMX 建一个最小 HAL 工程，再按上面的文件结构填逻辑。

## 来源

- 作业要求基于 STM32 HAL 完成简易步兵电控程序，并考察架构、控制流程、运动控制、PID、状态机、通信和保护：`C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:11`
- 题目要求模块包括底盘、云台、遥控输入和安全保护：`C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:17`
- 推荐文件结构包含 `chassis/gimbal/remote/pid/main`：`C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:32`
- 底盘要求全向轮正逆运动学、编码器闭环和独立/小陀螺/跟随模式：`C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:43`
- 云台要求 yaw/pitch 目标角跟随、Pitch 限位、PID 输出和陀螺仪反馈：`C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:54`
- 安全保护至少实现输出限幅、Pitch 限位、急停中的两个：`C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:66`
- 进阶要求强调任务调度和不能把逻辑堆在 `main`：`C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:71`
- 提交 Git 仓库链接可加 10 分，实践时间为 2026.6.1-2026.6.15，不要求全部做完：`C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:85`
