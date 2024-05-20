def create_kakao_response(outputs, quick_replies=None):
    response = {
        "version": "2.0",
        "template": {
            "outputs": outputs
        }
    }
    if quick_replies:
        response["template"]["quickReplies"] = quick_replies
    return response

