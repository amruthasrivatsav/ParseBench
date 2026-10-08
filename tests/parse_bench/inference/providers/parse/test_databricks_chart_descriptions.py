import pytest

from parse_bench.evaluation.metrics.parse.rules_chart import ChartDataPointRule
from parse_bench.inference.providers.parse.databricks_ai_parse import _render_markdown


@pytest.mark.parametrize("content", ["Figure text", ""])
def test_legacy_figure_description_reaches_scorer(content):
    figure = {
        "type": "figure",
        "content": content,
        "description": 'JSON:\n```json\n{"values":{"Sales":{"2024":7}}}\n```',
    }
    markdown = _render_markdown([figure])
    rule = ChartDataPointRule({"type": "chart_data_point", "value": "7", "labels": ["Sales", "2024"]})
    assert rule.run(markdown)[0]
    assert markdown.startswith(content)


def test_figure_content_reaches_scorer_without_rendering_raw_json():
    content = '{"values":{"Sales":{"2024":7}},"additional_info":"Forecast"}'
    figure = {
        "type": "figure",
        "content": content,
        "description": "A bar chart of sales.",
    }

    markdown = _render_markdown([figure])
    rule = ChartDataPointRule({"type": "chart_data_point", "value": "7", "labels": ["Sales", "2024"]})

    assert rule.run(markdown)[0]
    assert markdown.startswith("<table>")
    assert content not in markdown
    assert "Forecast" in markdown
