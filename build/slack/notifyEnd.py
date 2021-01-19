import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# NB: WE CAN ALSO UPLOAD FILES

# TODO 1: Take a comma-seperated list at RESULT_LIST and add a list of URLs to the completion report

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
ghaLink = "https://github.com/{}/actions/runs/{}".format(os.environ['GITHUB_REPOSITORY'], os.environ['GITHUB_RUN_ID'])

resultList = os.environ["RESULT_LIST"].split(",")

resultLinks = "*Test Results*\n"
baseResultUrl = os.environ["TEST_RESULTS_LINK"]

for result in resultList:
    resultLinks += baseResultUrl + "/" + result + "\n"


if "NIGHTLY" not in os.environ or os.environ["NIGHTLY"] == "false":
    messageText="*Commit:* {}\n*User:* {}\n*Results:* {}\n*GitHub Action Link:* {}".format(os.environ['GITHUB_SHA'],os.environ['GITHUB_ACTOR'],os.environ['TEST_RESULTS_LINK'], ghaLink)
    messageText += "\n" + resultLinks
    messageText += "\n" + baseResultUrl + "/" + "report.html"

else:
    messageText="_*NIGHTLY TEST*_\n*Commit:* {}\n*User:* {}\n*Results:* {}\n*GitHub Action Link:* {}".format(os.environ['GITHUB_SHA'],os.environ['GITHUB_ACTOR'],os.environ['TEST_RESULTS_LINK'], ghaLink)
    messageText += "\n" + resultLinks
    messageText += "\n" + baseResultUrl + "/" + "report.html"

targetChannel = os.environ['TARGET_SLACK_CHANNEL']

try:
    response = client.chat_postMessage(channel=targetChannel, text=messageText, icon_emoji=":alembic:", unfurl_links=False) # send this to myself first
    assert response["message"]["text"]
    print("Success")
except SlackApiError as e:# 
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")
