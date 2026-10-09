#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 img-frame.py 的几何与投影常量是否仍与 fs/ 里的真实窗口截图一致。

做法：把 fs/ 中两张 `screencapture -w` 素材（同一应用的两次截图，剖面逐像素相同）当作基准，
用同尺寸的纯色内容渲染一个窗口框，再逐像素比较「窗口下 / 右 / 上三条剖面」的 alpha 曲线；
窗口边缘 1-4px 混合了窗口自身的抗锯齿，比对时跳过。

注意：不是所有真实窗口都长这样——fs/26-10-09-pi-status-tmux.png 是另一种更重的「浮动窗口」
投影，本脚本不以它为基准。

    python3 .pi/scripts/img-frame-check.py            # 退出码 0 通过，1 不通过

改动 img-frame.py 的 SPEC（圆角、边距、阴影层）后必须跑一次。
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
REFERENCES = (
    ROOT / "fs/26-09-26-tablelite-main-window.png",
    ROOT / "fs/26-09-26-tablelite-query-editor.png",
)
RANGES = {"bottom": 120, "side": 90, "top": 55}
SKIP_EDGE = 4     # 窗口边缘 1-4px 混合了窗口自身的抗锯齿，不参与比对
TOL_MEAN = 3.0    # 平均差（0-255）
TOL_MAX = 25.0    # 单点最大差


def load_frame_module():
    spec = importlib.util.spec_from_file_location("imgframe", pathlib.Path(__file__).with_name("img-frame.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def window_rect(im: Image.Image, threshold: int = 200):
    alpha = im.convert("RGBA").getchannel("A")
    bbox = alpha.point(lambda v: 255 if v > threshold else 0).getbbox()
    if bbox is None:
        raise ValueError("找不到不透明区域，源图可能没有 alpha 通道")
    return (bbox[0], bbox[1], bbox[2] - 1, bbox[3] - 1)


def profiles(im: Image.Image, rect, ranges=RANGES):
    width, height = im.size
    px = im.load()
    left, top, right, bottom = rect
    cx, cy = (left + right) // 2, (top + bottom) // 2
    out = {}
    out["bottom"] = [px[cx, bottom + 1 + d][3] for d in range(min(ranges["bottom"], height - bottom - 1))]
    out["side"] = [px[right + 1 + d, cy][3] for d in range(min(ranges["side"], width - right - 1))]
    out["top"] = [px[cx, top - 1 - d][3] for d in range(min(ranges["top"], top))]
    return out


def corner_insets(im: Image.Image, rect, count: int = 16):
    """左上角每下一行、不透明区相对窗口左边内的内缩量（用于反推圆角）。"""
    left, top = rect[0], rect[1]
    px = im.load()
    out = []
    for dy in range(count):
        x = left
        while x < left + 120 and px[x, top + dy][3] <= 200:
            x += 1
        out.append(x - left)
    return out


def main() -> int:
    module = load_frame_module()
    scale = 2
    radius = module.px(module.SPEC["radius"], scale)
    pad = (module.px(module.SPEC["pad_side"], scale), module.px(module.SPEC["pad_top"], scale),
           module.px(module.SPEC["pad_bottom"], scale))
    ok = True
    for reference in REFERENCES:
        ref = Image.open(reference).convert("RGBA")
        rect = window_rect(ref)
        content = Image.new("RGBA", (rect[2] - rect[0] + 1, rect[3] - rect[1] + 1), (255, 255, 255, 255))
        rendered = module.render(content, "window", scale, module.SPEC["bar_white"], "", "center", radius)
        ours_rect = (pad[0], pad[1], rendered.size[0] - pad[0] - 1, rendered.size[1] - pad[2] - 1)
        expected = profiles(ref, rect)
        actual = profiles(rendered, ours_rect)
        print(f"基准: {reference.name}  窗口 {rect[2]-rect[0]+1}x{rect[3]-rect[1]+1}")

        margins = (rect[0], rect[1], ref.size[0] - 1 - rect[2], ref.size[1] - 1 - rect[3])
        for label, ours, theirs in (("上", pad[1], margins[1]), ("左", pad[0], margins[0]),
                                    ("右", pad[0], margins[2]), ("下", pad[2], margins[3])):
            flag = "ok" if abs(ours - theirs) <= 2 else "FAIL"
            if flag == "FAIL":
                ok = False
            print(f"  画布外边距({label}) ours={ours} ref={theirs}  {flag}")

        ours_insets = corner_insets(rendered, ours_rect)
        ref_insets = corner_insets(ref, rect)
        diffs = [abs(a - b) for a, b in zip(ours_insets[1:SKIP_EDGE + 8], ref_insets[1:SKIP_EDGE + 8])]
        flag = "ok" if max(diffs) <= 3 else "FAIL"
        if flag == "FAIL":
            ok = False
        print(f"  圆角内缩 ours={ours_insets[1:12]} ref={ref_insets[1:12]}  最大差 {max(diffs)}  {flag}")

        for key in ("bottom", "side", "top"):
            pairs = list(zip(actual[key][SKIP_EDGE:], expected[key][SKIP_EDGE:]))
            diffs = [abs(a - b) for a, b in pairs]
            mean = sum(diffs) / len(diffs)
            worst = max(diffs)
            flag = "ok" if (mean <= TOL_MEAN and worst <= TOL_MAX) else "FAIL"
            if flag == "FAIL":
                ok = False
            print(f"  {key:6s} n={len(diffs):3d}  平均差 {mean:5.2f}  最大差 {worst:3d}  {flag}")
            if flag == "FAIL":
                print(f"         ours: {actual[key][SKIP_EDGE:SKIP_EDGE+16]}")
                print(f"         ref : {expected[key][SKIP_EDGE:SKIP_EDGE+16]}")
    print("通过" if ok else "不通过：请复核 img-frame.py 的 SPEC 或重新拟合阴影参数")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
