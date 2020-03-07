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
import time


class HWOcrClientToken(object):
    """OCR Client authenticated by token

    initializd by username,domainname,passwrod,region,endpoint

    Attributes:
        domainname: domainname for ocr user.If not IAM user, it's the same with username
        region: region name for the ocr user,such as cn-north-1,cn-east-2
        password:password for the ocr user
        httpendpoint:httpendpoint for the ocr request
        token: temporary authentication key for the ocr user, expired after 24 hours
    """
    def __init__(self,domainname, username, password, region,endpoint):
        """
        Constructor for the HWOcrClientToken
        """
        if domainname=="" or username == "" or password == "" or region == "" or endpoint == "":
            raise ValueError('The parameter for the HWOcrClientToken constructor cannot be empty')
        self.domainname=domainname
        self.username = username
        self.password = password
        self.region = region
        self.httpendpoint = endpoint
        self.token = None

        self.refreshCount = 0
        self._RETRY_TIMES = 3
        self._POLLING_INTERVAL = 2.0

    def get_token(self):
        """
        get the token for the ocr user from IAM server
        :return:
        """
        if self.token is not None:
            return self.token
        retry_times = 0
        endpoint = 'iam.%s.myhuaweicloud.com' % self.region
        url = 'https://%s/v3/auth/tokens' % endpoint
        headers = {'Content-Type': 'application/json'}
        payload = {
          "auth": {
            "identity": {
              "methods": [
                "password"
              ],
              "password": {
                "user": {
                  "name": self.username,
                  "password": self.password,
                  "domain": {
                    "name": self.domainname
                  }
                }
              }
            },
            "scope": {
              "project": {
                "name": self.region  # region name
              }
            }
          }
        }
        try:
            while True:
                response = requests.post(url, json=payload, headers=headers)
                if 201 != response.status_code:
                    if retry_times < self._RETRY_TIMES:
                        retry_times += 1
                        print("Reget token.")
                        time.sleep(self._POLLING_INTERVAL)
                        self.token = None
                        continue
                    else:
                        print("Get token failed!")
                        print(response.text)
                        self.token = None
                        return None
                else:
                    print("Get token success!")
                    token = response.headers.get('X-Subject-Token', '')
                    self.token = token
                    return token
        except Exception as e:
            print(e)
            return None

    def refresh_token(self):
        """
        refresh the attribute token
        :return:None
        """
        print("token expired, refresh.")
        self.token = None
        self.get_token()

    def request_ocr_service_base64(self,uri,filepath,options=None):
        """
        :param uri: the uri for the http request to be called
        :param filepath: the fullpath of the file to be recognized
        :param options: optional parameter in the ocr http request
        :return:None
        """
        if filepath == "" or uri == "":
            raise ValueError("the parameter for request_ocr_service_base64 cannot be empty")
        self.get_token()
        if self.token is not None:
            try:
                url="https://"+self.httpendpoint+uri
                headers = {
                    'Content-Type' : 'application/json',
                    'X-Auth-Token' : self.token
                }
                with open(filepath, 'rb') as bin_data:
                    image_data=bin_data.read()
                image_base64= base64.b64encode(image_data).decode("utf-8")
                payload = {}
                payload['image'] = image_base64
                if options:
                    payload.update(options)
                response = requests.post(url, json=payload, headers=headers)
                if 401 == response.status_code and ("Token expired" in response.text):
                    #token expired,refresh token
                    self.refresh_token()
                    return self.request_ocr_service_base64(uri, filepath, options)

                elif 403 == response.status_code and ("The authentication token is abnormal." in response.text):
                    # token expired,refresh token
                    self.refresh_token()
                    return self.request_ocr_service_base64(uri, filepath, options)

                return response
            except Exception as e:
                print(e)
                return None
        return None




