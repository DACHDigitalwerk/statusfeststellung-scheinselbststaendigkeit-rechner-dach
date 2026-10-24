# -*- coding: utf-8 -*-
"""
Kommandozeilen-Interface (CLI) für dach-statusfeststellung.
"""

import argparse
import json
import sys
from .evaluator import evaluate_status
from .models import Country


def main():
    parser = argparse.ArgumentParser(
        prog="dach-statusfeststellung",
        description="DACH Scheinselbstaendigkeit- & Statusfeststellungs-Pruefer 2026 (SGB IV, ASVG, AHVG)",
    )
    parser.add_argument("--capital-risk", action="store_true", help="Eigenes unternehmerisches Kapitalrisiko vorhanden")
    parser.add_argument("--own-hours", action="store_true", help="Freie Bestimmung der Arbeitszeit")
    parser.add_argument("--own-location", action="store_true", help="Freie Wahl des Arbeitsorts")
    parser.add_argument("--own-equipment", action="store_true", help="Einsatz eigener Betriebsmittel und Hardware")
    parser.add_argument("--own-marketing", action="store_true", help="Eigener Marktauftritt (Website, Logo, Briefkopf)")
    parser.add_argument("--single-client-pct", type=float, default=50.0, help="Umsatzanteil des groessten Auftraggebers in Prozent (z.B. 85 für 85 Prozent)")
    parser.add_argument("--integrated-hierarchy", action="store_true", help="Eingliederung in Team-Hierarchie oder Weisungen des Auftraggebers")
    parser.add_argument("--client-email", action="store_true", help="Nutzung von Kunden-Email oder Dienstkleidung")
    parser.add_argument("--absence-approval", action="store_true", help="Urlaubs- oder Abwesenheitsantraege muessen genehmigt werden")
    parser.add_argument("--own-employees", action="store_true", help="Beschaeftigung eigener sozialversicherungspflichtiger Mitarbeiter")
    parser.add_argument("--annual-fees", type=float, default=60000.0, help="Jaehrliches Honorarvolumen in EUR fuer Nachzahlungs-Simulation")
    parser.add_argument("--audit-years", type=int, default=1, help="Pruefzeitraum in Jahren fuer Nachzahlungssimulation")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")

    args = parser.parse_args()

    res = evaluate_status(
        has_own_capital_risk=args.capital_risk,
        determines_own_working_hours=args.own_hours,
        determines_own_location=args.own_location,
        uses_own_equipment=args.own_equipment,
        has_own_website_marketing=args.own_marketing,
        has_multiple_clients=(args.single_client_pct < 83.33),
        revenue_share_single_client_pct=args.single_client_pct,
        integrated_in_team_hierarchy=args.integrated_hierarchy,
        wears_client_uniform_or_email=args.client_email,
        needs_approval_for_absence=args.absence_approval,
        has_own_employees=args.own_employees,
        annual_fee_volume_eur=args.annual_fees,
        years_under_audit=args.audit_years,
        country=Country.DE,
    )

    if args.json:
        out = {
            "score": res.score,
            "classification": res.classification.value,
            "recommendation": res.recommendation,
            "positive_indicators": res.positive_indicators,
            "risk_indicators": res.risk_indicators,
            "backpay_simulation": res.backpay_simulation,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print("=" * 70)
        print("⚖️  STATUSFESTSTELLUNG & SCHEINSELBSTSTAENDIGKEIT PRUEFUNG 2026")
        print("=" * 70)
        print(f"Risiko-Score        : {res.score:.1f} von 100 Punkten")
        print(f"Einstufung          : {res.classification.value}")
        print(f"Empfehlung          : {res.recommendation}")
        print("\n(+) Entlastende Kriterien:")
        for pos in res.positive_indicators:
            print(f"  • {pos}")
        print("\n(!) Risiko-Indikatoren:")
        for r in res.risk_indicators:
            print(f"  • {r}")
        print("\n💰 Finanzielle Risikosimulation (Sozialversicherungs-Nachzahlung gem. § 25/24 SGB IV):")
        bp = res.backpay_simulation
        print(f"  Gepruefte Jahre   : {bp['audited_years']} Jahr(e)")
        print(f"  Honorarvolumen    : {bp['total_fee_volume_eur']:,.2f} EUR")
        print(f"  Gesamt-SV Nachz.  : ~{bp['estimated_sv_backpay_eur']:,.2f} EUR (~40 Prozent)")
        print(f"  Saeumniszuschlaege: ~{bp['estimated_late_surcharges_eur']:,.2f} EUR (1 Prozent pro Monat)")
        print(f"  Gesamtrisiko      : ~{bp['total_financial_risk_eur']:,.2f} EUR")
        print("=" * 70)


if __name__ == "__main__":
    main()
