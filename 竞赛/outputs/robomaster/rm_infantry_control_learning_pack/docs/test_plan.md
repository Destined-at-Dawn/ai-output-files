# 测试计划

## 结论

测试顺序必须从低风险到高风险：先验证变量和 LED，再验证电机悬空，最后才落地跑车。

## 静态检查

- `main.c` 里只保留初始化和 `App_Loop()`。
- `chassis.c` 不直接调用 GPIO。
- `gimbal.c` 不直接调用 GPIO。
- `remote.c` 不直接控制电机。
- 所有硬件访问集中在 `bsp_port.c`。

## 功能检查

1. L1 呼吸灯
   - 现象：上电后亮度周期变化。
   - 失败排查：TIM PWM、GPIO 复用、`BSP_SetLedL1()`。

2. L2 模式灯
   - 现象：独立模式约 1Hz，小陀螺约 2Hz。
   - 失败排查：`cmd->chassis_mode` 是否切换。

3. 急停
   - 现象：按 stop 后所有电机输出为 0。
   - 失败排查：`ROBOT_STOP` 是否传到 `Chassis_Control()` 和 `Gimbal_Control()`。

4. 底盘运动学
   - 现象：修改 `vx/vy/wz` 后四个 `wheel_target` 按公式变化。
   - 失败排查：轮子编号是否和实际安装一致。

5. 电机 PID
   - 现象：目标速度大于反馈速度时输出为正，接近目标后输出变小。
   - 失败排查：编码器方向、PID 参数、输出限幅。

6. 云台 Pitch 限位
   - 现象：反复按 key3，目标角不超过 30 度。
   - 失败排查：是否对目标角限幅，而不是只对输出限幅。

7. 云台 PID
   - 现象：目标角变化后，输出方向推动云台靠近目标。
   - 失败排查：IMU 角度方向、yaw 角 wrap、pitch 电机方向。

8. 遥控超时
   - 现象：接入真实遥控器后，通信中断会进入停机保护。
   - 失败排查：`valid` 和 `last_update_ms` 是否只在收到真实遥控数据时更新。

## README 里建议记录的测试结果

- 测试日期
- 测试硬件
- 已验证功能
- 未验证原因
- 下一步计划

Source: `C:/Temp/codex_rm_assignment/rm_control_assignment_extracted.md:66`
