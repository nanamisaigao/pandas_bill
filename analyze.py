
import pandas as pd
import sys

CATEGORY_ORDER = ["交通", "购物", "娱乐", "餐饮", "其他"]

def load(path):
    return pd.read_csv(path, parse_dates=["日期"])

def monthly_report(df):
    df["月份"]=df["日期"].dt.to_period("M").astype(str)
    monthly_cat=df.groupby(["月份","类别"])["金额"].sum() #变为双索引
    pivot=monthly_cat.unstack(fill_value=0).reindex(columns=CATEGORY_ORDER,fill_value=0) #变成二维横表，且补零
    monthly_total=pivot.sum(axis=1) #计算月份总额
    pct=pivot.div(monthly_total,axis=0)*100
    # 新增：merge 预算
    budget=pd.read_csv("budget.csv")
    total_df= monthly_total.reset_index()
    total_df.columns = ["月份", "实际"]
    merged=pd.merge(total_df,budget,on="月份",how="outer")
    merged["差额"]=merged["实际"]-merged["预算"]
    merged=merged.fillna(0) #填充缺失值
    merged=merged.set_index("月份")
    return pivot,monthly_total,pct,merged



def print_report(pivot,monthly_total,pct,merged):
    # 遍历行（月份）、列（类别），格式化输出
    for month in pivot.index:
        print(f"{month} 总花费：{monthly_total[month]:.1f} 预算：{merged.loc[month,"预算"]:.0f} 差额：{merged.loc[month,"差额"]:.1f}")
        for category in CATEGORY_ORDER:
            print(f"  {category}：{pivot.loc[month,category]:.1f}（{pct.loc[month,category]:.1f}%）")
        print()
    print(f"全年实际：{merged["实际"].sum():.1f}")
    print(f"全年预算：{merged["预算"].sum():.0f}")
    print(f"全年结余：{merged["差额"].sum():.1f}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "cleaned.csv"
    df = load(path)
    pivot,total,pct,merged = monthly_report(df)
    print_report(pivot,total,pct,merged)



if __name__ == "__main__":
    main()

