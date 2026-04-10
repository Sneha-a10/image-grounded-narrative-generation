from validation_layer.routing.output_router import OutputRouter

def test_output_router():
    router = OutputRouter()

    # --- ACCEPT CASE ---
    accept = router.route(
        decision="ACCEPT",
        image_id="img_001",
        story_payload={"story": "A fox holds a rabbit"},
        failure_type=None,
        retry_count=0
    )

    print("ACCEPT:", accept)

    assert accept["route"] == "TTS"
    assert accept["status"] == "success"
    assert accept["data"]["image_id"] == "img_001"
    assert "story_payload" in accept["data"]

    # --- REJECT CASE ---
    reject = router.route(
        decision="REJECT",
        image_id="img_002",
        story_payload={"story": "A car on highway"},
        failure_type="image_misalignment",
        retry_count=1
    )

    print("REJECT:", reject)

    assert reject["route"] == "REGENERATION"
    assert reject["status"] == "retry"
    assert reject["data"]["retry_count"] == 2
    assert reject["data"]["failure_type"] == "image_misalignment"
    assert "story_payload" in reject["data"]

    # --- INVALID CASE ---
    invalid = router.route(
        decision="UNKNOWN",
        image_id="img_003",
        story_payload={},
        failure_type=None,
        retry_count=0
    )

    print("INVALID:", invalid)

    assert invalid["route"] == "ERROR"
    assert invalid["status"] == "invalid_decision"