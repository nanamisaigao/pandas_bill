import sys
import pandas as pd

def load(path):
    return pd.read_csv(path, on_bad_lines="warn")

def clean(df):
    # 第一步：删重复表头
    clean_df=df[df["日期"]!="日期"].copy()

    #第二步：修日期
    s=pd.to_datetime(clean_df["日期"],errors="coerce",format="mixed")
    bad=clean_df[s.isna()]
    print(f"无法解析的日期： {len(bad)} 行")
    print(bad["日期"].tolist())
    clean_df= clean_df[s.notna()].copy()
    clean_df["日期"] = s.dt.strftime("%Y-%m-%d")

    # 第三步：修金额
    s=clean_df["金额"].astype(str)
    s=s.str.strip()
    s=s.str.replace("元","",regex=False)
    clean_df["金额"]=pd.to_numeric(s,errors="coerce")
    clean_df= clean_df.dropna(subset=["金额"]).copy()


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

