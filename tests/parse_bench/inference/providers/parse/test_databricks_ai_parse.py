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
