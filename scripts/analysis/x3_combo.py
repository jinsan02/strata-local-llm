"""X3 전체 기록 조합 분석 (11-21, docs/combo-analysis-20261121.md). 원장 + 실행 config -> 데이터셋 -> 과제 보정 베이즈 로지스틱 -> 그리드.
서버 없음, numpy 만. 산출물은 work/stage/ 에 쓴다. python x3_combo.py"""
# ── 1. 데이터셋 ──
import csv, json, re, glob, os, collections, hashlib
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.repo import error_type_of  # noqa: E402
R=Path(__file__).resolve().parents[2].as_posix()+"/"
rows=list(csv.DictReader(open(R+"experiments/LEDGER.tsv",encoding="utf-8"),delimiter="\t"))
cfgcache={}
out=[]; miss=collections.Counter()
for r in rows:
    rid=r["run_id"]
    if not rid.startswith("x3"): continue
    run=re.sub(r"_r\d+$","",rid)
    p=R+"experiments/runs/"+run+"/config.json"
    if p not in cfgcache:
        cfgcache[p]=json.load(open(p,encoding="utf-8")) if os.path.exists(p) else None
        if cfgcache[p] is not None:
            cfgcache[p]["_sha"]=hashlib.sha256(open(p,"rb").read()).hexdigest()
    cfg=cfgcache[p]
    et = error_type_of(r["note"]) or "?"
    tp=r["tests_passed"]
    if cfg is None: miss["nocfg"]+=1; continue
    mode=cfg.get("mode","?")
    sc=cfg.get("server_config") or {}
    rec=dict(run_id=rid, set=rid.split("_")[0], task=cfg.get("task"), mode=mode, et=et, tp=tp,
        pass_=int(et=="pass"), model=r["model_id"], ctx=r["ctx"], harness=cfg.get("harness"),
        sampling=cfg.get("sampling") if isinstance(cfg.get("sampling"),str) else json.dumps(cfg.get("sampling"),sort_keys=True)[:80],
        edit_apply=cfg.get("edit_apply","strict"), mask=cfg.get("mask","off"), echo=cfg.get("reasoning_echo","none"),
        final_turn=cfg.get("final_turn","none"), run_tests=cfg.get("run_tests","off"), edit_hint=cfg.get("edit_hint","off"),
        reread=cfg.get("reread_guard","off"), tool_out=cfg.get("tool_out","chars"), budget=cfg.get("budget"),
        rbudget=cfg.get("reasoning_budget"), limit=cfg.get("tool_out_limit"), seedp=cfg.get("seed_policy","none") if not isinstance(cfg.get("seed_policy"),dict) else "per_rep",
        mtp=r["mtp"], cfg_match=int(cfg["_sha"]==r["config_sha256"]), day=r["ts_utc"][:10], commit=r["git_commit"][:7])
    out.append(rec)
print("loaded",len(out),dict(miss))
json.dump(out,open(R+"work/stage/x3_dataset.json","w",encoding="utf-8"),ensure_ascii=False)
c=collections.Counter((x["mode"]) for x in out); print(c)
print("cfg mismatch", sum(1 for x in out if not x["cfg_match"]), collections.Counter(x["set"] for x in out if not x["cfg_match"]).most_common(20))
print("samplings", collections.Counter(x["sampling"] for x in out))
print("models", collections.Counter(x["model"] for x in out), "ctx", collections.Counter(x["ctx"] for x in out))
print("tasks", collections.Counter(x["task"] for x in out))
print("et", collections.Counter(x["et"] for x in out))

# ── 2. 조합별 집계 ──
import json, re, collections, math
R=Path(__file__).resolve().parents[2].as_posix()+"/"
D=json.load(open(R+"work/stage/x3_dataset.json",encoding="utf-8"))
TASKS=["dg_group_names","marker_extras","version_bump","tags_platform_filter","metadata_extra_dupes","specifier_bounds"]
def samp(s):
    j=s
    t=re.search(r'"temperature": ([\d.]+)',j).group(1); pp=re.search(r'"presence_penalty": ([\d.]+)',j).group(1)
    return {"1.0/1.5":"card-general","0.6/0.0":"card-coding","0.0/0.0":"greedy"}.get(t+"/"+pp, t+"/"+pp)
for x in D:
    x["samp"]=samp(x["sampling"])
    if not x["task"]:
        x["task"]=next((t for t in TASKS if t in x["run_id"]),None)
F=["model","ctx","harness","samp","edit_apply","mask","echo","final_turn","run_tests","edit_hint","reread","tool_out","budget","rbudget","limit"]
def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return (c-h,c+h)
g=collections.defaultdict(list)
for x in D: g[tuple(x[f] for f in F)].append(x)
print("signatures",len(g))
rows=[]
for sig,xs in g.items():
    sets=sorted(set(x["set"] for x in xs)); tk=collections.Counter(x["task"] for x in xs)
    k=sum(x["pass_"] for x in xs); n=len(xs)
    # 6-task balanced score: mean per-task pass rate over tasks present
    per={t:(sum(x["pass_"] for x in xs if x["task"]==t),tk[t]) for t in TASKS if tk[t]}
    rows.append((sig,sets,k,n,per))
diff=lambda sig: ", ".join(f"{f}={v}" for f,v in zip(F,sig) if v not in ("M0","32768","H0","card-general","strict","off","none","none","chars",8192,None,12000,"off"))
for sig,sets,k,n,per in sorted(rows,key=lambda r:-r[3]):
    lo,hi=wilson(k,n)
    print(f"{k:3}/{n:<3} {k/n:5.2f} [{lo:.2f}-{hi:.2f}] {'+'.join(sets)[:40]:40} | {diff(sig) or 'BASE'} | "+" ".join(f"{t[:4]}{a}/{b}" for t,(a,b) in per.items()))
json.dump(D,open(R+"work/stage/x3_dataset2.json","w",encoding="utf-8"),ensure_ascii=False)

# ── 3. 모델 · 그리드 ──
import json, itertools, numpy as np, collections
R=Path(__file__).resolve().parents[2].as_posix()+"/"
D=json.load(open(R+"work/stage/x3_dataset2.json",encoding="utf-8"))
TASKS=["dg_group_names","marker_extras","version_bump","tags_platform_filter","metadata_extra_dupes","specifier_bounds"]
D=[x for x in D if x["task"] in TASKS and x["set"] not in ("x3q","x3n")]
print("rows",len(D))
FEATS={
 "samp=coding": lambda x: x["samp"]=="card-coding",
 "samp=greedy": lambda x: x["samp"]=="greedy",
 "tool_out=paged(H1)": lambda x: x["tool_out"]=="paged",
 "echo=all(H2a)": lambda x: x["echo"]=="all",
 "echo=last(H2b)": lambda x: x["echo"]=="last",
 "echo_all x coding": lambda x: x["echo"]=="all" and x["samp"]=="card-coding",
 "reread=on(C1)": lambda x: x["reread"]=="on",
 "run_tests=on": lambda x: x["run_tests"]=="on",
 "edit_hint=on(H6)": lambda x: x["edit_hint"]=="on",
 "final_turn=edit(H4)": lambda x: x["final_turn"]=="edit",
 "budget=16K(T1)": lambda x: x["budget"]==16384,
 "rbudget=3072": lambda x: x["rbudget"]==3072,
 "edit_apply=lenient(H7)": lambda x: x["edit_apply"]=="lenient",
 "mask=on(L2)": lambda x: x["mask"]=="on",
 "ctx=64K": lambda x: x["ctx"]=="65536",
 "model=M1e": lambda x: x["model"]=="M1e",
 "model=M2": lambda x: x["model"]=="M2",
 "model=M1a": lambda x: x["model"]=="M1a",
 "model=M1b": lambda x: x["model"]=="M1b",
}
names=[f"task:{t}" for t in TASKS]+list(FEATS)
def row(x): return [1.0*(x["task"]==t) for t in TASKS]+[1.0*bool(f(x)) for f in FEATS.values()]
X=np.array([row(x) for x in D]); y=np.array([x["pass_"] for x in D],float)
lam=np.array([0.01]*len(TASKS)+[1.0]*len(FEATS))   # 약한 ridge (특성 계수 ~ N(0,1) 사전분포)
b=np.zeros(X.shape[1])
for _ in range(100):
    p=1/(1+np.exp(-X@b)); W=p*(1-p)
    H=X.T@(X*W[:,None])+np.diag(lam); g=X.T@(y-p)-lam*b
    step=np.linalg.solve(H,g); b+=step
    if np.abs(step).max()<1e-8: break
Cov=np.linalg.inv(H); se=np.sqrt(np.diag(Cov))
n_on={k:int(X[:,len(TASKS)+i].sum()) for i,k in enumerate(FEATS)}
print("\n== 요인 효과 (로그 오즈, 과제 효과 보정, ridge 사전분포 N(0,1)) ==")
for i,nm in enumerate(names):
    tag=""
    if i>=len(TASKS):
        z=b[i]/se[i]; tag=f"n={n_on[nm]:3}  z={z:+.2f}  P(>0)={0.5*(1+__import__('math').erf(z/2**0.5)):.2f}"
    print(f"{nm:28} {b[i]:+.2f} ± {se[i]:.2f}  {tag}")
# 기준(H7 + coding)에서 과제 평균 통과 확률
def prob6(feat_on, bb):
    v=np.zeros(len(names))
    for k in feat_on: v[names.index(k)]=1
    ps=[]
    for t in TASKS:
        vv=v.copy(); vv[names.index("task:"+t)]=1; ps.append(1/(1+np.exp(-vv@bb)))
    return float(np.mean(ps))
# 그리드: 운영 후보 요인만 (모델은 M0 고정, 양자화 탈락)
grid_axes={"samp":["general","coding","greedy"],"paged":[0,1],"lenient":[0,1],"reread":[0,1],"ft_edit":[0,1],"ctx64":[0,1],"mask":[0,1],"rt":[0,1]}
def feats(c):
    f=[]
    if c["samp"]=="coding": f.append("samp=coding")
    if c["samp"]=="greedy": f.append("samp=greedy")
    if c["paged"]: f.append("tool_out=paged(H1)")
    if c["lenient"]: f.append("edit_apply=lenient(H7)")
    if c["reread"]: f.append("reread=on(C1)")
    if c["ft_edit"]: f.append("final_turn=edit(H4)")
    if c["ctx64"]: f.append("ctx=64K")
    if c["mask"]: f.append("mask=on(L2)")
    if c["rt"]: f.append("run_tests=on")
    return f
# 함께 관측된 적 있는 요인 쌍 (외삽 표시)
obs=set()
for x in D:
    on=[k for k,f in FEATS.items() if f(x)]
    for a in on:
        for c2 in on: obs.add((a,c2))
rng=np.random.default_rng(0); S=rng.multivariate_normal(b,Cov,size=4000)
base=["samp=coding","edit_apply=lenient(H7)"]
keys=list(grid_axes); res=[]
for vals in itertools.product(*grid_axes.values()):
    c=dict(zip(keys,vals)); f=feats(c)
    if c["mask"] and c["ctx64"]: continue
    pm=prob6(f,b)
    sims=np.array([prob6(f,s) for s in S[:600]]); bs=np.array([prob6(base,s) for s in S[:600]])
    extra=[(a,c2) for a in f for c2 in f if a<c2 and (a,c2) not in obs]
    res.append((pm, float((sims>bs).mean()), float(np.percentile(sims,5)), float(np.percentile(sims,95)), f, len(extra)))
res.sort(key=lambda r:-r[0])
print("\n== 그리드 (M0, 6과제 평균 통과 확률 예측; P(>H7) = 지금 기준보다 나을 사후확률; 외삽 = 함께 잰 적 없는 요인 쌍 수) ==")
print(f"현재 기준 H7+coding: {prob6(base,b):.3f} (x30 = {30*prob6(base,b):.1f})")
for pm,pb,lo,hi,f,ex in res[:20]:
    print(f"{pm:.3f} (x30={30*pm:4.1f}) [{lo:.2f}-{hi:.2f}] P(>H7)={pb:.2f} 외삽{ex} | {' + '.join(f) or 'general 기본'}")
print("...\n관측된 조합만 (외삽 0):")
for pm,pb,lo,hi,f,ex in [r for r in res if r[5]==0][:10]:
    print(f"{pm:.3f} (x30={30*pm:4.1f}) [{lo:.2f}-{hi:.2f}] P(>H7)={pb:.2f} | {' + '.join(f) or 'general 기본'}")
print("\n== 후보 지정 ==")
for f in [["samp=coding","edit_apply=lenient(H7)","tool_out=paged(H1)"],["samp=greedy","edit_apply=lenient(H7)"],["samp=greedy","edit_apply=lenient(H7)","ctx=64K"],["samp=coding","edit_apply=lenient(H7)","tool_out=paged(H1)","ctx=64K"],["samp=greedy","edit_apply=lenient(H7)","tool_out=paged(H1)","ctx=64K"]]:
    sims=np.array([prob6(f,s) for s in S[:1500]]); bs=np.array([prob6(base,s) for s in S[:1500]])
    ex=[(a,c2) for a in f for c2 in f if a<c2 and (a,c2) not in obs]
    print(f"{prob6(f,b)*30:4.1f}/30 [{np.percentile(sims,5)*30:.1f}-{np.percentile(sims,95)*30:.1f}] P(>H7)={(sims>bs).mean():.2f} 외삽{len(ex)} | {' + '.join(f)}")
