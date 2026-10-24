# -*- coding: utf-8 -*-
"""
Statusfeststellung & Scheinselbstständigkeit Kriterienkatalog 2026 (SGB IV, ASVG, AHVG).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List


class StatusClassification(Enum):
    CLEARLY_INDEPENDENT = "Eindeutig Selbstständig (0 % Nachzahlungsrisiko)"
    BORDERLINE_RISK = "Grauzone / Statusfeststellungsverfahren § 7a SGB IV dringend empfohlen"
    CLEARLY_DEPENDENT = "Akute Scheinselbstständigkeit / Abhängige Beschäftigung"


class Country(Enum):
    DE = "Deutschland (§ 7a SGB IV, DRV Bund)"
    AT = "Österreich (§ 4 Abs. 4 ASVG & § 1151 ABGB)"
    CH = "Schweiz (Art. 9 AHVG Ausgleichskasse)"


@dataclass
class CriteriaEvaluation:
    score: float  # 0 to 100
    classification: StatusClassification
    positive_indicators: List[str]
    risk_indicators: List[str]
    backpay_simulation: Dict[str, float]
    recommendation: str
