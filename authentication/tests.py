import base64
import time


def timestamp_to_datetime(timestamp):
    """
    timestamp:时间戳
    将时间戳转换为日期格式字符串
    :return:日期格式字符串
    """
    # 首先需要将时间戳转换成localtime，再转换成时间的具体格式
    time_local = time.localtime(timestamp)
    # 利用strftime()函数重新格式化时间
    datetime_str = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return datetime_str


def decode_base64(data):
    """Decode base64, padding being optional.
    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    # base64长度是4的倍数，如果不足，需要用'='补齐
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return str(base64.b64decode(data),
               encoding='utf-8')


if __name__ == '__main__':
    code = 'eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NTczMjM5NCwiaWF0IjoxNjQ1NjQ1OTk0LCJqdGkiOiI2MWYwY2Q2NmEzN2E0NWM4OWIyMzE5NTlmNjAwM2YyMSIsInVzZXJfaWQiOjMsIm1vYmlsZSI6IjEzNzc4MjYwNDY2Iiwibmlja25hbWUiOiJcdTYwYzVcdTRmNTVcdTRlZTVcdTU4MmFcdTIwMTQiLCJlbWFpbCI6ImFkbWluMTEyQHFxLmNvbSJ9'
    code2 = 'eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NTczMjM5NCwiaWF0IjoxNjQ1NjQ1OTk0LCJqdGkiOiI2MWYwY2Q2NmEzN2E0NWM4OWIyMzE5NTlmNjAwM2YyMSIsInVzZXJfaWQiOjN9'
    res = decode_base64(code)
    res2 = decode_base64(code2)
    print(res)
    print(res2)
    # print(timestamp_to_datetime(1645635737))
    # print(timestamp_to_datetime(1645635917))
