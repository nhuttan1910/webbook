from app.models import (TheLoai, Sach, TacGia, NhaXuatBan, Sach_TheLoai, Sach_TacGia,
                        KhachHang,HoaDon,ChiTietHD,TaiKhoan,QuiDinh)
from app import app, db
import hashlib
from flask_login import current_user

def load_theloai():
    return TheLoai.query.all()

def sach_nv():
    return Sach.query.all()

def load_sach(kw=None, theloai_id=None, page=None):
    sach = Sach.query
    theloai = TheLoai.query
    ma = Sach_TheLoai.query


    if kw:
        sach = sach.filter(Sach.name.contains(kw))

    if theloai_id:
        sach = sach.filter(Sach.sach_theloai.any(TL_id=theloai_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return sach.offset(start).limit(page_size).all()

    return sach.all()

def count_sach():
    return Sach.query.count()


def load_sachprofile(id):
    sach = Sach.query

    sach_profile = sach.filter(Sach.id == id)

    return sach_profile.all()

def load_theloaiprofile(id):
    theloai = TheLoai.query

    theloai_profile = theloai.filter(TheLoai.sach_theloai.any(Sach_TheLoai.S_id == id))

    return theloai_profile.all()


def load_tacgiaprofile(id):
    tacgia = TacGia.query

    tacgia_profile = tacgia.filter(TacGia.sach_tacgia.any(Sach_TacGia.S_id == id))

    return tacgia_profile.all()


def load_nxbrpofile(id):
    nxb = NhaXuatBan.query

    sach_nxb = nxb.filter(NhaXuatBan.id == Sach.nxb_id)
    nxb_profile = sach_nxb.filter(Sach.id == id)

    return nxb_profile.all()


def load_info(user_id):
    info_user = KhachHang.query

    info_user = info_user.filter(KhachHang.tk_id == user_id)

    return info_user.all()


def load_tk_info(user_id):
    tk = TaiKhoan.query

    tk = tk.filter(TaiKhoan.id == user_id)

    return tk.all()


def load_hoadon(user_id):
    hd = HoaDon.query

    hd = hd.filter(HoaDon.kh_id == user_id)

    return hd.all()


def load_chitiethd(hd_id):
    cthd = ChiTietHD.query

    cthd = cthd.filter(ChiTietHD.hd_id == hd_id)

    return cthd.all()


def load_hdinfo(hd_id):
    hd_info = HoaDon.query

    hd_info=hd_info.filter(HoaDon.id == hd_id)

    return hd_info.all()


def load_sach_info():
    sach_info = Sach.query

    return sach_info.all()


def load_day():
    day = QuiDinh.query

    day = day.filter(QuiDinh.name.contains('QD3'))

    return day.all()

def add_order(cart_info):
    info = KhachHang.query
    info = info.filter(KhachHang.tk_id == current_user.id)

    if cart_info:
        o = HoaDon(kh_id=info[0].id, thanhtoan = 0)
        db.session.add(o)
        db.session.commit()

        for c in cart_info.values():
            cthd = ChiTietHD(quantity = c['quantity'], price = c['price'], hd_id=o.id,sach_id=c['id'])

            db.session.add(cthd)

        db.session.commit()


def add_order_online(cart_info):
    info = KhachHang.query
    info = info.filter(KhachHang.tk_id == current_user.id )

    if cart_info:
        o = HoaDon(kh_id=info[0].id, thanhtoan = 1)
        db.session.add(o)
        db.session.commit()

        for c in cart_info.values():
            cthd = ChiTietHD(quantity = c['quantity'], price = c['price'], hd_id=o.id,sach_id=c['id'])

            db.session.add(cthd)

        db.session.commit()



