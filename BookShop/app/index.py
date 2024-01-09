import math
import utils
from flask import render_template, request, redirect, session, jsonify, url_for
import dao
from app import app, login
from app.admin import *
import cloudinary.uploader
from flask_login import login_user, logout_user, current_user
from datetime import datetime,timedelta


@app.route('/')
def index():
    kw = request.args.get('kw')

    theloai_id = request.args.get('theloai_id')

    page = request.args.get("page")

    theloai = dao.load_theloai()

    sach = dao.load_sach(kw=kw, theloai_id = theloai_id, page=page)

    total = dao.count_sach()

    return render_template('index.html', theloai=theloai,
                           sach=sach,
                           pages=math.ceil(total / app.config['PAGE_SIZE']))


@app.route('/nv')
def nv():
    return render_template('nv/index.html')

@app.route('/qlk')
def qlk():
    return render_template('qlk/index.html', stats=utils.load_hd_nhap())


@app.route('/qlk/create', methods=['get', 'post'])
def qlk_cr():
    if request.method.__eq__('POST'):
        sach_id = request.form.get('bookSelect')
        quantity = request.form.get('quantity_into')
        utils.hd_nhap(sach_id=sach_id, quantity=quantity)
    return render_template('qlk/create.html', b=utils.data_book(), qd=utils.data_qd())

@app.route('/nv/create', methods=['get', 'post'])
def nvCr():
    id = 1
    if request.method.__eq__('POST'):
        id = int(request.form.get('mavach'))
    return render_template('nv/create.html', s=utils.add_book_nv(int(id))\
                           , stats=utils.count_cart(session.get('viewtt')), r = VaiTro.NV)


@app.route('/sach/<id>')
def details(id):
    sach_profile = dao.load_sachprofile(id)
    theloai_profile = dao.load_theloaiprofile(id)
    tacgia_profile = dao.load_tacgiaprofile(id)
    nxb_profile = dao.load_nxbrpofile(id)
    return render_template('details.html', sach_profile=sach_profile,theloai_profile=theloai_profile,
                           tacgia_profile=tacgia_profile,nxb_profile=nxb_profile)


@app.route('/api/cart', methods=['post'])
def add_cart():
    """
        {
        "cart": {
                "1": {
                    "id": 1,
                    "name": "ABC",
                    "price": 12,
                    "quantity": 2
                }, "2": {
                    "id": 2,
                    "name": "ABC",
                    "price": 12,
                    "quantity": 2
                }
            }
        }
        :return:
        """
    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("id"))

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/nvcart', methods=['post'])
def add_view_nv():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')


    viewtt = session.get('viewtt')
    if not viewtt :
        viewtt = {}

    if id in viewtt:
        viewtt[id]['quantity'] = viewtt[id]['quantity'] + 1
    else:
        viewtt[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['viewtt'] = viewtt

    return jsonify(utils.count_cart(viewtt))

@app.route("/api/cart/<sach_id>", methods=['put'])
def update_cart(sach_id):
    cart = session.get('cart')
    if cart and sach_id in cart:
        quantity = request.json.get('quantity')
        cart[sach_id]['quantity'] = int(quantity)

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/api/cart/<sach_id>", methods=['delete'])
def delete_cart(sach_id):
    cart = session.get('cart')
    if cart and sach_id in cart:
        del cart[sach_id]

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/api/pay", methods=['post'])
def pay():
        try:
            dao.add_order(session.get('cart'))
        except:
            return jsonify({'code':500,'err_msg': 'Có lỗi xảy ra trong quá trình thanh toán!!!'})
        else:
            del session['cart']
            return jsonify({'code': 200})


@app.route("/api/pay_online", methods=['post'])
def pay_online():
        try:
            dao.add_order_online(session.get('cart'))
        except:
            return jsonify({'code':500,'err_msg': 'Có lỗi xảy ra trong quá trình thanh toán!!!'})
        else:
            del session['cart']
            return jsonify({'code': 200})


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/info')
def info():
    info_user = dao.load_info(user_id=current_user.id)
    return render_template('info.html', info_user=info_user)


@app.route('/userinfo')
def tk_info():
    tk = dao.load_tk_info(user_id=current_user.id)
    info_user = dao.load_info(user_id=current_user.id)
    hd = dao.load_hoadon(user_id=info_user[0].id)

    return render_template('userinfo.html',tk = tk,info_user=info_user,hd=hd)


@app.route('/hd/<id>')
def hd_info(id):
    cthd = dao.load_chitiethd(id)
    info_user = dao.load_info(user_id=current_user.id)
    hd = dao.load_hoadon(user_id=id)
    hd_info = dao.load_hdinfo(id)
    sach_info = dao.load_sach_info()
    day = dao.load_day()
    ngay_thanh_toan = (hd_info[0].ngay + timedelta(days=day[0].value))
    total_quanti = 0
    total_sum = 0
    for c in cthd:
        total_quanti = total_quanti + c.quantity
        total_sum = total_sum + (c.quantity*c.price)

    return render_template('orderdetails.html', cthd=cthd, info_user=info_user,hd=hd,hd_info=hd_info,
                           total_sum=total_sum,total_quanti=total_quanti,ngay_thanh_toan=ngay_thanh_toan,sach_info=sach_info,
                           day=day)


@app.context_processor
def common_resp():
    return {
        'theloai': dao.load_theloai(),
        'cart': utils.count_cart(session.get('cart'))
    }


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        location = request.form.get('location')
        phonenum = request.form.get('phonenum')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_tk(username=username, password=password, avatar=avatar_path)
                tk_id = utils.get_id_from_username(username)
                utils.tk_link_kh(tk_id=tk_id, name=name, location=location, phonenum=phonenum, email=email)
                return redirect(url_for('signin'))
            else:
                err_msg = "Password not valid"
        except Exception as ex:
            err_msg = "System is having error" + str(ex)

    return render_template('register.html', err_msg=err_msg)

@app.route('/signin',methods=['get','post'])
def signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        tk = utils.check_login(username=username, password=password)
        if tk:
            login_user(user=tk)
            next = request.args.get('next')
            return redirect('/' if next is None else next)
        else:
            err_msg = 'Username or password is wrong'
    return render_template('login.html', err_msg=err_msg)


@app.route('/quanly-login', methods=['post'])
def signin_quanly():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        tk = utils.check_login(username=username, password=password, role=VaiTro.QL)
        if tk:
            login_user(user=tk)
            return redirect('/admin')


@app.route('/nv/signin', methods=['get', 'post'])
def signin_nv():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        tk = utils.check_login(username=username, password=password, role=VaiTro.NV)
        if tk:
            login_user(user=tk)
            return redirect('/nv')
        else:
            err_msg = 'Username or password is wrong'
    return render_template('nv/login.html', err_msg=err_msg)

@app.route('/qlk/signin', methods=['get', 'post'])
def signin_qlk():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        tk = utils.check_login(username=username, password=password, role=VaiTro.QLK)
        if tk:
            login_user(user=tk)
            return redirect('/qlk')
        else:
            err_msg = 'Username or password is wrong'
    return render_template('qlk/login.html', err_msg=err_msg)


@app.route('/logoutTkNV')
def logoutTkNV():
    logout_user()
    return redirect(url_for('signin_nv'))

@app.route('/logoutTkQLK')
def logoutTkQLK():
    logout_user()
    return redirect(url_for('signin_qlk'))


@login.user_loader
def tk_load(tk_id):
    return utils.get_tk_by_id(tk_id=tk_id)

@app.route('/logoutTk')
def logoutTk():
    logout_user()
    return redirect(url_for('signin'))


@app.route("/api/pay_nv", methods=['post'])
def pay_nv():
        try:
            utils.cre_hd(session.get('viewtt'))
        except:
            return jsonify({'code':500,'err_msg': 'Có lỗi xảy ra trong quá trình thanh toán!!!'})
        else:
            del session['viewtt']
            return jsonify({'code': 200})




if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)
