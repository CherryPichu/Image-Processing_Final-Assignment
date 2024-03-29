﻿|영상처리프로그래밍|기말 프로젝트 보고서|작성자|허남정|
| :-: | :- | :- | :- |
|||작성일자|2022-06-03|


|프로젝트 시작 배경|<p>하나의 이미지 분류 모델은 만들기 위해서 굉장히 많은 이미지 데이터가 필요하다. 이때 드론으로 360도 동영상 촬영을 한다면 짧은 시간에 다양한 각도에서 많은 영상 데이터를 뽑아낼 수 있다. 그러나 숙련된 조종자가 아니면 드론 촬영은 대상 물체의 크기와 위치를 일정하게 촬영하지 못한다.</p><p>이 프로젝트는 드론 촬영 영상에서 사용자가 관심 영역을 지정하면 크기와 위치가 일정한 영상 데이터를 뽑아낼 수 있도록 도와주는 프로젝트이다. 또한 스마트폰이나 태블릿 등 실제 드론 조종에 사용되는 디바이스에서 쉽게 사용할 수 있도록 그림판 모듈을 제공한다.</p>|
| :-: | :- |
|프로젝트 결과물 구조 및 설명|<p>![](Aspose.Words.4a7b3439-8448-42fc-8594-91cfa98ca647.001.png)</p><p></p>|
|프로젝트 요구 사항|<p>1. 사용자는 그림판 모듈을 이용해 관심영역을 지정할 수 있다. (스마트폰, 태블릿 디바이스에서 유의)</p><p>2. 대상 물체의 크기와 상태가 변하면 사용자는 중간에 멈추고 다시 관심영역을 그릴 수 있어야 한다.</p><p>3. 관심영역에 있는 대상 물체를 다양한 데이터 증감 기법을 이용해서 좋은 데이터를 만들어야 한다.<br>   ■이 프로젝트에서 구현된 데이터 증감 기술<br>       - flipping 좌우대칭, 상하대칭<br>       - Rotation : 35도 회전, 335도 회전<br>       - Random Erasing (RE) : (논문 알고리즘을 구현) 전체 부분의 일부를 가리는 방법으로 객체의 일부가 가려지는 경우에도 신경망이 올바르게 예측하는데 도움이 된다.</p>|
|프로젝트 실행|![](Aspose.Words.4a7b3439-8448-42fc-8594-91cfa98ca647.002.png)|
|프로젝트 향후 계획|프로젝트 제작에서 각각의 필요한 모듈을 만들고 합치는 방향으로 진행되어 유지 보수가 어려운 코드가 나왔다. 이를 보완하기 위해서 하나의 클래스로 다시 만든다면 유지 보수가 개선된 좋은 코드가 나올 수 있을 것이다. 또한 **[참고자료1]** 이 페이지를 참고하여 향후에는 더 많은 데이터 증강 기법을 사용할 것이다.|
|참고자료|<p>[참고자료1]데이터 증강 기법의 종류</p><p><https://affine.ai/data-augmentation-for-deep-learning-algorithms/></p><p></p><p>Random Erasing 알고리즘</p><p><https://sh-tsang.medium.com/random-erasing-re-random-erasing-data-augmentation-image-classification-37f11627b38></p><p>RE 알고리즘 라이브러리 (코드리뷰용)</p><p><https://timm.fast.ai/RandomErase></p>|

