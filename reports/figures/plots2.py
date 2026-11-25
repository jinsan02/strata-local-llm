"""11-25 최종 정리 그림 (06~12). 수치는 원장(experiments/LEDGER.tsv)과 STATE 결정 기록에서.
    python reports/figures/plots2.py
과제 내용은 쓰지 않는다(F1 은 과제 ID · 통과 여부 · 시간만)."""
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as md
import matplotlib.pyplot as plt
import matplotlib.ticker as mt
from matplotlib import font_manager

here = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(here, "..", "..", "experiments", "LEDGER.tsv")
font_manager.fontManager.addfont(os.path.join(here, "fonts", "NanumPenScript-Regular.ttf"))   # 나눔손글씨 펜(OFL), 구조도와 같은 글꼴
plt.rcParams.update({"font.family": ["Nanum Pen", "Malgun Gothic"], "axes.unicode_minus": False, "font.size": 16,
    "figure.facecolor": "#fffdf7", "axes.facecolor": "#fffdf7", "savefig.facecolor": "#fffdf7",
    "axes.edgecolor": "#ced4da", "axes.labelcolor": "#495057", "xtick.color": "#495057", "ytick.color": "#495057",
    "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#eceff1", "grid.linewidth": 1.0})
# Tiny Lab 톤: 종이색 바탕 · Open Color · Lucide 아이콘(구조도와 같은 세트)
SURF, INK, INK2, MUTED = "#fffdf7", "#343a40", "#495057", "#868e96"
BLUE, ORANGE, AQUA, GRAY = "#228be6", "#f76707", "#7950f2", "#adb5bd"
ICONS = os.path.join(here, "icons")


def title(fig, t, s, icon=None):
    x = 0.02
    if icon:
        W, H = fig.get_size_inches()
        hh = 0.34 / H                      # 아이콘 높이 0.34인치
        ww = 0.34 / W
        iax = fig.add_axes([0.02, 0.975 - hh + 0.005, ww, hh])
        iax.imshow(plt.imread(os.path.join(ICONS, f"icon-{icon}.png")))
        iax.axis("off")
        x = 0.02 + ww + 0.1 / W
    fig.text(x, 0.975, t, fontsize=21.8, color=INK, va="top")
    fig.text(0.02, 0.895, s, fontsize=14.5, color=INK2, va="top")


def save(fig, name):
    fig.savefig(os.path.join(here, name), dpi=200)
    plt.close(fig)


rows = []
for ln in open(LEDGER, encoding="utf-8"):
    f = ln.rstrip("\n").split("\t")
    if len(f) < 41 or f[0] == "ts_utc":
        continue
    rows.append(f)


def note(f, k):
    m = re.search(re.escape(k) + r" ([^;,]+)", f[40])
    return m.group(1).strip() if m else None


# 06 기준 조합의 변화 ---------------------------------------------------------
st = [("11-18\n읽기 도구만", 0, None, "0/5"), ("11-20\ncard-coding", 16, None, ""), ("11-21\nH7 편집 보강", 17, None, ""),
      ("11-22\n64K + high", 21, None, ""), ("11-23\nH9 + E2", 24, 21, ""), ("11-25\nH12", 23, 24, "")]
fig, ax = plt.subplots(figsize=(10, 5.6))
fig.subplots_adjust(left=0.08, right=0.97, top=0.78, bottom=0.24)
xs = range(len(st))
x3 = [s[1] / 30 * 100 if i else 0 for i, s in enumerate(st)]
ax.plot(list(xs), x3, color=BLUE, lw=2, marker="o", ms=8, mec=SURF, mew=2, label="X3 (packaging 6과제 × 5회)", zorder=3)
yx = [i for i, s in enumerate(st) if s[2] is not None]
ax.plot(yx, [st[i][2] / 30 * 100 for i in yx], color=ORANGE, lw=2, marker="s", ms=8, mec=SURF, mew=2, label="Y (packaging · flask 6과제 × 5회)", zorder=3)
for i, s in enumerate(st):
    dy = -9 if i == len(st) - 1 else 4
    ax.text(i, x3[i] + dy, s[3] or f"{s[1]}/30", ha="center", fontsize=14.5, color=BLUE if i else INK)
for i in yx:
    up = i == len(st) - 1
    ax.text(i, st[i][2] / 30 * 100 + (4 if up else -9), f"{st[i][2]}/30", ha="center", fontsize=14.5, color=ORANGE)
ax.axhline(68 / 90 * 100, color=MUTED, lw=1, ls=(0, (4, 3)))
ax.text(0.02, 68 / 90 * 100 + 1.5, "F1 최종 평가 68/90 (튜닝에 안 쓴 저장소 4개)", fontsize=13.8, color=INK2)
ax.set_xticks(list(xs))
ax.set_xticklabels([s[0] for s in st], fontsize=13.8)
ax.set_ylim(-3, 100)
ax.set_ylabel("통과율 (%)")
ax.grid(axis="x", visible=False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False, fontsize=13.8)
title(fig, "같은 모델, 하네스와 실행 설정만으로 16/30 → 24/30",
      "모델(Qwen3.6-35B-A3B Q4)은 처음부터 끝까지 그대로. 변경마다 같은 seed 30회 짝 비교로 채택 여부를 정했다", icon="trending-up")
save(fig, "06_baseline_progress.png")

# 07 F1 유형별 · 저장소별 -----------------------------------------------------
f1 = [f for f in rows if f[1].startswith("f1_m0_e2_s0_ctx64k_nav_")]
TN = {"F1": "버그 보고", "F2": "실패 테스트 고치기", "F3": "작은 기능", "F4": "여러 파일 연결", "F5": "리팩터링", "F6": "테스트 작성(돌연변이)"}
RN = {"attrs": "attrs", "click": "click", "du": "dateutil", "pluggy": "pluggy"}
bt, br = defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0])
for f in f1:
    m = re.match(r"f1_m0_e2_s0_ctx64k_nav_(f\d)_(attrs|click|du|pluggy)_", f[1])
    ok = note(f, "error_type") == "pass"
    for d, k in ((bt, m.group(1).upper()), (br, m.group(2))):
        d[k][0] += ok
        d[k][1] += 1
fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.8), gridspec_kw={"width_ratios": [1.5, 1]})
fig.subplots_adjust(left=0.2, right=0.96, top=0.76, bottom=0.12, wspace=0.55)
for ax, d, names, lab in ((axs[0], bt, TN, "유형"), (axs[1], br, RN, "저장소")):
    keys = list(names)[::-1]
    vals = [100 * d[k][0] / d[k][1] for k in keys]
    ax.barh(range(len(keys)), [100] * len(keys), color="#f1f3f5", height=0.6)
    ax.barh(range(len(keys)), vals, color=BLUE, height=0.6)
    for i, k in enumerate(keys):
        ax.text(min(vals[i], 100) + 2 if vals[i] < 80 else vals[i] - 2, i, f"{d[k][0]}/{d[k][1]}", va="center",
                ha="left" if vals[i] < 80 else "right", fontsize=13.8, color=INK if vals[i] < 80 else SURF)
    ax.set_yticks(range(len(keys)))
    ax.set_yticklabels([(k + " " + names[k]) if lab == "유형" else names[k] for k in keys], color=INK)
    ax.set_xlim(0, 100)
    ax.set_title(lab + "별", loc="left", fontsize=16, color=INK)
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.set_major_formatter(mt.FuncFormatter(lambda v, p: f"{v:.0f}%"))
tot = sum(v[0] for v in bt.values()), sum(v[1] for v in bt.values())
title(fig, f"F1 최종 평가 {tot[0]}/{tot[1]} ({100 * tot[0] / tot[1]:.1f}%): 버그 수정은 강하고 테스트 작성은 약하다",
      "튜닝에 쓰지 않은 저장소 4개 · Codex 출제 30과제 × 3회. 튜닝 담당 에이전트는 과제 내용을 보지 않았다", icon="flask-conical")
save(fig, "07_f1_by_type.png")

# 08 E2 디코드 속도 ---------------------------------------------------------
ctx = ["8K", "24K", "40K"]
e0, e2 = [57.7, 41.7, 26.8], [66.0, 57.0, 52.9]
fig, ax = plt.subplots(figsize=(8.5, 4.8))
fig.subplots_adjust(left=0.1, right=0.97, top=0.76, bottom=0.17)
w = 0.36
ax.bar([i - w / 2 - 0.01 for i in range(3)], e0, w, color=GRAY, label="E0 (원본 엔진)")
ax.bar([i + w / 2 + 0.01 for i in range(3)], e2, w, color=BLUE, label="E2 (디코드 어텐션 GQA 커널)")
for i in range(3):
    ax.text(i - w / 2 - 0.01, e0[i] + 1, f"{e0[i]:.1f}", ha="center", fontsize=13.8, color=INK2)
    ax.text(i + w / 2 + 0.01, e2[i] + 1, f"{e2[i]:.1f}", ha="center", fontsize=13.8, color=INK)
    ax.text(i + w / 2 + 0.01, e2[i] + 7, f"+{100 * (e2[i] / e0[i] - 1):.0f}%", ha="center", fontsize=14.5, color=BLUE, fontweight="bold")
ax.set_xticks(range(3))
ax.set_xticklabels([f"문맥 {c}" for c in ctx])
ax.set_ylabel("생성 속도 (tok/s)")
ax.set_ylim(0, 80)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=13.8)
title(fig, "긴 문맥일수록 빨라진 엔진 변경 E2, 출력은 비트 단위로 같다",
      "엔진 벤치 --bench-tg 128, 3회 중 2 · 3회차 평균. parity 10/10 · 긴 프롬프트 3/3 동일 확인 뒤 채택", icon="zap")
save(fig, "08_e2_decode_speed.png")

# 09 채택 · 보류 · 기각 전체 -------------------------------------------------
dec = [  # 라벨, 대조, 후보, n, 판정
    ("샘플링 card-coding", 9, 16, 30, "채택"), ("64K + 노력치 high", 17, 21, 30, "채택"), ("H9 줄 공백 무시 편집", 21, 24, 30, "채택"),
    ("H12 (Y 세트)", 21, 24, 30, "채택"), ("H12 (X3)", 24, 23, 30, "채택"), ("H7 편집 너그럽게", 16, 17, 30, "채택"),
    ("C1 (48회)", 19, 19, 48, "기각"), ("H8 체크 턴", 21, 20, 30, "보류"), ("노력치 xhigh", 21, 20, 30, "기각"),
    ("E3 엔진 (모델 시간 0.59배)", 24, 20, 30, "기각"), ("E1 턴 체크포인트 (prefill -76%)", 21, 17, 30, "보류"),
    ("T2 개요 · 심볼 도구", 21, 17, 30, "기각"), ("run_tests 기본값", 24, 21, 30, "기각"), ("L2 오래된 결과 지우기", 17, 14, 30, "기각"),
    ("노력치 medium", 17, 13, 30, "기각"), ("양자화 M1e", 16, 13, 30, "기각"), ("H3 페이지 + 재전송", 17, 12, 30, "기각"),
    ("양자화 M2", 16, 11, 30, "기각"), ("H2a 생각 재전송", 16, 8, 30, "기각"),
]
col = {"채택": BLUE, "보류": MUTED, "기각": ORANGE}
fig, ax = plt.subplots(figsize=(10, 8.2))
fig.subplots_adjust(left=0.3, right=0.8, top=0.87, bottom=0.1)
for i, (lab, c, k, n, o) in enumerate(dec):
    y = len(dec) - 1 - i
    cr, kr = 100 * c / n, 100 * k / n
    ax.plot([cr, kr], [y, y], color="#dee2e6", lw=2, zorder=1, solid_capstyle="round")
    ax.scatter([cr], [y], s=60, color=SURF, edgecolor=GRAY, lw=2, zorder=2)
    ax.scatter([kr], [y], s=75, color=col[o], edgecolor=SURF, lw=2, zorder=3)
    ax.text(102, y, f"{c} → {k} / {n}  {o}", va="center", fontsize=13.8, color=INK2, clip_on=False)
ax.set_yticks(range(len(dec)))
ax.set_yticklabels([d[0] for d in dec][::-1], color=INK, fontsize=14.5)
ax.set_xlim(0, 100)
ax.xaxis.set_major_formatter(mt.FuncFormatter(lambda v, p: f"{v:.0f}%"))
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.scatter([], [], s=60, color=SURF, edgecolor=GRAY, lw=2, label="대조군")
for o in ("채택", "보류", "기각"):
    ax.scatter([], [], s=75, color=col[o], label=f"후보 · {o}")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=4, frameon=False, fontsize=13.8)
title(fig, "30회 짝 비교로 판정한 변경 19개: 채택 6 · 보류 2 · 기각 11",
      "같은 seed 대조군과 비교. 일반 변경은 대조 -1 이내 · 회귀 증가 없음, 엔진 변경은 숨은 테스트 합 95% 이상이어야 채택", icon="scale")
save(fig, "09_decisions.png")

# 10 원장이 쌓이는 모습 -------------------------------------------------------
ts = sorted(datetime.strptime(f[0], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=9) for f in rows)
fig, ax = plt.subplots(figsize=(10, 4.6))
fig.subplots_adjust(left=0.08, right=0.97, top=0.78, bottom=0.14)
ax.step(ts, range(1, len(ts) + 1), where="post", color=BLUE, lw=2)
ax.fill_between(ts, range(1, len(ts) + 1), step="post", color=BLUE, alpha=0.12)
night = [(datetime(2026, 11, d, 22), datetime(2026, 11, d + 1, 8)) for d in range(18, 25)]
for a, b in night:
    ax.axvspan(a, b, color="#f1f3f5", zorder=0)
ax.xaxis.set_major_locator(md.DayLocator())
ax.xaxis.set_major_formatter(md.DateFormatter("%m-%d"))
ax.set_ylabel("원장 행 (누적)")
ax.grid(axis="x", visible=False)
ax.text(0.01, 0.92, f"총 {len(ts):,}행 · 회색 띠 = 밤(22~08시) 무인 체인", transform=ax.transAxes, fontsize=13.8, color=INK2)
title(fig, "8일 동안 원장에 쌓인 실험 1,554회",
      "한 행 = 한 번의 측정(모델 sha256 · 엔진 커밋 · 설정 해시 · 결과). 밤에도 WMI 로 띄운 체인이 계속 쌓았다", icon="book-open")
save(fig, "10_ledger_growth.png")

# 11 F1 체인 실행 타임라인 ----------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 4.4))
fig.subplots_adjust(left=0.1, right=0.97, top=0.76, bottom=0.16)
order = ["attrs", "click", "du", "pluggy"]
for f in f1:
    m = re.match(r"f1_m0_e2_s0_ctx64k_nav_(f\d)_(attrs|click|du|pluggy)_", f[1])
    end = datetime.strptime(f[0], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=9)
    wall = float(note(f, "wall_ms") or 0) / 1000
    ok = note(f, "error_type") == "pass"
    y = order.index(m.group(2))
    ax.barh(y, timedelta(seconds=wall), left=end - timedelta(seconds=wall), height=0.6, color=BLUE if ok else ORANGE, edgecolor=SURF, lw=1)
ax.set_yticks(range(4))
ax.set_yticklabels([RN[o] for o in order], color=INK)
ax.invert_yaxis()
ax.xaxis.set_major_locator(md.HourLocator())
ax.xaxis.set_major_formatter(md.DateFormatter("%H:%M"))
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label="통과"), Patch(color=ORANGE, label="실패")],loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=13.8)
title(fig, "F1 체인 11-25 09:01~17:29: 실행 90회의 시간과 결과",
      "막대 하나 = 실행 한 번(길이 = 모델 + 도구 + 채점 시간). 저장소 사이의 빈칸은 서버 재기동 · 모드 전환. 마지막 click 1회는 채점기 수정 뒤 재실행", icon="timer")
save(fig, "11_f1_timeline.png")
print("ok 06~11", len(rows), len(f1), tot)
