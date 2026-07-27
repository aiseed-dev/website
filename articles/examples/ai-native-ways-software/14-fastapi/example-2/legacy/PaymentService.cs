// 既存 C# の決済処理(模擬)。

using System;

namespace Example.Payment
{
    public class PaymentService
    {
        // 決済成功率の判定: 過去 24 時間以内に 3 回以上失敗していると要確認
        private const int FAILURE_THRESHOLD = 3;
        private const int FAILURE_WINDOW_HOURS = 24;

        // 1 回の決済上限: 50 万円(これ以上は別途承認フロー)
        private static readonly decimal SINGLE_PAYMENT_LIMIT = 500_000m;

        // 月次累計上限: 500 万円(B2B 顧客のみ、それ以外は 100 万円)
        private static readonly decimal MONTHLY_LIMIT_B2B = 5_000_000m;
        private static readonly decimal MONTHLY_LIMIT_RETAIL = 1_000_000m;

        // 自動再試行の間隔(分)
        private const int RETRY_INTERVAL_MINUTES = 15;
        private const int MAX_RETRIES = 3;

        // 決済手数料: 3.6% + 30 円(クレジットカード)
        private const decimal FEE_RATE = 0.036m;
        private const decimal FEE_FIXED = 30m;

        public PaymentResult Process(PaymentRequest req)
        {
            // 上限チェック
            decimal monthlyLimit = req.IsBusinessCustomer ? MONTHLY_LIMIT_B2B : MONTHLY_LIMIT_RETAIL;
            if (req.Amount > SINGLE_PAYMENT_LIMIT)
            {
                return PaymentResult.RequiresApproval("単発上限超過");
            }
            if (req.MonthlyTotal + req.Amount > monthlyLimit)
            {
                return PaymentResult.RequiresApproval("月次上限超過");
            }

            // 失敗履歴チェック
            int recentFailures = req.GetRecentFailures(FAILURE_WINDOW_HOURS);
            if (recentFailures >= FAILURE_THRESHOLD)
            {
                return PaymentResult.RequiresVerification("失敗多数");
            }

            // 手数料計算
            decimal fee = req.Amount * FEE_RATE + FEE_FIXED;
            decimal netAmount = req.Amount - fee;

            // 実決済処理 ...
            return PaymentResult.Success(netAmount, fee);
        }
    }
}
