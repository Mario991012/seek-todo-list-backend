from src.core.common.return_codes import ReturnCode

def format_response(return_code: ReturnCode, data: dict = None):
    if data is None:
        data = {}
    return {
        "return_code": return_code.value,
        "data": data
    }
