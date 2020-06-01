import boto3
import base64
from botocore.exceptions import ClientError
import json
import requests
from mysite import settings



class Secret():

    def __init__(self, secret_name=None):

        region_name = "us-west-2"

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e  # Meh, should probably handle this. Oh well...
        else:
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])

        self.secret = json.loads(secret)


class SecretKey(Secret):

        def __init__(self):
            super().__init__('django_blog_secret_key')
            self.secret_key = self.secret['django_blog_secret_key']


class DatabaseCredentials(Secret):

    def __init__(self):
        super().__init__('django_db_creds')
        self.user = self.secret['username']
        self.password = self.secret['password']
        self.engine = self.secret['engine']
        self.host = self.secret['host']
        self.port = self.secret['port']


def get_allowed_hosts():
    """
    Grab instance meta-data for public DNS name.
    :return: Fully-qualified domain name of instance - str
    """
    r = requests.get('http://169.254.169.254/latest/meta-data/public-hostname')
    fqdn = r.text
    return [fqdn]
