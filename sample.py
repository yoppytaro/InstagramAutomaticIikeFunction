# -*- coding: utf-8 -*-

#モジュール
import chromedriver_binary #これがないとバージョンエラーが出る
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import urllib.parse
import time
import random
from time import sleep
import schedule
import pyautogui
import datetime
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import os
import requests
import sys

#スリープ時間指定
l = [30,40,60]

#chatwork APIキー、ルームキー設定
CHATWORK_ROOM_ID = "*************"
CHATWORK_API_TOKEN = "*****************************"

dt_now = datetime.datetime.now()
dt_now_day = dt_now.strftime('%Y年%m月%d日')

def chatworkmessage(meg):
    url = 'https://api.chatwork.com/v2/rooms/' + CHATWORK_ROOM_ID + '/messages'
    headers = { 'X-ChatWorkToken': CHATWORK_API_TOKEN }
    params = { 'body': meg }

    requests.post(url,
         headers=headers,
         params=params
    )
    
    
try:
    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = '************************************'

    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #認証情報設定
    #ダウンロードしたjsonファイル名をcredentials変数に設定
    credentials = ServiceAccountCredentials.from_json_keyfile_name('*******************************.json', scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートを開く
    workbook = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = workbook.worksheet('記録')
    worksheetinfo = workbook.worksheet('アカウント情報')

    #アカウント情報取得
    #ユーザー名
    username = worksheetinfo.acell('B2').value
    #パスワード
    password = worksheetinfo.acell('C2').value
    #いいね数指定
    maxcount = worksheetinfo.acell('D2').value
except Exception as e:
    chatworkmessage("スプレット処理中にエラーが発生しました。\n" + str(e))
    sys.exit()

#フォルダ作成
try:
    os.mkdir('image/' + username)
except:
    print("作成済み")

try:
    #サイト表示
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.instagram.com/accounts/login/")
    driver.implicitly_wait(10)
    sleep(1)

     #ログインID・PWを入力
    elem_search_word = driver.find_element_by_name("username")
    elem_search_word.send_keys(username)
    sleep(1)
    elem_search_password = driver.find_element_by_name('password')
    elem_search_password.send_keys(password)
    sleep(1)
    elem_search_password.send_keys(Keys.ENTER)
    driver.implicitly_wait(10)
    sleep(10)


    #フォロワー確認
    driver.get("https://www.instagram.com/" + username)
    driver.implicitly_wait(6)
    sleep(2)
    #ログイン確認
    driver.find_elements_by_class_name("AFWDX")[0]
    followcount = driver.find_elements_by_class_name("g47SY")[1].text
except Exception as e:
    chatworkmessage("ログインに失敗しました。\n" + str(e))
    sys.exit()

cell = 1
#更新日
while True:
  time.sleep(1)
  cell_value = worksheet.acell('A' + str(cell)).value
  if (cell_value == dt_now_day):
    print("今日は" + str(cell))
    likecount = worksheet.acell('B' + str(cell)).value
    likecount = int(likecount)
    break
  elif (cell_value == ""):
    print("この空は" + str(cell))
    #更新日、いいね数、フォロワー数を入力
    worksheet.update_acell('A' + str(cell), dt_now_day)
    worksheet.update_acell('B' + str(cell), 0)
    worksheet.update_acell('C' + str(cell), followcount)
    likecount = 0
    break
  else:
    cell += 1

#フォロー中取得
try:
    follownum = driver.find_elements_by_class_name("g47SY")[1].text    
    driver.find_elements_by_class_name("-nal3")[2].click()
    sleep(2)
    count = int(follownum) // 6

    for i in range(count):
        followitems = driver.find_elements_by_class_name("MqpiF")
        followitems[i*6].location_once_scrolled_into_view
        i += 1
        sleep(10)
    
    Follow = []
    follownum = int(follownum) - 1
    for i in range(follownum):
        Follow.append(followitems[i].text)
        i += 1
except:
    print("error")
finally:
    driver.find_elements_by_class_name("wpO6b")[1].click()

    
#ページスクロール
def clickserch():
  serchount = True
  while serchount:
    driver.get("https://www.instagram.com/" + random.choice(Follow))
    driver.implicitly_wait(6)
    try:
      driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[3]/article/div/div/div[1]/div[1]/a").click()
      sleep(5)
      serchount = False
    except:
      serchount = True
    
clickserch()

def error_sending(file_name,file_path):
    #バイナリファイルでの読み込み
    file_data = open(file_path, 'rb').read()

    #ファイルの形式を設定
    files = {
        "file": (file_name, file_data, "image/png"),
    }

    #メッセージ設定
    data = {
        "message": "エラーが発生しました。"
    }

    #URL、ヘッダーを設定
    post_message_url = f"https://api.chatwork.com/v2/rooms/{CHATWORK_ROOM_ID}/files"
    headers = {'X-ChatWorkToken': CHATWORK_API_TOKEN}


    #リクエスト送信
    requests.post(
      post_message_url,
      headers=headers,
      files=files,
      data=data,
    )
    

def job():
  global likecount
  for i in range(20):
    try:
      elem = driver.find_element_by_css_selector("span.fr66n > button > div > span > svg").get_attribute('aria-label')
      if elem == "いいね！":
        #いいねする
        driver.find_element_by_xpath("/html/body/div[*]/div[2]/div/article/div[3]/section[1]/span[1]/button").click()
        print(str(dt_now.strftime('%Y年%m月%d日%H時%M分%S秒')) + "：いいね：" + str(likecount))
        driver.find_element_by_css_selector("a.coreSpriteRightPaginationArrow").click()
        sleep(4)
        likecount += 1
        i += 1
        clickserch()
      elif elem == "「いいね！」を取り消す":
        #いいね判定
        driver.find_element_by_css_selector("[aria-label=「いいね！」を取り消す]")
        sleep(1)
        #いいねされていたらパス
        print(str(dt_now.strftime('%Y年%m月%d日%H時%M分%S秒')) + "：いいね済み、パス")
        driver.find_element_by_css_selector("a.coreSpriteRightPaginationArrow").click()
        sleep(4)
    except:
      print("エラー")
      file_name = str(dt_now.strftime('%Y年%m月%d日%H時%M分%S秒')) + '.png'
      file_path = 'image/' + username + '/' + file_name
      driver.save_screenshot(file_path)
      #スクリーンショットファイル名、パス設定
      error_sending(file_name,file_path)
      clickserch()
      return
  clickserch()



def main():
  global l
  global maxcount
  schedule.every(random.choice(l)).minutes.do(job)
  while likecount <= int(maxcount):
    if likecount == 0:
      job()
    else:
      schedule.run_pending()
      time.sleep(1)
      pass
  else:
    driver.close()
    return



if __name__ == "__main__":
    main()