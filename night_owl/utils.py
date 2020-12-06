def success_response(data=None, code=200):
    if data is None:
        return {"success": True}, code

    return {"success": True, "data": data}, code


def failure_response(message, code=404):
    return {"success": False, "message": message}, code
