# -*- coding: utf-8 -*-
import json
import urllib.request
import datetime

from bs4 import BeautifulSoup
from flask import Flask, request, make_response
from slackclient import SlackClient
app = Flask(__name__)

slack_token = "xoxb-506062083639-506863453985-Jg9uGjvX9bWNdKGNWWbpxPnh"
slack_client_id = "506062083639.507464847938"
slack_client_secret = "25eef095154e02dcec5b60893159a6e6"
slack_verification = "DyIVRjKV3mU35cPMx8LoxVvy"
sc = SlackClient(slack_token)

#?
# 크롤링 함수 구현하기
def _crawl_job_keywords(text):
    # 여기에 함수를 구현해봅시다.
    text = text.replace('<@UEWRDDBUZ>','').strip()
    url_text = []
    url_text = text.split(" ")
    if text == "1" : # if. elif로 메뉴 선택
        url = "http://www.jobkorea.co.kr/starter/live/View/29986?LinkGbn=1"
        req = urllib.request.Request(url)

        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")

        list_name = []
        list_money = []

        for i in soup.find_all("td", attrs={
            "style": "border-width: medium 1px 1px medium; border-style: none solid solid none; border-color: currentColor windowtext windowtext currentColor; border-image: none; width: 206.66px; height: 18px; text-align: center; color: black; font-size: 10pt; white-space: normal;"}):
            list_name += [i.get_text().strip()]


        for i in soup.find_all("td", class_="xl64"):
            list_money += [i.get_text().strip()]

        keywords = ["공공기관 연봉정보"]
        for i in range(len(list_money)):
            keywords.append('{} : {}'.format(list_name[i], list_money[i]))
        return u'\n'.join(keywords)

    elif text == "3" : # if. elif로 메뉴 선택
        url = "http://www.jobkorea.co.kr/Top100/?Main_Career_Type=1&Search_Type=1&BizJobtype_Bctgr_Code=10016&BizJobtype_Bctgr_Name=IT%C2%B7%EC%9D%B8%ED%84%B0%EB%84%B7&Major_Big_Code=0&Major_Big_Name=%EC%A0%84%EC%B2%B4&Edu_Level_Code=9&Edu_Level_Name=%EC%A0%84%EC%B2%B4"
        req = urllib.request.Request(url)

        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")

        keywords = []
        abcd = ["IT 인터넷 기업 일간 채용 TOP 10"]
        for i, keyword in enumerate(soup.find("ol",class_="rankList").find_all("b")):
            keywords.append(keyword.get_text().strip())
        for i in range(len(keywords)):
            abcd.append('{}위: {}'.format(i+1, keywords[i]))
        return u'\n'.join(abcd)

    elif text == "2" : # if. elif로 메뉴 선택
        url = "http://www.jobkorea.co.kr/Salary/Index?coKeyword=&tabindex=2&indsCtgrCode=&indsCode=&jobTypeCode=10016&haveAGI=0&orderCode=2&coPage=1#salarySearchCompany"

        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

        keywords1 = []
        keywords2 = []
        abcd = []
        for txt in soup.find_all("ul", attrs={"id": "listCompany"}):
            for i in txt.find_all("div", class_="text"):
                keywords1.append(i.get_text().strip())
            for i in txt.find_all("div", class_="salary"):
                keywords2.append(i.get_text().strip())
        abcd += ["I T 기업 일간 채용 TOP 10"]
        for i in range(10):
            abcd.append('{}위: {}  {}'.format(i+1, keywords1[i], keywords2[i]))
        return u'\n'.join(abcd)

    elif text == '4' :

        url = "http://www.jobkorea.co.kr/starter/calendar?Sel_Date=201812&GI_Ing_Stat_Code_Text=10&Area_Code_Text=&Jobtype_Code_Text=&Major_Code_Text=&Edu_Level_Code_Text=&Work_Type_Code_Text=&Co_Type_Code_Text=&Is_Save=1&Is_Scrap=0&Is_Interest=0&GI_Ing_Stat_Code=&Is_Open=1&Is_EndOpen=0&Co_Name="

        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        day = []
        list = {}
        for txt in soup.find_all("div", class_="dayDiv"):
            for i in txt.find_all("strong", class_="day"):
                day.append(i.get_text().strip())
            for i in txt.find_all("span"):
                if i.get_text().strip().replace('시작', '') == "더보기":
                    pass
                else:
                    if day[len(day) - 1] in list:
                        list[day[len(day) - 1]] += [i.get_text().strip().replace('시작', '')]
                    else:
                        list[day[len(day) - 1]] = ["---- "+day[len(day) - 1]+"일 시작 기업----"]
                        list[day[len(day) - 1]] += [i.get_text().strip().replace('시작', '')]
        lst = []
        dt = datetime.datetime.now()
        i = dt.weekday()
        start = (dt.day -i)
        end = (dt.day + 6 -i)
        lst += ["이번주{}({}~{}) 채용시작 IT기업".format(str(dt.year)+str(dt.month),start, end)]
        for i in range(start, end):
            if str(i) in list:
                lst += list[str(i)]
            else:
                pass
        return u'\n'.join(lst)

    elif text == "메뉴" :
        return (
            '-원하는 숫자를 입력해봐!\n\n  1. 공공기관 연봉정보\n  2. I T 기업 연봉정보 (인기도순)\n  3. I T 기업 일간 채용 TOP 10\n  4. 이번주 채용 시작 IT 기업\n\n-기업분석보고서를 알아보자!\n\n  검색양식. [회사이름] 기업분석보고서\n  ([회사이름]에 원하는 회사 이름을 입력해!)\n')
    else : # if. elif로 메뉴 선택
        if url_text[-1] == "기업분석보고서":
            url = "http://www.jobkorea.co.kr/starter/companyreport?schTxt=" + text.replace(" 기업분석보고서",
                                                                                           "") + "&schCtgr=101012&schGrpCtgr=101012"
            return url
        else :
            fail = ["멍멍?\n(\'메뉴\'를 입력하면 메뉴에 대한 정보가 나와)"]

            return u'\n'.join(fail)


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = _crawl_job_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000)
