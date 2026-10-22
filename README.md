# pb-jo：从零重写 `jo`（命令行 JSON 生成器）

**难度：medium**　语言：C　上游：[jpmens/jo](https://github.com/jpmens/jo) @ `2cc4761`

agent 拿到一个只能执行、不能读取的 `jo` 二进制文件，再加上使用文档。它要用任意语言重新实现一个行为完全相同的程序，并提供 `compile.sh`，编译产物是 `./executable`。

## 文件结构

```
task.yaml                 元数据（上游 commit、难度、gold 哈希）
instruction.md            给 agent 的题面
original/build.sh         怎么编译上游源码（pbkit 和 Dockerfile 都用它）
environment/Dockerfile    无菌室镜像：二进制设为 0111 权限，非 root 用户，不含源码
environment/docs/         agent 能看到的文档
tests/                    隐藏测试（pytest，1158 个），由 pbkit 生成
tests.json                测试分组
authoring/cases.py        测试输入设计（质量核心）
authoring/report.md       过滤统计
authoring/coverage/       覆盖率汇总和未覆盖行
authoring/validation.md   在真实题目镜像里的端到端验证结果
```