import numpy as np
import pandas as pd
from decimal import Decimal
class HackjumCalculator:
  def __init__(self,학칙,교양이수구분=['교양필수','교양선택','일반선택'],전공이수구분=['전공기초','전공필수','전공선택','융합필수']):
    self.학칙=학칙
    self.교양이수구분=교양이수구분
    self.전공이수구분=전공이수구분
  def __makeData(self,hackjum):
    인정학점_성적={ #인정학점*성적 총합
        '교양':Decimal('0'),
        '전공':Decimal('0'),
        '채플':Decimal('0')
       }
    인정학점총합={ #인정학점 총합
        '교양':Decimal('0'),
        '전공':Decimal('0'),
        '교양P':Decimal('0'),
        '전공P':Decimal('0')}
    이수중={
    '전공':[],
    '교양':[]
    } # [('이수구분','과목명','인정학점'),...]

    for idx in range(len(hackjum)):
      row=hackjum.iloc[idx]
      if row['이수구분'] in self.교양이수구분: # 교양
        if row['성적']=='P': #교양 - P/F과목인 경우
          인정학점총합['교양P']+=row['인정학점']
        elif row['성적'] in self.학칙.gradeConverter.keys():# 교양 - 이수한 과목
          인정학점_성적['교양']+=(row['인정학점']*self.학칙.gradeConverter[row['성적']])
          인정학점총합['교양']+=row['인정학점']
        else:# 교양 - 이수중 과목
          이수중['교양'].append((row['이수구분'],row['과목명'],row['인정학점']))

      elif row['이수구분'] in self.전공이수구분: # 전공
        if row['성적']=='P': #전공 - P/F과목인 경우 
          인정학점총합['전공P']+=row['인정학점']
        elif row['성적'] in self.학칙.gradeConverter.keys(): #전공 - 이수한 과목
          인정학점_성적['전공']+=(row['인정학점']*self.학칙.gradeConverter[row['성적']]) 
          인정학점총합['전공']+=row['인정학점']
        else:# 전공-이수중 과목
          이수중['전공'].append((row['이수구분'],row['과목명'],row['인정학점']))
      else: #채플 ['교양필수', '교양선택', '전공기초', '전공필수', '전공선택', '융합필수', '채플'],
        인정학점_성적['채플']+=row['인정학점']
    return 인정학점_성적, 인정학점총합, 이수중   

  def __전체평점평균(self,hackjum):
    결과={'전체평점평균':0 , '전공평점평균': 0, '교양평점평균':0,'제외':{'교양P':0,'전공P':0,'이수중':0}}

    인정학점_성적, 인정학점총합, 이수중 = self.__makeData(hackjum) 
    
    결과['전체평점평균']=(인정학점_성적['전공']+인정학점_성적['교양'])/(인정학점총합['전공']+인정학점총합['교양'])
    결과['교양평점평균']=인정학점_성적['교양']/인정학점총합['교양']
    결과['전공평점평균']=인정학점_성적['전공']/인정학점총합['전공']
    결과['제외']['교양P']=인정학점총합['교양P']
    결과['제외']['전공P']=인정학점총합['전공P']
    결과['제외']['이수중']=이수중
    
    return 결과 # {전체평점평균: , 전공평점평균: , 교양평점평균:,'제외':{교양P:,전공P:,이수중:}}
  
  def __학기평점평균(self,hackjum):
    결과={}
    이수시기리스트=hackjum['이수시기'].unique()
    
    for 이수시기 in 이수시기리스트:
      이수시기별학점=hackjum.loc[hackjum['이수시기']==이수시기]
      인정학점_성적, 인정학점총합, 이수중 = self.__makeData(이수시기별학점) 
      결과[이수시기+'_전체평점평균']=0 if 인정학점총합['전공']+인정학점총합['교양']==0 else (인정학점_성적['전공']+인정학점_성적['교양'])/(인정학점총합['전공']+인정학점총합['교양'])
      결과[이수시기+"_전공평점평균"]=0 if 인정학점총합['전공']==0 else 인정학점_성적['전공']/인정학점총합['전공']
      결과[이수시기+'_교양평점평균']=0 if 인정학점총합['교양']==0 else 인정학점_성적['교양']/인정학점총합['교양']
    
    return 결과 # {'20XX-X학기_전공평점평균':전공평점평균,....}

  def caculate평점평균(self,myHackjum, group='전체'):# 총 평점 계산 = {P/F제외한 과목의 학점 * 성적}의 총합 / {P/F를 제외한 학점}의 총합
    결과={}
    if group=='전체': 
      결과=self.__전체평점평균(myHackjum.hackjum)
    elif group=='학기':
      결과=self.__학기평점평균(myHackjum.hackjum)
    else:
      결과="잘못된 group 요청입니다."
    return 결과
class University():
  def __init__(self):
    self.gradeConverter={}
    self.이수구분=[]

class Soongsil(University):
  def __init__(self):
    self.gradeConverter={'A+':Decimal('4.5'),'A0':Decimal('4.3'),'A-':Decimal('4.0'),'B+':Decimal('3.5'),'B0':Decimal('3.3'),'B-':Decimal('3.0'),'C+':Decimal('2.5'),'C0':Decimal('2.3'),'C-':Decimal('2.0')}
    self.이수구분=['교양필수','교양선택','전공기초','전공필수','전공선택','융합필수','일반선택']

class MyHackjum:
  
  def __init__(self,path='./grade/hackjum.xlsx',university=Soongsil()):
    def decimal_from_value(value):
      return Decimal(str(value))
    self.university=university
    df= pd.read_excel(path)
    df['인정학점']= df['인정학점'].apply(Decimal)
    self.hackjum=df
  def get평점평균(self,group="전체"):
      계산기=HackjumCalculator(self.university)
      return 계산기.caculate평점평균(self,group)  


FILE_PATH  = "./grade/hackjum.xlsx"

print("====학기별 성적====")
myhackjum=MyHackjum(FILE_PATH,Soongsil())
학기별성적=myhackjum.get평점평균('학기')
for key in 학기별성적:
  학기별성적[key]=np.floor(학기별성적[key]*100)/100
print(학기별성적)


print("====전체 성적====")
전체성적=myhackjum.get평점평균('전체')
for key in ['전체평점평균','전공평점평균','교양평점평균']:
  전체성적[key]=np.floor(전체성적[key]*100)/100
print(전체성적)


print("====학점 변화 그래프====")
from matplotlib import pyplot as plt
plt.rc('font', family='NanumBarunGothic') 

key=hackgi
name=['전체평점평균','전공평점평균']
for n in name:
  grade=[]
  for k in key:
    grade.append(학기별성적[n][k])
  plt.plot(key,grade,label=n)
  plt.legend()