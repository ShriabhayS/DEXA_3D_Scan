"""
Utilities for parsing DEXA scan PDFs into structured metrics.
"""
from __future__ import annotations

import io
import re
from datetime import datetime
from typing import Dict, Optional, Tuple

import pdfplumber

from .models import DexaBodyMetrics, DexaRegionMetrics, DexaScanData


METRIC_PATTERNS: Dict[str, re.Pattern[str]] = {
    "total_fat_percent": re.compile(r"total\s+body\s+fat\s*%?\s*[:\-]?\s*(\d+(?:\.\d+)?)", re.I),
    "total_lean_mass_kg": re.compile(r"lean\s+mass\s*\(kg\)\s*[:\-]?\s*(\d+(?:\.\d+)?)", re.I),
    "total_bone_mass_kg": re.compile(
        r"(?:bone\s+mass|bmd)\s*\(kg\)\s*[:\-]?\s*(\d+(?:\.\d+)?)", re.I
    ),
    "weight_kg": re.compile(r"weight\s*\(kg\)\s*[:\-]?\s*(\d+(?:\.\d+)?)", re.I),
    "height_cm": re.compile(r"height\s*\(cm\)\s*[:\-]?\s*(\d+(?:\.\d+)?)", re.I),
    "android_fat_percent": re.compile(r"android\s+fat\s*%?\s*[:\-]?\s*(\d+(?:\.\d+)?)", re.I),
    "gynoid_fat_percent": re.compile(r"gynoid\s+fat\s*%?\s*[:\-]?\s*(\d+(?:\.\d+)?)", re.I),
}

REGION_NAMES = ["arms", "legs", "trunk", "android", "gynoid"]


class DexaParserError(RuntimeError):
    """Raised when the parser cannot recover meaningful metrics."""


def _extract_first(pattern: re.Pattern[str], text: str) -> Optional[float]:
    match = pattern.search(text)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def _extract_region_metrics(text: str) -> Dict[str, DexaRegionMetrics]:
    regions: Dict[str, DexaRegionMetrics] = {}
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    tokenized = [re.split(r"\s{2,}|\t", line) for line in lines]

    for tokens in tokenized:
        if not tokens:
            continue

        key = tokens[0].lower()
        if any(region in key for region in REGION_NAMES):
            values = [float(val) for val in re.findall(r"\d+(?:\.\d+)?", " ".join(tokens[1:]))]
            if values:
                fat_percent = values[0] if values else None
                regions[key] = DexaRegionMetrics(
                    fat_percent=fat_percent,
                    lean_mass_kg=values[1] if len(values) > 1 else None,
                    bone_mass_kg=values[2] if len(values) > 2 else None,
                )
    return regions


def parse_pdf_bytes(pdf_bytes: bytes) -> DexaScanData:
    """
    Parse a DEXA PDF (provided as bytes) into a DexaScanData object.
    """

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        pages_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    if not pages_text.strip():
        raise DexaParserError("Unable to read text from PDF")

    body_kwargs = {
        key: _extract_first(pattern, pages_text) for key, pattern in METRIC_PATTERNS.items()
    }

    if not any(body_kwargs.values()):
        raise DexaParserError("Failed to extract primary DEXA metrics")

    regions = _extract_region_metrics(pages_text)

    patient_id = None
    patient_match = re.search(r"patient\s+id\s*[:\-]?\s*([A-Za-z0-9_-]+)", pages_text, re.I)
    if patient_match:
        patient_id = patient_match.group(1)

    scan_date = None
    date_match = re.search(
        r"(?:scan|report)\s+date\s*[:\-]?\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})", pages_text, re.I
    )
    if date_match:
        raw = date_match.group(1)
        for fmt in ("%m/%d/%Y", "%d/%m/%Y", "%m/%d/%y"):
            try:
                scan_date = datetime.strptime(raw, fmt).date().isoformat()
                break
            except ValueError:
                continue

    device_model = None
    device_match = re.search(r"(?:device|model)\s*[:\-]?\s*([A-Za-z0-9\s-]+)", pages_text, re.I)
    if device_match:
        device_model = device_match.group(1).strip()

    return DexaScanData(
        patient_id=patient_id,
        scan_date=scan_date,
        device_model=device_model,
        body_metrics=DexaBodyMetrics(**body_kwargs),
        regions=regions,
    )


