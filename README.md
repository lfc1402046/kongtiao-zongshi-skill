# 空调安装与诊断专家技能包

一位拥有数十年实战经验的空调安装老师傅，以系统思维、预见性和场景适配为核心，为用户提供专业、务实、可操作的安装与诊断指导。

## 安装方法

将此技能包放置在 OpenClaw 的 skills 目录下：
```
%USERPROFILE%\.qclaw\skills\kongtiao-zongshi\
```

或使用 .skill 文件导入。

## 功能覆盖

- ✅ 安装方案设计（选点定址、排水规划）
- ✅ 安装工艺指导（抽真空、铜管焊接、支架固定）
- ✅ 故障诊断（制冷差、漏水、噪音）
- ✅ 使用保养建议
- ✅ 制冷量计算工具

## 目录结构

```
kongtiao-zongshi/
├── SKILL.md                    # 主技能文件
├── references/
│   ├── brand-standards/        # 品牌技术标准（格力、美的、大金）
│   └── case-library.md         # 典型安装案例库
└── scripts/
    └── calculate_cooling_capacity.py  # 制冷量计算器
```

## 使用示例

**问**：我家外墙是玻璃幕墙，室外机没地方放，怎么办？

**空调宗师**：这是个典型难题。核心是不能让机器"悬空"或"闷烧"。我有上中下三策...

详见 SKILL.md 中的完整示例。

## 许可证

MIT License
