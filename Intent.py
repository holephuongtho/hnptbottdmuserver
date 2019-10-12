#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import json
import itertools
from fuzzywuzzy import process,fuzz
from Extract import extract


# In[3]:


alias = dict()
attention = dict()


# In[4]:


attention['Truong'] = ['Trường', 'Truong', 'Trg', 'Truog'] 
alias['Truong'] = [
    'Trường gì',
    'Trường nào',
    'Truong gì', 
    'Truong nào',
    'Trg gì', 
    'Trg nào',
    'Truog gì ', 
    'Truog nào ',
    # ...
 ]


# In[5]:


attention['KhoiThi'] = ['Khối', 'Khoi'] 
alias['KhoiThi'] = [
    'Khối gì',
    'Khối nào',
    'Khoi gì',
    'khoi nào',
    # ...
]


# In[6]:


attention['DiemChuan'] = ['Điểm chuẩn', 'Điểm'] 
alias['DiemChuan'] = [
    'Điểm chuẩn bao nhiêu',
    'Điểm chuẩn tầm bao nhiêu',
    'Điểm chuẩn khoảng bao nhiêu',
    'Điểm chuẩn lấy bao nhiêu',
    'bao nhiêu Điểm',
    'tầm bao nhiêu Điểm',
    'khoảng bao nhiêu Điểm ',
    'lấy bao nhiêu Điểm',
    'Điểm bao nhiêu',
    'Điểm tầm bao nhiêu',
    'Điểm khoảng bao nhiêu',
    'Điểm lấy bao nhiêu',
    'bao nhiêu Đ',
    'tầm bao nhiêu Đ',
    'khoảng bao nhiêu Đ',
    'lấy bao nhiêu Đ',
    'Đ bao nhiêu',
    'Đ tầm bao nhiêu',
    'Đ khoảng bao nhiêu',
    'Đ lấy bao nhiêu',
# ...
 ]


# In[7]:


attention['NganhHoc'] = ['Ngành'] 
alias['NganhHoc'] = [
    'học ngành gì',
    'học ngành nào',
    'chọn ngành gì',
    'chọn ngành nào',
    'thi ngành gì',
    'thi ngành nào',
    'đi ngành gì',
    'đi ngành nào',
    'đi theo ngành gì',
    'đi theo ngành nào'
# ...
 ]


# In[8]:


attention['LoaiHinh'] = ['loại hình']

alias['LoaiHinh']= [
    'loại hình gì'
# ...
]


# In[9]:


attention['DiaChi'] = ['Địa chỉ', 'ĐC', 'DC' , 'ĐChi ' , ' DChi ',' Cơ Sở', ' CS']

alias['DiaChi']= [
'Địa chỉ ở đâu',
'ĐC ở đâu',
'DC ở đâu',
'ĐChỉ ở đâu',
'DChỉ ở đâu',
'Có mấy cơ sở'
]


# In[10]:


attention['KyTucXa'] = ['ký túc xá', 'KTX']
alias['KyTucXa']= [
'Có ký túc xá hay không',
'Có ký túc xá không'
]


# In[11]:


attention['MaTruong'] = ['Mã trường', 'Ký hiệu trường', 'Kí hiệu trường']

alias['MaTruong']= [
'Mã trường là gì',
'Mã trường?',
'Mã trường như thế nào',
'Mã trường thế nào',
'Ký hiệu trường là gì',
]


# In[12]:


attention['HocPhi'] = ['Học phí', 'HP', 'HPhí']

alias['HocPhi']= [
'Học phí bao nhiêu',
'Học phí có cao không',
'Một năm bao nhiêu',
'Bao nhiêu một năm',
'1năm bao nhiêu',
'Bao nhiêu 1 năm',
'Học phí thế nào',
'Bao nhiêu 1 học kỳ',
'1 học kỳ bao nhiêu',
'Bao nhiêu một học kỳ',
'một học kỳ bao nhiêu',
# ...
]


# In[13]:


def score_similarity(text, key):
    a1 = process.extract(text, alias[key])
    a2 = process.extract(text, attention[key], scorer=fuzz.token_set_ratio)          
#     print('a1', a1, 'a2', a2)
    score_list = list()
    for i in range(len(a1)):
        score = 0;
        score_a1 = a1[i][1];
#         score_a3 = fuzz.ratio(text, a1[i][0])
        for j in range(len(a2)):
            score_a2 = a2[j][1]
            score = max(score, harmony(score_a1, score_a2))
        score_list.append((a1[i][0], score))
    return score_list


# In[14]:


def harmony(a, b, c=None):
    if c is None:
        if a == 0 or b == 0:
            return 0
        return 2*a*b/(a+b)
    else:
        if a == 0 or b == 0 or c == 0:
            return 0
        return 3*a*b*c/(a*c + a*b + b*c)


# In[15]:


DEFINED_INTENTS = ["Truong", "KhoiThi", "DiemChuan", "NganhHoc", "LoaiHinh", "DiaChi", "KyTucXa", "MaTruong", "HocPhi"]
INTENT_THRESHOLD = 87 #magical number
MIN_NORMAL_LENGTH = 3 #Những normal nào length quá ngắn thì sẽ filter đi vì không có ý nghĩa xác định intent
def get_candidate_intent(list_normal_text):
    print('Input: ' + str(list_normal_text))
    candidate_intent_dict = dict()
    if list_normal_text is None:
        return candidate_special_intent_dict
    for text in list_normal_text:
        text = text.strip()
        if len(text) < MIN_NORMAL_LENGTH:
            continue
        for intent in DEFINED_INTENTS:
            list_score = score_similarity(text, intent)
            list_score.sort(key=lambda tup: tup[1], reverse = True)
            best = list_score[0]
            if best[1] > INTENT_THRESHOLD:
                print("Similarity score of [", text,"]: ", best)
                if intent in candidate_intent_dict:
                    candidate_intent_dict[intent].append(text)
                else:
                    candidate_intent_dict[intent] = [text]
    print('Output: ' + str(candidate_intent_dict))
    return candidate_intent_dict


# In[1]:


def extract_and_get_intent(text):
#     try:
#         text = compound2unicode(text)
#         if text.count(" ") == 0:
#             text = text + "."
#         for k,v in MAPPING_DICT.items():
#             text = text.replace(k, v)
            
        print('\nINPUT: ' + text)
        extracted = extract(text)
        extracted_dict = dict()
        for extractEle in extracted:
            key = extractEle['key']
            value = extractEle['value']
            if key not in extracted_dict.keys():
                extracted_dict[key] = [value]
            else:
                if value not in extracted_dict[key]:
                    extracted_dict[key].append(value)
        extracted_dict_keys = extracted_dict.keys() 
        candidate_intent_dict = get_candidate_intent([text]) 

        for key in DEFINED_INTENTS:
            if key in extracted_dict_keys and key in candidate_intent_dict.keys():
                candidate_intent_dict.pop(key)
                

        print('\n     OUTPUT: INTENT:' + str(candidate_intent_dict))
        print('\n     OUTPUT: EXTRACT:' + str(extracted_dict))
        return extracted, extracted_dict, candidate_intent_dict


# In[17]:


extract_and_get_intent("Trường giao thông vận tải học phí có cao không?")


# In[18]:


extract_and_get_intent("Em không biết thì trường gì")


# In[19]:


extract_and_get_intent("Khoa học và kỹ thuật máy tính")


# In[20]:


extract_and_get_intent("25")


# In[21]:


extract_and_get_intent("Trường Thủ Dầu Một có ký túc xá không? học phí như thế nào?")


# In[ ]:




