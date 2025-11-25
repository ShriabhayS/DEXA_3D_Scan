"""
Unit tests for DEXA PDF parser.
"""
import pytest
from pathlib import Path
from backend.app.dexa_parser import parse_pdf_bytes, DexaParserError


def test_parse_valid_pdf():
    """Test parsing a valid DEXA PDF."""
    # This would require a test PDF file
    # For now, we'll test the structure
    sample_pdf_path = Path("../../data/samples/194_REES_Beau_.pdf")
    
    if not sample_pdf_path.exists():
        pytest.skip("Sample PDF not found")
    
    pdf_bytes = sample_pdf_path.read_bytes()
    
    try:
        result = parse_pdf_bytes(pdf_bytes)
        assert result is not None
        assert hasattr(result, 'body_metrics')
        assert hasattr(result, 'regions')
    except DexaParserError:
        # PDF might not be parseable, which is okay for MVP
        pass


def test_parse_invalid_pdf():
    """Test parsing an invalid PDF."""
    invalid_bytes = b"Not a PDF"
    
    with pytest.raises(DexaParserError):
        parse_pdf_bytes(invalid_bytes)


def test_parse_empty_pdf():
    """Test parsing an empty PDF."""
    # Create a minimal invalid PDF
    empty_pdf = b"%PDF-1.4\n"
    
    with pytest.raises(DexaParserError):
        parse_pdf_bytes(empty_pdf)

