# [後日執筆] blog 024 草稿：2026年4月、Windows は「Microsoftが承認したコードしか動かないOS」になった

このファイルは将来のブログ記事 024（仮）の作業用草稿。
最終的に `articles/blog/024-windows-kernel-signing/ja.md`（仮）として公開する想定。

> **執筆の前提**：本草稿は 023 (`microsoft-power-and-environment`) の姉妹篇。
> 023 が「ハードウェアの線引き（TPM 2.0 / CPU 世代 / 5年サポート）による物理的なエンクロージャ」を扱ったのに対し、
> 024 は「**カーネルへの信頼の線引き**による論理的なエンクロージャ」を扱う。
> 二つを合わせて、Microsoft が物理層とソフトウェア層の両方で同時に囲い込みを進めている、という構造が見える。

---

## メタ情報（公開時に frontmatter にする）

- **slug 候補**：
  - `windows-kernel-signing`
  - `windows-no-longer-free`
  - `microsoft-zero-trust-sovereignty`
- **タイトル候補**：
  - 「2026年4月、Windows は『Microsoft が承認したコードしか動かない OS』になった」
  - 「Windows がもう自由に使える OS ではなくなった日」
  - 「Microsoft のゼロトラスト、Linux のゼロトラスト ── 主権はどこに置かれるか」
- **subtitle 候補**：
  - 「同じ『ゼロトラスト』でも、信頼の起点を Microsoft に置く設計と、自分に置ける設計の差」
  - 「BYOVD は本物の脅威。だが処方箋の選び方は別の問題である」
- **category**: 構造分析ノート / Structural Analysis Notes
- **label**: Blog
- **lang**: ja / en（両言語で書く）
- **date**: 2026.06.xx（執筆時に確定）
- **hero_image**: 未定（鍵 / カーネルリング / 署名証明書のイメージなど。または無指定でデフォルト）

---

## 一次資料（確認済み）

### Microsoft 公式
- [Advancing Windows driver security: Removing trust for the cross-signed driver program — TechCommunity (Windows IT Pro Blog)](https://techcommunity.microsoft.com/blog/windows-itpro-blog/advancing-windows-driver-security-removing-trust-for-the-cross-signed-driver-pro/4504818) ← 最重要・直接引用元
- [The Windows Driver Policy — Microsoft Support](https://support.microsoft.com/en-us/windows/the-windows-driver-policy-ecd2a78c-750c-415d-93f2-e37302ce0443)
- [Custom kernel signers for App Control for Business — Microsoft Learn](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/custom-kernel-signers)

### 二次資料（業界報道・確認用）
- [Microsoft cracks down on old Windows kernel drivers — The Register (2026/03/27)](https://www.theregister.com/2026/03/27/microsoft_kernel_trust/)
- [A critical Windows security fix puts legacy hardware on borrowed time — Computerworld](https://www.computerworld.com/article/4151390/a-critical-windows-security-fix-puts-legacy-hardware-on-borrowed-time.html)
- [Microsoft is changing a Windows kernel policy that's been around for decades — Neowin](https://www.neowin.net/news/microsoft-is-changing-a-windows-kernel-policy-thats-been-around-for-decades/)
- [BYOVD in 2026: the signed-driver loophole powering EDR bypass at scale — Threat Intel Report (2026/02/21)](https://www.threatintelreport.com/2026/02/21/articles/byovd-in-2026-the-signed-driver-loophole-powering-edr-bypass-at-scale/)

### 確認できた事実（執筆時にそのまま使える）
- **施行**：2026年4月の Windows update（セキュリティアップデート / サービシングリリース）
- **対象 OS**：Windows 11 24H2, 25H2, 26H1 と Windows Server 2025
- **何が変わるか**：cross-signed root program で署名されたカーネルドライバーへのデフォルト信頼を撤回。今後デフォルトで読み込まれるのは WHCP（Windows Hardware Compatibility Program）を通って Microsoft が直接署名したドライバーのみ
- **段階移行**：
  - Evaluation mode（評価モード）から開始。カーネルが driver load を監査するが、ブロックはしない
  - 移行条件：Windows クライアントで 100時間のアクティブ使用 + 3回の再起動サイクル（Server は 2回）をポリシー違反なく通過したら enforcement mode へ自動移行
  - cross-signed driver が evaluation 中もロードされ続けている限り、evaluation mode に留まる（イベント ID 3076 で記録）
- **抜け道**：
  - Microsoft が allow-list を維持（広く使われている reputable な cross-signed driver は一定期間信頼継続）
  - Application Control for Business（旧 WDAC）で企業 IT 管理者は個別ドライバーを許可可能（custom kernel signers の登録も可能）
- **Microsoft の表向きの動機**：BYOVD (Bring Your Own Vulnerable Driver) 攻撃の遮断
  - LOLDrivers カタログの 81.7% (1,983件中 1,620件) がクロス署名プログラムのサードパーティ CA 署名（VeriSign/Symantec 1,045件、GlobalSign 412件、DigiCert 287件など）
  - 実例：Scattered Spider が「POORTRY」をロードして 2023年のカジノインフラ攻撃、BlackByte が RTCore64.sys (MSI Afterburner) で HVCI バイパス、Lazarus が appid.sys ゼロデイ (CVE-2024-21338) で FudModule ルートキット
- **歴史**：クロス署名プログラムは2000年代初頭〜、2021年に非推奨、証明書は既に失効、だが互換性のため信頼継続だった

---

## 重要：書いてはいけない論点（Gemini の Deep Research で検証済み）

執筆前に必ず確認。**以下を主張するとファクトチェックで論破される**。

1. ❌「Windows は KMDF だけでドライバー全部をカーネル空間で動かしている」
   → UMDF (User-Mode Driver Framework) v2 を 2014年から提供。プリンタ・USB 等は既にユーザー空間ドライバー可能
2. ❌「Linux はドライバーをユーザー空間で分離している（マイクロカーネル的）」
   → Linux はモノリシックカーネル。ドライバー（カーネルモジュール）は Ring 0 で動作。カーネルパニックは BSOD と同質
3. ❌「eBPF をコアに据えてドライバーを置き換えられる」
   → eBPF ベリファイアはメモリ書き込み・無限ループ・DMA・割り込み処理を禁止。原理的にデバイスドライバーになれない。Microsoft 自身も ebpf-for-windows (2021〜MIT ライセンス) で eBPF 統合を進めている
4. ❌「Microsoft が4月に強行した怠惰な規制」
   → 評価モード (100時間 + 3再起動 + 違反でリセット) で段階移行。技術的設計としては慎重
5. ❌「BYOVD は誇張」
   → ランサムウェア・APT の実例が多数。LOLDrivers 81.7% がクロス署名

これらは「Microsoft の対応は技術的には合理的である」と認めた上で論を組まないと、blog が信用を失う。

---

## 構成案（章立て）

### 導入：2026年4月、何が変わったのか

- 4月の Windows update で、cross-signed kernel driver はデフォルトで信頼されなくなった
- 評価モードを経て、強制モードへ自動移行する設計
- 「ソフトウェアレベルで OS が囲い込まれた」最初の月

> **書き方の注意**: 段階移行の丁寧さは認めつつ、最終的な到達点は変わらないことを明示する。「ゆっくり進む変化は変化ではない」というニュアンスを避け、「**到達点が何か**を見る」というスタンスで書く。

### 第1節：BYOVD は本物の脅威である ── まず認めるところから

- BYOVD 攻撃の仕組み（Ring 3 → Ring 0、EDR 無効化）
- 実例：Scattered Spider (POORTRY)、BlackByte (RTCore64.sys + HVCI バイパス)、Lazarus (appid.sys / CVE-2024-21338)
- LOLDrivers 統計（81.7% がクロス署名）
- 「Microsoft が放置していた信頼のギャップ」が実際に攻撃に使われている

> **書き方の注意**: ここを軽視するとブログ全体が技術的に脆くなる。先に脅威の現実を認めた上で、その次の節で「処方箋の選び方」を問題化する。

### 第2節：処方箋の選び方が問われている

- 同じ「BYOVD を遮断する」という目標でも、実装の選び方は一つではない:
  - (A) **中央集権モデル**：Microsoft が WHCP で全てを審査し、allow-list を独占管理（Microsoft の選択）
  - (B) **オーナーシップモデル**：ユーザーが自分の信頼の起点を選択できる（Linux の選択）
  - (C) **コミュニティモデル**：分散検証 + 透明な配布 + 自動 CI/CD（部分的に Linux のエコシステムが体現、ただし純粋にはどこにも存在しない）
- Microsoft は (A) を選んだ。これは技術的に正しい/間違いという話ではなく、**主権をどこに置くかという設計判断**
- WHCP の通過判定も、allow-list の選定も、App Control for Business の運用範囲も、すべて Microsoft が単独で握る

### 第3節：「ゼロトラスト」の二つの実装 ── Linux との違いは「マイクロカーネル」ではなく「ガバナンス」

- ゼロトラストには必ず「**信頼の起点 (root of trust)**」が要る
- Windows の信頼の起点 = Microsoft
  - WHCP 認証 = Microsoft の審査
  - allow-list = Microsoft の選定
  - Test Signing / App Control = Microsoft が認めた範囲内での例外
  - BIOS で Secure Boot は無効化できるが、これは「OS 外への退避」
- Linux の信頼の起点 = ユーザー本人（あるいは選んだディストリビューション）
  - Secure Boot を BIOS で無効化できる
  - **MOK (Machine Owner Key) で自分の鍵を登録してモジュール署名できる**
  - **カーネル自体をソースからビルドできる**
  - ディストリビューション間で実装方針が違う（Debian、Arch、Fedora、Ubuntu 等が独立した判断）
- アーキテクチャが似てきても（どちらもゼロトラスト方向）、**主権の所在が違う**
- これは「Linux はマイクロカーネルだから安全」という技術論ではなく、「Linux はガバナンスが分散している」という統治論

> **書き方の注意**: Gemini が「Linux も Secure Boot で収斂しつつある」と書いたことへの正面からの反論にあたる箇所。技術収斂と主権収斂は別物。

### 第4節：023 との接続 ── 物理層 + 論理層、二重の囲い込み

- 023 でみた線引き：TPM 2.0、CPU 8世代以降、Windows 10 サポート終了、Copilot+ PC の 40 TOPS NPU 要件
  - = **ハードウェアの線引き**で古い PC を切り捨てる
- 024 でみる線引き：cross-signed driver のデフォルト信頼撤回、WHCP 経由のみ許可、allow-list は Microsoft 単独管理
  - = **ソフトウェアの線引き**で古いドライバー（≒ 古い周辺機器）を切り捨てる
- 二つは同じスケジュール、同じ方向で進んでいる
- 「中世の囲い込み」のメタファーを 023 から引き継ぐ：
  - 物理層 = 共有地を物理的に柵で囲った
  - 論理層 = 共有地への入り口に「領主の許可状」を求めるようになった
- どちらも個別に見れば技術的・経営的に合理化できる。だが**重ねて見ると、これは方向の一致である**

### 第5節：自己責任で残せる自由はどこまでか（Gemini に追加調査依頼予定）

> **TODO**: Gemini で「ユーザーが自己責任で古いドライバーを使う方法」を調査済。結果が出たら以下のリストを実値で埋める。

予想される選択肢（執筆時に詳細・手順を追記）:
1. **Secure Boot を BIOS で無効化** + Test Signing Mode を有効化（`bcdedit /set testsigning on`）
   - リスク：HVCI、Credential Guard など多くのセキュリティ機能が無効化される
2. **Application Control for Business で個別ドライバーを許可**
   - 企業向け、個人ユーザーには手順が複雑
3. **古いドライバー署名を個別にインポート / Custom Kernel Signers の登録**
   - 難易度高、再起動必須
4. **Microsoft Intune / WDAC ポリシーを使った企業向け運用**
   - 個人ユーザーには非現実的

> **書き方の注意**: 各選択肢について「**ただしいずれも Microsoft の建付けに従う形でしか実行できない**」点を明示する。
> 「自由は残っている」のではなく、「Microsoft が認めた形での『自由風の例外』が残っている」のだという構造を見せる。

### 第6節（結論）：Windows は「自由に使える OS」ではなくなった

- 「自由に使える」の定義を二つに分ける:
  - (a) アプリを起動して仕事ができる ── これは依然として可能
  - (b) **OS の心臓部で何を信頼するかを、ユーザー自身が決められる** ── ここが 2026年4月で失われた
- 023 と 024 が一緒に示しているのは、Microsoft が (b) の自由を**ハードウェア層 + ソフトウェア層の両方で同時に閉じてきた**ということ
- 「BYOVD があるから仕方ない」ではない。BYOVD への対処は他の設計でもできた。Microsoft はその中で**自社が信頼の起点になる設計**を選んだ
- Linux（Debian）に移れば、(b) の自由は失われない。これは「Linux のカーネルが安全だから」ではなく、「**ガバナンスが分散していて、信頼の起点を自分で持てるから**」
- 結語：「アプリが動く OS」を求めるなら Windows でいい。「**自分が信頼の起点である OS**」を求めるなら、Linux しかない

---

## 関連記事（公開時に末尾に置く）

- *関連: [Microsoftが引き起こす電力問題と環境問題](/blog/microsoft-power-and-environment/)*（023, 物理層の囲い込み）
- *関連: [PCが大幅値上げ ── 今あるPCにLinuxをインストールして活用](/blog/windows-10-to-debian/)*（022, 出口戦略）
- *関連: [Windowsはこわれていく](/blog/windows-breaking-down/)*（017）
- *関連: [本当に Windows・Office を使い続けますか？](/blog/windows-office-facts/)*（014）

---

## 残タスク

- [ ] Gemini に「自己責任で古いドライバーを使う方法」を確認、第5節を実値で埋める
- [ ] Microsoft 公式 TechCommunity ブログから直接引用（できれば英語原文 + 訳）を1〜2本入れる
- [ ] David Weston など Microsoft セキュリティ部門の発言があれば探す
- [ ] hero_image を決める（または無指定で進む）
- [ ] 英語版（en.md）を起こす
- [ ] 公開時に slug / タイトル / 日付を確定

---

## 編集上の注意（執筆時に守ること）

- **予測は書かない**（aiseed.dev の編集方針）。「今後 Microsoft はこうするだろう」式の推測は避け、現時点で確認できる事実と構造の指摘に留める
- BYOVD の技術的記述は一次資料（Microsoft TechCommunity blog、LOLDrivers）で裏取りした表現のみ使う
- Linux の優位を語るとき、**マイクロカーネル神話には踏み込まない**（Linux はモノリシック）。代わりに「**ガバナンスの分散**」を軸にする
- 「Microsoft が怠慢」「Microsoft の傲慢」といった人格化した強い言葉は使わず、**設計判断の結果として何が起きるか**を構造で書く
- Gemini Deep Research は Microsoft の技術判断を肯定的に評価している。これに**正面から反論せず、論点をずらす**（技術の合理性は認め、主権の所在を問う）
