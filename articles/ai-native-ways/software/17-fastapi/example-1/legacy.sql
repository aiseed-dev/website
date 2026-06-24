-- 「既存業務システム」の PL/SQL 風ロジック (実際は SQLite で動かす)
-- 注文に対して送料・割引・税を計算する。
-- 業務担当者の頭の中だけにあった暗黙ルールが、コードに埋まっている。

CREATE TABLE orders (
  id          INTEGER PRIMARY KEY,
  customer    TEXT,
  region      TEXT,
  qty         INTEGER,
  unit_price  INTEGER,
  is_member   INTEGER  -- 0=ゲスト, 1=会員
);

INSERT INTO orders (id, customer, region, qty, unit_price, is_member) VALUES
  (1, '山田農園', '東京', 5,  2400, 1),
  (2, '鈴木商店', '北海道', 12, 1800, 0),
  (3, '高橋食品', '沖縄', 3,  3600, 0),
  (4, '佐藤畜産', '大阪', 8,  1500, 1),
  (5, '田中株式会社', '東京', 1, 12000, 0),
  (6, '渡辺青果', '北海道', 25, 800, 1),
  (7, '中村製作所', '東京', 4,  4500, 0),
  (8, '小林技研', '九州', 6,  2200, 1),
  (9, '斎藤運輸', '東京', 18, 950, 1),
  (10, '加藤建設', '沖縄', 2, 7800, 0);

-- ビジネスロジック: 注文ごとの請求額を出す
-- ルール(現場担当者の頭にあった暗黙のもの):
--   1. 小計 = qty * unit_price
--   2. 送料: 北海道・沖縄は 1,500 円、それ以外は 800 円。10,000 円以上なら無料
--   3. 会員割引: is_member=1 なら小計の 5% を引く
--   4. 大口割引: 小計が 30,000 円以上なら追加 3% を引く(会員割引の後)
--   5. 消費税: (小計 - 割引 + 送料) * 10%(切り捨て)
--   6. 最終請求 = 小計 - 割引 + 送料 + 税

CREATE VIEW invoices AS
SELECT
  id,
  customer,
  region,
  qty,
  unit_price,
  is_member,
  -- 小計
  (qty * unit_price) AS subtotal,
  -- 送料
  CASE
    WHEN (qty * unit_price) >= 10000 THEN 0
    WHEN region IN ('北海道','沖縄') THEN 1500
    ELSE 800
  END AS shipping,
  -- 会員割引
  CASE WHEN is_member = 1 THEN CAST((qty * unit_price) * 0.05 AS INTEGER) ELSE 0 END AS member_discount,
  -- 大口割引(会員割引適用後の小計に対して 3%)
  CASE
    WHEN (qty * unit_price - CASE WHEN is_member=1 THEN CAST((qty*unit_price)*0.05 AS INTEGER) ELSE 0 END) >= 30000
      THEN CAST((qty * unit_price - CASE WHEN is_member=1 THEN CAST((qty*unit_price)*0.05 AS INTEGER) ELSE 0 END) * 0.03 AS INTEGER)
    ELSE 0
  END AS bulk_discount,
  -- ここで税前小計
  (
    qty * unit_price
    - CASE WHEN is_member=1 THEN CAST((qty*unit_price)*0.05 AS INTEGER) ELSE 0 END
    - CASE
        WHEN (qty * unit_price - CASE WHEN is_member=1 THEN CAST((qty*unit_price)*0.05 AS INTEGER) ELSE 0 END) >= 30000
          THEN CAST((qty * unit_price - CASE WHEN is_member=1 THEN CAST((qty*unit_price)*0.05 AS INTEGER) ELSE 0 END) * 0.03 AS INTEGER)
        ELSE 0
      END
    + CASE
        WHEN (qty * unit_price) >= 10000 THEN 0
        WHEN region IN ('北海道','沖縄') THEN 1500
        ELSE 800
      END
  ) AS pretax_total
FROM orders;

-- 出力: id, customer, subtotal, shipping, member_discount, bulk_discount,
--      tax (= pretax_total * 10%, 切り捨て), final_total
.headers on
.mode csv
.output legacy_output.csv

SELECT
  id,
  customer,
  subtotal,
  shipping,
  member_discount,
  bulk_discount,
  CAST(pretax_total * 0.10 AS INTEGER) AS tax,
  pretax_total + CAST(pretax_total * 0.10 AS INTEGER) AS final_total
FROM invoices
ORDER BY id;
