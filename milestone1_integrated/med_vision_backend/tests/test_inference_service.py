from app.services.inference import inference_service

SAMPLE_IMAGE = "test_data/sample_xray.png"


def test_run_returns_probability_for_every_pathology():
    result = inference_service.run(SAMPLE_IMAGE)

    assert isinstance(result, dict)
    assert len(result) == 18
    assert all(isinstance(v, float) for v in result.values())
