from unittest.mock import patch, mock_open

def MOCKED_open(filename,read_mode=None):
    content = ""
    if filename == 'general_config.yaml':
        # Address is null
        # Missing MongoDB_user_collection & MongoDB_apiKey_collection
        content = """
MongoDB_address: ""
MongoDB_database: ilo_mock
Potion_IP: "   "
"""
    elif filename == 'x 2.txt':
        content = 'We Mocking!\n✨'
    else:
        raise FileNotFoundError(filename)
    file_object = mock_open(read_data=content).return_value
    file_object.__iter__.return_value = content.splitlines(True)
    return file_object