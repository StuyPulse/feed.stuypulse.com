from timezone import UTC, Eastern

def datetimeformat(value, format='%B %d, %Y - %I:%M %p'):
    try:
        value = value.replace(tzinfo=UTC())
        value = value.astimezone(Eastern)
        return value.strftime(format)
    except:
        return value
