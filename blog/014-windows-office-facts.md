---
slug: windows-office-facts
title: それでも Windows と Office を使い続けますか？
subtitle: Copilot は使われていない。それでも世界の資源は吸い上げられ続ける
description: 企業向け AI 市場で Anthropic が Microsoft を抜き、Copilot の利用率は 35.8%、NPS は -19.8。LLM のアーキテクチャ上の限界 (O(N²·d)) でハルシネーションは数学的に回避不可能。それでも Microsoft は Copilot を OS 最深部に統合し、データセンター建設で世界のメモリ・電力・ナフサを吸い上げている。Linux への早急な移行を提案する。
date: 2026.04.26
label: Blog
category: 構造分析ノート
hero_image: 014-IMG_3437.jpg
---

# それでも Windows と Office を使い続けますか？

## 概要

**第一に、エンタープライズ市場における勝敗はすでに決している**。企業は Anthropic の Claude を選択しており（ARR **300億ドル**突破、Fortune 100 の70%が採用）、Microsoft Copilot のアクティブ利用率は **35.8%** に留まり、NPS は **-19.8** と深いマイナスを示している。

**第二に、LLM のアーキテクチャ上の計算限界（O(N²·d) の制約）により、複雑な業務タスクにおけるハルシネーションは回避不可能**である。この本質的な欠陥を抱えたシステムを Windows OS の最深部に統合し、無効化を困難にしている Microsoft の設計姿勢は、医療や金融をはじめとする全ての産業に、**監査不能なコンプライアンス・リスク**を負わせている。

**第三に、回収見込みのない AI への巨額投資が、物理的現実を破壊している**。2026年2月のイラン戦争によるホルムズ海峡封鎖とそれに伴うナフサ危機が進行する中、医療インフラに必要な生命維持のための資源、一般消費者の電子機器用メモリ（DRAM 価格の異常高騰）、地域社会の電力網までもが、利用率の低い AI データセンターのインフラ維持のために容赦なく吸い上げられている。

2025年10月の Windows 10 サポート終了に伴い、企業は年々倍増する高額な ESU（延長セキュリティ更新プログラム）の負担を強いられる。一方で、ハードウェアを更新しようとすれば、AI 需要でメモリ価格が史上最高値をつけている最中に、不必要な高スペック（Copilot+ PC）の購入を強制される。さらに、Windows 11 に移行した先には、オプトアウトが極めて困難で法的リスクを伴う AI の監視と処理経路が待ち受けている。

企業や自治体の IT 責任者、および最高情報セキュリティ責任者（CISO）は、Microsoft のプラットフォームがもはやかつてのような「業務を支える中立的で安定したインフラ」ではなく、**自社の予算を無制限に吸い上げ、コンプライアンス上の社会的責任を脅かす「高い維持費を伴うハイリスクなエージェント」**へと変質したことを明確に認識すべきである。

---

## Windows PC の要求 Spec

Microsoft が AI 統合に合わせてハードウェア要件を段階的に引き上げた結果、世界中のユーザーのPC が「使えない」ものになった。

**段階的に切り捨てられてきた PC**

- **Windows 11（2021）**：2017年以前に買った PC は使えなくなった（TPM 2.0、Intel 第8世代/Ryzen 2000以降が必須）
- **24H2（2024）**：TPM を迂回する手段も封じられた（SSE4.2、POPCNT 必須）
- **Copilot+ PC（2024）**：2024年中頃以前に買ったすべての PC が、Copilot 機能を完全には使えない（40 TOPS NPU、16GB DDR5、256GB SSD）

**Copilot+ PC は買い替えるしかない**

- 既存 PC のアップグレード不可、新規購入のみ
- NPU 単体で 40 TOPS（CPU/GPU 合算は認めない）
- 対応 CPU は Qualcomm Snapdragon X、Intel Core Ultra 200V、AMD Ryzen AI 300 系列だけ

**Windows 10 サポート終了で世界中のユーザーが直面している現実**

- 2025年10月14日、サポート終了
- **2億4,000万台**の PC が廃棄対象（Canalys 推定、世界の Windows 端末の約20%）
- 廃棄重量4億8,000万キログラム = 自動車32万台分
- 使い続けたければ ESU（Extended Security Updates）を払う：1年目61ドル → 2年目122ドル → 3年目244ドル。3年で1台427ドル

**廃棄される PC の行き先**

- 廃棄 PC の80〜85%が埋立に向かう
- 鉛・水銀・カドミウム・難燃剤が土壌と地下水に漏出
- 多くは Windows が動かないだけで、Linux なら数年は使える

---

## ナデラの Copilot 統合戦略

### Microsoft 社内の AI 義務化

サティア・ナデラは、社内で以下を実行している。

- 社員の人事評価 KPI に AI 採用指標を組み込む
- 内部メモで「AI の使用はもはやオプションではない」と全社員に通達
- AI 統合に抵抗する幹部の退場
- プロトタイプを CEO 自らレビューし、予算を直接再配分

さらに経営陣は、AI 導入によるコーディング業務効率の飛躍的向上を理由に、大規模なレイオフや配置転換を実施している。米国従業員向けの「自発的退職プログラム」は、AI ネイティブな役割に移行できない従業員を組織から排除する機能として働いている。

経営トップ自らが「AI によって人員が代替可能であること」を証明し、それを理由に人員削減を進めている組織環境下で、現場のエンジニアや営業担当者が「Copilot は顧客に信頼されておらず、実際の利用率も低い」という都合の悪い真実を上層部に報告することは極めて困難である。**組織のフィードバックループが機能不全に陥り、実態と乖離したまま計画だけが推進されるサイロが形成されている**。

### ユーザーの同意なしの自動インストール ―― Mozilla による批判

Microsoft 365 デスクトップアプリを実行している Windows デバイスに、プロンプトもユーザーの同意もなしに M365 Copilot アプリが自動インストールされた。

Mozilla の副社長 Linda Griffin は、Microsoft がユーザーの同意なしに M365 Copilot アプリを Windows デバイスに自動インストールしたことや、物理キーボードに Copilot 起動を強制する専用キーを配置し、その再マッピングを困難にしていることを公然と批判し、これを **「ユーザーの選択権を剥奪し、自社の利益を優先するダークパターンの典型」**と非難している。

### タスクバーへのデフォルトピン留め

Copilot は Windows 11 のタスクバーにデフォルトでピン留めされた。通知センター、設定アプリ、ファイルエクスプローラーといった OS の最も基本的な表面に直接埋め込む計画が進行している。

### EEA だけが除外されている

Microsoft は欧州経済領域（EEA）を Copilot の自動インストール対象から除外している。

EEA は規制があるからやらない。それ以外の地域では強行する。**日本、米国、アジア、中南米、アフリカのユーザーは規制で守られていない**。Microsoft 自身が、これはユーザーの利益にならない、法的に問題があると認識しているということ。

### 24H2 以降のオプトアウトは極めて困難

IT 管理者がグループポリシーやレジストリを通じて Copilot の機能を無効化しようと試みても、システムは Edge ブラウザのコンポーネントを通じて AI の処理経路を維持するように深くルーティングされており、**完全なオプトアウトが極めて困難な構造**になっている。

### 医療現場と金融機関の法的責任

医療現場の IT 管理者は、グループポリシーで Copilot を完全に無効化せざるを得なかったと証言している。患者情報を AI が処理することは、明示的で文書化された同意と適切な監査なしには許可できない。**もし無効化を見落とせば、病院が法的責任を負う**。

金融機関のコンプライアンス担当者も、Copilot が機微な財務データを分析したり、承認されていない通信を作成したりする可能性を懸念している。**漏洩が起きれば責任を負うのは Microsoft ではなく、その金融機関**である。

監査不可能な AI が、OS レベルで機微な患者データや財務情報にデフォルトでアクセス可能な状態に置かれることは、**重大な法的責任（Liability）の所在を曖昧にする**。**自治体、病院、銀行、学校 ―― すべてが同じリスクを負わされている**。

---

## データセンターの建設ラッシュは、何のため？

Microsoft は、世界規模のリソースを集中投入してデータセンターを建設している。その規模は、**多くの中堅国家の年間予算に匹敵する**。

**Microsoft の設備投資**

- 2026会計年度の設備投資：**1,000〜1,200億ドル**
- Q1 だけで349億ドル（うちデータセンターリースで111億ドル）、Q2 で375億ドル
- ナデラ宣言：「2年でデータセンター・フットプリントを倍増」

**世界に展開するデータセンター**

- 400拠点以上、70リージョン、40カ国
- 1 GW あたり250億ドルのコスト構造

**旗艦プロジェクト Fairwater**

- Mount Pleasant, WI（Foxconn が完成できなかった跡地）：73億ドル → 最終133億ドル、9百万平方フィート
- 数十万基の NVIDIA GB200 GPU を統合した単一スーパーコンピューター
- アトランタの Fairwater 2 と AI WAN で接続して仮想スーパーコンピューター化

**OpenAI/Stargate との関係**

- 2025年1月に OpenAI との独占解除
- 2026年3月、テキサス・アビリーンで OpenAI/Oracle 放棄分の700 MW を Microsoft が吸収

**日本にも100億ドルが入ってくる（2026年4月発表）**

- **100億ドル（約1.6兆円）、4年間（2026〜2029）**
- SoftBank、さくらインターネットと連携
- 経済産業省（METI）の数兆円規模 AI 投資戦略と連動
- 日本国内にデータを留める **「Sovereign AI（主権AI）」インフラ**を構築する国家プロジェクトの中核
- 国家警察庁、内閣官房とのサイバーセキュリティ協業

日本政府は2040年までに **326万人**の AI・ロボティクス人材が不足すると予測しており、そのリスキリングと社会実装の基盤として、Microsoft のテクノロジーエコシステムに国家レベルで全面的に依存する方針を固めている。

**資金は中東から流れている**

- BlackRock + MGX（UAE）+ Global Infrastructure Partners と1,000億ドルファンド組成
- 中東資本が米国 AI インフラに流入する経路

**ナデラ自身が認めている問題**

- Azure 受注残800億ドル超（電力不足が原因）
- 「GPU は在庫にあるが、設置する電力が見つからない」

**この建設ラッシュの本質**

これは「買い占め」のような意図的な市場操作ではない。年間1,000億ドル超の資本支出（Capex）が、市場の購買力を介して **クラウディングアウト効果（他者の締め出し）**を引き起こしている状態である。Microsoft は単に最も強い買い手であり、それが結果として世界のサプライチェーンを根底から歪めている。

EEA のような規制的距離が日本にはない。これから見るように、この建設ラッシュの副作用が、世界中の他の産業と一般市民を直撃している。

---

## データセンターの建設ラッシュに伴う副作用

### 半導体メモリ価格の異常高騰 ―― 世界中の電子機器が値上がりしている

OpenAI が2025年10月、Samsung と SK Hynix と世界 DRAM の **約40%（月90万ウェハー）** に相当する意向書（letter of intent）に署名した。法的購入義務はないが、両社は生産ラインを再配分した。

Microsoft も SK Hynix と数十兆ウォン規模の3年 DDR5 長期契約を最終調整中。Samsung・Google・AMD とも長期契約に移行している。Samsung と SK Hynix で世界 DRAM の約78%を占める。

データセンター向けの AI サーバーには、HBM（広帯域メモリ）や大容量エンタープライズ SSD が不可欠である。半導体メーカー（Samsung、SK Hynix など）は、ハイパースケーラーの長期契約に応じて生産ラインを AI 向けに大幅にシフトさせた。この供給能力の再配分により、汎用の消費者向け電子機器に使用される DRAM および NAND フラッシュメモリの供給が極度に逼迫している。

**Counterpoint Research による DRAM 価格動向**

| 時期 | 動向 |
|---|---|
| 2025年Q3 | DRAM 価格、年比 **172% 上昇** |
| 2025年Q4 | 前四半期比 **約50% 上昇** |
| 2026年Q1 | さらに **40〜50% 上昇** |
| 2026年Q2 | 通常 DRAM、さらに **58〜63% 上昇予測** |

**64GB RDIMM の具体的な価格推移**

- 2025年Q3：**255ドル**
- 2026年Q1：**450ドル超**（半年で76%上昇）
- 2026年Q4予測：**700〜1,000ドル**（年内に最大4倍）

**NAND Flash も同様の高騰**

- TLC NAND デバイス価格が半年で **2倍以上**に高騰
- SLC・MLC NAND は **400〜500% 上昇**のケース
- 2026年通期予測：DRAM + SSD 合計で **130% 上昇**（Gartner）

**直撃を受けている人々と業界**

- **個人ユーザー**：PC 自作・修理が事実上できない価格に
- **PC・スマートフォンメーカー（HP、Lenovo、Xiaomi など）**：部品コスト（BOM）の急激な増加を吸収しきれず、製品の小売価格を **15〜25% 引き上げ**を余儀なくされている
- **Xiaomi**：2026年モデルで携帯あたり DRAM コスト **25% 増**、500ドルのスマホは625ドルへ
- **Dell**：「経験したことのない速度でコストが動いている」（決算電話会議）
- **HP**：通期業績見通しを下方修正
- **Cisco**：メモリ価格でマージン圧迫、株価2022年以来最大の下落
- **IDC 予測**：2026年の世界スマートフォン出荷 **12.9% 減**、PC 市場 **11.3% 縮小** ―― 二桁の市場縮小

**Counterpoint Research の要約：**

> メモリ各社はスマートフォンメーカーに、ハイパースケーラーの後ろに並べと言っている。

**日本の小売現場**

- 秋葉原のツクモ、ソフマップで購入制限（SATA SSD 2台、NVMe SSD 2台、SO-DIMM 4枚まで）
- 「メモリ予約証明書」：2025年価格で2026年納品の予約金制度
- パニック買い防止のための小売規制が、コロナ禍以来に戻ってきた

**いつまで続くか**

- Counterpoint Research：需給バランスは **2028年まで**正常化しない
- 供給は世界需要の60%しか満たさない
- Micron：DRAM の枯渇は2028年まで続く可能性

**メモリ工場は短期で建てられない。世界中の電子機器ユーザーは、あと2〜3年、Microsoft の設備投資のしわ寄せを受け続ける**。

---

### 資材の枯渇 ―― データセンター自体も完成できなくなる

#### 半分以上が完成できない

2026年に米国で稼働予定の12〜16 GW のデータセンター容量のうち、実際に建設中なのは **約3分の1のみ**。残りは電気設備の納入待ちで止まっている。

業界分析では、2026年計画分の **30〜50% が2028年以降にずれ込む**と予測されている。**Microsoft は完成できない設備のために、世界中のリソースを優先確保している**。

#### 変圧器の奪い合いで起きていること

データセンターは壁のコンセントに繋ぐわけではない。高圧送電線から使用可能な電圧に落とすため、**数百トン規模の変圧器が必要**になる。

- カスタム設計、手巻き製造（自動化できない）
- 大型変圧器の納期：通常で **3〜5年**、最長で **120週（2年強）**
- 価格：2022年比で **4〜6倍**
- 世界で大型変圧器を製造できる企業：**5〜6社のみ**

ハイパースケーラーは、着工 **3〜4年前**から変圧器を予約している。**結果として、米国の電力会社が老朽変圧器の交換プログラムを延期せざるを得ない**。米国の高圧配電変圧器の半分以上が33年を超え、寿命に近づいているか超過している。**地域社会における停電リスクが構造的に高まっている**。

#### 電気鋼板（GOES）、銅、ヘリウム、臭素

すべての素材で、データセンターが優先供給を受け、それ以外の用途が後回しになっている。

- **GOES**（変圧器のコア材）：米国唯一の生産者は Cleveland-Cliffs。大型変圧器の80%は輸入依存。価格倍増、納期12〜18カ月。**再エネ・EV・グリッド近代化が後回し**
- **銅**：データセンター1MWあたり27〜33トン消費。2025年に30万4千トンの不足、1ポンド6ドル過去最高値。**EV 産業、再エネ送電網、住宅配線が値上がり**
- **ヘリウム**：カタール攻撃で価格倍増、**台湾・韓国の半導体工場で配給制**。チップ生産量が純減する可能性
- **臭素**：イスラエル ICL Group が世界供給40%支配。1トン12,000ドルに急騰

#### 系統接続待ち ―― 電力契約が3〜7年待ち

米国の系統接続待ち行列は **2,100 GW 超**に膨れ上がっている。これは米国の総送電網容量を超える数字。系統接続プロセスには **3〜7年**を要する。

**新しい工場、新しい病院、新しい学校、新しい住宅 ―― すべてがデータセンターの後ろに並んでいる**。電力可用性の制約だけで、建設工期が **24〜72カ月延長**されているケースが報告されている。

---

### 化石燃料の大量使用 ―― 気候変動対策の事実上の撤回

データセンターの電力を確保するため、Microsoft は2026年に入って化石燃料インフラへの大規模な直接投資へと舵を切った。**気候変動対策の進捗が、巨大テック企業1社によって大きく後退した**。

#### Chevron との70億ドル契約

2026年4月、Microsoft はエネルギー大手 Chevron および投資会社 Engine No. 1 との間で、テキサス州西部のパーミアン盆地における **2.5 GW の巨大天然ガス火力発電所**の共同建設に関する **70億ドル**規模の独占契約を締結した。

- 規模：2,500 MW（最大 5,000 MW まで拡張可能）
- 米国の家庭約400万世帯分の電力に相当
- 稼働開始予定：2027年後半
- 設計：送電網の逼迫を回避するため、データセンターキャンパスに直接電力を供給する **「ビハインド・ザ・メーター」方式**

**米国400万世帯分の電力を、1社の AI のためだけに使う**。

#### CO₂ 排出量と「2030年カーボンネガティブ」公約の形骸化

Microsoft が2020年比で報告した CO₂ 排出量は、すでに **23.4% 増加**を記録している。同社が掲げていた「2030年までにカーボンネガティブを達成する」という野心的な環境公約は事実上形骸化した。

テキサス州の巨大天然ガス発電所が本格稼働すれば、この排出量はさらに増加することが確実視されている。Stand.earth Research Group の分析によると、Microsoft は2026年の最初の数カ月だけで合計 **4.75 GW** の新規化石燃料発電を提案している。

**産業全体の文脈**：Goldman Sachs の分析によれば、AI の爆発的普及により、データセンターの **電力需要は2030年までに 160% 増加**すると予測されている。

#### 天然ガスインフラの3分の1以上をデータセンターが奪う

2024年末、データセンターはメタンガス発電需要の 5% を占めていた。それが2025年末には **39%** に跳ね上がった。1年で約8倍。

**家庭暖房、産業ボイラー、発電 ―― あらゆる天然ガス需要が、データセンターと同じパイプラインを奪い合っている**。

---

### イラン戦争に伴うオイルショックでのナフサとエネルギーの奪い合い

Microsoft が天然ガス火力発電所への大規模投資を決めた、まさにその時期に、世界はエネルギー危機に入った。**Microsoft の建設計画は、戦争による供給ショックと真正面から衝突している**。

#### 2026年2月28日：Operation Epic Fury とホルムズ海峡封鎖

2026年2月28日、米国とイスラエルの連合軍はイランの軍事施設および政府中枢に対する大規模な空爆作戦（コードネーム **「Operation Epic Fury」**）を敢行した。この急襲により、イランの最高指導者アリ・ハメネイ師をはじめとする多数の政府高官が暗殺された。

報復として、イランは中東全域のアメリカ軍基地およびイスラエルに対する数千発規模のミサイル・ドローン攻撃を実施するとともに、世界のエネルギー大動脈である **ホルムズ海峡を事実上封鎖**する強硬措置に出た。

ホルムズ海峡を通る貨物：

- 世界の海上原油貿易の **約20%**
- 世界の LNG（液化天然ガス）貿易の **約20%**
- 世界の尿素肥料の **30% 以上**
- 世界の硫黄供給の **約45%**（湾岸諸国）

国際エネルギー機関（IEA）はこれを **「世界石油市場史上最大の供給ショック」**と表現した。

#### ガソリン代と電気代が世界中で上がっている

- ガソリン価格：数週間で **30% 上昇**
- ブレント原油：戦争前の72ドル/バレルから、ピーク時120ドル近くまで上昇（55%超）
- アジア向け LNG スポット価格：カタール Ras Laffan 施設への攻撃も相まって **140% 以上の急騰**
- カタールの LNG 生産能力：17% 減少、完全復旧には3〜5年

**世界中の家庭の電気代、燃料代、暖房費が上がっている**。

天然ガス火力発電所は、燃料の継続供給を前提として設計される。Microsoft の70億ドル投資判断は、**化石燃料が安価かつ安定供給される世界**を前提にしている。その前提は2026年2月28日に崩れた。それでも建設は止まらない。

#### ナフサ危機 ―― 代替不可能な基礎化学原料の供給断絶

ホルムズ海峡封鎖は、原油と LNG だけでなく、**ナフサ**の供給を直撃した。ナフサは原油の蒸留プロセスから得られる基礎化学原料であり、プラスチック、合成繊維、医薬品包装、半導体製造プロセスの出発点となる **代替不可能な物質**である。

**ナフサ価格の崩壊的な急騰**

- 2026年2月28日（戦争開始時）の直後、スポット価格が1トンあたり **約600ドル → 1,190ドル**へほぼ倍増
- 戦争開始から1カ月で **60% 上昇**、アジア市場で1メートルトンあたり **1,000ドル**到達
- インドの PVC 価格は3月単月で **78% 上昇**

**日本・韓国・マレーシアの状況 ―― 中東依存度の極端な高さ**

- 日本国内のナフサ在庫：**わずか10〜20日分**という危機的水準
- 日本のタンカーの **約80%** がホルムズ海峡を通過、中東原油依存度95%超
- 韓国の原油輸入の **70% 超** がホルムズ海峡経由
- 日本政府：**8,000万バレル規模**の戦略的備蓄を放出（焼け石に水）
- **出光興産**：エチレンプラントの生産停止を取引先に警告。徳山（年産62万トン）と千葉（37万トン）の停止候補。日本のエチレン生産能力の約16%
- **東ソー株式会社**：MDI 製品の大幅な価格引き上げを発表
- **三菱化学**：ナフサ在庫の持続期間を評価中
- **韓国**：ロシア産ナフサの緊急輸入、ナフサの輸出禁止

**force majeure（不可抗力）宣言で生産停止**

- インドネシア最大の化学企業 Chandra Asri Pacific
- シンガポールの PCS（ペトロケミカル・コーポレーション）
- 韓国の Yeochun
- アジアで **10カ所以上の石油化学工場**が生産停止

#### 医療インフラと AI インフラの衝突 ―― ナフサのトリアージ

ナフサの極端な不足は、グローバルサプライチェーンにおいて究極の **「トリアージ（資源の選別的配分）」**を引き起こした。

| 競合するナフサ由来の最終製品 | 医療・ヘルスケア・一般産業 | AI・データセンターインフラ |
|---|---|---|
| ポリ塩化ビニル（PVC） | 透析回路、血液チューブ、IV バッグ | データセンター用ケーブルの絶縁体、大型配管材 |
| ポリエチレン（PE） | シリンジ、無菌包装材料、医薬品容器 | 光ファイバーの被覆材、液浸冷却用の特殊配管 |
| ポリウレタン / 各種特殊樹脂 | 各種医療用バルブ、クランプ、カテーテル | サーバー筐体のプラスチック部品、マザーボードのコーティング材 |

マレーシア腎臓財団などが警告するように、現代の医療システムは透析用のダイアライザーや注射器など、使い捨てのプラスチック製医療機器に完全に依存している。

通常であれば、市場メカニズムを通じてこれらの医療インフラに必要な原料は確保される。しかし2026年の危機においては、年間1,000億ドル以上の設備投資予算を持つ Microsoft などの巨大ハイパースケーラーが、建設中のデータセンターに不可欠なケーブルや冷却設備の材料を確保するため、価格を度外視してサプライチェーンの上流で原材料（PVC や PE など）の予約購入を進めた。

**資金力で圧倒的に劣る医療機器メーカーや中小の包装材料メーカーは、高騰した原料価格を製品価格に転嫁することができず、調達市場から物理的に締め出される事態となった**。

「**透析を受けている患者が、誰も使っていない AI のために犠牲になっている**」という認識は、文学的な比喩ではなく、**2026年春にアジア全域で発生している深刻な医療物資のサプライチェーンの逼迫構造を正確に記述したもの**である。

ドイツの包装製造業者の99%が値上げを受けているが、転嫁できているのは一部のみ（2026年3月、ドイツプラスチック加工業協会調査）。**中小製造業の倒産リスクが世界中で高まっている**。

---

## Copilot を組み込んだことは、ナデラの失敗

ここまでの被害は、すべて Copilot を社会基盤に組み込むためのものである。社員に拒絶され、ユーザーに信頼されず、市場シェアで敗北しても、ナデラは Copilot 統合を止めない。

しかし **Copilot は使われていない**。これは Microsoft 自身のデータが示している。

### 利用率の数字 ―― 配布されたライセンスと実際の利用の巨大な乖離

Microsoft の AI 展開における最大の構造的課題は、配布されたライセンス数（Provisioned seats）と実際の利用率との間に生じている巨大な乖離である。

- **Microsoft 365 Copilot 有料シート**：1,500万（2026年Q2）
- **アクセスを持つ社員のうち実際に使っているのは 35.8%**（Recon Analytics、米国15万人規模調査、2026年）
- 残りの約3分の2の従業員は、アクセス権を持ちながらも AI ツールを使用していないか、他のプラットフォームへ移行

つまり、企業が Copilot のライセンスを買っても、**社員の3分の2は使っていない**。

### 信頼スコア（NPS）の崩壊

Copilot の精度に対する NPS（ネット・プロモーター・スコア）：

- 2025年7月：**-3.5**
- 2025年9月：**-24.1**（深刻に悪化）
- 2026年1月：**-19.8**（部分的に回復、依然マイナス圏）

NPS がこれほど低いマイナスを示すことは、使用したユーザーが結果に不満を抱き、同僚に推奨しないだけでなく、**積極的に使用を避けるよう警告している状態**を意味する。

Copilot の使用を中止したユーザーを対象とした調査では、**44.2% の回答者が「回答への不信」を中止の主な理由**として挙げており、これは競合他社の AI ツールと比較しても突出して高い不信感の表れである。

OS や Office アプリケーションにデフォルトで組み込まれているという比類なき流通上の優位性が、製品の品質に対する信頼や実際の利用率に全く結びついていない実態が浮き彫りになっている。

### 企業 AI 市場で Anthropic に追い抜かれた

企業向け AI 市場では、Microsoft はもはや勝者ではない。Anthropic の Claude が市場の覇権を握っている。

**2026年4月時点の Anthropic vs Microsoft Copilot**

| 財務・採用指標 | Anthropic（Claude） | Microsoft（Copilot 企業向け） |
|---|---|---|
| 年間経常収益（ARR） | **300億ドル**突破 | 非公開（1,500万シートから推計15〜25億ドル規模） |
| 成長率（過去15ヶ月） | 約30倍（10億ドル → 300億ドル） | 利用率35.8%で停滞 |
| Fortune 100 採用状況 | **70%が主要モデルとして採用** | Office バンドルにより配布率は高いが実働は限定的 |
| Fortune 10 採用状況 | **10社中8社が顧客** | ―― |
| 開発者からの信頼度（NPS） | 54（Claude Code、2026年1月） | -19.8（全般的なビジネス用途、2026年1月） |

**Anthropic の成長軌跡 ―― エンタープライズソフトウェア史上最速**

- 2025年1月：ARR 10億ドル
- 2025年内：90億ドルに到達
- 2026年2月：140億ドル（Series G、企業評価額3,800億ドル）
- 2026年4月：**300億ドル突破** ―― OpenAI の推定250億ドルを抜いた
- B2B ソフトウェア企業として、3年連続で年10倍成長 ―― Slack、Zoom、Snowflake のいずれも未達

**Claude Code の躍進**

ソフトウェア開発の領域における「Claude Code」の躍進が著しい。Claude Code は単体で **ARR 25億ドル**を達成し、プロのソフトウェアエンジニアの **45% が日常的に使用するツール**へと成長した。

開発現場では、自律的なエージェント機能や複雑なリファクタリング、アーキテクチャ設計といった高度な推論を要するタスクには Claude Code や Cursor を利用するという **「マルチツール・スタック」** が2026年の標準的なパラダイムとして定着している。

**Claude の大規模導入の例**

- Cognizant：35万人にClaude 配備
- Accenture：3万人を Claude でトレーニング、専用 Anthropic Business Group を設置
- Deloitte：47万人へ展開
- Salesforce Agentforce の優先モデルが Claude

**回収できない設備投資**

- Microsoft Copilot 推定 ARR：**15〜25億ドル**
- Microsoft 設備投資：**1,000〜1,200億ドル**
- 設備投資は Copilot 売上の **50倍以上**

その間、Anthropic は同じ AI 市場で **300億ドル**の ARR を、Microsoft の何分の1の設備投資で達成している。**問題は AI への需要がないことではなく、Microsoft の Copilot が選ばれていないこと**である。

### Microsoft 自身が認めるパイロット失敗率

Gartner 調査：**Copilot のパイロット導入のうち、社員の20%以上に拡大できたのはわずか24%**。残りの76%はパイロットで止まっている。

### 構造の要点

ナデラは、社員・ユーザー・パートナー・国家を巻き込んだ巨大な統合戦略を実行した。しかしその戦略の中身（Copilot）は、**選択肢を与えられた人間からは選ばれない製品**である。Fortune 10 の8社、Fortune 100 の70%は、Claude を選んでいる。

「企業は AI を買っているが、Copilot は買われていない」という構造は、客観的な市場データと完全に一致している。

---

## Word, Excel, PowerPoint で起きること ―― 数学的に避けられない破綻

2025年7月、スタンフォード大学の Varin Sikka らが arXiv に論文を投稿した。

**Varin Sikka, Vishal Sikka, "Hallucination Stations: On Some Basic Limitations of Transformer-Based Language Models" (arXiv:2507.07505)**

著者の Vishal Sikka は、SAP 元 CTO、Infosys 元 CEO、Oracle・BMW・GSK の取締役。

論文は、大規模言語モデル（LLM）が引き起こすハルシネーション（もっともらしい虚偽情報の生成）が、単なる学習データの不足や確率的なエラーの産物ではなく、**Transformer アーキテクチャの根底に存在する「計算複雑性のミスマッチ」による不可避の物理的・数学的現象**であることを証明した。

**論文の定理：**

標準的な Transformer ベースの LLM がテキストを生成する際の推論プロセス（自己注意機構）は、入力されたトークン数 N とベクトル次元数 d に対して、常に **O(N²·d)** の計算時間で実行されるという厳格な固定予算の制約下にある。

一方で、企業が LLM に要求する実務的なタスクの多くは、この計算予算をはるかに超える複雑性を持っている：

- 長大な文書群から特定の論理的矛盾を抽出 ―― **O(n³)**
- 複数のデータベースをまたいだ関係代数的な結合（JOIN） ―― **O(n³)**
- 行列の乗算 ―― **O(n³)**
- 巡回セールスマン問題の最適解の厳密検証 ―― **(n-1)!/2**（階乗オーダー）

モデルに与えられたタスクの固有の計算複雑性が、モデルの推論能力の限界である O(N²·d) を超えた瞬間、LLM はタスクを正しく実行するための計算ステップを踏むことが物理的に不可能になる。しかし、**LLM は計算の失敗を明示的に宣言する機能を持たない**ため、文脈上「最も確率的に高いと思われる次のトークン」を盲目的に生成するモードへと移行する。

その結果生じるのが、**文法的には完璧でありながら内容が完全に破綻している、確信に満ちた誤答** ―― すなわちハルシネーションである。

スケールアップでは越えられない。アーキテクチャに内在する天井である。

### Copilot で起きること

ある複雑度を超えたタスクで、Copilot は失敗するか、自信を持って誤答する。Word の長文編集、Excel の複雑な集計、PowerPoint の構造化、Outlook のメール要約 ―― いずれも、複雑度が閾値を超えた瞬間に静かに破綻する。

破綻したことを Copilot は告げない。**失敗と正答が外形上区別できない、というのが本質**である。

**Copilot が生成したコンテンツは、人間が逐語的に検証していない**。「自分で書いていない」「説明できない」部分が、企業文書、自治体文書、医療記録、財務記録の中に蓄積していく。

**ある日、住民票の数字が間違っていることが発見される。財務報告に存在しない取引が記載されていることが発見される。医療記録の処方が誤っていることが発見される**。それが Copilot 経由なのか人間のミスなのか、誰にも分からない。

### エージェント型 AI でも検証は不可能

Sikka 論文は、自律的に動作する「エージェント型 AI」における検証の難しさも指摘している。AI エージェントが生成した解が正しいかどうかを別の AI が検証するタスクは、多くの場合、**解を生成するよりもさらに高い計算複雑性**を伴う。

これは、複数の AI エージェントを組み合わせたとしても、高度なタスクの正確性を担保することは原理的に不可能であることを意味している。

---

## 攻撃面 ―― OS最深部への統合がもたらすコンプライアンス・クライシス

数学的に証明された不可避の限界が存在するにもかかわらず、Microsoft は Windows 11 および Microsoft 365 の OS およびプラットフォームの最深部に Copilot を統合する戦略を採った。

ここでの最大の問題は、システムが静かに破綻（計算限界を超過して誤答を生成）した際に、**失敗と正答を外形上区別する仕組みが存在しない**ことである。

Windows + Office + Copilot のスタックは、OS の最深部から AI 処理経路が常時開いた状態を作り出す。何が AI を経由したかが分からないシステムでは、攻撃者の介入痕跡も識別できない。

監査不可能な AI が、OS レベルで機微な患者データや財務情報にデフォルトでアクセス可能な状態に置かれることは、**重大な法的責任（Liability）の所在を曖昧にする**。AIが作成した間違った処方箋のサマリーや、存在しない架空の取引を含む財務レポートが生成され、それがシステム内に蓄積していくリスクは、もはや理論上の懸念ではなく、**現実の業務インフラを脅かすサイバーセキュリティ上の脆弱性そのもの**である。

**自治体、病院、銀行、学校 ―― 重要インフラのすべてが、監査不能な状態に置かれている**。

Mythos 級の攻撃速度の前で、AI の処理経路を完全に監査することは、外注先にも内部 IT 部門にも不可能である。法的にも物理的にも。**侵害が起きても、誰もそれに気づかない可能性が高い**。

---

## それでもナデラは Copilot を組み込むことをやめられない

社員に拒絶され、ユーザーに信頼されず、市場シェアで敗北しても、ナデラは Copilot 統合を止められない。理由は単純で、止めた瞬間に複数の前提が崩れるからである。

### 止められない理由

**(1) 株価の前提**

Microsoft の時価総額は3兆ドル超。この水準は **「AI が次の成長ドライバー」**という物語の上に成り立っている。ナデラが「Copilot は採用されていない」「設備投資を縮小する」と認めた瞬間、株価は急落する。

2026会計年度の設備投資1,000〜1,200億ドルの大半は、株式発行と負債で調達されている。**株価が下がれば、資金調達コストが急上昇し、建設中のデータセンターが完成できなくなる**。

**(2) OpenAI との戦略的地位**

2025年1月に独占関係を緩和したが、Microsoft Azure は依然として OpenAI のステートレス API の独占クラウドである。OpenAI が独自インフラ（Stargate）を構築する中で、**Microsoft は「OpenAI を持つクラウド事業者」という地位を維持する**ために、設備投資を続ける必要がある。

**(3) 長期契約の縛り**

Microsoft は2026年に入って、SK Hynix と数十兆ウォン規模の3年 DDR5 契約、Chevron と70億ドルの天然ガス契約、Samsung と長期 DRAM 契約、BlackRock + MGX と1,000億ドルファンドを締結した。**これらの契約は、Copilot が成功しても失敗しても支払い義務が発生する**。途中で止めれば、損失は確定する。

**(4) Sovereign AI 構想による国家安全保障への組み込み**

日本との100億ドル契約（2026〜2029年）は、単なるデータセンターの増設にとどまらず、ソフトバンクやさくらインターネットといった国内通信・クラウド事業者と深く連携し、日本国内にデータを留める **「Sovereign AI（主権AI）」インフラ**を構築する国家プロジェクトの中核を成している。

経済産業省（METI）が推進する数兆円規模の AI 投資戦略と完全に連動し、警察庁や内閣官房とのサイバーセキュリティ領域における密接な協業を含んでいる。サウジアラビアの Sovereign Cloud、UAE 資本（MGX）との連動、米国警察との Copilot 連携も同様。

**Microsoft は単なる企業ではなく、複数の国家との安全保障に関わる条約的関係に絡め取られている**。途中で撤退することは、これらの関係を破壊することを意味する。

**(5) ハードウェア更新サイクルの強制**

Copilot+ PC（NPU 40 TOPS、16GB DDR5、256GB SSD）の要件と Windows 10 サポート終了を組み合わせて、**世界の Windows ユーザーの相当数を新規 PC 購入に押し出した**。Copilot 統合を止めれば、この強制購入の正当化が崩れる。Dell、HP、Lenovo、Acer、ASUS、各 PC メーカーの2026年売上計画も連動して崩れる。

**(6) ナデラ個人の経歴**

ナデラは2014年に CEO 就任後、Microsoft をクラウドと AI の会社に転換した功績で評価されてきた。Copilot は彼の最大の戦略的賭けである。**ここで撤退すれば、ナデラの CEO 在任の総括が「失敗」になる**。

### 結果として何が起きるか ―― 自己破壊的な負のループ

止められないので、強制が深まる。「AI のリーディングカンパニー」としての成長ストーリーを演じ続け、巨額の資金調達を回し続けなければ、株価の暴落にとどまらず、複数の国家との安全保障に関わる条約的関係を破綻させることになる。**結果として、誰も望まない投資と OS への機能統合がさらに加速するという、自己破壊的な負のループが完成している**。

- ハードウェア要件のさらなる引き上げ → 世界中のユーザーが PC をさらに買い替える
- Copilot のさらなる深い OS 統合 → 切る選択肢がさらに失われる
- 個人ユーザーへの Copilot 強制（自動インストールはすでに開始）
- 自治体・医療・金融への営業圧力強化 → 法的責任が組織に転嫁され続ける
- Microsoft 365 E3（432ドル/年）への移行強制 → サブスクリプション料金が3倍に
- Windows 10 ESU 価格の継続的引き上げ
- 規制が緩い地域での新興市場展開（日本、東南アジア、中東） → 規制で守られた EEA 以外の被害が拡大

そして同時に、世界中のメモリ・電力・銅・ヘリウム・臭素・ナフサが、**売れない Copilot を動かすため**に消費され続ける。

医療現場が透析装置の包装材を確保できなくなる。自動車工場が部品供給に支障を来す。半導体工場がヘリウムを配給制で動かす。家庭の電気代が上がる。スマートフォンと PC の値段が上がる。気候変動対策が後退する。中小製造業が倒産する。

---

## 結論 ―― トップの暴走を止められなくなった組織は物理的に破綻する

ナデラの暴走を止められなくなった Microsoft がどうなるか ―― ナデラは強制的に止められるまで暴走する。これは、人類が繰り返してきたパターンである。

Microsoft が優良で巨大な企業だっただけに、すでに世界に撒き散らされている被害は計り知れない。これからその被害は加速する。

それでも、Windows と Office を使い続けますか？

PC の買い替え、Office 利用料の値上げ、そしてサイバー攻撃対策の費用の増加に苦しむことになる。

Microsoft のプラットフォームは、もはやかつてのような「業務を支える中立的で安定したインフラ」ではなく、**自社の予算を無制限に吸い上げ、コンプライアンス上の社会的責任を脅かす「高い維持費を伴うハイリスクなエージェント」**へと変質した。

デスクトップ環境におけるオープンソース OS（Linux等）への移行、オフィススイートの脱 Microsoft 化、および必要に応じた独立系 AI ベンダー（Anthropic 等）の API を介した限定的かつ検証可能な形での AI の導入 ―― これは、複合的なグローバル危機に巻き込まれることを防ぎ、組織の自己決定権と予算を守り抜くための、最も確実かつ合理的なテクノロジー戦略である。

**Linux に早急に移行しましょう。**

Claude と一緒に学べば、Linux も難しくない。

具体的な実践方法は、記事「[Claude と一緒に学ぶ Debian](https://aiseed.dev/claude-debian/)」
を書いたので参考にしてください。

---

## 参考文献

### LLM の数学的天井
- Varin Sikka, Vishal Sikka, "Hallucination Stations: On Some Basic Limitations of Transformer-Based Language Models", arXiv:2507.07505 (2025年7月)
- WIRED, "A research paper suggests AI agents are mathematically doomed to fail. The industry doesn't agree." (2026年1月)

### Microsoft / Copilot 強制
- Mozilla Blog, Linda Griffin, "Old habits die hard: Microsoft tries to limit our options, this time with AI" (2026年4月)
- The Register, "Mozilla calls out Microsoft over Copilot push in Windows" (2026年4月)
- AI Business Weekly, "Accenture Ties Promotions to AI Use; KPMG, Meta Follow"
- Microsoft Internal Memo, "Using AI Is No Longer Optional" (2025年)
- HRD America, "Microsoft offers to buy out 7% of its workforce as it pivots towards AI"
- TNW, "Meta cuts 8,000 jobs and Microsoft offers first-ever buyouts as Big Tech converts payroll into AI capital expenditure"

### Copilot 利用率・採用失敗
- Recon Analytics, "AI Choice 2026: Why Licenses Don't Equal Adoption"（米国15万人調査、2026年1月）
- Stackmatix, "Microsoft Copilot Adoption Statistics & Trends (2026)" (2026年4月)
- AI Business Weekly, "Microsoft Copilot Statistics 2026: Users & Adoption" (2026年3月)
- Avantiico, "The Definitive Microsoft 365 Copilot Adoption Guide for Businesses [2026]" (2026年4月)
- Adoptify AI, "Why Microsoft Copilot Adoption Often Stalls" (2026年1月)
- Whatfix, "Microsoft Copilot Adoption: From Enterprise Rollout to Habitual Usage" (2026年1月)
- Gartner Copilot パイロット拡大率調査

### 企業 AI 市場での Claude / Anthropic 採用
- Medium, David C., "Anthropic Just Passed OpenAI in Revenue. Here Is Why It Matters." (2026年4月)
- AI Business Weekly, "Claude AI Statistics 2026: Users, Revenue & Market Share" (2026年4月)
- Searchlyn, "Claude Statistics: Users, Revenue & Growth in 2026" (2026年4月)
- Second Talent, "Claude AI Statistics and User Trends for 2026" (2026年4月)
- The AI Corner, "Claude AI in 2026: Stats, Workflows, and Resources" (2026年3月)
- Thunderbit, "Claude Gemini Adoption Trends and Statistics for 2026" (2026年3月)
- IdeaPlan, "AI Coding Assistants Market Share 2026"
- Uvik Software, "AI Coding Assistant Statistics 2026: 50+ Key Data Points"
- systemprompt.io, "Claude Code vs Cursor"
- Menlo Ventures, "2025 Enterprise LLM Spend Report"
- Anthropic Series G 発表 (2026年2月)
- Anthropic ARR 300億ドル発表 (2026年4月)

### Windows ハードウェア要件・廃棄
- Microsoft, "Windows 11 Specs and System Requirements"
- Canalys, "End of Windows 10 support could turn 240 million PCs into e-waste" (2023年12月)
- Tom's Hardware, "Microsoft's draconian Windows 11 restrictions" (2024年12月)
- Microsoft Learn, "Extended Security Updates (ESU) program for Windows 10"
- Brytesoft, "Windows 10 ESU Cost in 2026: 3-Year Pricing Breakdown"
- Microsoft Learn, "Windows 11, versions 25H2 and 24H2 required diagnostic data events and fields"

### Microsoft データセンター建設計画
- Network World, "Microsoft will invest \$80B in AI data centers in fiscal 2025" (2025年5月)
- Data Center Dynamics, "Microsoft spent \$11.1bn on data center leases alone in Q1 2026" (2026年2月)
- Introl Blog, "Hyperscaler CapEx Hits \$690B in 2026" (2026年2月)
- Microsoft On the Issues, "Made in Wisconsin: The world's most powerful AI datacenter" (2025年9月18日)
- Microsoft Blog, "Inside the world's most powerful AI datacenter"
- Data Center Frontier, "Microsoft Builds for Two Worlds: Sovereign Cloud and AI Factories" (2026年)
- Microsoft Source Asia, "Microsoft deepens its commitment to Japan with \$10 billion investment" (2026年4月3日)
- Windows Forum, "Sakura Internet Rises as Japan Sovereign AI Gets a \$10B Boost"
- Dark Reading, "Microsoft Bets \$10 Billion to Boost Japan's AI, Cybersecurity"
- RCR Wireless, "Five key things to know about AI infra investments in Japan"

### CO₂ 排出量・気候変動
- NYC Comptroller, NYCERS Annual Climate Report FY2025（Microsoft 2020年比 23.4% 増加）
- Energy Platform News, "Microsoft carbon emissions jump as AI and cloud demand rises"
- Goldman Sachs, "AI is poised to drive 160% increase in data center power demand"
- Stand.earth Research Group, "160% data center carbon footprint increase" (2026年4月)
- IT Pro, "Gas-powered data centers could more than double Microsoft's emissions" (2026年4月)

### メモリ・ストレージ
- Counterpoint Research, "Memory Prices Soar by 50% in Q4, Rally to Continue in 2026" (2026年1月)
- BuySellRam, "Samsung's 100% DRAM Price Hike and Why Even Apple Had to Pay Up"
- SmarterArticles, "Priced Out by AI: The Memory Chip Crisis Hitting Every Consumer"
- SoftwareSeni, "DRAM Prices in 2026 Have Doubled and the Numbers Are Getting Worse"
- Tom's Hardware, "OpenAI's Stargate project to consume up to 40% of global DRAM output" (2025年10月)
- Open Markets Institute, "OpenAI's RAMpage" (2026年2月)
- TrendForce, "From Annual Deals to 3–5 Year LTAs: Samsung and SK hynix" (2026年4月)
- IDC, "Global Memory Shortage Crisis" (2026年2月)
- IEEE Spectrum, "AI Boom Fuels DRAM Shortage and Price Surge" (2026年4月号)

### データセンター完成不能・資材
- Manufacturing Dive, "The great data center delay" (2026年4月)
- Tom's Hardware, "Half of planned US data center builds have been delayed or canceled" (2026年4月)
- Tom's Hardware, "AI data-centre buildout pushes copper toward shortages" (2025年12月)
- Power Magazine, "Transformers in 2026" (2026年1月)
- The Invading Sea, "Supply-chain delays threaten power grid" (2025年12月)
- Sandstone Group, "More than half of the Data Centers may be delayed" (2026年4月)

### Chevron 契約・化石燃料
- Fortune, "Microsoft and Chevron enter exclusivity deal" (2026年4月1日)
- IDC Nova, "Microsoft, Chevron, and Engine No. 1 Forge Landmark Gas-to-Power Partnership"
- Energynow, "Microsoft in Talks With Chevron, Engine No. 1 Over \$7 Billion Texas Power Plant"
- Motley Fool, "Chevron Could Build a \$7 Billion Gas Plant to Power Microsoft's AI Ambitions"

### イラン戦争・ホルムズ海峡
- Wikipedia, "2026 Iran war"
- Wikipedia, "Reactions to the 2026 Iran war"
- Wikipedia, "Economic impact of the 2026 Iran war"
- Britannica, "2026 Iran war: Explained, United States, Israel, Strait of Hormuz"

### ナフサ危機・医療インフラ
- CNN, "Noodles, kidney dialysis, condoms – the global oil crisis is turning into an everything crisis" (2026年4月)
- CNBC, "Iran war Strait of Hormuz petrochemicals oil plastics" (2026年3月)
- Inbound Logistics, "The Invisible Shortage: How Petrochemical Shortages Could Impact Packaging" (2026年4月)
- Plastmatch News, "Hormuz Strait Blockade Sparks Shortage of Plastic Raw Materials" (2026年4月)
- Financial Content, "Naphtha Surges to \$1,000: The Petrochemical Crisis of 2026 Explained" (2026年3月)
- Iran International, "Strikes on petrochemical hubs leave Iran short of plastics" (2026年4月)
- PUdaily, "Japanese MDI Suppliers Forced to Raise Prices as Upstream Supply Risks Persist"（出光興産、東ソー）
- Japan NRG Weekly 20260406
- CodeBlue, "Malaysia Faces Emerging Shortage Of Dialysers, Haemodialysis Components"
- ICIS, "INSIGHT: Asia petrochemical demand muted amid feedstock shortage" (2026年4月)

### Windows / Microsoft 365 ユーザー数
- Microsoft 公式 Windows Experience Blog (2025年6月)
- Microsoft 2026年Q2決算電話会議 (2026年1月28日)
- StatCounter Global Stats (2026年2月)
- Expanded Ramblings, "Microsoft Office Statistics (2026)" (2026年2月)

### 既存データセンター・系統影響
- arXiv:2509.07218, "Electricity Demand and Grid Impacts of AI Data Centers"
- World Resources Institute, "Powering the US Data Center Boom"

---

[Geminiのチェック資料](014-windows-office-facts.pdf)
