import sys
import pandas as pd

def load(path):
    return pd.read_csv(path, on_bad_lines="warn")

def clean(df):
    # 第一步：删重复表头
    clean_df=df[df["日期"]!="日期"].copy()

    #第二步：修日期
    bad_df=clean_df["日期"].copy()
    clean_df["日期"]=pd.to_datetime(clean_df["日期"],errors="coerce",format="mixed")

    bad=clean_df["日期"].isna()
    print(f"无法解析的日期： {bad.sum()} 行")
    print(bad_df[bad].tolist())

    clean_df= clean_df[clean_df["日期"].notna()].copy()
    clean_df = clean_df[clean_df["日期"].dt.year == 2024].copy()
    clean_df["日期"] = clean_df["日期"].dt.strftime("%Y-%m-%d")

    # 第三步：修金额
    clean_df["金额"]=clean_df["金额"].astype(str)
    clean_df["金额"]=clean_df["金额"].str.strip()
    clean_df["金额"]=clean_df["金额"].str.replace("元","",regex=False)
    clean_df["金额"]=pd.to_numeric(clean_df["金额"],errors="coerce")
    clean_df= clean_df.dropna(subset=["金额"]).copy()

    # 第四步：修类别

    clean_df["类别"] = clean_df["类别"].str.strip()  # 去前后空格
    clean_df["类别"] = clean_df["类别"].str.lower()  # 统一小写（中文不受影响，英文同义词受益）
    clean_df["类别"]=clean_df["类别"].replace({
        "吃饭": "餐饮", "food": "餐饮",
        "出行": "交通", "taxi": "交通",
        "买东西": "购物", "shopping": "购物",
        "玩乐": "娱乐", "game": "娱乐",
    })
    std = ["餐饮", "交通", "购物", "娱乐"]
    clean_df["类别"]=clean_df["类别"].where(clean_df["类别"].isin(std),"其他")
    clean_df=clean_df.drop_duplicates().copy()
    clean_df=clean_df.sort_values("日期").reset_index(drop=True)

    return clean_df

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data_sample.csv"
    df = load(path)
    df_clean = clean(df)
    df_clean.to_csv("cleaned.csv", index=False,encoding="utf-8")
    print(f"清洗前：{len(df)} 行")
    print(f"清洗后：{len(df_clean)} 行")

if __name__ == "__main__":
    main()

