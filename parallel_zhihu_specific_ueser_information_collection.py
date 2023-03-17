# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import multiprocessing as mp
from time import sleep
import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import starmap

chrome_ports = ['9222','9223','9224','9225','9226']

visible = 1
if visible:
    window_position = {'x':'0','y':'0'}
    
else:
    window_position = {'x':'4000','y':'0'}
    
class Login_ZhiHu():
    
    def __init__(self,url,chrome_port):
        cmd = 'chrome.exe --remote-debugging-port='+ chrome_port + ' --window-position='+ window_position['x'] + ',' + window_position['y'] + ' --user-data-dir=\"E:\Iront\StudyItems\TC\Crouses\ContentSecurity\EX1_ZhiHu_Info_collention\project\chrome_user_data_'+ chrome_port + '\"'
        os.popen(cmd)
        # 连接chrome浏览器，否则会出现知乎搜索功能不可用，某用户的回答不可见
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:" + chrome_port)  #  前面设置的端口号
        # chrome在后台运行，没有显示在屏幕最上方，可能会导致一些元素无法被定位或加载
        # 下两行的option可以避免后台运行chrome导致元素无法加载的问题
        options.add_argument("--headless")
        # 解决元素在headless模式下不可见的问题
        # options.add_argument("--window-size=1920,1080")
        self.url = url
        self.driver = webdriver.Chrome(options=options)
        self.login_cookie = None
        self.driver.set_window_position(int(window_position['x']), int(window_position['y']))
        # if url == 'https://zhihu.com':
            
            # self.driver.maximize_window()  # 设置页面最大化，用于设置其他窗口大小
        
    def third_party_WeiBo_login(self,usr,pwd):
        self.driver.get(self.url)
        self.driver.maximize_window()
        # 点击通过微博登录
        self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[3]/span/button[3]').click()                            
        # 操作刚打开的微博第三方登陆界面
        all_handles = self.driver.window_handles
        # 稍后从第三方登录页面切换回知乎主页会用到
        ZhiHu_Handle = all_handles[0] 
        # 切换到微博登陆界面句柄
        WeiBo_Handle = all_handles[1] 
        self.driver.switch_to.window(WeiBo_Handle)
        # 切换到输入用户名和密码的界面
        self.driver.find_element(By.XPATH,'//*[@id="jump_login_url_a"]').click()
        
        # 等待加载页面，下同
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        except:
            print("Login Failed! Check u network statue")
        # 输入微博账号和密码
        self.driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(usr)
        self.driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(pwd)   
        sleep(1)
        # 登录
        self.driver.find_element(By.XPATH,'//*[@id="vForm"]/div[2]/div/ul/li[7]/div[1]/input').click()  
        try:                          
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="message_sms_login"]')))
        except:
            print("Login Failed! Check u network statue")
        # 点击扫码验证
        self.driver.find_element(By.XPATH,'//*[@id="qrCodeCheck"]').click()
        # find 验证码的链接
        img_src = self.driver.find_element(By.XPATH,'//*[@id="qrcode"]')
        src = img_src.get_attribute("src")
        
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="outer"]/div/div[2]/div/div[2]/div[2]/p/a[1]')))
        except:
            print("Login Failed! Check u network statue")
        # 确认授权
        self.driver.find_element(By.XPATH,'//*[@id="outer"]/div/div[2]/div/div[2]/div[2]/p/a[1]').click()
        self.driver.switch_to.window(ZhiHu_Handle)
        
    def sign_cookie(self):
        # self.driver.get(self.url)
        try:
            WebDriverWait(self.driver,10000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Popover1-toggle"]')))
        except:
            print("Waiting for you to scan for a long time -_-")
        dictCookies = self.driver.get_cookies() # 获取list的cookies
        jsonCookies = json.dumps(dictCookies) # 转换成字符串保存
        with open('ZhiHu_cookies.txt', 'w') as f:
            f.write(jsonCookies)
            print('cookies保存成功！')
            
    def cookie_login(self):
        self.driver.get(self.url)
        # try:
        #     WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[2]/div[2]/label/input')))
        # except:
        #     print("Check u network statue")
        # 还需要在开头加上：# -*- coding: utf-8 -*-
        if self.login_cookie == None:
            with open('ZhiHu_cookies.txt', 'r', encoding='utf-8') as f:
                self.login_cookie = listCookies = json.loads(f.read())
        else:
             listCookies = self.login_cookie
        # 往driver里添加cookies
        for cookie in listCookies:
            cookie_dict = {
                'domain': '.zhihu.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            self.driver.add_cookie(cookie_dict)
        # 此处没有必要sleep
        self.driver.refresh()
        
    def prepared_drive(self):
        return self.driver
    
    
class User_ZhiHu():
    
    def __init__(self,driver):
        
        self.driver = driver
        # 第零个元素为用户asks/answers的总数
        self.answers_edit_statue = ['']*10
        self.asks_edit_statue = ['']*10
        self.valid_asks_count = 0
        self.valid_answers_count = 0

    def goto_user_home_page(self,username):
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Popover1-toggle"]')))
        except:
            print("Search Failed! Check u network statue")
        # //*[@id="SearchMain"]/div/div/div/div/div[2]/div/div
        # //*[@id="SearchMain"]/div/div/div/div/div[2]/div/div
        # 输入搜索内容
        self.driver.find_element(By.XPATH,'//*[@id="Popover1-toggle"]').send_keys(username)
        # 点击搜索
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/header/div[2]/div[1]/div/form/div/div/label/button/span')))
        except:
            print("Search Failed! Check u network statue")
        self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/header/div[2]/div[1]/div/form/div/div/label/button/span').click()
        # 点击搜索内容为用户
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div[1]/div/div/ul/li[2]/a')))
        except:
            print("Search Failed! Check u network statue")
        self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div[1]/div/div/ul/li[2]/a').click()
        # 上述操作会被知乎检测出来（可能会被识别出来是爬虫？反正不管怎么sleep，除了综合那一栏，其他栏都不能正常加载，但是人为点击不会出错），但是可以通过刷新页面绕过检测
        self.driver.refresh()
        # 等待搜索页面加载
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="SearchMain"]/div/div/div/div/div[2]/div/div/div/div[1]/div/span/div/a/img')))
        except:
            print("Search Failed! Check u network statue")
        # 将第一个搜索结果视为目标搜索结果
        self.driver.find_element(By.XPATH,'//*[@id="SearchMain"]/div/div/div/div/div[2]/div/div/div/div[1]/div/span/div/a/img').click()
        # 切换到目的用户主页的句柄
        all_handles = self.driver.window_handles
        user_home_Handle = all_handles[1]
        # 始终保持最多仅有两个窗口，一个是正在处理的，一个是处理完当前串口需要返回的
        self.driver.close() 
        self.driver.switch_to.window(user_home_Handle)
        
        # 切换窗口后，再次使用该语句，可以新打开的窗口解决元素在headless模式下不可见的问题 # 看着晃眼睛，而且现在我质疑这条语句的有效性，先删掉
        # self.driver.set_window_size(1920, 1080)
        # self.driver.maximize_window()   
        return self.driver.current_url
    
    def user_basic_information_collection(self,output_filename):
        user_information = {}
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[1]')))
        except:
            print("Search Failed! Check u network statue")
        # xpath value is not //*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[1]/text()
        username = self.driver.find_element(By.XPATH,'//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[1]').text
        user_information['用户名'] = username
        ####################获取一句话介绍#######################
        declaration = self.driver.find_element(By.XPATH,'//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[2]').text
        if declaration == '':
            declaration = 'empty'
        user_information['一句话介绍'] = declaration
        ####################获取用户性别#######################
        try:
            self.driver.find_element(By.CSS_SELECTOR,'svg.Zi.Zi--Male').get_attribute("class")
            gender = 'Male'
        except:
            try:
                self.driver.find_element(By.CSS_SELECTOR,'svg.Zi.Zi--Female').get_attribute("class")
                gender = 'Female'
            except:
                gender = 'Not Found'
        user_information['性别'] = gender
        ####################查找'居住地', '所在行业','职业经历'，'个人简介'等信息#######################
        # 点击“查看详细资料”
        self.driver.find_element(By.XPATH,'//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[3]/button').click()
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/div/div')))
        except:
            print("Search Failed! Check u network statue")
        elements = self.driver.find_elements(By.CSS_SELECTOR,'div.ProfileHeader-detailItem')
        # labels = []
        # 遍历每个元素，并获取其子元素<span class="ProfileHeader-detailLabel">和<div class="ProfileHeader-detailValue">的inner HTML字符串
        for element in elements:
            label = element.find_element(By.CSS_SELECTOR,'span.ProfileHeader-detailLabel').text
            raw_value = element.find_element(By.CSS_SELECTOR,'div.ProfileHeader-detailValue')
            value = re.sub("<[^>]+>", "", raw_value.get_attribute("innerHTML"))
            # labels.append(label)
            if label in ['居住地', '所在行业','职业经历']:
                if value == '':      
                    value = 'empty'
                user_information[label] = value
            if label == '个人简介':
                # 使用正则表达式去除所有尖括号及尖括号以内的内容re.sub(r'<[^>]*>', '', html)
                personal_profile = re.sub(r'<[^>]*>', '', self.driver.find_element(By.CSS_SELECTOR,'div.ztext.ProfileHeader-detailValue').get_attribute("innerHTML"))
                user_information[label] = personal_profile
        # print(labels)
        user_information_tag_list =  ['用户名','性别','一句话介绍','居住地','所在行业','职业经历','个人简介']
        for user_information_tag in user_information_tag_list:
            if user_information_tag not in user_information:
                user_information[user_information_tag] = 'Not Found' 
        with open(output_filename, 'a', encoding='utf-8') as f:
                # ['用户名','性别','一句话介绍','居住地','所在行业','职业经历','个人简介']
                # ['发帖时间','发帖内容','评论次数','点赞次数','评论信息']
            f.write('<------------------------User--Information--Collection--start------------------------->' + '\n')
            f.write('->当前搜索用户的基本信息：' + '\n')
            for information in user_information:
                f.write(information + ":" + user_information[information] + '\n')
        
    def user_relationship_information_collection(self,follower_XPATH,active_or_passive,output_filename):
        # 点击关注按钮（ps：这里如果是需要搜集“关注该用户的人“，是不需要进行下面这条语句的，但是执行搜索“该用户关注的人”的信息时，又是只需要下面这条语句，而不需要下下条语句，但是为了调用接口函数的统一性，这两条语句都写在这里）
        self.driver.find_element(By.XPATH,'//*[@id="ProfileMain"]/div[1]/ul/li[9]/a').click()
        # 点击“该用户关注的人”或者“关注该用户的人”按钮
        self.driver.find_element(By.XPATH,follower_XPATH).click()
        self.driver.refresh()
        followers_active_and_passive_count = self.driver.find_elements(By.XPATH,'//strong[@class="NumberBoard-itemValue"]')
        if active_or_passive == 'active':
            followers_count = int(followers_active_and_passive_count[0].get_attribute("title"))
        else:
            followers_count = int(followers_active_and_passive_count[1].get_attribute("title"))
            
        valid_followers_count = min(followers_count,10)
        
        followers_information = [{"isEmpty": 0} for i in range(10)]
        if valid_followers_count == 0:
            followers_information = [{"isEmpty": 1} for i in range(10)]
        else: 
            for i in range(valid_followers_count,10):
                followers_information[i]['isEmpty'] = 1
            follower_information_tag_list = ['用户昵称','链接地址','回答数','文章数','关注者数']
            try:
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="List-item"]')))
            except:
                print("Search Failed! Check u network statue")
            # 获取它关注的人的信息
            # followers_href_and_name_list = self.driver.find_elements(By.XPATH,'//span[@class="UserLink"]/div/a')
            # 如果follower的个数小于10，那么对应的isEmpty的值设置为1，否则为0
            # 定位一个用户信息栏
            list_items = self.driver.find_elements(By.XPATH,'//div[@class="List-item"]')
            # 从这里开始我才开始了解xpath的原理..
            index = 0
            # followers_href_and_name_list = self.driver.find_elements(By.XPATH,'//span[@class="UserLink"]/div/a')
            for list_item in list_items[0:valid_followers_count]:
                follower_href_and_name = list_item.find_element(By.XPATH,'.//span[@class="UserLink"]/div/a')
                followers_information[index]['用户昵称'] = follower_href_and_name.text


                followers_information[index]['链接地址'] = follower_href_and_name.get_attribute("href")
                followers_answers_articles_followers = list_item.find_elements(By.XPATH,'.//div[@class="ContentItem-status"]/span')
                tag_list = ['回答','文章','关注者']
                # 是当前follower的[{'回答':'62' },{'文章':'1'},{'关注者':'151'}]信息
                # current_followers_info = [{follower_answers_articles_followers.text.split(' ')[1]: follower_answers_articles_followers.text.split(' ')[0]} for follower_answers_articles_followers in followers_answers_articles_followers]
                for tag in tag_list:
                    followers_information[index][tag+'数'] = '0'
                    for follower_answers_articles_followers in followers_answers_articles_followers:
                        if tag == follower_answers_articles_followers.text.split(' ')[1]:
                            followers_information[index][tag+'数'] = follower_answers_articles_followers.text.split(' ')[0]
                index += 1      
                  

        with open(output_filename, 'a', encoding='utf-8') as f:
            f.write('>>>>>>>>接下来显示该用户的关注与被关注信息：' + '\n')
            if active_or_passive == 'active':
                f.write('->该用户关注的人' + '\n')
            else:
                f.write('->关注该用户的人' + '\n')
            for i in range(valid_followers_count):
                
                for follower_information_tag in follower_information_tag_list:
                    f.write(follower_information_tag + ':' + followers_information[i][follower_information_tag] + '\n')
                
    def answers_information_collection(self,index,output_filename):
        # pass
        answers_information = [{"isEmpty": 0} for i in range(10)]
        # 切换到新打开的回答问题的页面的句柄
        # 切换窗口后，再次使用该语句，可以新打开的窗口解决元素在headless模式下不可见的问题 # 看着晃眼睛，而且现在我质疑这条语句的有效性，先删掉
        # self.driver.set_window_size(1920, 1080)
        # self.driver.maximize_window()
        try:
            # 有的页面的这个xpath值和大多数的不一样。
            # 等待时间所在的xpath值出现
            # WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div[1]/div/a/span')))
            
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="ContentItem-time"]/a/span')))
        except:
            print("Search Failed! Check u network statue")
      
        # 回答不分是否有推荐提问的人干扰xpath的情况 # 当有推荐提问的人时，会出现额外的干扰项的class = List-item的标签
        
        # time_raw 是一个列表：['发布于' '年-月-日' '时:分']
        # time_raw = self.driver.find_element(By.XPATH,'//div[@class="ContentItem-time"]/a/span').get_attribute("aria-label").split(' ')
        time_raw = self.driver.find_element(By.XPATH,'//div[@class="ContentItem-time"]/a/span').text.split(' ')
        # ['发帖时间','发帖内容','评论次数','点赞次数','评论信息']
        answers_information[index]['发帖时间'] = time_raw[1] + '-' + time_raw[2]
        
        # 回答内容的HTML代码，因为不确定内容中是否有图片等内容，后续计划将这部分内容使用flask呈现出来
        # 若为视频回答，则使用except的代码
        ask_title = self.driver.find_element(By.XPATH,'//h1[@class="QuestionHeader-title"]').text 
        try:
            # answers_information[index]['发帖内容'] = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/span[1]/div/div/span').get_attribute("outerHTML")
            answers_information[index]['发帖内容'] = ask_title + '\n' + self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/span[1]/div/div/span').text

        except:
            try:
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//img[@class="css-lawu0e"]')))
            except:
                print("Search Failed! Check u network statue")
            answers_information[index]['发帖内容'] = ask_title + '\n' + self.driver.find_element(By.XPATH,'//img[@class="css-lawu0e"]').get_attribute("src")
                                                                   
        comment_description = self.driver.find_element(By.XPATH,'//button[@class="Button ContentItem-action FEfUrdfMIKpQDJDqkjte Button--plain Button--withIcon Button--withLabel fEPKGkUK5jyc4fUuT0QP B46v1Ak6Gj5sL2JTS4PY RuuQ6TOh2cRzJr6WlyQp"]').text

        if comment_description == '添加评论':
            answers_information[index]['评论次数'] = '0'
        else:
            answers_information[index]['评论次数'] = comment_description.split(' ')[0]
        # 经验教训：下面注释掉的4行代码使用的xpath完全不如跟具class定位的xpath要精确，有的页面注释掉的部分的xpath值会有些变动
        answers_information[index]['点赞次数'] = self.driver.find_element(By.XPATH,'//button[@class="Button VoteButton VoteButton--up FEfUrdfMIKpQDJDqkjte"]').get_attribute("aria-label").split(' ')[1]    
       
        # 还需要在开头加上：# -*- coding: utf-8 -*-
        # with open(output_filename, 'a', encoding='utf-8') as f:
        #         # ['用户名','性别','一句话介绍','居住地','所在行业','职业经历','个人简介']
        #         # ['发帖时间','发帖内容','评论次数','点赞次数','评论信息']
        #     f.write('>>>>>>当前用户的回答：' + '\n')
        #     f.write('-->第'+ str(index) + "条回答:" + '\n')
        #     answers_tags = ['发帖时间','发帖内容','评论次数','点赞次数']
        #     for answers_tag in answers_tags:
        #         f.write(answers_tag + ":" + answers_information[index][answers_tag]+'\n')
        
        
        ####### 评论 # 有的文章过长会出现固定在页面下方的评论框，并弹窗出现评论
        if comment_description == '添加评论':
            comments_information = [{"isEmpty": 1} for i in range(10)]
        else:
            comments_information = [{"isEmpty": 0} for i in range(10)]
            
            self.driver.find_element(By.XPATH,'//button[@class="Button ContentItem-action FEfUrdfMIKpQDJDqkjte Button--plain Button--withIcon Button--withLabel fEPKGkUK5jyc4fUuT0QP B46v1Ak6Gj5sL2JTS4PY RuuQ6TOh2cRzJr6WlyQp"]').click()

              
            # 等待至第一个评论加载出来 # 有的评论是js脚本加载出的弹窗处理与下述代码有异需要做特殊处理

            
            unfold_comment_buttons = self.driver.find_elements(By.CLASS_NAME, 'Button--secondary')
            for button in unfold_comment_buttons:
                self.driver.execute_script("arguments[0].click();", button)

            try:
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="CommentContent css-1ygdre8"]')))
            except:
                print("Search Failed! Check u network statue")
            comments_content = self.driver.find_elements(By.XPATH, '//div[@class="CommentContent css-1ygdre8"]')

            comments_times = self.driver.find_elements(By.XPATH,'//span[@class="css-12cl38p"]')
            
            comments_href_and_usernames =self.driver.find_elements(By.XPATH,'//a[@class="css-1rd0h6f"]')
          
            comments_likes = self.driver.find_elements(By.CSS_SELECTOR, '.Button--plain.Button--grey.Button--withIcon.Button--withLabel.css-h1yvwn')

            all_comments_count = len(comments_likes)
            valid_comment_count = 10
            if all_comments_count < 10:
                for i in range(all_comments_count,10):
                    comments_information[i]['isEmpty'] = 1
                valid_comment_count = all_comments_count
            for i in range(0,valid_comment_count):
                # 评论人ID、评论人昵称、评论时间、评论内容、点赞次数
                comments_information[i]['评论人昵称'] = comments_href_and_usernames[i].text
                if comments_href_and_usernames[i].text != '匿名用户':
                    comments_information[i]['评论人ID'] = comments_href_and_usernames[i].get_attribute("href").split('/')[-1]
                else:
                    comments_information[i]['评论人ID'] = 'Not Found because of anonymous'
                
                comments_information[i]['评论时间'] = comments_times[i].text
                
                comments_information[i]['评论内容'] = comments_content[i].text
                if comments_likes[i].text == '赞':
                    comments_information[i]['点赞次数'] = '0'
                else:
                    comments_information[i]['点赞次数'] = comments_likes[i].text
                    
                    
                # with open(output_filename, 'a', encoding='utf-8') as f:
                    
                #         f.write('---->第'+ str(i) + "条评论:" +'\n')
                #         comments_tags = ['评论人ID','评论人昵称','评论时间','评论内容','点赞次数']
                #         for comments_tag in comments_tags:
                #             f.write(comments_tag + ":" + comments_information[i][comments_tag] + '\n')
                                                     
        answers_information[index]['评论信息'] = comments_information
        
        self.driver.close()
    
              
    def user_answers_information_collection(self):
        
        # 处理回答数为0的特殊情况：
        answers_tag_in_this_list = self.driver.find_elements(By.XPATH, '//a[@class="Tabs-link"]')
        for answers_tag in answers_tag_in_this_list:
            if answers_tag.get_attribute("href").split('/')[-1] == 'answers' and answers_tag.find_element(By.XPATH, './/span').text != '':
                answers_tag_clickable = answers_tag
                answers_count = int(answers_tag.find_element(By.XPATH, './/span').text)
                break
        answers_tag.click()
        self.driver.refresh()
        # answers_information = [{"isEmpty": 0} for i in range(10)]
        valid_answers_count = min(answers_count,10)
        
        if valid_answers_count == 0:
            print("No Answers!!")
            answers_href_list = []

        else:
            # 等待加载出回答
            try:
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="List-item"]')))
                # WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//a[@data-za-detail-view-element_name="Title"]')))
            except:
                print("Search Failed! Check u network statue")
            # 获取当前页面所有回答的element列表
            # answers_pages = self.driver.find_elements(By.XPATH, '//a[@data-za-detail-view-element_name="Title"]')
            answers_href_list = [element.get_attribute("href") for element in self.driver.find_elements(By.XPATH, '//a[@data-za-detail-view-element_name="Title"]')[0:valid_answers_count]]
            answer_index = 0
            # for answer_page in answers_pages[:valid_answers_count]:
            #     # answer_page.click()
            #     # self.answers_information_collection(answers_information,answer_index,output_filename)
            #     answer_index += 1
        # for i in range(valid_answers_count,10):
        #     answers_information[i]['isEmpty'] = 1
        
        return answers_href_list[0:10]
    def asks_information_collection(self,asks_information,index,answers_count,output_filename):

        # 切换窗口后，再次使用该语句，可以新打开的窗口解决元素在headless模式下不可见的问题 # 看着晃眼睛，而且现在我质疑这条语句的有效性，先删掉
        # self.driver.set_window_size(1920, 1080)
        # self.driver.maximize_window()
        try:
            # 依据关注问题按钮问题标题是否出现判断页面加载完全（感觉其实是有问题的）
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//h1[@class="QuestionHeader-title"]')))
        except:
            print("Search Failed! Check u network statue")
        try:
            self.driver.find_element(By.XPATH,'//Button[@class="Button QuestionRichText-more FEfUrdfMIKpQDJDqkjte Button--plain fEPKGkUK5jyc4fUuT0QP"]').click()
        except:
            x = 1
        try:
            ask_content = self.driver.find_element(By.XPATH,'//span[@class="RichText ztext css-1g0fqss"]').text
        except:
            ask_content = ''
        ask_title = [title.text for title in self.driver.find_elements(By.XPATH,'//h1[@class="QuestionHeader-title"]') if title.text != ''][0]
        asks_information[index]['提问内容'] =   ask_title + '\n' + ask_content 

        asks_tags = ['提问时间','回答数','关注人数','提问内容'] 
        # with open(output_filename, 'a', encoding='utf-8') as f:
        #     f.write('---->第'+ str(index) + "条提问:" +'\n')
        #     for tag in asks_tags:
        #                 # ['用户名','性别','一句话介绍','居住地','所在行业','职业经历','个人简介']
        #                 # ['发帖时间','发帖内容','评论次数','点赞次数','评论信息']
        #         f.write(tag + ":" + asks_information[index][tag] + '\n')
        
            
        # print(ask_content)
        
        ask_answers_information = [{"isEmpty": 0} for i in range(10)]
        answers_count = int(answers_count)
        valid_answers_count = min(answers_count,10)
        # print(ask_title)
        # print("--->",answers_count)
        # print(valid_answers_count)
        # 使最少加载出valid_answer_count数量的回答
        # print(answers_count)
        if valid_answers_count > 0:
            try:
                # 依据关注问题按钮问题标题是否出现判断页面加载完全（感觉其实是有问题的）
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="List-item" and @tabindex="0"]')))
            except:
                print("Search Failed! Check u network statue")
        
        # 
        # print("--->",ask_answers_count)
        # print(valid_answers_count)
            # Scroll down until the count is at least 10

        # while ask_answers_count < valid_answers_count:
            # Scroll by 100 pixels
        
            ask_answers = self.driver.find_elements(By.XPATH,'//div[@class="List-item" and @tabindex="0"]')
            ask_answers_count = len(ask_answers)
            while ask_answers_count < valid_answers_count:
                # Scroll by 100 pixels
                self.driver.execute_script("window.scrollBy(0, -30);")
                self.driver.execute_script("window.scrollBy(0, 100);")# self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                ask_answers = self.driver.find_elements(By.XPATH,'//div[@class="List-item" and @tabindex="0"]')
                ask_answers_count = len(ask_answers)
                if (ask_answers_count == answers_count):
                    break
                
            ask_answer_tags = ['回答人ID','回答人昵称','回答时间','回答内容','点赞次数']
            ask_answers_index = 0
            for ask_answer in ask_answers[0:valid_answers_count]:
                ask_answers_information[ask_answers_index]['回答人ID'] = ask_answer.find_element(By.XPATH,'.//div[@class="css-1gomreu"]/a').get_attribute("href").split('/')[-1]
                ask_answers_information[ask_answers_index]['回答人昵称'] = ask_answer.find_elements(By.XPATH,'.//div[@class="css-1gomreu"]/a')[1].text
                # 有时会报错？
                # 有一些多余的list items
                try:
                
                    WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="ContentItem-time"]/a')))
                except:
                    print("Search Failed! Check u network statue")
                try:
                    raw_time = ask_answer.find_element(By.XPATH,'.//div[@class="ContentItem-time"]/a').text.split(' ')
                except:
                    continue
                ask_answers_information[ask_answers_index]['回答时间'] = raw_time[1] + '-' + raw_time[2]
            
                ask_answers_information[ask_answers_index]['回答内容'] = ask_answer.find_element(By.XPATH,'.//span[@class="RichText ztext CopyrightRichText-richText css-1g0fqss"]').text
                try:
                    ask_answers_information[ask_answers_index]['点赞次数'] = ask_answer.find_element(By.XPATH,'.//Button[@class="Button VoteButton VoteButton--up FEfUrdfMIKpQDJDqkjte"]').text.split(' ')[1]
                except:
                    ask_answers_information[ask_answers_index]['点赞次数'] = '0'
                # with open(output_filename, 'a', encoding='utf-8') as f:
                #     f.write('>>第'+ str(ask_answers_index) + "条回答:" +'\n')
                #     for tag in ask_answer_tags:
                #         f.write(tag + ":" + ask_answers_information[ask_answers_index][tag] + '\n')
                # ask_answers_index += 1

        

            # print("No Ask_answers!!")
            
        # ask_answer_tags = ['回答人ID','回答人昵称','回答时间','回答内容','点赞次数']
        # ask_answers_index = 0
        # for ask_answer in ask_answers[0:valid_answers_count]:
        #     ask_answers_information[ask_answers_index]['回答人ID'] = ask_answer.find_element(By.XPATH,'.//div[@class="css-1gomreu"]/a').get_attribute("href").split('/')[-1]
        #     ask_answers_information[ask_answers_index]['回答人昵称'] = ask_answer.find_elements(By.XPATH,'.//div[@class="css-1gomreu"]/a')[1].text
        #     # 有时会报错？
        #     # 有一些多余的list items
        #     try:
            
        #         WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="ContentItem-time"]/a')))
        #     except:
        #         print("Search Failed! Check u network statue")
        #     try:
        #         raw_time = ask_answer.find_element(By.XPATH,'.//div[@class="ContentItem-time"]/a').text.split(' ')
        #     except:
        #         continue
        #     ask_answers_information[ask_answers_index]['回答时间'] = raw_time[1] + '-' + raw_time[2]
        
        #     ask_answers_information[ask_answers_index]['回答内容'] = ask_answer.find_element(By.XPATH,'.//span[@class="RichText ztext CopyrightRichText-richText css-1g0fqss"]').text
        #     try:
        #         ask_answers_information[ask_answers_index]['点赞次数'] = ask_answer.find_element(By.XPATH,'.//Button[@class="Button VoteButton VoteButton--up FEfUrdfMIKpQDJDqkjte"]').text.split(' ')[1]
        #     except:
        #         ask_answers_information[ask_answers_index]['点赞次数'] = '0'
        #         # with open(output_filename, 'a', encoding='utf-8') as f:
        #         #     f.write('>>第'+ str(ask_answers_index) + "条回答:" +'\n')
        #         #     for tag in ask_answer_tags:
        #         #         f.write(tag + ":" + ask_answers_information[ask_answers_index][tag] + '\n')
        #         # ask_answers_index += 1

        
        self.driver.close()
      
    
    def user_questions_information_collection(self):   
        
        asks_tag_in_this_list = self.driver.find_elements(By.XPATH, '//a[@class="Tabs-link"]')
        # 这里会有个空字符串是我妹能理解的
        for asks_tag in asks_tag_in_this_list:
            if asks_tag.get_attribute("href").split('/')[-1] == 'asks' and asks_tag.find_element(By.XPATH, './/span').text != '':
                asks_tag_clickable = asks_tag
                asks_count = int(asks_tag.find_element(By.XPATH, './/span').text)
                break
        
        self.driver.execute_script("arguments[0].click();", asks_tag_clickable)
        # asks_tag_clickable.click()
        self.driver.refresh()
        asks_information = [{"isEmpty": 1} for i in range(10)]
        # valid可能有问题，可能仅有九个，min的第二个参数可能应该取11才正确，
        valid_asks_count = min(asks_count,10)
        
        if valid_asks_count == 0:
            x = 1
            asks_href_list = []
            # p
        else:
            # 等待加载出回答
            try:
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="List-item"]')))
            except:
                print("Search Failed! Check u network statue")
            # 获取当前页面所有回答的element列表
            asks_list_items = self.driver.find_elements(By.XPATH, '//div[@class="List-item"]')
            asks_href_list = [ask_list_item.find_element(By.XPATH, './/div[@class="QuestionItem-title"]/a').get_attribute("href") for ask_list_item in asks_list_items[0:valid_asks_count]]
            # https://www.zhihu.com/question/303899535
            # print(asks_href_list)
            ask_index = 0
            for asks_list_item in asks_list_items[0:valid_asks_count]:
                asks_information[ask_index]['isEmpty'] = 0
                asks_time_answers_followers =  asks_list_item.find_elements(By.XPATH,'.//span[@class="ContentItem-statusItem"]')
                asks_information[ask_index]['提问时间'] = asks_time_answers_followers[0].text
                answers_count = asks_time_answers_followers[1].text.split(' ')[0]
                asks_information[ask_index]['回答数'] = answers_count
                asks_information[ask_index]['关注人数'] = asks_time_answers_followers[2].text.split(' ')[0]
    
                # asks_list_item.find_element(By.XPATH, './/a[@data-za-detail-view-name="Title"]').click()
                # self.asks_information_collection(asks_information,ask_index,answers_count,output_filename)
                ask_index += 1
            # print(asks_information)
        
        return asks_href_list,asks_information


    def check_update(self):
        check_update_list = [False,False]
        # 有更新返回True，否则False
        answers_asks_tag_in_this_list = self.driver.find_elements(By.XPATH, '//a[@class="Tabs-link"]')
        for asks_answers_tag in answers_asks_tag_in_this_list:
            if asks_answers_tag.get_attribute("href").split('/')[-1] == 'answers' and asks_answers_tag.find_element(By.XPATH, './/span').text != '':
                answers_tag_clickable = asks_answers_tag
                try:
                    total_answers_count = int(asks_answers_tag.find_element(By.XPATH, './/span').text)
                except:
                    total_answers_count = 0
            if asks_answers_tag.get_attribute("href").split('/')[-1] == 'asks' and asks_answers_tag.find_element(By.XPATH, './/span').text != '':
                asks_tag_clickable = asks_answers_tag
                try:
                    total_asks_count = int(asks_answers_tag.find_element(By.XPATH, './/span').text)
                except:
                    total_asks_count = 0
            
        valid_answers_count = min(total_answers_count,10)
        valid_asks_count = min(total_asks_count,10)
        if valid_answers_count == self.valid_answers_count:
            self.valid_answers_count = valid_answers_count
            check_update_list[0] = True
        else:
            self.driver.execute_script("arguments[0].click();", answers_tag_clickable)
            # answers_tag_clickable.click()
            self.driver.refresh()
            try:
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="List-item"]')))
            except:
                print("Search Failed! Check u network statue")
            answers_list_items = self.driver.find_elements(By.XPATH,'//div[@class="List-item"]')
            answers_edit_statue = []
            for answers_list_item in answers_list_items[0:10]:
                # 注释掉的部分可能导致非预期错误发生 # 可能是refresh导致的
                # answers_list_item.find_element(By.XPATH,'//Button[@class="Button ContentItem-more FEfUrdfMIKpQDJDqkjte Button--plain fEPKGkUK5jyc4fUuT0QP"]').click()
                self.driver.execute_script("arguments[0].click();",answers_list_item.find_element(By.XPATH,'.//Button[@class="Button ContentItem-more FEfUrdfMIKpQDJDqkjte Button--plain fEPKGkUK5jyc4fUuT0QP"]'))
                answers_edit_statue.append(answers_list_item.find_element(By.XPATH,'.//div[@class="ContentItem-time"]/a/span').text)
            if answers_edit_statue != self.answers_edit_statue:
                self.answers_edit_statue = answers_edit_statue
                check_update_list[0] = True         
        if valid_asks_count == self.valid_asks_count:
            self.valid_asks_count = valid_asks_count
            check_update_list[1] = True
        else:
            # answers_list_item.find_element(By.XPATH,'//Button[@class="Button ContentItem-more FEfUrdfMIKpQDJDqkjte Button--plain fEPKGkUK5jyc4fUuT0QP"]').click()可能导致下一步的click出错
            username = self.driver.find_element(By.XPATH, '//span[@class="ProfileHeader-name"]').text
            self.driver.find_element(By.XPATH, '//*[@id="ProfileMain"]/div[1]/ul/li[4]/a').click()
            self.driver.refresh()
            try:
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="List-item"]')))
            except:
                print("Search Failed! Check u network statue")
            asks_list_items = self.driver.find_elements(By.XPATH,'//div[@class="List-item"]')
            asks_edit_statue = []
            ask_index = 0
            for asks_list_item in asks_list_items[0:10]:
                asks_list_item.find_element(By.XPATH, './/a[@data-za-detail-view-name="Title"]').click()
                all_handles = self.driver.window_handles
                user_home_Handle = all_handles[0]
                new_answer_page = all_handles[1]

                self.driver.switch_to.window(new_answer_page)
                # 切换窗口后，再次使用该语句，可以新打开的窗口解决元素在headless模式下不可见的问题 # 看着晃眼睛，而且现在我质疑这条语句的有效性，先删掉
                # self.driver.set_window_size(1920, 1080)
                # self.driver.maximize_window()
                try:
                    # 依据关注问题按钮问题标题是否出现判断页面加载完全（感觉其实是有问题的）
                    WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//Button[@class="Button FEfUrdfMIKpQDJDqkjte Button--plain Button--withIcon Button--iconOnly fEPKGkUK5jyc4fUuT0QP B46v1Ak6Gj5sL2JTS4PY hIwDV_tcL6XN1HprrnAq"]')))
                except:
                    print("Search Failed! Check u network statue")
                self.driver.find_element(By.XPATH, '//Button[@class="Button FEfUrdfMIKpQDJDqkjte Button--plain Button--withIcon Button--iconOnly fEPKGkUK5jyc4fUuT0QP B46v1Ak6Gj5sL2JTS4PY hIwDV_tcL6XN1HprrnAq"]').click()
                self.driver.find_element(By.XPATH, '//a[@class="Button Menu-item QuestionHeader-menu-item FEfUrdfMIKpQDJDqkjte Button--plain fEPKGkUK5jyc4fUuT0QP"]').click()
                
                
                try:
                    # 依据关注问题按钮问题标题是否出现判断页面加载完全（感觉其实是有问题的）
                    WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="zm-item"]')))
                except:
                    print("Search Failed! Check u network statue")
                edit_blogs = self.driver.find_elements(By.XPATH, '//div[@class="zm-item"]')
                for blog in edit_blogs:
                    if username == blog.find_element(By.XPATH, './/a[@target="_blank"]').text :
                        latest = blog.find_element(By.XPATH, './/div[@class="zm-item-meta"]/time').text
                        if latest != self.asks_edit_statue[ask_index]:
                            self.asks_edit_statue[ask_index] = latest
                            check_update_list[1] = True
                ask_index += 1
                self.driver.close()
                self.driver.switch_to.window(user_home_Handle)

        
class parallel():
    def __init__(self,home_page_url):
        self.home_page_url = home_page_url
        self.half_window_width = 1936 
        self.half_window_height = 1056
        
    # 关注者
    def get_driver(self,page_url,chrome_port,position_x,position_y,width,height):
        
        Login_user_home_page = Login_ZhiHu(page_url,chrome_port)
        Login_user_home_page.cookie_login()
        Login_user_home_page_driver = Login_user_home_page.prepared_drive()
        Login_user_home_page_driver.set_window_position(int(window_position['x'])+position_x, position_y)
        Login_user_home_page_driver.set_window_size(width, height)
        
        return Login_user_home_page_driver
    def  follower(self):
        
        follower_driver = self.get_driver(self.home_page_url,chrome_ports[1],0,0,self.half_window_width,self.half_window_height)
        
        follower_active_XPATH = '//*[@id="Profile-following"]/div[1]/h4/div/a[1]'

        User_ZhiHu(follower_driver).user_relationship_information_collection(follower_active_XPATH,'active','active_followers_information.txt')
        follower_driver.close()
    
    def following(self):
        driver = self.get_driver(self.home_page_url,chrome_ports[2],self.half_window_width,0,self.half_window_width,self.half_window_height)
        
        follower_passive_XPATH = '//*[@id="Profile-following"]/div[1]/h4/div/a[2]'

        User_ZhiHu(driver).user_relationship_information_collection(follower_passive_XPATH,'passive','passive_followers_information.txt')
        driver.close()
    # def following():
    def answers(self):
        driver = self.get_driver(self.home_page_url,chrome_ports[3],0,self.half_window_height,self.half_window_width,self.half_window_height)
        answers_chrome_port = [str(i) for i in range(9233,9243)]
        answers_href_list =  User_ZhiHu(driver).user_answers_information_collection()
        # answers_href_list_head = answers_href_list[:5]
        # answers_href_list_tail = answers_href_list[5:10]
        

        driver.close()
        if len(answers_href_list) > 0 :
            width = (self.half_window_width*2)/10
            # answers_href_list = answers_href_list_head
            args_list = [( answers_href_list[i],answers_chrome_port[i],width*i,0,width,self.half_window_height,i,'answers_information.txt') for i in range(len(answers_href_list))]

            with ThreadPoolExecutor(max_workers=len(answers_href_list)) as executor:
                executor.map(self.para_answers, *zip(*args_list))
                
                
            # answers_href_list = answers_href_list_tail
            # args_list = [( answers_href_list[i],answers_chrome_port[i],width*i,0,width,self.half_window_height,i,'answers_information.txt') for i in range(5,5+len(answers_href_list))]

            # with ThreadPoolExecutor(max_workers=len(answers_href_list)) as executor:
            #     executor.map(self.para_answers, *zip(*args_list))

    def para_answers(self,answers_href,answers_chrome,pos_x,pos_y,width,height,answer_index,output_filename):
        
        driver = self.get_driver(answers_href,answers_chrome,pos_x,pos_y,width,height)
        User_ZhiHu(driver).answers_information_collection(answer_index,output_filename)
        
    def asks(self):
        driver = self.get_driver(self.home_page_url,chrome_ports[4],self.half_window_width,self.half_window_height,self.half_window_width,self.half_window_height)
        # driver = self.get_driver(self.home_page_url,chrome_ports[4],self.half_window_width,self.half_window_height,self.half_window_width,self.half_window_height)
        asks_chrome_port = [str(i) for i in range(9243,9253)]
    
        
        asks_href_list,asks_information = User_ZhiHu(driver).user_questions_information_collection()
        
        driver.close()
        if len(asks_href_list) > 0 :
        # asks_href_list_head = asks_href_list[:5]
        # asks_href_list_tail = asks_href_list[5:10]
        # asks_href_list = asks_href_list_head
        # sleep(10000)
            width = (self.half_window_width*2)/10
            args_list = [( asks_href_list[i],asks_chrome_port[i],width*i,self.half_window_height,width,self.half_window_height,asks_information,i,asks_information[i]['回答数'],'asks_information.txt') for i in range(len(asks_href_list))]
        
            with ThreadPoolExecutor(max_workers=len(asks_href_list)) as executor:
                executor.map(self.para_asks, *zip(*args_list))
            
        # asks_href_list = asks_href_list_tail
        # # sleep(10000)
        # args_list = [( asks_href_list[i],asks_chrome_port[i],width*i,self.half_window_height,width,self.half_window_height,asks_information,i,asks_information[i]['回答数'],'asks_information.txt') for i in range(5,5+len(asks_href_list))]
        # with ThreadPoolExecutor(max_workers=len(asks_href_list)) as executor:
        #     executor.map(self.para_asks, *zip(*args_list))

        # driver.close()
        # asks_information[ask_index]['回答数'] = answers_count
        # self.asks_information_collection(asks_information,ask_index,answers_count,output_filename)
    def para_asks(self,asks_href,asks_chrome,pos_x,pos_y,width,height,asks_information,ask_index,answers_count,output_filename):
        driver = self.get_driver(asks_href,asks_chrome,pos_x,pos_y,width,height)
        User_ZhiHu(driver).asks_information_collection(asks_information,ask_index,answers_count,output_filename)

if __name__ == '__main__':

    WeiBo_usr = '3247842625@qq.com'
    WeiBo_pwd = 'irontys'

    Login = Login_ZhiHu('https://zhihu.com',chrome_ports[0])
    # 此处有个问题，就是远程cmd打开的chrome
    Login.third_party_WeiBo_login(WeiBo_usr,WeiBo_pwd)
    Login.sign_cookie()
    sleep(100000)
    # Login.cookie_login()
    driver_ZhiHu = Login.prepared_drive()
    # 孟冬石榴
    username_ZhiHu = '喜欢阿尔帕西诺'
    User = User_ZhiHu(driver_ZhiHu)
    
    # 查找过程中浏览器界面貌似必须处于最上方显示（必须看着他加载），不然会报错，找不到某XPATH，不知道为什么
    # 通过设置option为headless + 设置窗口分辨率解决
    home_page_url = User.goto_user_home_page(username_ZhiHu)

    output_filenames = ['basic_information.txt','active_followers_information.txt','passive_followers_information.txt','answers_information.txt','asks_information.txt']
    for output_filename in output_filenames:
        with open(output_filename, "w", encoding='utf-8') as in_file:
            in_file.write('')
    User.user_basic_information_collection('basic_information.txt')

    do_parallel =  parallel(home_page_url)
    # do_parallel.half_window_width = driver_ZhiHu.get_window_size()["width"] //2
    # do_parallel.half_window_height = driver_ZhiHu.get_window_size()["height"]//2
    # print(driver_ZhiHu.get_window_size()["width"],driver_ZhiHu.get_window_size()["height"])
    # t0 = threading.Thread(target= User.user_basic_information_collection,args=('basic_information.txt',))
    driver_ZhiHu.close()
    functions = [do_parallel.follower,do_parallel.following,do_parallel.answers,do_parallel.asks]
    # functions = [do_parallel.asks]
    # for functions in functions:

    threads = [threading.Thread(target=function,args=()) for function in functions]
    # 启动四个线程
    start = [thread.start() for thread in threads]
    
    # 等待四个线程结束
    join = [thread.join() for thread in threads]

    
    
    
    output_filenames = ['basic_information.txt','active_followers_information.txt','passive_followers_information.txt','answers_information.txt','asks_information.txt']
    with open('./User_Information.txt','w', encoding='utf-8') as final_file:
        for output_filename in output_filenames:
            with open(output_filename, "r", encoding='utf-8') as in_file:
                content = in_file.read()
                # 将内容写入到新的txt文件中，并换行
                final_file.write(content + "\n")
    print('Done')
    