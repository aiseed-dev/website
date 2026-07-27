# Windows の現状まとめ ── ユーザーの反発と品質問題(2026年7月時点)

**作成の経緯**: r/FuckMicrosoft の最新投稿の要約を依頼されたが、本作業環境からは
Reddit へのアクセスが全経路(直接・ミラー・リーダープロキシ)でブロックされており、
投稿そのものは取得できなかった。代替として、同コミュニティで話題になっている
種類の事象を、報道・フォーラムの検索結果から収集して整理した。**Reddit の
生の投稿の要約ではない**ことに注意。生の投稿を反映したい場合は、投稿本文を
貼り付けてもらえれば追記する。

**一言でいうと**: 2026年上半期の Windows は「AI の押し付けへの反発」と
「基本品質の崩れ」が同時進行し、Microsoft 自身が路線後退(AI 縮小と品質回帰の
公式表明)に追い込まれた半年だった。ただしユーザー側は後退を「看板の掛け替え」と
見ており、反発は収まっていない。

---

## 1. Copilot 押し付けへの反発と、Microsoft の後退

- コミュニティの反発は「**Microslop**」という蔑称が定着するほどに達し、
  Microsoft が公式 Discord サーバーでこの語を禁止する事態になった
- 2026年3月20日、Windows 責任者 Pavan Davuluri が「**Windows の品質への
  コミットメント**」と題する公式ブログを公表 ── 混乱の少ない更新と、
  「不要な Copilot 導線の削減」(Snipping Tool、フォト、ウィジェット、
  メモ帳から着手)を約束([Windows Latest 2026-05-07](https://www.windowslatest.com/2026/05/07/windows-11-pulls-back-ai-as-microsoft-plans-to-remove-copilot-where-it-doesnt-meet-its-promise/)、
  [Tom's Guide](https://www.tomsguide.com/computing/windows-operating-systems/microsoft-is-reportedly-pulling-back-on-stuffing-windows-11-with-ai-and-i-couldnt-be-happier))
- 一方で、**2026年6月から法人向け Windows 11 端末に Microsoft 365 Copilot
  アプリを自動配備**する計画を再開 ── 一度反発で停止したロールアウトの再点火
  ([Windows News](https://windowsnews.ai/article/microsoft-to-force-install-copilot-app-on-windows-11-business-pcs-by-june-2026-heres-how-to-block-it.431803))
- ユーザーの受け止めは冷ややか:「**結局 Copilot は残る。見えなくしただけ**」
  「削除ではなくブランド変更で反発を減らす作戦」
  ([TechRadar](https://www.techradar.com/computing/windows/microsoft-has-begun-stripping-out-ai-from-windows-11-but-its-already-being-criticized-for-not-going-far-enough))
- 6月には一転して「Windows 11 を **AI を作るための OS** にする」と宣言
  ([Windows Latest 2026-06-03](https://www.windowslatest.com/2026/06/03/microsoft-pledges-to-make-windows-11-the-os-for-building-ai-after-years-of-copilot-backlash/))
  ── 縮小と拡大の方針が数ヶ月単位で揺れている

## 2. 基本品質の崩れ(2026年上半期の更新不具合)

- **1月の月例更新(2026-01-13)**: シャットダウン/休止で黒画面→勝手に再起動する
  リグレッション。Windows 11 と **Windows 10 ESU の両方**に波及
  ([Windows Forum](https://windowsforum.com/threads/windows-shutdown-bug-after-january-2026-updates-affects-windows-11-and-windows-10-esu.400673/))。
  ESU 更新 KB5073724 適用後に**起動4〜5分でフリーズ**する報告
  ([TenForums](https://www.tenforums.com/windows-updates-activation/222472-january-2026-esu-kb5073724-windows-freezes-after-4-5-minutes.html))
- **2月**: Windows 10 ESU KB5075912 でシャットダウンバグ修正
  ([Windows Latest](https://www.windowslatest.com/2026/02/11/windows-10-kb5075912-esu-out-with-shutdown-bug-fix-direct-download-links-for-offline-installer-cab/))
- **3月**: 特定 GPU 構成でスタートメニュー・タスクバーが停止する Windows 10 の
  安定性バグを修正([Windows Latest](https://www.windowslatest.com/2026/03/11/windows-10-kb5078885-out-with-a-gpu-fix-secure-boot-2023-direct-download-links-for-offline-installers-msu/))
- **5月**: Microsoft が **explorer.exe がタスクバー・サインイン・Task View に
  またがって不安定**だったことを認め修正
  ([Windows Latest](https://www.windowslatest.com/2026/05/22/microsoft-says-windows-11s-explorer-exe-has-been-unstable-across-taskbar-sign-in-and-task-view-rolls-out-fix/))
- **6月**: **遅いシャットダウンがバグだったことを認め**、タスクバーのアイコンが
  白紙になる不具合も修正
  ([Windows Latest](https://www.windowslatest.com/2026/06/26/microsoft-admits-windows-11s-slow-shutdown-is-a-bug-plus-blank-taskbar-icons-in-a-new-update/))
- パターン: **毎月の更新が別の基本機能を壊し、翌月それを認めて直す** サイクルが
  半年続いている。Davuluri の「品質コミットメント」はこの文脈で出た

## 3. Windows 10 の残留と ESU

- Windows 10 は 2025年10月14日にサポート終了。しかし **6割超のユーザーが
  Windows 11 への移行を拒否して Windows 10 に残留** という推計
  ([Windows News](https://windowsnews.ai/article/copilot-everywhere-microsofts-2026-ai-gamble-collides-with-windows-10-holdouts-and-office-backlash.428441))
- 残留の理由: ハードウェア要件(TPM 等)、レガシーアプリ互換、そして
  **AI の押し付けへの拒否感**
- ESU(拡張セキュリティ更新)は継続しているが、上記のとおり ESU 更新自体が
  不具合を持ち込む事例が発生 ── 「金を払って延命したのに壊される」という不満

## 4. 広告・プライバシー・アカウント強制

- Windows 11 の広告はスタートメニュー、ロック画面、設定アプリ、
  **File Explorer 内**にまで拡大。「おすすめ」の名で配信される
  ([XDA](https://www.xda-developers.com/disable-windows-11-ads-by-changing-these-settings/)、
  [Computerworld](https://www.computerworld.com/article/1616461/how-to-protect-your-privacy-in-windows-11.html))
- **File Explorer 内広告は、単なる不快さの問題ではなく、最高に危険な設計だ**。
  File Explorer は、ユーザーが「自分のファイル」を見る、OS が最も信頼されている
  面である。そこに **第三者由来のコンテンツを配信する経路を通した** ということは、
  その経路にマルウェアを載せられる、ということだ。表示するリンク先、勧める
  ダウンロード、差し込むバナー ── どれも「Microsoft の画面に出ている」という
  信頼を借りて、ユーザーの警戒を解く。**マルバタイジング(広告経由のマルウェア
  配布)を、OS が自らの最も信頼された面に招き入れた** ことになる。攻撃者から
  見れば、これほど質の高い配布面はない。そして広告経由で置かれるマルウェアの
  典型が、次節のインフォスティーラー ── つまり **File Explorer の広告枠と、
  第5節のパスワード窃取は、一本の線でつながっている**(広告面 → マルウェア →
  資格情報の窃取 → アカウント乗っ取り)。「収益のために信頼面を売る」という
  判断が、そのままセキュリティの穴になっている。
- **Recall**(画面の継続スクリーンショット+AI 検索)は反発を受けてオプトイン化・
  暗号化強化されたが、「入力したパスワード・読んだ私信・開いた文書が全部
  キャプチャされ得る」という基本設計への不信は残る
  ([Yahoo Tech](https://tech.yahoo.com/cybersecurity/articles/7-windows-11-features-silently-153020064.html))
- テレメトリ・広告 ID・Microsoft アカウント紐付けが既定で有効であり、
  「2026年版プライバシー防衛チェックリスト」の類が定番コンテンツ化している
  ([Windows Forum](https://windowsforum.com/threads/windows-11-2026-privacy-and-declutter-checklist-to-reclaim-control.399639/))
  ── **既定値との戦いがユーザーの日常になっている** こと自体が症状

## 5. アカウント乗っ取り・パスワード窃取(2026-07-05 追記)

「Microsoft アカウントのパスワードを盗まれた」という投稿は、Microsoft 公式の
Q&A フォーラム上に多数、継続的に上がっている。

**個人の被害報告(Microsoft Q&A、2026年)**:

- 2026年1月22日、Outlook アカウントが乗っ取られ連絡先リストを持ち出された
  ([Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5735720/my-outlook-account-was-hacked-on-1-22-2026))
- 2026年1月30日、無断でパスワードが変更され、回復用メールアドレスまで
  攻撃者のものに差し替えられた
  ([Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5820962/my-account-got-hacked-compromised))
- **所有権の証明を提出しても復旧できない** ── メールとパスワードとセキュリティ
  情報を全部変えられ、回復コードの受信先ごと失った、という訴え
  ([Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5860791/microsoft-account-hacked-email-changed-unable-to-r)、
  [同種の相談](https://learn.microsoft.com/en-us/answers/questions/5815530/microsoft-account-theft))

被害報告に共通するパターン: **パスワード変更 → 回復用メール・セキュリティ情報の
差し替え → 本人が回復手段ごと締め出される → 自動化された復旧プロセスが通らず、
人間のサポートには辿り着けない**。

窃取の入口の一つが、第4節で挙げた **信頼面に流し込まれる広告・おすすめ** だ。
File Explorer やスタートメニューの広告からインフォスティーラーが入り込めば、
端末に保存されたパスワード・Cookie・トークンがまとめて抜かれる。**広告面が
入口、パスワード窃取が出口** ── 別々の不満に見えて、同じ一本の経路である。

**規模の裏付け(2026年上半期)**:

- インフォスティーラー型マルウェアが **2025年の1年間で推定18億件の資格情報を
  窃取**([まとめ](https://shattered.io/infostealer-malware-1-8b-credentials/))。
  2026年6月、Microsoft と Europol が StealC / Amadey の摘発作戦を実施し、
  サーバー326台を停止、**約2,700万件の窃取済み資格情報を回収**
  ([Cybersecurity Dive](https://www.cybersecuritydive.com/news/microsoft-europol-international-takedown-infostealer-malware/823655/)、
  [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/06/24/stealc-and-amadey-breaking-down-infostealers-and-the-cybercrime-services-that-deliver-them/))
- 2026年6月12〜26日、Microsoft 365 アカウントに対して **8,100万回のログイン
  試行**(パスワードスプレー)を伴う攻撃で、64組織・78アカウントが侵害された。
  攻撃者は盗んだ資格情報に加え、条件付きアクセスの実装不備(ROPC OAuth)や、
  IT サポートを装って**セルフサービス・パスワードリセット(SSPR)を悪用**する
  ソーシャルエンジニアリングを使った
  ([TechRadar](https://www.techradar.com/pro/security/81-million-login-attempts-hit-microsoft-365-accounts-as-hackers-try-password-spraying-to-force-entry-using-stolen-credentials-and-oauth-to-bypass-authentication))
- Microsoft は 2026年Q1 もフィッシングで**最も偽装されたブランド**(全ブランド
  偽装の22%)([Forbes](https://www.forbes.com/sites/zakdoffman/2026/04/19/if-you-see-this-microsoft-login-your-account-is-being-hacked/))

**構造的な読み**: これは個々の不注意の問題ではない。一つのアカウントに
メール・ファイル・OS ログイン・購入履歴・回復手段のすべてが束ねられている
(= 鍵の集中)ため、**鍵一つの窃取が生活全体の乗っ取りになり、復旧の入口
までもが同じ鍵の内側にある**。ソフトウェア開発編 2-01 の「閉+他人の鍵」、
2-03 の「出るのも一点だ」の裏面(乗っ取られるのも一点)がそのまま当てはまる。
最も偽装されるブランドである時点で、アカウント集中設計そのものがフィッシングの
的を一点に絞らせている。

## 6. サイトの既存分析との対応

この状況は、本サイトの既存の構造分析がそのまま当てはまる:

- 取り込み(AI の内蔵化)が自己破壊を加速 → [構造分析 1-12「領主層の自己破壊」](/insights/lord-class-collapse/)
  (Recall = 融合スタック×AI の必然、の実証が続いている)
- 「AI は開発に使う。プロダクトの中には入れない」→ [1-05「Mythosが来た」](/insights/mythos/)
- 内蔵しないと価値が出ない構造と Entra ID → [3-04「クラウドからの自立」](/insights/cloud-independence/)、
  [ブログ029「アメリカのAI覇権の終わりの始まり」](/blog/end-of-us-ai-hegemony/)第3層
- デフォルト enable = 税の自動徴収 → [1-08「企業ITの税を引く」](/insights/enterprise-tax/)
- 出口: [ソフトウェア開発編 自立編](/ai-native-ways/software/)、[Claudeと一緒に学ぶDebian](/claude-debian/)

**記事化の種**: 「Microsoft 自身が後退を表明したのに、ユーザーは信じなかった」
── 信頼の非対称性(壊すのは一瞬、回復は年単位)は、ブログの好素材。
「毎月の更新が基本機能を壊す」は 1-11 の reliability/validity(出荷 KPI は
達成され続けている)の実例としても使える。

## 未確認・要注意

- 「Microslop」Discord 禁止と Windows 10 残留 6 割超は、windowsnews.ai という
  二次ソース経由。記事に使う場合は一次ソースの確認が必要
- Reddit の生の投稿(個々の体験談・温度感)は未取得 ── 必要なら投稿本文の
  貼り付けを受けて追記する
