def predict_risk(amount, frequency):
    risk_amount = 0.3 * (amount / 10000)
    risk_freq = 0.7 * (frequency / 10)

    total_risk = risk_amount + risk_freq
    total_risk = min(total_risk, 1.0)

    # Explanation logic
    reasons = []

    if amount > 7000:
        reasons.append("High transaction amount")

    if frequency > 7:
        reasons.append("High transaction frequency")

    if total_risk > 0.7:
        reasons.append("Unusual behavior pattern")

    return total_risk, reasons