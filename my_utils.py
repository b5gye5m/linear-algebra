import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

INF = 1000    # TIE Fighter 그림판 크기
INF_X = 600   # 스타십 그림판 가로 범위
INF_Y = 1000  # 스타십 그림판 세로 범위
LEN = 100     # 처음 사각형의 크기
ROCKET_W = 150
NOSE_TIP_Y = 850
NOSE_H = 130
SHIP_H = 630                          # 노즈콘 포함
BOOSTER_H = 770
SHIP_BOTTOM_Y = NOSE_TIP_Y - SHIP_H   # 220
NOZZLE_Y = SHIP_BOTTOM_Y - BOOSTER_H  # -550
ENGINE_H = 50

# 그림판, 사각형 그리기
def draw_axis(ax):  # TIE Fighter용
  ax.axhline(0, color='black', alpha=0.3)  # x-axis line
  ax.axvline(0, color='black', alpha=0.3)  # y-axis line
  ax.set_xlim(-INF, INF)
  ax.set_ylim(-INF, INF)
  ax.set_aspect('equal')  # 정사각형 모양으로 backboard 그리기

def draw_canvas(ax):  # 스타십용 (세로로 긴 그림판, 축 숨김)
  ax.set_xlim(-INF_X, INF_X)
  ax.set_ylim(-INF_Y, INF_Y)
  ax.set_aspect('equal')  # 사각형이 찌그러지지 않게 비율 유지
  ax.axis('off')          # 축, 눈금 숨기기

def draw_rectangle(ax, p1, p2, p3, p4, color='C0', edge='none', alpha=1.0):
  my_polygon = Polygon([p1, p2, p3, p4], facecolor=color, edgecolor=edge, alpha=alpha)
  ax.add_patch(my_polygon)


# 변환 구현
# 점 p를 x축 방향으로 dx만큼, y축 방향으로 dy만큼 이동시킨 점 q를 구할 것
# q = T(dx, dy)·p1
def translate(p, dx, dy):
  # 1. 동차좌표계 (homogeneous coordinate)으로 변환
  hp = np.array([p[0], p[1], 1.0])

  # 2. 이동 변환 행렬 생성
  m = np.array([[1.0, 0.0, dx], [0.0, 1.0, dy], [0.0, 0.0, 1.0]])

  # 3. 행렬과 벡터의 곱
  q = np.dot(m, hp)  # (3,3) x (3,1) -> (3,1)
  #print(q)

  # 4. 2차원 좌표계로 변환
  q = np.array([q[0], q[1]])
  return q

# 점 p를 theta 만큼 회전 시킨 q
# q = R(theta)·p
def rotate(p, theta):
  # 1. 동차좌표계로 (homogeneous coordinate)로 변환
  hp = np.array([p[0], p[1], 1.0])

  # 2. 회전 변환 행렬 생성
  m = np.array([[np.cos(theta), -(np.sin(theta)), 0.0], [np.sin(theta), np.cos(theta), 0.0], [0.0, 0.0, 1.0]])

  # 3. 행렬과 벡터의 곱
  q = np.dot(m, hp)

  # 4. 2차원 좌표계로 변환
  q = np.array([q[0], q[1]])
  return q

# 점 p를 x축으로 sx만큼, y축으로 sy만큼 스케일링 한 q
# q = S(sx, sy)·p
def scale(p, sx, sy):
  # 1. 동차좌표계로 (homogeneous coordinate)로 변환
  hp = np.array([p[0], p[1], 1.0])

  # 2. 크기 변환 행렬 생성
  m = np.array([[sx, 0.0, 0.0], [0.0, sy, 0.0], [0.0, 0.0, 1.0]])

  # 3. 행렬과 벡터의 곱
  q = np.dot(m, hp)

  # 4. 2차원 좌표계로 변환
  q = np.array([q[0], q[1]])
  return q

# 점 p를 x축으로 sx만큼 밀림 변환 한 q
# q = Shx(sx)·p
def shear_x(p, sx):
  # 1. 동차좌표계 (homogeneous coordinate)로 변환
  hp = np.array([p[0], p[1], 1.0])

  # 2. x축 밀림 변환 행렬 생성
  m = np.array([[1.0, sx, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

  # 3. 행렬과 벡터의 곱
  q = np.dot(m, hp)

  # 4. 2차원 좌표계로 변환
  q = np.array([q[0],q[1]])
  return q

# 점 p를 y축으로 sy만큼 밀림 변환 한 q
# q = Shy(sy)·p
def shear_y(p, sy):
  # 1. 동차좌표계(homogeneous coordinate)로 변환
  hp = np.array([p[0], p[1], 1.0])

  # 2. y축 밀림 변환 행렬 생성
  m = np.array([[1.0, 0.0, 0.0], [sy, 1.0, 0.0], [0.0, 0.0, 1.0]])

  # 3. 행렬과 벡터의 곱
  q = np.dot(m, hp)

  # 4. 2차원 좌표계로 변환
  q = np.array([q[0],q[1]])
  return q

# 점 p를 x축 기준으로 반전한 q
# q = Rfx·p
def reflect_x(p):
  # 1. 동차좌표계(homogeneous coordinate)로 변환
  hp = np.array([p[0], p[1], 1.0])

  # 2. x축 기준 반전 변환 행렬 생성
  m = np.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]])

  # 3. 행렬과 벡터의 곱
  q = np.dot(m, hp)

  # 4. 2차원 좌표계로 변환
  q = np.array([q[0],q[1]])
  return q

# 점 p를 y축 기준으로 반전한 q
# q = Rfy·p
def reflect_y(p):
  # 1. 동차좌표계(homogeneous coordinate)로 변환
  hp = np.array([p[0], p[1], 1.0])

  # 2. y축 기준 반전 변환 행렬 생성
  m = np.array([[-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

  # 3. 행렬과 벡터의 곱
  q = np.dot(m, hp)

  # 4. 2차원 좌표계로 변환
  q = np.array([q[0],q[1]])
  return q

# 점 p를 원점 기준으로 반전한 q
# q = Rfo·p
def reflect_origin(p):
  # 1. 동차좌표계(homogeneous coordinate)로 변환
  hp = np.array([p[0], p[1], 1.0])

  # 2. 원점 기준 반전 변환 행렬 생성
  m = np.array([[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]])

  # 3. 행렬과 벡터의 곱
  q = np.dot(m, hp)

  # 4. 2차원 좌표계로 변환
  q = np.array([q[0], q[1]])
  return q

# 점 p를 y=x 기준으로 반전한 q
# q = Rfxy·p
def reflect_xy(p):
  # 1. 동차좌표계(homogeneous coordinate)로 변환
  hp = np.array([p[0], p[1], 1.0])

  # 2. y=x 기준 반전 변환 행렬 생성
  m = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])

  # 3. 행렬과 벡터의 곱
  q = np.dot(m, hp)

  # 4. 2차원 좌표계로 변환
  q = np.array([q[0], q[1]])
  return q


# TIE Fighter 파트 그리기
def draw_cockpit(ax, p1, p2, p3, p4):  # 중앙 조종석
  # 1. 사각형을 원점으로 이동 변환: T(-LEN/2, -LEN/2)
  # q = T(-LEN/2, -LEN/2)p
  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4 = translate(p4, -LEN/2, -LEN/2)

  # 2. 크기 변환: S(5, 5)
  s = 5
  q1 = scale(q1, s, s)
  q2 = scale(q2, s, s)
  q3 = scale(q3, s, s)
  q4 = scale(q4, s, s)

  # 3. 회전 변환: R(pi/4)
  q1 = rotate(q1, np.pi/4)
  q2 = rotate(q2, np.pi/4)
  q3 = rotate(q3, np.pi/4)
  q4 = rotate(q4, np.pi/4)

  # 4. polygon 그리기
  draw_rectangle(ax, q1, q2, q3, q4)

def draw_left_arm(ax, p1, p2, p3, p4): #왼쪽 날개축
  # 위쪽 날개축
  # 1. 사각형을 원점으로 이동변환: T(-LEN/2, -LEN/2)
  # q = T(-LEN/2, -LEN/2)p
  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4 = translate(p4, -LEN/2, -LEN/2)

  # 2. 크기 변환: S(6, 0.8)
  q1 = scale(q1, 6, 0.8)
  q2 = scale(q2, 6, 0.8)
  q3 = scale(q3, 6, 0.8)
  q4 = scale(q4, 6, 0.8)

  # 3. y축 기울기: shy(-0.2)
  q1 = shear_y(q1, -0.2)
  q2 = shear_y(q2, -0.2)
  q3 = shear_y(q3, -0.2)
  q4 = shear_y(q4, -0.2)

  # 4. 이동: T(500, 50)
  q1 = translate(q1, 500, 50)
  q2 = translate(q2, 500, 50)
  q3 = translate(q3, 500, 50)
  q4 = translate(q4, 500, 50)

  # 5. polygon 그리기
  draw_rectangle(ax, q1, q2, q3, q4)

  # 아랫쪽 날개축
  # 1. 위쪽 날개축을 x축 기준 반전
  r1 = reflect_x(q1)
  r2 = reflect_x(q2)
  r3 = reflect_x(q3)
  r4 = reflect_x(q4)

  # 2. polygon 그리기
  draw_rectangle(ax, r1, r2, r3, r4)

def draw_left_wing(ax, p1, p2, p3, p4): # 왼쪽 날개
  # 1. 원점이동
  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4  = translate(p4, -LEN/2, -LEN/2)

  # 2. 크기변환
  q1 = scale(q1, 1, 10)
  q2 = scale(q2, 1, 10)
  q3 = scale(q3, 1, 10)
  q4 = scale(q4, 1, 10)

  # 3. y축 기울임
  q1 = shear_y(q1, -2)
  q2 = shear_y(q2, -2)
  q3 = shear_y(q3, 2)
  q4 = shear_y(q4, 2)

  # 4. 이동
  q1 = translate(q1, 750, 0)
  q2 = translate(q2, 750, 0)
  q3 = translate(q3, 750, 0)
  q4 = translate(q4, 750, 0)

  # 5. polygon 그리기
  draw_rectangle(ax, q1, q2, q3, q4)

def draw_right_arm(ax, p1, p2, p3, p4):
  # 위쪽 날개축
  # 1. 원점 이동
  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4 = translate(p4, -LEN/2, -LEN/2)

  # 2. 크기 변환
  q1 = scale(q1, 6, 0.8)
  q2 = scale(q2, 6, 0.8)
  q3 = scale(q3, 6, 0.8)
  q4 = scale(q4, 6, 0.8)

  # 3. shy 기울임
  q1 = shear_y(q1, 0.2)
  q2 = shear_y(q2, 0.2)
  q3 = shear_y(q3, 0.2)
  q4 = shear_y(q4, 0.2)

  # 4. 이동
  q1 = translate(q1, -500, 50)
  q2 = translate(q2, -500, 50)
  q3 = translate(q3, -500, 50)
  q4 = translate(q4, -500, 50)

  # 5. polygon 그리기
  draw_rectangle(ax, q1, q2, q3, q4)

  # 아래쪽 날개축
  # 1. 위쪽 날개축을 x축 기준 반전
  r1 = reflect_x(q1)
  r2 = reflect_x(q2)
  r3 = reflect_x(q3)
  r4 = reflect_x(q4)

  # 2. polygon 그리기
  draw_rectangle(ax, r1, r2, r3, r4)

def draw_right_wing(ax, p1, p2, p3, p4):
  # 1. 원점 이동
  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4 = translate(p4, -LEN/2, -LEN/2)

  # 2. 크기변환
  q1 = scale(q1, 1, 10)
  q2 = scale(q2, 1, 10)
  q3 = scale(q3, 1, 10)
  q4 = scale(q4, 1, 10)

  # 3. shy 기울임
  q1 = shear_y(q1, 2)
  q2 = shear_y(q2, 2)
  q3 = shear_y(q3, -2)
  q4 = shear_y(q4, -2)

  # 4. 이동
  q1 = translate(q1, -750, 0)
  q2 = translate(q2, -750, 0)
  q3 = translate(q3, -750, 0)
  q4 = translate(q4, -750, 0)

  # 5. polygon 그리기
  draw_rectangle(ax, q1, q2, q3, q4)

# starship+superheavy 파트 그리기
def draw_background(ax, p1, p2, p3, p4):
  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4 = translate(p4, -LEN/2, -LEN/2)

  q1 = scale(q1, 2*INF_X/LEN, 2*INF_Y/LEN)
  q2 = scale(q2, 2*INF_X/LEN, 2*INF_Y/LEN)
  q3 = scale(q3, 2*INF_X/LEN, 2*INF_Y/LEN)
  q4 = scale(q4, 2*INF_X/LEN, 2*INF_Y/LEN)

  draw_rectangle(ax, q1, q2, q3, q4, color='skyblue')

def draw_flames(ax, p1, p2, p3, p4):
  flame_top = NOZZLE_Y + 25
  length = flame_top - (-INF_Y)
  
  layers = [
      (150, 1.00, 0.10, 'red', 0.55),
      (100, 0.85, 0.08, 'orange', 0.65),
      (55, 0.65, 0.05, 'yellow', 0.80)
  ]
  angles = [-0.25, 0.0, 0.25]
  
  for w, ratio, s, color, alpha in layers:
    L = length * ratio
    for theta in angles:
      sh = s * np.sign(theta)
      result = []
      for p in (p1, p2, p3, p4):
        q = translate(p, -LEN/2, -LEN/2) # 중심을 원점으로
        q = scale(q, w/LEN, L/LEN) # 폭w, 길이 L
        q = translate(q, 0, -L/2) # 불꽃 위가 원점(노즐)에 오도록
        q = shear_x(q, sh) # 불꽃 아래쪽을 밀기
        q = rotate(q, theta) # 노즐을 기준으로 회전
        q = translate(q, 0, flame_top) # 불꽃을 노즐 위치로 이동
        result.append(q)
      draw_rectangle(ax, *result, color=color, alpha=alpha)
  
def draw_superheavy(ax, p1, p2, p3, p4):
  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4 = translate(p4, -LEN/2, -LEN/2)

  q1 = scale(q1, ROCKET_W/LEN, BOOSTER_H/LEN)
  q2 = scale(q2, ROCKET_W/LEN, BOOSTER_H/LEN)
  q3 = scale(q3, ROCKET_W/LEN, BOOSTER_H/LEN)
  q4 = scale(q4, ROCKET_W/LEN, BOOSTER_H/LEN)

  q1 = translate(q1, 0, (SHIP_BOTTOM_Y+NOZZLE_Y)/2)
  q2 = translate(q2, 0, (SHIP_BOTTOM_Y+NOZZLE_Y)/2)
  q3 = translate(q3, 0, (SHIP_BOTTOM_Y+NOZZLE_Y)/2)
  q4 = translate(q4, 0, (SHIP_BOTTOM_Y+NOZZLE_Y)/2)

  draw_rectangle(ax, q1, q2, q3, q4, color='white')

def draw_engine(ax, p1, p2, p3, p4):
  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4 = translate(p4, -LEN/2, -LEN/2)

  q1 = scale(q1, ROCKET_W/LEN, ENGINE_H/LEN)
  q2 = scale(q2, ROCKET_W/LEN, ENGINE_H/LEN)
  q3 = scale(q3, ROCKET_W/LEN, ENGINE_H/LEN)
  q4 = scale(q4, ROCKET_W/LEN, ENGINE_H/LEN)
  
  q1 = translate(q1, 0, NOZZLE_Y+ENGINE_H/2)
  q2 = translate(q2, 0, NOZZLE_Y+ENGINE_H/2)
  q3 = translate(q3, 0, NOZZLE_Y+ENGINE_H/2)
  q4 = translate(q4, 0, NOZZLE_Y+ENGINE_H/2)
  
  q1 = translate(q1, -20, 0)
  q2 = translate(q2, 20, 0)

  draw_rectangle(ax, q1, q2, q3, q4, color='black')

def draw_grid_fins(ax, p1, p2, p3, p4):
  fin_y = SHIP_BOTTOM_Y - 40
  edge = ROCKET_W/2 + 70/2
  grid_position = [-edge, 0, edge]

  for x in grid_position:
    result = []
    for p in (p1, p2, p3, p4):
      q = translate(p, -LEN/2, -LEN/2)
      q = scale(q, 70/LEN, 40/LEN)
      q = translate(q, x, fin_y)
      result.append(q)
    draw_rectangle(ax, *result, color='black')

def draw_nosecone(ax, p1, p2, p3, p4):
  half_diag = LEN/np.sqrt(2)

  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4 = translate(p4, -LEN/2, -LEN/2)

  q1 = rotate(q1, -3.14/4)
  q2 = rotate(q2, -3.14/4)
  q3 = rotate(q3, -3.14/4)
  q4 = rotate(q4, -3.14/4)

  q1 = scale(q1, (ROCKET_W/2)/half_diag, NOSE_H/half_diag)
  q2 = scale(q2, (ROCKET_W/2)/half_diag, NOSE_H/half_diag)
  q3 = scale(q3, (ROCKET_W/2)/half_diag, NOSE_H/half_diag)
  q4 = scale(q4, (ROCKET_W/2)/half_diag, NOSE_H/half_diag)

  q1 = translate(q1, 0, NOSE_TIP_Y - NOSE_H)
  q2 = translate(q2, 0, NOSE_TIP_Y - NOSE_H)
  q3 = translate(q3, 0, NOSE_TIP_Y - NOSE_H)
  q4 = translate(q4, 0, NOSE_TIP_Y - NOSE_H)

  draw_rectangle(ax, q1, q2, q3, q4, color='black')

def draw_starship_body(ax, p1, p2, p3, p4):
  q1 = translate(p1, -LEN/2, -LEN/2)
  q2 = translate(p2, -LEN/2, -LEN/2)
  q3 = translate(p3, -LEN/2, -LEN/2)
  q4 = translate(p4, -LEN/2, -LEN/2)

  q1 = scale(q1, ROCKET_W/LEN, (SHIP_H - NOSE_H)/LEN)
  q2 = scale(q2, ROCKET_W/LEN, (SHIP_H - NOSE_H)/LEN)
  q3 = scale(q3, ROCKET_W/LEN, (SHIP_H - NOSE_H)/LEN)
  q4 = scale(q4, ROCKET_W/LEN, (SHIP_H - NOSE_H)/LEN)

  q1 = translate(q1, 0, SHIP_BOTTOM_Y + ((SHIP_H - NOSE_H)/2))
  q2 = translate(q2, 0, SHIP_BOTTOM_Y + ((SHIP_H - NOSE_H)/2))
  q3 = translate(q3, 0, SHIP_BOTTOM_Y + ((SHIP_H - NOSE_H)/2))
  q4 = translate(q4, 0, SHIP_BOTTOM_Y + ((SHIP_H - NOSE_H)/2))

  draw_rectangle(ax, q1, q2, q3, q4, color='black')

def draw_flap(ax, p1, p2, p3, p4, inner_x, outer_x, bottom_y, h_root, h_outer):
  w = inner_x - outer_x
  cx = (inner_x + outer_x)/2
  cy = bottom_y + h_root/2
  q = []
  for p in (p1, p2, p3, p4):
    t = translate(p, -LEN/2, -LEN/2)
    t = scale(t, w/LEN, h_root/LEN)
    t = translate(t, cx, cy)
    q.append(t)
  q[3] = translate(q[3], 0, -(h_root - h_outer))

  draw_rectangle(ax, *q, color='black')
  draw_rectangle(ax, *[reflect_y(pt) for pt in q], color='black')

def draw_flaps(ax, p1, p2, p3, p4):
  # forward flaps
  draw_flap(ax, p1, p2, p3, p4, inner_x=-40, outer_x=-118, bottom_y=722, h_root=68, h_outer=28)
  # aft flaps
  draw_flap(ax, p1, p2, p3, p4, inner_x=-60, outer_x=-131, bottom_y=225, h_root=150, h_outer=84)


# TIE Figher 그리기
def draw_object(ax):
  p1 = np.array([0, 0])
  p2 = np.array([LEN, 0])
  p3 = np.array([LEN, LEN])
  p4 = np.array([0, LEN])

  # 1. 중앙 조종석 그리기
  draw_cockpit(ax, p1, p2, p3, p4)

  # 2. 왼쪽 날개축 그리기
  draw_left_arm(ax, p1, p2, p3, p4)

  # 3. 왼쪽 날개 그리기
  draw_left_wing(ax, p1, p2, p3, p4) # 왼쪽 날개

  # 4. 오른쪽 날개축 그리기
  draw_right_arm(ax, p1, p2, p3, p4)

  # 5. 오른쪽 날개 그리기
  draw_right_wing(ax, p1, p2, p3, p4)


# Starship 파트 그리기
def draw_starship(ax):
  p1 = np.array([0, 0])
  p2 = np.array([LEN, 0])
  p3 = np.array([LEN, LEN])
  p4 = np.array([0, LEN])

  # 1. 배경인 하늘 그리기
  draw_background(ax, p1, p2, p3, p4)

  # 2. 불꽃 그리기
  draw_flames(ax, p1, p2, p3, p4)

  # 3. 슈퍼헤비 그리기
  draw_superheavy(ax, p1, p2, p3, p4)

  # 4. 엔진부 그리기
  draw_engine(ax, p1, p2, p3, p4)

  # 5. 그리드 핀 그리기
  draw_grid_fins(ax, p1, p2, p3, p4)

  # 6. 노즈콘 그리기
  draw_nosecone(ax, p1, p2, p3, p4)

  # 7. 스타쉽 그리기
  draw_starship_body(ax, p1, p2, p3, p4)

  # 8. 플랩 그리기
  draw_flaps(ax, p1, p2, p3, p4)