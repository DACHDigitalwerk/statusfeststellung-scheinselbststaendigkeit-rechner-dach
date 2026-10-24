# -*- coding: utf-8 -*-
"""
DACH Statusfeststellung & Scheinselbstständigkeit Prüfer 2026.
Kriterienmodelle und Risikosimulation für Deutschland (§ 7a SGB IV), Österreich (ASVG) und die Schweiz (AHVG).
"""

__version__ = "1.0.0"
__author__ = "DACH Digitalwerk"

from .evaluator import evaluate_status
from .models import StatusClassification, CriteriaEvaluation, Country

__all__ = [
    "evaluate_status",
    "StatusClassification",
    "CriteriaEvaluation",
    "Country",
]
