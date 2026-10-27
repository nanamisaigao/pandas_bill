import sys
import pandas as pd

def profile(path):
    """读 CSV，打印各项脏数据统计。"""
    df = pd.read_csv(path, on_bad_lines="warn")
    print(f"形状：{df.shape}")
    df.info()
    print()
    #重复表头
    bad_header=df[(df["日期"]=="日期")]
    print(f"重复表头：{len(bad_header)}")
    print()

    # 1. 日期长度≠10
    clean=df.drop(bad_header.index)
    s=clean['日期'].astype(str)
    bad=s[s.str.len()!=10]
    print('长度不等于10：',len(bad))
    print(bad.tolist())
    print()

    # 2. 日期含斜杠
    bad=s[s.str.contains('/',na=False)]
    print('含斜杠：',len(bad))
    print(bad.tolist())
    print()

    # 3. 日期含空格
    bad=s[s.str.contains(' ',na=False)]
    print('含空格：',len(bad))
    print(bad.tolist())
    print()

    # 4. 金额无法转数字
    s=clean['金额']
    n=pd.to_numeric(s,errors='coerce')
    bad=s[n.isna() & s.notna()]
    print('无法转数字',len(bad))
    print(bad.tolist())
    print()

    # 5. 类别带前后空格
    s=clean['类别'].astype(str)
    bad=s[s.notna() & (s!=s.str.strip())]
    print('带空格',len(bad))
    print(bad.tolist())
    print()

    # 6. 类别非标准值
    std=['餐饮','交通','购物','娱乐']
    bad=s[~s.isin(std)]
    print('非类别',len(bad))
    print(bad.tolist())
    print()
    return


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data_sample.csv"
    profile(path)