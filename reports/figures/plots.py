import json, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mt

here = os.path.dirname(os.path.abspath(__file__))
out = here
os.makedirs(out, exist_ok=True)
plt.rcParams.update({"font.family": "Malgun Gothic", "axes.unicode_minus": False, "font.size": 11,
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb",
    "axes.edgecolor": "#c9c8c2", "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e",
    "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e8e7e2", "grid.linewidth": 0.8})
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
BLUE, ORANGE, AQUA, GRAY = "#2a78d6", "#eb6834", "#1baf7a", "#b4b2aa"


def title(fig, t, s):
    fig.text(0.02, 0.975, t, fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.905, s, fontsize=10, color=INK2, va="top")


def save(fig, name):
    fig.savefig(os.path.join(out, name), dpi=200)
    plt.close(fig)


# A. 30-run confirmations: candidate vs control
rows = [  # label, control, cand, n, outcome
    ("샘플링 card-coding", 9, 16, 30, "채택"),
    ("H7 편집 적용 너그럽게", 16, 17, 30, "채택"),
    ("64K 컨텍스트", 17, 21, 30, "채택"),
    ("run_tests 도구", 16, 16, 30, "효과 없음"),
    ("C1 (48회)", 19, 19, 48, "효과 없음"),
    ("L2 오래된 도구 결과 지우기", 17, 14, 30, "기각"),
    ("H3 페이지 나누기 + 재전송", 17, 12, 30, "기각"),
    ("H2a thinking 재전송", 16, 8, 30, "기각"),
    ("양자화 M1e", 16, 13, 30, "기각"),
    ("양자화 M2", 16, 11, 30, "기각"),
]
col = {"채택": BLUE, "효과 없음": MUTED, "기각": ORANGE}
fig, ax = plt.subplots(figsize=(9.5, 6.4))
fig.subplots_adjust(left=0.26, right=0.80, top=0.82, bottom=0.13)
for i, (lab, c, k, n, o) in enumerate(rows):
    y = len(rows) - 1 - i
    cr, kr = 100 * c / n, 100 * k / n
    ax.plot([cr, kr], [y, y], color="#d6d5cf", lw=2, zorder=1, solid_capstyle="round")
    ax.scatter([cr], [y], s=70, color="#fcfcfb", edgecolor=GRAY, lw=2, zorder=2)
    ax.scatter([kr], [y], s=80, color=col[o], edgecolor="#fcfcfb", lw=2, zorder=3)
    ax.text(102, y, f"{c} → {k} / {n}  {o}", va="center", fontsize=9.5, color=INK2, clip_on=False)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows][::-1], color=INK)
ax.set_xlim(0, 100)
ax.set_xlabel("통과율 (%)")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.scatter([], [], s=70, color="#fcfcfb", edgecolor=GRAY, lw=2, label="대조군")
for o in ("채택", "효과 없음", "기각"):
    ax.scatter([], [], s=80, color=col[o], label=f"후보 · {o}")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=4, frameon=False, fontsize=9.5)
title(fig, "30회 확인을 통과한 변경은 셋뿐이었다",
      "후보마다 같은 seed(42~46)의 대조군과 6과제 × 5회로 비교. 30회에서 ±7회 안쪽 차이는 우연으로도 나온다")
save(fig, "01_harness_confirmations.png")


# B. per-turn cache: H0 vs H2a
def load(n):
    return json.load(open(os.path.join(here, f"turns_{n}.json"), encoding="utf-8"))


fig, axs = plt.subplots(1, 2, figsize=(10, 4.9), sharey=True)
fig.subplots_adjust(left=0.08, right=0.98, top=0.76, bottom=0.18, wspace=0.08)
for ax, (n, lab) in zip(axs, (("x3s1c", "H0: 이전 답을 thinking 없이 보냄"), ("x3h2k", "H2a: thinking까지 그대로 다시 보냄"))):
    t = load(n)
    x = [d["step"] + 1 for d in t]
    cached = [d.get("cached_tokens") or 0 for d in t]
    new = [d["prompt_tokens"] - c for d, c in zip(t, cached)]
    ax.bar(x, cached, color=BLUE, width=0.8, label="캐시에서 재사용")
    ax.bar(x, new, bottom=cached, color=ORANGE, width=0.8, label="처음부터 다시 읽음", edgecolor="#fcfcfb", lw=1)
    ax.set_title(lab, fontsize=11, color=INK, loc="left")
    ax.set_xlabel("턴")
    ax.xaxis.set_major_locator(mt.MaxNLocator(integer=True))
    ax.grid(axis="x", visible=False)
    ax.text(0.02, 0.93, f"다시 읽은 토큰 {sum(new)/1000:.0f}K / 입력 합계 {sum(d['prompt_tokens'] for d in t)/1000:.0f}K",
            transform=ax.transAxes, fontsize=9.5, color=INK2)
axs[0].yaxis.set_major_formatter(mt.FuncFormatter(lambda v, p: f"{v/1000:.0f}K"))
axs[1].annotate("강제 마지막 턴: 도구 목록이 빠져\n앞부분이 달라짐", xy=(len(load("x3h2k")) - 0.4, 23800), xytext=(0.04, 0.76), textcoords="axes fraction", fontsize=9, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=1))
axs[1].legend(loc="upper center", bbox_to_anchor=(-0.04, -0.14), ncol=2, frameon=False)
title(fig, "이전 답을 다르게 보내면 매 턴 처음부터 다시 읽는다",
      "같은 과제(dg_group_names) 1회차의 턴별 입력. 엔진은 들고 있는 토큰 전체가 그대로 이어질 때만 재사용한다")
save(fig, "02_cache_per_turn.png")

# C. 32K vs 64K
mets = [("통과 (/30)", 17, 21, "{:.0f}"), ("과제당 도구 호출", 11.1, 16.5, "{:.1f}"),
        ("호출당 thinking 토큰", 604, 672, "{:.0f}"), ("호출당 시간 (초)", 21.2, 29.0, "{:.1f}")]
fig, axs = plt.subplots(1, 4, figsize=(10.5, 4.1))
fig.subplots_adjust(left=0.03, right=0.99, top=0.7, bottom=0.1, wspace=0.3)
for ax, (lab, a, b, f) in zip(axs, mets):
    ax.bar([0, 1], [a, b], color=[GRAY, BLUE], width=0.62, edgecolor="#fcfcfb", lw=2)
    for xx, v in ((0, a), (1, b)):
        ax.text(xx, v, f.format(v), ha="center", va="bottom", fontsize=10.5, color=INK)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["32K", "64K"])
    ax.set_title(lab, fontsize=10.5, color=INK)
    ax.set_ylim(0, max(a, b) * 1.25)
    ax.grid(visible=False)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.text(0.98, 0.98, f"{(b - a) / a * 100:+.0f}%", transform=ax.transAxes, ha="right", va="top", fontsize=10, color=INK2)
title(fig, "64K에서 더 푼 건 오래 생각해서가 아니라 더 많이 찾아봐서였다",
      "M0 · H7 · card-coding, 6과제 × 5회. 호출당 thinking은 거의 그대로인데 도구 호출이 약 1.5배로 늘었다")
save(fig, "03_ctx32k_vs_64k.png")

# D. felt time per task
tasks = [("version_bump", 2.4, 3.6, "4/5", 100), ("tags_platform", 5.7, 7.1, "5/5", 189),
         ("dg_group_names", 6.3, 7.5, "5/5", 325), ("marker_extras", 6.9, 9.8, "4/5", 332),
         ("specifier_bounds", 14.9, 19.7, "3/5", 412), ("metadata_extra", 16.6, 22.7, "0/5", 426)]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 5), sharey=True, gridspec_kw={"width_ratios": [1.4, 1]})
fig.subplots_adjust(left=0.15, right=0.97, top=0.76, bottom=0.13, wspace=0.08)
ys = list(range(len(tasks)))[::-1]
for y, (n, avg, worst, ok, tok) in zip(ys, tasks):
    a1.barh(y, avg, color=BLUE, height=0.55)
    a1.plot([avg, worst], [y, y], color=INK2, lw=1.4)
    a1.plot([worst], [y], "|", color=INK2, ms=10, mew=1.6)
    a1.text(worst + 0.6, y, f"{avg:g}분 (최악 {worst:g}) · {ok}", va="center", fontsize=9, color=INK2)
    a2.barh(y, tok, color=AQUA, height=0.55)
    a2.text(tok + 10, y, f"{tok:,}K", va="center", fontsize=9, color=INK2)
a1.set_yticks(ys)
a1.set_yticklabels([t[0] for t in tasks], color=INK)
a1.tick_params(axis="y", length=0)
a1.set_xlim(0, 36)
a1.set_xlabel("분")
a1.grid(axis="y", visible=False)
a2.set_xlim(0, 560)
a2.set_xlabel("K 토큰")
a2.grid(axis="y", visible=False)
a1.set_title("회당 시간 (막대 = 평균, 선 끝 = 최악) · 통과", fontsize=10.5, color=INK, loc="left")
a2.set_title("처리한 입력 토큰", fontsize=10.5, color=INK, loc="left")
title(fig, "쉬운 과제는 몇 분, 어려운 과제는 15분 넘게 걸리고도 자주 실패",
      "64K 서버 · 노력치 high 한 번 (x3k64h7 실측, 6과제 × 5회). 시간 = 모델 + 도구 + 테스트, 통과 = 엄격 기준")
save(fig, "04_felt_time_by_task.png")

# E. quant
q = [("M0 (기준)", 100, "16/30", GRAY), ("M1a", 56, "G4 전 정지", ORANGE), ("M1b", 77, "G4 전 정지", ORANGE),
     ("M1e", 111, "13/30", BLUE), ("M2", 96.5, "11/30", BLUE)]
fig, ax = plt.subplots(figsize=(9, 4.8))
fig.subplots_adjust(left=0.09, right=0.98, top=0.76, bottom=0.2)
for i, (n, v, p, c) in enumerate(q):
    ax.bar(i, v, color=c, width=0.6, edgecolor="#fcfcfb", lw=2)
    ax.text(i, (102.5 if 90 <= v < 100 else v + 2.5), f"{v:g}%", ha="center", fontsize=10.5, color=INK)
    ax.text(i, -19, f"X3 {p}", ha="center", fontsize=9, color=INK2)
ax.axhline(100, color=MUTED, lw=1, ls="--")
ax.set_xticks(range(len(q)))
ax.set_xticklabels([x[0] for x in q], color=INK)
ax.set_ylim(0, 128)
ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, p: f"{v:.0f}%"))
ax.set_title("긴 입력 처리 속도 (M0 = 100%), 아래는 X3 30회 통과", fontsize=10.5, color=INK, loc="left")
ax.grid(axis="x", visible=False)
ax.tick_params(axis="x", length=0)
title(fig, "형식 하나 때문에 느린 커널로 빠졌다가, 고치니 기준보다 빨라졌다",
      "M1a · M1b는 down 층 형식이 엔진의 빠른 커널 목록 밖. M1e는 그 층만 바꿔 39/41층이 빠른 경로 (품질 관문 G4에서는 탈락)")
save(fig, "05_quant_prefill_speed.png")
print("ok", sorted(os.listdir(out)))
