from validation_layer.routing.output_router import OutputRouter

def test_accept_route():
    router = OutputRouter()

    result = router.route("ACCEPT", "img1", {}, None, 0)

    assert result["route"] == "TTS"


def test_reject_route():
    router = OutputRouter()

    result = router.route("REJECT", "img1", {}, "signal_violation", 0)

    assert result["route"] == "REGENERATION"