from datetime import datetime

from parse_bench.evaluation.layout_adapters.adapters import DatabricksAiParseLayoutAdapter
from parse_bench.schemas.parse_output import LayoutItemIR, LayoutSegmentIR, ParseLayoutPageIR, ParseOutput
from parse_bench.schemas.pipeline_io import InferenceRequest, InferenceResult
from parse_bench.schemas.product import ProductType


def test_chart_html_is_attributed_as_table_content_while_label_stays_picture():
    segment = LayoutSegmentIR(x=0.1, y=0.2, w=0.4, h=0.3, label="Picture")
    output = ParseOutput(
        task_type="parse",
        example_id="chart",
        pipeline_name="databricks_ai_parse",
        pages=[],
        layout_pages=[
            ParseLayoutPageIR(
                page_number=1,
                width=100,
                height=200,
                items=[
                    LayoutItemIR(
                        type="image",
                        value="Sales 7",
                        html="<table><tr><th>Sales</th><th>2024</th></tr><tr><td>7</td></tr></table>",
                        bbox=segment,
                        layout_segments=[segment],
                    )
                ],
            )
        ],
        markdown="",
    )
    now = datetime.now()
    result = InferenceResult(
        request=InferenceRequest(
            example_id="chart",
            source_file_path="chart.pdf",
            product_type=ProductType.PARSE,
        ),
        pipeline_name="databricks_ai_parse",
        product_type=ProductType.PARSE,
        raw_output={},
        output=output,
        started_at=now,
        completed_at=now,
        latency_in_ms=0,
    )
    adapter = DatabricksAiParseLayoutAdapter()

    layout_output = adapter.to_layout_output(result)
    prediction = layout_output.predictions[0]
    blocks = adapter.to_attribution_blocks(layout_output, page_number=1)

    assert prediction.label == "Picture"
    assert prediction.content is not None
    assert prediction.content.type == "table"
    assert blocks[0].label == "Picture"
    assert blocks[0].block_type == "table"
    assert blocks[0].text == "Sales 2024 7"
