# -*- coding:utf-8 -*-
# Copyright 2018 Huawei Technologies Co.,Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License.  You may obtain a copy of the
# License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.

import base64
import requests
import json
from apig_sdk import signer


class HWOcrClientAKSK(object):
    """OCR Client authenticated by AKSK

    initializd by ak,sk,endpoint

    Attributes:
        ak: Access key for ocr user
        sk: Secret key for ocr user
        httpendpoint:httpendpoint for the ocr request
    """
    def __init__(self,ak,sk,httpendpoint):
        if ak == "" or sk == "" or httpendpoint == "":
            raise ValueError('The parameter for the HWOcrClientAKSK constructor cannot be empty')
        self.endpoint=httpendpoint
        self.sig=signer.Signer()
        self.sig.AppKey=ak
        self.sig.AppSecret=sk
        self.httpschema="https" #currently only support https
        self.httpmethod="POST"  #currently only support post

    def request_ocr_service_base64(self,uri, filepath, options=None):
        """
        :param uri: the uri for the http request to be called
        :param filepath: the fullpath of the file to be recognized
        :param options: optional parameter in the ocr http request
        :return:None
        """
        if filepath == "" or uri == "":
            raise ValueError("the parameter for requestOcrServiceBase64 cannot be empty")
        request=signer.HttpRequest()
        request.scheme=self.httpschema
        request.host=self.endpoint
        request.method=self.httpmethod
        request.uri=uri
        request.headers={"Content-Type": "application/json"}
        with open(filepath, 'rb') as f:
            img = f.read()
        img_base64 = base64.b64encode(img).decode("utf-8")
        body = {}
        body['image'] = img_base64
        if options:
            body.update(options)
        request.body=json.dumps(body)
        self.sig.Sign(request)
        url = self.httpschema+"://"+self.endpoint+uri
        #response=requests.request(self.httpmethod,url,data=request.body,headers=request.headers)
        response = requests.post(url, data=request.body, headers=request.headers)
        return response


