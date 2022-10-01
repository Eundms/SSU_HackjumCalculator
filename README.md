## 숭실대 `전체/학기별`-`교양/전공` 평균평점 계산 코드

### 특이 사항
* [Decimal](https://docs.python.org/ko/3/library/decimal.html) : 십진 고정 소수점 및 부동 소수점 산술
### 
* (추가 예정) 그래프 

#### 가상환경
> python -m venv venv
> ./venv/Scripts/activate
> pip install numpy pandas openpyxl
> python main.py

```Python
myhackjum=MyHackjum("./grade/hackjum.xlsx",Soongsil())
```
### 학기별 성적
```Python
학기별성적=myhackjum.get평점평균('학기',['교양필수','교양선택','일반선택'],['전공기초','전공필수','전공선택','융합필수'])
for key in 학기별성적:
  학기별성적[key]=np.floor(학기별성적[key]*100)/100
print(학기별성적)
```
![image]("./학기별성적.png")

### 전체 성적
```Python
전체성적=myhackjum.get평점평균('전체',['교양필수','교양선택','일반선택'],['전공기초','전공필수','전공선택','융합필수'])
for key in ['전체평점평균','전공평점평균','교양평점평균']:
  전체성적[key]=np.floor(전체성적[key]*100)/100
print(전체성적)
```
![image]("./전체성적.png")