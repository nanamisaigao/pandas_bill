import matplotlib.pyplot as plt
from pathlib import Path
import sys
import numpy as np

import analyze

Path("figures").mkdir(exist_ok=True)
# # 折线图：趋势
# plt.plot([1, 2, 3], [4, 5, 6])
#
# # 散点图：两个变量的关系
# plt.scatter([1, 2, 3], [4, 5, 6])
#
# 柱状图：分类对比
# plt.bar(["A", "B", "C"], [10, 20, 15])
# plt.show()

# # 直方图：数值分布
# plt.hist([1, 2, 2, 3, 3, 3, 4])
# 饼图：占比
# plt.pie([30, 50, 20], labels=["A", "B", "C"], autopct="%1.1f%%")


plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def line_chart(merged):
    #2024年月度花费趋势折线图
    plt.close("all")  # 清空之前的画布
    plt.figure(figsize=(10, 5))
    plt.plot(merged.index,merged["实际"],marker="o")
    plt.title("2024 年月度花费趋势")
    plt.xlabel("月份")
    plt.ylabel("实际花费")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("figures/monthly_trend.png", dpi=150, bbox_inches="tight")
    plt.show()

def bar_chart(merged):
    #2024 年月度实际 vs 预算柱状图。
    plt.close("all")
    x=np.arange(len(merged.index))
    width=0.35
    plt.bar(x - width / 2, merged["实际"], width, label="实际")
    plt.bar(x + width / 2, merged["预算"], width, label="预算")
    # merged[["实际","预算"]].plot(kind="bar",figsize=(10, 5))
    plt.xticks(x,merged.index,rotation=45,ha="right")
    plt.title("2024 年月度实际 vs 预算柱状图。")
    plt.xlabel("月份")
    plt.ylabel("金额")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/actual_vs_budget.png", dpi=150, bbox_inches="tight")
    plt.show()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "cleaned.csv"
    df = analyze.load(path)
    pivot,total,pct,merged =analyze.monthly_report(df)
    line_chart(merged)
    bar_chart(merged)


if __name__ == "__main__":
    main()