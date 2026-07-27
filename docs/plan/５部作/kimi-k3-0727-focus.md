# 7月27日、Kimi K3の重み公開で本当に見るべきもの

2026年7月25日

Moonshot AIは7月16日にKimi K3を発表し、完全な重みを7月27日までにHugging Faceで公開すると約束した。総パラメータ2.8兆、MoEで1トークンあたり896エキスパート中16(約50B)が動く。MXFP4形式で約1.4TB、同社の展開ガイドはアクセラレーター64基以上を求める。つまり27日に配られるのは、個人はもちろん中小企業でも動かせない巨大な塊だ。

それでも27日は節目になる。見るべきは「重みが出るか」だけではない。この日は、Moonshotという会社がこれから何屋になるのかを測る試験紙になる。

## 前提が二つ変わった

一つは政治。7月22日、米OSTPのKratsios局長はMoonshotがAnthropicのFableを蒸留してK3を開発したと名指しで主張し、Bessent財務長官は制裁とエンティティリスト登録の可能性に言及した。出力ログなどの証拠は公開されていないが、配布経路であるHugging Faceは米企業だ。27日に予定どおり重みが出るか、ライセンス(Modified MIT見込み)の条項に変更がないか、配布経路が維持されるか。この三点が最初の観測項目になる。

もう一つは需要。K3公開の48時間後、Moonshotは想定を超える利用で計算能力の限界に達し、新規有料契約を停止した。売る能力より欲しがる人が多い。この状態は、後述するとおり同社の損得計算を変える。

## 楊植麟を理念で予測してはいけない

創業者の楊植麟は、清華大からCMUで博士号、Transformer-XLとXLNetの第一著者、Google BrainとMeta FAIRを経た研究者だ。「規模で解決できるなら新アルゴリズムで解決するな」「AGI企業は今日の巨人を超える」と語り、汎用能力への集中を公言してきた。

だが発言より行動を見るべきだ。2023年には「クローズドこそスーパーアプリへの唯一の道」と言い、DeepSeek後にオープンへ転換した。2025年にはユーザー獲得競争から降り、マーケティング投資を切って研究開発へ回帰した。K3ではAPI価格を入力3ドル・出力15ドルとClaude Sonnet水準に上げ、「オープンは安い」という自陣営の建前も捨てた。どの局面でも、前言との一貫性より状況への適応を選んでいる。つまり現実主義者であり、予測の根拠は理念ではなく損得計算に置くべきだ。

そして現実を直視すれば、汎用フロンティアの正面競争は成立しない。OpenAIは一回の調達で1220億ドル、Anthropicの訓練費は2028年頃に年300億ドル規模。Moonshotの直近調達は約20億ドルで、H800の「一枚あたりを搾る」効率技術で追走している。蒸留疑惑が部分的にでも正しいなら、追走の一部は先頭の出力に依存しており、その経路は米側の締め付けで細る。残る勝ち筋は、頂点ではなく「数ヶ月差のオープン最強」を配り続ける標準の座と、物量勝負が効かない展開階層だ。

## 空白の階層──128GBから192GB

いま市場で伸びているハードの帯がある。ユニファイドメモリ128〜512GBの机上機──Strix Halo系、Mac Studio、DGX Spark。24GBの単体GPUと数百GBのラックの間にあるこの帯には、実需に対してモデルが少ない。4bit量子化なら総パラメータ約200Bが128GBの上限、192GBなら350Bクラスまで載る。K3と同じ疎なMoE思想で総200B・アクティブ10〜20Bに作れば、この帯域でも実用速度が出る。

Moonshotがこの帯に出す動機は、理念で見れば弱い。スケール第一主義にとって小型は副産物だからだ。だが損得で見れば強い。第一に、K2.7 Codeの重みを無償公開しながら19〜199ドルのサブスクが売れている以上、彼らの課金は重みではなくCLI・速度・手間の省略に対して成立しており、小型版を配っても商売は壊れない。第二に、計算逼迫で捌けない需要は、ローカルで自走してもらう方が得だ。失う売上はもともと取れない売上で、ユーザーはKimiのハーネスに残る。第三に、制裁リスクは「配れるうちに世界中のハードへ撒く」保険としての配布を急がせる。第四に、香港上場を控え、エコシステム採用の物語が要る。K2 ThinkingのAMAでは開発者から小型版の催促が本人に直接届いてもいる。

## 27日のチェックリスト

第一に、重みとライセンス。予定どおり出るか、Modified MITのままか、蒸留・派生モデルの扱いに関する条項が変わっていないか。米側の告発後に条項をいじってくれば、それ自体がメッセージになる。

第二に、技術レポートの言葉。小型ライン、Code特化版、蒸留への言及があるか。K2.7 Codeは新規ベースモデルではなくK2.6基盤のポストトレーニングで、K2.5〜2.7は同一アーキテクチャのため重み差し替えだけで移行できる。K3を教師に1TクラスのK3 Codeを作るのは、彼らにとって安い次の一手だ。

第三に、製品側の気配。APIやKimi Code CLIのモデルID一覧、huggingface.co/moonshotai のリポジトリ作成、サブスク価格の改定予告。K2.7のときはHF公開とAPI追加が同日だった。

予想を書いておく。順番はK3 Code(1Tクラス)が先、128〜192GB級はその後。ただし楊植麟が現実主義者であるほど後者の確率は上がり、過去の方針転換はどれも1〜2年以内に起きている。「1Tクラスしか出したことがない」という実績は、蒸留とポストトレーニングが事前学習より桁違いに安い以上、障害として軽い。

27日に小型ラインの気配が出れば、それは「理念が現実に譲った」合図だ。出なければ、彼らはまだ登山の物語の中にいる。どちらでも、観測する価値はある。

## 主な出典

- ITmedia「Kimi K3人気でGPUひっ迫 新規サブスク受け付けを一時停止」 https://www.itmedia.co.jp/news/articles/2607/21/news099.html
- GIGAZINE「Kimi K3はClaude Fableの蒸留によって作られたとホワイトハウス高官が発言」 https://gigazine.net/news/20260723-kimi-k3-distillation-anthropic/
- XenoSpectrum「米政府がMoonshot AIを名指し、Kimi K3の『蒸留』とGB300利用を告発」 https://xenospectrum.com/moonshot-kimi-k3-distillation-accusation/
- byteiota「Kimi K3 Open Weights Drop July 27: The Developer Prep Guide」 https://byteiota.com/kimi-k3-open-weights-july-27-developer-prep/
- Nathan Lambert「Kimi K3: The open-weights escalation」 https://www.interconnects.ai/p/kimi-k3-the-open-weights-escalation
- 36氪「K2 Thinking再炸場、楊植麟が21の質問に回答」 https://36kr.com/p/3548523752173447
- アリ雲創新中心「対話 Moonshot AI 楊植麟:閉源は超級APPへの唯一の通路」 https://startup.aliyun.com/info/1066387.html
- Science Portal China「Moonshot AI、Kimiシリーズで進化させた長文処理とAIエージェント機能」 https://spap.jst.go.jp/china/experiences/science/st_26060.html
- MarkTechPost「Moonshot AI Releases Kimi K2.7-Code」 https://www.marktechpost.com/2026/06/12/moonshot-ai-releases-kimi-k2-7-code-a-coding-model-reporting-21-8-on-kimi-code-bench-v2-over-k2-6/
