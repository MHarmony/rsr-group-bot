import logging
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


class Alert:
    def craftTextBody(favorites):
        return "Test"

    @staticmethod
    def craftEmailBody(favorites):
        return "Test"

    @staticmethod
    def sendEmail(favorites=[]):
        load_dotenv()
        logger = logging.getLogger("logger")

        client = boto3.client("pinpoint", region_name=os.getenv("AWS_REGION"))

        try:
            response = client.send_messages(
                ApplicationId=os.getenv("PINPOINT_PROJECT_ID"),
                MessageRequest={
                    "Addresses": {os.getenv("ALERT_EMAIL"): {"ChannelType": "EMAIL"}},
                    "MessageConfiguration": {
                        "EmailMessage": {
                            "Body": Alert.craftEmailBody(favorites),
                            "SimpleEmail": {
                                "Subject": {
                                    "Charset": "UTF-8",
                                    "Data": "[RSR GROUP BOT] - STOCK UPDATE",
                                },
                                "TextPart": {
                                    "Charset": "UTF-8",
                                    "Data": Alert.craftEmailBody(favorites),
                                },
                            },
                        },
                    },
                },
            )
        except ClientError as e:
            logger.error(e.response["Error"]["Message"])
        else:
            logger.info(
                f"Message: {response['MessageResponse']['Result'][os.getenv('ALERT_EMAIL')]['MessageId']} send successfully"
            )

    @staticmethod
    def sendText(favorites=[]):
        load_dotenv()
        logger = logging.getLogger("logger")

        client = boto3.client("pinpoint", region_name=os.getenv("AWS_REGION"))

        try:
            response = client.send_messages(
                ApplicationId=os.getenv("PINPOINT_PROJECT_ID"),
                MessageRequest={
                    "Addresses": {os.getenv("ALERT_NUMBER"): {"ChannelType": "SMS"}},
                    "MessageConfiguration": {
                        "SMSMessage": {
                            "Body": Alert.craftTextBody(favorites),
                            "Keyword": os.getenv("PINPOINT_KEYWORD"),
                            "MessageType": "TRANSACTIONAL",
                            "OriginationNumber": os.getenv("PINPOINT_NUMBER"),
                            "SenderId": "rsrgroupbot",
                        }
                    },
                },
            )
        except ClientError as e:
            logger.error(e.response["Error"]["Message"])
        else:
            logger.info(
                f"Message: {response['MessageResponse']['Result'][os.getenv('ALERT_NUMBER')]['MessageId']} sent successfully"
            )
