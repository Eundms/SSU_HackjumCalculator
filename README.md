# 숭실대 `전체/학기별`-`교양/전공` 평균평점 계산 코드
## [1] 요약
### ※ 특이 사항 ※ 
* [Decimal](https://docs.python.org/ko/3/library/decimal.html) : 십진 고정 소수점 및 부동 소수점 산술
### 
* (추가 예정) 그래프 

### 학기별 성적
```Python
학기별성적=myhackjum.get평점평균('학기',['교양필수','교양선택','일반선택'],['전공기초','전공필수','전공선택','융합필수'])
for key in 학기별성적:
  학기별성적[key]=np.floor(학기별성적[key]*100)/100
print(학기별성적)
```
![image](https://github.com/Eundms/SSU_HackjumCalculator/blob/master/img/%EC%A0%84%EC%B2%B4%EC%84%B1%EC%A0%81.png)

### 전체 성적
```Python
전체성적=myhackjum.get평점평균('전체',['교양필수','교양선택','일반선택'],['전공기초','전공필수','전공선택','융합필수'])
for key in ['전체평점평균','전공평점평균','교양평점평균']:
  전체성적[key]=np.floor(전체성적[key]*100)/100
print(전체성적)
```
![image](https://github.com/Eundms/SSU_HackjumCalculator/blob/master/img/%EC%A0%84%EC%B2%B4%EC%84%B1%EC%A0%81.png)

## [2] 사용 방법
### 1. 가상환경
> python -m venv venv  
> ./venv/Scripts/activate  
> pip install numpy pandas openpyxl  
> python main.py  

```Python
myhackjum=MyHackjum("./grade/hackjum.xlsx",Soongsil())
```

### 2. 성적 엑셀파일 준비
#### 1) 이수구분별 성적표를 PDF 형식으로 다운로드 받기 
![result](https://user-images.githubusercontent.com/50352139/223919954-6f3c4e09-3d84-45c0-adce-c052fa34e14b.JPG)

#### 2) PDF -> EXCEL 로 변환
![image](https://user-images.githubusercontent.com/50352139/223926794-d200a67c-c1d8-4099-8923-13931f4a9358.png)

#### 3) 주어진 엑셀 파일에 형식 맞춰 붙여넣기
![image](https://user-images.githubusercontent.com/50352139/223927280-3d216c33-84c4-45c3-898b-d8ce6c2bc9fd.png)

### 3. 실행
