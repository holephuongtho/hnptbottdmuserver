#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pymongo import MongoClient
try:
    client = MongoClient('mongodb+srv://admin:G5mwPiDbMSZrVs2d@chatbottuvantuyensinh-acxk9.mongodb.net/test?retryWrites=true&w=majority')
    db = client['ChatbotTuVanTuyenSinh']
    col_diem_chuan = db['DiemChuan']
    col_khoi_thi = db['KhoiThi']
    col_truong = db['Truong']
    col_rating = db['PhanHoi']
except:
    print("ERROR IN DATABASE CONNECTION\n")


# In[2]:


import re
def remove_vietnamese_accent(s):
#     s = s.decode('utf-8')
    s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(u'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(u'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(u'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(u'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(u'[ìíịỉĩ]', 'i', s)
    s = re.sub(u'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(u'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(u'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(u'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(u'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(u'[Đ]', 'D', s)
    s = re.sub(u'[đ]', 'd', s)
#     return s.encode('utf-8')
    s = s.lower()
    s = re.sub("li", "ly", s)
    s = re.sub("ki", "ky", s)
    return s


# In[3]:


from collections import defaultdict
MON_THI_2_KHOI_THI = defaultdict(lambda: 'Unknown')
for doc in col_khoi_thi.find():
    MON_THI_2_KHOI_THI[frozenset([remove_vietnamese_accent(x) for x in doc["To Hop Mon"]])] = doc["Khoi"]
    
# Chả biết sao có mấy khối khác mã mà lại có cùng môn thi
print(len(MON_THI_2_KHOI_THI.keys()))

def convertMonThi2KhoiThi(DanhSachMon):
    return MON_THI_2_KHOI_THI[frozenset([remove_vietnamese_accent(x) for x in DanhSachMon])]

print(convertMonThi2KhoiThi(["ngữ văn", "lich su", "Địa lý"]))


# In[4]:


def is_inside(a, listOfA):
    for b in listOfA:
        if remove_vietnamese_accent(b) == remove_vietnamese_accent(a):
            return True
    return False


# In[5]:


def findDiemChuanByTruong(MaTruong, Nganh = None):
    DiemChuan = list()
    if Nganh:
        Nganh = Nganh.lower()
    for doc in col_diem_chuan.find():
        if MaTruong == doc["Ma Truong"]:
            if Nganh: 
                if Nganh == doc["Nganh"].lower():
                    DiemChuan.append(doc["Diem Chuan"])
            else:
                DiemChuan.append(doc["Diem Chuan"])
    return DiemChuan

findDiemChuanByTruong("HCMUE", "Giáo dục Chính trị")
# findDiemChuanByTruong("HCMUE", "hihi")


# In[6]:


# có điểm thi + Môn thi + trường => biết đậu ngành gì trong trường đó
# Nếu không có mã trường thì tìm tất cả các ngành có thể đậu của tất cả trường
def findNganhByDiemThi(DiemThi, Khoi, MaTruong = None):
    TruongList = list()
    if isinstance(Khoi, list):
        Khoi = convertMonThi2KhoiThi(Khoi)
    for doc in col_diem_chuan.find():
        if Khoi in doc["Khoi"] and DiemThi >= doc["Diem Chuan"]:
            if MaTruong:
                if MaTruong == doc["Ma Truong"]:
                    TruongList.append(doc)
            else: TruongList.append(doc)
    return sorted(TruongList, key = lambda i: i["Diem Chuan"],reverse=True) 

# Nhập list môn hay mã khối đều OK
# findNganhByDiemThi(16.5, ["hoá học", "toan", "Sinh Học"], "NTU")
findNganhByDiemThi(25, "A00")


# In[7]:


def common_member(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if (a_set & b_set): 
        return True 
    else: 
        return False


# In[8]:


# có điểm thi + Môn thi + trường => biết đậu ngành gì trong trường đó
# Nếu không có mã trường thì tìm tất cả các ngành có thể đậu của tất cả trường
def findNganhByDiemThiKhoiTruong(DiemThi, Khoi, MaTruong):
    TruongSet = set()
    TruongList = list()
    DiemThiSet = set()
    KhoiSet = set()
    MaTruongSet = set()
        
    for doc in col_diem_chuan.find():
        TruongList.append(doc)
        TruongSet.add(doc['_id'])
        if DiemThi is not None and DiemThi >= doc["Diem Chuan"]:
            DiemThiSet.add(doc['_id'])
        if Khoi is not None and common_member(Khoi, doc["Khoi"]):
            KhoiSet.add(doc['_id'])
        if MaTruong is not None and doc["Ma Truong"] in MaTruong:
            MaTruongSet.add(doc['_id'])        
            
    if len(DiemThiSet) == 0: 
        DiemThiSet = TruongSet
    if len(KhoiSet) == 0: 
        KhoiSet = TruongSet
    if len(MaTruongSet) == 0: 
        MaTruongSet = TruongSet
        
    TruongSet = DiemThiSet.intersection(KhoiSet).intersection(MaTruongSet)
    
    TruongList[:] = [d for d in TruongList if d['_id'] in TruongSet]

    return sorted(TruongList, key = lambda i: i["Diem Chuan"],reverse=True) 

# Nhập list môn hay mã khối đều OK
# findNganhByDiemThi(16.5, ["hoá học", "toan", "Sinh Học"], "NTU")
findNganhByDiemThiKhoiTruong(25.5, ['A02', 'B01'], ["BK"])


# In[9]:


def findDiemChuanByTruongNganh(MaTruong, Nganh):
    DiemThiSet = set()
    DiemThiList = list()
    MaTruongSet = set()
    NganhSet = set()
    
    for doc in col_diem_chuan.find():
        DiemThiList.append(doc)
        DiemThiSet.add(doc['_id'])
        
        if MaTruong is not None and doc["Ma Truong"] in MaTruong:
            MaTruongSet.add(doc['_id'])        
        if Nganh is not None and is_inside(doc["Nganh"], Nganh):
            NganhSet.add(doc['_id'])        
            
    if len(NganhSet) == 0: 
        NganhSet = DiemThiSet
    if len(MaTruongSet) == 0: 
        MaTruongSet = DiemThiSet
        
    DiemThiSet = MaTruongSet.intersection(NganhSet)
    
    DiemThiList[:] = [d for d in DiemThiList if d['_id'] in DiemThiSet]
    
    return DiemThiList

findDiemChuanByTruongNganh(["HCMUE", "BK"], ["Giáo dục Chính trị", "Khoa học máy tính ; Kỹ thuật Máy tính"])
# findDiemChuanByTruong("HCMUE", "hihi")


# In[10]:


# có điểm thi + Môn thi + trường => biết đậu ngành gì trong trường đó
# Nếu không có mã trường thì tìm tất cả các ngành có thể đậu của tất cả trường
def findTruongByDiemThiKhoiNganh(DiemThi, Khoi, NganhHoc):
    TruongSet = set()
    TruongList = list()
    DiemThiSet = set()
    KhoiSet = set()
    NganhSet = set()
        
    for doc in col_diem_chuan.find():
        TruongList.append(doc)
        TruongSet.add(doc['_id'])
        if DiemThi is not None and DiemThi >= doc["Diem Chuan"]:
            DiemThiSet.add(doc['_id'])
        if Khoi is not None and common_member(Khoi, doc["Khoi"]):
            KhoiSet.add(doc['_id'])
        if NganhHoc is not None and is_inside(doc["Nganh"], NganhHoc):
            NganhSet.add(doc['_id'])        
            
    if len(DiemThiSet) == 0: 
        DiemThiSet = TruongSet
    if len(KhoiSet) == 0: 
        KhoiSet = TruongSet
    if len(NganhSet) == 0: 
        NganhSet = NganhSet
        
    TruongSet = DiemThiSet.intersection(KhoiSet).intersection(NganhSet)
    
    TruongList[:] = [d for d in TruongList if d['_id'] in TruongSet]

    return sorted(TruongList, key = lambda i: i["Diem Chuan"],reverse=True) 

# Nhập list môn hay mã khối đều OK
# findNganhByDiemThi(16.5, ["hoá học", "toan", "Sinh Học"], "NTU")
findTruongByDiemThiKhoiNganh(30, [], ['Công nghệ kĩ thuật ô tô'])


# In[11]:


def findDiemChuanByTruongNganh(MaTruong, Nganh):
    DiemThiSet = set()
    DiemThiList = list()
    MaTruongSet = set()
    NganhSet = set()
    
    for doc in col_diem_chuan.find():
        DiemThiList.append(doc)
        DiemThiSet.add(doc['_id'])
        
        if MaTruong is not None and doc["Ma Truong"] in MaTruong:
            MaTruongSet.add(doc['_id'])        
        if Nganh is not None and is_inside(doc["Nganh"], Nganh):
            NganhSet.add(doc['_id'])        
            
    if len(NganhSet) == 0: 
        NganhSet = DiemThiSet
    if len(MaTruongSet) == 0: 
        MaTruongSet = DiemThiSet
        
    DiemThiSet = MaTruongSet.intersection(NganhSet)
    
    DiemThiList[:] = [d for d in DiemThiList if d['_id'] in DiemThiSet]
    
    return DiemThiList


# In[12]:


def findKhoiThiByTruongNganh(MaTruong, Nganh):
    return findDiemChuanByTruongNganh(MaTruong, Nganh)


# In[13]:


def findHocPhiByTruong(Truong):
    returnHocPhi = None
    for doc in col_truong.find():
        if doc["Ma Truong"] == Truong:
            returnHocPhi = doc["Hoc Phi"]
    return returnHocPhi


# In[14]:


def findKyTucXaByTruong(Truong):
    returnKyTucXa = None
    for doc in col_truong.find():
        if doc["Ma Truong"] == Truong:
            returnKyTucXa = doc["Ky Tuc Xa"]
    return returnKyTucXa


# In[15]:


def findLoaiHinhByTruong(Truong):
    returnLoaiHinh = None
    for doc in col_truong.find():
        if doc["Ma Truong"] == Truong:
            returnLoaiHinh = doc["isCongLap"]
    return returnLoaiHinh


# In[16]:


def findDiaChiByTruong(Truong):
    returnDiaChi = None
    for doc in col_truong.find():
        if doc["Ma Truong"] == Truong:
            returnDiaChi = doc["Dia Chi"]
    return returnDiaChi


# In[27]:


def saveRating(ratingToSave):
    return col_rating.insert_one(ratingToSave)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




