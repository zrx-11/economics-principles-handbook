#!/usr/bin/env python3
"""生成经济学示意图 SVG（内联进章节 md）。
用法：from svgfactory import Graph; g = Graph(...); print(g.render())
"""
W, H = 560, 400
PAD_L, PAD_R, PAD_T, PAD_B = 70, 30, 30, 60


class Graph:
    def __init__(self, xmax=60, ymax=30, xlabel="数量 Q", ylabel="价格 P", title="", w=W, h=H):
        self.xmax, self.ymax = xmax, ymax
        self.xlabel, self.ylabel, self.title = xlabel, ylabel, title
        self.w, self.h = w, h
        self.curves = []   # (pts list of (x,y), color, label, dash, labelpos)
        self.areas = []    # (polygon pts, color, opacity, label)
        self.marks = []    # (x,y,label,color,shape) shape: dot/cross/dash-v
        self.notes = []    # (x,y,text,color)
        self.arrows = []   # (x1,y1,x2,y2,color)

    def px(self, x):
        return PAD_L + (self.w - PAD_L - PAD_R) * x / self.xmax

    def py(self, y):
        return self.h - PAD_B - (self.h - PAD_T - PAD_B) * y / self.ymax

    def curve(self, pts, color="#2563eb", label="", dash=False, label_at=None, width=2.2):
        self.curves.append((pts, color, label, dash, label_at, width))
        return self

    def area(self, pts, color="#93c5fd", opacity=0.35, label=""):
        self.areas.append((pts, color, opacity, label))
        return self

    def mark(self, x, y, label="", color="#111827", shape="dot"):
        self.marks.append((x, y, label, color, shape))
        return self

    def note(self, x, y, text, color="#374151"):
        self.notes.append((x, y, text, color))
        return self

    def arrow(self, x1, y1, x2, y2, color="#dc2626"):
        self.arrows.append((x1, y1, x2, y2, color))
        return self

    def legend(self, x, y, lines, w=170, title="读数"):
        """在数据坐标 (x,y) 处以左上角为起点画一个白底图例框。"""
        self.notes.append(("__LEGEND__", x, y, (lines, w, title)))
        return self

    def render(self):
        s = ['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
             'style="width:100%%;max-width:%dpx;display:block;margin:12px auto;font-family:inherit" '
             'role="img">' % (self.w, self.h, self.w)]
        # 网格与坐标轴
        for i in range(0, 5):
            gx = self.px(self.xmax * i / 4)
            gy = self.py(self.ymax * i / 4)
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e5e7eb" stroke-width="1"/>'
                     % (gx, self.py(0), gx, self.py(self.ymax)))
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e5e7eb" stroke-width="1"/>'
                     % (self.px(0), gy, self.px(self.xmax), gy))
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#111827" stroke-width="1.6"/>'
                 % (self.px(0), self.py(0), self.px(self.xmax), self.py(0)))
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#111827" stroke-width="1.6"/>'
                 % (self.px(0), self.py(0), self.px(0), self.py(self.ymax)))
        s.append('<text x="%.1f" y="%.1f" font-size="12" fill="#374151" text-anchor="middle">%s</text>'
                 % (self.px(self.xmax / 2), self.h - 18, self.xlabel))
        s.append('<text x="16" y="%.1f" font-size="12" fill="#374151" text-anchor="middle" '
                 'transform="rotate(-90 16 %.1f)">%s</text>' % (self.py(self.ymax / 2), self.py(self.ymax / 2), self.ylabel))
        if self.title:
            s.append('<text x="%.1f" y="18" font-size="13" fill="#111827" text-anchor="middle" '
                     'font-weight="600">%s</text>' % (self.px(self.xmax / 2), self.title))
        for pts, color, opacity, label in self.areas:
            d = " ".join("%.1f,%.1f" % (self.px(x), self.py(y)) for x, y in pts)
            s.append('<polygon points="%s" fill="%s" fill-opacity="%.2f" stroke="none"/>' % (d, color, opacity))
            if label:
                cx = sum(self.px(x) for x, _ in pts) / len(pts)
                cy = sum(self.py(y) for _, y in pts) / len(pts)
                s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#111827" text-anchor="middle">%s</text>'
                         % (cx, cy, label))
        for pts, color, label, dash, label_at, width in self.curves:
            d = " ".join("%.1f,%.1f" % (self.px(x), self.py(y)) for x, y in pts)
            s.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f"%s/>'
                     % (d, color, width, ' stroke-dasharray="6,4"' if dash else ''))
            if label:
                lx, ly = label_at if label_at else pts[-1]
                s.append('<text x="%.1f" y="%.1f" font-size="12" fill="%s" font-weight="600">%s</text>'
                         % (self.px(lx) + 4, self.py(ly) - 4, color, label))
        for x, y, label, color, shape in self.marks:
            X, Y = self.px(x), self.py(y)
            if shape == "dot":
                s.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (X, Y, color))
            elif shape == "cross":
                s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2"/>' % (X - 5, Y - 5, X + 5, Y + 5, color))
                s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2"/>' % (X - 5, Y + 5, X + 5, Y - 5, color))
            elif shape == "dashv":
                s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2" stroke-dasharray="5,4"/>' % (X, Y, X, self.py(0), color))
            elif shape == "dashh":
                s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2" stroke-dasharray="5,4"/>' % (X, Y, self.px(0), Y, color))
            if label:
                s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="%s">%s</text>' % (X + 7, Y - 7, color, label))
        for x, y, text, color in self.notes:
            if x == "__LEGEND__":
                lines, lw, ltitle = color
                X, Y = self.px(y), self.py(text)
                hgt = 18 + 15 * len(lines) + 4
                s.append('<rect x="%.1f" y="%.1f" width="%d" height="%.1f" rx="6" fill="#ffffff" '
                         'fill-opacity="0.96" stroke="#d1d5db"/>' % (X, Y, lw, hgt))
                s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#6b7280">%s</text>'
                         % (X + 8, Y + 15, ltitle))
                for i, ln in enumerate(lines):
                    s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#111827">%s</text>'
                             % (X + 8, Y + 30 + 15 * i, ln))
            else:
                s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="%s">%s</text>'
                         % (self.px(x), self.py(y), color, text))
        for x1, y1, x2, y2, color in self.arrows:
            s.append('<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
                     '<path d="M0,0 L6,3 L0,6 z" fill="%s"/></marker></defs>' % color)
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.8" '
                     'marker-end="url(#ar)"/>' % (self.px(x1), self.py(y1), self.px(x2), self.py(y2), color))
        s.append('</svg>')
        return "".join(s)


def line(pts=None, a=None, b=None, x0=0, x1=1, n=12):
    """直线：给定斜率截距 a+bx 或两点。"""
    if a is not None and b is not None:
        return [(x0 + (x1 - x0) * i / (n - 1), a + b * (x0 + (x1 - x0) * i / (n - 1))) for i in range(n)]
    return [(p[0], p[1]) for p in pts]
