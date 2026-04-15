#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
空调制冷量计算器
根据房间参数计算所需制冷量，并给出机型建议
"""

import sys
import json

def calculate_cooling_capacity(area, direction="north", floor_type="middle", window_ratio=0.3, insulation="normal"):
    """
    计算所需制冷量
    
    参数:
        area: 房间面积 (㎡)
        direction: 朝向 (north/south/east/west)
        floor_type: 楼层类型 (top/middle/bottom)
        window_ratio: 窗户占比 (0-1)
        insulation: 保温情况 (good/normal/poor)
    
    返回:
        dict: 包含制冷量、机型建议等信息
    """
    
    # 基础制冷量 (W/㎡)
    base_capacity_per_area = 180
    
    # 朝向系数
    direction_factors = {
        "north": 1.0,
        "south": 1.1,
        "east": 1.05,
        "west": 1.15
    }
    
    # 楼层系数
    floor_factors = {
        "top": 1.2,      # 顶层受屋顶热辐射
        "middle": 1.0,
        "bottom": 0.95   # 底层相对凉爽
    }
    
    # 保温系数
    insulation_factors = {
        "good": 0.9,
        "normal": 1.0,
        "poor": 1.15
    }
    
    # 窗户影响系数 (窗户越大，热负荷越高)
    window_factor = 1 + (window_ratio - 0.3) * 0.5
    
    # 计算总制冷量
    total_factor = (
        direction_factors.get(direction, 1.0) *
        floor_factors.get(floor_type, 1.0) *
        insulation_factors.get(insulation, 1.0) *
        window_factor
    )
    
    capacity_w = area * base_capacity_per_area * total_factor
    
    # 机型建议
    def get_unit_suggestion(capacity_w):
        """根据制冷量推荐机型"""
        # 常见机型制冷量范围 (W)
        units = [
            {"name": "1P", "min": 2300, "max": 2600, "suitable_area": "10-15㎡"},
            {"name": "1.5P", "min": 3200, "max": 3600, "suitable_area": "15-22㎡"},
            {"name": "2P", "min": 4500, "max": 5200, "suitable_area": "22-30㎡"},
            {"name": "2.5P", "min": 6000, "max": 6500, "suitable_area": "30-40㎡"},
            {"name": "3P", "min": 7000, "max": 7500, "suitable_area": "40-50㎡"},
        ]
        
        for unit in units:
            if capacity_w <= unit["max"]:
                return unit
        
        # 超大空间
        return {"name": "5P或中央空调", "min": 12000, "max": 99999, "suitable_area": "50㎡以上"}
    
    unit = get_unit_suggestion(capacity_w)
    
    return {
        "area": area,
        "direction": direction,
        "floor_type": floor_type,
        "window_ratio": window_ratio,
        "insulation": insulation,
        "calculated_capacity_w": round(capacity_w),
        "calculated_capacity_kw": round(capacity_w / 1000, 2),
        "adjustment_factor": round(total_factor, 2),
        "recommended_unit": unit["name"],
        "unit_capacity_range": f"{unit['min']}-{unit['max']}W",
        "suitable_area": unit["suitable_area"],
        "notes": []
    }


def main():
    """交互式计算"""
    print("=" * 50)
    print("空调制冷量计算器")
    print("=" * 50)
    
    try:
        area = float(input("\n请输入房间面积(㎡): "))
        
        print("\n朝向选择:")
        print("  1-北向  2-南向  3-东向  4-西向")
        dir_choice = input("请选择(默认1): ").strip() or "1"
        direction_map = {"1": "north", "2": "south", "3": "east", "4": "west"}
        direction = direction_map.get(dir_choice, "north")
        
        print("\n楼层类型:")
        print("  1-顶层  2-中间层  3-底层")
        floor_choice = input("请选择(默认2): ").strip() or "2"
        floor_map = {"1": "top", "2": "middle", "3": "bottom"}
        floor_type = floor_map.get(floor_choice, "middle")
        
        print("\n窗户占比:")
        print("  1-小(≤20%)  2-中(30%左右)  3-大(≥50%)")
        window_choice = input("请选择(默认2): ").strip() or "2"
        window_map = {"1": 0.2, "2": 0.3, "3": 0.5}
        window_ratio = window_map.get(window_choice, 0.3)
        
        print("\n保温情况:")
        print("  1-好(有隔热层)  2-一般  3-差(老房子)")
        insul_choice = input("请选择(默认2): ").strip() or "2"
        insul_map = {"1": "good", "2": "normal", "3": "poor"}
        insulation = insul_map.get(insul_choice, "normal")
        
        # 计算
        result = calculate_cooling_capacity(
            area, direction, floor_type, window_ratio, insulation
        )
        
        # 输出结果
        print("\n" + "=" * 50)
        print("计算结果")
        print("=" * 50)
        print(f"房间面积: {result['area']}㎡")
        print(f"调整系数: {result['adjustment_factor']}")
        print(f"所需制冷量: {result['calculated_capacity_w']}W ({result['calculated_capacity_kw']}kW)")
        print(f"推荐机型: {result['recommended_unit']}")
        print(f"机型制冷量范围: {result['unit_capacity_range']}")
        print(f"适用面积: {result['suitable_area']}")
        
        # 特殊情况提示
        if result['adjustment_factor'] > 1.3:
            print("\n⚠️ 注意: 您的房间热负荷较高，建议:")
            if direction == "west":
                print("  - 西晒严重，考虑加装遮阳帘")
            if floor_type == "top":
                print("  - 顶层受热辐射大，如有条件做屋顶隔热")
        
        print("\n" + "=" * 50)
        
    except ValueError as e:
        print(f"输入错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # 支持命令行参数模式
    if len(sys.argv) > 1:
        # 简化命令行调用: python script.py 面积 [朝向] [楼层] [窗户占比] [保温]
        try:
            area = float(sys.argv[1])
            direction = sys.argv[2] if len(sys.argv) > 2 else "north"
            floor_type = sys.argv[3] if len(sys.argv) > 3 else "middle"
            window_ratio = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3
            insulation = sys.argv[5] if len(sys.argv) > 5 else "normal"
            
            result = calculate_cooling_capacity(
                area, direction, floor_type, window_ratio, insulation
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"参数错误: {e}")
            sys.exit(1)
    else:
        # 交互模式
        main()
