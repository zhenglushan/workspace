# -*- coding:utf-8 -*-

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

try:
    cred = credential.Credential("AKIDSkncN9AzBZFgw1CYxe8SWSAeu0J7nz97", "qWwLUOuBHCsJVR7ZliU0GH2YprfIf5IG")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "nlp.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

    req = models.LexicalAnalysisRequest()
    params = '{"Flag":1,"Text":"看不够的迷人韩国美女车模—韩敏智"}'
    req.from_json_string(params)

    resp = client.LexicalAnalysis(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)
