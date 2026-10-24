# -*- coding: utf-8 -*-
import json
import subprocess
import sys


def test_cli_help():
    cmd = [sys.executable, "-m", "statusfeststellung_dach.cli", "--help"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "dach-statusfeststellung" in res.stdout
    assert "SGB IV" in res.stdout


def test_cli_independent_run():
    cmd = [
        sys.executable,
        "-m",
        "statusfeststellung_dach.cli",
        "--capital-risk",
        "--own-hours",
        "--own-location",
        "--own-equipment",
        "--own-marketing",
        "--own-employees",
        "--single-client-pct", "30",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "Eindeutig Selbstständig" in res.stdout
    assert "Entlastende Kriterien" in res.stdout


def test_cli_dependent_json():
    cmd = [
        sys.executable,
        "-m",
        "statusfeststellung_dach.cli",
        "--integrated-hierarchy",
        "--client-email",
        "--absence-approval",
        "--single-client-pct", "100",
        "--annual-fees", "80000",
        "--audit-years", "3",
        "--json",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["score"] > 50.0
    assert "Scheinselbstständigkeit" in data["classification"]
    assert data["backpay_simulation"]["total_fee_volume_eur"] == 240000.0
