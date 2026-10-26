import csv
import random

random.seed(42)

HEADER = ["日期", "类别", "金额"]
CATEGORIES = ["餐饮", "交通", "购物", "娱乐"]
ALIASES = {"餐饮": ["吃饭", "food", "FOOD"],
           "交通": ["出行", "taxi"],
           "购物": ["买东西", "shopping"],
           "娱乐": ["玩乐", "game"]}

def clean_date():
    m = random.randint(1, 12)
    d = random.randint(1, 28)
    return f"2024-{m:02d}-{d:02d}"

def clean_amount():
    return str(round(random.uniform(5, 300), 1))

def clean_category():
    return random.choice(CATEGORIES)

# ---------- 脏数据工厂 ----------
def dirty_date():
    kind = random.choices(
        ["no_pad", "slash", "datetime", "empty",
         "bad_month", "bad_day", "cross_year"],
        weights=[3, 3, 2, 2, 1, 1, 2],
    )[0]
    if kind == "no_pad":
        return f"2024-{random.randint(1,12)}-{random.randint(1,28)}"
    if kind == "slash":
        return f"2024/{random.randint(1,12):02d}/{random.randint(1,28):02d}"
    if kind == "datetime":
        return f"{clean_date()} {random.randint(0,23):02d}:{random.randint(0,59):02d}:00"
    if kind == "empty":
        return ""
    if kind == "bad_month":
        return "2024-13-05"
    if kind == "bad_day":
        return "2024-02-30"
    return "2023-12-31"          # 跨年

def dirty_amount():
    kind = random.choices(
        ["empty", "abc", "unit", "thousand", "space",
         "negative", "zero", "multi_dot", "sci", "fullwidth"],
        weights=[3, 3, 2, 2, 2, 1, 1, 1, 1, 1],
    )[0]
    if kind == "empty":
        return ""
    if kind == "abc":
        return "abc"
    if kind == "unit":
        return f"{clean_amount()}元"
    if kind == "thousand":
        return f"{random.randint(1,9)},200.0"
    if kind == "space":
        return f"  {clean_amount()}  "
    if kind == "negative":
        return f"-{clean_amount()}"
    if kind == "zero":
        return "0"
    if kind == "multi_dot":
        return "35.5.5"
    if kind == "sci":
        return "1e3"
    return "１２３"              # 全角数字

def dirty_category():
    kind = random.choices(
        ["space", "case", "alias", "empty", "unknown"],
        weights=[3, 2, 3, 2, 2],
    )[0]
    base = random.choice(CATEGORIES)
    if kind == "space":
        return f" {base} "
    if kind == "case":
        return base.upper() if random.random() < 0.5 else base.lower()
    if kind == "alias":
        return random.choice(ALIASES[base])
    if kind == "empty":
        return ""
    return "其他"

# ---------- 组装 ----------
rows = [HEADER]

for month in range(1, 7):
    for _ in range(15):
        r = random.random()
        if r < 0.70:                     # 70% 正常
            row = [clean_date(), clean_category(), clean_amount()]
        elif r < 0.85:                   # 15% 金额脏
            row = [clean_date(), clean_category(), dirty_amount()]
        elif r < 0.95:                   # 10% 日期脏
            row = [dirty_date(), clean_category(), clean_amount()]
        else:                            # 5% 类别脏
            row = [clean_date(), dirty_category(), clean_amount()]

        rows.append(row)

        # 额外结构异常（低频）
        extra = random.random()
        if extra < 0.03:                 # 3% 缺列
            rows.append([clean_date(), clean_category()])
        elif extra < 0.05:               # 2% 多一列
            rows.append([clean_date(), clean_category(), clean_amount(), "备注"])
        elif extra < 0.07:               # 2% 完全空行
            rows.append([])
        elif extra < 0.09:               # 2% 重复表头
            rows.append(HEADER[:])
        elif extra < 0.11:               # 2% 完全重复上一行
            rows.append(rows[-2][:])

# 再插几条完全重复的干净数据（练去重）
for _ in range(5):
    rows.append(["2024-03-15", "餐饮", "88.0"])

with open("data_sample.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(rows)

print(f"生成 {len(rows)-1} 行数据（含异常）")