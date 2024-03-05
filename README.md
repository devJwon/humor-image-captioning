# humor-image-captioning

참여자: 가연, 재원, 조은

##<Pilot test>
1. 한국어 '제목학원' 데이터 (이미지+캡션) 14개 수집
→ 구글 이미지 크롤링 후 정제

2. 영어 '제목학원' 데이터(이미지+캡션) 14개 수집
→ from oxford_hic_data

*제목학원: 제목학원은 본래 유머 자료를 올리는 사이트에서 흔히 쓰이던 말로 이미지와 관련된 적절한 제목을 다는 컨테스트를 일컫는다. 이는 일본의 유머사이트 보케테에서 유래하였다. 

3. 한국어 및 영어 이미지에 대한 캡션 판별력 비교
3.1 실험 방법
→ ①해당 이미지에 대한 유머(사람 생성), ②다른 이미지에 대한 유머(사람 생성), ③해당 이미지 묘사(GPT-4V 생성)
→ GPT-4V가 정답 고르기!
3.2 실험 결과
→ 영어: 8/14, 한국어: 8/14

※ 실험 데이터를 늘려 영어와 한국어의 이미지 유머 캡셔닝 정확도를 비교할 예정
※ GPT-4V의 한국어 능력 및 한국에 대한 문화적 이해가 영어보다 부족하다고 가정! 현재는 인사이트 발견을 위해 한국어의 약세를 예상(?) 바라고(?) 있음
※ 이미지 유머 캡셔닝에 대한 영어와 한국어의 차이가 확실하게 밝혀진다면, 일본어를 추가로 실험할 계획도 있음

=============================================
##<추가 Pilot test 및 아이디어 정리>
한국어 및 영어 '제목학원' 데이터의 이미지만을 활용하여 캡션 생성을 진행해본 결과, 한국어의 유머 캡션 능력이 영어보다 현저히 떨어졌음. 멀티모달(vision+language) 모델의 유머 캡션 생성에 대한 평가 실험 진행 예정
ex. '제목학원'의 원 캡션 vs GPT-4V 생성 캡션 ← BLEU, ROUGE, BERT_SCORE, METEOR, CIDER etc 
ex. GPT-4V 생성 캡션에 대한 언어학적 분석 ← 정서적 풍부함, 문법 패턴 다양성, 유창성 etc
