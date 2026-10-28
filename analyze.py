
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
    return pivot,monthly_total,pct

def print_report(pivot,monthly_total,pct):
    # 遍历行（月份）、列（类别），格式化输出
    for month in pivot.index:
        print(f"{month} 总花费：{monthly_total[month]:.1f}")
        for category in CATEGORY_ORDER:
            print(f"  {category}：{pivot.loc[month,category]:.1f}（{pct.loc[month,category]:.1f}%）")
        print()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "cleaned.csv"
    df = load(path)
    pivot,total,pct = monthly_report(df)
    print_report(pivot,total,pct)



if __name__ == "__main__":
    main()

