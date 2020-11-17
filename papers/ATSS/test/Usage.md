## How to use
### step-by-step 따라해보기
일단, 학습에 필요한 config/_base_ 안에 dataset, model, schedule 이 있음 (primitive)
* dataset : 데이터 셋에 대한 경로를 지정한다
* model : 학습에 사용할 네트워크 구성
* schedule : optimizer 같은거 선언

그리고 config 안에 모든걸 지시할 .py 파일은 이런식으로 구성한다.
```
_base_ = [
    '_base_/models/model.py',
    '_base_/datasets/changwoo.py',
    '_base_/schedules/schedule_1x.py', '../_base_/default_runtime.py'
]
```

train.py, test.py는 건드리지 않는 것 같음..
 