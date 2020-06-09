# -*- coding: utf-8 -*-
from flask import render_template,request,url_for,redirect,flash
from flask_login import login_user,login_required,logout_user,current_user

from watchlist import app,db
from watchlist.models import User,Movie

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST': #判断是否是post请求
        if not current_user.is_authenticated:  #如果当前用户未认证
            return redirect(url_for('index'))
        title = request.form.get('title')
        year = request.form.get('year')

        if not title or not year or len(year) > 4  or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('index'))
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created')
        return redirect(url_for('index'))

    user = User.query.first()
    movies = Movie.query.all()
    #return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
    return render_template('index.html',movies=movies)


@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input')
            return redirect(url_for('settings'))

        current_user.name = name
        #current_user 会返回当前登陆用户的数据库记录对象
        #等同于下面的用法
        #user = User.query.first()
        #user.name = name
        db.session.commit()
        flash('Settings updated')
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':   #处理表单的请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('edit',movie_id=movie_id))

        movie.title = title  #更新标题
        movie.year = year    #更新年份
        db.session.commit()
        flash('Item updated')
        return redirect(url_for('index'))   #重定向回主页
    return render_template('edit.html',movie=movie)   #传入被编辑的记录

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('index'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        #验证用户密码是否一致

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success')
            return redirect(url_for('index'))  ###登陆成功，重定向到主页

        flash('Invalid username or password')  ##验证失败，显示错误信息
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye')
    return redirect(url_for('index'))
