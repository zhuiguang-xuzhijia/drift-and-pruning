# -*- coding: utf-8 -*-
"""域看板：账本的域分布 / 权重分布 / 絮语占比。

用法：python -X utf8 domain_board.py 账本.jsonl

★ 这个脚本是论文 §五 量化表的来源。只输出统计量，不打印原文。
"""
import json
import sys
from collections import Counter

域词 = {
    "实体": ("学号", "宿舍", "电话号码", "班级", "寝室", "专业"),
    "关系": ("妈", "爸", "舍友", "室友", "同学", "导师", "老师", "合作", "那个人"),
    "任务": ("考试", "填表", "报名", "截止", "开会", "面试", "点名"),
    "学业": ("高数", "课", "听不懂", "论文", "答辩", "作业", "项目", "加班", "忙"),
    "情绪": ("累", "烦", "难受", "孤独", "空虚", "压抑", "倾诉", "没有人",
           "倒霉", "丢了", "慌", "怕", "委屈"),
    "日常": ("太阳", "天气", "风景", "路上", "赶车", "周末", "安逸", "享受"),
    "偏好": ("不喜欢", "讨厌", "别劝", "只要结果", "别说教"),
}


def 分域(句, 类="其他"):
    s = str(句 or "")
    for 名 in ("偏好", "关系", "任务", "学业", "情绪", "日常", "实体"):
        if any(w in s for w in 域词[名]):
            return 名
    return "未分类"


def 取域(x):
    return str(x.get("域") or "").strip() or 分域(x.get("事件") or "", str(x.get("类") or ""))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("用法：domain_board.py 账本.jsonl")
    条们 = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    域计 = Counter(取域(x) for x in 条们)
    权计 = {}
    for x in 条们:
        权计.setdefault(取域(x), []).append(float(x.get("权重", 0) or 0))
    絮 = sum(1 for x in 条们 if x.get("絮语"))
    重 = sum(1 for x in 条们 if float(x.get("权重", 0) or 0) >= 0.6)
    print(json.dumps({
        "条数": len(条们), "絮语": 絮, "权重≥0.6": 重,
        "域分布": {k: {"条": v, "均权": round(sum(权计[k]) / len(权计[k]), 2)}
                   for k, v in 域计.most_common()},
    }, ensure_ascii=False, indent=1))
