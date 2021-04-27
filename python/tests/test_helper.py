import Helper
import pytest


@pytest.mark.helper_validate_keys
def test_valid_key(apikey):
    """Ensure the helper returns True for a valid key"""
    assert Helper.validate_APIKey(apikey["valid"]) == True


@pytest.mark.helper_validate_keys
def test_invalid_key(apikey):
    """Ensure the helper returns false for an invalid key"""
    assert Helper.validate_APIKey(apikey["invalid"]) == False


@pytest.mark.helper_validate_keys
def test_empty_key():
    """Ensure the helper returns false for an empty key"""
    assert Helper.validate_APIKey("") == False


@pytest.mark.helper_validate_keys
def test_invalid_format_key(apikey):
    """Ensure the helper returns false for an incorrectly formatted key"""
    assert Helper.validate_APIKey(apikey["invalid_incorrect_format"]) == False


@pytest.mark.helper_validate_password
def test_correct_password():
    """Ensure the helper returns True for a valid password"""
    assert Helper.validate_password("Feathers_F@lling_0n_Fresh_Sn0w") == True


@pytest.mark.helper_validate_password
def test_correct_no_minimum_length():
    """Ensure the helper enforces length"""
    assert Helper.validate_password("M0on!") == False


@pytest.mark.helper_validate_password
def test_correct_no_numbers():
    """Ensure the helper enforced numbers"""
    assert Helper.validate_password("Mooooooooooooon!") == False


@pytest.mark.helper_validate_password
def test_correct_no_lowercase():
    """Ensure the helper enforces lowercase"""
    assert Helper.validate_password("FEATHERS_F@LLING_0N_FRESH_SN0W") == False


@pytest.mark.helper_validate_password
def test_correct_no_uppercase():
    """Ensure the helper encforces uppercase"""
    assert Helper.validate_password("feathers_f@lling_0n_fresh_sn0w") == False


@pytest.mark.helper_validate_password
def test_correct_special_character():
    """Ensure the helper enforces the use of a special character"""
    assert Helper.validate_password("Feathers_Falling_0n_Fresh_Sn0w") == False