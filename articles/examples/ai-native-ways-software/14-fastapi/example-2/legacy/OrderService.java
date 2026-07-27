// 既存 Java の業務サービス(模擬)。
// このコードに、コメントや変数名・分岐の中に「業務ルール」が散らばっている。
// それを Python スクリプトで Markdown に抽出する。

package com.example.order;

import java.math.BigDecimal;
import java.time.LocalDate;

public class OrderService {

    // 送料は離島が高い ── 北海道・沖縄は 1500 円、それ以外 800 円
    private static final BigDecimal SHIPPING_REMOTE = new BigDecimal("1500");
    private static final BigDecimal SHIPPING_NORMAL = new BigDecimal("800");

    // 小計が 10,000 円以上で送料無料
    private static final BigDecimal SHIPPING_FREE_THRESHOLD = new BigDecimal("10000");

    // 会員割引: 5%
    private static final BigDecimal MEMBER_DISCOUNT_RATE = new BigDecimal("0.05");

    // 大口割引(会員割引適用後の小計が 30,000 円以上で 3% 引き)
    private static final BigDecimal BULK_DISCOUNT_THRESHOLD = new BigDecimal("30000");
    private static final BigDecimal BULK_DISCOUNT_RATE = new BigDecimal("0.03");

    // 消費税率(2026 年現在 10%)
    private static final BigDecimal TAX_RATE = new BigDecimal("0.10");

    /**
     * 注文の請求書を計算する。
     * 業務ルール:
     *   1. 小計 = 数量 × 単価
     *   2. 送料 (北海道・沖縄/その他、10000 円以上で無料)
     *   3. 会員割引 (5%, 切り捨て)
     *   4. 大口割引 (会員割引後 30000 円以上で 3%, 切り捨て)
     *   5. 消費税 = 税前合計 × 10% (切り捨て)
     */
    public Invoice calculate(Order order) {
        BigDecimal subtotal = order.getQty().multiply(order.getUnitPrice());

        // 送料
        BigDecimal shipping;
        if (subtotal.compareTo(SHIPPING_FREE_THRESHOLD) >= 0) {
            shipping = BigDecimal.ZERO;
        } else if ("北海道".equals(order.getRegion()) || "沖縄".equals(order.getRegion())) {
            shipping = SHIPPING_REMOTE;
        } else {
            shipping = SHIPPING_NORMAL;
        }

        // 会員割引
        BigDecimal memberDiscount = order.isMember()
            ? subtotal.multiply(MEMBER_DISCOUNT_RATE).setScale(0, BigDecimal.ROUND_DOWN)
            : BigDecimal.ZERO;

        // 大口割引(会員割引後の小計に対して)
        BigDecimal afterMember = subtotal.subtract(memberDiscount);
        BigDecimal bulkDiscount = afterMember.compareTo(BULK_DISCOUNT_THRESHOLD) >= 0
            ? afterMember.multiply(BULK_DISCOUNT_RATE).setScale(0, BigDecimal.ROUND_DOWN)
            : BigDecimal.ZERO;

        BigDecimal pretax = subtotal
            .subtract(memberDiscount)
            .subtract(bulkDiscount)
            .add(shipping);
        BigDecimal tax = pretax.multiply(TAX_RATE).setScale(0, BigDecimal.ROUND_DOWN);
        BigDecimal total = pretax.add(tax);

        return new Invoice(subtotal, shipping, memberDiscount, bulkDiscount, tax, total);
    }
}
