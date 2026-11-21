# STRATA q36 프롬프트 expert 커널 경로 · RTX 5070 Ti 지원 형식 (11-21)

계기: Q1-0c 에서 M1a · M1b 의 긴 입력 PP 가 −44% · −23% 로 떨어졌다(q1-plan 13절). 엔진 로그는 `prompt experts on the native grouped kernels`(M0 는 `fused int8 kernels`). 사용자 요청으로 엔진 소스와 그래픽 카드를 자세히 확인했다.
출처 표시: [소스] = `C:\strata-lab\engine` (E0 c775728) 파일:줄, [기기] = 이 본체에서 직접 조회, [측정] = 원장 · 엔진 로그.

## 1. 그래픽 카드 (실물 확인) [기기]

| 항목 | 값 | 확인 방법 |
|---|---|---|
| 이름 | **NVIDIA GeForce RTX 5070 Ti** (지금까지 문서의 '5070' 표기는 Ti 가 빠진 것) | nvidia-smi |
| 컴퓨트 능력 | **12.0 (sm_120, Blackwell 소비자형)** | nvidia-smi `compute_cap`, CUDA driver |
| SM 수 | **70** | `cuDeviceGetAttribute(MULTIPROCESSOR_COUNT)` |
| VRAM | 16,303 MiB GDDR7, 256-bit, 메모리 클럭 14,001 MHz(28 Gbps → 약 896 GB/s) | nvidia-smi, CUDA driver |
| L2 | 48 MB | CUDA driver |
| 블록당 공유 메모리(opt-in) / SM 당 | 99 KB / 100 KB | CUDA driver |
| SM 당 레지스터 | 65,536 | CUDA driver |
| 최대 SM 클럭 · 전력 한도 | 3,090 MHz · 300 W | nvidia-smi |
| PCIe | Gen 5 x16 (최대) | nvidia-smi |
| 드라이버 | 616.92 | nvidia-smi |

- 엔진 빌드: `CMAKE_CUDA_ARCHITECTURES=120`, **`STRATA_MMQ=OFF`**(llama.cpp MMQ 없음), `STRATA_NATIVE_EXPERTS=ON` [소스 `build\CMakeCache.txt`]. 쓰는 실행 파일 `engine\engine\strata.exe` 는 `build\strata.exe` 와 크기 같음(66,781,696 B, 11-18 10:23).
- 엔진 규칙이 카드를 나누는 기준: sm_86 계열 · sm_120 이고 **SM 80개 이상이면 항상**, 40~79개면 '가중치 스테이징 gate/up + 정해진 down' 조합만 [소스 `include/strata/prefill/fused_tile_rule.hpp:139`]. 5070 Ti(70 SM)는 아래쪽 등급이다. 다만 이 빌드는 MMQ 가 없어 시작할 때 `STRATA_PF_FUSED=1` 을 스스로 켜므로(`q36_engine.cu:3964-3972`) 카드 등급 규칙을 건너뛰고 **'커널이 그 조합을 덮으면 항상 fused'** 가 된다(`fused_tile_rule.hpp:178` `env > 0 → true`). 같이 켜는 것: `STRATA_PF_FUSED_KQ` · `_Q6K` · `_Q8GU` = 1 (`q36_engine.cu:3952`).

## 2. 프롬프트 expert 경로 고르기 [소스]

`q36_engine.cu:1396-1486`, `include/strata/kernels/q36_prompt_route.hpp`:

1. 층마다(MTP 블록 포함) 순서대로: **fused int8**(`FQ::native_layer_ext(gate/up 형식, down 형식)`) → 우리 int8(`native_expert_i8`, 스위치 1일 때) → MMQ(**이 빌드엔 없음**) → 우리 int8 → **grouped**.
2. **한 층이라도 grouped 이면 모든 층 · 모든 프롬프트 청크가 grouped 로 간다** — `q36_prompt_path_ok(n, n_grouped) = n_grouped == 0` (`q36_prompt_route.hpp:34`, 주석: '엔진은 모델당 프롬프트 경로 하나'). 이번 PP 하락의 직접 원인.
3. 로그 문구로 구분: `fused int8 kernels`(전 층 fused) / `fused int8 kernels (a of n layers), the rest on MMQ` / `a of n layers on the fused int8 kernels, b on our int8 kernels` / `native grouped kernels`(낭떠러지).

## 3. 형식별 지원 (CUDA, 이 빌드 · 이 카드) [소스]

ggml 형식 번호: Q5_0 6 · Q5_1 7 · Q8_0 8 · Q4_K 12 · Q5_K 13 · Q6_K 14 · IQ2_XXS 16 · IQ2_XS 17 · IQ3_XXS 18 · IQ4_NL 20 · IQ3_S 21 · IQ2_S 22 · IQ4_XS 23 · Q2_0 42.

**(a) fused int8 커널** — gate/up 와 down 의 '짝' 으로 정해진다 (`src/prefill/moe_fused_iq.cu:2565-2704, 2891-3040`, `moe_fused_iq_q36.cu:110-141`):

| gate/up | down | 이 빌드 기본 | 근거 |
|---|---|---|---|
| IQ2_XXS · IQ2_XS · IQ2_S · IQ3_XXS · IQ3_S · **IQ4_XS** | **IQ4_NL** · Q2_0 | **fused** | `gu_covered` · `d_covered`(down 은 Q2_0 · IQ4_NL 만) |
| Q4_K · Q5_K | **Q5_K · Q6_K** (M0 = UD-Q4_K_XL) | fused | `is_kq_down_pair` + kq 커널 준비(`native_supported_ext`) |
| Q4_K · Q5_K | Q5_1 · Q8_0 | fused | kq · kq8 |
| Q6_K | Q8_0 | fused (`_Q6K=1` 를 엔진이 켬) | `moe_fused_iq.cu:2925` |
| Q8_0 | Q8_0 | fused (`_Q8GU=1`) | `:2920` |
| i-quant | Q8_0 | `STRATA_PF_FUSED_Q8D=1` 일 때만 | `:2950` |
| 아무거나 | Q5_0 | `STRATA_PF_FUSED_Q50=1` 일 때만 | `:2962` |
| NVFP4 | NVFP4 | 조건부(Blackwell FP4 계열, 모델 형식 따로 필요) | `:2945` |
| 아무거나 | **IQ4_XS** | **없음** | `d_covered` 에 없음 |
| Q4_K · Q5_K | IQ4_NL · IQ4_XS | **없음** | K-quant gate 는 Q5_1 · Q8_0 · Q5_K · Q6_K down 만 |

**(b) 우리 int8 커널(`native_expert_i8`)** — 형식 각각 (`src/kernels/cuda/i8_expert.cuh:61-62`, `iq_kernels.cu:6330`):
- gate/up: IQ2_XXS · IQ2_XS · IQ3_XXS · IQ3_S · IQ2_S · IQ4_XS · Q2_0 · Q4_K · Q5_K · Q6_K · Q8_0 (+29)
- down: **IQ4_NL · Q2_0 · Q5_0 · Q8_0 · Q5_1 · Q5_K · Q6_K** — **IQ4_XS 없음**
- 그 밖에 n_ff % 128(Q5_K · Q6_K down 은 % 256), 공유 메모리 한도(카드 99 KB) 조건. Qwen3.6(n_embd 2048, n_ff 512)은 통과.

**(c) MMQ** — 이 빌드에 없음(`STRATA_MMQ=OFF`, `mmq_absent.cpp`: `supported() = false`). 있었다면 IQ4_XS 도 받았다(`moe_mmq.cu:211-218`).

**(d) CPU 풀(하이브리드, VRAM 밖 expert)** — 전용 SIMD 짝 목록에 iq4_xs/iq4_nl 은 있고 iq4_xs down 은 없다. IQ4_XS 는 일부러 ggml 일반 dot 을 쓴다(`src/kernels/cpu/iq_avx1.cpp:396-398`, 그쪽이 더 빠르다는 주석). CPU 쪽이 출력 tok/s 하락에 얼마나 기여했는지는 **분리 안 함**.

## 4. 이번 후보에 적용 [소스 + 측정]

| 후보 | 주된 층 짝 (gate/up / down) | 경로 | 측정 PP (1.97만 토큰) |
|---|---|---|---|
| M0 | Q4_K / Q5_K · Q6_K | 전 층 fused | 1,515 tok/s |
| M1b | IQ4_XS / **IQ4_XS** (34 · 38 층 IQ4_XS / Q6_K, 39 층 Q5_K / Q6_K) | IQ4_XS down 층이 fused · int8 모두 불가 → grouped → **전 층 grouped** | 1,169 (−23%) |
| M1a | Q4_K / **IQ4_XS** | 같음 → 전 층 grouped | 843 (−44%) |

- M1a 가 M1b 보다 느린 것은 grouped 커널에서 Q4_K gate/up 디코드가 IQ4_XS 보다 느린 탓으로 보이나 **확인 안 함**.
- 원인은 '양자화가 무거워서' 가 아니라 **down 형식 하나(IQ4_XS)가 엔진의 빠른 커널 목록에 없어서** 다.

## 5. 고칠 길 (제안, 아직 안 함)

1. **M1e = gate/up IQ4_XS + down IQ4_NL** (나머지 M1b 와 같음): 주된 층이 fused 표의 첫 줄 짝이 된다. 이 짝은 엔진 쪽 측정 근거가 있다(RTX A4000 한 층, 스테이징 128행 타일 대 MMQ 2K/8K/20K/32K 에서 1.62 / 1.33 / 1.18 / 1.06배, `fused_tile_rule.hpp:135`). 34 · 38 층(IQ4_XS / Q6_K)은 int8 경로(grouped 아님), 39 층(Q5_K / Q6_K)은 fused. 크기: down 0.25 bpw 증가 ≈ 층당 8.4 MB, 약 +0.3 GiB(expert 16.6 → 약 16.9 GiB, 슬롯 약 86 예상).
   - 34 · 38 층까지 fused 로 하려면 그 두 층 gate/up 을 Q4_K 로(K-quant 짝) 둘 수 있다(+수십 MB).
2. M1a 계열(Q4_K gate)은 down 을 IQ4_NL 로 바꿔도 fused 가 안 된다(K-quant gate 는 IQ4_NL down 짝이 없음) → int8 경로. 이득이 작아 후보에서 뺀다.
3. 엔진을 MMQ 포함으로 다시 빌드(`STRATA_MMQ=ON`)하면 IQ4_XS down 층이 MMQ 로 가서 낭떠러지는 피한다. 엔진 변경(E1 성격)이라 뒤로.
4. 확인 순서(싸게): M1e 생성(서버 없이 약 5분) → 엔진 로그가 `fused int8 kernels` 인지 + PP 탐침(약 5분) → G2 KL(같은 기준 로짓) → G3. PP 가 M0 근처로 돌아오면 G4 후보는 M1e.
