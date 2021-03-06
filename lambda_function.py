import urllib.request, urllib.error, urllib.parse
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    lineMessage = event["lineMessage"]["events"][0]["message"]["text"]
    logger.info("lineMessage : " + lineMessage)
    res = getReply(lineMessage)
    if res != None:
        logger.info("response message : " + res)
        return {"message":res}
    else:
        logger.info("response message : " + "No Response")
        return None
    

def getReply(message):

    url = os.environ.get('TalkAPI_URL')

    reqdata = {}
    reqdata['apikey'] = os.environ.get('TalkAPI_Key')
    reqdata['query'] = message

    params = urllib.parse.urlencode(reqdata).encode('utf-8')
    request = urllib.request.Request(url, params)
    response = urllib.request.urlopen(request)
    resJson = response.read()

    resDict = json.loads(resJson)

    logger.info("response from API(json) : " + json.dumps(resDict, ensure_ascii=False, indent=4 ) )

    status = resDict["status"]

    if status == 0:
        perplexity = resDict["results"][0]["perplexity"]
        if perplexity > 0.2 and perplexity < 1.0:
            reply = resDict["results"][0]["reply"]
        else:
            reply = None
    else:
        reply = None
    
    logger.info("response from API : " + resDict["message"])

    return reply