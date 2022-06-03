import numpy as np, cv2

cnt =0
# 이미지 추적 추가
# 트랙커 객체 생성자 함수 리스트 ---①
# 참고사이트 : https://bkshin.tistory.com/entry/OpenCV-32-%EA%B0%9D%EC%B2%B4-%EC%B6%94%EC%A0%81%EC%9D%84-%EC%9C%84%ED%95%9C-Tracking-API
# track_targeting 함수는 참고 사이트의 코드를 함수로 변환해서 일부 수정한 코드입니다.

trackerIdx = 0  # 트랙커 생성자 함수 선택 인덱스
tracker = None # 클래스로 짤까 고민하다가 그냥...

bbox = None
frame_name = "image_proccessing"
isfirst  = True
def pass_def (a,b,c,d,e):
    pass
def track_targeting(video_src, delay, box_point, ret, frame, draw_focuse_point, draw_circle):
    global tracker
    global bbox, isfirst
    """src : "동영상 위치"
    delay : 1= 1초 딜레이
    box_point (x1, y1, x2, y2)
    ret : cv2.VideoCapture(video_src).read()[0]
    frame :  cv2.VideoCapture(video_src).read()[1]
    draw_focuse_point : 파이썬에서 함수는 일급 객체로 간주하기에 함수를 매개변수로 받을 수 있다. 
    작동 중 사용자가 원하면 중간에 그림판 모드로 변환하기 위해 멈추고 다시 함수 호출.
    
    draw_circle : 마우스 이벤트를 취소하고 다시 설정하기 위해 함수를 매개변수로 받습니다.
    """
    cv2.setMouseCallback('frame', pass_def, frame) ## callback 취소


    img_draw = frame.copy() # 매번 새로운 프레임을 받아옴
    if not (tracker is None): # 트랙커 생성 안된 경우
        ok, bbox = tracker.update(frame)   # 새로운 프레임에서 추적 위치 찾기 ---③
        (x,y,w,h) = bbox
        if ok: # 추적 성공
            cv2.rectangle(img_draw, (int(x), int(y)), (int(x + w), int(y + h)), \
                          (0,255,0), 2, 1)
        else : # 추적 실패
            cv2.putText(img_draw, "Tracking fail.", (100,80), \
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2,cv2.LINE_AA)


    key = cv2.waitKey(delay) & 0xff # 키 입력을 받아옴
    # roi = cv2.selectROI(win_name, frame, False) # 사각형 드래그 함수
    if key == ord(' ') or (video_src != 0 and isfirst): # 스페이스 바 입력시
        if isfirst is False :
            cv2.setMouseCallback('frame', draw_circle, frame)  ## callback 취소
            box_point = draw_focuse_point() # 관심 포인트 좌표 구하는 함수, 메인 코드에 있음.
            tracker = cv2.TrackerBoosting_create()  #
            tracker.init(frame, box_point)

        isfirst = False  # 최초 1회 작동을 보장
        if bbox is None : # tracker update 호출이 한번도 없을 때ㅑ:
            tracker = cv2.TrackerBoosting_create()  # 트랙커 객체 생성
            isInit = tracker.init(frame, box_point) #   tracker.init 초기화
            bbox =  box_point

    return img_draw, bbox # 관심영에 사각형이 그려진 이미지, 사각형 좌표 리턴

