#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给截图合成 macOS 窗口效果（圆角窗口 + 标题栏 + 交通灯 + 投影）。

视觉规格以 fs/ 里的真实 `screencapture -w` 素材（26-09-26-tablelite-main-window.png /
26-10-09-pi-status-tmux.png）为基准做像素级标定：画布外边距、圆角、交通灯尺寸与位置来自
实测，三层投影（alpha 曲线）由实测剖面拟合而来。

用法::

    # 最省事：白色标题栏 + 交通灯 + 投影，不写标题
    python3 .pi/scripts/img-frame.py local/img/app.png -o fs/26-10-10-app-window.png

    # 灰底标题栏 + 居中标题
    python3 .pi/scripts/img-frame.py local/img/app.png -o fs/26-10-10-app-window.png \\
        --title "TableLite" --bar gray

    # 只加圆角与投影，不加标题栏
    python3 .pi/scripts/img-frame.py local/img/app.png -o fs/26-10-10-app-shadow.png --style shadow-only

    # 不落盘，只看将要做什么（供发布前向用户确认）
    python3 .pi/scripts/img-frame.py local/img/app.png -o fs/x.png --dry-run --json

退出码：0 成功，1 出错，2 参数错误。
"""

from __future__ import annotations

import argparse
import json
import sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

# --------------------------------------------------------------------------- #
# 视觉规格：长度单位 pt（1x 逻辑像素），实际像素 = pt × scale
# --------------------------------------------------------------------------- #
SPEC = {
    # 窗口
    "radius": 17.0,           # 窗口圆角（实测拟合 34px @2x）
    "bar_white": (255, 255, 255),
    "bar_gray": (246, 246, 246),
    "hairline": 1.0,
    "hairline_color": (226, 226, 226),
    # 标题栏
    "titlebar": 28.0,         # 标题栏高度
    "light_d": 13.0,          # 交通灯直径
    "light_gap": 10.0,        # 交通灯间距（圆心距 23pt - 直径 13pt）
    "light_left": 9.25,       # 首灯左边缘距窗口左边
    "light_ring": 0.5,        # 灯描边宽度
    "title_size": 13.0,
    "title_color": (60, 60, 60, 255),
    "title_left_gap": 8.0,    # 左对齐时标题距末位交通灯右侧
    # 画布外边距（窗口实心区 → 画布边缘，实测 76/112/148 px @2x）
    "pad_top": 38.0,
    "pad_side": 56.0,
    "pad_bottom": 74.0,
    # 投影：三层 (sigma, alpha, offset_y)，由实测剖面拟合（见模块 docstring）
    "shadow": (
        (1.50, 0.450, 0.00),
        (17.67, 0.196, 14.97),
        (19.99, 0.207, 23.31),
    ),
}

# 交通灯：(填充色, 描边色)
LIGHTS = (
    ((255, 95, 87), (224, 68, 62)),
    ((254, 188, 46), (222, 161, 35)),
    ((40, 200, 64), (29, 173, 43)),
)

LATIN_FONTS = (
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
)
CJK_FONTS = (
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
)
CJK_PREFERRED = ("Regular", "W3", "W4")


def px(value: float, scale: int) -> int:
    return int(round(value * scale))


# --------------------------------------------------------------------------- #
# 工具
# --------------------------------------------------------------------------- #
def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def detect_scale(im: Image.Image, override: str) -> int:
    """auto：DPI ≥ 120 → 2x；否则宽 ≥ 1400px → 2x；否则 1x（macOS 截图带 144dpi 元数据）。"""
    if override in ("1", "2"):
        return int(override)
    dpi = im.info.get("dpi") or (0, 0)
    if dpi[0] and dpi[0] >= 120:
        return 2
    return 2 if im.width >= 1400 else 1


def looks_like_window_capture(im: Image.Image) -> bool:
    """是否看起来已经是 macOS 窗口截图（自带圆角 + 投影）。

    仅用于给出「框套框」的提醒，不影响处理行为。
    """
    if im.mode not in ("RGBA", "LA"):
        return False
    rgba = im.convert("RGBA")
    alpha = rgba.getchannel("A")
    w, h = rgba.size
    solid = alpha.point(lambda v: 255 if v > 200 else 0).getbbox()
    faint = alpha.point(lambda v: 255 if v > 10 else 0).getbbox()
    if not solid or not faint:
        return False
    solid_margins = (solid[0], solid[1], w - solid[2], h - solid[3])
    faint_margins = (faint[0], faint[1], w - faint[2], h - faint[3])
    if min(solid_margins) <= 8 or min(faint_margins) <= 2:
        return False
    corners = (
        alpha.getpixel((0, 0)),
        alpha.getpixel((w - 1, 0)),
        alpha.getpixel((0, h - 1)),
        alpha.getpixel((w - 1, h - 1)),
    )
    return max(corners) < 8


def _load_face(path: str, size: int, preferred: tuple[str, ...]) -> ImageFont.FreeTypeFont | None:
    """加载字体文件；`.ttc` 时在多个字面里挑名字最贴近 preferred 的那个。"""
    if not path.endswith(".ttc"):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return None
    first = None
    for index in range(12):
        try:
            font = ImageFont.truetype(path, size, index=index)
        except Exception:
            break
        if first is None:
            first = font
        try:
            name = font.getname()[1]
        except Exception:
            name = ""
        if any(p in name for p in preferred):
            return font
    return first


def load_fonts(size: int) -> tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont | None]:
    latin = cjk = None
    for path in LATIN_FONTS:
        latin = _load_face(path, size, CJK_PREFERRED)
        if latin:
            break
    for path in CJK_FONTS:
        cjk = _load_face(path, size, CJK_PREFERRED)
        if cjk:
            break
    if latin is None:
        raise RuntimeError("找不到可用的拉丁字体（SFNS/Helvetica/Arial 均不可用）")
    return latin, cjk


def _is_cjk(ch: str) -> bool:
    code = ord(ch)
    return (
        0x2E80 <= code <= 0x2EFF      # 部首
        or 0x3000 <= code <= 0x303F   # CJK 标点
        or 0x3040 <= code <= 0x30FF   # 假名
        or 0x3400 <= code <= 0x4DBF
        or 0x4E00 <= code <= 0x9FFF
        or 0xF900 <= code <= 0xFAFF
        or 0xFF00 <= code <= 0xFFEF   # 全角
    )


def _runs(text: str, cjk) -> list[tuple[str, ImageFont.FreeTypeFont]]:
    """按字体切分文本（拉丁用 SF，中文用 Hiragino/PingFang）。"""
    out: list[tuple[str, ImageFont.FreeTypeFont]] = []
    for ch in text:
        font = cjk if (cjk is not None and _is_cjk(ch)) else None
        if out and out[-1][1] is font:
            out[-1] = (out[-1][0] + ch, font)
        else:
            out.append((ch, font))
    return out


def light_geometry(scale: int):
    """返回 (首灯左边缘, 直径, 圆心距)。"""
    d = px(SPEC["light_d"], scale)
    return px(SPEC["light_left"], scale), d, d + px(SPEC["light_gap"], scale)


def draw_title(draw, text, fonts, window_w, scale, align):
    latin, cjk = fonts
    runs = [(t, f if f is not None else latin) for t, f in _runs(text, cjk)]
    widths = [f.getlength(t) for t, f in runs]
    total = sum(widths)
    if align == "center":
        x = (window_w - total) / 2
    else:
        left, d, step = light_geometry(scale)
        x = left + 2 * step + d + px(SPEC["title_left_gap"], scale)   # 末位交通灯右侧
    y = px(SPEC["titlebar"], scale) / 2
    for (t, f), w in zip(runs, widths):
        draw.text((x, y), t, font=f, fill=SPEC["title_color"], anchor="lm")
        x += w


# --------------------------------------------------------------------------- #
# 渲染
# --------------------------------------------------------------------------- #
def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255
    )
    return mask


def build_window(content, style, scale, bar, title, title_align, fonts, radius):
    """返回 (窗口图像, 窗口圆角遮罩)。"""
    cw, ch = content.size
    tbar = px(SPEC["titlebar"], scale) if style == "window" else 0
    size = (cw, ch + tbar)
    mask = rounded_mask(size, radius)

    if style == "window":
        window = Image.new("RGBA", size, bar + (255,))
        window.alpha_composite(content, (0, tbar))
    else:
        window = content.copy()

    if style == "window" and bar == SPEC["bar_gray"]:
        hair = px(SPEC["hairline"], scale)
        y = tbar - hair
        ImageDraw.Draw(window).rectangle(
            [radius * 0.5, y, cw - radius * 0.5, y + hair - 1], fill=SPEC["hairline_color"] + (255,)
        )

    if style == "window":
        draw = ImageDraw.Draw(window)
        cy = tbar / 2
        left, d, step = light_geometry(scale)
        ring = max(1, px(SPEC["light_ring"], scale))
        for i, (fill, edge) in enumerate(LIGHTS):
            x0 = left + i * step
            draw.ellipse([x0, cy - d / 2, x0 + d, cy + d / 2], fill=fill + (255,), outline=edge + (255,), width=ring)
        if title:
            draw_title(draw, title, fonts, cw, scale, title_align)

    window.putalpha(ImageChops.multiply(window.getchannel("A"), mask))
    return window, mask


def render(content, style, scale, bar, title, title_align, radius, shadow=True):
    fonts = load_fonts(px(SPEC["title_size"], scale)) if title else (None, None)
    window, mask = build_window(content, style, scale, bar, title, title_align, fonts, radius)
    w, h = window.size
    pad = (px(SPEC["pad_side"], scale), px(SPEC["pad_top"], scale), px(SPEC["pad_bottom"], scale))
    canvas_size = (w + 2 * pad[0], h + pad[1] + pad[2])
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))

    if shadow:
        shadow_layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        for sigma, alpha, offset_y in SPEC["shadow"]:
            layer_mask = Image.new("L", canvas_size, 0)
            layer_mask.paste(mask, (pad[0], pad[1] + px(offset_y, scale)))
            layer_mask = layer_mask.filter(ImageFilter.GaussianBlur(px(sigma, scale)))
            layer = Image.new("RGBA", canvas_size, (0, 0, 0, 255))
            layer.putalpha(layer_mask.point(lambda v: int(v * alpha)))
            shadow_layer = Image.alpha_composite(shadow_layer, layer)
        canvas.alpha_composite(shadow_layer)

    canvas.alpha_composite(window, (pad[0], pad[1]))
    return canvas


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(
        prog="img-frame.py",
        description="给截图合成 macOS 窗口效果（圆角窗口 + 标题栏 + 交通灯 + 投影）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  img-frame.py local/img/app.png -o fs/26-10-10-app-window.png\n"
            "  img-frame.py local/img/app.png -o fs/26-10-10-app-window.png --title TableLite --bar gray\n"
            "  img-frame.py local/img/app.png -o fs/26-10-10-app-shadow.png --style shadow-only\n"
        ),
    )
    p.add_argument("src", help="源图片路径（草稿里引用的原图，不会被修改）")
    p.add_argument("-o", "--out", required=True, help="输出 PNG 路径")
    p.add_argument("--style", choices=("window", "shadow-only"), default="window",
                   help="window=圆角+标题栏+交通灯+投影（默认）；shadow-only=只加圆角与投影")
    p.add_argument("--title", default="", help="标题栏文字（默认不写）")
    p.add_argument("--title-align", choices=("center", "left"), default="center", help="标题对齐（默认居中）")
    p.add_argument("--bar", choices=("white", "gray"), default="white", help="标题栏底色（默认 white）")
    p.add_argument("--no-shadow", action="store_true", help="不画投影")
    p.add_argument("--radius", type=float, default=None, help=f"窗口圆角 pt（默认 {SPEC['radius']}）")
    p.add_argument("--scale", choices=("auto", "1", "2"), default="auto", help="渲染倍率（默认按 DPI/宽度推断）")
    p.add_argument("--dry-run", action="store_true", help="只汇报将要做什么，不写文件")
    p.add_argument("--json", action="store_true", help="以 JSON 输出结果（便于 agent 解析）")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        content = Image.open(args.src)
    except Exception as exc:
        print(f"error: 无法读取源图 {args.src}: {exc}", file=sys.stderr)
        return 1
    content.load()

    scale = detect_scale(content, args.scale)
    radius = px(args.radius if args.radius is not None else SPEC["radius"], scale)
    bar = SPEC["bar_gray"] if args.bar == "gray" else SPEC["bar_white"]

    warnings = []
    if looks_like_window_capture(content):
        warnings.append(
            "源图看起来已经是 macOS 窗口截图（自带圆角与投影），本次仍按参数再套一层，"
            "结果会出现「框套框」"
        )
        warn(warnings[-1])

    content = content.convert("RGBA")
    if args.style == "shadow-only" and args.title:
        warn("--style shadow-only 下 --title 无效，已忽略")
    title = args.title if args.style == "window" else ""

    result = render(
        content, args.style, scale, bar, title, args.title_align, radius, shadow=not args.no_shadow
    )
    out_size = result.size

    if not args.dry_run:
        dpi = 72 * scale
        try:
            result.save(args.out, dpi=(dpi, dpi))
        except Exception as exc:
            print(f"error: 写入 {args.out} 失败: {exc}", file=sys.stderr)
            return 1

    info = {
        "src": args.src,
        "out": args.out,
        "style": args.style,
        "scale": scale,
        "src_size": list(content.size),
        "window_size": [out_size[0] - 2 * px(SPEC["pad_side"], scale),
                        out_size[1] - px(SPEC["pad_top"], scale) - px(SPEC["pad_bottom"], scale)],
        "out_size": list(out_size),
        "titlebar": args.style == "window",
        "title": title,
        "bar": args.bar,
        "radius": args.radius if args.radius is not None else SPEC["radius"],
        "shadow": not args.no_shadow,
        "dpi": 72 * scale,
        "wrote": not args.dry_run,
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        action = "将写入" if args.dry_run else "已写入"
        shadow_desc = "有" if not args.no_shadow else "无"
        print(f"{action}: {args.out}")
        if args.style == "window":
            title_desc = f"「{title}」（{'居中' if args.title_align == 'center' else '左对齐'}）" if title else "无"
            print(f"  样式: window（圆角 + 标题栏 + 交通灯）  标题栏底色: {args.bar}  标题: {title_desc}  投影: {shadow_desc}")
        else:
            print(f"  样式: shadow-only（圆角 + 投影，无标题栏）  投影: {shadow_desc}")
        print(f"  倍率: {scale}x (dpi {72 * scale})  源图: {args.src} {content.size[0]}x{content.size[1]}")
        print(f"  输出: {out_size[0]}x{out_size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
