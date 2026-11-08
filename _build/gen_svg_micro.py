#!/usr/bin/env python3
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgfactory import Graph

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
BLUE, RED, GREEN, GRAY, ORANGE = "#2563eb", "#dc2626", "#16a34a", "#6b7280", "#ea580c"


def save(name, g):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(g.render())
    print("wrote", name)


# ch04 供给与需求：Qd=60-2P，Qs=2P-20，均衡 P=20 Q=20
def ch04():
    g = Graph(xmax=60, ymax=34, title="第 4 章示例：奶茶市场")
    g.curve([(40, 10), (30, 15), (20, 20), (10, 25), (0, 30)], BLUE, "需求 D", label_at=(2, 28))
    g.curve([(0, 10), (10, 15), (20, 20), (30, 25), (40, 30)], RED, "供给 S", label_at=(38, 31))
    g.mark(20, 20, "", "#111827")
    g.note(21.6, 21.2, "均衡 E 20 元 20 杯", "#111827")
    g.mark(20, 20, "", "#111827", "dashv")
    g.mark(20, 20, "", "#111827", "dashh")
    g.note(50, 21, "P*=20 元", "#111827")
    g.note(50, 15, "Q*=20 杯", "#111827")
    g.note(3, 32.6, "交点即均衡：20 元、20 杯", "#6b7280")
    save("ch04_ds", g)


# ch05 弹性与总收益：同一条需求曲线，P=20 与 P=25 的收益矩形
def ch05():
    g = Graph(xmax=60, ymax=34, title="第 5 章示例：总收益 = P × Q")
    g.curve([(40, 10), (30, 15), (20, 20), (10, 25), (0, 30)], BLUE, "需求 D", label_at=(2, 28))
    g.area([(0, 0), (20, 0), (20, 20), (0, 20)], ORANGE, 0.25, "TR=400 元")
    g.area([(0, 20), (10, 20), (10, 25), (0, 25)], GREEN, 0.3, "TR=250 元")
    g.mark(20, 20, "P=20, Q=20", "#111827")
    g.mark(10, 25, "P=25, Q=10", "#111827")
    save("ch05_tr", g)


# ch06 价格上限：上限 15 元 -> 短缺 10 杯
def ch06():
    g = Graph(xmax=60, ymax=34, title="第 6 章示例：奶茶价格上限 15 元")
    g.curve([(40, 10), (30, 15), (20, 20), (10, 25), (0, 30)], BLUE, "需求 D", label_at=(2, 28))
    g.curve([(0, 10), (10, 15), (20, 20), (30, 25), (40, 30)], RED, "供给 S", label_at=(38, 31))
    g.curve([(0, 15), (60, 15)], GRAY, "价格上限", dash=True, label_at=(52, 15))
    g.mark(30, 15, "Qd=30", "#111827", "dashv")
    g.mark(10, 15, "Qs=10", "#111827", "dashv")
    g.arrow(11, 13.3, 29, 13.3, RED)
    g.note(16, 12.4, "短缺 20 杯", RED)
    save("ch06_ceiling", g)


# ch06 税收：向卖者征 6 元，楔子（买者 23、卖者 17、数量 14）
def ch06_tax():
    g = Graph(xmax=60, ymax=34, title="向卖者征 6 元税：价格楔子")
    g.curve([(40, 10), (30, 15), (20, 20), (10, 25), (0, 30)], BLUE, "需求 D", label_at=(2, 28))
    g.curve([(0, 10), (10, 15), (20, 20), (30, 25), (40, 30)], RED, "原供给 S", label_at=(38, 30.6))
    g.curve([(0, 16), (14, 23), (20, 26)], GREEN, "税后供给 S′", label_at=(21, 26.6))
    g.mark(14, 23, "", "#111827", "dashh")
    g.mark(14, 17, "", "#111827", "dashh")
    g.mark(14, 23, "", "#111827", "dashv")
    g.note(15.4, 24.6, "买者付 23 元", "#111827")
    g.note(15.4, 15.2, "卖者得 17 元", "#111827")
    g.note(15.4, 13.4, "数量 14", "#6b7280")
    g.note(1, 32.6, "楔子 6 元：买者多付、卖者少得", "#6b7280")
    save("ch06_tax", g)


# ch07 消费者剩余与生产者剩余
def ch07():
    g = Graph(xmax=60, ymax=34, title="第 7 章示例：总剩余最大")
    g.curve([(40, 10), (30, 15), (20, 20), (10, 25), (0, 30)], BLUE, "需求 D", label_at=(2, 28))
    g.curve([(0, 10), (10, 15), (20, 20), (30, 25), (40, 30)], RED, "供给 S", label_at=(38, 31))
    g.area([(0, 20), (20, 20), (0, 30)], BLUE, 0.3, "消费者剩余")
    g.area([(0, 10), (20, 20), (0, 20)], RED, 0.3, "生产者剩余")
    g.mark(20, 20, "均衡", "#111827")
    g.mark(20, 20, "", "#111827", "dashh")
    save("ch07_surplus", g)


# ch08 赋税的无谓损失：税 6 元，DWL 三角
def ch08():
    g = Graph(xmax=60, ymax=34, title="第 8 章示例：6 元税的无谓损失")
    g.curve([(40, 10), (30, 15), (20, 20), (10, 25), (0, 30)], BLUE, "需求 D", label_at=(2, 28))
    g.curve([(0, 10), (10, 15), (20, 20), (30, 25), (40, 30)], RED, "供给 S", label_at=(38, 30.6))
    g.curve([(0, 16), (14, 23), (20, 26)], GREEN, "税后供给 S′", label_at=(21, 26.6))
    g.area([(14, 23), (14, 17), (20, 20)], ORANGE, 0.5)
    g.area([(0, 17), (14, 17), (14, 23), (0, 23)], GRAY, 0.22)
    g.mark(14, 23, "", "#111827", "dashh")
    g.mark(14, 17, "", "#111827", "dashh")
    g.mark(20, 20, "", "#111827", "cross")
    g.note(1, 24.6, "税收收入 84", "#111827")
    g.note(21.4, 22.4, "无谓损失 18", "#111827")
    g.note(10.6, 24.2, "买者付 23", "#111827")
    g.note(10.6, 17.4, "卖者得 17", "#111827")
    g.note(1, 32.6, "交易量 20 → 14 杯", "#6b7280")
    save("ch08_dwl", g)


# ch09 关税：世界价格 15，关税后 18，进口 20 -> 8
def ch09():
    g = Graph(xmax=60, ymax=34, title="第 9 章示例：进口国加征 3 元关税")
    g.curve([(40, 10), (30, 15), (20, 20), (10, 25), (0, 30)], BLUE, "国内需求 D", label_at=(1, 28))
    g.curve([(0, 10), (10, 15), (20, 20), (30, 25), (40, 30)], RED, "国内供给 S", label_at=(38, 30.6))
    g.curve([(0, 15), (60, 15)], GRAY, "世界价格 15", dash=True, label_at=(44, 14.2))
    g.curve([(0, 18), (60, 18)], ORANGE, "关税后 18", dash=True, label_at=(44, 18.6))
    g.mark(10, 15, "", GRAY, "dashv")
    g.mark(30, 15, "", GRAY, "dashv")
    g.mark(16, 18, "", ORANGE, "dashv")
    g.mark(24, 18, "", ORANGE, "dashv")
    g.note(11, 13.6, "进口 20 杯", "#111827")
    g.note(17, 19.4, "进口 8 杯", "#111827")
    g.note(15.6, 32.6, "自由贸易时消费者多买 20 杯，关税后只剩 8 杯", "#6b7280")
    save("ch09_tariff", g)


# ch10 负外部性：每杯 4 元外部成本，社会最优 16 杯
def ch10():
    g = Graph(xmax=60, ymax=40, title="第 10 章示例：4 元外部成本下的社会最优")
    g.curve([(40, 10), (30, 15), (20, 20), (10, 25), (0, 30)], BLUE, "需求 D", label_at=(1, 28))
    g.curve([(0, 10), (10, 15), (20, 20), (30, 25)], RED, "私人成本 S", label_at=(24, 26.4))
    g.curve([(0, 14), (8, 18), (16, 22), (24, 26), (30, 29)], GREEN, "社会成本 S′", label_at=(25, 31))
    g.mark(20, 20, "", "#111827", "dashv")
    g.mark(16, 22, "", "#111827", "dashv")
    g.mark(20, 20, "", "#111827", "dashh")
    g.mark(16, 22, "", "#111827", "dashh")
    g.note(21, 21.2, "市场均衡 20 杯", "#111827")
    g.note(8.6, 23.4, "社会最优 16 杯", "#111827")
    g.note(15.4, 38.2, "过量生产 4 杯；每杯 4 元外部成本，无谓损失 8 元", "#6b7280")
    g.area([(16, 22), (16, 18), (20, 20)], ORANGE, 0.4)
    save("ch10_ext", g)


# ch13 成本曲线：MC、ATC、AVC
def ch13():
    g = Graph(xmax=12, ymax=30, xlabel="产量 Q", ylabel="单位成本", title="第 13 章示例：典型成本曲线")
    # MC = 1 + 0.6q^1.4 近似
    mc = [(q, 2 + 0.55 * q ** 1.5) for q in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    atc = [(q, 16 / q + 3 + 0.35 * q) for q in [1.2, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    avc = [(q, 9 / q + 2.2 + 0.42 * q) for q in [1.2, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    g.curve(mc, RED, "MC 边际成本", label_at=(8.4, mc[-2][1]))
    g.curve(atc, BLUE, "ATC 平均总成本", label_at=(3.2, atc[3][1] + 1))
    g.curve(avc, GREEN, "AVC 平均可变成本", label_at=(4.4, avc[4][1] + 0.6))
    g.arrow(2.2, 32, 2.2, 30.5, GRAY) if False else None
    g.note(0.3, 36, "MC 穿过 ATC 与 AVC 的最低点；ATC 在最低点附近达规模最优", GRAY)
    save("ch13_cost", g)


# ch14 完全竞争企业：P=MR=MC
def ch14():
    g = Graph(xmax=12, ymax=30, xlabel="产量 Q", ylabel="价格与成本", title="第 14 章示例：P=MR 水平线与 MC 相交")
    mc = [(q, 4 + 0.6 * q ** 1.6) for q in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    atc = [(q, 20 / q + 6 + 0.3 * q) for q in [1.2, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    g.curve(mc, RED, "MC", label_at=(7.6, mc[-2][1]))
    g.curve(atc, BLUE, "ATC", label_at=(3.2, atc[3][1] + 1.2))
    g.curve([(0, 16), (12, 16)], GREEN, "P=MR=16", label_at=(9.4, 16.6))
    g.mark(6, 16, "Q*=6 时 MR=MC", "#111827", "dashv")
    g.area([(0, 16), (6, 16), (6, 21.2), (0, 21.2)], ORANGE, 0.22, "经济利润为正")
    save("ch14_comp", g)


# ch15 垄断：D: P=30-0.5Q，MR: P=30-Q，MC: P=10+Q
def ch15():
    g = Graph(xmax=40, ymax=34, title="第 15 章示例：垄断者按 MR=MC 定产量，再按需求曲线定价")
    g.curve([(0, 30), (10, 25), (20, 20), (30, 15), (40, 10)], BLUE, "需求 D", label_at=(1, 28))
    g.curve([(0, 30), (15, 15), (30, 0)], RED, "边际收益 MR", label_at=(19, 10))
    g.curve([(0, 10), (10, 20), (20, 30)], GREEN, "边际成本 MC", label_at=(20.4, 30))
    g.area([(10, 25), (10, 20), (13.3, 16.7)], ORANGE, 0.45)
    g.mark(10, 20, "", "#111827", "dashv")
    g.mark(10, 25, "", "#111827", "dashh")
    g.mark(10, 20, "", "#111827")
    g.note(10.8, 26.4, "垄断价 25 元", "#111827")
    g.note(11, 18.6, "MR=MC 处产量 10", "#111827")
    g.note(14.6, 15.4, "无谓损失", "#111827")
    g.note(1, 33, "竞争结果：产量 13.3、价格 16.7；垄断把产量压低 3.3 单位", "#6b7280")
    save("ch15_monopoly", g)


if __name__ == "__main__":
    fns = {k: v for k, v in list(globals().items()) if k.startswith("ch") and callable(v)}
    for name in (sys.argv[1:] or fns.keys()):
        fns[name]()
