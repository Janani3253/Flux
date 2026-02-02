"""OEM matching utilities for phase2_excel_to_web

Provides functions to normalize text, match OEM names (substring + fuzzy),
and attach OEM credentials from an OEM list to an invoices DataFrame.
"""
from __future__ import annotations

import re
from typing import Optional, Iterable

import pandas as pd

try:
    from rapidfuzz import process, fuzz
    _HAS_RAPIDFUZZ = True
except Exception:
    _HAS_RAPIDFUZZ = False


def normalize_text(s: Optional[str]) -> str:
    """Uppercase, remove non-alphanumerics (keep spaces), and collapse whitespace."""
    if pd.isna(s) or s is None:
        return ""
    s = str(s).upper()
    s = re.sub(r'[^A-Z0-9\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def match_oem(invoice_series: pd.Series, oem_list: pd.Series, fuzz_threshold: int = 85, return_details: bool = False):
    """Return a Series of matched OEM names from oem_list for each invoice value.

    Strategy:
    1. Normalize both sides.
    2. Try normalized substring/exact match.
    3. If not found and rapidfuzz is available, use token_set_ratio fuzzy match.

    Returns:
        pd.Series with matched OEM (original form from oem_list) or None.
    """
    # Prepare OEM list once, then match each invoice value using the single-value matcher
    oems = [str(x) for x in pd.Series(oem_list).dropna().unique()]
    if return_details:
        rows = [match_single_oem(val, oems, fuzz_threshold=fuzz_threshold, return_details=True) for val in invoice_series]
        df = pd.DataFrame(rows, index=invoice_series.index)
        for c in ('matched', 'score', 'method'):
            if c not in df.columns:
                df[c] = None
        df = df.rename(columns={'matched': 'matched_oem', 'score': 'match_score', 'method': 'match_method'})
        return df

    results = [match_single_oem(val, oems, fuzz_threshold=fuzz_threshold) for val in invoice_series]
    return pd.Series(results, index=invoice_series.index)


def match_single_oem(invoice_oem: Optional[str], oem_list: Iterable[str], fuzz_threshold: int = 85, return_details: bool = False):
    """Match a single invoice OEM string against an iterable of OEM names.

    If `return_details` is False (default) returns matched OEM (original casing) or None.
    If `return_details` is True returns a dict: {'matched': str|None, 'score': int|None, 'method': str|None}.
    """
    oems = [str(x) for x in oem_list if pd.notna(x)]
    oems_norm = [normalize_text(x) for x in oems]
    norm_to_orig = {n: o for n, o in zip(oems_norm, oems)}

    text = normalize_text(invoice_oem)
    if not text:
        return {'matched': None, 'score': None, 'method': None} if return_details else None

    # substring/exact normalized match first
    for n_oem, orig in norm_to_orig.items():
        if n_oem and n_oem in text:
            return ({'matched': orig, 'score': 100, 'method': 'substring'} if return_details else orig)

    # token-level substring: match when invoice token is a substring of OEM name
    tokens = text.split()
    if tokens:
        for tok in tokens:
            if len(tok) < 3:
                continue
            for n_oem, orig in norm_to_orig.items():
                if tok in n_oem:
                    return ({'matched': orig, 'score': 90, 'method': 'token_substring'} if return_details else orig)

    # fuzzy fallback if available
    if _HAS_RAPIDFUZZ:
        # fuzzy on whole string
        match = process.extractOne(text, oems_norm, scorer=fuzz.token_set_ratio)
        if match and match[1] >= fuzz_threshold:
            return ({'matched': norm_to_orig.get(match[0]), 'score': int(match[1]), 'method': 'fuzzy_whole'} if return_details else norm_to_orig.get(match[0]))

        # token-level fuzzy partial matching for short/typo tokens (e.g. BRIDGESTON -> BRIDGESTONE)
        for tok in tokens:
            if len(tok) < 3:
                continue
            tmatch = process.extractOne(tok, oems_norm, scorer=fuzz.partial_ratio)
            if tmatch and tmatch[1] >= max(75, fuzz_threshold - 10):
                return ({'matched': norm_to_orig.get(tmatch[0]), 'score': int(tmatch[1]), 'method': 'fuzzy_token_partial'} if return_details else norm_to_orig.get(tmatch[0]))

    return ({'matched': None, 'score': None, 'method': None} if return_details else None)


def attach_credentials(invoices_df: pd.DataFrame, oem_df: pd.DataFrame, invoice_col: str = 'OEM_raw', oem_col: str = 'OEM', fuzz_threshold: int = 85) -> pd.DataFrame:
    """Match OEMs and attach credential columns from `oem_df` to `invoices_df`.

    Returns a new DataFrame with a `matched_oem` column and OEM credential columns merged.
    """
    if invoice_col not in invoices_df.columns:
        raise KeyError(f"invoice_col '{invoice_col}' not in invoices_df")
    if oem_col not in oem_df.columns:
        raise KeyError(f"oem_col '{oem_col}' not in oem_df")

    invoices = invoices_df.copy()
    invoices['matched_oem'] = match_oem(invoices[invoice_col], oem_df[oem_col], fuzz_threshold=fuzz_threshold)

    columns_to_drop = [col for col in oem_df.columns if col in invoices.columns]

    clean_oem_df = oem_df.drop(columns=columns_to_drop)

    merged = invoices.merge(
        clean_oem_df,
        left_on="matched_oem",
        right_on=oem_col,
        how="left"
    )
    return merged


__all__ = ['normalize_text', 'match_oem', 'attach_credentials']
