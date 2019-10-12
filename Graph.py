#!/usr/bin/env python
# coding: utf-8

# In[1]:


from DB import *
from statistics import mean 


# In[2]:


PREDEFINE_RESPONSE = {
    "KhongHieu": "Tôi không hiểu ý của bạn. Xin vui lòng nhập lại.",
    "Truong": "Bạn muốn hỏi về trường gì?",
    "KhoiThi": "Bạn muốn hỏi về khối gì?",
    "DiemChuan": "Bạn ngắm mình thi được bao nhiêu điểm?",
    "NganhHoc": "Bạn muốn hỏi về ngành học nào?",
    "Other": "Bạn còn muốn hỏi gì không?"
}

PREDEFINE_ANSWER_FAILED = {
    "HocPhi": "Bạn phải cung cấp tên trường nếu muốn biết thông tin về học phí.",
    "MaTruong": "Bạn phải cung cấp tên trường nếu muốn biết thông tin về mã trường.",
    "KyTucXa": "Bạn phải cung cấp tên trường nếu muốn biết thông tin về ký túc xá.",
    "LoaiHinh": "Bạn phải cung cấp tên trường nếu muốn biết thông tin về loại hình.",
    "DiaChi": "Bạn phải cung cấp tên trường nếu muốn biết thông tin về địa chỉ.",
    "NganhHoc": "Thông tin được cung cấp chưa đủ để tư vấn ngành học cho bạn được.",
    "DiemChuan": "Thông tin được cung cấp chưa đủ để tìm kiếm về điểm chuẩn.",
    "KhoiThi": "Thông tin được cung cấp chưa đủ để tìm kiếm về khối thi",
    "Truong": "Thông tin được cung cấp chưa đủ để tư vấn trường học cho bạn được."
}


# In[3]:


def listToString(l):
    s = ""
    for e in l:
        s += e + ", "
    s = s[0:-2]
    return s


# In[4]:


DEFINED_INTENTS = ["Truong", "KhoiThi", "DiemChuan", "NganhHoc", "LoaiHinh", "DiaChi", "KyTucXa", "MaTruong", "HocPhi"]


# In[5]:


def cleanUpList(l):
    lSet = set(l)
    rSet = lSet.intersection(set(DEFINED_INTENTS))
    return list(rSet)


# In[17]:


def getAnswer(key, query, value):
    if key == "HocPhi":
        if value is None:
            return "Không tìm thấy thông tin học phí của Trường " + str(query)
        else:
            return "Vui lòng tham khảo thông tin học phí của Trường " + str(query) + ' tại: <a target="_blank" href="'+value+'">' + value + "</a>"

    if key == "MaTruong":
        if value is None:
            return "Không tìm thấy thông tin Mã trường"
        else:
            return "Mã trường là: " + value
        
    if key == "KyTucXa":
        if value is None:
            return "Không tìm thấy thông tin về ký túc xá của Trường " + str(query)
        else:
            return "Vui lòng tham khảo thông tin ký túc xá của Trường " + str(query) + ' tại: <a target="_blank" href="'+value+'">' + value + "</a>"

    if key == "LoaiHinh":
        if value is None:
            return "Không tìm thấy thông tin về loại hình của Trường " + str(query)
        elif value is True:
            return "Trường " + str(query) + " là trường công lập."
        else: 
            return "Trường " + str(query) + " là trường dân lập."
        
    if key == "DiaChi":
        if value is None:
            return "Không tìm thấy thông tin về địa chỉ của Trường " + str(query)
        else:
            return "Địa chỉ của Trường " + str(query) + " là: " + value
        
    if key == "NganhHoc":
        if value is None:
            return "Không tìm thấy ngành học phù hợp với nhu cầu của bạn."
        else:
            return "Ngành " + value['Nganh'] + " - Trường " + value['Ten Truong'] + " với điểm chuẩn ở mức " + str(value['Diem Chuan']) + " của khối " + listToString(value['Khoi'])
    if key == "DiemChuan":
        if value is None:
            return "Không tim thấy thông tin điểm chuẩn phù hợp với nhu cầu của bạn."
        else:
            return "Điểm chuẩn của ngành " + value['Nganh'] + " - Trường " + value['Ten Truong'] + " là ở mức <strong>" + str(value['Diem Chuan']) + " </strong>"
    if key == "KhoiThi":
        if value is None:
            return "Không tim thấy thông tin khối thi phù hợp với nhu cầu của bạn."
        else:
            return "Khối thi của ngành " + value['Nganh'] + " - Trường " + value['Ten Truong'] + " là: <strong>" + listToString(value['Khoi']) + " </strong>"
    if key == "Truong":
        if value is None:
            return "Không tim thấy trường phù hợp với nhu cầu của bạn."
        else:
            return "Trường " + value['Ten Truong']


# In[2]:


class HuongNghiep_Graph():
    def __init__(self):
        self.extracted_values = dict()
        self.intents = dict()
        self.asked_features = list()
    
  
    def fill(self, extracted_dict, candidate_intent_dict):
        # fill values
        for key in extracted_dict.keys():
            if key in self.extracted_values.keys():
                self.extracted_values[key] = self.extracted_values[key].union(set(extracted_dict[key]))
            else:
                self.extracted_values[key] = set(extracted_dict[key])
        # mark intents
        for key in candidate_intent_dict.keys():
            if key in self.intents:
                # hỏi đi hỏi lại một intent tạm thời không có ý nghĩa trong chatbot này
                continue
            else:
                # có intent mới, đánh dấu chưa trả lời để hàm getResponse kiểm tra
                if key not in self.extracted_values:
                    self.intents[key] = False
        
        # Nếu fill mà không có intent, cứ coi như là tìm trường 
        if len(self.intents.keys()) == 0:
            self.intents['Truong'] = False
                
    def toString(self):
        print(self.extracted_values)
        print(self.intents)
    
    def checkForValueOrAsked(self, listOfFeatures):
        ok = True
        needAsk = ""
        for f in listOfFeatures:
            if f not in self.extracted_values.keys() and f not in self.asked_features and f not in self.intents.keys():
                ok = False
                needAsk = f
        return ok, needAsk
    
    def markIntentStatus(self):
        needAskSet = list()
        # Các intent sẽ được đánh dấu true nếu đã có thể trả lời được 
        # hoặc các thông tin cần có để trả lời đã được chatbot hỏi 
        if "HocPhi" in self.intents.keys():
            # Học phí thì chỉ cần có tên trường là trả lời được 
            self.intents["HocPhi"], t = self.checkForValueOrAsked(["Truong"])
            needAskSet.append(t)
            
        if "MaTruong" in self.intents.keys():
            # Học phí thì chỉ cần có tên trường là trả lời được 
            self.intents["MaTruong"], t = self.checkForValueOrAsked(["Truong"])
            needAskSet.append(t)
            
        if "KyTucXa" in self.intents.keys():
            # Ký túc xá thì chỉ cần có tên trường là trả lời được 
            self.intents["KyTucXa"], t = self.checkForValueOrAsked(["Truong"])
            needAskSet.append(t)
            
        if "LoaiHinh" in self.intents.keys():
            # Ký túc xá thì chỉ cần có tên trường là trả lời được 
            self.intents["LoaiHinh"], t = self.checkForValueOrAsked(["Truong"])
            needAskSet.append(t)
            
        if "NganhHoc" in self.intents.keys():
            # Ngành học thì cần trường, điểm chuẩn và khối để trả lời được 
            self.intents["NganhHoc"], t = self.checkForValueOrAsked(["Truong", "KhoiThi", "DiemChuan"])
            needAskSet.append(t)
            
        if "DiemChuan" in self.intents.keys():
            # Điểm chuẩn thì cần trường, khối thi và ngành học để trả lời được 
            self.intents["DiemChuan"], t = self.checkForValueOrAsked(["Truong", "NganhHoc"])
            needAskSet.append(t)
        if "KhoiThi" in self.intents.keys():
            # Điểm chuẩn thì cần trường, khối thi và ngành học để trả lời được 
            self.intents["KhoiThi"], t = self.checkForValueOrAsked(["Truong", "NganhHoc"])
            needAskSet.append(t)
            
        if "Truong" in self.intents.keys():
            # Điểm chuẩn thì cần trường, khối thi và ngành học để trả lời được 
            self.intents["Truong"], t = self.checkForValueOrAsked(["DiemChuan", "KhoiThi", "NganhHoc"])
            needAskSet.append(t)
            
        return needAskSet
    
    def getAnswerNow(self):
        responseList = list() 
        if "HocPhi" in self.intents.keys():
            if "Truong" not in self.extracted_values.keys():
                    responseList.append({"key": "HocPhi", "value": PREDEFINE_ANSWER_FAILED["HocPhi"]})
            else:
                for truong in self.extracted_values["Truong"]:
                    dbValue = findHocPhiByTruong(truong)
                    responseList.append({"key": "HocPhi", "value": getAnswer("HocPhi", truong, dbValue)})
            
        if "MaTruong" in self.intents.keys():
            if "Truong" not in self.extracted_values.keys():
                    responseList.append({"key": "MaTruong", "value": PREDEFINE_ANSWER_FAILED["MaTruong"]})
            else:
                for truong in self.extracted_values["Truong"]:
                    responseList.append({"key": "MaTruong", "value": getAnswer("MaTruong", None, truong)})
                    
        if "KyTucXa" in self.intents.keys():
            if "Truong" not in self.extracted_values.keys():
                    responseList.append({"key": "KyTucXa", "value": PREDEFINE_ANSWER_FAILED["KyTucXa"]})
            else:
                for truong in self.extracted_values["Truong"]:
                    dbValue = findKyTucXaByTruong(truong)
                    responseList.append({"key": "KyTucXa", "value": getAnswer("KyTucXa", truong, dbValue)})
                    
        if "LoaiHinh" in self.intents.keys():
            if "Truong" not in self.extracted_values.keys():
                    responseList.append({"key": "LoaiHinh", "value": PREDEFINE_ANSWER_FAILED["LoaiHinh"]})
            else:
                for truong in self.extracted_values["Truong"]:
                    dbValue = findLoaiHinhByTruong(truong)
                    responseList.append({"key": "LoaiHinh", "value": getAnswer("LoaiHinh", truong, dbValue)})
                    
        if "DiaChi" in self.intents.keys():
            if "Truong" not in self.extracted_values.keys():
                    responseList.append({"key": "DiaChi", "value": PREDEFINE_ANSWER_FAILED["DiaChi"]})
            else:
                for truong in self.extracted_values["Truong"]:
                    dbValue = findDiaChiByTruong(truong)
                    responseList.append({"key": "DiaChi", "value": getAnswer("DiaChi", truong, dbValue)})
                    
        if "NganhHoc" in self.intents.keys():
            if "Truong" in self.extracted_values.keys():
                TruongList = self.extracted_values["Truong"]
            else: 
                TruongList = None
            
            if "KhoiThi" in self.extracted_values.keys():
                KhoiThiList = self.extracted_values["KhoiThi"]
            else: 
                KhoiThiList = None
                
            if "DiemChuan" in self.extracted_values.keys():
                DiemChuanAvg = mean(list(self.extracted_values["DiemChuan"]))
            else: 
                DiemChuanAvg = None
            
            if TruongList is None and KhoiThiList is None and DiemChuanAvg is None:
                responseList.append({"key": "NganhHoc", "value": PREDEFINE_ANSWER_FAILED["NganhHoc"]})
            else:
                NganhList = findNganhByDiemThiKhoiTruong(DiemChuanAvg, KhoiThiList, TruongList)
                if len(NganhList) == 0:
                    responseList.append({"key": "NganhHoc", "value": getAnswer("NganhHoc", None, None)})
                else:
                    for n in NganhList[:3]:
                        responseList.append({"key": "NganhHoc", "value": getAnswer("NganhHoc", None, n)})
                        
        if "DiemChuan" in self.intents.keys():
            if "Truong" in self.extracted_values.keys():
                TruongList = self.extracted_values["Truong"]
            else: 
                TruongList = None
            
            if "NganhHoc" in self.extracted_values.keys():
                NganhHocList = self.extracted_values["NganhHoc"]
            else: 
                NganhHocList = None
            
            if TruongList is None and NganhHocList is None:
                responseList.append({"key": "DiemChuan", "value": PREDEFINE_ANSWER_FAILED["DiemChuan"]})
            else:
                DiemChuanList = findDiemChuanByTruongNganh(TruongList, NganhHocList)
                if len(DiemChuanList) == 0:
                    responseList.append({"key": "DiemChuan", "value": getAnswer("DiemChuan", None, None)})
                else:
                    for n in DiemChuanList[:3]:
                        responseList.append({"key": "DiemChuan", "value": getAnswer("DiemChuan", None, n)})
                        
        if "KhoiThi" in self.intents.keys():
            if "Truong" in self.extracted_values.keys():
                TruongList = self.extracted_values["Truong"]
            else: 
                TruongList = None
            
            if "NganhHoc" in self.extracted_values.keys():
                NganhHocList = self.extracted_values["NganhHoc"]
            else: 
                NganhHocList = None
            
            if TruongList is None and NganhHocList is None:
                responseList.append({"key": "KhoiThi", "value": PREDEFINE_ANSWER_FAILED["KhoiThi"]})
            else:
                KhoiThiList = findKhoiThiByTruongNganh(TruongList, NganhHocList)
                if len(KhoiThiList) == 0:
                    responseList.append({"key": "KhoiThi", "value": getAnswer("KhoiThi", None, None)})
                else:
                    for n in KhoiThiList[:3]:
                        responseList.append({"key": "KhoiThi", "value": getAnswer("KhoiThi", None, n)})
        if "Truong" in self.intents.keys():
            if "NganhHoc" in self.extracted_values.keys():
                NganhHocList = self.extracted_values["NganhHoc"]
            else: 
                NganhHocList = None
            
            if "KhoiThi" in self.extracted_values.keys():
                KhoiThiList = self.extracted_values["KhoiThi"]
            else: 
                KhoiThiList = None
                
            if "DiemChuan" in self.extracted_values.keys():
                DiemChuanAvg = mean(list(self.extracted_values["DiemChuan"]))
            else: 
                DiemChuanAvg = None
            
            if NganhHocList is None and KhoiThiList is None and DiemChuanAvg is None:
                responseList.append({"key": "Truong", "value": PREDEFINE_ANSWER_FAILED["Truong"]})
            else:
                TruongList = findTruongByDiemThiKhoiNganh(DiemChuanAvg, KhoiThiList, NganhHocList)
                if len(TruongList) == 0:
                    responseList.append({"key": "Truong", "value": getAnswer("Truong", None, None)})
                else:
                    for n in TruongList[:3]:
                        responseList.append({"key": "Truong", "value": getAnswer("Truong", None, n)})
        
        return responseList   
    
    def getResponse(self):
        isDone = False
        if len(self.intents.keys()) == 0:
            # Cuộc hội thoại không hề có intent
            return isDone, PREDEFINE_RESPONSE["KhongHieu"]
        needAskList = cleanUpList(self.markIntentStatus())
        if len(needAskList) == 0:
            # Không tìm ra feature gì để hỏi nữa, trả lời người dùng luôn
            isDone = True
            return isDone, self.getAnswerNow()
        # Hỏi feature cần hỏi ,tốt nhất là nên hỏi feature quan trọng nhất, tuy nhiên tạm lấy phần tử dầu cho dễ debug
        featureToAsk = "Other"
        if needAskList[0] in PREDEFINE_RESPONSE.keys():
            featureToAsk = needAskList[0]
        self.asked_features.append(featureToAsk)
        return isDone, PREDEFINE_RESPONSE[featureToAsk]
        


# In[4]:


a = HuongNghiep_Graph()
# a.fill({}, {'HocPhi': ['Học phí của Trường đại học bách khoa có cao không?'], 'MaTruong': ['LOL'], 'KyTucXa': ['LOL'], 'LoaiHinh': ['LOL'], 'DiaChi': ['LOL']})
a.fill({}, {'Truong': ['LOL']})


# In[5]:


print(a.getResponse())


# In[10]:


a.fill({'DiemChuan':[25, 26]}, {})


# In[32]:


a.fill({'KhoiThi':['A00', 'B00']}, {})


# In[33]:


a.fill({'Truong':['BK', 'HCMUE']}, {})


# In[11]:


a.fill({'NganhHoc': ['Giáo dục Chính trị']}, {})


# In[24]:


a.toString()


# In[12]:


a.fill({}, {})


# In[ ]:


{25, 26}.union(set([15, 16]))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




