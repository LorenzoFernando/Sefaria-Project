import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# NB: WE CAN ALSO UPLOAD FILES

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
ghaLink = "https://github.com/{}/runs/{}".format(os.environ['GITHUB_REPOSITORY'], os.environ['GITHUB_RUN_ID'])
messageText="*Commit:* {}\n*User:* {}\n*Results:* {}\n*GitHub Action Link:* {}".format(os.environ['GITHUB_SHA'],os.environ['GITHUB_ACTOR'],os.environ['TEST_RESULTS_LINK'], ghaLink)

targetChannel = os.environ['TARGET_SLACK_CHANNEL']

try:
    response = client.chat_postMessage(channel=targetChannel, text=messageText, icon_emoji=":alembic:", unfurl_links=False) # send this to myself first
    assert response["message"]["text"]
    print("Success")
except SlackApiError as e:# 
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")
