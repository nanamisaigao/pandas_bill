import sys
import pandas as pd

def load(path):
    return pd.read_csv(path, on_bad_lines="warn")

def clean(df):
    # 第一步：删重复表头
    clean_df=df[df["日期"]!="日期"].copy()
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

