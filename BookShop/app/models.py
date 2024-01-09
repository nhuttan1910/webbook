from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
import enum
from datetime import datetime,timedelta
from enum import Enum as EnumTK
import hashlib


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

class TheLoai(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    sach_theloai = relationship('Sach_TheLoai', backref='TheLoai', lazy=True)

    def __str__(self):
        return self.name


class NhaXuatBan (BaseModel):

    __tablename__ = 'nhaxuatban'


    name = Column(String(50), nullable=False, unique=True)
    sach = relationship('Sach', backref='nhaxuatban', lazy=False)

    def __str__(self):
        return self.name


class Sach(BaseModel):

    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(100))
    miniid = Column(String(50), nullable=False, unique=True)
    sach_info = Column(String(8000), nullable=False)
    quanti=Column(Integer, nullable=False)
    nxb_id = Column(Integer, ForeignKey(NhaXuatBan.id), nullable=False, default=1)
    sach_theloai = relationship('Sach_TheLoai', backref='Sach', lazy=True)
    sach_tacgia = relationship('Sach_TacGia', backref='Sach', lazy=True)
    cthd = relationship('ChiTietHD',backref='Sach',lazy=True)
    cthdn = relationship('ChiTietHDN',backref='Sach',lazy=True)
    def __str__(self):
        return self.name


class TacGia(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    sach_tacgia = relationship('Sach_TacGia', backref='TacGia', lazy=True)

    def __str__(self):
        return self.name


class Sach_TheLoai (BaseModel):
    S_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    TL_id = Column(Integer, ForeignKey(TheLoai.id), nullable=False)

    def __str__(self):
        return self.name


class Sach_TacGia (BaseModel):
    S_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    TG_id = Column(Integer, ForeignKey(TacGia.id), nullable=False)

    def __str__(self):
        return self.name


class VaiTro(EnumTK):
    KH = 1
    NV = 2
    QTV = 3
    QL = 4
    QLK = 5

    def __str__(self):
        return self.name


class TaiKhoan(BaseModel, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar= Column(String(100))
    active = Column(Boolean, default=True)
    join_date = Column(DateTime, default=datetime.now())
    role = Column(Enum(VaiTro), default=VaiTro.KH)
    kh = relationship('KhachHang', backref='TaiKhoan', lazy=True, uselist=False)
    nv = relationship('NhanVien', backref='TaiKhoan', lazy=True, uselist=False)
    qtv = relationship('QTV', backref='TaiKhoan', lazy=True, uselist=False)
    qlk = relationship('QLK', backref='TaiKhoan', lazy=True, uselist=False)
    ql = relationship('QL', backref='TaiKhoan', lazy=True, uselist=False)

    def __str__(self):
        return self.name


class QTV(BaseModel):
    name = Column(String(50), nullable=False)
    tk_id = Column(Integer, ForeignKey(TaiKhoan.id))

    def __str__(self):
        return self.name


class QLK(BaseModel):
    name= Column(String(50), nullable=False)
    tk_id = Column(Integer, ForeignKey(TaiKhoan.id))
    hdn_id= relationship('HoaDonNhap', backref='QLK', lazy=True)
    def __str__(self):
        return self.name


class QL(BaseModel):

    name= Column(String(50), nullable=False)
    tk_id = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)

    def __str__(self):
        return self.name

class KhachHang(BaseModel):

    name = Column(String(50), nullable=False)
    email = Column(String(50))
    diachi = Column(String(50), nullable=False)
    sdt = Column(String(50), nullable=False)
    tk_id = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)
    hd = relationship('HoaDon',backref='KhachHang',lazy=True)

    def __str__(self):
        return self.name

class QuiDinh(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    value = Column(Integer, nullable=False)
    info = Column(String(8000))

    def __str__(self):
        return self.name

class NhanVien(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    tk_id = Column(Integer, ForeignKey(TaiKhoan.id))
    hd = relationship('HoaDon', backref='NhanVien', lazy=True)
    def __str__(self):
        return self.name


class HoaDon(BaseModel):

    kh_id = Column(Integer, ForeignKey(KhachHang.id))
    ngay = Column(DateTime, default=datetime.now())
    thanhtoan = Column(Boolean, default=1)
    cthd = relationship('ChiTietHD', backref='HoaDon', lazy=True)
    nv_id = Column(Integer, ForeignKey(NhanVien.id))
    def __str__(self):
        return self.name


class ChiTietHD(BaseModel):

    quantity = Column(Integer,default=0)
    price = Column(Float,default=0)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    hd_id = Column (Integer, ForeignKey(HoaDon.id), nullable=False)

    def __str__(self):
        return self.name

class HoaDonNhap(BaseModel):
    ngay = Column(DateTime, default=datetime.now())
    thanhtoan = Column(Boolean, default=1)
    cthdn = relationship('ChiTietHDN', backref='HoaDonNhap', lazy=True)
    qlk_id = Column(Integer, ForeignKey(QLK.id))
    def __str__(self):
        return self.name


class ChiTietHDN(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    hd_id = Column (Integer, ForeignKey(HoaDonNhap.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()

        t1 = TheLoai(name='Technology')
        t2 = TheLoai(name='English')
        t3 = TheLoai(name='Story')

        db.session.add(t1)
        db.session.add(t2)
        db.session.add(t3)
        db.session.commit()
        #

        n1 = NhaXuatBan(name='Công Nghệ')
        n2 = NhaXuatBan(name='Thanh Niên')
        n3 = NhaXuatBan(name='Kim Đồng')
        db.session.add_all([n1, n2, n3])
        db.session.commit()


        s1 = Sach(name = 'Ngôn ngữ C', price = '120000', miniid = 10001,nxb_id = 1 , quanti= 100 ,
                  image = 'https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093852/C_yano6k.jpg',
                  sach_info = 'Giáo trình kỹ thuật lập trình C căn bản và nâng cao được hình thành qua nhiều năm giảng dạy của các tác giả. Ngôn ngữ lập trình C là một môn học cơ sở trong chương trình đào tạo kỹ sư, cử nhân tin học của nhiều trường đại học. Ở đây sinh viên được trang bị những kiến thức cơ bản nhất về lập trình, các kỹ thuật  tổ chức dữ liệu và lập trình căn bản với ngôn ngữ C')
        s2 = Sach(name='C++ Cơ Bản', price='130000', miniid=10002, nxb_id=1,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093860/C_k9hdrg.jpg',
                  sach_info ='Giáo trình Ngôn ngữ lập trình C++ được biên soạn nhằm mục đích phục vụ cho sinh viên các ngành kỹ thuật đồng thời là cuốn giáo trình tham khảo cho các giảng viên trong lĩnh vực Công nghệ thông tin. Mục đích của giáo trình này cung cấp đầy đủ các kiến thức về lập chương trình trên máy tính bằng ngôn ngữ C++, sau khi tìm hiểu xon giáo trình này độc giả có thể học tiếp các môn học về lập trình chuyên sâu trong các lĩnh vực chuyên ngành như Vi xử lý - Vi điều khiển, Lập trình Java, ASP, Lập trình phần mềm các thiết bị di động.')
        s3 = Sach(name='Python', price='150000', miniid=10003, nxb_id=1,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093881/python_fxnhfv.jpg',
                  sach_info='Cuốn sách Python Cơ Bản (Tái Bản 2023) là một tài liệu học tập chính thức dành cho những người mới bắt đầu học ngôn ngữ lập trình Python. Với cách viết lệnh đặc biệt sử dụng các dấu cách, sách giúp đưa ngôn ngữ Python trở nên dễ học và dễ viết. Đặc biệt, sách bao gồm trên 350 bài tập từ đơn giản đến phức tạp, phù hợp cho mọi đối tượng từ học sinh cấp THCS, THPT đến sinh viên đại học. Nội dung của sách bao gồm 16 chương về các chủ đề căn bản như input và chuyển đổi dữ liệu, hàm số, đối tượng trong Python, kiểu dữ liệu list, đồ họa con rùa, và cả bắt lỗi và kiểm soát lỗi trong Python.')
        s4 = Sach(name='Lập Trình Java', price='100000', miniid=10004, nxb_id=1,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093872/java_uqlzek.jpg',
                  sach_info='Hiện nay, học phần lập trình Java căn bản đã được đưa vào chương trình giảng dạy ở các bậc học chương trình đào tạo cử nhân thông tin. Để tạo điều kiện thuận lợi về tài liệu học tập cho sinh viên, cuốn sách “Lập trình Java căn bản” được biên soạn nhằm cung cấp các kiến thức cơ bản về ngôn ngữ lập trình Java; kiến thức về lập trình hướng đối tượng, xử lý biệt lệ, lập trình đa luồng, các luồng vào/ra, lập trình Form với Swing và kết nối cơ sở dữ liệu (CSDL) với Java. Ngoài ra, cuốn sách còn cung cấp thêm các lớp tiện ích hỗ trợ lập trình cấu trúc dữ liệu trong ngôn ngữ lập trình Java.')
        s5 = Sach(name='English Grammar', price='80000', miniid=10005, nxb_id=2,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093868/grammar_wgmvfy.jpg',
                  sach_info='Ngữ pháp là một phần quan trọng trong việc học tiếng Anh. Đây là bộ quy tắc và cấu trúc ngôn ngữ giúp người học hiểu cách sử dụng từ vựng và cấu trúc câu một cách chính xác. Sách ngữ pháp tiếng Anh thường bao gồm các bài học về các loại từ (danh từ, động từ, tính từ, trạng từ), cấu trúc câu (câu đơn, câu phức), cách sử dụng thì và dấu câu.')
        s6 = Sach(name='English Listening', price='60000', miniid=10006, nxb_id=2,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093875/listen_d2ndg8.jpg',
                  sach_info='Sách luyện nghe tiếng Anh (Listening) là tài liệu học cung cấp các hoạt động, bài tập và tài liệu nghe giúp người học cải thiện kỹ năng nghe trong tiếng Anh. Các sách này thường tập trung vào việc phát triển khả năng nghe thông qua việc lắng nghe các đoạn hội thoại, bài diễn thuyết, các đoạn tin tức, hoặc nói chuyện hàng ngày trong tiếng Anh.')
        s7 = Sach(name='English Reading', price='80000', miniid=10007, nxb_id=2,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093884/reading_l4qyd5.jpg',
                  sach_info='Sách đọc tiếng Anh (Reading) là tài liệu học cung cấp các bài đọc và hoạt động giúp người học nâng cao khả năng đọc và hiểu văn bản bằng tiếng Anh. Các sách này thường chứa các bài đọc từ đa dạng nguồn tài liệu như báo, tạp chí, truyện ngắn, sách, bài viết chuyên ngành,...')
        s8 = Sach(name='English Writing', price='70000', miniid=10008, nxb_id=2,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093892/writing_paiaa4.jpg',
                  sach_info='Sách viết tiếng Anh (Writing) là tài liệu học cung cấp hướng dẫn và các bài tập giúp người học cải thiện kỹ năng viết tiếng Anh. Các sách này thường tập trung vào việc phát triển khả năng viết từ việc xây dựng cấu trúc câu, vận dụng ngữ pháp và từ vựng, đến việc sắp xếp ý tưởng và tổ chức bố cục văn bản.')
        s9 = Sach(name='Trôi ', price='50000', miniid=10009, nxb_id=3,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093890/troi_aufoeh.jpg',
                  sach_info='Độc giả dễ dàng tìm thấy sự đồng cảm nơi mỗi nhân vật, như thể họ là từng phần trong mỗi con người chúng ta - và con người ấy, được mô tả như vật thể lang thang vô định - luôn ở trong trạng thái loay hoay lý giải, làm sáng tỏ về điều mà họ đã mất đi. Và trong hành trình dạt trôi theo quỹ đạo của riêng mình, những vật thể này sượt qua nhau bất giác làm vẩn lên hơi ấm con người, gợi cảm giác cái đẹp được cầm trên tay, thường trực sẵn một nguy cơ tan rã. Sau rốt, liệu rằng các nối kết giữa người với người có đủ bền chặt để mỗi tâm hồn thôi là sự nổi trôi vĩnh viễn?')
        s10 = Sach(name='Trật Nhịp', price='70000', miniid=10010, nxb_id=3,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093887/tratnhip_d91rxr.jpg',
                   sach_info='Tiểu Thuyết Trật Nhịp của Lương Anh Đan mang đậm tình cảm và những khía cạnh tâm lý phức tạp của nhân vật. Tác phẩm này đi sâu vào cuộc sống của những người trẻ tuổi, đặc biệt là trong bối cảnh xã hội đương đại đầy rẫy những áp lực và thách thức.')
        s11 = Sach(name='Cây Cam Ngọt', price='80000', miniid=10011, nxb_id=3,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093897/caycam_s0alas.jpg',
                   sach_info='Tiểu thuyết "Cây Cam Ngọt Của Tôi" là một tác phẩm của tác giả cực kỳ tài năng và đầy sáng tạo. Tác phẩm này mang đậm tâm hồn Việt Nam và đi sâu vào những chủ đề nhân văn, gia đình và tình người. Cuốn sách này tập trung vào câu chuyện về một gia đình Việt Nam và mối quan hệ giữa các thành viên trong gia đình đó. Nó không chỉ đề cập đến cuộc sống hàng ngày mà còn sâu rộng vào tâm trạng, xung đột và những khó khăn mà mỗi người trong gia đình phải đối mặt.')
        s12 = Sach(name='Một Tuần', price='60000', miniid=10012, nxb_id=3,quanti= 100,
                  image='https://res.cloudinary.com/dtbjoxzxy/image/upload/v1704093878/mottuan_hfvnt9.jpg',
                   sach_info='Tiểu thuyết Một Tuần là một tác phẩm văn học nổi tiếng. Cuốn sách này tập trung vào hành trình cuộc đời và tâm trạng của nhân vật chính là ông Ilya Ilyich Oblomov. Tiểu thuyết Một Tuần không chỉ là câu chuyện về một tuần trong cuộc đời của tác giả mà còn là một tác phẩm văn học có ảnh hưởng sâu sắc với những thông điệp về sự lười biếng, sự thay đổi và ý nghĩa của cuộc sống.')

        db.session.add_all([s1, s2, s3, s4, s5,s6])
        db.session.add_all([s7, s8, s9, s10, s11, s12])
        db.session.commit()


        #
        t1 = TacGia(name = 'Trần Nhựt Tân')
        t2 = TacGia(name='Mai Trần Nhật Tuấn')
        t3 = TacGia(name='Đỗ Chí Hưng')
        t4 = TacGia(name='Nguyễn Trọng Phúc')
        t5 = TacGia(name='Nguyễn Song Hậu')
        t6 = TacGia(name='Trần Thanh Hiệp')
        db.session.add_all([t1,t2,t3,t4,t5,t6])
        db.session.commit()

        stl1 = Sach_TheLoai(S_id=1,TL_id=1)
        stl2 = Sach_TheLoai(S_id=2, TL_id=1)
        stl3 = Sach_TheLoai(S_id=3, TL_id=1)
        stl4 = Sach_TheLoai(S_id=4, TL_id=1)
        stl5 = Sach_TheLoai(S_id=5, TL_id=2)
        stl6 = Sach_TheLoai(S_id=6, TL_id=2)
        stl7 = Sach_TheLoai(S_id=7,TL_id=2)
        stl8 = Sach_TheLoai(S_id=8, TL_id=2)
        stl9 = Sach_TheLoai(S_id=9, TL_id=3)
        stl10 = Sach_TheLoai(S_id=10, TL_id=3)
        stl11 = Sach_TheLoai(S_id=11, TL_id=3)
        stl12 = Sach_TheLoai(S_id=12, TL_id=3)
        db.session.add_all([stl1,stl2,stl3,stl4,stl5,stl6])
        db.session.add_all([stl7, stl8, stl9, stl10, stl11, stl12])
        db.session.commit()

        stg1 = Sach_TacGia(S_id=1, TG_id=1)
        stg2 = Sach_TacGia(S_id=2, TG_id=1)
        stg3 = Sach_TacGia(S_id=3, TG_id=2)
        stg4 = Sach_TacGia(S_id=4, TG_id=2)
        stg5 = Sach_TacGia(S_id=5, TG_id=3)
        stg6 = Sach_TacGia(S_id=6, TG_id=3)
        stg7 = Sach_TacGia(S_id=7, TG_id=4)
        stg8 = Sach_TacGia(S_id=8, TG_id=4)
        stg9 = Sach_TacGia(S_id=9, TG_id=5)
        stg10 = Sach_TacGia(S_id=10, TG_id=5)
        stg11 = Sach_TacGia(S_id=11, TG_id=6)
        stg12 = Sach_TacGia(S_id=12, TG_id=6)
        db.session.add_all([stg1, stg2, stg3, stg4, stg5, stg6])
        db.session.add_all([stg7, stg8, stg9, stg10, stg11, stg12])
        db.session.commit()

        q1 = QuiDinh (name = 'QD1', info='Số lượng sách nhập tối thiểu',  value='150')
        q2 = QuiDinh(name='QD2', info='Chỉ nhập sách còn ít hơn', value='300')
        q3 = QuiDinh(name='QD3', info='Thời gian thanh toán sau khi đặt hàng tối đa ', value='2')
        db.session.add(q1)
        db.session.add(q2)
        db.session.add(q3)
        db.session.commit()

        admin = TaiKhoan(username='admin', password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()), role=VaiTro.QL)
        db.session.add(admin)
        db.session.commit()


        nv = TaiKhoan(username='nv', password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()), role=VaiTro.NV)
        db.session.add(nv)
        db.session.commit()



        qlk = TaiKhoan(username='qlk', password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()),
                      role=VaiTro.QLK)
        db.session.add(qlk)
        db.session.commit()








