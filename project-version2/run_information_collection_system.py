# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap
from tool_parallel_zhihu_specific_ueser_information_collection import get_specific_user_info,Login_ZhiHu
import time
import json, os
import threading,requests
import subprocess

class Display():
    def __init__(self):
        self.app=Flask(__name__,template_folder="templates")
        
        self.app.add_url_rule("/", "/index/", methods=["GET","POST"],view_func = self.index)
        self.app.add_url_rule("/index/", methods=["GET","POST"],view_func = self.index)
        self.app.add_url_rule("/login/", methods=["GET","POST"],view_func = self.login)
        self.app.add_url_rule("/successfully_login/", methods=["GET","POST"],view_func = self.successfully_login)
        # self.app.add_url_rule("/logout/", methods=["GET","POST"],view_func = self.logout)
        self.app.add_url_rule("/basic_info/", methods=["GET","POST"],view_func = self.basic_info)
        self.app.add_url_rule("/followings/", methods=["GET","POST"],view_func = self.followings)
        self.app.add_url_rule("/followers/", methods=["GET","POST"],view_func = self.followers)
        self.app.add_url_rule("/answers/", methods=["GET","POST"],view_func = self.answers)
        self.app.add_url_rule("/asks/", methods=["GET","POST"],view_func = self.asks)
        
        self.app.config['SECRET_KEY'] = 'secret_key'
        self.WeiBo_username = '3247842625@qq.com'
        self.WeiBo_password = 'irontys'
        self.specific_username = None
        self.initial_login = 0
        self.img_src = None
        self.cond = None
        self.finish_initial_login = None
        self.specific_user_info_tag = {'basic_info','followers_info','followings_info','answers_info','asks_info'}
        self.specific_user_info_list = None
        self.basic_info_tag_list =  ['用户名','性别','一句话介绍','居住地','所在行业','职业经历','个人简介']
        self.basic_info = None
        self.followings_info_tag_list = ['头像','用户昵称','链接地址','回答数','文章数','关注者数']
        self.followings_info = None
        self.followers_info_tag_list = ['头像','用户昵称','链接地址','回答数','文章数','关注者数']
        self.followers_info = None
        self.current_ask_index = 0
        self.asks_info = None
        self.current_answer_index = 0
        self.answers_info = None
        self.login_mode = 1
        self.login_cookie = None
        self.is_search_done = 0
        self.accessed_answers_page = 0
        self.accessed_asks_page = 0

    def successfully_login(self):
        # self.specific_username = None当访问很多页面时会报错
        if self.specific_username == None and not self.initial_login:
             return redirect(url_for('index'))
        login_mode_tag = ['微博','微博','QQ','QQ','微信']
        return render_template('successfully_login.html'
                               ,login_via = login_mode_tag[self.login_mode]
                               ,is_search_done = self.is_search_done
                               )

    def login(self):
        if request.method == 'POST':
            
            self.login_mode = int(request.form.get('login_mode'))
            if self.login_mode == 0:
                self.login_username = request.form["login_username"]
                self.login_password = request.form["login_password"]
            self.sign_cookie(login_mode = self.login_mode)
            # self.initial_login用于判断是否登录
            # 而如果没有经过login，self.initial_login = 0，当访问其他页面时重定向到index页面，即可避免该问题
            self.initial_login = 1
            return render_template('successfully_login.html')
        # 用于后续判断是否进行过搜索，否则self.specific_username = None当访问很多页面时会报错
        return render_template('login.html'
                                ,is_search_done = self.is_search_done
                                )    
    def get_specific_user_info(self):
            
            self.specific_user_info_list = {}
            self.specific_user_info_list_filename = 'specific_user_info_list.txt'
            if os.path.isfile(self.specific_user_info_list_filename):
            # 文件存在，执行读取操作等
                with open(self.specific_user_info_list_filename, 'r') as f:
                    self.specific_user_info_list = json.load(f)
                    if self.specific_username in self.specific_user_info_list:
                        current_user_info = self.specific_user_info_list[self.specific_username]

            if self.specific_username not in self.specific_user_info_list:
                current_user_info = get_specific_user_info(1,self.WeiBo_username,self.WeiBo_password,self.specific_username,1,0)
                if os.path.isfile(self.specific_user_info_list_filename):
                    with open(self.specific_user_info_list_filename, 'r') as f:
                        self.specific_user_info_list = json.load(f)
                self.specific_user_info_list[self.specific_username] = current_user_info
                with open(self.specific_user_info_list_filename, 'w') as f:
                    json.dump(self.specific_user_info_list, f)
            # print(self.specific_user_info_list[self.specific_username])
            # {'basic_info','followers_info','followings_info','answers_info','asks_info'}
            self.basic_info = current_user_info['basic_info']
            self.followings_info = current_user_info['followings_info']
            self.followers_info = current_user_info['followers_info']
            self.answers_info = current_user_info['answers_info']
            self.asks_info = current_user_info['asks_info']
            self.is_search_done = 1
    def index(self):

        # 处理点击搜索框的搜索用户信息的操作
        if request.method == 'POST':
            self.specific_username = request.form.get('specific_username')
            if self.specific_username != None:
                self.get_specific_user_info()

        # 用于处理更新数据的请求
        if self.specific_username != None:
            if request.method == 'GET':
                if 'update' in request.args:
                    current_user_info = get_specific_user_info(1,self.WeiBo_username,self.WeiBo_password,self.specific_username,1,0)
                    self.specific_user_info_list[self.specific_username] = current_user_info
                    with open(self.specific_user_info_list_filename, 'w') as f:
                        json.dump(self.specific_user_info_list, f)
                    self.basic_info = current_user_info['basic_info']
                    self.followings_info = current_user_info['followings_info']
                    self.followers_info = current_user_info['followers_info']
                    self.answers_info = current_user_info['answers_info']
                    self.asks_info = current_user_info['asks_info']
        # 默认显示的页面
        return render_template('index.html'
                                ,is_search_done = self.is_search_done
                               )
    # 登陆操作中的保存cookie
    def sign_cookie(self,login_mode = 1):
        login_url = 'https://www.zhihu.com'
        Login = Login_ZhiHu(login_url,'9301',0)      
        Login.third_party_login(mode = login_mode,username = self.WeiBo_username, password = self.WeiBo_password)
        self.login_cookie = Login.sign_cookie()
        Login.close_current_drive()
    
    def basic_info(self):
        if self.specific_username == None:
             return redirect(url_for('index'))
        # self.basic_info_tag_list =  ['用户名','性别','一句话介绍','居住地','所在行业','职业经历','个人简介']
        return render_template('basic_info.html'
                            ,basic_info = self.basic_info
                            ,is_search_done = self.is_search_done
                            )
    def followings(self):
        if self.specific_username == None:
             return redirect(url_for('index'))
        # followings_info_tag_list = ['头像','用户昵称','链接地址','回答数','文章数','关注者数']
        return render_template('followings.html'
                            ,followings_info = self.followings_info
                            ,basic_info = self.basic_info
                            ,is_search_done = self.is_search_done   
                            )
        
    def followers(self):
        if self.specific_username == None:
             return redirect(url_for('index'))
        # followings_info_tag_list = ['头像','用户昵称','链接地址','回答数','文章数','关注者数']
        return render_template('followers.html'
                            ,followers_info = self.followers_info
                            ,basic_info = self.basic_info
                            ,is_search_done = self.is_search_done   
                            )
    def answers(self):
        if self.specific_username == None:
             return redirect(url_for('index'))
        if request.method == 'POST':
            self.current_answer_index = int(request.form.get('current_answer_index'))
        return render_template('answers.html'
                            ,answers_info = self.answers_info
                            ,basic_info = self.basic_info
                            ,current_answer_index = self.current_answer_index
                            ,is_search_done = self.is_search_done
                            ,answers_count = len(self.answers_info)
                            )
        
    def asks(self):
        if self.specific_username == None:
             return redirect(url_for('index'))
        if request.method == 'POST':
            self.current_ask_index = int(request.form.get('current_ask_index'))

        return render_template('asks.html'
                            ,asks_info = self.asks_info
                            ,basic_info = self.basic_info
                            ,current_ask_index = self.current_ask_index
                            ,is_search_done = self.is_search_done
                            ,asks_count = len(self.asks_info)
                            )
    def run(self):
        self.app.run(host='127.0.0.1',port=5002,debug=True,threaded=True)

if __name__ == '__main__':
    app = Display()
    subprocess.Popen("python check_update.py", shell=True)
    app.run()
   
    
    