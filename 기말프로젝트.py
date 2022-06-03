import numpy as np,cv2
import library.track_modul as tm

print(np.__version__) # 1.21.5
print(cv2.__version__) # 3.4.11
import sys
print(sys.version) # 3.7.8
"""
1. 관심영역을 그림판 모듈로 지정
2. Q 로 실행.
3. space bar로 관심영역을 다시 지정.

"""

pen_size = [10]  # 리스트로 사용해야 함수 안에서 사용 가능

flag_type = [0]  # 0번 상태 : 아무것도 아님 , 1번 상태 : 팬 모드, 2번 상태 :  지우개 모드


def onChange(pos):
    pen_size[0] = cv2.getTrackbarPos("size", "menu");

def draw_circle(event, x, y, flags, frame):  # 원 그리기

    if flag_type[0] == 1:  # pen 상태일 경우
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(grid, (x, y), pen_size[0], (0, 0, 100), -1)

        elif event == cv2.EVENT_LBUTTONUP:
            cv2.circle(grid, (x, y), pen_size[0], (0, 0, 100), -1)

        elif event == cv2.EVENT_MOUSEMOVE:
            if flags & cv2.EVENT_FLAG_LBUTTON:
                cv2.circle(grid, (x, y), pen_size[0], (0, 0, 100), -1)

    if flag_type[0] == 2:  # 지우개 상태일 경우
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(grid, (x, y), pen_size[0], (0, 0, 0), -1)

        elif event == cv2.EVENT_LBUTTONUP:
            cv2.circle(grid, (x, y), pen_size[0], (0, 0, 0), -1)

        elif event == cv2.EVENT_MOUSEMOVE:
            if flags & cv2.EVENT_FLAG_LBUTTON:
                cv2.circle(grid, (x, y), pen_size[0], (0, 0, 0), -1)
    cv2.imshow("frame", cv2.addWeighted(grid, 0.8, frame, 0.5, 0))
    # print("debug")

def butten_handler(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP and (x < 50) and (y < 50):
        flag_type[0] = 1  # pen 기능
    if event == cv2.EVENT_LBUTTONUP and (x < 100 and x > 50) and (y < 50):
        flag_type[0] = 2  # 지우개 기능



focus_point = None
def write_gauge(process_point):
    global grid, frame
    print("처리중 : ",round(process_point / (grid.shape[0] * grid.shape[1]) * 100 / 2), " %")

def draw_focuse_point():
    global focus_point
    while cv2.waitKey(1) != ord('q'):
        cv2.imshow("menu", menu)

    flag_type[0] = 0
    point1 = [0, 0]  # x, y
    max_height = 0
    max_width = 0
    min_height = grid.shape[0]
    min_width = grid.shape[1]

    x1, x2, y1, y2 = 0, 0, 0, 0

    process_size = grid.shape[0] * grid.shape[0]
    process_point = 0
    for y in range(grid.shape[0]):  # shape  return (y, x ,차원)
        flag = 0
        write_gauge(process_point )
        for x in range(grid.shape[1]):
            process_point += 1  # 프로세스 게이지 측정
            temp = grid[y, x, 2]
            if temp > 20:
                if x > max_width:
                    max_width = x  # 가장 오른쪽에 있는 값을 구하는 알고리즘
                    x1 = y

            if temp > 20 and flag != 1:
                flag = 1
                if x < min_width:
                    min_width = x  # 가장 왼쪽에 있는 값을 구하는 알고리즘
                    x2 = y

    for x in range(grid.shape[1]):  # shape  return (y, x ,차원)
        flag = 0  #
        write_gauge(process_point)
        for y in range(grid.shape[0]):
            process_point += 1  # 프로세스 게이지 측정
            temp = grid[y, x, 2]
            if temp > 20:
                if y > max_height:
                    max_height = y
            if temp > 20 and flag != 1:  #
                flag = 1
                if y < min_height:
                    min_height = y

    # point1 = (min_width, min_height)
    # point2 = (max_width, max_height)
    focus_point = (min_width, min_height, max_width - min_width, max_height - min_height)
    return focus_point

import math
def Random_Erasing_Procedure(img, width, height, S,  p = 0.5,  sl = 0.02, sh = 1/3, r1 = 0.3, r2 =  None) :  # 논문에서 가장 좋은 수치
    """
    :param img: Input image I
    :param width: Image size W
    :param height: Image size H
    :param S: Area of image
    :param p: Erasing probability p
    :param sl: Erasing area ratio range sl
    :param sh: and sh
    :param r1: Erasing acpect ratio range r1
    :param r2: and r2
    :return output_img : Erased image output_img;
    """
    # 다음의 알고리즘 설계도 참고 https://deepapple.tistory.com/8
    # 다음의 실제 라이브러리 코드 참고 https://timm.fast.ai/RandomErase

    while True :
            Se = random.uniform(sl, sh) * S
            re = random.uniform(r1, r2) # r1~r2 실수 랜덤
            # re = math.exp(random.uniform(*log_aspect_ratio))
            He = int(round(math.sqrt(Se * re)))
            We = int(round(math.sqrt(Se/re)))
            xe = random.randrange(0, width)
            ye = random.randrange(0, height)
            if xe + We < width and ye +He <= height :
                Ie = (xe, ye,xe+We, ye+He)
                output_img = img.copy()
                # output_img[ye:ye+He, xe:xe+We] = random.randrange(0, 255)
                for i in range(We) : # 랜덤한 지우개...
                    for j in range(He) :
                        output_img[ye+j,xe+i] = random.randrange(0, 255)
                return output_img




video_src = "./DJI_0089.MP4"
# video_src = "./target_movie2.mp4"
cap = cv2.VideoCapture(video_src)
ret, frame =  cap.read()


menu_w = 300
menu_h = 50
menu = np.full((menu_h, menu_w), 200, np.uint8)

cv2.namedWindow("menu") # 미리 선언
cv2.namedWindow("frame")
# cv2.namedWindow("grid")

# 트랙바
cv2.createTrackbar("size", "menu", 1 , 100, onChange)
cv2.setTrackbarPos("size", "menu", 20) # 3번째 인자 Trackbar 기본 값

pen_img = cv2.imread("./image/MicroSoft-Paint.png", cv2.IMREAD_GRAYSCALE)
eraser_img = cv2.imread("./image/eraser.png", cv2.IMREAD_GRAYSCALE)

pen_img = cv2.resize(pen_img, (50,50))
eraser_img = cv2.resize(eraser_img , (50,50))

menu[0:50, 0:50] = pen_img
menu[0:50, 50:100] = eraser_img

# 그리다 사이즈 지정
grid_size = (frame.shape[0], frame.shape[1], 3)
grid = np.zeros(grid_size, np.uint8) # 그리드 생성
# 그리도는 frame과 cv2.addweight 용도

# 마우스 이벤트 그림그리기
cv2.setMouseCallback('frame', draw_circle, frame) # 마지막 인자로 frame을 넘겨줌

# cv2.setMouseCallback('grid', draw_circle)
cv2.setMouseCallback('menu', butten_handler)



draw_focuse_point() # 그림 그리기

cnt = 0 # 저장할 이미지 이름 순서번호
import random
while True : # 추적
    ret, frame =  cap.read()
    if not ret: # 이미지 오류
        print('비디오 파일을 읽을 수 없습니다.')
        break

    if frame is None :
        print("완료되었습니다.")
        break;
    img, rect_point = tm.track_targeting(video_src, 1, focus_point , ret, frame, draw_focuse_point, draw_circle)
    cv2.imshow("frame", img)
    (x, y, w, h) = rect_point
    # https://foreverhappiness.tistory.com/112
    # https://affine.ai/data-augmentation-for-deep-learning-algorithms/
    # 데이터 증강 기법 참고

    # Genometric Transformation
    clip_img = img[int(y + 2):int(y + h - 2), int(x + 2):int(x + w - 2)]
    imgflip1 = cv2.flip(clip_img, 1) # flipping (horizontal) 좌우대칭
    imgflip0 = cv2.flip(clip_img, 0) # flipping (horizontal) # 상하대칭

    (h, w) = clip_img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), 25, 1.0)
    imgrot1 = cv2.warpAffine(clip_img, M, (w, h)) # Rotation

    (h, w) = clip_img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), 335, 1.0)
    imgrot0 = cv2.warpAffine(clip_img, M, (w, h))
    # Tranlation 는 구현 안함.. 이 또한 관심영역을 다시 설정하면된다.
    # Cropping 도 구현 안함.. cropping 이 필요하다면 중간에 관심영역을 다시 설정해주면 그만이다.

    # Random Erasing
    # 전체 부분을 일부 가리는 것, 물체의 전체 구조가 보존
    # -> 랜덤하게 지정된 영역의 pixel 에 값을 재할당
    # RE_img = clip_img.copy()
    img_h, img_w = clip_img.shape[:2]
    RE_img = Random_Erasing_Procedure(clip_img, img_w, img_h,  img_w * img_h,0, 0.02,  0.4,
                            1, 0.3) # 실제 논문에서 가장 결과가 좋았다는 수치.
    """
    :param img: Input image I
    :param width: Image size W
    :param height: Image size H
    :param S: Area of image
    :param p: Erasing probability p 프로젝트에서 사용 안함.
    :param sl: Erasing area ratio range sl   삭제 비율
    :param sh: and sh
    :param r1: Erasing acpect ratio range r1
    :param r2: and r2
    :return output_img : Erased image output_img;
    """

    # 추가부분
    cnt += 1
    # output_img = np.zeros((h, w), dtype=np.uint8)
    if cnt > 1:
        output_img = img[int(y + 2):int(y + h - 2), int(x + 2):int(x + w - 2)]

        if cnt % 30 == 0:
            cv2.imwrite("./output/image" + str(cnt // 15) + ".jpg", output_img)
            cv2.imwrite("./output/image" + str(cnt // 15) + "_flip1.jpg", imgflip1)
            cv2.imwrite("./output/image" + str(cnt // 15) + "_flip0.jpg", imgflip0)
            cv2.imwrite("./output/image" + str(cnt // 15) + "_rotate1.jpg", imgrot1)
            cv2.imwrite("./output/image" + str(cnt // 15) + "_rotate0.jpg", imgrot0)
            cv2.imwrite("./output/image" + str(cnt // 15) + "_ER.jpg", RE_img)

            # 회전 저장 옵션 만들기

cap.release()
cv2.destroyAllWindows()


