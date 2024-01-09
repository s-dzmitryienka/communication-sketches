class Template(Model):
    unique_name: str
    plain_text: str
    html_text: str
    sms_text: str  # validation on legnth symbols + validation on symbols to exclude html tags

