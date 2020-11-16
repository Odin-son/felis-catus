## Configs - mmdetection
### atss_r50_fpn_1x_coco.py 해석해보기 

#####1.'_base_' 
```
_base_ = [
    '../_base_/datasets/coco_detection.py',
    '../_base_/schedules/schedule_1x.py', '../_base_/default_runtime.py'
]
# dataset - 말그대로 데이터 셋, 데이터셋을 새로 만들고 싶으면 여기서 작업하면 됌 
# models - 학습에 사용되는 네트워크
# schedules - optimizer를 어떤걸 쓰는지..하이퍼파라미터에 관련된 것
```
#####2.'_model_'
 * part 1. pretrain model & backbone
```
model = dict(
    type='ATSS',
    pretrained='torchvision://resnet50',
    backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=True),
        norm_eval=True,
        style='pytorch'),
   ...

#backbone으로 무얼 쓸껀지, 여기서는 ResNet
```
 * part 2. neck 
```
    ...
    neck=dict(
        type='FPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        start_level=1,
        add_extra_convs='on_output',
        num_outs=5),
    ...
# neck은 뭔지 모르겠으나 Feature Pyramid Networ(FPN)
```
 * part 3. bbox_head
```
    ...
    bbox_head=dict(
        type='ATSSHead',
        num_classes=80,
        in_channels=256,
        stacked_convs=4,
        feat_channels=256,
        anchor_generator=dict(
            type='AnchorGenerator',
            ratios=[1.0],
            octave_base_scale=8,
            scales_per_octave=1,
            strides=[8, 16, 32, 64, 128]),
        bbox_coder=dict(
            type='DeltaXYWHBBoxCoder',
            target_means=[.0, .0, .0, .0],
            target_stds=[0.1, 0.1, 0.2, 0.2]),
        loss_cls=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            loss_weight=1.0),
        loss_bbox=dict(type='GIoULoss', loss_weight=2.0),
        loss_centerness=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0)))
    ...
#bbox_head도 뭔지 모르겠다..일단 loss fuction으로 FocalLoss를 쓴다는건 알겠네
```
#####3.training and testing settings
```
# training and testing settings
train_cfg = dict(
    assigner=dict(type='ATSSAssigner', topk=9),
    allowed_border=-1,
    pos_weight=-1,
    debug=False)
test_cfg = dict(
    nms_pre=1000,
    min_bbox_size=0,
    score_thr=0.05,
    nms=dict(type='nms', iou_threshold=0.6),
    max_per_img=100)

# train에서 ATSSAssigner라는 걸 사용하고 k는 9
# test에서는 nms를 사용하고 IoU는 0.6
```
#####4.optimizer
```
   ...
# optimizer
optimizer = dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0001)
   ...
# SGD, 확률적경사하강법으로 학습? learning-rate 는 0.1 momentum 0.9 
```

