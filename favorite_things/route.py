from flask import render_template, request, jsonify
from requests import put, get, post
from favorite_things import app
from favorite_things.forms import LoginForm, RegForm


@app.route('/')
def index():
    form = LoginForm()
    comp = render_template('login.html', form=form)
    return render_template('index.html', comp=comp)


@app.route('/home', methods=['POST'])
def home():
    forms = request.form
    cate = get('http://api.spibes.com/api/cat?user='+str(forms['user']))
    cates = cate.json()
    cont = render_template('add.html', cats=cates['data'])
    return cont


@app.route('/signup')
def signup():
    form = RegForm()
    cont = render_template('reg.html', form=form)
    return cont


@app.route('/signin')
def signin():
    form = LoginForm()
    cont = render_template('login.html', form=form)
    return cont


@app.route('/register', methods=['POST'])
def reg():
    if request.method == 'POST':
        forms = jsonify(request.form)
        resp = post('http://api.spibes.com/api/user', data=forms.data, json=True)
        status = resp.json()
        if status['status'] == "error":
            ret = str(status['status'])+"//"+str(status['message'])
        else:
            ret = str(status['status'])
        return ret
    else:
        status = "Access denied!"
        return status


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        forms = request.form
        email = forms['email']
        password = forms['password']
        resp = get('http://api.spibes.com/api/user?email='+email+'&password='+password)
        status = resp.json()
        print(status)
        if status['status'] != "error":
            dat = str(status['status']+"//"+str(status['data']['id'])+"//"+status['data']['username'])
        else:
            dat = str(status['status']+"//"+status['message'])
        return dat
    else:
        status = "Access denied!"
        return status


@app.route('/list', methods=['POST'])
def fetch():
    if request.method == 'POST':
        forms = request.form
        cate = get('http://api.spibes.com/api/cat?user='+str(forms['user']))
        cates = cate.json()
        resp = get('http://api.spibes.com/api/list?user='+str(forms['user']))
        fav_list = resp.json()
        comp = render_template('list.html', list=fav_list['data'], cats=cates['data'])
        return comp


@app.route('/log', methods=['POST'])
def fetch_log():
    if request.method == 'POST':
        forms = request.form
        resp = get('http://api.spibes.com/api/list?id='+str(forms['id']))
        log_list = resp.json()
        dt = []
        data = log_list['data']
        log = data['log']
        if log is not None and log != "":
            lgz = log.split('{:||:}')
            for lgs in lgz:
                logs = lgs.split('(+||+)')
                lnt = len(logs)
                lst = lnt - 1
                for log in logs:
                    if log != logs[lst]:
                        logg = log+" <i style='float: right;'>"+logs[lst]+"</i>"
                        dt.append(logg)
        lnt = len(dt)
        comp = render_template('log.html', list=dt, lnt=lnt)
        return comp


@app.route('/edit', methods=['POST'])
def edit():
    if request.method == 'POST':
        forms = jsonify(request.form)
        resp = put('http://api.spibes.com/api/list', data=forms.data, json=True)
        res = str(resp)
        print(res)
        return res


@app.route('/add', methods=['POST'])
def new_favorite():
    if request.method == 'POST':
        forms = jsonify(request.form)
        resp = post('http://api.spibes.com/api/list', data=forms.data, json=True)
        return jsonify(resp.json())
    else:
        resp = {
            "status": "error",
            "message": 'Oops!!! Something went wrong.'
        }
        return jsonify(resp)


@app.route('/cat/new', methods=['POST'])
def new_cat():
    if request.method == 'POST':
        forms = jsonify(request.form)
        resp = post('http://api.spibes.com/api/cat', data=forms.data, json=True)
        return resp.json()['status']
    else:
        resp = {
            "status": "error",
            "message": 'Oops!!! Something went wrong.'
        }
        return jsonify(resp)


@app.route('/sort', methods=['POST'])
def sort():
    if request.method == 'POST':
        forms = request.form
        cate = get('http://api.spibes.com/api/cat?user=' + str(forms['user']))
        cates = cate.json()
        if forms['cat'] == "":
            resp = get('http://api.spibes.com/api/list?user=' + str(forms['user']))
        else:
            resp = get('http://api.spibes.com/api/list?user=' + str(forms['user']) + '&cat=' + str(forms['cat']))
        fav_list = resp.json()
        comp = render_template('sort.html', list=fav_list['data'], cats=cates['data'])
        return comp

