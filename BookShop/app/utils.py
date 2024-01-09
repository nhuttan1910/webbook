from app import db, app
import json, os
from app.models import TaiKhoan, KhachHang, ForeignKey, Sach,TheLoai, Sach_TheLoai, VaiTro, ChiTietHD, HoaDon, QuiDinh, HoaDonNhap, ChiTietHDN,NhaXuatBan
import hashlib
from flask import session
from flask_login import current_user, UserMixin
from sqlalchemy import func
from sqlalchemy.sql import extract
def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity']*c['price']

    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }

def add_tk(username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    tk = TaiKhoan(username=username.strip(), password=password,
                  avatar=kwargs.get('avatar'))

    db.session.add(tk)
    db.session.commit()


def get_id_from_username(username):
    username = username.strip()
    tk = TaiKhoan.query.filter_by(username=username).first()
    if tk:
        return tk.id
    else:
        return None
def tk_link_kh(tk_id, name, location,phonenum, **kwargs):
    kh = KhachHang(tk_id=tk_id, name=name, diachi=location, sdt=phonenum, email=kwargs.get('email'))
    db.session.add(kh)
    db.session.commit()

def check_login(username,password, role=VaiTro.KH):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username.strip()),
                                    TaiKhoan.password.__eq__(password),
                                    TaiKhoan.role.__eq__(role)).first()

def get_tk_by_id(tk_id):
    return TaiKhoan.query.get(tk_id)

def view_sach():
    result = db.session.query(TheLoai, func.count(Sach.id).label('sach_count'))\
                    .outerjoin(Sach_TheLoai, TheLoai.id == Sach_TheLoai.TL_id)\
                    .outerjoin(Sach, Sach_TheLoai.S_id == Sach.id)\
                    .group_by(TheLoai.id).all()
    return result


def book_stats(kw=None, from_date=None, to_date=None):
    b = db.session.query(Sach, ChiTietHD.quantity)\
                        .outerjoin(ChiTietHD, ChiTietHD.sach_id == Sach.id)\
                        .outerjoin(HoaDon, HoaDon.id == ChiTietHD.hd_id)\
                        .group_by(Sach.id, Sach.name, ChiTietHD.quantity)

    if kw:
        b = b.filter(Sach.name.contains(kw))

    if from_date:
        b = b.filter(HoaDon.ngay.__ge__(from_date))

    if to_date:
        b = b.filter(HoaDon.ngay.__le__(to_date))
    return b.all()


def month_type_stats(year, type=None):
    kq =  db.session.query(TheLoai, extract('month', HoaDon.ngay),\
                            func.sum(ChiTietHD.price * ChiTietHD.quantity))\
                            .outerjoin(Sach_TheLoai, Sach_TheLoai.TL_id == TheLoai.id)\
                            .outerjoin(Sach, Sach.id == Sach_TheLoai.S_id)\
                            .outerjoin(ChiTietHD, ChiTietHD.sach_id == Sach.id)\
                            .outerjoin(HoaDon, ChiTietHD.hd_id == HoaDon.id)\
                            .filter(extract('year', HoaDon.ngay) == year)\
                            .group_by(TheLoai, extract('month', HoaDon.ngay))

    if type:
        kq = kq.filter(TheLoai.name.contains(type))

    return kq


def add_book_nv(b_id):
    return Sach.query.get(b_id)

def cre_hd(viewtt):
    hd = HoaDon(thanhtoan=1)
    db.session.add(hd)
    db.session.commit()

    for c in viewtt.values():
        cthd = ChiTietHD(quantity=c['quantity'], price=c['price'], hd_id=hd.id, sach_id=c['id'])

        db.session.add(cthd)

    db.session.commit()


def data_book():
    return Sach.query.all()

def data_qd():
    return QuiDinh.query.all()

def hd_nhap(sach_id, quantity):
    hd = HoaDonNhap(thanhtoan=1)
    qd_sl_nhap = QuiDinh.query.filter(QuiDinh.name == 'QD1').first()
    ql_sl_con = QuiDinh.query.filter(QuiDinh.name == 'QD2').first()
    s = Sach.query.get(sach_id)
    sl_sach_con = s.quanti
    if int(quantity) > int(qd_sl_nhap.value) and int(sl_sach_con) < int(ql_sl_con.value):
        db.session.add(hd)
        db.session.commit()

        cthd = ChiTietHDN(quantity=quantity, price=s.price, hd_id=hd.id, sach_id=sach_id)
        db.session.add(cthd)
        db.session.commit()

        s.quanti = int(s.quanti) + int(quantity)
        db.session.add(s)
        db.session.commit()


def load_hd_nhap():
    return db.session.query(HoaDonNhap, ChiTietHDN, Sach, NhaXuatBan, func.sum(ChiTietHDN.price*ChiTietHDN.quantity))\
                                        .outerjoin(ChiTietHDN, ChiTietHDN.hd_id == HoaDonNhap.id)\
                                        .outerjoin(Sach, Sach.id == ChiTietHDN.sach_id)\
                                        .outerjoin(NhaXuatBan, NhaXuatBan.id == Sach.nxb_id)\
                                        .group_by(HoaDonNhap.id, ChiTietHDN,Sach, NhaXuatBan).all()
