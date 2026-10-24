# -*- coding: utf-8 -*-
import pytest
from statusfeststellung_dach.evaluator import evaluate_status
from statusfeststellung_dach.models import StatusClassification


def test_clearly_independent():
    res = evaluate_status(
        has_own_capital_risk=True,
        determines_own_working_hours=True,
        determines_own_location=True,
        uses_own_equipment=True,
        has_own_website_marketing=True,
        has_multiple_clients=True,
        revenue_share_single_client_pct=30.0,
        integrated_in_team_hierarchy=False,
        wears_client_uniform_or_email=False,
        needs_approval_for_absence=False,
        has_own_employees=True,
    )
    assert res.score < 30.0
    assert res.classification == StatusClassification.CLEARLY_INDEPENDENT
    assert len(res.positive_indicators) >= 5
    assert len(res.risk_indicators) == 0


def test_clearly_dependent_scheinselbstaendig():
    res = evaluate_status(
        has_own_capital_risk=False,
        determines_own_working_hours=False,
        determines_own_location=False,
        uses_own_equipment=False,
        has_own_website_marketing=False,
        has_multiple_clients=False,
        revenue_share_single_client_pct=100.0,
        integrated_in_team_hierarchy=True,
        wears_client_uniform_or_email=True,
        needs_approval_for_absence=True,
        has_own_employees=False,
    )
    assert res.score > 60.0
    assert res.classification == StatusClassification.CLEARLY_DEPENDENT
    assert len(res.risk_indicators) >= 6


def test_borderline_risk():
    res = evaluate_status(
        has_own_capital_risk=True,
        determines_own_working_hours=True,
        determines_own_location=False,
        uses_own_equipment=True,
        has_own_website_marketing=True,
        has_multiple_clients=True,
        revenue_share_single_client_pct=70.0,
        integrated_in_team_hierarchy=True,
        wears_client_uniform_or_email=False,
        needs_approval_for_absence=False,
        has_own_employees=False,
    )
    assert 30.0 <= res.score <= 60.0
    assert res.classification == StatusClassification.BORDERLINE_RISK


def test_five_sixths_threshold_rule():
    # 85% Umsatzanteil verletzt die 5/6 Grenze (83.33%) nach § 2 Satz 1 Nr. 9 SGB VI
    res = evaluate_status(
        has_own_capital_risk=True,
        determines_own_working_hours=True,
        determines_own_location=True,
        uses_own_equipment=True,
        has_own_website_marketing=True,
        has_multiple_clients=True,
        revenue_share_single_client_pct=85.0,
        integrated_in_team_hierarchy=False,
        wears_client_uniform_or_email=False,
        needs_approval_for_absence=False,
        has_own_employees=False,
    )
    assert any("5/6" in r for r in res.risk_indicators)


def test_backpay_simulation():
    res = evaluate_status(
        has_own_capital_risk=False,
        determines_own_working_hours=False,
        determines_own_location=False,
        uses_own_equipment=False,
        has_own_website_marketing=False,
        has_multiple_clients=False,
        revenue_share_single_client_pct=100.0,
        integrated_in_team_hierarchy=True,
        wears_client_uniform_or_email=True,
        needs_approval_for_absence=True,
        has_own_employees=False,
        annual_fee_volume_eur=100000.0,
        years_under_audit=2,
    )
    sim = res.backpay_simulation
    assert sim["total_fee_volume_eur"] == 200000.0
    assert sim["estimated_sv_backpay_eur"] == 80000.0  # 40% SV
    assert sim["estimated_late_surcharges_eur"] > 0.0
    assert sim["total_financial_risk_eur"] > 80000.0
