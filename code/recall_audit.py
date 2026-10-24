# -*- coding: utf-8 -*-
"""逐句对账：他说的话里，有多少真的进了账本。

用法：
    python -X utf8 recall_audit.py 账本.jsonl 聊天.jsonl

★ 这个脚本是论文 §五 那张表的来源。它只依赖标准库。
  它输出的是**计数**，不打印任何一句原文（隐私）。
"""
import json
import sys

虚 = set("的了呢嗯哦啊吧嘛呀么我你他她它在是有就不都也还只把被给让和跟对说"
        "要会能可这那哪个些一上下中前后没很少多好去来到过吗")


def 切句(原):
    return [x.strip() for x in str(原 or "").replace("！", "。").replace("？", "。")
            .replace("；", "。").split("。") if len(x.strip()) >= 2][:4]


def 是絮语(句):
    s = str(句 or "").strip()
    if len(s) <= 2:
        return True
    纯 = "".join(c for c in s if c not in "，。！？…、；：,.!?;: \t")
    return len(纯) <= 4 and any(w in 纯 for w in ("嗯", "哦", "好", "行", "算了", "没事"))


def 主(账本路, 聊天路, uid):
    条们 = [json.loads(l) for l in open(账本路, encoding="utf-8") if l.strip()]
    事件 = [str(x.get("事件") or "") for x in 条们]
    他说们 = []
    for l in open(聊天路, encoding="utf-8"):
        if not l.strip():
            continue
        x = json.loads(l)
        if str(x.get("uid")) == uid and str(x.get("他说") or "").strip():
            他说们.append(str(x["他说"]).strip())

    应有 = [片 for t in 他说们 for 片 in 切句(t)]

    def 落了(片):
        头 = 片[:6].strip("，。！？…、 ")
        return bool(头) and any(头 in e for e in 事件)

    真落 = [片 for 片 in 应有 if 落了(片)]
    絮 = [片 for 片 in 应有 if 是絮语(片) and not 落了(片)]
    print(json.dumps({
        "轮数": len(他说们), "切出句数": len(应有), "落地": len(真落),
        "保留率": round(100.0 * len(真落) / max(1, len(应有)), 1),
        "絮语未落": len(絮), "账本条数": len(条们),
    }, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SystemExit("用法：recall_audit.py 账本.jsonl 聊天.jsonl uid")
    主(sys.argv[1], sys.argv[2], sys.argv[3])
