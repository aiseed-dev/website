---
slug: ai-companies-reality
title: AI企業の現実と、Kimi K3 がそこに与える影響
subtitle: 収益は本物である。しかし損失とインフラ約束はもっと大きい ── そして負債の塔は「借り手が2社しかいない」という一点の上に立っている
date: 2026.07.25
description: 「AIに需要がない」という主張は、少なくとも最上位2社については成り立たない。OpenAI は年率240億ドル、Anthropic は300億ドルに達した。だが損失とインフラ約束はそれより大きく、その下にはデータセンターの SPV 負債という、総額すら誰にも分からない層がある。GPU の経済寿命は2〜3年、対して負債の期間は5〜20年。そして決定的なのは借り手の集中で、賃料を実際に払っているのはほぼ2社に限られる。本稿はこの構図を数字で確認したうえで、Kimi K3 という変数が四方向に作用することを示す ── 価格決定力の圧縮、第三の借り手層が生まれる可能性、その形成が粗利の毀損より遅ければ塔が崩れるという逆方向、そして配布経路を握る政治。DeepSeek ショックを先例に、判定すべき指標を三つに絞る。本連載(五部作)の二本目。
lang: ja
label: Blog
category: 構造分析ノート
---

# AI企業の現実と、Kimi K3がそこに与える影響

[前稿](https://aiseed.dev/blog/kimi-k3-what-to-watch/)では7月27日のKimi K3重み公開の注目点を整理した。本稿はその前提となる問い、「AI企業の現実はどうなっているのか」を数字で確認し、そこにK3という変数がどう作用するかを考える。

## 収益は本物である

まず「AIに需要がない」という主張は、少なくとも最上位2社については成り立たない。OpenAIは月20億ドル(年率240億ドル)の収益を公表し、Anthropicは年率換算300億ドルに達した。1年前はAnthropicが約10億ドル、OpenAIが60億ドル前後だった。この成長速度は、ソフトウェア産業の歴史に前例がない。

## しかし損失とインフラ約束はもっと大きい

OpenAIは2026年に140億ドルの損失、2023〜2028年の累積損失は440億ドル、黒字化は早くて2029〜2030年——これが当初の見立てだった。実際には2026年Q1だけで約70億ドルの営業損失(営業利益率はマイナス122%前後)を出し、直近の試算では2028年単年の損失が850億ドルまで膨らむ。売上が急伸しても、コストがそれ以上の速度で伸びている。

さらに重いのはインフラ側の約束だ。OpenAIは年200億ドル規模の売上の段階で1.4兆ドルのインフラ支出を約束し、後に2030年までの約6000億ドルへ下方修正した。業界全体では2026年だけで6900億ドルの設備投資が見込まれ、Google単独で1850億ドル。モデル企業の売上がどれだけ速く伸びても、支払いを約束した総額はさらに大きい。

## 同じ「AI企業」でも財務は分岐した

Anthropicは2026年Q2に売上109億ドル、初の営業黒字5.59億ドルを投資家に開示した。訓練費はOpenAIの約4分の1で、通年での黒字化は2028年頃と見込む。片方は黒字転換の実証を始め、片方は売上だけではハードウェアコストすら賄えず、2028年には単年で850億ドルの損失へ向かっている。企業向け8割の収益構成と、9億人の週次利用者のうち払うのは一部という消費者型の構成。ビジネスモデルの違いが、そのまま財務の分岐になった。

両社とも2026年後半のIPOに向かっている。損失の資金源がベンチャー資金から公開市場へ、最終的には個人の資産へ移る局面に入った。

## データセンター負債という下部構造

この2社の下には、もっと見えにくい層がある。データセンターはSPV(特別目的会社)で組成され、負債の相当部分が簿外にある。総額は1.65兆ドルとも、簿外分を含めればその倍とも言われ、正確には誰にも分からない。返済原資は顧客(主にモデル企業)が払う賃料だけで、多くはノンリコース。担保資産のGPUの耐用年数は会計上5〜6年とされるが、これは各社が利益管理のために伸縮させている数字で、経済的な寿命はもっと短い。H100のレンタル価格は2024年初の8〜10ドル/時から2026年には2〜3.5ドルへ落ち、発売から約2年半で投資回収ぎりぎりの水準に達した。中古価格は2年で半分以下、新世代との推論コスト差は10倍超。収益力ベースの寿命は2〜3年とみるべきで、それに対して負債の期間は5〜20年ある。年金・保険マネーがプライベートクレジット経由で入り込み、リスクの所在が分からなくなっている。

そして決定的なのは、借り手の集中だ。GPU賃料を実際に払っているのは、ほぼOpenAIとAnthropicと数社のハイパースケーラーに限られる。この2社の粗利が細れば、負債の塔全体の返済原資が細る。

## K3はこの構図にどう作用するか

Kimi K3は7月16日に公開された総2.8兆パラメータのMoEモデルで、独立評価で最上位の非公開モデルに次ぐ位置につけ、27日に重みの完全公開を予告している。オープンモデルが非公開フロンティアと数ヶ月差まで迫った。これが上の構図に与える影響は、一方向ではない。

第一に、モデル企業の価格決定力を長期的に圧縮する。数ヶ月待てばほぼ同等がオープンで手に入るなら、非公開モデルのプレミアムには上限がつく。ただしK3自身がAPI価格を入力3ドル・出力15ドルとClaude Sonnet水準に設定した事実は、推論コストの重さから誰も逃げられないことを示す。オープン化は訓練費回収の放棄であり、K3の存在はむしろ「フロンティアは誰がやっても高い」ことの傍証でもある。

第二に、需要集中を緩和する可能性がある。データセンター負債の最大の弱点は「借り手が2社しかいない」ことだった。重みが公開され、企業が自社ホストやクラウド推論に動けば、初めて「第三の借り手層」が生まれうる。実際K3は公開48時間で自社の計算能力の限界に達し、新規契約を止めた。需要は消えず、推論需要として分散する。傍証もある。2025年末、Blackwell普及で旧世代Hopperの賃料は暴落すると予想されていたが、オープンウェイトモデルの普及と推論需要の加速で逆に堅調化し、H100の1年予約価格は2025年10月の底から約40%反発した。旧世代GPUの経済寿命を延ばしているのは、まさにオープンモデルの推論需要だ。推奨構成64基以上という要件は、その需要がコンシューマ機ではなくデータセンター級に落ちることを意味する。

第三に、逆方向にも効く。オープンモデルが2社の粗利を削り、第三の借り手層の形成がそれより遅ければ、唯一の返済原資が細るだけで終わる。どちらが速いかの競争であり、答えはまだ出ていない。

第四に、政治が変数を増やした。米政府はK3がAnthropicのFableの蒸留で作られたと名指しで主張し、制裁とエンティティリスト登録に言及した。証拠は公開されていないが、配布経路(Hugging Faceは米企業)が閉じれば、第三の借り手層の形成は分断される。逆にMoonshot側には「配れるうちに撒く」動機が生まれる。

## 先例と判定基準

2025年1月のDeepSeekショックが先例になる。市場は一日揺れたが、ハイパースケーラーの設備投資はその後むしろ増えた。株価の一日は何も決めない。決めるのは、推論需要が賃料として実際にSPVに流れ込むかどうかだけだ。

だから見るべき指標は三つ。モデル企業2社の粗利率の推移(オープンモデルの価格圧力がいつ数字に出るか)。ハイパースケーラー以外のGPU賃借の総額(第三の借り手層が数十億ドルの壁を超えるか)。そしてデータセンター側の債務不履行の初例(顧客の3ヶ月不払いで契約違反となる条項が多く、2027年前後に集中する)。

K3クラスのオープンモデルは、この三つ全部に触る唯一の変数だ。バブルを破裂させる針にも、借り手層を広げて延命させる支柱にもなりうる。27日の重み公開は、その分岐の始点になる。

なお本稿の分析はAnthropicのモデル(Claude)との対話をもとに作成した。Anthropicは本稿が扱う建設ラッシュの受益側にあり、K3の蒸留疑惑の当事者でもある。その立場を差し引いて読んでほしい。

---

## 関連

本稿は五本の連載の二本目である。

- ブログ [7月27日、Kimi K3 の重み公開で本当に見るべきもの](https://aiseed.dev/blog/kimi-k3-what-to-watch/) ── 一本目。27日のチェックリストと、空白の階層
- ブログ [7月29日、Microsoft の決算で見るべきもの](https://aiseed.dev/blog/microsoft-earnings-verdict/) ── 三本目。本稿の構図が市場で判定される日
- ブログ [同じ週に、三つの決着が近づいている](https://aiseed.dev/blog/three-fronts-same-week/) ── 四本目。同じ週に動く、AIの外側の三つの限界
- ブログ [ITという産業が終わり、素材と組立の時代が始まる](https://aiseed.dev/blog/after-it-industry/) ── 五本目。終わったあとに何が育つか
- ブログ [アメリカのAI覇権の終わりの始まり](https://aiseed.dev/blog/end-of-us-ai-hegemony/) ── 中国オープンウェイト勢が台頭する地政学的背景

## 参考

1. OpenAI And Anthropic Are Testing Two Very Different AI Business Models(Forbes, 2026-05-21)── https://www.forbes.com/sites/paulocarvao/2026/05/21/anthropic-openai-enterprise-ai-profitability/
2. Anthropic Just Passed OpenAI in Revenue. While Spending 4x Less to Train Their Models(SaaStr)── https://www.saastr.com/anthropic-just-passed-openai-in-revenue-while-spending-4x-less-to-train-their-models/
3. Sam Altman's OpenAI is burning billions(European Business Magazine)── https://europeanbusinessmagazine.com/sam-altmans-openai-is-burning-billions-most-users-pay-nothing-as-anthropic-closes-in/
4. Anthropic revenue, valuation & funding(Sacra)── https://sacra.com/c/anthropic/
5. Better Offline / The Tech Report(Ed Zitron)によるデータセンターSPV・私募クレジット分析(番組書き起こし)
6. Kimi K3人気でGPUひっ迫 新規サブスク受け付けを一時停止(ITmedia, 2026-07-21)── https://www.itmedia.co.jp/news/articles/2607/21/news099.html
7. 米政府がMoonshot AIを名指し、Kimi K3の「蒸留」とGB300利用を告発(XenoSpectrum)── https://xenospectrum.com/moonshot-kimi-k3-distillation-accusation/
8. Kimi K3: The open-weights escalation(Nathan Lambert, Interconnects)── https://www.interconnects.ai/p/kimi-k3-the-open-weights-escalation
9. Kimi K3's open weights arrive July 27. The catch is 1.4TB(TECHi)── https://www.techi.com/kimi-k3-open-weights-inference-economics/
10. AI Chip Lifespans: A Note on the Secondary Market(CITP, Princeton, 2025-12-18)── https://blog.citp.princeton.edu/2025/12/18/ai-chip-lifespans-a-note-on-the-secondary-market/
11. H100 GPU Cost In 2026: Buy, Rent, And Cloud Pricing Compared(CloudZero)── https://www.cloudzero.com/blog/h100-gpu-cost/
12. The Great GPU Shortage – Rental Capacity(SemiAnalysis)── https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity
13. Is the AI Chip Shortage Over in 2026?(Value Add VC)── https://valueaddvc.com/blog/is-the-ai-chip-shortage-over-in-2026-gpu-pricing-and-what-comes-next
