##### two-stage detector
selective search 이후 R-CNN의 기술은 two-stage에 근간이 되는 논문임.
보통 R-CNN 계열의 모델들은 region proposal stage(1), classification stage(1)가 되어있어서 two-stage detector라 불림

##### R-CNN
selective search를 딥러닝에 적용한 알고리즘. ILSVRC 2012 의 AlexNet을 CNN 모델로 사용하여, transfer learning (pretrained AlexNet)
- 1.Selective search 를 통해 ROI를 약 2000개 가량 추출
- 2.ROI 크기를 조절해 동일한 사이즈로 만듦
- 3.ROI를 CNN에 넣어 feature 추출
- 4.추출된 걸 SVM에 넣어 classification
- 5.추출된 걸 regression에 넣어 bbox 예측

<img src="https://user-images.githubusercontent.com/31475037/74123157-088f8580-4c11-11ea-8555-39cfb5d770c0.gif" width="50%" height="50%">

- 문제점 : end-to-end 방식이 아님(따로따로 학습해야함; CNN, classifier, bbox regression), 시간이 너무 오래걸림

##### Fast R-CNN
학습과는 별개로 selective search에서 얻어진 2000개를 넣는게 아니라 이미지 통채로 CNN에 넣음
따라서, R-CNN에서 CNN 2000번 하던걸 한번으로 줄임

Fast R-CNN ; ROI projection, SPPNet

####### ROI projection
feature map 상에 있는 ROI를 구하기 위한 프로세스
- 이미지에 대해 selective search 를 통해 ROI 획득
- 구해진 ROI 좌표값을 feature map에 projection -> feature map 상에 ROI
(이때 feature map과 입력의 해상도는 동일)

<img src="https://user-images.githubusercontent.com/31475037/74294049-1283c680-4d80-11ea-8c68-fa1b84f52bd3.png" width="50%" height="50%">

이러한 ROI projection이 가능한 이유는 CNN을 통해 추출된 feature map에 이미지와 같이 물체의 중요한 정보가 담겨있기 때문

####### SPP(Spatial Pyramid Pooling)
SPPNet은 R-CNN에서 resize(wraping)하는 과정을 SPP를 이용해 고정크기로 바꿈. 
SPP layer는 다양한 크기의 입력으로 부터 일정한 크기의 feature를 추출가능.
- 이미지를 일정 개수 지역으로 나눈 뒤, 각 지역에 BOW(Bag-of-words)를 적용하여 local 정보를 유지 (무슨소리지..)
암튼, SPP layer는 feature map 상의 특정 영역에 대해 고정된 개수의 영역으로 나눈 뒤, 
각 영역에 대해 max-pooling/average pooling을 취함으로써 고정된 길이의 feature를 추출
<img src="https://1.bp.blogspot.com/-4XYvgIQ6T8E/VZEPbZyYo7I/AAAAAAAABHE/D_HccWnYK6Q/s1600/s4.jpg" width="50%" height="50%">
Fast R-CNN에서는 이런 SPP layer의 single level pyramid만 사용하여 이를 ROI layer 라고 명명함

따라서, Faster R-CNN의 과정은
- 전체 이미지를 CNN에 넣어 feature 추출 (한번만)
- ROI projection을 통해 feature map 상의 ROI를 구함
- 이 ROI는 ROI layer를 통과한후 일정 크기의 feature가 됌
- 추출된 이 feature는 fc layer(fully connected layer)를 통과해 나온 뒤, classification, bbox regression
(이때, end-to-end)

##### Faster R-CNN
문제가 된 selective search 부분을 RPN(Region Proposal Network)로 대체

####### RPN 
RPN은 내부 feature map의 영역 내에서도 충분히 객체의 위치,특징정보가 남아 있기에 이 feature map 정보를 통해 학습을 하는 방식
RPN에서 각각의 영역을 어떻게 학습할지에 대해 도입한 개념이 anchor box,
anchor를 중심으로 anchor box를 설정해 feature map에서 영역을 설정함.
- anchor box를 사용하면 transaltion-invariance, reduce model size

<img src="https://user-images.githubusercontent.com/31475037/74295754-4ca39700-4d85-11ea-96ef-99320b686da5.png" width="80%">

이 이전에는 translation-invariance를 하기 위해 scale도 조정해보고, filter size도 이용해보고..

<img src="https://user-images.githubusercontent.com/31475037/74295756-4ca39700-4d85-11ea-9a1b-0f9a7fe64e1d.png" width="80%">

RPN의 목적은 객체를 잘 분류하는게 아니라, 객체가 있는 영역인 positive anchor box를 잘 찾는것.
positive/negative : GT box IoU 0.7 이상/ 0.3 이하
0.3~0.7은 사용하지않음
실제 사용한 앵커박스는 위치당 scale 3 ratio 3 = 9개

<img src="https://user-images.githubusercontent.com/31475037/74295761-4dd4c400-4d85-11ea-8a26-5387a5a063b8.png" width="60%">

한 이미지당 앵커를 256개 샘플링함 -> 1:1 비율로 positive/negative로 RPN 에 넣어주면, 해당 anchor에 object가 있는지 이진분류하는 classifer를 학습하고
앵커 내 물체의 위치를 찾는 bbox regression을 해줌. (만약 positive anchor 갯수가 128개보다 적을경우, 빈자리는 negative anchor sample로 채움)
- bbox regression은 smooth L1 Loss

###### detector 학습
현재는 그냥 두단계로 학습

<img src="https://user-images.githubusercontent.com/31475037/74295747-4ad9d380-4d85-11ea-9be8-f6e63e901f6f.png" width="50%" height="50%">

- RPN과 CNN만 따로 학습
- RPN과 CNN은 freeze한채로 detector만 학습
- CNN은 freeze한채로 RPN만 finetuning
- RPN과 CNNs freeze한채로 detector finetuning

###### 후처리 기법

- confidence score threshold, NMS threshold,
  - 낮은 score의 bbox는 사용하지 않고, 이후 겹치는 IOU가 nms 보다 높으면 가장 높은 score만 남김
- NMS(Non-Maximum Suppression)
  - RPN -> 한 객체당 여러개의 region -> NMS

##### FPN

- HOG와 SIFT 같은 feature pyramid를 이용한 방법을 딥러닝에 적용시킨 것. 각 scale 마다 CNN 으로 feature 추출, 마지막 feature map에서 prediction
- Bottom-up 방식으로 이미지를 본다고도 불림

<img src="https://user-images.githubusercontent.com/31475037/74511677-def49800-4f49-11ea-96ff-9ed82d42dc8e.png" width="30%">

- Bottom-up(픽셀부터 특징을 계산) + Top-down (이미지 전체를 보고 원하는 특징을 찾음)
 
<img src="https://user-images.githubusercontent.com/31475037/74511675-de5c0180-4f49-11ea-96fa-730c64517ead.png" width="50%">

- 1x1 conv 로 채널을 맞춰줌

<img src="https://user-images.githubusercontent.com/31475037/74509754-9e931b00-4f45-11ea-858f-b77b08141d3d.png" width="40%">



 
