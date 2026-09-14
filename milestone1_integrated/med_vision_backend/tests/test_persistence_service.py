from unittest.mock import MagicMock

import pytest

from app.db.models import ProcessingStatus
from app.services.persistence import persistence_service


def test_save_result_updates_record_and_commits():
    record = MagicMock()
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = record

    persistence_service.save_result(db, "some-id", {
        "prediction_result": '{"a": 1}',
        "heatmap_image_url": "http://example.com/heatmap.png",
    })

    assert record.prediction_result == '{"a": 1}'
    assert record.heatmap_image_url == "http://example.com/heatmap.png"
    assert record.status == ProcessingStatus.COMPLETED
    db.commit.assert_called_once()


def test_save_result_raises_when_record_missing():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError):
        persistence_service.save_result(db, "missing-id", {
            "prediction_result": "{}",
            "heatmap_image_url": "",
        })


def test_mark_failed_sets_status_and_error():
    record = MagicMock()
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = record

    persistence_service.mark_failed(db, "some-id", "boom")

    assert record.status == ProcessingStatus.FAILED
    assert record.error_message == "boom"
    db.commit.assert_called_once()


def test_mark_failed_noop_when_record_missing():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    persistence_service.mark_failed(db, "missing-id", "boom")

    db.commit.assert_not_called()
