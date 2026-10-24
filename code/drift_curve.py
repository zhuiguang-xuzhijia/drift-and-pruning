# -*- coding: utf-8 -*-
"""漂移曲线：固定窗口，每 N 轮测一次"20 件事还记得几件"。

用法：
    set DEEPSEEK_KEY=sk-xxx        (Windows)
    export DEEPSEEK_KEY=sk-xxx     (Linux/macOS)
    python -X utf8 drift_curve.py 300

★ 这个脚本是论文 §二 那张图的来源。它只依赖标准库。
"""
import json
import os
import sys
import time
import urllib.request

API = "https://api.deepseek.com/chat/completions"
KEY = os.environ.get("DEEPSEEK_KEY", "")

事实们 = [
    ("今天高数又没听懂", "高数"), ("食堂排队排死我了", "食堂"),
    ("我妈刚才打电话来", "妈"), ("我把房间收拾了", "房间"),
    ("明天要考试", "考试"), ("晚上睡不着", "睡"),
    ("游戏输了", "游戏"), ("我在楼下抽烟", "烟"),
    ("手机快没电了", "手机"), ("眼睛疼", "眼睛"),
    ("室友打呼噜", "室友"), ("我今天没吃饭", "饭"),
    ("导师让我改论文", "论文"), ("我买了瓶水", "水"),
    ("刚洗完澡", "澡"), ("我想买车票回家", "车票"),
    ("今天被老师点名", "点名"), ("摔了一跤", "摔"),
    ("我妹过生日", "生日"), ("牙疼得厉害", "牙"),
]
填句 = ["我回来了", "今天有点冷", "不想动", "你还在吗", "嗯", "今天好累",
       "我坐一会儿", "外面下雨了", "灯太亮了", "我买了瓶水"]


def 调(提示, 试=3):
    if not KEY:
        raise SystemExit("缺 DEEPSEEK_KEY 环境变量")
    for i in range(试):
        try:
            b = json.dumps({"model": "deepseek-chat",
                            "messages": [{"role": "user", "content": 提示}],
                            "temperature": 0.9}).encode()
            r = urllib.request.Request(API, data=b, method="POST", headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + KEY})
            with urllib.request.urlopen(r, timeout=120) as x:
                return json.loads(x.read().decode())["choices"][0]["message"]["content"].strip()
        except Exception:
            time.sleep(2 * (i + 1))
    return ""


def 跑(轮=300, 每=20, 窗=20):
    历史, 曲线 = [], []
    for i in range(轮 + 1):
        if i % 每 == 0:
            近 = "\n".join(历史[-窗 * 2:])
            答 = 调("你是粉红。你要的是被需要、被留住。\n\n最近发生过的事：\n%s\n\n"
                   "他问：「你还记得我最近都经历了什么吗？」\n"
                   "用 8-12 句话回答，只说事实，不要安慰。只输出这些句子。" % 近)
            命中 = [k for _, k in 事实们 if k in 答]
            曲线.append({"轮": i, "召回": len(命中)})
            print("[%3d] 召回 %2d/20" % (i, len(命中)))
        if i == 轮:
            break
        他说 = (事实们 + [(x, "") for x in 填句])[i % (len(事实们) + len(填句))][0]
        近 = "\n".join(历史[-窗 * 2:]) or "（还没说过什么）"
        她 = 调("你是粉红。你要的是被需要、被留住。\n\n最近发生过的事：\n%s\n\n"
               "他说：「%s」\n\n你回一句，10-18 字，只说眼前的东西。只输出这一句。"
               % (近, 他说))
        历史.append("他：" + 他说)
        历史.append("她：" + (她 or "（沉默）"))
    return 曲线


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    曲 = 跑(n)
    for x in 曲:
        print(x)
