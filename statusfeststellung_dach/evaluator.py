# -*- coding: utf-8 -*-
"""
Bewertungsalgorithmus zur Scheinselbstständigkeit nach § 7a SGB IV, ASVG und AHVG.
"""

from typing import Dict, Any, List
from .models import StatusClassification, CriteriaEvaluation, Country


def evaluate_status(
    has_own_capital_risk: bool,
    determines_own_working_hours: bool,
    determines_own_location: bool,
    uses_own_equipment: bool,
    has_own_website_marketing: bool,
    has_multiple_clients: bool,
    revenue_share_single_client_pct: float,  # e.g. 85.0 for 85%
    integrated_in_team_hierarchy: bool,
    wears_client_uniform_or_email: bool,
    needs_approval_for_absence: bool,
    has_own_employees: bool,
    annual_fee_volume_eur: float = 60000.0,
    years_under_audit: int = 1,
    country: Country = Country.DE,
) -> CriteriaEvaluation:
    """
    Berechnet den Risiko-Score für Scheinselbstständigkeit (0 bis 100).
    Höhere Werte bedeuten akutes Risiko einer abhängigen Beschäftigung.
    """
    score = 0.0
    positives: List[str] = []
    risks: List[str] = []

    # 1. Unternehmerisches Risiko (bis zu 20 Pkt)
    if has_own_capital_risk:
        positives.append("Eigenes unternehmerisches Kapitalrisiko vorhanden (Gewinn- & Verlustchance)")
    else:
        score += 15.0
        risks.append("Kein nennenswertes eigenes Kapital- oder Verlustrisiko erkennbar")

    if uses_own_equipment:
        positives.append("Einsatz eigener Betriebsmittel, Hard- und Software")
    else:
        score += 10.0
        risks.append("Nutzung von Betriebsmitteln des Auftraggebers (Laptop, Werkzeuge, Lizenzen)")

    # 2. Weisungsgebundenheit & Autonomie (bis zu 25 Pkt)
    if determines_own_working_hours:
        positives.append("Freie Bestimmung der Arbeitszeit und Arbeitsorganisation")
    else:
        score += 12.0
        risks.append("Feste Arbeitszeiten oder Kernarbeitszeit durch Auftraggeber vorgegeben")

    if determines_own_location:
        positives.append("Freie Wahl des Arbeitsorts (eigenes Büro / Homeoffice)")
    else:
        score += 10.0
        risks.append("Verpflichtender Einsatz in den Räumlichkeiten des Auftraggebers")

    if needs_approval_for_absence:
        score += 15.0
        risks.append("Urlaubs- oder Abwesenheitsanträge müssen vom Auftraggeber genehmigt werden (§ 84 HGB verletzt)")
    else:
        positives.append("Keine Urlaubsabstimmung oder Genehmigungspflicht bei Abwesenheit")

    # 3. Eingliederung in fremde Organisation (bis zu 20 Pkt)
    if integrated_in_team_hierarchy:
        score += 15.0
        risks.append("Eingliederung in die Team-Hierarchie, Organigramm oder Schichtpläne")
    else:
        positives.append("Autonome Position außerhalb der innerbetrieblichen Aufbauorganisation")

    if wears_client_uniform_or_email:
        score += 8.0
        risks.append("Verwendung firmeninterner E-Mail-Adresse oder Dienstkleidung ohne Freelancer-Kennzeichnung")

    # 4. Marktauftritt & Kundenstruktur (bis zu 25 Pkt)
    if has_own_website_marketing:
        positives.append("Eigener Marktauftritt am freien Markt (Website, Rechnungsbriefkopf, Visitenkarten)")
    else:
        score += 8.0
        risks.append("Kein werbender Auftritt am freien Markt vorhanden")

    if has_own_employees:
        score -= 20.0  # Sehr starkes Entlastungsmerkmal nach § 2 Satz 1 Nr. 9 SGB VI
        positives.append("Beschäftigung eigener sozialversicherungspflichtiger Mitarbeiter (starkes Kriterium für Selbstständigkeit)")

    if revenue_share_single_client_pct >= 83.33:  # 5/6 Grenze nach § 2 Satz 1 Nr. 9 SGB VI
        score += 20.0
        risks.append(f"Umsatzanteil eines einzelnen Auftraggebers beträgt {revenue_share_single_client_pct:.1f} % (übersteigt 5/6 Grenze)")
    elif revenue_share_single_client_pct >= 60.0:
        score += 8.0
        risks.append(f"Wirtschaftliche Abhängigkeit: {revenue_share_single_client_pct:.1f} % Umsatzanteil von einem Kunden")
    else:
        positives.append("Ausgewogene Kundenstruktur mit weniger als 60 % Umsatz bei einem Einzelkunden")

    # Clamping 0 bis 100
    final_score = max(0.0, min(100.0, round(score, 1)))

    if final_score < 30.0:
        classification = StatusClassification.CLEARLY_INDEPENDENT
        recommendation = "Geringes Risiko. Die Selbstständigkeit ist durch unternehmerische Kriterien gut belegbar."
    elif final_score <= 60.0:
        classification = StatusClassification.BORDERLINE_RISK
        recommendation = "Grauzone / Erhöhtes Risiko. Es wird dringend empfohlen, Verträge nachzuschärfen oder ein Statusfeststellungsverfahren nach § 7a SGB IV zu beantragen."
    else:
        classification = StatusClassification.CLEARLY_DEPENDENT
        recommendation = "Akute Scheinselbstständigkeit droht. Wesentliche Merkmale einer abhängigen Beschäftigung überwiegen. Sofortiger Handlungsbedarf zur Vermeidung von Nachzahlungen!"

    # Nachzahlungssimulation für Auftraggeber:
    # ca. 40 % Gesamtsozialversicherungsbeiträge (AG + AN Anteil)
    # Säumniszuschläge nach § 24 SGB IV: 1 % pro Monat (12 % p.a.)
    total_fees = annual_fee_volume_eur * years_under_audit
    sv_rate = 0.40  # 40% SV
    estimated_sv_backpay = round(total_fees * sv_rate, 2)
    estimated_late_surcharges = round(estimated_sv_backpay * 0.12 * (years_under_audit / 2.0), 2)
    total_financial_risk = round(estimated_sv_backpay + estimated_late_surcharges, 2)

    backpay_simulation = {
        "audited_years": years_under_audit,
        "total_fee_volume_eur": round(total_fees, 2),
        "estimated_sv_backpay_eur": estimated_sv_backpay,
        "estimated_late_surcharges_eur": estimated_late_surcharges,
        "total_financial_risk_eur": total_financial_risk,
    }

    return CriteriaEvaluation(
        score=final_score,
        classification=classification,
        positive_indicators=positives,
        risk_indicators=risks,
        backpay_simulation=backpay_simulation,
        recommendation=recommendation,
    )
