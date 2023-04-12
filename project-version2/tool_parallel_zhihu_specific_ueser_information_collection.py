# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor
import time,sys

# 之后会用做多线程加速的端口号列表，可修改，
# 注：不要使用range(9243,9253)的端口号，
# 后于多线程加速时会用到
chrome_ports = ['9222','9223','9224','9225','9226']
# 设置信息搜集的浏览器界面是否可见
# 若不可见，visible = 0
# 不可见的实现方法是
# 把打开的浏览器窗口的position
# 设置到屏幕以外的区域，不同电脑
# 根据分辨率不同可能需要修改
# window_position变量中的x的值
visible = 0
if visible:
    window_position = {'x':'0','y':'0'}
    
else:
    window_position = {'x':'4000','y':'0'}

specific_user_info = {'basic_info':None,'followers_info':None,'followings_info':None,'answers_info':None,'asks_info':None}
class Login_ZhiHu():
    
    def __init__(self,url,chrome_port,is_visible):
        self.visible = is_visible
        self.window_position = window_position
        self.window_width = 1936 
        self.window_height = 1056
        self.set_visible()
        cmd = 'chrome.exe --remote-debugging-port='+ chrome_port + ' --window-position='+ self.window_position['x'] + ',' + self.window_position['y'] + ' --user-data-dir=\"E:\Iront\StudyItems\TC\Crouses\ContentSecurity\EX1_ZhiHu_Info_collention\project\chrome_user_data_'+ chrome_port + '\"'
        os.popen(cmd)
        # 连接chrome浏览器，否则会出现知乎搜索功能不可用，某用户的回答不可见
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:" + chrome_port)  #  前面设置的端口号
        options.add_argument("--headless") # 不清楚这个option是否有用
        self.url = url
        self.driver = webdriver.Chrome(options=options)
        self.login_cookie = None
        self.driver.set_window_position(int(self.window_position['x']), int(self.window_position['y']))
    
    def set_visible(self):

        if self.visible:
            self.window_position = {'x':'0','y':'0'}
            
        else:
            self.window_position = {'x':'4000','y':'0'}
    
    def third_party_login(self,mode = 1,username = None,password = None,is_online_search = 1):
        # print(">>>>>",type(mode))
        if mode == 0:
            self.third_party_login_WeiBo_1(username,password,is_online_search)
        elif mode == 1:
            self.third_party_login_WeiBo_2(is_online_search)
        elif mode == 2:
            self.third_party_login_QQ_1(is_online_search)
        elif mode == 3:
            self.third_party_login_QQ_2(is_online_search)
        elif mode == 4:
            self.third_party_login_WeChat(is_online_search)
        else :
            self.third_party_login_WeiBo_2(is_online_search)
    
    def third_party_login_WeChat(self,is_online_search):
        self.driver.get(self.url,)

        # self.driver.maximize_window()
        
        # 这样可以做到隐藏窗口，16是分界线，否则微博登录的弹窗弹不出来
        if self.visible:
            do_nothing = 1
        else:
            self.driver.set_window_position(self.window_width-16.0001, 0)
        # 让窗口不可见
        if is_online_search:
            self.driver.set_window_size(self.window_width/2, self.window_height/100)
        else:
            self.driver.set_window_size(self.window_width/10,self.window_height/4)
        # 点击通过微博登录
        while True:
            try:
                self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[3]/span/button[1]').click()                            
            
                break  # if no error occurred, exit the loop
            except:
                continue  # if an error occurred, continue to the next iteration of the loop
        
        # set window position以后要sleep一下才能稳定的找到xpath
        # 操作刚打开的微博第三方登陆界面
        all_handles = self.driver.window_handles
        
        # 稍后从第三方登录页面切换回知乎主页会用到
        ZhiHu_Handle = all_handles[0] 
        # 切换到微博登陆界面句柄
        WeChat_Handle = all_handles[1] 
        
        
        self.driver.switch_to.window(WeChat_Handle)
        self.driver.maximize_window()
        self.driver.switch_to.window(ZhiHu_Handle)
    def third_party_login_QQ_1(self,is_online_search):
        self.driver.get(self.url,)

        # self.driver.maximize_window()
        
        # 这样可以做到隐藏窗口，16是分界线，否则微博登录的弹窗弹不出来
        if self.visible:
            do_nothing = 1
        else:
            self.driver.set_window_position(self.window_width-16.0001, 0)
        # 让窗口不可见
        if is_online_search:
            self.driver.set_window_size(self.window_width/2, self.window_height/100)
        else:
            self.driver.set_window_size(self.window_width/10,self.window_height/4)
        # 点击通过微博登录
        while True:
            try:
                self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[3]/span/button[2]').click()                            
            
                break  # if no error occurred, exit the loop
            except:
                continue  # if an error occurred, continue to the next iteration of the loop
        
        # set window position以后要sleep一下才能稳定的找到xpath
        # 操作刚打开的微博第三方登陆界面
        all_handles = self.driver.window_handles
        
        # 稍后从第三方登录页面切换回知乎主页会用到
        ZhiHu_Handle = all_handles[0] 
        # 切换到微博登陆界面句柄
        QQ_Handle = all_handles[1] 
        
        
        self.driver.switch_to.window(QQ_Handle)
        self.driver.maximize_window()
        self.driver.switch_to.window(ZhiHu_Handle)
        
    def third_party_login_QQ_2(self,is_online_search):
        self.driver.get(self.url)

        # self.driver.maximize_window()
        
        # 这样可以做到隐藏窗口，16是分界线，否则微博登录的弹窗弹不出来
        if self.visible:
            do_nothing = 1
        else:
            self.driver.set_window_position(self.window_width-16.0001, 0)
        # 让窗口不可见
        if is_online_search:
            self.driver.set_window_size(self.window_width/2, self.window_height/100)
        else:
            self.driver.set_window_size(self.window_width/10,self.window_height/4)
        # 点击通过微博登录
        while True:
            try:
                self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[3]/span/button[2]').click()                            
            # 操作刚打开的微博第三方登陆界面
            
                break  # if no error occurred, exit the loop
            except:
                continue  # if an error occurred, continue to the next iteration of the loop
        
        # self.driver.maximize_window()
        # sleep(3)
        all_handles = self.driver.window_handles
            
        # 稍后从第三方登录页面切换回知乎主页会用到
        ZhiHu_Handle = all_handles[0] 
        # 切换到微博登陆界面句柄
        QQ_Handle = all_handles[1] 
        
        self.driver.switch_to.window(QQ_Handle)
        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.ID, "ptlogin_iframe")))
            # /html/body/div[1]/div[4]/div[8]/div/a[1]/span[4]
        iframe = self.driver.find_element(By.ID, "ptlogin_iframe")
        # set window position以后要sleep一下才能稳定的找到xpath
        self.driver.switch_to.frame(iframe)
        
        self.driver.find_element(By.XPATH,'//div[@id="qlogin_list"]/a[1]').click()
        self.driver.switch_to.window(ZhiHu_Handle)                           
       
    
    def third_party_login_WeiBo_2(self,is_online_search):
        self.driver.get(self.url)

        # self.driver.maximize_window()
        
        # 这样可以做到隐藏窗口，16是分界线，否则微博登录的弹窗弹不出来
        if self.visible:
            do_nothing = 1
        else:
            self.driver.set_window_position(self.window_width-16.0001, 0)
        # 让窗口不可见
        if is_online_search:
            self.driver.set_window_size(self.window_width/2, self.window_height/100)
        else:
            self.driver.set_window_size(self.window_width/10,self.window_height/4)
        # 点击通过微博登录
        while True:
            try:
                self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[3]/span/button[3]').click()                            
            
                break  # if no error occurred, exit the loop
            except:
                continue  # if an error occurred, continue to the next iteration of the loop

        # set window position以后要sleep一下才能稳定的找到xpath
        # 操作刚打开的微博第三方登陆界面
        all_handles = self.driver.window_handles
        
        # 稍后从第三方登录页面切换回知乎主页会用到
        ZhiHu_Handle = all_handles[0] 
        # 切换到微博登陆界面句柄
        WeiBo_Handle = all_handles[1] 
        self.driver.switch_to.window(WeiBo_Handle)
        self.driver.maximize_window()
        self.driver.switch_to.window(ZhiHu_Handle)
        
    def third_party_login_WeiBo_1(self,usr,pwd,is_online_search):
        self.driver.get(self.url)

        # self.driver.maximize_window()
        
        # 这样可以做到隐藏窗口，16是分界线，否则微博登录的弹窗弹不出来
        if self.visible:
            do_nothing = 1
        else:
            self.driver.set_window_position(self.window_width-16.0001, 0)
        # 让窗口不可见
        if is_online_search:
            self.driver.set_window_size(self.window_width/2, self.window_height/100)
        else:
            self.driver.set_window_size(self.window_width/10,self.window_height/4)
        # 点击通过微博登录
        while True:
            try:
                self.driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[3]/span/button[3]').click()                            
            
                break  # if no error occurred, exit the loop
            except:
                continue  # if an error occurred, continue to the next iteration of the loop

        # set window position以后要sleep一下才能稳定的找到xpath
            # 操作刚打开的微博第三方登陆界面
        all_handles = self.driver.window_handles
        
        # 稍后从第三方登录页面切换回知乎主页会用到
        ZhiHu_Handle = all_handles[0] 
        # 切换到微博登陆界面句柄
        WeiBo_Handle = all_handles[1] 
        
        
        self.driver.switch_to.window(WeiBo_Handle)
        self.driver.maximize_window()
        # 切换到输入用户名和密码的界面
       
        while True:
            try:
                self.driver.find_element(By.XPATH,'//*[@id="jump_login_url_a"]').click()
                break
            except:
                continue  
        
        # 有时浏览器保存的cookie没有清空
        # 将浏览器设置中的隐私设置设置为每次关闭浏览器是清空cookie
        try:
            self.driver.find_element(By.XPATH,'//*[@node-type="submit" and @title="允许" and @action-type="submit"]').click()
            self.driver.switch_to.window(ZhiHu_Handle)
            return
        except:
            do_nothing = 1
        
        # 等待加载页面，下同
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        except:
            print("Login Failed! Check u network statue")
        # 输入微博账号和密码
        # sleep(3)
        self.driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(usr)
        self.driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(pwd)   

        # while True:
        #     try:
        #         self.driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(usr)
        #         self.driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(pwd)   
        #         break
        #     except:
        #         continue
        # 登录
        self.driver.find_element(By.XPATH,'//*[@id="vForm"]/div[2]/div/ul/li[7]/div[1]/input').click()  
        try:                          
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="message_sms_login"]')))
        except:
            print("Login Failed! Check u network statue")
        # 点击扫码验证
        self.driver.find_element(By.XPATH,'//*[@id="qrCodeCheck"]').click()
        # find 验证码的链接
        img_src = self.driver.find_element(By.XPATH,'//*[@id="qrcode"]').get_attribute("src")
        # src = img_src.get_attribute("src")
        # print(img_src)
        # url = "http://127.0.0.1/index?img_src="+img_src
        # self.driver.set_window_position(int(self.window_position['x']), int(self.window_position['y']))
        # url = "http://127.0.0.1:5000/index"
        # data = {'img_src' : img_src}
        # # requests.post(url,img_src)
        # requests.post(url,data=data)
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="outer"]/div/div[2]/div/div[2]/div[2]/p/a[1]')))
        except:
            print("Login Failed! Check u network statue")
        # 确认授权
        # url = "http://127.0.0.1:5000/index"
        # data = {'img_src' : img_src}
        # # requests.post(url,img_src)
        # requests.post(url,data=data)
        self.driver.find_element(By.XPATH,'//*[@id="outer"]/div/div[2]/div/div[2]/div[2]/p/a[1]').click()
        self.driver.switch_to.window(ZhiHu_Handle)
        
    # 将cookie存储起来到指定文件
    def sign_cookie(self):
        
        try:
            WebDriverWait(self.driver,10000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Popover1-toggle"]')))
        except:
            print("Waiting for you to scan for a long time -_-")
        dictCookies = self.driver.get_cookies() # 获取list的cookies
        jsonCookies = json.dumps(dictCookies) # 转换成字符串保存
        
        with open('ZhiHu_cookies.txt', 'w') as f:
            f.write(jsonCookies)
            print('cookies保存成功！')
        return  jsonCookies
    # 为下一步多线程操作做准备，也可用作调试，即可避免每次调试重新扫码登录
    def cookie_login(self):
        self.driver.get(self.url)
        # 还需要在开头加上：# -*- coding: utf-8 -*-，否则open会出问题
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
    # 为下一个用于搜集指定用户信息的类：User_ZhiHu传递driver
    def prepared_drive(self):
        return self.driver
    def close_current_drive(self):
        print("close")
        self.driver.close()
    
class User_ZhiHu():
    
    def __init__(self,driver):
        #　继承Login_ZhiHu的driver
        self.driver = driver
        # 下述参数是为实现定时检测用户信息更新情况而设置的
        # 第零个元素为用户asks/answers的总数
        self.answers_edit_statue = ['']*10
        self.asks_edit_statue = ['']*10
        self.valid_asks_count = 0
        self.valid_answers_count = 0
    
    # 目的是将driver切换到“目标”用户（username）的主页，返回值获取url是为了后续多线程加速而设计的
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
        sleep(0.5)
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
    
    # 最终的信息存储在 user_information = {}这个字典中，界面没有显示的个人信息视为用户未设置，其值设为'Not Found'
    def user_basic_information_collection(self):
        user_information = {}
        try:
            WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[1]')))
        except:
            print("Search Failed! Check u network statue")
        # xpath value is not //*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[1]/text()
        
        user_information['头像'] = self.driver.find_element(By.XPATH,'//img[@class="Avatar Avatar--large UserAvatar-inner"]').get_attribute('src')
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
            WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/div/div')))
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
        specific_user_info['basic_info'] = user_information
        
    # 关注的人和粉丝
    # followers_information存储关注的人或粉丝所有信息，是个字典数组，有效则"isEmpty"= 0，否则为1
    def user_relationship_information_collection(self,follower_XPATH,followings_or_followers):
        # 点击关注按钮（ps：这里如果是需要搜集“关注该用户的人“，是不需要进行下面这条语句的，但是执行搜索“该用户关注的人”的信息时，又是只需要下面这条语句，而不需要下下条语句，但是为了调用接口函数的统一性，这两条语句都写在这里）
        self.driver.find_element(By.XPATH,'//*[@id="ProfileMain"]/div[1]/ul/li[9]/a').click()
        # 点击“该用户关注的人”或者“关注该用户的人”按钮
        self.driver.find_element(By.XPATH,follower_XPATH).click()
        # 点击后若不刷新界面，受反爬机制的的影响，页面不能正常显示，此处通过刷新页面的方法绕过反扒机制
        self.driver.refresh()
        # 分类分别搜集关注着和粉丝信息的情况，并统计关注着和粉丝的总数
        followings_or_followers_count = self.driver.find_elements(By.XPATH,'//strong[@class="NumberBoard-itemValue"]')
        if followings_or_followers == 'followings':
            followers_count = int(followings_or_followers_count[0].get_attribute("title"))
        else:
            followers_count = int(followings_or_followers_count[1].get_attribute("title"))
        
        # 设置搜集信息是的有效采集信息条数
        # 如果粉丝或关注的人数量多于10，取10
        # 否则取相应数目
        valid_followers_count = min(followers_count,10)
        
        # followers_information存储关注的人或粉丝所有信息，是个字典数组，有效则"isEmpty"= 0，否则为1
        followers_information = [{"isEmpty": 0} for i in range(10)]
        if valid_followers_count == 0:
            followers_information = [{"isEmpty": 1} for i in range(10)]
        else: 
            for i in range(valid_followers_count,10):
                followers_information[i]['isEmpty'] = 1
            follower_information_tag_list = ['头像','用户昵称','链接地址','回答数','文章数','关注者数']
            try:
                WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@class="List-item"]')))
            except:
                print("Search Failed! Check u network statue")
            # 定位一个用户信息栏
            list_items = self.driver.find_elements(By.XPATH,'//div[@class="List-item"]')
            # 从这里开始我才开始了解xpath的细节，而不是再复制源码中的xpath值..
            
            index = 0
            for list_item in list_items[0:valid_followers_count]:
                # name和链接地址在同一个a标签中
                followers_information[index]['头像'] = list_item.find_element(By.XPATH,'.//img[@class="Avatar UserLink-avatar css-ymspo8"]').get_attribute("src")
                follower_href_and_name = list_item.find_element(By.XPATH,'.//span[@class="UserLink"]/div/a')
                followers_information[index]['用户昵称'] = follower_href_and_name.text
                followers_information[index]['链接地址'] = follower_href_and_name.get_attribute("href")
                # 是当前follower的[{'回答':'62' },{'文章':'1'},{'关注者':'151'}]信息
                followers_answers_articles_followers = list_item.find_elements(By.XPATH,'.//div[@class="ContentItem-status"]/span')            
                tag_list = ['回答','文章','关注者']
                for tag in tag_list:
                    followers_information[index][tag+'数'] = '0'
                    for follower_answers_articles_followers in followers_answers_articles_followers:
                        if tag == follower_answers_articles_followers.text.split(' ')[1]:
                            followers_information[index][tag+'数'] = follower_answers_articles_followers.text.split(' ')[0]
                index += 1        
        
       
        if followings_or_followers == 'followings':
            specific_user_info['followings_info'] = followers_information
        else:
                specific_user_info['followers_info'] = followers_information
 
    def user_answers_information_collection(self):
        
        # 处理回答数为0的特殊情况：
        #   
        answers_information = [{"isEmpty": 1} for i in range(10)]
        answers_tag_in_this_list = self.driver.find_elements(By.XPATH, '//a[@class="Tabs-link"]')
        for answers_tag in answers_tag_in_this_list:
            if answers_tag.get_attribute("href").split('/')[-1] == 'answers' and answers_tag.find_element(By.XPATH, './/span').text != '':
                answers_tag_clickable = answers_tag
                answers_count = int(answers_tag.find_element(By.XPATH, './/span').text)
                break
        # answers_tag.click()
        self.driver.execute_script("arguments[0].click();", answers_tag_clickable)
        self.driver.refresh()
        valid_answers_count = min(answers_count,10)
        if valid_answers_count == 0:
            print("No Answers!!")
        else:
            # 等待加载出回答
            try:
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="List-item"]')))
            except:
                print("Search Failed! Check u network statue")
            answers_list = self.driver.find_elements(By.XPATH,'//div[@class="List-item" ]')[0:valid_answers_count]
            for i,answer in enumerate(answers_list):
                answers_information[i]['isEmpty'] = 0
                answers_information[i]['回答序号'] = i+1
                buttons = answer.find_elements(By.XPATH,'.//Button[@class="Button ContentItem-action FEfUrdfMIKpQDJDqkjte Button--plain Button--withIcon Button--withLabel fEPKGkUK5jyc4fUuT0QP B46v1Ak6Gj5sL2JTS4PY RuuQ6TOh2cRzJr6WlyQp"]')
                remarks_information = []        
                if buttons[0].text != '添加评论':
                    answers_information[i]['评论次数'] = buttons[0].text.split(' ')[0]
                    # print("---->",answers_information[i]['评论次数'])
                    self.driver.execute_script("arguments[0].click();", buttons[0])
                    # remarks_list = answer.find_elements(By.CLASS_NAME, 'css-1frn93x')
                    # try:
                        # WebDriverWait(answer, 100).until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1frn93x"]/div')))# 这个标签不行
                    # 处理点击出现的 展开其他回复
                    WebDriverWait(answer, 10).until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-194v73m"]')))
                    # except:                                                                            
                    #     print("Search Failed! Check u network statue")
                    # 这里有些糙了，评论并不是按顺序提取的
                    try:
                        more_remarks_buttons = answer.find_elements(By.XPATH,'.//Button[@class="Button Button--secondary Button--grey css-1p04wnp"]')
                        for more_remarks_button in more_remarks_buttons:
                            self.driver.execute_script("arguments[0].click();",  more_remarks_button)
                    except:
                        do_nothing = 1
                    remarks_list = answer.find_elements(By.XPATH,'.//div[@class="css-194v73m"]')  + answer.find_elements(By.XPATH,'.//div[@class="css-8j5fyx"]')
                    for remark_index,remark in enumerate(remarks_list):
                                
                        try:
                            remarker_photo = remark.find_element(By.XPATH,'.//img[@class="Avatar css-1s1htbw"]').get_attribute("src")
                            remarker_href = remark.find_element(By.XPATH,'.//a[@class="css-1rd0h6f"]').get_attribute("href")
                            remarker_id = remark.find_element(By.XPATH,'.//a[@class="css-1rd0h6f"]').get_attribute("href").split('/')[-1]
                            remarker_username = remark.find_element(By.XPATH,'.//a[@class="css-1rd0h6f"]').text
                            remarker_time = remark.find_element(By.XPATH,'.//*[@class="css-12cl38p"]').text
                            remarker_content = remark.find_element(By.XPATH,'.//div[@class="CommentContent css-1ygdre8"]').text
                            if remark.find_element(By.XPATH,'.//Button[@class="Button Button--plain Button--grey Button--withIcon Button--withLabel css-h1yvwn"]').text == '赞':
                                remarker_likes = '0'
                            else:
                                remarker_likes = remark.find_element(By.XPATH,'.//Button[@class="Button Button--plain Button--grey Button--withIcon Button--withLabel css-h1yvwn"]').text
                            remarker_info = {"isEmpty":0,'评论序号':remark_index+1,"评论者昵称":remarker_username,"评论者主页":remarker_href,"评论者ID":remarker_id,"评论时间":remarker_time,"评论内容":remarker_content,"点赞次数": remarker_likes,'头像':remarker_photo}
                            if remarker_info not in remarks_information:
                                remarks_information.append(remarker_info)
                        except:
                            do_nothing = 1
                    # 处理点击出现的 展开其他回复
                    # try:
                    #     more_remarks_buttons = answer.find_elements(By.XPATH,'.//Button[@class="Button Button--secondary Button--grey css-1p04wnp"]')
                        
                    #     for more_remarks_button in more_remarks_buttons:
                    #         self.driver.execute_script("arguments[0].click();",  more_remarks_button)  
                    #         try:
                    #             # WebDriverWait(answer, 100).until(EC.presence_of_element_located((By.XPATH, './/div[@class="css-1frn93x"]/div')))# 这个标签不行
                    #             WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-weau4n"]/div/div/div[2]')))
                    #         except:
                    #             print("Search Failed! Check u network statue")
                    #         remarks_list = self.driver.find_elements(By.XPATH,'//div[@class="css-weau4n"]/div/div/div[2]')
                    #         for remark_index,remark in enumerate(remarks_list):
                    #             remarker_photo = remark.find_element(By.XPATH,'.//img[@class="Avatar css-1s1htbw"]').get_attribute("src")
                    #             remarker_href = remark.find_element(By.XPATH,'.//a[@class="css-1rd0h6f"]').get_attribute("href")
                    #             remarker_id = remarker_href.split('/')[-1]
                                
                    #             remarker_username = remark.find_element(By.XPATH,'.//a[@class="css-1rd0h6f"]').text
                    #             remarker_time = remark.find_element(By.XPATH,'.//span[@class="css-12cl38p"]').text
                    #             remarker_content = remark.find_element(By.XPATH,'.//div[@class="CommentContent css-1ygdre8"]').text
                    #             if remark.find_element(By.XPATH,'.//Button[@class="Button Button--plain Button--grey Button--withIcon Button--withLabel css-h1yvwn"]').text == '赞':                                                 
                    #                 remarker_likes = '0'
                    #             else:
                    #                 remarker_likes = remark.find_element(By.XPATH,'.//Button[@class="Button Button--plain Button--grey Button--withIcon Button--withLabel css-h1yvwn"]').text
                    #             remarker_info = {"isEmpty":0,'评论序号':remark_index+1,"评论者昵称":remarker_username,"评论者主页":remarker_href,"评论者ID":remarker_id,"评论时间":remarker_time,"评论内容":remarker_content,"点赞次数": remarker_likes,'头像':remarker_photo}
                    #             # 在弹窗中，有的内容都一样，但是评论日期不一样，算作不一样
                    #             if remarker_info not in remarks_information:
                    #                 remarks_information.append(remarker_info)
                    #         self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH,'.//Button[@aria-label="关闭"]'))
                    # except:
                    #     do_noting = 1         
                    fold_remarks =  answer.find_element(By.XPATH,'.//Button[@class="Button ContentItem-action FEfUrdfMIKpQDJDqkjte Button--plain Button--withIcon Button--withLabel fEPKGkUK5jyc4fUuT0QP B46v1Ak6Gj5sL2JTS4PY RuuQ6TOh2cRzJr6WlyQp"]').text
                    if fold_remarks == '收起评论':
                        self.driver.execute_script("arguments[0].click();", buttons[0])
                else:
                    answers_information[i]['评论次数'] = '0'
                    
                # print(remarks_information)
                # 处理回答者的回答信息
                try:
                    button = answer.find_element(By.XPATH,'.//Button[@class="Button ContentItem-more FEfUrdfMIKpQDJDqkjte Button--plain fEPKGkUK5jyc4fUuT0QP"]')
                    self.driver.execute_script("arguments[0].click();", button)
                except:
                    do_nothing = 1
                # try:# 这里不能加and
                # 这个隐式等待语句不好使
                WebDriverWait(answer, 100).until(EC.presence_of_element_located((By.XPATH, './/span[@class="RichText ztext CopyrightRichText-richText css-1g0fqss"]')))
                answer_title = answer.find_element(By.XPATH,'.//a[@data-za-detail-view-element_name="Title"]').text
                # 这里好像是必须显式等待，等待时间不确定，如果报错，就设置久一点
                # sleep(0.1)
                while True:
                    try:
                        answer_content =  answer.find_element(By.XPATH,'.//span[@class="RichText ztext CopyrightRichText-richText css-1g0fqss"]').text
                        break                    
                    except:
                        continue
                # answer_content =  answer.find_element(By.XPATH,'.//span[@class="RichText ztext CopyrightRichText-richText css-1g0fqss"]').text
                answer_time = answer.find_element(By.XPATH,'.//div[@class="ContentItem-time"]/a/span').text.split(' ')[1] +"-"+ answer.find_element(By.XPATH,'.//div[@class="ContentItem-time"]/a/span').text.split(' ')[-1]
                answer_likes = answer.find_element(By.XPATH,'.//Button[@class="Button VoteButton VoteButton--up FEfUrdfMIKpQDJDqkjte"]').get_attribute("aria-label").split(' ')[1]
                
                                                                    
                # answer.find_element(By.XPATH,'.//span[@class="RichContent-collapsedText"]').click()
                answers_information[i]['所回答的问题'] = answer_title
                answers_information[i]['回答内容'] = answer_content
                answers_information[i]['回答时间'] = answer_time
                answers_information[i]["点赞次数"] = answer_likes
                answers_information[i]["评论信息"] = remarks_information[0:10]
                # print(answers_information[i])
        old_list = answers_information
        answers_information = [answer_information for answer_information in old_list if not all('isEmpy'==0 for empty in answer_information.values())]
                     
        specific_user_info['answers_info'] = answers_information
                
    def parallel_asks_information_collection(self,asks_information,index,answers_count):
        try:
            # 依据关注问题按钮问题标题是否出现判断页面加载完全（感觉其实是有问题的）
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//h1[@class="QuestionHeader-title"]')))
        except:
            print("Search Failed! Check u network statue")
            
        # 可能会有点击阅读全文的按钮
        try:
            self.driver.find_element(By.XPATH,'//Button[@class="Button QuestionRichText-more FEfUrdfMIKpQDJDqkjte Button--plain fEPKGkUK5jyc4fUuT0QP"]').click()
        except:
            do_nothing = 1
            
        # 排除视频回答
        try:
            ask_content = self.driver.find_element(By.XPATH,'//span[@class="RichText ztext css-1g0fqss"]').text
        except:
            ask_content = ''
        asks_information[index]['提问序号'] = index+1    
        ask_title = [title.text for title in self.driver.find_elements(By.XPATH,'//h1[@class="QuestionHeader-title"]') if title.text != ''][0]
        asks_information[index]['提问标题'] =   ask_title 
        asks_information[index]['提问内容'] =   ask_content 
        asks_tags = ['提问时间','回答数','关注人数','提问标题','提问内容','提问序号'] 
        
        answers_count = int(answers_count)
        valid_answers_count = min(answers_count,10)
        ask_answers_information = [{"isEmpty": 0} for i in range(valid_answers_count)]
        if valid_answers_count > 0:
            try:
                # 依据关注问题按钮问题标题是否出现判断页面加载完全（感觉其实是有问题的）
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="List-item" and @tabindex="0"]')))
            except:
                print("Search Failed! Check u network statue")
             
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
                
            ask_answer_tags = ['回答序号','回答者ID','回答者头像','回答者昵称','回答时间','回答内容','点赞次数']
            
            for ask_answers_index,ask_answer in enumerate(ask_answers[0:valid_answers_count]):
                ask_answers_information[ask_answers_index]['回答序号'] = ask_answers_index
                ask_answers_information[ask_answers_index]['回答者头像'] = ask_answer.find_element(By.XPATH,'.//img[@class="Avatar AuthorInfo-avatar css-1oqflzh"]').get_attribute("src")
                ask_answers_information[ask_answers_index]['回答者主页'] = ask_answer.find_element(By.XPATH,'.//div[@class="css-1gomreu"]/a').get_attribute("href")
                ask_answers_information[ask_answers_index]['回答者ID'] = ask_answer.find_element(By.XPATH,'.//div[@class="css-1gomreu"]/a').get_attribute("href").split('/')[-1]
                ask_answers_information[ask_answers_index]['回答者昵称'] = ask_answer.find_elements(By.XPATH,'.//div[@class="css-1gomreu"]/a')[1].text
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
        
        asks_information[index]['回答信息'] = ask_answers_information
        self.driver.close()
      
    def parallel_user_asks_information_collection(self):   
        asks_tag_in_this_list = self.driver.find_elements(By.XPATH, '//a[@class="Tabs-link"]')
        # 这里会有个空字符串是我妹能理解的
        for asks_tag in asks_tag_in_this_list:
            if asks_tag.get_attribute("href").split('/')[-1] == 'asks' and asks_tag.find_element(By.XPATH, './/span').text != '':
                asks_tag_clickable = asks_tag
                asks_count = int(asks_tag.find_element(By.XPATH, './/span').text)
                break
        self.driver.execute_script("arguments[0].click();", asks_tag_clickable)
        # asks_tag_clickable.click() # 这个不如上面这个优，有时候点不到
        self.driver.refresh()
        

        valid_asks_count = min(asks_count,10)
        asks_information = [{"isEmpty": 0} for i in range(valid_asks_count)]
        if valid_asks_count == 0:
            asks_href_list = []
        else:
            # 等待加载出回答
            try:
                WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//div[@class="List-item"]')))
            except:
                print("Search Failed! Check u network statue")
            # 获取当前页面所有回答的element列表
            asks_list_items = self.driver.find_elements(By.XPATH, '//div[@class="List-item"]')
            asks_href_list = [ask_list_item.find_element(By.XPATH, './/div[@class="QuestionItem-title"]/a').get_attribute("href") for ask_list_item in asks_list_items[0:valid_asks_count]]
            ask_index = 0
            for asks_list_item in asks_list_items[0:valid_asks_count]:
                asks_information[ask_index]['isEmpty'] = 0
                asks_time_answers_followers =  asks_list_item.find_elements(By.XPATH,'.//span[@class="ContentItem-statusItem"]')
                asks_information[ask_index]['提问时间'] = asks_time_answers_followers[0].text
                answers_count = asks_time_answers_followers[1].text.split(' ')[0]
                asks_information[ask_index]['回答数'] = answers_count
                asks_information[ask_index]['关注人数'] = asks_time_answers_followers[2].text.split(' ')[0]
                ask_index += 1
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
        self.half_window_width = 1936 //2
        self.half_window_height = 1056//2
        
    def get_driver(self,page_url,chrome_port,position_x,position_y,width,height):
        
        Login_user_home_page = Login_ZhiHu(page_url,chrome_port,visible)
        Login_user_home_page.cookie_login()
        Login_user_home_page_driver = Login_user_home_page.prepared_drive()
        Login_user_home_page_driver.set_window_position(self.half_window_width*2-16.5, position_y)
        Login_user_home_page_driver.set_window_size(width, height)
        
        return Login_user_home_page_driver
       
    def asks(self):
        print("start")
        asks_information = []
        driver = self.get_driver(self.home_page_url,chrome_ports[4],self.half_window_width,self.half_window_height,self.half_window_width,self.half_window_height)
        # driver = self.get_driver(self.home_page_url,chrome_ports[4],self.half_window_width,self.half_window_height,self.half_window_width,self.half_window_height)
        asks_chrome_port = [str(i) for i in range(9243,9253)]
        asks_href_list,asks_information = User_ZhiHu(driver).parallel_user_asks_information_collection()
        driver.close()
        if len(asks_href_list) > 0 :
            width = (self.half_window_width*2)/10
            args_list = [( asks_href_list[i],asks_chrome_port[i],width*i,self.half_window_height,width,self.half_window_height,asks_information,i,asks_information[i]['回答数']) for i in range(len(asks_href_list))]
            with ThreadPoolExecutor(max_workers=len(asks_href_list)) as executor:
                executor.map(self.para_asks, *zip(*args_list))
        specific_user_info['asks_info'] = asks_information
        
    def para_asks(self,asks_href,asks_chrome,pos_x,pos_y,width,height,asks_information,ask_index,answers_count):
        driver = self.get_driver(asks_href,asks_chrome,pos_x,pos_y,width,height)
        User_ZhiHu(driver).parallel_asks_information_collection(asks_information,ask_index,answers_count)

# def get_specific_user_info(login_mode = 4,login_name = '3247842625@qq.com',login_password = 'irontys',specific_user_name='孟冬石榴',use_cookie = 0,visible = 1):
def get_specific_user_info(login_mode,login_name,login_password,specific_user_name,use_cookie,visible):
    # mode=1->wei bo login
    
    start_time = time.time()
    global window_position
    if visible:
        window_position = {'x':'0','y':'0'}
        
    else:
        window_position = {'x':'4000','y':'0'}
    login_url = 'https://www.zhihu.com'
    Login = Login_ZhiHu(login_url,chrome_ports[3],visible)
    
    # 由于直接账号密码登录会被识别出来使用自动化工具，使用第三方登录来绕过反爬
    if not use_cookie:
        # Login.third_party_login_WeiBo_1(login_name,login_password)
        Login.third_party_login(login_mode,username=login_name,password=login_password,is_online_search=0)
        # 将登录后的得到的cookie保存下来，以便后续再次登录使用
        Login.sign_cookie()
    print("?")
    Login.cookie_login()
    driver_ZhiHu = Login.prepared_drive()
    User = User_ZhiHu(driver_ZhiHu)
    
    
    home_page_url = User.goto_user_home_page(specific_user_name)
    # 创建子线程，搜集用户的提问信息，之所以创建这个线程来单独处理用户的提问信息
    # 是因为用户的提问信息需要打开新页面才能获取一些必要的新信息
    # 打开页面的过程比较慢,而搜集用户的提问信息所需要的时间,与所有的其他信息搜集所用的时间
    # 大致相当,所以,设置两个线程,并行处理用户的其他信息的搜集工作和用户的提问信息搜集工作
    # 启动第二个线程处理用户的提问信息
    thread_asks_information = threading.Thread(target=parallel(home_page_url).asks)
    thread_asks_information.start()
    # 搜集基本信息
    User.user_basic_information_collection()
    # 搜集关注的人的信息
    following_XPATH = '//*[@id="Profile-following"]/div[1]/h4/div/a[1]'
    User.user_relationship_information_collection(following_XPATH,'followings')
    # 搜集粉丝的信息 
    follower_XPATH = '//*[@id="Profile-following"]/div[1]/h4/div/a[2]'
    User.user_relationship_information_collection(follower_XPATH,'followers')    
    # 搜集回答信息
    User.user_answers_information_collection()
    driver_ZhiHu.close()
    thread_asks_information.join()
    end_time = time.time()
    print("代码执行时间：{:.2f}秒".format(end_time - start_time))
    return specific_user_info
if __name__ == '__main__':
    print('在程序运行结束之前，不要点击屏幕')
    start_time = time.time()
    
    login_username = '3247842625@qq.com'
    login_password = 'irontys'
    visible = 0
    use_cookie = 0
    login_mode = 4
    # 该用户只是我随机找的，如有冒犯，万分抱歉
    username_ZhiHu = '孟冬石榴'
    for arg in sys.argv[1:]:
        if '--login_mode=' in arg:
            login_mode = int(arg.split("=")[1])
        elif "--visible=" in arg:
            visible = int(arg.split("=")[1])
        elif "--specific_username=" in arg:
            username_ZhiHu = arg.split("=")[1]
        elif "--use_cookie=" in arg:
            use_cookie = int(arg.split("=")[1])
        elif "--login_username=" in arg:
            login_username = arg.split("=")[1]
        elif "--login_password=" in arg:
            login_password = arg.split("=")[1]
    specific_user_info = get_specific_user_info(login_mode,login_username,login_password,username_ZhiHu,use_cookie,visible)
    end_time = time.time()
    print("代码执行时间：{:.2f}秒".format(end_time - start_time))

    for info in specific_user_info:
        print("-->",info)
        print(specific_user_info[info])
        print("-------------------------------------------")
    
    print('Done')
