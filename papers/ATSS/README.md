#### Bridging the Gap Between Anchor-based and Anchor-free Detection via Adaptive Training Sample Selection
> [ATSS](https://arxiv.org/abs/1912.02424) <br>

##### INTRO
###### 1. 분야에 대한 설명
- object-detection 분야는 anchor-based, anchor-free 분야로 나눌 수 있다.

- anchor-based) anchor-based는 one-stage method와 two-stage method로 나눌 수 있다.
- one-stage의 대표적인 방법은 retinaNet이며 이후 FCOS 와 비교를 한다.
- two-stage는 더 정확하지만 높은 계산량을 필요로 한다. (결과는 당연히 좋겠지)

- anchor-free) anchor-free는 keypoint-based 와 center-based로 나눌 수 있다.
- keypoint-based는 미리 정의된 keypoint나 자가학습한 keypoint를 사용해서 위치를 찾고, 공간정보로 묶는다(like clustering)
- center-based는 객체의 영역이나 중심점을 positive로 정의하고, 4 distance로 경계면에서 예측하는 것 (사실 무슨 소린지 모르겠음)

- 결국 anchor-free 방법이 anchor-based의 하이퍼파라미터를 제거해주는 효과와 일반화 성능에서 비슷하다고 할 수 있기에 잠재력이 있음!
- (따라서, 목표는 둘의 갭을 완화시키는것...이 논문에서는 ATSS를 사용하여 해결)

###### 2. 두 방법의 비슷한점
- one-stage anchor-based detector, RetinaNet
- center-based anchor-free detector, FCOS

- 둘은 분명 다른 파이프라인을 가지고 있지만, FCOS에서 이야기하는 포인트가 RetinaNet의 anchor-box의 중심점과 같다. (편의상 FCOS 에서 찾는 해당 포인트를 anchor point라 지칭)

- difference)

|Method|# of anchor|Def. pos/neg sample|regress starting status|
|:---:|:---:|:---:|:---:|
|RetinaNet|several per loc.|resort by IOU for pos and neg| regress the obj. bounding box from preset anchor box|
|FCOS|one per loc.|spatial and scale constraints to selected samples|obj. from anchor point|
