#### Bridging the Gap Between Anchor-based and Anchor-free Detection via Adaptive Training Sample Selection
> [ATSS](https://arxiv.org/abs/1912.02424) <br>

##### INTRO
###### 1. 분야에 대한 설명
* object-detection 분야는 anchor-based, anchor-free 분야로 나눌 수 있다.
* anchor-based) anchor-based는 one-stage method와 two-stage method로 나눌 수 있다.
  * one-stage의 대표적인 방법은 retinaNet이며 이후 FCOS 와 비교를 한다.
  * two-stage는 더 정확하지만 높은 계산량을 필요로 한다. (결과는 당연히 좋겠지)
* anchor-free) anchor-free는 keypoint-based 와 center-based로 나눌 수 있다.
  * keypoint-based는 미리 정의된 keypoint나 자가학습한 keypoint를 사용해서 위치를 찾고, 공간정보로 묶는다(like clustering)
  * center-based는 객체의 영역이나 중심점을 positive로 정의하고, 4 distance로 경계면에서 예측하는 것 (사실 무슨 소린지 모르겠음)
* 결국 anchor-free 방법이 anchor-based의 하이퍼파라미터를 제거해주는 효과와 일반화 성능에서 비슷하다고 할 수 있기에 잠재력이 있음!
* (따라서, 목표는 둘의 갭을 완화시키는것...이 논문에서는 ATSS를 사용하여 해결)

###### 2. 두 방법의 비슷한점
* one-stage anchor-based detector, RetinaNet
* center-based anchor-free detector, FCOS
  * 둘은 분명 다른 파이프라인을 가지고 있지만, FCOS에서 이야기하는 포인트가 RetinaNet의 anchor-box의 중심점과 같다. (편의상 FCOS 에서 찾는 해당 포인트를 anchor point라 지칭)
* difference)

|Method|# of anchor|Def. pos/neg sample|regress starting status|
|:---:|:---:|:---:|:---:|
|RetinaNet|several per loc.|resort by IOU for pos and neg| regress the obj. bounding box from preset anchor box|
|FCOS|one per loc.|spatial and scale constraints to selected samples|obj. from anchor point|

  * 결론적으로는 두번째 항목인 pos/neg sample에 대한 정의를 같게한다면 결과는 크게 차이나지않는다는 점. 
    * 놀랍구먼..

##### Related work
###### 1. Anchor-based detector
 * Two-stage method) 
   * 대표적으로 그 유명한 Faster R-CNN(2017)은 region proposal network(RPN) 와 region-wise prediction network(R-CNN)으로 구성된다.
   이 방법이 해당 분야에 지배적이였다고 함.
   그리고 그동안 다양한 방법들이 시도되었는데...뭐 구조를 바꾼다던지, 손실함수를 바꾼다던지, feature fusion을 한다던지..무튼, 요즘에도 two-stage 방법으로 벤치마크를 한다고함(2019년 기준)
 * One-stage method) 
   * SSD(2016)는 높은 연산 효율로 관심을 끌었다(닉값하는듯). 
   SSD는 오브젝트의 카테고리와 anchorbox offset을 바로 예측하기 위해 ConvNet의 multi-scale layer에 anchor box를 펼친다(spread out).
   무튼, 잘 찾는다는 소리겠지. 이것도 유행이 됐는지 그 뒤로 다른 관점에서 보는 방법으로 여러 시도들을 했나봄. 가령 구조를 바꾼다던지 등등.. 
   현재는 더 빠른 속도로 two-stage랑 거의 비슷한 성능이라고 함(2019년 기준)
 
###### 2. Anchor-free detector
 * Keypoint-based method) 미리 정의되거나 자가학습한 키포인트들로 위치를 찾고 박스를 생성함
   * CornerNet는 (top-left,bottom-right) 이런 페어의 키퐁니트로 오브젝트의 바운딩 박스를 찾음
   * Grid R-CNN의 두번째 단계는 FCN의 민감한장점(?)을 가지고 grid point를 예측하고 그리드를 가이드삼아 바운딩 박스를 결정한다. 
   * ExtremeNet은 4개의 포인트(상하좌우)와 중앙점을 탐지함
   * Zhu 의 방법은 키포인트 추정을 사용하여 객체의 중심점을 찾고 3D 위치, 방향, 자세와 같은 다른 속성으로 예측함
   * CenterNet은 CornerNet의 확장판으로, 페어가 아니라 트리플로해서...무튼 precision recall을 개선했다고 함
   * RepPoint는 샘플 포인트의 집합으로 객체를 나타내는데...객체를 구분하기 위해 시멘틱 영역의 정보를 사용했음
 * Center-based method) 오브젝트의 중심을 positive로 정의하고, 오브젝트 바운딩 박스의 4방향까지의 거리를 예측함. (이게 4 distance 인듯..)
   * YOLO는 이미지를 S x S grid로 나누고, 찾아낸 객체의 중심점을 포함하는 grid cell은 이 물체를 탐지하는 것...(오..이런거였구만)
   * DenseBox는 객체의 중앙부터 채워진 원(filled circle)을 사용하여 이를 positive로 정의하고, 바운딩 박스의 4방향을 찾음 (핵심은 원이네)
   * GA-RPN은 Faster R-CNN 을 좀 더 향상 시키기 위해 오브젝트의 중심영역을 positive로 정의했다. 다른 방법들도 추가로 했음. ( 괜히 헷갈리게 써놨네..)
   * FSAF는 RetinaNet에 'online feature selection'을 더함 (온라인..?이게 뭐람..)
   * 최근 트랜드는 오브젝트의 중심 영역을 positive로 정의하여 그 경계까지의 4 거리를 예측함. (원래 센터 포인트였는데 조금 더 offset을 준듯)
   * FCOS는 오브젝트 바운딩 박스안에 모든 위치를 4 거리와 물체를 감지할 수 있는 novel centerness score를 사용했음 (score 쓴게 큰듯)
   * CSP는 보행자 검출을 위해 오브젝트 박스의 중심점과 그 비율을 조정했음 (aspect ratio 를 비율이라고 했음)
   * FoveaBox는 오브젝트의 middle part를 positive라고 보고 4 거리를 측정했음
 * (결국, 각각의 방법들은 비슷한 연구를 했다..이말이 하고 싶은것 같다 왜냐면 related work니까)
  
##### Difference Analysis of Anchor-based and Anchor-free Detection
(집요하게 RetinaNet이랑 FCOS를 가지고 차이를 분석해보려 한다)

###### 3.1 Experiment Setting
 * Dataset
   * MS COCO
   
   |Category|# of imgs|split|
   |:---:|:---:|:---:|
   |Train|115K|trainval35k|
   |Valid.|5K|minival|
 
 * Training Detail
   * pretrain 모델로 ResNet-50을 사용하고, 5레벨 특징 피라미드 구조를 백본으로 사용 (what is backbone...)
   * RetinaNet의 경우, 5-레벨 형상 피라미드의 각 층은 8S(stride) anchor size임 (anchor box 크기 말하는듯)
   * iter 90K, 0.9 momentum, 0.0001 가중치 감소와 16배치사이즈, learning-rate 0.01, 60K,80K 에서 0.1로 감소 (왜 감소지..0.01 -> 0.1인데)
 * Inference Detail
   * 학습과 같이 입력 영상 사이즈를 조정하고 predict.
   * 그 후엔 0.05 로 배경 바운딩 박스를 제거하고, feature pyramid당 상위 1000개를 뽑음
   * NMS(non-maximum suppression)는 클래스당 IOU 0.6을 적용하여 이미지당 상위 100개 탐지를 함
 
###### 3.2 Inconsistency Removal
 * ![table1](https://user-images.githubusercontent.com/33476636/99183370-8b380900-277e-11eb-8248-19d5d56ca1dc.png)
 * RetinaNet에서 위치당 한개 정방 앵커박스를 사용하면 결과가 FCOS랑 거의 같다
 * 하지만, FCOS는 AP 성능이 RetinaNet을 능가하는데, 그 차이 중 GIoU 손실함수나 일반적인 개선사항이 일부를 차지함 (저런 방법들을 사용해서 높다고 주장함)
 * (뭘 개선했나..GroupNorm, GIoU regression loss func, limiting pos samples in the GT 등)
 * 이러한 개선사항은 앵커 기반 검출기에도 적용될 수 있으므로, 이는 본질적인 차이는 아니다.
 * 따라서, 이런 구현상 불일치를 배제하고 한다. 이런걸 더해도 0.8% 밖에 차이가 안난다.

###### 3.3 Essential Difference
 * Classification
   * ![fig1](https://user-images.githubusercontent.com/33476636/99183325-34caca80-277e-11eb-9f84-3350b756cf5e.png)
   * RetinaNet은 IOU를 사용하여 다른 피라미드 레벨의 앵커박스를 positive, negative로 나눔, 다른건 학습 과정 중 무시 (anchor box)
   * FCOS는 다른 피라미드 레벨에서 spatial로 후보군을 정하고, scale constraint로 찾음. (anchor point)
   * (비슷하지만 살짝 다름)
   * ![table2](https://user-images.githubusercontent.com/33476636/99183592-52009880-2780-11eb-9868-6d107aee748b.png)
   * 위치당 앵커가 하나인 RetinaNet은 IOU 대신 FCOS처럼 하면 그 0.8%를 채울 수 있다. 그리고 FCOS를 IOU 써서 샘플을 선택하면 36.9%로 떨어진다..(결국 이 데이터 샘플링 과정이 중요함)
   * 결국 이런 데이터 샘플에 대한 정의를 하는게 중요한 차이점이란거다. (between anchor-based and anchor-free)
 * Regression
   * ![fig2](https://user-images.githubusercontent.com/33476636/99183570-3d240500-2780-11eb-904f-aef7dc741a33.png)
   * RetinaNet은 anchor box 로 부터 시작하고, FCOS는 point로 부터 시작함
   * 무튼, 시작점은 그리 중요하지않음
 * Conclusion
   * 중요한 차이점은 positive/negative training sample을 어떻게 정의하는지가 중요함 (그래서 연구가치가 있음)
