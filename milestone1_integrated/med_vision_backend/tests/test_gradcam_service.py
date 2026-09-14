import io
import threading

from PIL import Image

from app.services.gradcam import gradcam_service

SAMPLE_IMAGE = "test_data/sample_xray.png"


def test_generate_heatmap_concurrent_calls_are_thread_safe():
    results = {}
    errors = []

    def worker(key):
        try:
            results[key] = gradcam_service.generate_heatmap(SAMPLE_IMAGE, 0)
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(key,)) for key in ("a", "b")]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert set(results) == {"a", "b"}
    for heatmap_bytes in results.values():
        img = Image.open(io.BytesIO(heatmap_bytes))
        assert img.size == (224, 224)
        assert img.mode == "RGB"
