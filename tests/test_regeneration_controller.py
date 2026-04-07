from regeneration_controller.controller import RegenerationController


def test_retry_flow():
    rc = RegenerationController("Neutral_Descriptive")

    result = rc.handle_rejection("signal_violation")

    assert result["action"] == "RETRY"
    assert result["constraint_input"]["retry_count"] == 1


def test_multiple_retries():
    rc = RegenerationController("Neutral_Descriptive")

    rc.handle_rejection("signal_violation")
    rc.handle_rejection("signal_violation")

    result = rc.handle_rejection("signal_violation")

    assert result["action"] == "STOP"


def test_user_prompts_persist():
    rc = RegenerationController(
        "Neutral_Descriptive",
        user_negative_prompts=["no rain"]
    )

    result = rc.handle_rejection("signal_violation")

    assert "no rain" in result["user_negative_prompts"]