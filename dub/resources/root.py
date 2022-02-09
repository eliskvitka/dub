from flask import Blueprint, current_app

root_blueprint = Blueprint(
    'root',
    __name__,
    url_prefix='/'
)


@root_blueprint.route('/', methods=['GET'])
def root():
    return {
            "meta": {
                "serverName": current_app.config.get("SERVER_NAME", "Server name"),
                "feature.non_email_login": True
            },
            "skinDomains": [
                current_app.config.get("SKIN_DOMAIN", ".example.com")
            ],
            "signaturePublickey": current_app.config.get("PUBLIC_RSA_KEY")
        }