from tfl.api_token import ApiToken
from tfl.client import Client

with open("app.key", "r") as f:
    app_key = f.readline()

with open("app.id", "r") as f:
    app_id = f.readline()

token = ApiToken(app_id, app_key)

client = Client(token)
print(client.get_line_meta_modes())
print(client.get_lines(line_id="tram"))
