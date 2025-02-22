#!/usr/bin/env python
# -*- coding:utf-8 -*-
###
# File: /home/hky/anisotropy/code/testwecom.py
# Project: /home/hky/anisotropy/code
# Created Date: 2022-05-01 16:29:53
# Author: Hu Kongyi
# Email:hukongyi@ihep.ac.cn
# -----
# Last Modified: 2022-06-16 16:55:50
# Modified By: Hu Kongyi
# -----
# HISTORY:
# Date      	By      	Comments
# ----------	--------	----------------------------------------------------
# 2022-06-10	K.Y.Hu		add except send
# 2022-05-25	K.Y.Hu		add Decorators
# 2022-05-01	K.Y.Hu		finish send text, image and markdown
###
import os
import json
import time
import datetime
import sys

import requests


def send_to_wecom_text(text,
                       wecom_cid,
                       wecom_aid,
                       wecom_secret,
                       wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "text",
            "text": {
                "content": text
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def send_to_wecom_image(image_content,
                        wecom_cid,
                        wecom_aid,
                        wecom_secret,
                        wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image'
        upload_response = requests.post(upload_url,
                                        files={
                                            "picture": image_content
                                        }).json()
        if "media_id" in upload_response:
            media_id = upload_response['media_id']
        else:
            print(upload_response)
            return False

        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "image",
            "image": {
                "media_id": media_id
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def send_to_wecom_file(file_content,
                       wecom_cid,
                       wecom_aid,
                       wecom_secret,
                       wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file'
        upload_response = requests.post(upload_url,
                                        files={
                                            "file": file_content
                                        }).json()
        if "media_id" in upload_response:
            media_id = upload_response['media_id']
        else:
            return False

        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "file",
            "file": {
                "media_id": media_id
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def send_to_wecom_markdown(text,
                           wecom_cid,
                           wecom_aid,
                           wecom_secret,
                           wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "markdown",
            "markdown": {
                "content": text
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def send_to_wecom(content, content_type="text"):
    with open('/home/hky/github/SendWecom/sendwecom/wecom_inform.json',
              "r") as f:
        data = json.load(f)
    wecom_cid = data["wecom_cid"]
    wecom_aid = data["wecom_aid"]
    wecom_secret = data["wecom_secret"]
    wecom_touid = data["wecom_touid"]
    if wecom_touid is None:
        wecom_touid = "@all"
    if content_type == "text":
        return send_to_wecom_text(content,
                                  wecom_cid,
                                  wecom_aid,
                                  wecom_secret,
                                  wecom_touid=wecom_touid)
    elif content_type == "image":
        if os.path.getsize(content) / float(1024 * 1024) < 10:
            image_content = open(content, "rb").read()
            return send_to_wecom_image(image_content,
                                       wecom_cid,
                                       wecom_aid,
                                       wecom_secret,
                                       wecom_touid=wecom_touid)
        elif os.path.getsize(content) / float(1024 * 1024) < 20:
            file_content = open(content, "rb")
            return send_to_wecom_file(file_content,
                                      wecom_cid,
                                      wecom_aid,
                                      wecom_secret,
                                      wecom_touid=wecom_touid)

    elif content_type == "markdown":
        return send_to_wecom_markdown(content,
                                      wecom_cid,
                                      wecom_aid,
                                      wecom_secret,
                                      wecom_touid=wecom_touid)


def send_to_wecom_after_finish(function):
    def new_function(*args, **kwargs):
        start_time = time.time()
        try:
            output = function(*args, **kwargs)
        except KeyboardInterrupt:
            send_to_wecom(f"{os.path.basename(sys.argv[0])} 键盘中断!!!!")
        except BaseException as err:
            send_to_wecom(f"{os.path.basename(sys.argv[0])} 报错!!!!")
            send_to_wecom(f"Unexpected {err=}, {type(err)=}")
        else:
            send_to_wecom(
                f"{os.path.basename(sys.argv[0])}已完成\n用时：{datetime.timedelta(seconds=time.time() - start_time)}"
            )
            if output is not None:
                send_to_wecom(f"{output=}")

    return new_function


@send_to_wecom_after_finish
def test():
    pass


if __name__ == "__main__":
    test()
    # res = send_to_wecom("/home/hky/latex/参数对比/image/sumNb1.jpg", content_type="image")
    # print(res)
