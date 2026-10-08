from parse_bench.inference.providers.parse import databricks_ai_parse


def test_signature_elements_are_retained_as_pictures(monkeypatch):
    monkeypatch.setattr(databricks_ai_parse, "_rendered_page_dims", lambda _: [(100.0, 200.0)])
    document = {
        "pages": [{"id": 0}],
        "elements": [
            {
                "type": "signature",
                "content": "Jane Doe",
                "confidence": 0.9,
                "bbox": [{"page_id": 0, "coord": [10, 20, 50, 60]}],
            }
        ],
    }

    pages = databricks_ai_parse._build_layout_pages(document, "unused.pdf")

    assert len(pages) == 1
    assert len(pages[0].items) == 1
    assert pages[0].items[0].type == "image"
    assert pages[0].items[0].value == "Jane Doe"
    assert pages[0].items[0].layout_segments[0].label == "Picture"


def test_figure_chart_content_is_retained_for_layout_attribution(monkeypatch):
    monkeypatch.setattr(databricks_ai_parse, "_rendered_page_dims", lambda _: [(100.0, 200.0)])
    document = {
        "pages": [{"id": 0}],
        "elements": [
            {
                "type": "figure",
                "content": '{"values":{"Sales":{"2024":7}},"additional_info":"Forecast"}',
                "description": "A bar chart of sales.",
                "bbox": [{"page_id": 0, "coord": [10, 20, 50, 60]}],
            }
        ],
    }

    pages = databricks_ai_parse._build_layout_pages(document, "unused.pdf")

    assert pages[0].items[0].type == "image"
    assert pages[0].items[0].layout_segments[0].label == "Picture"
    assert "<table>" in pages[0].items[0].html
    assert "Sales" in pages[0].items[0].html
    assert "2024" in pages[0].items[0].html
    assert "7" in pages[0].items[0].html
    assert "Forecast" in pages[0].items[0].html


def test_legacy_figure_chart_description_remains_supported(monkeypatch):
    monkeypatch.setattr(databricks_ai_parse, "_rendered_page_dims", lambda _: [(100.0, 200.0)])
    document = {
        "pages": [{"id": 0}],
        "elements": [
            {
                "type": "figure",
                "content": "Sales 7",
                "description": 'JSON:\n```json\n{"values":{"Sales":{"2024":7}}}\n```',
                "bbox": [{"page_id": 0, "coord": [10, 20, 50, 60]}],
            }
        ],
    }

    pages = databricks_ai_parse._build_layout_pages(document, "unused.pdf")

    assert "Sales" in pages[0].items[0].html
    assert "2024" in pages[0].items[0].html
    assert "7" in pages[0].items[0].html
