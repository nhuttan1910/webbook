from app import app, db, dao, utils
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app.models import Sach, TheLoai, NhaXuatBan, TacGia, VaiTro, QuiDinh
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from flask_login import current_user, logout_user
from flask import redirect, request
from datetime import datetime

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils.view_sach())


admin = Admin(app=app, name="Bookshop Administrator", template_mode='bootstrap4', index_view=MyAdminIndex())


class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        return self.render('admin/stats.html', stats=utils.book_stats(kw=kw, from_date=from_date, to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.__eq__(VaiTro.QL)


class StatsMonthView(BaseView):
    @expose('/')
    def index(self):
        type = request.args.get('type')
        year = request.args.get('year', datetime.now().year)
        return self.render('admin/statsmonth.html', stats=utils.month_type_stats(year=year, type=type))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.__eq__(VaiTro.QL)

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.__eq__(VaiTro.QL)

# class QLAuthenticatedModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.role.__eq__(VaiTro.QL)




class SachView(AuthenticatedModelView):
    column_list = ('id', 'name', 'price', 'quanti', 'nxb_id')
    can_export = True
    column_filters = ['price', 'name']
    can_view_details = True
    column_searchable_list = ['name']


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(SachView(Sach, db.session))
admin.add_view(AuthenticatedModelView(TheLoai, db.session))
admin.add_view(AuthenticatedModelView(QuiDinh, db.session))
admin.add_view(AuthenticatedModelView(NhaXuatBan, db.session))
admin.add_view(StatsView(name='Stats'))
admin.add_view(StatsMonthView(name='Stats Month'))
admin.add_view(LogoutView(name='Logout'))