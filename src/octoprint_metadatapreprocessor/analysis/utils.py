def strip_comment(string):
    return string[string.find(";")+1:] if ";" in string else ""
