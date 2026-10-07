# サイバー攻撃の調査メモ(2025-01〜2026-10) ── 委託先の特権と、外向き通信

2026-10-08。構造分析に「守りは買えない」の章を書く前の事実確認。
発注者の二つの仮説を、一次情報で確かめる。

1. 大事件は、委託先(保守業者・MSP・再委託先)に渡した root/管理者権限の管理が弱い所から起きているのではないか
2. 外向きの HTTPS もできるだけ塞がなければならないのではないか

凡例:○=一次資料で確認、△=二次資料のみ/一部、×=否定または別経路、?=未公表。
数字は引用元の頁で確認したものだけ。確認できないものは「未確認」と書く。

---

## 第 1 部 事件の表 ── 委託先・特権・サプライチェーン

| # | 日付 | 被害者 / 業種 | 攻撃者 | 初期侵入経路 | 委託先/特権 | 奪取した権限・到達点 | 影響 | 出典 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2025-06-05 侵入 / 10-19 発覚 | アスクル(日本・EC/物流) | 未公表 | 業務委託先向け管理者アカウントの ID/PW が漏えいし VPN 経由で侵入。当該アカウントは「例外的に多要素認証を適用していなかった」 | ○ | 管理者→EDR 無効化→認証情報収集→横展開(6/5〜10/19、約 4 か月半)。暗号化+バックアップ削除 | 受注・出荷停止。約 74 万件(事業所向け 59 万、個人向け 13.2 万、取引先 1.5 万、役職員 2,700) | https://netshop.impress.co.jp/n/2025/12/15/15295 ・ https://it.impress.co.jp/articles/-/28741 |
| 2 | 2025-09-29(侵入は約 10 日前) | アサヒグループ HD(日本・飲料) | Qilin が犯行声明 | 「拠点にあるネットワーク機器を経由し」侵入→データセンターで「パスワードの脆弱性をついて管理者権限を奪取」 | ×(委託先関与の公表なし) | 管理者権限。DC 内サーバ+ゼロトラスト移行前 PC を暗号化 | 物流再開 2025-12-02/03、通常化 2026-02。漏えい確定約 11.5 万件、可能性約 192 万件 | https://www.asahigroup-holdings.com/newsroom/detail/20251127-0104.html ・ https://www.asahigroup-holdings.com/newsroom/detail/20260218-0101.html |
| 3 | 2025-11-07 | 東海大学の委託先・東海ソフト開発(ネットワーク保守・管理) | 未公表 | 「リモートメンテナンス用の入り口から、何らかの方法で窃取した管理者アカウントを用いて進入された可能性」(大学第 1 報) | ○(委託先自身の保守用管理者アカウント) | 委託先サーバ 20〜30 台に侵入・暗号化。サーバに大学の教職員・学生の ID/PW 入りファイル(保護なし) | 漏えい対象 最大延べ 193,118 人(第 2 報 2026-02-18) | https://www.u-tokai.ac.jp/uploads/2025/11/98f076c9a565146be4c95ac155960fd04f8d5ddc.pdf ・ https://scan.netsecurity.ne.jp/article/2026/03/06/54778.html ・ IPA 解説書も事例として引用 |
| 4 | 2025-11-05 | 国立国会図書館(開発中システム) | 未公表 | 再委託先の網に侵入→委託先 IIJ 管理の開発環境へ | ○(再委託先経由) | 開発環境の構成情報・一部利用者情報 | 当初 40,373 件の可能性→2026-03-11 第 3 報で漏えいなし | https://www.ndl.go.jp/jp/news/fy2025/251111_01.html ・ https://scan.netsecurity.ne.jp/article/2026/03/25/54900.html |
| 5 | 2026-04-02 | YCC 情報システム(山形市等の自治体システム委託先) | 未公表 | 「ネットワーク機器の管理者アカウントに係る認証情報が…推測または取得され…内部ネットワークに侵入」 | ○(委託先自身の機器管理者アカウント、弱いパスワード運用) | ファイルサーバ暗号化、脅迫文 | 山形市 約 50 万件(健康情報等)、山形県 約 2 万 6,800 件ほか。外部送信の明確な痕跡なし | https://www.yamagata-ycc.co.jp/news/20260520-1/ ・ https://internet.watch.impress.co.jp/docs/news/2102758.html |
| 6 | 2026-03-13 | メディカ出版(大学の委託先) | 未公表 | 未公表 | △(委託先が被害、経路不明) | 社内サーバ暗号化 | 近畿大、大手前大(431 名)、東京医療保健大などに波及 | https://pc.watch.impress.co.jp/docs/release/atpress/2094009.html ・ https://scan.netsecurity.ne.jp/article/2026/04/23/55125.html |
| 7 | 2026-08-14 | 両毛システムズ(自治体・ガス会社向け IT ベンダー) | 未公表 | 「調査中」 | ?(ベンダー自身が被害) | 社内システム | 伊勢崎市 3,789 件、大東ガス約 12.4 万件など(二次) | https://www.ryomo.co.jp/news/202608_02.html |
| 8 | 2025-01 下旬 | 米 MSP(匿名)とその顧客 | Qilin アフィリエイト | MSP 管理者へ ScreenConnect 偽装フィッシング。AitM(evilginx)で TOTP も窃取し MFA 突破 | ○(MSP の RMM「スーパー管理者」) | RMM の super administrator→攻撃者の ScreenConnect を複数顧客へ配布→Qilin 展開 | 複数顧客で暗号化 | https://www.sophos.com/en-us/blog/sophos-mdr-tracks-ongoing-campaign-by-qilin-affiliates-targeting-screenconnect |
| 9 | 2025-05 公表 | MSP(匿名)とその顧客 | DragonForce | MSP の SimpleHelp RMM の脆弱性(CVE-2024-57727/57728/57726) | ○(RMM 乗っ取り) | RMM 経由で顧客端末に配布、二重恐喝 | 複数組織 | https://www.sophos.com/en-us/blog/dragonforce-actors-target-simplehelp-vulnerabilities-to-attack-msp-customers/ |
| 10 | 2025-04-17 侵入 | Marks & Spencer(英・小売) | Scattered Spider 系+DragonForce | CEO「social engineering and entering through a third party rather than a system weakness」。第三者は TCS のヘルプデスクと報道(M&S は社名を明言せず) | ○(委託先ヘルプデスク、△社名) | 未公表 | 営業利益影響 £300m、オンライン注文停止数週間 | https://www.cyberdaily.au/security/12131-m-s-says-cyber-incident-resulted-from-third-party-attack-faces-625m-loss ・ https://diginomica.com/learnings-retail-cyber-attack-victims-1-more-ms-out-body-experience |
| 11 | 2025-04 | Co-op(英・小売) | Scattered Spider 系(推定) | ヘルプデスク等へのソーシャルエンジニアリング(推定) | ? | 会員システム | 全会員 650 万人分流出(CEO 証言) | https://www.hl.co.uk/shares/stock-market-news/company--news/data-on-all-6.5m-co-op-members-stolen-in-attack-ceo |
| 12 | 2025-08-31 検知 | Jaguar Land Rover(英・自動車) | Scattered Lapsus$ Hunters が声明 | 攻撃者は「従業員の Jira 認証情報」と主張。JLR は公表せず | ×/? | 未公表 | 全英工場停止〜10 月 8 日、四半期の cyber related costs £196m、英政府 £1.5bn 融資保証 | https://media.jlr.com/corporate/news/2025/09/statement-cyber-incident |
| 13 | 2025-09-19 | Collins Aerospace MUSE(空港チェックイン共通基盤)→Heathrow/Brussels/Berlin | ENISA がランサムウェアと確認 | 未公表 | ○(第三者ソフトウェア供給者の障害が波及) | 未公表 | 欠航多数 | https://www.techrepublic.com/article/news-eu-airport-ransomware/ |
| 14 | 2025-08-08〜18 | Salesloft Drift→顧客 Salesforce(700 超) | UNC6395 | 第三者アプリ Drift の OAuth/リフレッシュトークン窃取 | ○(第三者アプリに委任した常設・広範囲の権限) | Salesforce API で一括取得、AWS キー・Snowflake トークン等を収集 | 700 超の組織 | https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift |
| 15 | 2025-11-19〜21 | Gainsight→顧客 Salesforce | ShinyHunters が声明 | 公開 Connected App の OAuth トークン悪用 | ○ | 委任権限で API 呼び出し | 200 超(二次) | https://kudelskisecurity.com/research/compromise-of-third-party-application-gainsight-enables-salesforce-oauth-token-abuse |
| 16 | 2025-08 検知 / 10-15 公表 | F5(ネットワーク機器ベンダー) | 国家支援(F5) | 長期潜伏(経路非公表) | ×(ベンダー自身。供給網リスク) | BIG-IP のソースコードと未公開脆弱性情報 | CISA 緊急指令 ED 26-01 | https://www.cisa.gov/news-events/directives/ed-26-01-mitigate-vulnerabilities-f5-devices |
| 17 | 2025-07 | オンプレ SharePoint(ToolShell CVE-2025-53770) | 中国系 3 グループ(Microsoft) | 公開サーバのゼロデイ | × | Web シェル→機械鍵窃取。ランサム展開も | 400 超のシステム(Eye Security) | https://www.recordedfuture.com/blog/toolshell-exploit-chain-thousands-sharepoint-servers-risk |
| 18 | 2025-09-25 | Cisco ASA/FTD | ArcaneDoor(国家系) | 境界 FW のゼロデイ(CVE-2025-20333/20362)、ROM 改変で永続化 | × | 機器の root 相当 | CISA ED 25-03 | https://www.cisa.gov/news-events/directives/ed-25-03-identify-and-mitigate-potential-compromise-cisco-devices |
| 19 | 2025-08 | Citrix NetScaler | 不明 | 認証前 RCE CVE-2025-7775、CitrixBleed 2 | × | Web シェル | CISA KEV | https://www.helpnetsecurity.com/2025/08/26/netscaler-adc-gateway-zero-day-exploited-by-attackers-cve-2025-7775/ |
| 20 | 2025-09-15 | npm「Shai-Hulud」 | 不明 | 窃取した npm/GitHub トークンでパッケージ改ざん、postinstall で秘密情報収集、Actions 注入 | ○(開発者の常設トークン) | npm 公開権限・GitHub PAT・クラウド鍵 | 500 超パッケージ | https://wiz.io/blog/shai-hulud-npm-supply-chain-attack |
| 21 | 2026-04-29→08-04 | 「Mini Shai-Hulud」:SAP CAP→172 パッケージ→@antv→keyv/cacheable | 不明 | preinstall で Bun を落としスティーラー実行、npm トークンで自己増殖 | ○ | CI/CD・クラウド・SSH の秘密情報 | 8 月までに 2,225 コンポーネント版(Sonatype) | https://www.sonatype.com/blog/mini-shai-hulud-npm-attack-more-than-2200-components-impacted |
| 22 | 2025-01〜 / 02-20 検知 | Oracle Health(旧 Cerner)旧サーバ→米病院 | 不明 | 「compromised customer credentials」で未移行の旧サーバへ | △ | 患者データ複製 | Oracle は顧客通知のみ | https://bleepingcomputer.com/news/security/oracle-health-breach-compromises-patient-data-at-us-hospitals |
| 23 | 2026-08〜09 | ConnectWise ScreenConnect 利用 MSP | 不明 | クライアント側の権限管理不備 CVE-2026-84869 | ○(RMM) | 無承認のファイル転送・実行 | CISA KEV 2026-09-11 | https://cyber.gc.ca/fr/alertes-avis/bulletin-securite-connectwise-av26-903 |

比較(期間外):イセトー 2024-05(VPN から侵入、委託元多数に波及。再発防止「VPN 廃止と認証強化」https://www.iseto.co.jp/news/news_202410.html)、KADOKAWA 2024-06(従業員のフィッシング、委託先経路ではない)、Snowflake 2024(約 165 組織。インフォスティーラー由来の認証情報、MFA なし、「契約業者が私用兼用端末で作業」https://cloud.google.com/blog/topics/threat-intelligence/unc5537-snowflake-data-theft-extortion)。

## 第 2 部 統計(年・出典)

- Verizon DBIR 2026(2024-11〜2025-10):「31% of breaches now start with software vulnerabilities(beating stolen passwords)」「48% involve ransomware」(公式頁で確認 https://www.verizon.com/business/resources/reports/dbir/)。第三者関与 48%(2025 年版 30%、2024 年版 15%)は二次資料で一致、**一次 PDF 本文は未確認**。
- Mandiant M-Trends 2026(2025 年調査):初期侵入はエクスプロイト 32%(6 年連続首位)、ボイスフィッシング 11%、prior compromise 10%(ランサムでは 30%、前年 15% から倍増)、メールフィッシング 6%。滞留時間中央値 14 日。「By compromising third-party SaaS vendors, attackers steal hard-coded keys and personal access tokens, using those secrets to seamlessly pivot into downstream customer environments」https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2026
- Sophos ランサムウェアの現状 2026(17 か国、n=2,158):根本原因は悪意あるメール 26%、フィッシング 24%、認証情報の侵害 23%、脆弱性悪用 18%(2025 年版 32% から低下)。「攻撃の 79% はアイデンティティベースの手法で開始」。認証情報侵害が原因の組織の **97% がインシデント時点で何らかの MFA を導入済み** → MFA が全部には適用されていない(例外アカウントが穴)。https://assets.sophos.com/X24WTUEQ/at/g7f9jwjwhsmrwsxxc9h8ftj6/sophos-state-ransomware-report-2026-ja.pdf
- IPA 情報セキュリティ 10 大脅威 2026(2026-01-29):組織編 2 位「サプライチェーンや委託先を狙った攻撃」(8 年連続)。1 位ランサム、4 位脆弱性悪用。解説書は手口に「MSP が利用する資産管理ソフトウェア等にマルウェアを仕込む」、事例に東海ソフト開発。https://www.ipa.go.jp/pressrelease/2025/press20260129.html ・ https://www.ipa.go.jp/security/10threats/omgdg50000008fi8-att/kaisetsu_2026_soshiki.pdf
- 警察庁 令和 7 年版:ランサム被害報告 226 件。「侵入経路は VPN 機器が 6 割以上」「未修正のぜい弱性、漏えいした認証情報や簡易なパスワード、設定不備等を悪用」「管理者権限の奪取やセキュリティ無効化を試み」。https://www.npa.go.jp/publications/statistics/cybersecurity/data/R7/R07_cyber_jousei.pdf
- 警察庁 令和 8 年上半期(2026-09-10):123 件(半期で過去最多)、中小 79/大企業 31/団体等 13、製造業 37 件が最多、「VPN 機器が約 5 割」。https://www.npa.go.jp/publications/statistics/cybersecurity/data/R8kami/R08_kami_cyber_jousei.pdf 。**委託先経由の割合という統計は警察庁資料には無い(未確認)**。
- JIPDEC/ITR 2025:メール 28.3%、VPN 等脆弱性 20.8%、RDP 19.9%。https://scan.netsecurity.ne.jp/article/2025/03/24/52537.html
- JPCERT/CC:委託先・特権アクセスの割合を示す一次統計は見つからず(未確認)。

## 第 3 部 仮説 1 の検証 ── 「委託先に root を渡し、管理が弱い所が穴」

**支持する事実**
- アスクル:起点は「業務委託先向け管理者アカウント」、MFA が「例外的に」未適用。侵入から発覚まで 4 か月半、EDR 無効化・権限奪取・横展開・バックアップ削除まで到達。
- 東海ソフト開発:委託先の「リモートメンテナンス用の入り口」+「窃取した管理者アカウント」。委託先のサーバに大学の ID/PW が「保護なし」で置かれていた。
- YCC:委託先自身の「ネットワーク機器の管理者アカウント」が「推測または取得」= 弱いパスワード運用。
- M&S:CEO「entering through a third party rather than a system weakness」。委託先ヘルプデスクがパスワードリセット権限を持つ構造が突破口。
- MSP/RMM:ScreenConnect の super administrator 一つ(TOTP は AitM で突破)で複数顧客に配布。SimpleHelp は RMM 自体の脆弱性。
- 第三者アプリの委任権限:Drift・Gainsight の OAuth トークンは常設・広範囲。GTIG は「スコープ制限・IP 制限」を勧告。
- Snowflake(2024):契約業者の私用端末→インフォスティーラー→MFA なしのまま数年有効。
- Sophos 2026:認証情報侵害の 97% が MFA 導入済み ── 例外アカウント(委託先用など)が穴という示唆。

**反証・限定**
- アサヒ:自社拠点の境界機器から侵入し、DC 内の「パスワードの脆弱性」で管理者権限奪取。委託先アカウントではない。
- KADOKAWA:従業員のフィッシング。JLR:攻撃者の主張は従業員の Jira 認証情報。UNC6040:従業員へのボイスフィッシングで Salesforce Data Loader を承認させた。
- 境界機器のゼロデイが件数では最大:ToolShell(400 超)、Cisco ASA、Citrix、F5。M-Trends でエクスプロイト 32% が首位、DBIR で脆弱性悪用 31% が首位、警察庁で VPN 機器 5〜6 割。
- ソフトウェア供給網(Shai-Hulud 系)の穴は「委託先の特権」ではなく「開発者の常設トークン」。
- 重なり:委託先経路でも実際の入口は VPN/リモート保守口(アスクル=VPN、東海ソフト=リモメン入口、イセトー=VPN)。「委託先の特権」と「境界機器」は排他ではなく、**委託先用の常設リモートアクセス + MFA の例外 + 共有/推測可能なパスワード**という組合せが共通項。

**結論(第 1 部・第 2 部から)**
- 日本の 2025〜26 年の大型事例(アスクル、東海ソフト開発、YCC、国会図書館の再委託先)では、仮説 1 は強く支持される。
- 件数で見れば、世界では境界機器(VPN・FW・公開サーバ)のゼロデイが首位。ただし日本の警察庁統計でも VPN 機器が 5〜6 割で、委託先の保守口の多くは VPN なので、二つは重なっている。
- 「第三者関与 48%」(DBIR、二次)は委託先の特権悪用に限らず、第三者ソフト・SaaS の侵害を含む広い定義。
- 大事件の共通点は、入口より **入った後に全体の管理者権限まで一本道で到達したこと**(アスクル、アサヒ、東海ソフト、YCC、MSP 二件)。委託先のアカウントは最初から管理者であることが多く、入口と root の距離がゼロ。

## 第 4 部 一次資料が示す委託先特権の対策

- CISA/NSA/FBI + 英加豪 NZ 共同勧告 AA22-131A(MSP と顧客向け):MSP アカウントは全部に MFA、特権として扱う。「Do not reuse admin credentials across multiple customers」「consider the use of time-based privileges」、最小権限、管理しなくなった MSP アカウントの無効化、MSP の接続と活動のログを顧客に可視化、ログ保持 6 か月以上、MSP 接続用に専用の経路。https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-131a
- NCSC「Secure system administration」:Tier 0〜3 の階層化、下位端末から上位を管理しない、高リスク操作は「just in time」「just enough」+ PAW、PAM、ログ・監査。https://www.ncsc.gov.uk/collection/secure-system-administration/risk-manage-administration-using-tiers
- NCSC「Principles for secure PAWs」(MSP に委ねる場合):「Identity services should never be shared and all MSP users should use accounts administered by your organisation」「must not use any shared access」「monitor and audit all connectivity from a MSP」。https://www.ncsc.gov.uk/collection/principles-for-secure-paws/establish-trust-foundation
- IPA 10 大脅威 2026 解説書(2 位の対策):「委託元組織が委託先組織のセキュリティ対策状況と情報資産の管理の実態を定期的に確認できる契約」「構成管理と変更管理を行い、委託先、取引先の ID やネットワーク接続を把握する」「責任範囲を明確化」。
- Mandiant/Google(Snowflake・Drift):全アカウント MFA、ネットワーク許可リスト、契約業者を含む認証情報のローテーション、Connected App のスコープ最小化・IP 制限、監査ログ長期保持。
- Sophos(MSP ScreenConnect):フィッシング耐性認証(FIDO2)、条件付きアクセス。TOTP は AitM で突破された。
- 被害企業の再発防止:アスクル「業務委託先を含むすべてのリモートアクセスに MFA、管理者権限の厳格な運用」;アサヒ「リモートアクセス VPN 装置の廃止」「ゼロトラストへの完全移行」「アカウント作成・変更・削除の自動化」;イセトー「VPN 廃止と認証強化」「管理区域外へデータの移送ができない環境」。
- 日本の制度:総務省の自治体ガイドライン 2025-03-28 改定版が委託先管理・特権 ID・MFA・リモート保守を扱うと報道(条文未確認)。

### 未確認・注意
- DBIR 2026 の第三者関与 48% は一次 PDF 未取得。
- M-Trends 2026 のクラウド別内訳(第三者侵害 17% 等)は SecurityWeek 経由。
- アスクル・東海ソフト開発・YCC・メディカ出版の攻撃者名は公表なし。JLR の「Jira 認証情報」は攻撃者の主張のみ。M&S の「TCS」は報道のみ。
- 「警察庁:1,000 万円超の被害の 6 割が委託先経由」という数字は警察庁 PDF で確認できず、採用しない。

---

## 第 5 部 仮説 2 ── 外向き HTTPS を塞ぐべきか

**結論**:方向は支持される。ただし言い方を変える。公的指針の表現は「443 を塞ぐ」ではなく
**「送信方向を既定拒否(deny by default)にし、宛先を名指しで許可する」**(NIST SP 800-41r1、CISA ほか 2024、ACSC)。
443 そのものを塞げという指針は無い。「C2 の X% が 443」という単一の統計も 2025〜26 の主要レポートには無い(未確認)。

### 5.1 証拠 ── C2 と持ち出しは HTTPS と正規クラウドに寄っている

- MITRE ATT&CK T1071.001(Web Protocols):HTTP/S に紛れる手口。T1567.002(クラウドストレージへの持ち出し):Dropbox・Google Drive・OneDrive・MEGA・S3 等を名指し、道具は Rclone(Medusa、Storm-0501 ほか)。緩和策 M1021「Web proxies can be used to enforce an external network communication policy that prevents use of unauthorized external services.」T1041 の DLP は「unencrypted protocols」のみ対象(暗号化経路には効かない)。https://attack.mitre.org/techniques/T1567/002/
- Recorded Future(Insikt):400 超のマルウェアファミリの 25% が正規インターネットサービス(LIS)を悪用、うち 68.5% が複数、インフォスティーラーは 37%。最多はクラウドストレージ、次いで Telegram・Discord。https://www.recordedfuture.com/research/threat-actors-leverage-internet-services-to-enhance-data-theft-and-weaken-security-defenses(公開年月は未確認)
- Recorded Future 2025 Year in Review(2026-03-19):LummaC2 がインフォスティーラー C2 の 35% 超。BRICKSTORM(UNC5221)は Cloudflare Workers を C2 に。イラン系は Cloudflare Workers / Supabase / Backblaze / Dropbox / Discord を持ち出しに。https://assets.recordedfuture.com/insikt-report-pdfs/2026/cta-2026-0319.pdf
- ReliaQuest(IR 事例 2023-09〜2024-07):Rclone が事例の 57%、次に WinSCP、cURL。宛先に MEGA。https://reliaquest.com/blog/exfiltration-tools/
- Red Canary 2026:Ingress Tool Transfer が顧客の 13.3%。緩和に「Windows host firewall to block outbound network connections for commonly abused LOLbins」。https://redcanary.com/threat-detection-report/techniques/ingress-tool-transfer/
- NVISO(2025-12-16):インフォスティーラーが Telegram Bot API で持ち出し。「Where there is no legitimate business need, blocking traffic to api.telegram.org is highly recommended.」https://blog.nviso.eu/2025/12/16/the-detection-response-chronicles-exploring-telegram-abuse/
- M-Trends 2026・DBIR 2026:持ち出し経路の割合の集計は公開版に無し(未確認)。

### 5.2 事例 ── 送信制御が効いたか

| 事例 | 送信先 | 送信制御で |
|---|---|---|
| Shai-Hulud(npm、2025-09):秘密情報を公開 GitHub リポへ、Actions から webhook.site へ | api.github.com、webhook.site | webhook.site は止まる。**GitHub は止まらない**(開発機・CI は GitHub を許している) |
| Shai-Hulud 2.0(2025-11):25,000 超のリポ、GitHub トークン 775・AWS 373・GCP 300 | GitHub のみ | 止まらない。ただしビルド機から GitHub/npm 以外を全遮断していれば、盗んだ鍵の「次の悪用」は妨げられる |
| ToolShell(SharePoint、2025-07):MachineKey は攻撃者の GET への**応答**で出る。後続 C2 は独自ドメイン | inbound 応答/独自ドメイン | **鍵窃取は止まらない**(応答で出る)。後続の C2・ツール取得は止まる |
| Medusa(CISA AA25-071A):Rclone で C2 へ持ち出し、Cloudflared でトンネル | 独自 C2、Cloudflare | Rclone→C2 は止まる。Cloudflared は 7844/tcp,udp を閉じれば止まる |
| Interlock(CISA AA25-203A):AzCopy で Azure Blob へ | *.blob.core.windows.net | Azure を業務で使う組織では止まらない |
| TryCloudflare 悪用(Proofpoint):RAT 配布 | *.trycloudflare.com | Cloudflare を丸ごと許していると止まらない。ドメイン単位なら止まる |
| Webworm(ESET 2026):Discord と Microsoft Graph API を C2 に | discord.com、graph.microsoft.com | M365 利用組織で Graph は止まらない。Discord は業務不要なら止まる |

### 5.3 公的指針の原文

- NIST SP 800-41 Rev.1:「Generally, all inbound and outbound traffic not expressly permitted by the firewall policy should be blocked」「Firewall policies should be based on blocking all inbound and outbound traffic, with exceptions made for desired traffic.」送信プロキシは「By far the most common type of outbound proxy is for HTTP.」https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf
- CISA/NSA/FBI/ACSC/CCCS/NCSC-NZ(2024-12-04、通信インフラ向け):「strict, default-deny ACL strategy to control inbound and egressing traffic」。https://www.cisa.gov/resources-tools/resources/enhanced-visibility-and-hardening-guidance-communications-infrastructure
- NCSC(UK)Network security fundamentals:最後に deny all を置く(方向は特定せず)。https://www.ncsc.gov.uk/guidance/network-security-fundamentals
- ACSC 37 戦略の一つ「Deny corporate computers direct internet connectivity. Use a gateway firewall to require use of … an authenticated web proxy server for outbound web connections.」Essential Eight(8 戦略)には送信フィルタは含まれない。
- CIS Controls v8:4.4(サーバにファイアウォール)、9.3(URL フィルタ)、13.4(セグメント間フィルタ)。
- NIST SP 800-207(ゼロトラスト):送信遮断の明示なし。
- 日本:NISC 統一基準(令和 7 年度版)6.4.1 は経路制御・アクセス制御・不正通信の「監視」まで。送信の既定拒否は明示していない。IPA は 2011〜2012 年の資料で「出口対策」(ファイアウォールの外向き通信の遮断ルール、プロキシ経由の経路制御)を書いている。https://www.ipa.go.jp/files/000024536.pdf 総務省・JPCERT/CC の該当一次資料は特定できず(未確認)。

### 5.4 小規模運用者の形(Debian 一台、Caddy / PostgreSQL / PocketBase / FastAPI)

- 層 1 ホスト全体:nftables の output チェーンを policy drop。established/related、loopback、DNS(固定した上流の 53/853)、NTP(123/udp)、許可宛先のセットを足す。プロセス単位は `meta skuid`(ユーザ)か `socket cgroupv2 … "system.slice/xxx.service"`。nft のホスト名は起動時に解決され動的に追従しない。https://wiki.debian.org/nftables
- 層 2 サービス単位:systemd の `IPAddressDeny=any` を上位 slice に、各 service に `IPAddressAllow=`(man の推奨そのもの)。IP/CIDR のみ。postgresql → `IPAddressAllow=localhost`。pocketbase/FastAPI → localhost と、アプリが叩く API の IP。caddy → ACME の宛先。https://man7.org/linux/man-pages/man5/systemd.resource-control.5.html
- 壊れるもの:apt(deb.debian.org は Fastly、IP 固定不可 → apt プロキシを一台に置くか `Acquire::http::Proxy`)、ACME(Let's Encrypt は検証元 IP を公開しない → 送信は宛先ドメインで許すか DNS-01)、OCSP(Let's Encrypt は 2025-08 に停止、CRL へ。Caddy の OCSP 向け外向きは LE では不要に)、NTP(pool は毎時変わる → 123/udp はドメイン非依存で開けるか固定 NTP)、GitHub(IP 許可を推奨しない → プロキシでドメイン許可)、webhook 送信(CDN 宛は IP が動く → 送信プロキシ経由)。
- DNS の固定:resolved か unbound で上流を固定し、53/853 の宛先を限定。DoH で他へ抜ける経路は 443 を宛先限定にしていれば塞がる。

### 5.5 正直な限界

1. IP の許可リストは CDN 時代に合わない。実用はドメイン(SNI)許可 + 送信プロキシ。nftables/systemd 単体は IP しか見ない。
2. SNI も消えつつある(RFC 9849 ECH、2026-03)。実測では ECH 展開の 99.99% が Cloudflare、Firefox 利用者の約 5 人に 1 人が毎日 ECH を使う。ただしサーバ側のクライアント(curl、Python、Go)は既定で ECH を使わないので、**サーバの送信制御では SNI はまだ使える**。
3. 許された宛先が武器になる:GitHub(Shai-Hulud)、Azure Blob(Interlock)、Graph API(Webworm)、Cloudflare Workers(BRICKSTORM)、Telegram。残るのは、宛先の粒度を下げる(自組織の org だけ)、送信量と頻度の監視、持ち出す鍵をそもそも置かない(短命トークン、最小権限)。
4. inbound の応答で出ていくものは止まらない(ToolShell の鍵窃取、Web シェルの応答、SSRF)。
5. DLP は暗号化経路に効かない。復号プロキシは小規模には重い。
6. 公的指針に温度差:NIST 800-41 と CISA 2024 は既定拒否を明記、NIST 800-207 と NISC 統一基準は「監視」止まり、Essential Eight は対象外。「国の基準が求めている」とは書けない。

---

## 第 6 部 冷静な結論

**仮説 1(委託先の特権)**
- 日本の 2025〜26 年の大型事例では当たっている。アスクル(委託先向け管理者アカウント、MFA の例外)、東海ソフト開発(保守口+管理者アカウント)、YCC(機器の管理者アカウント、弱いパスワード)、国会図書館(再委託先)。世界でも M&S(委託先ヘルプデスク)、MSP の RMM 二件、第三者アプリの常設トークン(Drift、Gainsight)。
- ただし件数で首位なのは境界機器(VPN・FW・公開サーバ)のゼロデイ(M-Trends 32%、DBIR 31%、警察庁 VPN 5〜6 割)。二つは排他ではなく、**委託先用の常時リモート口 + MFA の例外 + 共有/推測できるパスワード**という形で重なる。
- 大事件の共通点は「入られたこと」より「入った後、全体の管理者権限まで一本道で行けること」。委託先のアカウントは最初から管理者で、入口と root の距離がゼロ。
- 言い切ってはいけないこと:「委託先経由が主因」(統計が無い)。言えること:「委託先に常時の特権を渡す設計は、2025〜26 年の日本の大型事件の入口として繰り返し現れ、公的指針(CISA AA22-131A、NCSC、IPA)はいずれも常時・共有の特権をやめよと書いている」。

**仮説 2(外向き HTTPS)**
- 方向は正しい。言い方は「443 を塞ぐ」ではなく「外向きも既定拒否、宛先を名指しで許す」。NIST 800-41 の原文がそのまま根拠になる。
- 効く範囲:独自 C2、Rclone→攻撃者サーバ、Telegram、Discord、トンネル(7844)、未知のドメインへのツール取得。効かない範囲:許された宛先(GitHub、Azure、Graph、Cloudflare)への持ち出し、inbound の応答で出る鍵、暗号化経路の中身。
- 小規模運用で現実的なのは、nftables の既定拒否 + systemd の `IPAddressAllow` + 送信プロキシでのドメイン許可、の三層。壊れる物(apt、ACME、NTP、GitHub、webhook)は一つずつ経路を決めれば済む。

**連載で直す候補**(発注者が決める)
- サーバー編 第 5 章 第二節:`ufw default allow outgoing` → 外向きも既定拒否。考え方(「デフォルトはすべて拒否」)と手順を一致させる。許可一覧(apt、ACME、NTP、DNS、アプリの API)の作り方と、壊れる物の対処、「Claude に聞いてみよう②」に外向きの設計を足す。
- サーバー編 第 8 章(systemd の砂場):`IPAddressDeny=any` / `IPAddressAllow=` をサービスごとに。
- 2-02(AI に PC を一台渡す):AI にも委託先と同じ規律 ── その一台の外向きを名指しで許す、他の機械と鍵には届かせない。
- 2-05(門番):委託先・外部の人に常時の管理者権限を渡さない、期限付き、記録、共有アカウント禁止(CISA AA22-131A)。
- 3-03(安全設計):「守りの製品が入口になる」(CrowdStrike、F5、Cisco、Citrix、SharePoint)の一段。
- 3-04(委託の不経済):有事に委託は回らない、守りの特需は守れない(別メモの議論)。
- 新章(構造分析):「守りは買えない」── 本メモの事実の上に、需要・資金の二本と並べて。

**取り直すべき数字**:DBIR 2026 の第三者関与 48%(一次 PDF)、M-Trends のクラウド別内訳、ACSC の戦略ランク、NSA の二文書、IPA 2014 年版ガイドの原文。
