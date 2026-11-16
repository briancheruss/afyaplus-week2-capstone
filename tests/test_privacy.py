from app.privacy import MaskingSession


def test_mask_kenyan_numbers_and_email():
    s = MaskingSession()
    masked = s.mask("Call +254 712 345 678 or 0712345678; email jane.doe+test@example.co.ke")
    assert "+254" not in masked
    assert "0712345678" not in masked
    assert "jane.doe" not in masked
    assert "[PHONE_1]" in masked and "[EMAIL_1]" in masked
    assert s.restore_approved(masked) == masked
    assert s.restore_approved(masked, authorized=True).startswith("Call +254")


def test_mask_stable_across_turns_and_clear():
    s = MaskingSession()
    assert s.mask("0712345678") == s.mask("0712345678")
    assert s.mask("[PHONE_1]") == "[PHONE_1]"
    s.clear()
    assert s.mapping == {}


def test_mask_other_local_formats():
    s = MaskingSession()
    for number in ["0112345678", "254712345678", "+254-712-345-678", "+254 112 345 678"]:
        assert number not in s.mask(number)
