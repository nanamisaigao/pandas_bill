import matplotlib.pyplot as plt
from pathlib import Path
import sys
import numpy as np

import analyze

Path("figures").mkdir(exist_ok=True)
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

COLOR_ACTUAL = "#4C78A8"
COLOR_BUDGET = "#F58518"
COLOR_CATS = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2"]

def line_chart(merged):
    #2024年月度花费趋势折线图
    plt.close("all")
    plt.figure(figsize=(10, 5))
    plt.plot(merged.index,merged["实际"],marker="o")
    plt.title("2024 年月度花费趋势")
    plt.xlabel("月份")
    plt.ylabel("实际花费")
    plt.xticks(rotation=45)
    plt.grid(axis="y", alpha=0.5)
    plt.tight_layout()
    plt.savefig("figures/monthly_trend.png", dpi=150, bbox_inches="tight")
    plt.show()

def bar_chart(merged):
    #2024 年月度实际 vs 预算柱状图。
    plt.close("all")
    x=np.arange(len(merged.index))
    width=0.35
    plt.bar(x - width / 2, merged["实际"], width, label="实际",color=COLOR_ACTUAL)
    plt.bar(x + width / 2, merged["预算"], width, label="预算",color=COLOR_BUDGET)
    plt.xticks(x,merged.index,rotation=45,ha="right")
    plt.title("2024 年月度实际 vs 预算柱状图。")
    plt.xlabel("月份")
    plt.ylabel("金额")
    plt.legend()
    plt.grid(axis="y", alpha=0.5)
    plt.tight_layout()
    plt.savefig("figures/actual_vs_budget.png", dpi=150, bbox_inches="tight")
    plt.show()

def pie_chart(pivot):
    #类别占比饼图
    plt.close("all")
    plt.figure(figsize=(8, 8))
    plt.pie(
        pivot.sum().values,
        labels=pivot.sum().index,
        autopct="%1.1f%%",
        startangle=90,
        colors=COLOR_CATS,
    )

    plt.title("2024 年各类别花费占比。")
    plt.tight_layout()
    plt.savefig("figures/category_pie.png", dpi=150, bbox_inches="tight")
    plt.show()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/cleaned.csv"
    df = analyze.load(path)
    pivot,total,pct,merged =analyze.monthly_report(df)
    line_chart(merged)
    bar_chart(merged)
    pie_chart(pivot)


if __name__ == "__main__":
    main()