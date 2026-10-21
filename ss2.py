# =================================================================
# 🛡️ [절대 보안 & 깃허브 실시간 자동 업데이트 엔진]
# 💡 ss2.exe 실행 시 깃허브의 최신 ss2.py 코드를 실시간으로 불러와 가동합니다.
# =================================================================
import os
import sys
import time
import json
import urllib.request
import ssl
import subprocess
import ctypes
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import pyperclip

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

AUTH_SERVER_URL = "https://raw.githubusercontent.com/velvet0414/gaja/main/keys.json"
SS2_GITHUB_URL = "https://raw.githubusercontent.com/velvet0414/gaja/main/ss2.py"

if not globals().get("_SS2_GITHUB_LOADED", False):
    globals()["_SS2_GITHUB_LOADED"] = True
    try:
        print("🔄 [자동 업데이트] 깃허브에서 최신 ss2.py 코드를 확인 중입니다...")
        _ctx = ssl.create_default_context()
        _ctx.check_hostname = False
        _ctx.verify_mode = ssl.CERT_NONE
        _req = urllib.request.Request(
            f"{SS2_GITHUB_URL}?t={int(time.time())}",
            headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'}
        )
        with urllib.request.urlopen(_req, timeout=5, context=_ctx) as _resp:
            _remote_code = _resp.read().decode('utf-8')
        if len(_remote_code) > 1000 and "authenticate_only" in _remote_code:
            print("✅ [자동 업데이트 완료] 깃허브 최신 ss2.py 버전으로 즉시 가동합니다!")
            exec(compile(_remote_code, "ss2_github.py", "exec"), globals())
            sys.exit(0)
    except SystemExit:
        raise
    except Exception as _e:
        print(f"⚠️ [깃허브 연결 생략] 내장된 로컬 버전으로 즉시 가동합니다. ({_e})")

def get_hwid():
    try:
        # 1순위: 최신 윈도우(11 이상) 호환 파워쉘 명령어 (wmic 삭제 대비)
        cmd = 'powershell -NoProfile -Command "(Get-CimInstance -Class Win32_ComputerSystemProduct).UUID"'
        return subprocess.check_output(cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
    except:
        try:
            # 2순위: 구형 윈도우(10 이하)용 wmic 명령어 (백업용)
            return subprocess.check_output('wmic csproduct get uuid', creationflags=subprocess.CREATE_NO_WINDOW).decode().split('\n')[1].strip()
        except:
            return "UNKNOWN-HWID"

def authenticate_only():
    temp_root = tk.Tk(); temp_root.withdraw()
    
    # 1. 🔐 HWID 보안 인증
    print("🔐 PC 하드웨어 인증을 확인 중입니다...")
    my_hwid = get_hwid()
    if my_hwid == "UNKNOWN-HWID": 
        messagebox.showerror("오류", "PC 고유번호를 읽을 수 없습니다.")
        sys.exit()

    valid_keys = {}
    is_offline = False
    
    try:
        ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(f"{AUTH_SERVER_URL}?t={int(time.time())}", headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req, timeout=5, context=ctx) as response:
            valid_keys = json.loads(response.read().decode('utf-8'))
            
    except Exception as e: 
        # 🚀 [절대 무적 방어막] 
        # 429 에러(요청 초과)나 깃허브 서버 장애 시, 통제실이 뻗지 않도록 "오프라인 가동" 처리
        print(f"⚠️ [시스템 알림] 통제실 서버 응답 지연 감지! (사유: {e})")
        print("✅ 오프라인 모드로 자동 우회하여 즉시 통제실을 가동합니다.")
        is_offline = True

    if not is_offline:
        if my_hwid in valid_keys:
            expire_date = datetime.strptime(valid_keys[my_hwid], "%Y-%m-%d")
            if datetime.now() <= expire_date: 
                print("✅ 통제실 인증 성공! (업데이트 검사 생략)")
            else: 
                messagebox.showerror("기간 만료", "사용 기간이 만료되었습니다. 관리자에게 문의하세요.")
                sys.exit()
        else:
            try:
                pyperclip.copy(my_hwid)
                msg_tail = "\n\n(클립보드에 시리얼 번호가 자동 복사되었습니다. 통제실 keys.json에 추가해주세요!)"
            except:
                msg_tail = ""
            messagebox.showerror("인증 실패", f"미등록 PC입니다.\n\n[내 PC 시리얼]\n{my_hwid}{msg_tail}")
            sys.exit()

    temp_root.destroy()

# 🚀 엔진 즉시 가동! (통과 못 하면 여기서 프로그램 자폭됨)
authenticate_only()
# =================================================================
import time
import random
import threading
import struct
import tkinter as tk
from tkinter import ttk
import win32api
import ctypes 
from pynput import keyboard, mouse
import serial
import serial.tools.list_ports 
from ctypes import wintypes
from ctypes.wintypes import RECT
import win32gui
import win32con
import math
import cv2
cv2.setNumThreads(1) # 🚀 [최적화 1] OpenCV가 1스레드당 1코어만 정직하게 쓰도록 강제 통제!
import numpy as np
import mss
import queue
import json
import os
import datetime

import win32com.client
import pythoncom
import heapq

import base64
import socket

# 💡 [CapSolver 단독 엔진] 로컬 제시어 이미지 매칭 + CapSolver API + 1~11번 중앙컴 프록시 우회
CAPSOLVER_API_KEY = "CAP-28B0F321F9019FFB9710F296FAA9AF561F01AABB6D40F8F35F70B8B26DBCE889"

os.makedirs("qq/certi/words", exist_ok=True)
os.makedirs("qq/certi/words_unseen", exist_ok=True)
os.makedirs("qq/certi/debug_log", exist_ok=True)
os.makedirs("qq/certi/recerti", exist_ok=True)

CAPTCHA_WORD_MAP = {
    "car":        "/m/0k4j",    # 자동차
    "traffic":    "/m/015qff",  # 신호등
    "crosswalk":  "/m/014xcs",  # 횡단보도
    "hydrant":    "/m/01pns0",  # 소화전
    "bus":        "/m/01bjv",   # 버스
    "bicycle":    "/m/0199g",   # 자전거
    "motorcycle": "/m/04_sv",   # 오토바이
    "stairs":     "/m/01lynh",  # 계단
    "chimney":    "/m/01jk_4",  # 굴뚝
    "tractor":    "/m/013xlm",  # 트랙터
    "bridge":     "/m/015kr",   # 다리
    "pier":       "/m/015kr",   # 교각
    "palm":       "/m/0cdl1",   # 야자수
    "boat":       "/m/019jd",   # 보트
    "mountain":   "/m/09d_r",   # 산 또는 언덕
    "taxi":       "/m/0pg52",   # 택시
    "parking":    "/m/015qbp",  # 주차요금정산기
}

_WORD_TEMPLATES_CACHE = {}
_SAVED_UNSEEN_BANNERS = []
_LAST_CAPTCHA_CALL_TIME = 0.0
SLOT_F6_CX, SLOT_F6_CY = 688, 502  # 💡 군주 접속 후 헤이스트(F6) 원클릭 좌표

def _detect_captcha_question_local(banner_bgr):
    if banner_bgr is None or banner_bgr.size == 0:
        return None, "배너없음(0%)"

    best_code, best_name, best_score = None, "없음", 0.0
    banner_gray = cv2.cvtColor(banner_bgr, cv2.COLOR_BGR2GRAY)

    for fname in os.listdir("qq/certi/words"):
        if not fname.lower().endswith((".png", ".jpg")):
            continue
        fpath = os.path.join("qq/certi/words", fname)

        matched_code = None
        fname_lower = os.path.splitext(fname)[0].lower()
        for key_prefix, q_code in CAPTCHA_WORD_MAP.items():
            if fname_lower.startswith(key_prefix):
                matched_code = q_code
                break
        if not matched_code:
            continue

        mtime = os.path.getmtime(fpath)
        cached = _WORD_TEMPLATES_CACHE.get(fpath)
        if not cached or cached["mtime"] != mtime:
            try:
                with open(fpath, "rb") as f:
                    np_arr = np.asarray(bytearray(f.read()), dtype=np.uint8)
                bgra = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
                if bgra is None:
                    continue
                color_img = bgra[:, :, :3] if len(bgra.shape) == 3 else cv2.cvtColor(bgra, cv2.COLOR_GRAY2BGR)
                gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
                cached = {"color": color_img, "gray": gray_img, "mtime": mtime}
                _WORD_TEMPLATES_CACHE[fpath] = cached
            except Exception:
                continue

        base_gray = cached["gray"]
        for scale in (1.0, 0.95, 1.05, 0.90, 1.10):
            th_s = max(5, int(round(base_gray.shape[0] * scale)))
            tw_s = max(5, int(round(base_gray.shape[1] * scale)))
            if banner_gray.shape[0] < th_s or banner_gray.shape[1] < tw_s:
                continue
            try:
                tmpl_s = base_gray if scale == 1.0 else cv2.resize(base_gray, (tw_s, th_s), interpolation=cv2.INTER_AREA)
                res = cv2.matchTemplate(banner_gray, tmpl_s, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if max_val > best_score:
                    best_score = max_val
                    best_code = matched_code
                    best_name = fname
            except Exception:
                continue

    info_str = f"{best_name}({best_score*100:.1f}%)"
    if best_score >= 0.75:
        return best_code, info_str
    return None, info_str

def save_unseen_banner_if_needed(img_bgr):
    global _SAVED_UNSEEN_BANNERS
    try:
        if img_bgr is None or img_bgr.size == 0:
            return None
        h, w = img_bgr.shape[:2]
        search_roi = img_bgr[max(0, 90):min(h, 290), max(0, 240):min(w, 550)]
        q_code, match_info = _detect_captcha_question_local(search_roi)
        if q_code:
            return (q_code, match_info)

        check_patch = cv2.cvtColor(img_bgr[max(0, 100):min(h, 250), max(0, 260):min(w, 430)], cv2.COLOR_BGR2GRAY)
        for prev_gray in _SAVED_UNSEEN_BANNERS:
            if prev_gray.shape == check_patch.shape:
                res = cv2.matchTemplate(check_patch, prev_gray, cv2.TM_CCOEFF_NORMED)
                if cv2.minMaxLoc(res)[1] >= 0.92:
                    return None

        _SAVED_UNSEEN_BANNERS.append(check_patch.copy())
        if len(_SAVED_UNSEEN_BANNERS) > 30:
            _SAVED_UNSEEN_BANNERS.pop(0)

        now_str = time.strftime("%H%M%S") + f"_{int((time.time() % 1) * 100):02d}"
        unseen_path = os.path.join("qq", "certi", "words_unseen", f"full_{now_str}.png")
        ok_enc, enc_buf = cv2.imencode(".png", img_bgr)
        if ok_enc:
            with open(unseen_path, "wb") as f:
                f.write(enc_buf.tobytes())
            print(f"📸 [미등록 제시어 저장] '{unseen_path}' (최고유사도: {match_info})")
        return None
    except Exception as e:
        print(f"⚠️ [전체화면 자동저장 오류]: {e}")
        return None

def _locate_captcha_banner_and_grid(img_bgr):
    h, w = img_bgr.shape[:2]
    gx1, gx2 = 259, 533
    by1, by2 = 126, 238
    try:
        roi_left = img_bgr[85:300, 265:415]
        hsv_left = cv2.cvtColor(roi_left, cv2.COLOR_BGR2HSV)
        mask_b = cv2.inRange(hsv_left, np.array([103, 185, 185]), np.array([117, 255, 255]))
        row_counts = np.sum(mask_b > 0, axis=1)

        in_banner = False
        start_r, end_r = None, None
        zero_streak = 0
        for r_idx, cnt in enumerate(row_counts):
            if not in_banner:
                if cnt >= 60:
                    in_banner = True
                    start_r = r_idx
                    end_r = r_idx
                    zero_streak = 0
            else:
                if cnt >= 35:
                    end_r = r_idx
                    zero_streak = 0
                else:
                    zero_streak += 1
                    if zero_streak >= 3 and (end_r - start_r) >= 70:
                        break

        if start_r is not None and end_r is not None and (end_r - start_r) >= 70:
            by1 = 85 + start_r
            by2 = 85 + end_r

        strip_y1 = max(0, by2 - 8)
        strip_y2 = min(h, by2)
        if strip_y2 > strip_y1:
            hsv_strip = cv2.cvtColor(img_bgr[strip_y1:strip_y2, 230:560], cv2.COLOR_BGR2HSV)
            mask_s = cv2.inRange(hsv_strip, np.array([103, 185, 185]), np.array([117, 255, 255]))
            col_counts = np.sum(mask_s > 0, axis=0)
            valid_c = np.where(col_counts >= max(2, (strip_y2 - strip_y1) // 2))[0]
            if len(valid_c) > 0:
                cand_x1 = 230 + int(valid_c[0])
                cand_x2 = 230 + int(valid_c[-1])
                if 268 <= (cand_x2 - cand_x1) <= 280:
                    gx1, gx2 = cand_x1, cand_x2
    except Exception:
        pass

    bx1, bx2 = gx1, gx2
    gy1 = by2 + 4
    grid_w = gx2 - gx1
    grid_h = grid_w + 16
    gy2 = min(h, gy1 + grid_h)
    return (bx1, by1, bx2, by2), (gx1, gy1, gx2, gy2)

def _detect_grid_size_opencv(grid_bgr, banner_bgr=None):
    try:
        if grid_bgr is None or grid_bgr.shape[0] < 200 or grid_bgr.shape[1] < 200:
            return 3
        gh, gw = grid_bgr.shape[:2]
        gray = cv2.cvtColor(grid_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)

        def line_prominence(pos, is_col=True):
            p = int(round(pos))
            if is_col:
                c1, c2 = max(0, p - 3), min(gw, p + 4)
                peak = np.max(gray[:, c1:c2], axis=1)
                left_bg = gray[:, max(0, p - 8)]
                right_bg = gray[:, min(gw - 1, p + 8)]
                diff = peak - 0.5 * (left_bg + right_bg)
                return float(np.mean((peak >= 175) & ((diff >= 12) | (peak >= 205))))
            else:
                r1, r2 = max(0, p - 3), min(gh, p + 4)
                peak = np.max(gray[r1:r2, :], axis=0)
                top_bg = gray[max(0, p - 8), :]
                bot_bg = gray[min(gh - 1, p + 8), :]
                diff = peak - 0.5 * (top_bg + bot_bg)
                return float(np.mean((peak >= 175) & ((diff >= 12) | (peak >= 205))))

        score_3x3 = (
            line_prominence(gw / 3.0, True) + line_prominence(gw * 2.0 / 3.0, True) +
            line_prominence(gh / 3.0, False) + line_prominence(gh * 2.0 / 3.0, False)
        ) / 4.0
        score_4x4 = (
            line_prominence(gw / 4.0, True) + line_prominence(gw * 2.0 / 4.0, True) + line_prominence(gw * 3.0 / 4.0, True) +
            line_prominence(gh / 4.0, False) + line_prominence(gh * 2.0 / 4.0, False) + line_prominence(gh * 3.0 / 4.0, False)
        ) / 6.0
        center_cross = 0.5 * (line_prominence(gw / 2.0, True) + line_prominence(gh / 2.0, False))

        if score_4x4 > score_3x3 and (score_4x4 >= 0.42 or center_cross >= 0.50):
            return 4
        return 3
    except Exception:
        return 3

def _is_tile_already_checked(grid_bgr, row_0based, col_0based, grid_size):
    try:
        gh, gw = grid_bgr.shape[:2]
        cw, ch = gw / float(grid_size), gh / float(grid_size)
        x1 = int(col_0based * cw)
        y1 = int(row_0based * ch)
        x2 = int(min(gw, x1 + cw * 0.45))
        y2 = int(min(gh, y1 + ch * 0.45))
        roi = grid_bgr[y1:y2, x1:x2]
        if roi.size == 0:
            return False
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask_blue = cv2.inRange(hsv, np.array([100, 150, 150]), np.array([125, 255, 255]))
        return cv2.countNonZero(mask_blue) >= 28
    except Exception:
        return False

def _save_captcha_debug_image(img_bgr, banner_rect, grid_rect, match_str, grid_size, valid_coords, status_text):
    try:
        dbg = img_bgr.copy()
        bx1, by1, bx2, by2 = banner_rect
        gx1, gy1, gx2, gy2 = grid_rect
        cv2.rectangle(dbg, (bx1, by1), (bx2, by2), (255, 200, 0), 2)
        cv2.rectangle(dbg, (gx1, gy1), (gx2, gy2), (255, 0, 255), 2)
        for idx_pt, (cx, cy) in enumerate(valid_coords):
            cv2.circle(dbg, (cx, cy), 14, (0, 0, 255), 3)
            cv2.putText(dbg, str(idx_pt + 1), (cx - 6, cy + 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.rectangle(dbg, (5, 5), (790, 65), (0, 0, 0), -1)
        cv2.putText(dbg, f"WORD: {match_str} | GRID: {grid_size}x{grid_size}", (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        cv2.putText(dbg, f"STATUS: {status_text} | TARGETS: {valid_coords}", (12, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 255), 2)
        now_str = time.strftime("%H%M%S") + f"_{int((time.time() % 1) * 100):02d}"
        dbg_path = os.path.join("qq", "certi", "debug_log", f"cap_dbg_{now_str}.png")
        ok_enc, enc_buf = cv2.imencode(".png", dbg)
        if ok_enc:
            with open(dbg_path, "wb") as f:
                f.write(enc_buf.tobytes())
    except Exception:
        pass

def analyze_captcha_with_gemini(img_bgr, banner_bottom_y=272):
    if not CAPSOLVER_API_KEY or "여기에" in CAPSOLVER_API_KEY:
        print("⚠️ [CapSolver 오류] API 키가 입력되지 않았습니다!")
        return []

    try:
        (bx1, by1, bx2, by2), (gx1, gy1, gx2, gy2) = _locate_captcha_banner_and_grid(img_bgr)
        search_roi = img_bgr[by1:by2, bx1:bx2]
        question_code, match_info = _detect_captcha_question_local(search_roi)

        if not question_code:
            globals()["_LAST_CAPTCHA_WORD_MATCHED"] = False
            save_unseen_banner_if_needed(img_bgr)
            print(f"⚠️ [제시어 미매칭] 최고유사도: {match_info} (기준 75% 미달) ➔ CapSolver 스킵")
            _save_captcha_debug_image(img_bgr, (bx1, by1, bx2, by2), (gx1, gy1, gx2, gy2), match_info, 3, [], "WORD_MISS")
            return []
        globals()["_LAST_CAPTCHA_WORD_MATCHED"] = True

        grid_crop = img_bgr[gy1:gy2, gx1:gx2]
        grid_size = _detect_grid_size_opencv(grid_crop, banner_bgr=search_roi)
        target_res = 450 if grid_size == 4 else 300
        grid_for_api = cv2.resize(grid_crop, (target_res, target_res), interpolation=cv2.INTER_CUBIC)
        print(f"🔎 [로컬 제시어 매칭 성공] {match_info} ➔ 코드:{question_code} ({grid_size}x{grid_size} 격자, {target_res}x{target_res} 변환 전송)")

        _, buffer = cv2.imencode('.jpg', grid_for_api, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        payload = {
            "clientKey": CAPSOLVER_API_KEY,
            "task": {
                "type": "ReCaptchaV2Classification",
                "image": img_base64,
                "question": question_code
            }
        }
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(
            "https://api.capsolver.com/createTask",
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=12, context=ctx) as response:
            res_json = json.loads(response.read().decode('utf-8'))

        if res_json.get("errorId", 1) != 0:
            err_msg = f"{res_json.get('errorCode')}:{res_json.get('errorDescription')}"
            print(f"⚠️ [CapSolver API 오류] {err_msg}")
            _save_captcha_debug_image(img_bgr, (bx1, by1, bx2, by2), (gx1, gy1, gx2, gy2), match_info, grid_size, [], f"API_ERR:{err_msg}")
            return []

        solution = res_json.get("solution", {})
        objects = solution.get("objects", [])
        valid_coords, seen = [], set()
        grid_w, grid_h = gx2 - gx1, gy2 - gy1
        cell_w, cell_h = grid_w / float(grid_size), grid_h / float(grid_size)

        for idx in objects:
            idx_int = int(idx)
            r_0, c_0 = idx_int // grid_size, idx_int % grid_size
            if not (0 <= r_0 < grid_size and 0 <= c_0 < grid_size) or (r_0, c_0) in seen:
                continue
            seen.add((r_0, c_0))
            if _is_tile_already_checked(grid_crop, r_0, c_0, grid_size):
                continue
            cx = int(round(gx1 + (c_0 + 0.5) * cell_w))
            cy = int(round(gy1 + (r_0 + 0.5) * cell_h))
            valid_coords.append((cx, cy))
            print(f"   📍 [CapSolver 타일 확정] {r_0+1}행 {c_0+1}열 (index:{idx_int}) ➔ 고정픽셀({cx}, {cy})")

        status_label = f"OK(tiles:{objects})" if objects else f"EMPTY(sol:{solution})"
        _save_captcha_debug_image(img_bgr, (bx1, by1, bx2, by2), (gx1, gy1, gx2, gy2), match_info, grid_size, valid_coords, status_label)
        return valid_coords
    except Exception as e:
        print(f"⚠️ CapSolver 캡차 판독 중 예외 발생: {e}")
        return []

# ==============================================================================
# 🌐 [통제실 전용 프록시 우회 클라이언트]
# - 커맨드컴(100.99.95.118)은 물리 회선을 '중앙 12번'과 공유하므로 내 기본 번호는 "12"로 취급!
# - 평상시("12")에는 1.png로 인증하며 12번 중앙컴과 IP 대기열을 공유하고,
#   fail.png 발생 시 1번~11번 중앙컴(sub.png)을 순차 로테이션합니다.
# ==============================================================================
CENTRAL_TAILSCALE_MAP = {
    "1":  "100.106.98.27",   # no1
    "2":  "100.102.199.44",  # no2
    "3":  "100.102.229.12",  # no3
    "4":  "100.117.6.55",    # no4
    "5":  "100.82.40.120",   # no5
    "6":  "100.111.124.91",  # no6
    "7":  "100.118.150.90",  # no7
    "8":  "100.99.116.37",   # no8
    "9":  "100.110.17.117",  # no9
    "10": "100.93.134.45",   # no10-2
    "11": "100.66.194.109",  # no11
    "12": "100.74.191.120",  # no12 (커맨드컴과 동일 물리 회선 공유)
}
CENTRAL_ORDER = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
PROXY_DIRECT_EXIT_PORT = 31280
MINI_PROXY_PORTS = {
    "미니1": 31281, "미니2": 31282, "미니3": 31283, "미니4": 31284
}
CURRENT_PROXY_TARGET_NUM = {
    "미니1": None, "미니2": None, "미니3": None, "미니4": None
}
ALIVE_OTHER_PROXIES = []
_LAST_PROXY_LOG_TIME = 0.0

_LOCAL_IP_LOCK_MUTEX = threading.Lock()
_LOCAL_IP_LOCK_HOLDER = None
_LOCAL_IP_LOCK_HEARTBEAT = 0.0
_LOCAL_IP_LOCK_START_TIME = 0.0
_LOCAL_IP_LOCK_COOLDOWN_UNTIL = 0.0
_LOCAL_IP_LOCK_QUEUE = []

def get_my_central_num():
    """커맨드컴은 중앙 12번과 물리 회선을 공유하므로 기본 회선 번호를 '12'로 반환합니다."""
    return "12"

def get_next_central_in_order(curr_c_num, pc_key=None):
    my_num = get_my_central_num()
    curr_str = str(curr_c_num).strip()
    if curr_str not in CENTRAL_ORDER:
        curr_str = my_num
    start_idx = CENTRAL_ORDER.index(curr_str)
    alive_nums = {c_num for c_num, _ in ALIVE_OTHER_PROXIES}
    total_cnt = len(CENTRAL_ORDER)
    for step in range(1, total_cnt + 1):
        cand_num = CENTRAL_ORDER[(start_idx + step) % total_cnt]
        if cand_num == my_num:
            return my_num
        if not alive_nums or cand_num in alive_nums:
            return cand_num
    return my_num

def _local_ip_lock_fallback(action, client_id):
    """중앙 12번 스크립트가 꺼져 있을 때도 커맨드컴 내부 미니1~4가 동시에 인증하지 않도록 순차 대기열을 보장합니다."""
    global _LOCAL_IP_LOCK_HOLDER, _LOCAL_IP_LOCK_HEARTBEAT, _LOCAL_IP_LOCK_START_TIME, _LOCAL_IP_LOCK_COOLDOWN_UNTIL, _LOCAL_IP_LOCK_QUEUE
    now = time.time()
    with _LOCAL_IP_LOCK_MUTEX:
        _LOCAL_IP_LOCK_QUEUE = [(cid, t) for cid, t in _LOCAL_IP_LOCK_QUEUE if now - t <= 15.0]
        if _LOCAL_IP_LOCK_HOLDER is not None:
            if (now - _LOCAL_IP_LOCK_HEARTBEAT > 15.0) or (now - _LOCAL_IP_LOCK_START_TIME > 120.0):
                _LOCAL_IP_LOCK_HOLDER = None
        if action == "RELEASE":
            _LOCAL_IP_LOCK_QUEUE = [(cid, t) for cid, t in _LOCAL_IP_LOCK_QUEUE if cid != client_id]
            if _LOCAL_IP_LOCK_HOLDER == client_id:
                _LOCAL_IP_LOCK_HOLDER = None
                _LOCAL_IP_LOCK_COOLDOWN_UNTIL = now + 3.5
            return True, "RELEASED"
        elif action == "ACQUIRE":
            if _LOCAL_IP_LOCK_HOLDER == client_id:
                _LOCAL_IP_LOCK_HEARTBEAT = now
                return True, "GRANTED"
            found_in_q = False
            for idx, (cid, _) in enumerate(_LOCAL_IP_LOCK_QUEUE):
                if cid == client_id:
                    _LOCAL_IP_LOCK_QUEUE[idx] = (client_id, now)
                    found_in_q = True
                    break
            if not found_in_q:
                _LOCAL_IP_LOCK_QUEUE.append((client_id, now))
            if _LOCAL_IP_LOCK_HOLDER is None:
                if _LOCAL_IP_LOCK_QUEUE and _LOCAL_IP_LOCK_QUEUE[0][0] == client_id:
                    if now < _LOCAL_IP_LOCK_COOLDOWN_UNTIL:
                        rem_cd = max(1, int(round(_LOCAL_IP_LOCK_COOLDOWN_UNTIL - now)))
                        return False, f"COOLDOWN|직전 인증 직후 안전 간격 대기({rem_cd}초)"
                    _LOCAL_IP_LOCK_QUEUE.pop(0)
                    _LOCAL_IP_LOCK_HOLDER = client_id
                    _LOCAL_IP_LOCK_HEARTBEAT = now
                    _LOCAL_IP_LOCK_START_TIME = now
                    return True, "GRANTED"
                else:
                    q_pos = next((i + 1 for i, (cid, _) in enumerate(_LOCAL_IP_LOCK_QUEUE) if cid == client_id), 1)
                    front_id = _LOCAL_IP_LOCK_QUEUE[0][0] if _LOCAL_IP_LOCK_QUEUE else "앞순번"
                    return False, f"WAIT|앞순번({front_id}) 대기 중 (내 순번: {q_pos}번)"
            else:
                q_pos = next((i + 1 for i, (cid, _) in enumerate(_LOCAL_IP_LOCK_QUEUE) if cid == client_id), 1)
                return False, f"BUSY|현재 [{_LOCAL_IP_LOCK_HOLDER}] 인증 진행 중 (내 대기순번: {q_pos}번)"
    return False, "ERROR"

def request_central_ip_lock(pc_key, target_c_num, action="ACQUIRE"):
    my_num = get_my_central_num()
    t_num = str(target_c_num or my_num).strip()
    if action == "RELEASE" or t_num == my_num:
        return True, "GRANTED"

    # 타 중앙컴 프록시(sub.png) 사용 시 해당 중앙컴(31280)이 켜져 있는지만 확인하고 대기 없이 즉시 동시 통과!
    host = CENTRAL_TAILSCALE_MAP.get(t_num, "100.74.191.120")
    try:
        s = socket.create_connection((host, PROXY_DIRECT_EXIT_PORT), timeout=1.0)
        s.close()
        return True, "GRANTED"
    except Exception:
        return False, "OFFLINE|타 중앙컴 연결 불가"

def release_central_ip_lock_async(pc_key):
    if pc_key not in ai_states:
        return
    st = ai_states[pc_key]
    locked_c = st.pop("certi_locked_central", None)
    if locked_c:
        threading.Thread(target=request_central_ip_lock, args=(pc_key, locked_c, "RELEASE"), daemon=True).start()

def _proxy_health_checker_thread():
    global ALIVE_OTHER_PROXIES
    while True:
        my_num = get_my_central_num()
        alive_temp = []
        for c_num in CENTRAL_ORDER:
            if c_num == my_num:
                continue
            ts_ip = CENTRAL_TAILSCALE_MAP.get(c_num)
            if not ts_ip:
                continue
            try:
                s = socket.create_connection((ts_ip, PROXY_DIRECT_EXIT_PORT), timeout=0.4)
                s.close()
                alive_temp.append((c_num, ts_ip))
            except Exception:
                pass
        ALIVE_OTHER_PROXIES = alive_temp
        time.sleep(5.0)

def _proxy_pipe_sockets(s1, s2):
    try:
        while True:
            data = s1.recv(8192)
            if not data:
                break
            s2.sendall(data)
    except Exception:
        pass
    finally:
        try: s1.close()
        except Exception: pass
        try: s2.close()
        except Exception: pass

def _handle_proxy_client(client_sock, pc_key):
    global _LAST_PROXY_LOG_TIME
    remote_sock = None
    try:
        client_sock.settimeout(10.0)
        try: client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception: pass

        now_t = time.time()
        my_num = get_my_central_num()
        target_num = CURRENT_PROXY_TARGET_NUM.get(pc_key) if pc_key else None
        if not target_num or target_num == my_num or target_num not in CENTRAL_TAILSCALE_MAP:
            target_num = get_next_central_in_order(my_num)
            if pc_key:
                CURRENT_PROXY_TARGET_NUM[pc_key] = target_num

        ehost = CENTRAL_TAILSCALE_MAP.get(target_num)
        if ehost:
            try:
                remote_sock = socket.create_connection((ehost, PROXY_DIRECT_EXIT_PORT), timeout=4.0)
                if now_t - _LAST_PROXY_LOG_TIME > 3.0:
                    print(f"🔗 [군주 프록시 우회] {pc_key} 크롬 ➔ [{target_num}번 중앙컴({ehost})] 회선으로 정상 연결됨!")
                    _LAST_PROXY_LOG_TIME = now_t
            except Exception:
                remote_sock = None

        if remote_sock is not None:
            try: remote_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            except Exception: pass
            client_sock.settimeout(None)
            remote_sock.settimeout(None)
            threading.Thread(target=_proxy_pipe_sockets, args=(client_sock, remote_sock), daemon=True).start()
            _proxy_pipe_sockets(remote_sock, client_sock)
            return
    except Exception:
        try: client_sock.close()
        except Exception: pass
        if remote_sock:
            try: remote_sock.close()
            except Exception: pass

def _start_proxy_listener(bind_port, pc_key):
    while True:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            srv.bind(("0.0.0.0", bind_port))
            srv.listen(64)
            break
        except Exception:
            try: srv.close()
            except Exception: pass
            time.sleep(3.0)
    print(f"🌐 [군주 우회 입구 개통] {pc_key} 전용 크롬 우회 포트({bind_port}) 오픈 완료!")
    while True:
        try:
            c_sock, _ = srv.accept()
            threading.Thread(target=_handle_proxy_client, args=(c_sock, pc_key), daemon=True).start()
        except Exception:
            time.sleep(0.05)

threading.Thread(target=_proxy_health_checker_thread, daemon=True).start()
for _mk, _mport in MINI_PROXY_PORTS.items():
    threading.Thread(target=_start_proxy_listener, args=(_mport, _mk), daemon=True).start()

# 🌟 로컬 YOLO 모델 Import
from ultralytics import YOLO
YOLO_CONF = 0.50

# =====================================================================
# 📡 [커맨드 센터 통신 코어] 테일스케일 1타 팩트체크 & 병목 제로 라우팅
# =====================================================================
import socket
import threading
import queue
import json
import time
import math
import random

CMD_PORT = 9999
connected_clients = {}

# 🚀 1. 테일스케일 IP ➔ 중앙컴(사냥컴) 번호 맵핑
TAILSCALE_IPS = {
    "100.73.27.56": 1, "100.102.199.44": 2, "100.102.229.12": 3, "100.117.6.55": 4,
    "100.82.40.120": 5, "100.111.124.91": 6, "100.118.150.90": 7,
    "100.99.116.37": 8, "100.110.17.117": 9, "100.93.134.45": 10,
    "100.66.194.109": 11, "100.74.191.120": 12
}

# 🚀 2. 서버 전담반 편성표 (모든 미니PC를 글루디오 전담으로 통합)
SERVER_ASSIGNMENTS = {
    "글루디오": ["미니1", "미니2", "미니3", "미니4"]
}

global_req_queue = queue.Queue() 
mini_queues = {k: queue.Queue() for k in ["미니1", "미니2", "미니3", "미니4"]}
internal_router_queue = queue.Queue() 

active_group_tasks = {} 
task_lock = threading.Lock()

# 👇👇👇 [신규 추가] 삑사리 캐릭의 재도전(새치기 방지)을 보장하는 VIP 예약석 장부 👇👇👇
reserved_servers = {} 

# 🚀 [신규 추가] 첫방 실패 이후 1분 경과 추적 장부
buff_fail_tracker = {} 

def get_target_server(pc_num, char_id):
    # 🚀 모든 사냥컴 번호를 불문하고 무조건 '글루디오'로 강제 연동!
    return "글루디오"

def allocate_casts(buffers_mp, total_casts=6):
    def get_max_casts(mp):
        # 🔒 [원본 코드 복구] 마나가 100%일 때만 6방을 쏠 수 있게 정상화!
        if mp >= 100.0: return 6   # 👈 형님 지시대로 98%에서 100%로 상향 완료!
        if mp >= 84.0: return 5
        if mp >= 67.0: return 4
        if mp >= 50.0: return 3
        if mp >= 33.0: return 2
        if mp >= 16.0: return 1
        return 0

    if sum(get_max_casts(v) for v in buffers_mp.values()) < total_casts: return None
    
    alloc = {k: 0 for k in buffers_mp}
    simulated_mp = buffers_mp.copy()
    for _ in range(total_casts):
        best_buffer = max(simulated_mp, key=simulated_mp.get)
        alloc[best_buffer] += 1
        # 🚀 [원본 복구] 마나 차감량을 다시 1방당 16.6으로 돌려놓았습니다.
        simulated_mp[best_buffer] -= 16.6 
    return {k: v for k, v in alloc.items() if v > 0}

def send_to_central_pc(client_id, data_dict):
    try:
        if client_id in connected_clients:
            sock = connected_clients[client_id]["socket"]
            sock.send((json.dumps(data_dict, ensure_ascii=False) + "\n").encode('utf-8'))
            return True
    except Exception as e: print(f"⚠️ [통신 오류] 사냥컴({client_id}) 전송 실패: {e}")
    return False

history_target_casts = {} # 🚀 [신규 추가] 사냥컴별 최초 목표 방수를 5분간 영구 기억하는 장부

def dispatcher_thread():
    global reserved_servers, history_target_casts, buff_fail_tracker 
    last_mp_wait_log = {}
    
    # 👇👇 [추가] 두 서버를 번갈아가며 스캔하기 위한 스위치
    server_turn = 0
    # 🚀 기존 로직 구조(mod 연산)를 100% 보존하면서 파아그리오를 글루디오로 교체!
    server_list = ["글루디오", "글루디오"]

    while True:
        try:
            curr_time = time.time()
            
            # 👇👇 [추가] 0.1초마다 타겟 렌즈를 바꿉니다 (파아 ➔ 캐스톨 ➔ 파아 ➔ 캐스톨)
            server_turn = (server_turn + 1) % 2
            priority_server = server_list[server_turn]
            
            with task_lock:
                expired_res = [srv for srv, res in reserved_servers.items() if curr_time > res["expire"]]
                for srv in expired_res:
                    del reserved_servers[srv]

                expired_fails = [cid for cid, t in buff_fail_tracker.items() if curr_time - t > 300.0]
                for cid in expired_fails:
                    del buff_fail_tracker[cid]

                to_delete = [cid for cid, task in active_group_tasks.items() if curr_time > task["timeout"]]
                for cid in to_delete:
                    for m_key in active_group_tasks[cid].get("pending_reports", set()):
                        mini_queues[m_key].put({"action": "ABORT_BUFF", "char_id": cid})
                    srv = active_group_tasks[cid].get("server")
                    if srv: 
                        reserved_servers[srv] = {"char_id": cid, "expire": curr_time + 20.0}
                    del active_group_tasks[cid]

            while not internal_router_queue.empty():
                report = internal_router_queue.get()
                r_char_id = str(report.get("char_id", ""))
                r_mini = report.get("mini_key")
                action = report.get("action")
                
                with task_lock:
                    if r_char_id in active_group_tasks:
                        task = active_group_tasks[r_char_id]
                        client_id = task["client_id"]
                        
                        if action == "FIRST_SHOT_DONE":
                            print(f"🎯 [통제실] {r_mini} 1타 발사 완료. 사냥컴({r_char_id})에 검증 지시!")
                            send_to_central_pc(client_id, {"action": "CHECK_FIRST_BUFF", "char_id": r_char_id})
                            
                        elif action == "TASK_DONE":
                            if r_mini in task["pending_reports"]:
                                task["pending_reports"].remove(r_mini)
                            if len(task["pending_reports"]) == 0:
                                send_to_central_pc(client_id, {"action": "BUFF_COMPLETE", "char_id": r_char_id})
                                print(f"✨ [통제실] {r_char_id} 최종 버프 완수! 사냥터 복귀 지시.")
                                
                                if r_char_id in history_target_casts:
                                    del history_target_casts[r_char_id]
                                    
                                if r_char_id in buff_fail_tracker:
                                    del buff_fail_tracker[r_char_id]
                                    
                                del active_group_tasks[r_char_id]
                                
                        elif action == "TASK_ABORTED":
                            print(f"🚨 [통제실] {r_char_id} 1타 삑사리/무응답! 임무 취소 및 새치기 방지 예약 가동.")
                            
                            if r_char_id not in buff_fail_tracker:
                                buff_fail_tracker[r_char_id] = curr_time
                                print(f"⏱️ [통제실] {r_char_id} 첫 삑사리 감지! 1분 타이머 가동.")

                            for m_key in task.get("pending_reports", set()):
                                mini_queues[m_key].put({"action": "ABORT_BUFF", "char_id": r_char_id})
                                
                            target_srv = task.get("server")
                            if target_srv:
                                reserved_servers[target_srv] = {
                                    "char_id": r_char_id, 
                                    "expire": curr_time + 20.0
                                }
                                print(f"🔒 [통제실 보안] {target_srv} 서버 예약석 40초 잠금! (새치기 차단)")
                                
                            del active_group_tasks[r_char_id]

            # 2. 새로운 버프 요청 처리 
            req_to_process = None
            req_index = -1
            target_server = None
            
            with global_req_queue.mutex:
                    # 🚀 [VIP 수던 새치기 자동 정렬] 
                    sorted_queue = sorted(list(global_req_queue.queue), key=lambda req: 0 if any(d in str(req.get("dungeon_name", "")) for d in ["본던", "수던"]) else 1)
                    global_req_queue.queue.clear()
                    global_req_queue.queue.extend(sorted_queue)

                    with task_lock:
                        i = 0
                        while i < len(global_req_queue.queue):
                            req = global_req_queue.queue[i]
                            chk_char = str(req.get("char_id"))
                            
                            if chk_char in buff_fail_tracker and (curr_time - buff_fail_tracker[chk_char]) > 60.0:
                                # 🚀 [핵심 수술] 1분 이상 버프 삑사리 시 강촐(CMD_FORCE_HUNT_HASTE) 발송 완전 삭제!
                                # 대신, 예약석(잠금)만 해제하고 대기열 맨 뒤로 보내서 밀려있던 다른 캐릭이 먼저 버프를 받도록 양보합니다.
                                print(f"🔄 [순서 양보] 사냥컴({chk_char}) 1분 초과 삑사리! 강촐 우회 지시를 삭제하고 대기열 맨 뒤로 보내 타 캐릭부터 진행합니다.")
                                del buff_fail_tracker[chk_char] # 타이머 리셋
                                
                                try: chk_pc = int(chk_char.split('-')[0])
                                except: chk_pc = 0
                                chk_srv = get_target_server(chk_pc, chk_char)
                                
                                # 1. 예약석 잠금 해제 (다른 캐릭이 먼저 버퍼를 쓸 수 있게 길을 터줌)
                                if chk_srv in reserved_servers and reserved_servers[chk_srv]["char_id"] == chk_char:
                                    del reserved_servers[chk_srv]
                                    
                                # 2. 해당 캐릭을 큐의 맨 뒤로 보내서 순서 양보
                                popped_req = global_req_queue.queue.pop(i)
                                global_req_queue.queue.append(popped_req)
                                
                                # 큐 순서가 변경되었으므로 안전하게 처음부터 다시 스캔
                                break
                            i += 1

                    # 👑 [해결의 핵심] 1차 스캔: 이번 턴에 해당하는 서버 캐릭터만 쏙 빼갑니다!
                    for i, req in enumerate(global_req_queue.queue):
                        char_id = str(req.get("char_id"))
                        try: pc_num = int(char_id.split('-')[0])
                        except: pc_num = 0
                        srv = get_target_server(pc_num, char_id)
                        
                        # 💡 이번 턴 서버(예: 파아그리오)가 아니면 일단 패스! (길 터주기)
                        if srv != priority_server: 
                            continue
                            
                        is_busy = any(t["server"] == srv for t in active_group_tasks.values())
                        is_reserved = srv in reserved_servers and reserved_servers[srv]["char_id"] != char_id
                        
                        if not is_busy and not is_reserved:
                            req_to_process = req
                            req_index = i
                            target_server = srv
                            break
                            
                    # 👑 [해결의 핵심] 2차 스캔: 만약 1차 스캔에서 못 찾았다면, 그때 나머지 서버를 확인합니다.
                    if not req_to_process:
                        for i, req in enumerate(global_req_queue.queue):
                            char_id = str(req.get("char_id"))
                            try: pc_num = int(char_id.split('-')[0])
                            except: pc_num = 0
                            srv = get_target_server(pc_num, char_id)
                            
                            # 💡 아까 1차에서 검사한 서버는 빼고 검사
                            if srv == priority_server: 
                                continue
                                
                            is_busy = any(t["server"] == srv for t in active_group_tasks.values())
                            is_reserved = srv in reserved_servers and reserved_servers[srv]["char_id"] != char_id
                            
                            if not is_busy and not is_reserved:
                                req_to_process = req
                                req_index = i
                                target_server = srv
                                break
                            
            if req_to_process:
                char_id = str(req_to_process.get("char_id"))
                client_id = req_to_process.get("client_id")
                dungeon_name = req_to_process.get("dungeon_name", "본던 1층")
                
                with task_lock:
                    if target_server in reserved_servers and reserved_servers[target_server]["char_id"] == char_id:
                        del reserved_servers[target_server]
                        print(f"🔓 [보안] {char_id} 복귀 완료. {target_server} 예약석 해제.")

                # 💡 인증(CERTI_) 진행 중인 군주는 가용 버퍼 명단에서 즉시 열외하여 사냥컴 대기열 병목 원천 차단!
                active_minis = [
                    m for m in SERVER_ASSIGNMENTS.get(target_server, []) 
                    if ai_states.get(m, {}).get("is_hunt_active", False)
                    and ai_states.get(m, {}).get("cmd_fsm") == "IDLE"
                    and not str(ai_states.get(m, {}).get("target_fsm", "")).startswith("CERTI_")
                ]
                
                buffers_mp = {}
                for m in active_minis:
                    st = ai_states.get(m, {})
                    mp_buf = st.get("mp_buffer", [])
                    if len(mp_buf) >= 3: buffers_mp[m] = sorted(mp_buf)[len(mp_buf)//2]
                    elif mp_buf: buffers_mp[m] = mp_buf[-1]
                    else: buffers_mp[m] = 0.0
                        
                # 🚀 [이벤트 던전 추가] "event" 또는 "이벤트"가 포함된 모든 던전(event1~10 등)을 탄력적 헤이방수로 자동 적용!
                ELASTIC_DUNGEONS = [
                    "기란 1층", "기란 2층", "개미굴 1층", "개미굴 2층", "개미굴 3층", 
                    "개미굴 4층", "개미굴 5층", "개미굴 6층", "개미굴 7층", "개미굴 8층", 
                    "사던 2층", "사던 3층", "event", "이벤트"
                ]
                
                is_elastic = any(d.lower() in str(dungeon_name).lower() for d in ELASTIC_DUNGEONS)
                
                def get_buffer_casts(mp):
                    if mp >= 100.0: return 6
                    if mp >= 84.0: return 5
                    if mp >= 67.0: return 4
                    if mp >= 50.0: return 3
                    if mp >= 33.0: return 2
                    if mp >= 16.0: return 1
                    return 0
                    
                total_current_casts = sum(get_buffer_casts(mp) for mp in buffers_mp.values()) if buffers_mp else 0
                num_buffers = len(buffers_mp)
                
                queue_length = 0
                fixed_dungeon_wait_count = 0
                
                with global_req_queue.mutex:
                    for r in global_req_queue.queue:
                        r_cid = str(r.get("char_id"))
                        try: r_pc = int(r_cid.split('-')[0])
                        except: r_pc = 0
                        
                        if get_target_server(r_pc, r_cid) == target_server:
                            if r_cid != char_id:
                                queue_length += 1
                                
                            # 🚀 [신규 추가] 해당 서버 대기열에 쌓인 수던/본던 캐릭 수를 정확하게 카운트 (본인 포함)
                            r_dname = str(r.get("dungeon_name", ""))
                            if any(d in r_dname for d in ["본던", "수던"]):
                                fixed_dungeon_wait_count += 1
                                
                # =====================================================================
                # 🚀 [알파고급 자원 관리 엔진 V2] 개별 약효 추적 & 대기열 비례 계단식 복용 엔진
                # =====================================================================
                active_blue_minis = []
                inactive_blue_minis = []
                
                for m in active_minis:
                    # 💡 10분(600초) 개별 타이머가 돌고 있다면 약효 지속 중!
                    if curr_time < ai_states.get(m, {}).get("buff_blue_pot_time", 0):
                        active_blue_minis.append(m)
                    else:
                        inactive_blue_minis.append(m)
                        
                # 👑 단 1명이라도 약효가 지속 중이면 전체를 파랭이 부스터(6방 고정) 모드로 판단
                is_blue_pot_active = len(active_blue_minis) > 0
                
                # 👑 [VIP 수던/본던 강제 발동 스위치] 대기자 수에 비례한 타겟 수
                # 대기 2명: 1명 복용 / 대기 3명: 2명 복용 / 대기 4명 이상: 3명 복용
                target_vip_blue_count = 0
                if fixed_dungeon_wait_count >= 2:
                    target_vip_blue_count = min(num_buffers, fixed_dungeon_wait_count - 1)
                
                # 이미 먹은 인원을 제외하고 '추가로' 먹어야 할 인원수 계산
                needed_vip_drinks = max(0, target_vip_blue_count - len(active_blue_minis))
                
                drink_candidates = []
                deficit_trigger = False
                final_threshold = 0
                deficit_casts = 0
                total_required_casts = 0
                
                # 💡 아직 안 먹은 인원(inactive_blue_minis)이 있을 때만 팩트체크 진행
                if inactive_blue_minis and num_buffers > 0:
                    # 🚨 오링(증발) 패널티를 받는 놈은 후보에서 제외하여 다른 버퍼에게 기회 양보
                    valid_inactive_minis = [m for m in inactive_blue_minis if curr_time >= ai_states.get(m, {}).get("blue_pot_penalty_time", 0)]
                    
                    vip_candidates = []
                    if needed_vip_drinks > 0 and valid_inactive_minis:
                        # 🚀 마나가 가장 적은(가장 헐떡이는) 버퍼부터 정렬해서 핀셋으로 뽑아 먼저 먹임!
                        sorted_valid = sorted(valid_inactive_minis, key=lambda x: buffers_mp.get(x, 100.0))
                        vip_candidates = sorted_valid[:needed_vip_drinks]
                        drink_candidates.extend(vip_candidates)
                        
                    # 일반 결손치(Deficit) 계산
                    pot_thresholds = []
                    use_blue_pot_any = False
                    
                    for m in inactive_blue_minis:
                        settings = current_settings.get(m, {})
                        if settings.get("use_blue_pot", False):
                            use_blue_pot_any = True
                            try: val = int(float(settings.get("blue_deficit", 11)))
                            except: val = 11
                            pot_thresholds.append(val)
                                
                    if use_blue_pot_any and pot_thresholds:
                        synced_threshold = min(pot_thresholds)
                        total_required_casts = (queue_length + 1) * 6
                        deficit_casts = max(0, total_required_casts - total_current_casts)
                        final_threshold = synced_threshold * num_buffers
                        
                        if deficit_casts >= final_threshold:
                            deficit_trigger = True
                            for m in valid_inactive_minis:
                                if m not in drink_candidates and current_settings.get(m, {}).get("use_blue_pot", False):
                                    drink_candidates.append(m)
                                    
                if drink_candidates:
                    drinks_consumed = 0
                    actually_drink_minis = []
                    
                    for m in drink_candidates:
                        # 📸 [실시간 팩트체크] 복용 대상자의 우측 하단 200x160 영역 스캔!
                        has_pot = False
                        img_bgr = latest_frames.get(m)
                        tmpl = WW_TEMPLATES.get("bluepot2")
                        
                        if img_bgr is not None and tmpl and tmpl["color"] is not None:
                            h_img, w_img = img_bgr.shape[:2]
                            roi_y1 = max(0, h_img - 160)
                            roi_x1 = max(0, w_img - 200)
                            roi = img_bgr[roi_y1:h_img, roi_x1:w_img]
                            try:
                                if tmpl["mask"] is not None:
                                    res = cv2.matchTemplate(roi, tmpl["color"], cv2.TM_CCORR_NORMED, mask=cv2.merge([tmpl["mask"]]*3))
                                else:
                                    res = cv2.matchTemplate(roi, tmpl["color"], cv2.TM_CCOEFF_NORMED)
                                _, max_val, _, _ = cv2.minMaxLoc(res)
                                
                                if max_val >= 0.80: has_pot = True
                            except: pass
                                
                        if has_pot:
                            if ai_states.get(m, {}).get("blue_pot_empty_logged", False):
                                print(f"✅ [{m}] 퀵슬롯에 파랭이(bluepot2.png) 실시간 재감지! 스마트 복용 모드를 재개합니다.")
                                ai_states[m]["blue_pot_empty_logged"] = False
                            actually_drink_minis.append(m)
                        else:
                            if not ai_states.get(m, {}).get("blue_pot_empty_logged", False):
                                print(f"⚠️ [{m}] 파랭이 오링(증발) 실시간 감지! 헛클릭 방지 3초 패널티 가동 및 다음 버퍼로 기회 양보.")
                                ai_states[m]["blue_pot_empty_logged"] = True
                            ai_states[m]["blue_pot_penalty_time"] = curr_time + 3.0 
                            
                    if actually_drink_minis:
                        if needed_vip_drinks > 0 and any(m in vip_candidates for m in actually_drink_minis):
                            print(f"🚨 [{target_server}] VIP 수던/본던 대기자 {fixed_dungeon_wait_count}명! 계단식 파랭이 부스터 투입: {actually_drink_minis}")
                        elif deficit_trigger:
                            print(f"💊 [{target_server}] 파랭이 결손치 부스터 가동: {actually_drink_minis} (결핍:{deficit_casts}방 >= 임계치:{final_threshold}방)")
                            
                        for m in actually_drink_minis:
                            # 💡 찰나의 순간 마우스와 꼬이지 않도록 큐에 깔끔하게 넣음
                            pico_queues[m].put({"action": "TAKE_BLUE_POTION"})
                            pico_queues[m].put({"action": "WAIT", "delay_min": 0.4, "delay_max": 0.6})
                            
                            # 🚀 먹자마자 바로 10분(600초) 개별 타이머 가동!
                            ai_states[m]["buff_blue_pot_time"] = curr_time + 600.0 
                            print(f"🧃 [{m}] 파랭이 개별 섭취 완료! (해당 봇 10분간 지속 효과 돌입)")
                            drinks_consumed += 1
                            
                        is_blue_pot_active = True 
                    
                    if drinks_consumed > 0:
                        save_buff_times(ai_states) 
                # =====================================================================
                
                target_casts = 6 
                mode_str = ""
                
                remembered_target = None
                if char_id in history_target_casts:
                    remembered_target = history_target_casts[char_id]["casts"]
                
                # 🚀 [고정 사냥터] "본던" 또는 "수던"은 복수버퍼/탄력 룰 모두 씹고 무조건 6방 고정!
                is_fixed_dungeon = any(d in str(dungeon_name) for d in ["본던", "수던"])
                
                # 🚀 [파랭이 부스터 & 고정 사냥터] 무조건 6방 풀버프 고정!
                if is_blue_pot_active or is_fixed_dungeon:
                    if is_blue_pot_active:
                        mode_str = "파랭이부스터(무조건6방)"
                    else:
                        mode_str = "고정사냥터(무조건6방)"
                    target_casts = 6
                    history_target_casts[char_id] = {"casts": target_casts, "timestamp": curr_time}
                else:
                    if num_buffers > 1:
                        mode_str = "복수버퍼(우선)"
                        if remembered_target is not None:
                            target_casts = remembered_target
                            mode_str += "-기억복구"
                        else:
                            if total_current_casts < 2: target_casts = 4
                            else: target_casts = 6
                            
                            if queue_length > 0:
                                dynamic_target = max(4, min(6, (total_current_casts // 2) * 2))
                                target_casts = dynamic_target if total_current_casts >= 4 else 4
                                
                            if target_casts != 6: # 6방은 기억할 필요 없음
                                history_target_casts[char_id] = {"casts": target_casts, "timestamp": curr_time}
                            
                    elif num_buffers == 1:
                        if is_elastic:
                            mode_str = "1인/탄력"
                            if remembered_target is not None:
                                target_casts = remembered_target
                                mode_str += "-기억복구"
                            else:
                                mp = list(buffers_mp.values())[0] if buffers_mp else 0
                                if mp <= 10.0: target_casts = 2
                                elif mp <= 30.0: target_casts = 3
                                elif mp <= 50.0: target_casts = 4
                                elif mp <= 70.0: target_casts = 5
                                else: target_casts = 6
                                
                                if queue_length > 0:
                                    target_casts = max(2, min(6, total_current_casts))
                                    
                                if target_casts != 6:
                                    history_target_casts[char_id] = {"casts": target_casts, "timestamp": curr_time}
                        else:
                            mode_str = "1인/고정"
                            target_casts = 6
                            history_target_casts[char_id] = {"casts": target_casts, "timestamp": curr_time}

                alloc = None
                # 🚀 파랭이 상태이거나 고정 사냥터면 최소 6방이 모일 때까지 절대 승인 안 함!
                min_required_casts = 6 if (is_blue_pot_active or is_fixed_dungeon) else (4 if num_buffers > 1 else 2)
                
                if total_current_casts >= target_casts and target_casts >= min_required_casts:
                    alloc = allocate_casts(buffers_mp, target_casts)

                if alloc:
                    with global_req_queue.mutex:
                        del global_req_queue.queue[req_index]
                        
                    first_shooter = list(alloc.keys())[0] 
                    
                    with task_lock:
                        active_group_tasks[char_id] = {
                            "client_id": client_id,
                            "server": target_server,
                            "alloc": alloc,
                            "pending_reports": set(alloc.keys()),
                            "timeout": curr_time + 40.0,
                            "first_shooter": first_shooter
                        }
                    
                    print(f"🧮 [{target_server}] 사냥컴({char_id}) {dungeon_name}({mode_str}) {target_casts}방 배분 완료! ➔ " + ", ".join([f"{k}({v}방)" for k, v in alloc.items()]) + f" | ★1타 대장: {first_shooter}")
                    
                    for mini_key in alloc.keys():
                        if mini_key in ai_states: ai_states[mini_key]["cmd_fsm"] = "ASSIGNED"
                    
                    send_to_central_pc(client_id, {"action": "CMD_MOVE_1CELL", "char_id": char_id, "commander_pc": first_shooter})
                        
                    for mini_key, cast_count in alloc.items():
                        mini_queues[mini_key].put({
                            "action": "DO_BUFF_TASK", 
                            "char_id": char_id, 
                            "client_id": client_id,
                            "cast_count": cast_count,
                            "is_first_shooter": (mini_key == first_shooter)
                        })

                else:
                    if curr_time - last_mp_wait_log.get(target_server, 0.0) > 5.0:
                        with global_req_queue.mutex:
                            waiting_chars = []
                            for r in global_req_queue.queue:
                                r_cid = str(r.get("char_id"))
                                try: r_pc = int(r_cid.split('-')[0])
                                except: r_pc = 0
                                
                                # 💡 [핵심] 현재 target_server(파아/캐스톨) 소속인 캐릭들만 핀셋으로 골라냅니다!
                                if get_target_server(r_pc, r_cid) == target_server:
                                    r_dname = str(r.get("dungeon_name", ""))
                                    mark = "[수던VIP]" if any(d in r_dname for d in ["본던", "수던"]) else ""
                                    waiting_chars.append(f"{r_cid}{mark}")
                        
                        mp_status = " / ".join([f"{k}:{v:.1f}%({get_buffer_casts(v)}방)" for k, v in buffers_mp.items()])
                        print(f"💤 [{target_server}] 버퍼 마나 충전 대기 중... [목표:{target_casts}방, 현재가능:{total_current_casts}방] [{mp_status}] (대기열 {len(waiting_chars)}명: {', '.join(waiting_chars)})")
                        last_mp_wait_log[target_server] = curr_time
                                
        except Exception: pass
        time.sleep(0.1)

threading.Thread(target=dispatcher_thread, daemon=True).start()

def command_server_thread():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', CMD_PORT))
    server.listen(20)
    print(f"\n📡 [통제실 네트워크] 1타 팩트체크 스마트 라우터 가동 완료! (포트: {CMD_PORT})")
    
    def handle_client(client_socket, addr):
        client_ip = addr[0]
        client_id = f"{client_ip}:{addr[1]}"
        connected_clients[client_id] = {"status": "connected", "socket": client_socket}
        
        buffer = ""  # 🚀 [수술 1] 패킷 엉킴 방지용 버퍼
        
        while True:
            try:
                data = client_socket.recv(4096)
                if not data: break
                
                buffer += data.decode('utf-8')
                
                # 🚀 \n 기준으로 패킷을 완벽히 분리하여 1개씩 처리!
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line: continue
                    
                    msg = json.loads(line)
                    action = msg.get("action", "")
                    char_id = str(msg.get("char_id", ""))
                    

                    msg['client_id'] = client_id
                    
                    if action == "REQ_BUFF":
                        # 🚀 [추가] 엠피 유무, 대기열 상관없이 일단 버프 요청이 오면 0.01초 만에 "통신양호" 팩트 회신!
                        ack_msg = {"action": "CC_STATUS_OK", "char_id": char_id}
                        try:
                            client_socket.send((json.dumps(ack_msg, ensure_ascii=False) + "\n").encode('utf-8'))
                            print(f"📡 [통제실] {char_id} 버프 요청 수신! 즉각 통신양호(CC_STATUS_OK) 신호 발송 완료.")
                        except Exception as e: pass
                        
                        # 🚀 [중복 예약 방지] 사냥컴이 지속적으로 요청(생존핑)을 보내도 큐에 1번만 등록되게 기억(방어막)!
                        with global_req_queue.mutex:
                            already_in_queue = any(str(req.get("char_id")) == char_id for req in global_req_queue.queue)
                        with task_lock:
                            already_in_process = char_id in active_group_tasks
                            
                        if not already_in_queue and not already_in_process:
                            global_req_queue.put(msg)
                            print(f"📝 [대기열 등록] {char_id}가 대기 명단에 추가되었습니다. (현재 대기자: {global_req_queue.qsize()}명)")
                            
                    elif action == "SEND_ANGLE":
                        with task_lock:
                            if char_id in active_group_tasks:
                                task = active_group_tasks[char_id]
                                angle_deg = float(msg.get("angle"))
                                for mini_key in task["pending_reports"]:
                                    mini_queues[mini_key].put({"action": "SEND_ANGLE", "char_id": char_id, "angle": angle_deg})

                    elif action == "FIRST_BUFF_OK":
                        with task_lock:
                            # 👇👇👇 [신규 추가] 1타 성공 시 어리버리 장부 초기화! 👇👇👇
                            if char_id in buff_fail_tracker:
                                del buff_fail_tracker[char_id]
                                print(f"✨ [보안] {char_id} 1타 명중으로 어리버리 타이머 팩트체크 초기화!")
                            
                            if char_id in active_group_tasks:
                                task = active_group_tasks[char_id]
                                print(f"✅ [통제실] {char_id} 1타 명중 확인 (OK)! 잔여 버프 발사 지시.")
                                for mini_key in task["pending_reports"]:
                                    mini_queues[mini_key].put({"action": "PROCEED_BUFF", "char_id": char_id})

                    elif action == "FIRST_BUFF_FAIL":
                        with task_lock:
                            # 🚀 예약석(Lock) 설정과 버퍼 멍때림 해제(ABORT_BUFF)는 위쪽 dispatcher_thread의 TASK_ABORTED에서 처리합니다!
                            if char_id in active_group_tasks:
                                print(f"🚨 [통제실] {char_id} 1타 삑사리 감지 (FAIL)! 즉각 사격 중지 및 예약 장부 가동.")
                                internal_router_queue.put({"action": "TASK_ABORTED", "mini_key": "ALL", "char_id": char_id})
                                
                    elif action == "PING":
                        with global_req_queue.mutex:
                            # 🚀 [추가] 대기열에 있다면 최신 통신 소켓으로 갱신!
                            for req in global_req_queue.queue:
                                if str(req.get("char_id")) == char_id:
                                    req["client_id"] = client_id
                                    break
                            already_in_queue = any(str(req.get("char_id")) == char_id for req in global_req_queue.queue)
                            
                        with task_lock:
                            # 🚀 [추가] 이미 작업 중인 캐릭이어도 최신 소켓으로 갱신!
                            if char_id in active_group_tasks:
                                active_group_tasks[char_id]["client_id"] = client_id
                            already_in_process = char_id in active_group_tasks
                            
                        # 🚨 장부에 없는데 핑이 왔다면? -> 통제실이 재시작 된 것이므로 핑을 보낸 놈을 즉각 대기 명단에 복구!
                        if not already_in_queue and not already_in_process:
                            global_req_queue.put(msg)
                            print(f"🔄 [기억 자동 복구] 미등록 캐릭({char_id})의 PING 수신! 재시작으로 간주하고 대기열에 즉각 편입합니다. (현재 대기자: {global_req_queue.qsize()}명)")

                    # 🚀 이 부분(ACK 전송)도 탭 안쪽으로 들어와야 합니다!
                    response = {"status": "ack", "received_action": action}
                    try: client_socket.send((json.dumps(response) + "\n").encode('utf-8'))
                    except: pass
                    # 👆👆👆 [여기까지 들여쓰기 탭 묶기 끝!] 👆👆👆
                
            except Exception: break
        if client_id in connected_clients: del connected_clients[client_id]
        client_socket.close()

    while True:
        try:
            client_sock, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()
        except Exception: time.sleep(1)

threading.Thread(target=command_server_thread, daemon=True).start()

# ==========================================
# 0-1. 🚑 코어 단축키 상수 맵핑 및 게임 내 퀵슬롯 세팅 가이드
# ==========================================
# 🟢 [1번 페이지 (F1) - 전투/생존/루팅]
# F4: 아이템 줍기 (SWEEP)
# F5: 체력 회복 물약 (POTION)
# F6: 힐 (HEAL)
# F7: 바디 투 마인드 (BODY_TO_MIND)
# F8: 귀환 (ESCAPE)
# F10: 해독제 / 큐어 포이즌 (ANTIDOTE)
# F11: 텔레포트 (TELEPORT)

# 🔵 [2번 페이지 (F2) - 메인 버프]
# F5: 실드 (Shield)
# F6: 홀리 웨폰 (Holy Weapon)
# F7: 인챈트 웨폰 (Enchant Weapon)
# F8: 블레스드 아머 (Blessed Armor)
# F9: 변신 주문서/스킬 (Trans)
# F10: 기타 버프
# F11: 덱스업/인덱 (Dex)
# F12: 디크리즈 웨이트 (Decrease Weight)

# 🟣 [3번 페이지 (F3) - 보조 버프]
# F12: 라이트 (Light)

# ==============================================================================
# [AI ASSISTANT STRICT DIRECTIVE - READ CAREFULLY BEFORE MODIFYING]
# 1. 절대 금지: 기존 기능의 삭제, 축소, 임의 수정, 변수명 변경을 엄격히 금지합니다.
# 2. 기능 추가 원칙: 사용자가 요청한 '새로운 기능'만 코드에 추가하십시오.
# 3. 로직 보존: 기존의 제어 흐름(if/else 분기), 딜레이(time.sleep), 스레드 구조는 100% 원본 그대로 유지해야 합니다.
# 4. 주석 보존: 기존에 작성된 모든 설명 및 디버그용 주석은 삭제하지 말고 유지하십시오.
# 5. 리팩토링 금지: 자체적인 최적화나 리팩토링을 수행하지 마십시오.
# 6. 모든 딜레이는 가우스난수를 사용한다 일반 random 사용금지.
# 7. 모든 이미지는 매크로 폴더내 >> qq폴더에 저장됨
# ==============================================================================

# ==========================================
# 🌟 [다중 맵 개별 할당 & 욜로 뇌(GPU) 공유 매니저]
# ==========================================
DUNGEON_SCALE_X = 0.1
DUNGEON_SCALE_Y = 0.1

# =================================================================
# 📐 [절대 각도 맵핑] 형님이 직접 측정한 리니지 8방향 타일 절대 각도!
# =================================================================
LINEAGE_ANGLES = {
    "3시": 359.0,
    "5시": 30.0,
    "6시": 92.0,
    "7시": 150.0,
    "9시": 181.0,
    "11시": 210.0,
    "12시": 268.0,
    "1시": 330.0
}

# 🚀 장애물(길막) 발생 시 좌/우로 1칸씩 비켜가기 위한 회피(우회) 사전
EVADE_MAP = {
    330.0: [268.0, 359.0],   # 1시 막힘 -> 12시 or 3시로 회피
    359.0: [330.0, 30.0],  # 3시 막힘 -> 1시 or 5시로 회피
    30.0:  [359.0, 92.0],    # 5시 막힘 -> 3시 or 6시로 회피
    92.0:  [30.0, 150.0],  # 6시 막힘 -> 5시 or 7시로 회피
    150.0: [92.0, 181.0],  # 7시 막힘 -> 6시 or 9시로 회피
    181.0: [150.0, 210.0], # 9시 막힘 -> 7시 or 11시로 회피
    210.0: [181.0, 268.0], # 11시 막힘 -> 9시 or 12시로 회피
    268.0: [210.0, 330.0]  # 12시 막힘 -> 11시 or 1시로 회피
}

# 🚀 맵/그래프는 개별 로드, YOLO 모델은 던전 계열별로 묶어서 1개만 공유!
DUNGEON_ASSETS = {
    "기란 1층": {"map": "giran_full_map_topdown.png", "graph": "giran1f_graph.json", "model": "best.pt"},
    "기란 2층": {"map": "giran2map.png", "graph": "giran2f_graph.json", "model": "best.pt"},
    "개미굴 1층": {"map": "ant1map.png", "graph": "ant1_graph.json", "model": "ant.pt"},
    "개미굴 2층": {"map": "ant2map.png", "graph": "ant2_graph.json", "model": "ant.pt"},
    "개미굴 3층": {"map": "ant3map.png", "graph": "ant3_graph.json", "model": "ant.pt"},
    "개미굴 4층": {"map": "ant4map.png", "graph": "ant4_graph.json", "model": "ant.pt"},
    "개미굴 5층": {"map": "ant5map.png", "graph": "ant5_graph.json", "model": "ant.pt"},
    "개미굴 6층": {"map": "ant6map.png", "graph": "ant6_graph.json", "model": "ant.pt"},
    "개미굴 7층": {"map": "ant7map.png", "graph": "ant7_graph.json", "model": "ant.pt"},
    "개미굴 8층": {"map": "ant8map.png", "graph": "ant8_graph.json", "model": "ant.pt"},
    "사던 2층": {"map": "silver2map.png", "graph": "silver2_graph.json", "model": "silver.pt"},
    "사던 3층": {"map": "silver3map.png", "graph": "silver3_graph.json", "model": "silver.pt"},
    "본던 3층": {"map": "gludio3map.png", "graph": "gludio3_graph.json", "model": "gludio.pt"},
    "본던 4층": {"map": "gludio4map.png", "graph": "gludio4_graph.json", "model": "gludio.pt"},
    "본던 5층": {"map": "gludio5map.png", "graph": "gludio5_graph.json", "model": "gludio.pt"},
    "본던 6층": {"map": "gludio6map.png", "graph": "gludio6_graph.json", "model": "gludio.pt"}
}

# 💡 이미 로드된 자원을 재활용하기 위한 메모리 창고
loaded_models = {}
loaded_maps = {}
asset_lock = threading.Lock() # 🚀 [VRAM 폭발 차단 자물쇠]

def get_pc_assets(dungeon_name):
    """각 미니PC가 자기가 있는 층수의 지도와 뇌(YOLO)를 꺼내갑니다."""
    assets = DUNGEON_ASSETS.get(dungeon_name)
    if not assets: return {"gray": None, "edges": None, "graph": None, "model": None}
    
    model_path = assets.get("model", "best.pt")
    
    if model_path in loaded_models and dungeon_name in loaded_maps:
        res = loaded_maps[dungeon_name]
        # 🚀 gray_los 추가!
        return {"gray": res["gray"], "gray_los": res.get("gray_los"), "edges": res["edges"], "graph": res["graph"], "model": loaded_models[model_path], "offset": res.get("offset", (0, 0))}
        
    # 캐시에 없어서 '최초 로딩'이 필요할 때만 1명씩 자물쇠를 열고 들어감!
    with asset_lock: 
        return _get_pc_assets_internal(dungeon_name)

def _get_pc_assets_internal(dungeon_name): # 💡 기존 코드 들여쓰기 100% 보존 꼼수!
    assets = DUNGEON_ASSETS.get(dungeon_name)
    if not assets: return {"gray": None, "gray_los": None, "edges": None, "graph": None, "model": None}
    
    model_path = assets.get("model", "best.pt")
    map_path = assets["map"]
    graph_path = assets["graph"]
    
    # 🧠 1. YOLO 뇌 로딩 (이미 로드된 테마 모델이면 중복 로드 안 하고 그걸 그대로 공유!)
    if model_path not in loaded_models:
        try:
            print(f"\n🧠 [YOLO 로드] 특화 뇌({model_path})를 4070 Ti에 이식 중...")
            loaded_models[model_path] = YOLO(model_path)
            print(f"✅ [YOLO 완료] {model_path} 장착 완료!")
        except Exception as e:
            print(f"⚠️ YOLO 모델 '{model_path}' 로드 실패: {e}")
            loaded_models[model_path] = None
            
    # 🗺️ 2. 지도 및 노선도 로딩 (이미 읽은 지도는 그대로 던져줌)
    if dungeon_name not in loaded_maps:
        map_gray, map_edges, pc_graph = None, None, None
        map_gray_los = None # 💡 시야용 맵 변수를 미리 만들어 둡니다.
        
        if os.path.exists(map_path):
            map_gray = cv2.imread(map_path, cv2.IMREAD_GRAYSCALE)
            if map_gray is not None:
                map_edges = cv2.Canny(map_gray, 50, 150)
                
        if os.path.exists(graph_path):
            try:
                with open(graph_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # 🚀 [형님의 타일 그리드 시스템 이식] 
                    # 기존 X,Y 뿐만 아니라 U,V, Manual 좌표, 그리고 포탈(is_portal) 꼬리표까지 모조리 파이썬 뇌에 박제합니다!
                    nodes = {}
                    for n in data.get("nodes", []):
                        nodes[int(n["id"])] = {
                            "x": n["x"], 
                            "y": n["y"], 
                            "u": n.get("u", 0), 
                            "v": n.get("v", 0),
                            "manual": n.get("manual", False),
                            "is_portal": n.get("is_portal", False),
                            "is_special": n.get("is_special", False) # 🚨 [치명적 흑막 수술 1] JSON에서 스페셜 꼬리표 챙겨오기!
                        }
                    
                    # 🚀 [앵커(ANCHOR) 역추산 엔진] 
                    anchor_x, anchor_y = -1000, -1000
                    if nodes:
                        first_node = list(nodes.values())[0]
                        anchor_x = first_node["x"] - (first_node["u"] * 5 - first_node["v"] * 5) // 2
                        anchor_y = first_node["y"] - (first_node["u"] * 5 + first_node["v"] * 5) // 4
                        print(f"🎯 [{dungeon_name}] 서버 타일 시스템 앵커 복원 완료! (X:{anchor_x}, Y:{anchor_y})")

                    edges = {}
                    for e in data.get("edges", []):
                        u_node, v_node = int(e["u"]), int(e["v"])
                        if u_node not in edges: edges[u_node] = []
                        if v_node not in edges: edges[v_node] = []
                        edges[u_node].append(v_node)
                        edges[v_node].append(u_node)
                        
                    # ========================================================
                    # 🚀 [듀얼 맵 시스템] 걷기용(충돌) 맵과 시야용(LOS) 맵 완벽 분리!
                    # 걷기용(map_gray)은 1픽셀도 안 건드리고 순정 유지! (벽 비비기 원천 차단)
                    # 시야용(map_gray_los)에만 형님표 핀셋 픽셀로 얇게 샛길을 뚫어줍니다!
                    # ========================================================
                    if map_gray is not None:
                        map_gray_los = map_gray.copy() # 💡 [핵심 1] 원본 훼손을 막기 위해 도화지를 1장 복사합니다!
                        drawn_edges = set() 
                        for u_node, v_nodes in edges.items():
                            for v_node in v_nodes:
                                if u_node in nodes and v_node in nodes:
                                    edge_key = tuple(sorted((u_node, v_node)))
                                    if edge_key in drawn_edges: continue
                                    drawn_edges.add(edge_key)
                                    
                                    p1, p2 = nodes[u_node], nodes[v_node]
                                    if p1.get("manual", False) or p2.get("manual", False):
                                        du = abs(p1.get("u", 0) - p2.get("u", 0))
                                        dv = abs(p1.get("v", 0) - p2.get("v", 0))
                                        
                                        if du <= 1 and dv <= 1:
                                            # 🚀 형님표 정밀 타격 로직 그대로 유지!
                                            x1, y1 = int(p1["x"]), int(p1["y"])
                                            x2, y2 = int(p2["x"]), int(p2["y"])
                                            
                                            steps = max(abs(x2 - x1), abs(y2 - y1))
                                            if steps > 0:
                                                for i in range(steps + 1):
                                                    px = int(round(x1 + (x2 - x1) * (i / steps)))
                                                    py = int(round(y1 + (y2 - y1) * (i / steps)))
                                                    # 🚨 [핵심 2] 원본(map_gray) 대신 시야맵(map_gray_los)에 점을 찍습니다!
                                                    if 0 <= py < map_gray_los.shape[0] and 0 <= px < map_gray_los.shape[1]:
                                                        map_gray_los[py, px] = 255
                                            else:
                                                # 🚨 [핵심 2] 원본(map_gray) 대신 시야맵(map_gray_los)에 점을 찍습니다!
                                                if 0 <= y1 < map_gray_los.shape[0] and 0 <= x1 < map_gray_los.shape[1]:
                                                    map_gray_los[y1, x1] = 255
                    # ========================================================
                    
                    if nodes:
                        # 💡 nodes의 구조가 딕셔너리로 바뀌었으므로 [0], [1] 대신 ["x"], ["y"] 로 뽑아오도록 수식 유지!
                        avg_x = sum(n["x"] for n in nodes.values()) / len(nodes)
                        avg_y = sum(n["y"] for n in nodes.values()) / len(nodes)
                        center_node = min(nodes.items(), key=lambda item: (item[1]["x"] - avg_x)**2 + (item[1]["y"] - avg_y)**2)[0]
                        cx, cy = nodes[center_node]["x"], nodes[center_node]["y"]
                        
                        PULL_DIST = 50 
                        def pull_inward(raw_node):
                            rx, ry = nodes[raw_node]["x"], nodes[raw_node]["y"]
                            dx, dy = cx - rx, cy - ry
                            dist = math.hypot(dx, dy)
                            if dist <= PULL_DIST: return raw_node
                            nx, ny = dx / dist, dy / dist
                            tx, ty = rx + (nx * PULL_DIST), ry + (ny * PULL_DIST)
                            return min(nodes.items(), key=lambda item: (item[1]["x"] - tx)**2 + (item[1]["y"] - ty)**2)[0]
                        
                        top_raw = min(nodes.items(), key=lambda item: item[1]["y"])[0]
                        bottom_raw = max(nodes.items(), key=lambda item: item[1]["y"])[0]
                        left_raw = min(nodes.items(), key=lambda item: item[1]["x"])[0]
                        right_raw = max(nodes.items(), key=lambda item: item[1]["x"])[0]
                        corners = [pull_inward(top_raw), pull_inward(right_raw), pull_inward(bottom_raw), pull_inward(left_raw)]
                        
                        offset = 120
                        target_pts = [(cx - offset, cy - offset), (cx + offset, cy - offset), (cx + offset, cy + offset), (cx - offset, cy + offset)]
                        sub_centers = [min(nodes.items(), key=lambda item: (item[1]["x"] - tx)**2 + (item[1]["y"] - ty)**2)[0] for tx, ty in target_pts]
                    else:
                        corners, center_node, sub_centers = [], None, []

                    # 💡 그래프 딕셔너리에 계산된 anchor_x, anchor_y (영점) 정보도 함께 넘겨줍니다!
                    pc_graph = {
                        "nodes": nodes, 
                        "edges": edges, 
                        "corners": corners, 
                        "center_node": center_node, 
                        "sub_centers": sub_centers, 
                        "anchor_x": anchor_x, 
                        "anchor_y": anchor_y,
                        "special_nodes": data.get("special_nodes", []) # 🚨 [치명적 흑막 수술 2] 스페셜 리스트 통째로 뇌에 이식!
                    }
            except Exception: pass
            
        # 🚀 [보완] 딕셔너리에 시야용 맵(gray_los)도 잊지 않고 저장합니다!
        loaded_maps[dungeon_name] = {"gray": map_gray, "gray_los": map_gray_los, "edges": map_edges, "graph": pc_graph}
        print(f"🗺️ [{dungeon_name}] 전용 지도 데이터 로드 완료!")
        
    res = loaded_maps[dungeon_name]
    return {"gray": res["gray"], "gray_los": res.get("gray_los"), "edges": res["edges"], "graph": res["graph"], "model": loaded_models[model_path]}

def get_robust_map_pos(img_bgr, full_map_edges_ref, last_pos=None, allow_full_scan=True):
    if img_bgr is None or img_bgr.size == 0 or full_map_edges_ref is None: 
        return None, None
    try:
        minimap_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        h, w = minimap_gray.shape
        
        OFFSET_X = 2  
        OFFSET_Y = 2  
        true_cx = (w // 2) + OFFSET_X
        true_cy = (h // 2) + OFFSET_Y
        
        cv2.circle(minimap_gray, (w // 2, h // 2), 8, 128, -1) 
        minimap_edges = cv2.Canny(minimap_gray, 50, 150)
        
        # =========================================================
        # 🚀 [CPU 스파이크 척결 1] 미니맵 전체 스캔(Full Scan) 방지!
        # 직전 좌표가 있다면, 반경 120픽셀 좁은 구역만 스마트하게 잘라서 매칭 (연산량 95% 삭감)
        # =========================================================
        if last_pos is not None:
            fh, fw = full_map_edges_ref.shape[:2]
            lx, ly = int(last_pos[0]), int(last_pos[1])
            pad = 120
            
            x1 = max(0, lx - true_cx - pad)
            y1 = max(0, ly - true_cy - pad)
            x2 = min(fw, lx - true_cx + w + pad)
            y2 = min(fh, ly - true_cy + h + pad)
            
            # 🚨 [방탄 조끼] 맵 끝자락 모서리 에러 차단
            if x2 > x1 and y2 > y1 and (x2 - x1) >= w and (y2 - y1) >= h:
                local_ref = full_map_edges_ref[y1:y2, x1:x2]
                res = cv2.matchTemplate(local_ref, minimap_edges, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                
                # 일치율이 높으면 국지적 스캔 성공! 
                if max_val >= 0.15:
                    return (max_loc[0] + x1 + true_cx, max_loc[1] + y1 + true_cy), minimap_edges

        # 🚨 [풀스캔 쿨타임 방어막] 허락되지 않았으면 여기서 연산 즉시 종료!
        if not allow_full_scan:
            return None, minimap_edges

        # 🚀 텔레포트 시 또는 초기 로딩 시에만 1회 전체 맵 스캔 발동!
        res = cv2.matchTemplate(full_map_edges_ref, minimap_edges, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        
        if max_val < 0.15: 
            return None, minimap_edges
            
        return (max_loc[0] + true_cx, max_loc[1] + true_cy), minimap_edges
    except:
        return None, None

# ====================================================================
# 🏹 [뼈대 F: V13 궁극체] 미니맵 화살표 방향 절대 추출기 (형님이 인정한 V6 완결판)
# 💡 형님께서 가장 낫다고 하신 V6(세 꼭지점 스캐너)를 원상 복구하고 추출 버그를 잡았습니다!
# 
# [형님 적발: 추출 실패 버그 원인 및 완벽 수술]
# 1. 12시/6시 방향일 때 화살표 선이 얇아지는데, 노이즈 제거 필터(MORPH_OPEN)가 
#    이것을 먼지로 착각하고 아예 지워버려서 각도 갱신이 안 되던(과거 각도 재사용) 버그 완벽 제거!
# 2. 오직 내 화살표 윤곽선만 깨끗한 캔버스에 핀셋으로 빼내어 주변 빨간 경로선 간섭 100% 차단!
# 3. 추출된 각도를 리니지 고유의 '8방향(45도 단위)'으로 자석(Snap) 보정하여 삑사리 원천 봉쇄!
# ====================================================================
def get_character_direction(minimap_bgr):
    """미니맵 BGR 이미지를 받아 캐릭터가 바라보는 방향(라디안 각도)을 반환합니다."""
    if minimap_bgr is None or minimap_bgr.size == 0: return None
    try:
        h, w = minimap_bgr.shape[:2]
        center_x, center_y = w // 2, h // 2 
        
        # 1. 꼬리 뒤로 길게 붙는 경로선 억까를 배제하기 위해 28x28 구역으로 타이트하게 자릅니다.
        roi_size = 14
        x1, y1 = max(0, center_x - roi_size), max(0, center_y - roi_size)
        x2, y2 = min(w, center_x + roi_size), min(h, center_y + roi_size)
        
        roi = minimap_bgr[y1:y2, x1:x2]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # 2. 순수 빨간색 추출 (리니지 맵 화살표 색상)
        mask1 = cv2.inRange(hsv, (0, 140, 140), (10, 255, 255))
        mask2 = cv2.inRange(hsv, (170, 140, 140), (180, 255, 255))
        mask_red = cv2.bitwise_or(mask1, mask2)
        
        # 🚨 [형님 적발: 치명적 버그 수술] 화살표를 지워버리던 MORPH_OPEN 필터 완전 삭제!
        # 대신, 면적/길이 조건으로만 쓰레기 픽셀을 스마트하게 걸러냅니다.
        
        # 3. 덩어리(윤곽선) 추출
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not contours: return None
        
        roi_cx, roi_cy = (x2 - x1) / 2.0, (y2 - y1) / 2.0
        best_contour = None
        min_dist = float('inf')
        
        for cnt in contours:
            if len(cnt) < 4: continue # 1~3픽셀짜리 흩날린 노이즈 점은 쿨하게 무시
            
            M = cv2.moments(cnt)
            if M["m00"] > 0:
                cx = M["m10"] / M["m00"]
                cy = M["m01"] / M["m00"]
            else:
                bx, by, bw, bh = cv2.boundingRect(cnt)
                cx = bx + bw / 2.0
                cy = by + bh / 2.0
                
            dist = (cx - roi_cx)**2 + (cy - roi_cy)**2
            if dist < min_dist:
                min_dist = dist
                best_contour = cnt
                
        if best_contour is None: return None
        
        # 👑 [핵심 수술 2] 깨끗한 도화지에 내 캐릭터 화살표 하나만 그리기!
        # 이렇게 하면 미니맵의 다른 빨간색(경로선, 유저)이 테두리 검사를 절대 방해하지 못합니다.
        clean_mask = np.zeros_like(mask_red)
        cv2.drawContours(clean_mask, [best_contour], -1, 255, -1)
        
        # 4. 껍질(Convex Hull)을 구하고 픽셀 목록 추출
        hull = cv2.convexHull(best_contour)
        pts = [p[0] for p in hull]
        n = len(pts)
        if n < 3: return None
        
        # 5. 형님의 V6 핵심: 세 꼭지점(가장 큰 삼각형) 찾기!
        max_area = -1
        best_tri = None
        
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    # 신발끈 공식으로 삼각형 넓이 구하기
                    area = abs(pts[i][0]*(pts[j][1] - pts[k][1]) + pts[j][0]*(pts[k][1] - pts[i][1]) + pts[k][0]*(pts[i][1] - pts[j][1]))
                    if area > max_area:
                        max_area = area
                        best_tri = (pts[i], pts[j], pts[k])
                        
        if not best_tri: return None
        A, B, C = best_tri
        
        # 6. 👑 [V6 엔진 복구] 선분의 '가운데 60%' 구간만 픽셀 검사! 
        def get_edge_score(p1, p2):
            dist = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
            steps = max(int(dist), 1)
            
            # 양 끝단 20%씩은 꼭지점(빨간색 몸통) 근처이므로 제외하고, 순수하게 파인 중간 허공만 예리하게 검사!
            start_step = int(steps * 0.2)
            end_step = int(steps * 0.8)
            
            red_cnt = 0
            total_checked = 0
            
            for i in range(start_step, end_step + 1):
                t = i / float(steps) if steps > 0 else 0
                px = int(round(p1[0] + (p2[0] - p1[0]) * t))
                py = int(round(p1[1] + (p2[1] - p1[1]) * t))
                
                if 0 <= py < clean_mask.shape[0] and 0 <= px < clean_mask.shape[1]:
                    # 💡 원본이 아닌 '100% 격리된 화살표 마스크'에서만 검사합니다!
                    if clean_mask[py, px] > 0:
                        red_cnt += 1
                total_checked += 1
                
            return red_cnt / float(total_checked) if total_checked > 0 else 0

        # 세 선분(AB, BC, CA)의 빨간 픽셀 통과 비율 검사
        scores = [
            (get_edge_score(A, B), (A, B), C),
            (get_edge_score(B, C), (B, C), A),
            (get_edge_score(C, A), (C, A), B)
        ]
        
        # 7. 빨간색 픽셀 점수가 가장 낮은(회색 허공을 지나가는) 선분이 무조건 두 꼬리를 이은 선!
        scores.sort(key=lambda x: x[0])
        
        tail_edge = scores[0][1] # 텅 빈 공간을 지나가는 선분 (꼬리 1, 꼬리 2)
        tip = scores[0][2]       # 그 반대편에 있는 100% 팩트 앞촉!
        
        # 8. 꼬리 선분의 정중앙점 계산
        mid_x = (tail_edge[0][0] + tail_edge[1][0]) / 2.0
        mid_y = (tail_edge[0][1] + tail_edge[1][1]) / 2.0
        
        # 9. 꼬리 중앙에서 앞촉을 향하는 라디안 각도 도출!
        vec_x = tip[0] - mid_x
        vec_y = tip[1] - mid_y
        
        if vec_x == 0 and vec_y == 0: return None
        raw_angle = math.atan2(vec_y, vec_x)
        
        # 👑 [핵심 수술 3] 리니지 전용 8방향(45도) 자석 스냅(Snap) 보정!
        # 픽셀 뭉개짐으로 인해 각도가 83도나 95도 등으로 삐딱하게 나오더라도 
        # 가장 가까운 정방향(45도 단위)으로 무조건 교정합니다!
        sector_size = math.pi / 4.0  
        snapped_angle = round(raw_angle / sector_size) * sector_size
        
        return snapped_angle
        
    except Exception:
        return None

# 📐 [형님의 타일 그리드(U, V) 쌍방향 번역 코어 엔진]
# 화면 픽셀 <-> 미니맵 좌표 <-> 서버 타일(U, V) 간의 완벽한 변환을 수행합니다!
# =====================================================================
def get_uv_from_map_pixel(map_x, map_y, anchor_x, anchor_y):
    """글로벌 맵 픽셀을 서버 타일 좌표(U,V)로 변환"""
    if anchor_x == -1000: return 0, 0
    dx = map_x - anchor_x
    dy = map_y - anchor_y
    u = int(round((dx + 2.0 * dy) / 5.0))
    v = int(round((-dx + 2.0 * dy) / 5.0))
    return u, v

def get_map_pixel_from_uv(u, v, anchor_x, anchor_y):
    """서버 타일 좌표(U,V)의 정중앙 수학적 맵 픽셀 도출"""
    px = anchor_x + (u * 5 - v * 5) // 2
    py = anchor_y + (u * 5 + v * 5) // 4
    return px, py

def check_line_of_sight(map_gray, start_point, end_point, margin_steps=3):
    
    if map_gray is None: return True
    
    # 정수로 내림하지 않고 소수점 정밀도를 유지하여 계산
    x0, y0 = float(start_point[0]), float(start_point[1])
    x1, y1 = float(end_point[0]), float(end_point[1])
    
    h, w = map_gray.shape[:2]
    
    # 두 점 사이의 실제 유클리드 픽셀 거리 계산
    dist = math.hypot(x1 - x0, y1 - y0)
    
    # 🚀 거리가 2.0 픽셀 이하일 때만 통과 (내 캐릭터 발밑의 자가 충돌 방지용)
    # 💡 1셀은 약 3.5~5픽셀이므로 2.0픽셀 마진은 1셀 밖의 몹/벽을 절대 건너뛰지 않습니다!
    if dist <= margin_steps * 2.0:
        return True
        
    # 🚀 형님 오더 반영: 1.5픽셀 꼼수 폐기! 무조건 1픽셀당 1번씩 촘촘하게 전수 검사 복구!
    steps = max(1, int(dist)) 
    dx = (x1 - x0) / steps
    dy = (y1 - y0) / steps
    
    has_entered_open_space = False # 밝은 길로 한 번이라도 나왔는가?
    
    for i in range(1, steps):
        cx = x0 + dx * i
        cy = y0 + dy * i
        ix, iy = int(round(cx)), int(round(cy))
        
        is_wall = False
        if 0 <= ix < w and 0 <= iy < h:
            val = map_gray[iy, ix]
            if isinstance(val, (list, tuple)) or hasattr(val, 'shape'):
                val = val[0]
            if val < 50: # 50 미만 어두운 픽셀은 벽으로 간주
                is_wall = True
                
        # 🚀 대각선 모서리 틈새 누수 차단 (레이저에 두께를 부여하여 통과 방지)
        if not is_wall:
            dx_frac = cx - ix
            dy_frac = cy - iy
            
            if abs(dx_frac) > 0.35:
                ax = ix + (1 if dx_frac > 0 else -1)
                if 0 <= ax < w:
                    val = map_gray[iy, ax]
                    if isinstance(val, (list, tuple)) or hasattr(val, 'shape'): val = val[0]
                    if val < 50: is_wall = True
                    
            if not is_wall and abs(dy_frac) > 0.35:
                ay = iy + (1 if dy_frac > 0 else -1)
                if 0 <= ay < h:
                    val = map_gray[ay, ix]
                    if isinstance(val, (list, tuple)) or hasattr(val, 'shape'): val = val[0]
                    if val < 50: is_wall = True

        # 🚀 맹목적 건너뛰기 방지 + 상태 추적형 마진 적용 (똑똑한 마진)
        if is_wall:
            dist_from_start = math.hypot(cx - x0, cy - y0)
            dist_from_end = math.hypot(x1 - cx, y1 - cy)
            
            if not has_entered_open_space:
                # 시작점 오차 구간(마진)을 못 벗어났는데 벽이면 갇힌 것으로 판별
                if dist_from_start > margin_steps:
                    return False 
            else:
                # 길로 한 번이라도 나왔는데 도착지 한참 전에 벽을 만남 -> 명백한 시야 차단!
                if dist_from_end > margin_steps:
                    return False 
        else:
            has_entered_open_space = True # 한 번이라도 밝은 길을 밟았음을 기록
            
    return True

def check_item_line_of_sight(map_gray, start_point, end_point, threshold=3):
    """🚀 아이템 전용 시야 검사: 경로 상에 어두운(벽) 픽셀이 누적 3개 이상이면 막힌 것으로 간주"""
    if map_gray is None: return True
    
    x0, y0 = float(start_point[0]), float(start_point[1])
    x1, y1 = float(end_point[0]), float(end_point[1])
    
    h, w = map_gray.shape[:2]
    dist = math.hypot(x1 - x0, y1 - y0)
    
    if dist <= 2.0:
        return True
        
    steps = max(1, int(dist)) 
    dx = (x1 - x0) / steps
    dy = (y1 - y0) / steps
    
    black_count = 0
    
    for i in range(1, steps):
        cx = x0 + dx * i
        cy = y0 + dy * i
        ix, iy = int(round(cx)), int(round(cy))
        
        if 0 <= ix < w and 0 <= iy < h:
            val = map_gray[iy, ix]
            if isinstance(val, (list, tuple)) or hasattr(val, 'shape'):
                val = val[0]
                
            if val < 50: # 어두운 픽셀(벽) 발견
                black_count += 1
                if black_count >= threshold: # 💡 누적 3개 이상이면 시야 차단(벽 너머) 확정!
                    return False
                    
    return True

def get_clear_distance(map_gray, start_point, angle, max_dist_screen):
    cx, cy = start_point
    h, w = map_gray.shape[:2]
    step = 5 
    max_steps = int(max_dist_screen / step)
    
    for i in range(1, max_steps + 1):
        dist_screen = i * step
        ix = int(cx + math.cos(angle) * dist_screen * DUNGEON_SCALE_X)
        iy = int(cy + math.sin(angle) * dist_screen * DUNGEON_SCALE_X) 
        
        if not (0 <= ix < w and 0 <= iy < h): 
            return max(0, dist_screen - step) 
            
        val = map_gray[iy, ix]
        if isinstance(val, (list, tuple)) or hasattr(val, 'shape'): val = val[0]
            
        if val < 80: # 🚀 50 -> 80 상향
            if dist_screen > 15: return dist_screen - step
    return max_dist_screen

# ==========================================
# 🗺️ [네비게이션 코어] 초고속 A* 장기 경로 엔진
# ==========================================
def find_farthest_empty_target(map_gray, start_pos, min_dist=100, step=3):
    if map_gray is None: return None
    h, w = map_gray.shape[:2]
    best_target, max_dist = None, 0
    for _ in range(100): 
        rx = (random.randint(10, w - 10) // step) * step
        ry = (random.randint(10, h - 10) // step) * step
        
        if 0 <= rx < w and 0 <= ry < h:
            val = map_gray[ry, rx]
            if isinstance(val, (list, tuple)) or hasattr(val, 'shape'): val = val[0]
            if val >= 80: # 🚀 50 -> 80 상향 (어두운 벽을 목표로 잡는 현상 차단)
                dist = math.hypot(rx - start_pos[0], ry - start_pos[1])
                if dist > max_dist and dist > min_dist:
                    max_dist = dist; best_target = (rx, ry)
    return best_target

def calculate_astar_path(map_gray, start, goal, step=3):
    """벽 몹 추적 시 사용하는 150x150 국지적 정밀 픽셀 A* 함수 (연산 부하 극소)"""
    if map_gray is None: return []
    h, w = map_gray.shape[:2]
    start_grid = (int(start[0]) // step, int(start[1]) // step)
    goal_grid = (int(goal[0]) // step, int(goal[1]) // step)
    
    # 🚀 [핵심 수술] 시작점 무적 통과(유령 모드) 완전 삭제! 첫 발자국부터 철저하게 벽 검사
    def is_valid_step(cx, cy, nx, ny, g_val_curr=0):
        dx, dy = nx - cx, ny - cy
        # 🚀 [형님 오더 복구] 중간/끝 꼼수 완전 폐기! 1픽셀 단위로 정직하게 전수 검사합니다!
        for i in range(1, step + 1):
            px = int(cx * step + dx * i)
            py = int(cy * step + dy * i)
            
            if not (0 <= px < w and 0 <= py < h): return False
            val = map_gray[py, px]
            if isinstance(val, (list, tuple)) or hasattr(val, 'shape'): val = val[0]
            
            if val < 80: return False 
        return True

    gx_px, gy_py = goal_grid[0] * step, goal_grid[1] * step
    if not (0 <= gx_px < w and 0 <= gy_py < h): return []
    
    open_set = []
    heapq.heappush(open_set, (0, start_grid))
    came_from = {}; g_score = {start_grid: 0}
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    loop_cnt = 0
    while open_set and loop_cnt < 10000:
        loop_cnt += 1
        _, current = heapq.heappop(open_set)
        
        if current == goal_grid:
            path = []
            while current in came_from:
                path.append((current[0] * step, current[1] * step))
                current = came_from[current]
            path.reverse()
            return path
            
        for dx, dy in dirs:
            nxt = (current[0] + dx, current[1] + dy)
            cost = 1.414 if dx != 0 and dy != 0 else 1.0
            tentative_g = g_score[current] + cost
            
            if not is_valid_step(current[0], current[1], nxt[0], nxt[1], g_val_curr=g_score[current]): continue
            
            if nxt not in g_score or tentative_g < g_score[nxt]:
                came_from[nxt] = current; g_score[nxt] = tentative_g
                f_score = tentative_g + math.hypot(goal_grid[0] - nxt[0], goal_grid[1] - nxt[1])
                heapq.heappush(open_set, (f_score, nxt))
    return []

def calculate_local_astar_path_for_loot(map_gray, start, goal, step=3, max_radius=40.0, max_nodes=10):
    """🚀 [수정] 아이템 전용! 템이 까만 픽셀에 떨어져도 가장 가까운 평지로 당겨와서 길을 찾는 스마트 A*"""
    if map_gray is None: return []
    h, w = map_gray.shape[:2]
    
    if math.hypot(goal[0] - start[0], goal[1] - start[1]) > max_radius:
        return []

    start_grid = (int(start[0]) // step, int(start[1]) // step)
    goal_grid = (int(goal[0]) // step, int(goal[1]) // step)
    
    # =================================================================
    # 👑 [형님 오더 수술] 템이 까만 픽셀(벽)에 떨어졌을 경우 억까 실패 방지 엔진!
    # =================================================================
    gx_px, gy_py = goal_grid[0] * step, goal_grid[1] * step
    if not (0 <= gx_px < w and 0 <= gy_py < h): return []
    
    val = map_gray[gy_py, gx_px]
    if isinstance(val, (list, tuple)) or hasattr(val, 'shape'): val = val[0]
    
    # 💡 템이 떨어진 곳이 어두운 픽셀(80 미만)이라면?
    if val < 80:
        found_safe_spot = False
        # 반경 1~3 그리드(약 3~9픽셀) 내에서 가장 가까운 밝은 땅을 찾아서 목적지를 변경!
        for r in range(1, 4):
            for dx in range(-r, r+1):
                for dy in range(-r, r+1):
                    if dx == 0 and dy == 0: continue
                    nx_px, ny_py = (goal_grid[0] + dx) * step, (goal_grid[1] + dy) * step
                    if 0 <= nx_px < w and 0 <= ny_py < h:
                        n_val = map_gray[ny_py, nx_px]
                        if isinstance(n_val, (list, tuple)) or hasattr(n_val, 'shape'): n_val = n_val[0]
                        if n_val >= 80:
                            goal_grid = (goal_grid[0] + dx, goal_grid[1] + dy)
                            found_safe_spot = True
                            break
                if found_safe_spot: break
            if found_safe_spot: break
            
        # 💡 주변 9픽셀을 다 뒤져도 땅이 없으면 그건 진짜 생벽 안에 떨어진 템이므로 포기!
        if not found_safe_spot: return []
    # =================================================================
    
    def is_valid_step(cx, cy, nx, ny):
        dx, dy = nx - cx, ny - cy
        for i in range(1, step + 1):
            px = int(cx * step + dx * i)
            py = int(cy * step + dy * i)
            if not (0 <= px < w and 0 <= py < h): return False
            val = map_gray[py, px]
            if isinstance(val, (list, tuple)) or hasattr(val, 'shape'): val = val[0]
            if val < 80: return False 
        return True

    # 이하 A* 연산 부분은 기존과 100% 동일
    open_set = []
    heapq.heappush(open_set, (0, start_grid))
    came_from = {}
    g_score = {start_grid: 0}
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    loop_cnt = 0
    while open_set and loop_cnt < 500: 
        loop_cnt += 1
        _, current = heapq.heappop(open_set)
        
        if g_score[current] > max_nodes * 1.415: 
            return []
            
        if current == goal_grid:
            path = []
            while current in came_from:
                path.append((current[0] * step, current[1] * step))
                current = came_from[current]
            path.reverse()
            if len(path) > max_nodes: return []
            return path
            
        for dx, dy in dirs:
            nxt = (current[0] + dx, current[1] + dy)
            cost = 1.414 if dx != 0 and dy != 0 else 1.0
            tentative_g = g_score[current] + cost
            
            if not is_valid_step(current[0], current[1], nxt[0], nxt[1]): continue
            
            if nxt not in g_score or tentative_g < g_score[nxt]:
                came_from[nxt] = current; g_score[nxt] = tentative_g
                f_score = tentative_g + math.hypot(goal_grid[0] - nxt[0], goal_grid[1] - nxt[1])
                heapq.heappush(open_set, (f_score, nxt))
    return []
# 🚀 [새 기능 추가] 연산 0%, 초고속 가중치 난수화 노선도 A* 함수
def find_nearest_visible_node(graph, pos, map_gray):
    if not graph or not graph.get("nodes"): return None
    best_node = None
    min_d = float('inf')
    
    # 🚀 [방탄 조끼 1] 좌표가 딕셔너리/튜플/리스트 무엇이든 완벽하게 파싱 (KeyError 파괴!)
    px = pos.get("x", 0) if isinstance(pos, dict) else pos[0]
    py = pos.get("y", 0) if isinstance(pos, dict) else pos[1]
    
    # 1차: 시야에 보이는 노드 중 가장 가까운 것 (반경 150픽셀 이내 제한)
    for nid, npos in graph["nodes"].items():
        nx = npos.get("x", 0) if isinstance(npos, dict) else npos[0]
        ny = npos.get("y", 0) if isinstance(npos, dict) else npos[1]
        
        d = (nx - px)**2 + (ny - py)**2
        if d < 150*150 and d < min_d:
            if check_line_of_sight(map_gray, (px, py), (nx, ny), margin_steps=2):
                min_d = d
                best_node = nid
                
    # 2차: 시야에 안 보이면 (예: 벽에 비벼졌을 때) 그냥 무조건 가장 가까운 노드 강제 선택
    if best_node is None:
        min_d = float('inf')
        for nid, npos in graph["nodes"].items():
            nx = npos.get("x", 0) if isinstance(npos, dict) else npos[0]
            ny = npos.get("y", 0) if isinstance(npos, dict) else npos[1]
            
            d = (nx - px)**2 + (ny - py)**2
            if d < min_d:
                min_d = d
                best_node = nid
    return best_node

# 🚀 [형님 기획 완벽 적용] 맵 그림(map_gray)을 버리고 차단된 노드 명단(blocked_nodes)을 받습니다!
def calculate_graph_astar_path(graph, start_pos, goal_node_id, map_gray, blocked_nodes=None):
    if not graph or not graph.get("nodes"): return []
    if blocked_nodes is None: blocked_nodes = set()
    
    start_node = find_nearest_visible_node(graph, start_pos, map_gray)
    if start_node is None: return []

    # 🚀 [방탄 수술 1] JSON 키값은 무조건 문자열(str)이므로 모든 노드 ID를 문자열로 통일합니다!
    goal_node_str = str(goal_node_id)
    start_node_str = str(start_node)
    blocked_nodes_str = {str(b) for b in blocked_nodes}

    open_set = []
    heapq.heappush(open_set, (0, start_node_str))
    came_from = {}
    g_score = {start_node_str: 0}
    
    # 맵 데이터도 안전하게 문자열로 캐스팅
    nodes = {str(k): v for k, v in graph["nodes"].items()}
    edges = {str(k): [str(n) for n in v] for k, v in graph.get("edges", {}).items()}
    
    if goal_node_str not in nodes: return []
    
    goal_n = nodes[goal_node_str]
    gx = goal_n.get("x", 0) if isinstance(goal_n, dict) else goal_n[0]
    gy = goal_n.get("y", 0) if isinstance(goal_n, dict) else goal_n[1]

    loop_cnt = 0
    while open_set and loop_cnt < 15000:
        loop_cnt += 1
        _, current = heapq.heappop(open_set)
        
        if current == goal_node_str:
            path = []
            while current in came_from:
                cn = nodes[current]
                path.append((cn.get("x", 0), cn.get("y", 0)) if isinstance(cn, dict) else (cn[0], cn[1]))
                current = came_from[current]
            sn = nodes[start_node_str]
            path.append((sn.get("x", 0), sn.get("y", 0)) if isinstance(sn, dict) else (sn[0], sn[1]))
            path.reverse()
            return path
            
        for nxt in edges.get(current, []):
            if nxt not in nodes: continue 
            
            # =================================================================
            # 🚨 [형님 마스터피스: 순수 노드 통제 엔진] 
            # 잉여 픽셀 검사 나발이고, 다음 정거장(nxt)이 '유저/몹이 점거한 차단 명단(blocked_nodes)'에 있으면?
            # 0.0001초 만에 무시하고 알아서 다른 뚫린 인접 노드로 우회합니다! (속도 10,000배 향상)
            # =================================================================
            if nxt in blocked_nodes_str and nxt != goal_node_str:
                continue 
            
            cn = nodes[current]
            cx = cn.get("x", 0) if isinstance(cn, dict) else cn[0]
            cy = cn.get("y", 0) if isinstance(cn, dict) else cn[1]
            
            nn = nodes[nxt]
            nx = nn.get("x", 0) if isinstance(nn, dict) else nn[0]
            ny = nn.get("y", 0) if isinstance(nn, dict) else nn[1]
            
            dist = math.hypot(nx - cx, ny - cy)
            
            # 🚀 [방탄 수술 2] TypeError 폭사 방지! 노드 번호가 문자열이라서 에러가 나는 현상 차단
            try:
                c_val = int(current)
                n_val = int(nxt)
            except:
                c_val = sum(ord(c) for c in current)
                n_val = sum(ord(c) for c in nxt)
                
            pseudo_noise = 1.0 + ((c_val + n_val) % 10) * 0.01 
            cost = dist * pseudo_noise
            
            tentative_g = g_score.get(current, 0) + cost
            if nxt not in g_score or tentative_g < g_score[nxt]:
                came_from[nxt] = current
                g_score[nxt] = tentative_g
                f_score = tentative_g + math.hypot(gx - nx, gy - ny)
                heapq.heappush(open_set, (f_score, nxt))
    return []

# ==========================================
# 🛡️ [보안 AI 파훼 코어] 통계적 난수 및 고급 피로도 유틸
# ==========================================
MACRO_GLOBAL_START_TIME = time.time()

def apply_human_variance(ideal_time):
    """수학적으로 100% 똑같이 계산된 궤적 시간에 인체 고유의 가우시안 오차(85%~115%)를 섞어 반환"""
    human_variance = random.gauss(1.0, 0.07)
    return ideal_time * max(0.85, min(1.15, human_variance))

def g_val(min_val, max_val):
    if min_val >= max_val: return min_val
    mu = (min_val + max_val) / 2.0
    sigma = (max_val - min_val) / 6.0
    return max(min_val, min(max_val, random.gauss(mu, sigma)))

def g_time(min_val, max_val, key=None):
    if min_val >= max_val: return min_val
    fatigue = 1.0
    is_panic = False
    if key and key in ai_states:
        st = ai_states[key]
        curr_time = time.time()
        last_check = st.get("last_g_time_call", curr_time)
        if st.get("is_hunt_active", False) and active_manual_target != key:
            st["accum_hunt_time"] = st.get("accum_hunt_time", 0.0) + (curr_time - last_check)
        st["last_g_time_call"] = curr_time
        accum_time = st.get("accum_hunt_time", 0.0)
        
        target_time = st.get("next_fatigue_target", 0)
        if target_time == 0: 
            target_time = g_val(1500, 4200)
            st["next_fatigue_target"] = target_time
            
        if accum_time > target_time:
            fatigue_chance = g_val(0.3, 0.7) 
            if random.random() < fatigue_chance:
                degradation = g_val(0.007, 0.020)
                st["fatigue_mult"] = min(1.21, st.get("fatigue_mult", 1.0) + degradation)
                dprint(key, f"💤 [인간화] 피로도 미세 누적됨 (현재: x{st['fatigue_mult']:.3f})")
            else:
                recovery = g_val(0.005, 0.010)
                st["fatigue_mult"] = max(0.95, st.get("fatigue_mult", 1.0) - recovery)
                dprint(key, f"☕ [인간화] 집중력 폭발! 텐션UP (현재: x{st['fatigue_mult']:.3f})")
            
            # 👇👇👇 [형님 오더 완벽 적용: 1.150 이상 시 자동 리셋!] 👇👇👇
            if st["fatigue_mult"] >= 1.150:
                dprint(key, f"🛌 [피로도 자동 리셋] 한계치(1.150) 도달! 푹 자고 일어나 컨디션을 1.0으로 회복합니다!")
                st["fatigue_mult"] = 1.0
                st["accum_hunt_time"] = 0.0
                accum_time = 0.0 # 현재 루프 변수도 초기화하여 맑은 정신으로 시작

            st["next_fatigue_target"] = accum_time + g_val(1500, 4200)
        
        fatigue = st.get("fatigue_mult", 1.0)
        is_panic = st.get("is_panic", False)
        
    if is_panic:
        mu = ((min_val + max_val) / 2.0) * 0.85
        sigma = (max_val - min_val) / 2.0 
    else:
        mu = ((min_val + max_val) / 2.0) * fatigue
        sigma = (max_val - min_val) / 6.0
        
    val = random.gauss(mu, sigma)
    final_val = max(min_val * 0.5 if is_panic else min_val * 0.8, val)
    
# 🟢 [수정 후 코드] (하한선을 50ms로 올리고 가우시안 처리)
    if min_val >= 0.05 and final_val < 0.05:
        final_val = max(0.050, random.gauss(0.055, 0.005))
        
    return final_val

def get_dynamic_cooldown(min_val, max_val, key):
    # 🚀 [멍때림 족쇄 완전 소각] 확률적 휴식 로직 삭제! 칼같이 기본 쿨타임만 계산해서 즉시 리턴합니다.
    curr = time.time()
    return curr + g_time(min_val, max_val, key)

# ==========================================
# 0. 디버그 뷰어 플래그 및 콘솔 출력 함수
# ==========================================
DEBUG_MODE = True

def dprint(key, msg):
    # 🚀 [맹인 벙어리 수술 완료] "미니1" 하드코딩 삭제! 1/2/3호기 모두 정상적으로 로그를 출력합니다!
    if DEBUG_MODE:
        t = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{t}] [{key}] {msg}")

# =================================================================
# 🚀 [궁극체] 피코 H/W 역송신(Hardware Echo) 절대 진실 로거 엔진
# =================================================================
logger_states = {}

# 기존 파이썬 뇌피셜 로거의 찌꺼기 호출을 무시하는 스텔스 함수
def log_intercept(*args, **kwargs):
    pass 

# 🚀 미니4 큐 추가!
debug_queues = {"미니1": queue.Queue(maxsize=2), "미니2": queue.Queue(maxsize=2), "미니3": queue.Queue(maxsize=2), "미니4": queue.Queue(maxsize=2)}
debug_windows_moved = False
raycast_debug_queues = {"미니1": queue.Queue(maxsize=2), "미니2": queue.Queue(maxsize=2), "미니3": queue.Queue(maxsize=2), "미니4": queue.Queue(maxsize=2)}
raycast_windows_moved = False

try: ctypes.windll.shcore.SetProcessDpiAwareness(2)
except: pass

winmm = None
try:
    winmm = ctypes.windll.winmm
    winmm.timeBeginPeriod(1) 
except: pass

KEY_F1, KEY_F2, KEY_F3, KEY_F4 = 194, 195, 196, 197
KEY_F5, KEY_F6, KEY_F7, KEY_F8 = 198, 199, 200, 201  
KEY_F9, KEY_F10, KEY_F11, KEY_F12 = 202, 203, 204, 205 
KEY_ESCAPE   = KEY_F8
KEY_ANTIDOTE = KEY_F10
KEY_HEAL     = KEY_F6
KEY_POTION   = KEY_F5
HP_Y_START, HP_Y_END = 485, 495
HP_X1, HP_X2 = 175, 350
MP_X1, MP_X2 = 416, 585
DRAGON_ROI_X1, DRAGON_ROI_X2 = 350, 416
DRAGON_ROI_Y1, DRAGON_ROI_Y2 = 460, 510

BUFF_DUR_SHIELD   = 1200 
BUFF_DUR_HOLY     = 1200 
BUFF_DUR_ENCHANT  = 1800 
BUFF_DUR_BLESSED  = 1800
BUFF_DUR_DEX      = 1200
BUFF_DUR_DECREASE = 1800
BUFF_DUR_TRANS    = 1200
BUFF_DUR_LIGHT    = 7200

# =================================================================
# 🚀 [런처 영구 소각] 4개의 미니컴을 1개의 창에서 완벽히 통제하므로,
# 개별 호기를 묻는 불필요한 런처를 날리고 세팅 파일을 하나로 통합합니다!
# =================================================================
BUFF_SAVE_FILE = "buff_times_cc.json"
SETTINGS_SAVE_FILE = "settings_cc.json"
file_io_lock = threading.Lock()

def load_buff_times():
    if os.path.exists(BUFF_SAVE_FILE):
        try:
            with open(BUFF_SAVE_FILE, "r") as f: return json.load(f)
        except: pass
    return {}

def save_buff_times(states_dict):
    with file_io_lock: return _save_buff_times_internal(states_dict)

def _save_buff_times_internal(states_dict): # 💡 들여쓰기 보호 마법
    try:
        data = {}
        curr_t = time.time() # 🚀 현재 시간을 가져옵니다.
        for k, st in states_dict.items():
            data[k] = {
                # 🚀 [형님 수술] 목표 시간에서 현재 시간을 빼서 '순수하게 남은 시간(초)'만 냉동 보관! (만료됐으면 0초 저장)
                "trans": max(0.0, st.get("buff_trans_time", 0) - curr_t),
                "shield": max(0.0, st.get("buff_shield_time", 0) - curr_t),
                "holy": max(0.0, st.get("buff_holy_time", 0) - curr_t),
                "enchant": max(0.0, st.get("buff_enchant_time", 0) - curr_t),
                "blessed": max(0.0, st.get("buff_blessed_time", 0) - curr_t),
                "dex": max(0.0, st.get("buff_dex_time", 0) - curr_t),
                "decrease": max(0.0, st.get("buff_decrease_time", 0) - curr_t),
                "extra_f10": max(0.0, st.get("buff_extra_f10_time", 0) - curr_t),
                "light": max(0.0, st.get("buff_light_time", 0) - curr_t),
                "blue_pot": max(0.0, st.get("buff_blue_pot_time", 0) - curr_t) # 👈 파랭이 남은 시간 저장 추가
            }
        with open(BUFF_SAVE_FILE, "w") as f: json.dump(data, f)
    except: pass

def load_settings():
    if os.path.exists(SETTINGS_SAVE_FILE):
        try:
            with open(SETTINGS_SAVE_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {}

def save_settings():
    with file_io_lock: return _save_settings_internal()

def _save_settings_internal():
    try:
        import win32gui
        data = {}
        for k, v in gui_vars.items():
            st = ai_states.get(k, {}) 
            
            # 🚀 [추가] 현재 떠 있는 디버그 창의 실제 좌표를 윈도우에서 훔쳐옵니다!
            dbg_x, dbg_y = -1, -1
            try:
                hwnd = win32gui.FindWindow(None, f"Debug_View_PC_{k[-1]}")
                if hwnd:
                    rect = win32gui.GetWindowRect(hwnd)
                    dbg_x, dbg_y = rect[0], rect[1]
            except: pass
            
            # 💡 창이 꺼져있거나 최소화 상태일 땐 기존 저장값을 유지합니다.
            if dbg_x == -1 or dbg_y == -1:
                dbg_x = saved_settings.get(k, {}).get("dbg_x", -1)
                dbg_y = saved_settings.get(k, {}).get("dbg_y", -1)

            # 파이썬 뇌에도 저장값 즉시 동기화
            if k not in saved_settings: saved_settings[k] = {}
            saved_settings[k]["dbg_x"] = dbg_x
            saved_settings[k]["dbg_y"] = dbg_y

            data[k] = {
                "com_port": v.get("com_port").get().strip() if "com_port" in v else "", 
                "pico_hwid": st.get("pico_hwid", ""),
                "use_blue_pot": v.get("use_blue_pot").get() if "use_blue_pot" in v else False,
                "blue_deficit": float(v.get("blue_deficit").get()) if "blue_deficit" in v else 11.0, # 🚀 파랭이 결손치 값 저장
                
                "use_dir_lock": v.get("use_dir_lock").get() if "use_dir_lock" in v else False,
                "lock_dir": v.get("lock_dir").get() if "lock_dir" in v else "9시",

                # 👇👇👇 [신규 추가] 여기에 복사해서 넣으세요! 👇👇👇
                "recall_item1": v.get("recall_item1").get() if "recall_item1" in v else "없음",
                "recall_item2": v.get("recall_item2").get() if "recall_item2" in v else "없음",
                "recall_item3": v.get("recall_item3").get() if "recall_item3" in v else "없음",
                
                "win_x": v.get("win_x").get() if "win_x" in v else "0",
                "win_y": v.get("win_y").get() if "win_y" in v else "0",
                "shop_item": v.get("shop_item").get() if "shop_item" in v else "yongi",
                "shop_qty": v.get("shop_qty").get() if "shop_qty" in v else "5000",
                "shop_price": v.get("shop_price").get() if "shop_price" in v else "700",
                "shop_info": v.get("shop_info").get() if "shop_info" in v else "dyddl 700",
                "auth_main_id": v.get("auth_main_id").get().strip() if "auth_main_id" in v else "",
                "auth_main_pw": v.get("auth_main_pw").get().strip() if "auth_main_pw" in v else "",
                "auth_main_email": v.get("auth_main_email").get().strip() if "auth_main_email" in v else "",
                "auth_main_phone": v.get("auth_main_phone").get().strip() if "auth_main_phone" in v else "",
                "auth_delay_use": v.get("auth_delay_use").get() if "auth_delay_use" in v else False,
                "auth_auto_captcha": v.get("auth_auto_captcha").get() if "auth_auto_captcha" in v else False,
                "auth_delay_start_min": v.get("auth_delay_start_min").get().strip() if "auth_delay_start_min" in v else "55",
                "auth_delay_end_min": v.get("auth_delay_end_min").get().strip() if "auth_delay_end_min" in v else "58",
                "auth_delay_sec": v.get("auth_delay_sec").get().strip() if "auth_delay_sec" in v else "180",
                "certi_curr_central": st.get("certi_curr_central", saved_settings.get(k, {}).get("certi_curr_central", "")),
                "dbg_x": dbg_x, # 👈 디버그 창 X
                "dbg_y": dbg_y  # 👈 디버그 창 Y
            }

        data["GLOBAL"] = {
            "base_x": globals()['entry_base_x'].get() if 'entry_base_x' in globals() else 350, 
            "base_y": globals()['entry_base_y'].get() if 'entry_base_y' in globals() else 1300, 
            "gui_x": entry_gui_x.get() if 'entry_gui_x' in globals() else 0, 
            "gui_y": entry_gui_y.get() if 'entry_gui_y' in globals() else 0,
            "debug_mode": DEBUG_MODE,  
            "frame_delay": GLOBAL_FRAME_DELAY
        }
        with open(SETTINGS_SAVE_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception: 
        pass

safe_gui_x = -1
safe_gui_y = -1

ARROW_ROI_X1, ARROW_ROI_X2 = 755, 795
ARROW_ROI_Y1, ARROW_ROI_Y2 = 540, 565
ARROW_STOP_TIMEOUT = 1.8

# =====================================================================
# 🏹 [신규 센서] 은화살 오링(증발) 절대 감지기
# 기존 ARROW_ROI(숫자 구역) 바로 위쪽인 순수 '아이콘' 영역만을 정밀 스캔합니다!
# =====================================================================
ARROW_ICON_X1, ARROW_ICON_X2 = 765, 785  # 좌우 여백 확보 (테두리 피함)
ARROW_ICON_Y1, ARROW_ICON_Y2 = 526, 538  # 하단 F12 글씨 완벽 회피

def check_arrow_empty(img_bgr):
    """F12 슬롯 상단의 아이콘 영역이 완전히 비었는지 확인"""
    if img_bgr is None: return False
    try:
        roi = img_bgr[ARROW_ICON_Y1:ARROW_ICON_Y2, ARROW_ICON_X1:ARROW_ICON_X2]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # 🚀 [수술 1단계] 밝기 커트라인 대폭 하향 (190 -> 100)
        # 은화살은 순백색이 아니라 회색/은색 톤이 섞여 있어 190을 넘지 못합니다!
        # 빈 슬롯의 칙칙한 돌바닥은 기껏해야 밝기가 30~45 수준이므로 100이면 완벽히 구분됩니다.
        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        
        # 💡 100이 넘는 밝은 픽셀이 단 '3개'도 안 남았다면 찐 오링으로 100% 확정 판정!
        return cv2.countNonZero(thresh) < 3
    except:
        return False

EXP_ROI_X1, EXP_ROI_X2 = 65, 135
EXP_ROI_Y1, EXP_ROI_Y2 = 480, 495

ANT_IN_X1, ANT_IN_X2 = 0, 150   
ANT_IN_Y1, ANT_IN_Y2 = 420, 485

try:
    img_sword_bgra = cv2.imread("qq/sword.png", cv2.IMREAD_UNCHANGED)
    if img_sword_bgra is not None and len(img_sword_bgra.shape) == 3 and img_sword_bgra.shape[2] == 4:
        img_sword = img_sword_bgra[:, :, :3]
        img_sword_mask = img_sword_bgra[:, :, 3]
    else:
        img_sword = cv2.imread("qq/sword.png", cv2.IMREAD_COLOR)
        img_sword_mask = None
except: img_sword, img_sword_mask = None, None

try:
    img_circle_bgra = cv2.imread("qq/circle.png", cv2.IMREAD_UNCHANGED)
    if img_circle_bgra is not None and len(img_circle_bgra.shape) == 3 and img_circle_bgra.shape[2] == 4:
        img_circle = img_circle_bgra[:, :, :3]
        img_circle_mask = img_circle_bgra[:, :, 3]
    else:
        img_circle = cv2.imread("qq/circle.png", cv2.IMREAD_COLOR)
        img_circle_mask = None
except: img_circle, img_circle_mask = None, None

# 🚀 [신규 추가] 인벤토리 열림 감지용 inven.png 로드
try:
    img_inven_bgra = cv2.imread("qq/inven.png", cv2.IMREAD_UNCHANGED)
    if img_inven_bgra is not None and len(img_inven_bgra.shape) == 3 and img_inven_bgra.shape[2] == 4:
        img_inven = img_inven_bgra[:, :, :3]
        img_inven_mask = img_inven_bgra[:, :, 3]
    else:
        img_inven = cv2.imread("qq/inven.png", cv2.IMREAD_COLOR)
        img_inven_mask = None
except: img_inven, img_inven_mask = None, None

# 💀 [신규 추가] 사망 감지창(death.png) 로드
try:
    img_death_bgra = cv2.imread("qq/death.png", cv2.IMREAD_UNCHANGED)
    if img_death_bgra is not None and len(img_death_bgra.shape) == 3 and img_death_bgra.shape[2] == 4:
        img_death = img_death_bgra[:, :, :3]
        img_death_mask = img_death_bgra[:, :, 3]
    else:
        img_death = cv2.imread("qq/death.png", cv2.IMREAD_COLOR)
        img_death_mask = None
except: img_death, img_death_mask = None, None

# 🏹 [신규 추가] 은화살 장착(ON) 글씨 감지용 이미지 로드
try:
    img_on_bgra = cv2.imread("qq/on.png", cv2.IMREAD_UNCHANGED)
    if img_on_bgra is not None and len(img_on_bgra.shape) == 3 and img_on_bgra.shape[2] == 4:
        img_on = img_on_bgra[:, :, :3]
        img_on_mask = img_on_bgra[:, :, 3]
    else:
        img_on = cv2.imread("qq/on.png", cv2.IMREAD_COLOR)
        img_on_mask = None
except: img_on, img_on_mask = None, None

# 🏃 [1트랙 신규 센서] 헤이스트(Haste) 버프 아이콘 감지용 이미지 로드 (투명 배경 마스크 지원)
try:
    img_haste_bgra = cv2.imread("haste.png", cv2.IMREAD_UNCHANGED)
    if img_haste_bgra is not None and len(img_haste_bgra.shape) == 3 and img_haste_bgra.shape[2] == 4:
        img_haste = img_haste_bgra[:, :, :3]
        img_haste_mask = img_haste_bgra[:, :, 3]
    else:
        img_haste = cv2.imread("haste.png", cv2.IMREAD_COLOR)
        img_haste_mask = None
except: img_haste, img_haste_mask = None, None

# 👇👇👇 [여기서부터 새로 추가!] 👇👇👇
# 🏃 [듀얼 센서 추가] 두 번째 헤이스트 보조 아이콘 (qq 폴더 내 haste2.png) 교차 검증용 로드
try:
    img_haste2_bgra = cv2.imread("qq/haste2.png", cv2.IMREAD_UNCHANGED)
    if img_haste2_bgra is not None and len(img_haste2_bgra.shape) == 3 and img_haste2_bgra.shape[2] == 4:
        img_haste2 = img_haste2_bgra[:, :, :3]
        img_haste2_mask = img_haste2_bgra[:, :, 3]
    else:
        img_haste2 = cv2.imread("qq/haste2.png", cv2.IMREAD_COLOR)
        img_haste2_mask = None
except: img_haste2, img_haste2_mask = None, None
# 👆👆👆 ============================== 👆👆👆

# 💬 [1트랙 하이브리드] 헤이스트 종료 채팅 메세지 감지용 이미지 로드
try:
    img_haste_x_bgra = cv2.imread("haste_x.png", cv2.IMREAD_UNCHANGED)
    if img_haste_x_bgra is not None and len(img_haste_x_bgra.shape) == 3 and img_haste_x_bgra.shape[2] == 4:
        img_haste_x = img_haste_x_bgra[:, :, :3]
        img_haste_x_mask = img_haste_x_bgra[:, :, 3]
    else:
        img_haste_x = cv2.imread("qq/haste_x.png", cv2.IMREAD_COLOR)
        img_haste_x_mask = None
except: img_haste_x, img_haste_x_mask = None, None

# 🚀 커서 로드 부분도 qq 안에 넣기 위해 추가!
try:
    cursor_bgra = cv2.imread("qq/cursor_custom.png", cv2.IMREAD_UNCHANGED) 
    if cursor_bgra is not None: cursor_color, cursor_mask = cursor_bgra[:, :, :3], cursor_bgra[:, :, 3]
    else: cursor_color, cursor_mask = None, None
except: cursor_color, cursor_mask = None, None

# 👇👇👇 (기존 코드) 손바닥 커서 (cursor2.png) 로드! 👇👇👇
try:
    cursor2_bgra = cv2.imread("qq/cursor2.png", cv2.IMREAD_UNCHANGED) 
    if cursor2_bgra is not None and len(cursor2_bgra.shape) == 3 and cursor2_bgra.shape[2] == 4:
        cursor2_color, cursor2_mask = cursor2_bgra[:, :, :3], cursor2_bgra[:, :, 3]
    else:
        cursor2_color = cv2.imread("qq/cursor2.png", cv2.IMREAD_COLOR)
        cursor2_mask = None
except: cursor2_color, cursor2_mask = None, None

# 👇👇👇 [여기에 신규 추가] 대화창 특수 커서 (cursor_talk.png) 로드! 👇👇👇
try:
    cursor_talk_bgra = cv2.imread("qq/cursor_talk.png", cv2.IMREAD_UNCHANGED) 
    if cursor_talk_bgra is not None and len(cursor_talk_bgra.shape) == 3 and cursor_talk_bgra.shape[2] == 4:
        cursor_talk_color, cursor_talk_mask = cursor_talk_bgra[:, :, :3], cursor_talk_bgra[:, :, 3]
    else:
        cursor_talk_color = cv2.imread("qq/cursor_talk.png", cv2.IMREAD_COLOR)
        cursor_talk_mask = None
except: cursor_talk_color, cursor_talk_mask = None, None

# 👇👇 [인증 추가] 윈도우 바탕화면/웹 인증용 커서 및 인증창 감지 이미지 로드
try:
    cursor3_bgra = cv2.imread("qq/certi/cursor3.png", cv2.IMREAD_UNCHANGED)
    if cursor3_bgra is not None and len(cursor3_bgra.shape) == 3 and cursor3_bgra.shape[2] == 4:
        globals()["cursor3_color"], globals()["cursor3_mask"] = cursor3_bgra[:, :, :3], cursor3_bgra[:, :, 3]
    else:
        globals()["cursor3_color"] = cv2.imread("qq/certi/cursor3.png", cv2.IMREAD_COLOR)
        globals()["cursor3_mask"] = None
except: globals()["cursor3_color"], globals()["cursor3_mask"] = None, None

try:
    cursor4_bgra = cv2.imread("qq/certi/cursor4.png", cv2.IMREAD_UNCHANGED)
    if cursor4_bgra is not None and len(cursor4_bgra.shape) == 3 and cursor4_bgra.shape[2] == 4:
        globals()["cursor4_color"], globals()["cursor4_mask"] = cursor4_bgra[:, :, :3], cursor4_bgra[:, :, 3]
    else:
        globals()["cursor4_color"] = cv2.imread("qq/certi/cursor4.png", cv2.IMREAD_COLOR)
        globals()["cursor4_mask"] = None
except: globals()["cursor4_color"], globals()["cursor4_mask"] = None, None

try:
    certi_bgra = cv2.imread("qq/certi/certi.png", cv2.IMREAD_UNCHANGED)
    if certi_bgra is not None and len(certi_bgra.shape) == 3 and certi_bgra.shape[2] == 4:
        globals()["certi_color"], globals()["certi_mask"] = certi_bgra[:, :, :3], certi_bgra[:, :, 3]
    else:
        globals()["certi_color"] = cv2.imread("qq/certi/certi.png", cv2.IMREAD_COLOR)
        globals()["certi_mask"] = None
except: globals()["certi_color"], globals()["certi_mask"] = None, None

try:
    _t2_path = "qq/certi/ticket2.png" if os.path.exists("qq/certi/ticket2.png") else "qq/ticket2.png"
    ticket2_bgra = cv2.imread(_t2_path, cv2.IMREAD_UNCHANGED)
    if ticket2_bgra is not None and len(ticket2_bgra.shape) == 3 and ticket2_bgra.shape[2] == 4:
        globals()["ticket2_color"], globals()["ticket2_mask"] = ticket2_bgra[:, :, :3], ticket2_bgra[:, :, 3]
    else:
        globals()["ticket2_color"] = cv2.imread(_t2_path, cv2.IMREAD_COLOR)
        globals()["ticket2_mask"] = None
except: globals()["ticket2_color"], globals()["ticket2_mask"] = None, None
# 👆👆👆 ======================================================== 👆👆👆

# =====================================================================
# 🌟 [마을 정비 전용 통합 엔진] 폴더 이미지 무지성 로드! (휴지통, 맡기기, 찾기)
# =====================================================================
TRASH_TEMPLATES = []
LEAVE_TEMPLATES = []
PICK_TEMPLATES = {}
INVEN_BLACK_TEMPLATE = None

def load_all_templates():
    global TRASH_TEMPLATES, LEAVE_TEMPLATES, PICK_TEMPLATES, INVEN_BLACK_TEMPLATE
    
    # 1. 인벤 여백 감지 
    if os.path.exists("qq/inven_black.png"): 
        INVEN_BLACK_TEMPLATE = cv2.imread("qq/inven_black.png", cv2.IMREAD_COLOR)
        if INVEN_BLACK_TEMPLATE is not None:
            print("🎒 [인벤 스크롤] 빈 공간(여백) 감지 이미지 로드 완료!")
            
    # 2. 휴지통 (trash 폴더)
    TRASH_TEMPLATES.clear()
    if os.path.exists("qq/trash"):
        for filename in os.listdir("qq/trash"):
            if filename.lower().endswith((".png", ".jpg")):
                path = os.path.join("qq/trash", filename)
                img = cv2.imread(path, cv2.IMREAD_COLOR)
                if img is not None:
                    h, w = img.shape[:2]
                    if h > 15 and w > 15: img = img[4:h-4, 4:w-4] # 테두리 4픽셀 가위질
                    TRASH_TEMPLATES.append({"color": img, "mask": None})
        print(f"🗑️ [휴지통] 쓰레기 알맹이 추출 완료! (총 {len(TRASH_TEMPLATES)}개 장전)")

    # 3. 창고 맡길 템 (leave 폴더 스캔 - 무지성 로딩)
    LEAVE_TEMPLATES.clear()
    if os.path.exists("qq/leave"):
        for f in os.listdir("qq/leave"):
            if f.lower().endswith((".png", ".jpg")):
                path = os.path.join("qq/leave", f)
                bgra = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if bgra is not None:
                    if len(bgra.shape) == 3 and bgra.shape[2] == 4:
                        color, mask = bgra[:, :, :3], bgra[:, :, 3]
                        h, w = color.shape[:2]
                        if h > 15 and w > 15: color, mask = color[4:h-4, 4:w-4], mask[4:h-4, 4:w-4]
                        LEAVE_TEMPLATES.append({"name": f, "color": color, "mask": mask})
                    else:
                        color = cv2.imread(path, cv2.IMREAD_COLOR)
                        if color is not None:
                            h, w = color.shape[:2]
                            if h > 15 and w > 15: color = color[4:h-4, 4:w-4]
                            LEAVE_TEMPLATES.append({"name": f, "color": color, "mask": None})
        print(f"📦 [창고 맡기기] 아이템 {len(LEAVE_TEMPLATES)}개 로드 완료!")
                    
    # 4. 창고 찾을 템 (pick 폴더 스캔)
    PICK_TEMPLATES.clear()
    if os.path.exists("qq/pick"):
        for f in os.listdir("qq/pick"):
            if f.lower().endswith((".png", ".jpg")):
                path = os.path.join("qq/pick", f)
                bgra = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if bgra is not None:
                    key_name = os.path.splitext(f)[0].lower() # 'arrow', 'teleport', 'ent' 등
                    if len(bgra.shape) == 3 and bgra.shape[2] == 4:
                        color, mask = bgra[:, :, :3], bgra[:, :, 3]
                        h, w = color.shape[:2]
                        if h > 15 and w > 15: color, mask = color[4:h-4, 4:w-4], mask[4:h-4, 4:w-4]
                        PICK_TEMPLATES[key_name] = {"name": f, "color": color, "mask": mask}
                    else:
                        color = cv2.imread(path, cv2.IMREAD_COLOR)
                        if color is not None:
                            h, w = color.shape[:2]
                            if h > 15 and w > 15: color = color[4:h-4, 4:w-4]
                            PICK_TEMPLATES[key_name] = {"name": f, "color": color, "mask": None}
        print(f"🛍️ [창고 찾기] 아이템 {len(PICK_TEMPLATES)}개 로드 완료!")

    global WW_TEMPLATES
    WW_TEMPLATES = {}
    if os.path.exists("ww"):
        for f in os.listdir("ww"):
            if f.lower().endswith((".png", ".jpg")):
                path = os.path.join("ww", f)
                bgra = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if bgra is not None:
                    key_name = os.path.splitext(f)[0].lower() # 'shop', 'godam', 'ok' 등
                    if len(bgra.shape) == 3 and bgra.shape[2] == 4:
                        WW_TEMPLATES[key_name] = {"color": bgra[:, :, :3], "mask": bgra[:, :, 3]}
                    else:
                        WW_TEMPLATES[key_name] = {"color": cv2.imread(path, cv2.IMREAD_COLOR), "mask": None}
        print(f"🏪 [장사 봇] ww 폴더 에셋 {len(WW_TEMPLATES)}개 팩트 체크 및 로드 완료!")
        
    # 👇👇👇 [신규 추가] qq 폴더에 저장된 순간이동 주문서(telleport) 개별 로드 👇👇👇
    if os.path.exists("qq/telleport.png"):
        path = "qq/telleport.png"
        bgra = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if bgra is not None:
            if len(bgra.shape) == 3 and bgra.shape[2] == 4:
                WW_TEMPLATES["telleport"] = {"color": bgra[:, :, :3], "mask": bgra[:, :, 3]}
            else:
                WW_TEMPLATES["telleport"] = {"color": cv2.imread(path, cv2.IMREAD_COLOR), "mask": None}
            print("🏪 [장사 봇] 판매 물품 (qq/telleport.png) 팩트 체크 및 로드 완료!")

    # 👇👇👇 [회수 봇 전용] 창고지기(npc_hakim)와 맡기기(leave) 이미지 개별 로드 👇👇👇
    if os.path.exists("qq/npc_hakim.png"):
        bgra = cv2.imread("qq/npc_hakim.png", cv2.IMREAD_UNCHANGED)
        if bgra is not None:
            if len(bgra.shape) == 3 and bgra.shape[2] == 4: WW_TEMPLATES["npc_hakim"] = {"color": bgra[:, :, :3], "mask": bgra[:, :, 3]}
            else: WW_TEMPLATES["npc_hakim"] = {"color": cv2.imread("qq/npc_hakim.png", cv2.IMREAD_COLOR), "mask": None}
            print("🔄 [회수 봇] 창고지기 (qq/npc_hakim.png) 로드 완료!")

    if os.path.exists("qq/leave.png"):
        bgra = cv2.imread("qq/leave.png", cv2.IMREAD_UNCHANGED)
        if bgra is not None:
            if len(bgra.shape) == 3 and bgra.shape[2] == 4: WW_TEMPLATES["leave"] = {"color": bgra[:, :, :3], "mask": bgra[:, :, 3]}
            else: WW_TEMPLATES["leave"] = {"color": cv2.imread("qq/leave.png", cv2.IMREAD_COLOR), "mask": None}
            print("🔄 [회수 봇] 맡기기 버튼 (qq/leave.png) 로드 완료!")

load_all_templates()

WEIGHT_ROI_X1, WEIGHT_ROI_X2 = 22, 63
WEIGHT_ROI_Y1, WEIGHT_ROI_Y2 = 535, 549

def check_weight_status(img_bgr):
    """무게 게이지 상태를 0(정상), 1(주황/노랑 무거움), 2(완전빨강 전투불능) 3단계로 정밀 판독"""
    if img_bgr is None: return 0
    try:
        roi = img_bgr[WEIGHT_ROI_Y1:WEIGHT_ROI_Y2, WEIGHT_ROI_X1:WEIGHT_ROI_X2]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # 🚨 빨간색 (82% 이상 전투불능) 마스크 (Hue: 0~10, 170~180)
        mask_red1 = cv2.inRange(hsv, (0, 150, 100), (10, 255, 255))
        mask_red2 = cv2.inRange(hsv, (170, 150, 100), (180, 255, 255))
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        # ⚠️ 주황색/노란색 (50% 이상 무거움) 마스크 (Hue: 11~35)
        mask_orange = cv2.inRange(hsv, (11, 100, 100), (35, 255, 255))
        
        if cv2.countNonZero(mask_red) > 15:
            return 2
        elif cv2.countNonZero(mask_orange) > 15:
            return 1
        return 0
    except:
        return 0


# ==========================================
# 1. 타겟 및 파티 설정 (1인칭 독립형)
# ==========================================
ALL_MINI_PCS = [
    {"key": "미니1", "title": "프로젝터 - 소스: 미니1", "com_port": "COM3"},
    {"key": "미니2", "title": "프로젝터 - 소스: 미니2", "com_port": "COM4"},
    {"key": "미니3", "title": "프로젝터 - 소스: 미니3", "com_port": "COM5"},
    {"key": "미니4", "title": "프로젝터 - 소스: 미니4", "com_port": "COM6"} # 🚀 미니4 추가 (포트는 임시값, GUI에서 언제든 변경 가능)
]

# 🚀 [커맨드 센터] 1클라 전용 모드 해제! 군주 4명을 모두 제어하는 4클라 모드로 원상복구!
MINI_PCS = ALL_MINI_PCS

CAPTURE_ROIS, latest_frames = {}, {}
root = tk.Tk()
gui_vars = {}

saved_settings = load_settings()
global_settings = saved_settings.get("GLOBAL", {})
BASE_X = int(global_settings.get("base_x", 350))
BASE_Y = int(global_settings.get("base_y", 1300))
current_pc_num = global_settings.get("pc_num", "1")
DEBUG_MODE = global_settings.get("debug_mode", True) 
# 🚀 [수정] 사진에 맞춰 기본 프레임을 40 FPS(0.025초)로 변경
GLOBAL_FRAME_DELAY = global_settings.get("frame_delay", 0.025) 

for pc in MINI_PCS:
    k = pc["key"]
    pc_set = saved_settings.get(k, {}) 
    
    if "com_port" in pc_set:
        pc["com_port"] = pc_set["com_port"]
        
    # 🚀 [사진과 동일하게 초기 기본값(Default) 풀세팅 완료]
    gui_vars[k] = {
        "com_port": tk.StringVar(value=pc.get("com_port", "")),
        "role": tk.StringVar(value=pc_set.get("role", "솔플 : 던전")),
        "dungeon_name": tk.StringVar(value=pc_set.get("dungeon_name", "개미굴 6층")),
        "heal_use": tk.BooleanVar(value=pc_set.get("heal_use", True)),
        "heal_pct": tk.StringVar(value=pc_set.get("heal_pct", "70")),
        "heal_mp_pct": tk.StringVar(value=pc_set.get("heal_mp_pct", "12")),
        "pot_use": tk.BooleanVar(value=pc_set.get("pot_use", True)),
        "pot_pct": tk.StringVar(value=pc_set.get("pot_pct", "45")),
        "poison_type": tk.StringVar(value=pc_set.get("poison_type", "해독제")),
        "poison_delay": tk.StringVar(value=pc_set.get("poison_delay", "8")), 
        # 🚀 [수정] 초기 기본값을 신규 3셋트 풀버프 이름으로 교체!
        "buff_set": tk.StringVar(value=pc_set.get("buff_set", "3셋트 (실드, 웨폰, 아머, 계열)")),
        "use_dec_weight": tk.BooleanVar(value=pc_set.get("use_dec_weight", True)),
        "use_trans": tk.BooleanVar(value=pc_set.get("use_trans", False)),
        "use_body": tk.BooleanVar(value=pc_set.get("use_body", True)),
        "body_pct": tk.StringVar(value=pc_set.get("body_pct", "80")),
        "body_stop_pct": tk.StringVar(value=pc_set.get("body_stop_pct", "85")),
        
        "use_mptam": tk.BooleanVar(value=pc_set.get("use_mptam", True)),
        "mptam_start_pct": tk.StringVar(value=pc_set.get("mptam_start_pct", "30")),
        "mptam_stop_pct": tk.StringVar(value=pc_set.get("mptam_stop_pct", "60")),
        
        "use_extra_f10": tk.BooleanVar(value=pc_set.get("use_extra_f10", False)),
        "extra_f10_dur": tk.StringVar(value=pc_set.get("extra_f10_dur", "10분")),
        "use_blue_pot": tk.BooleanVar(value=pc_set.get("use_blue_pot", False)),
        "blue_deficit": tk.StringVar(value=str(pc_set.get("blue_deficit", "11"))), # 🚀 결손방수 변수 적용
        "tele_hunt_use": tk.BooleanVar(value=pc_set.get("tele_hunt_use", True)),
        "tele_hunt_time": tk.StringVar(value=pc_set.get("tele_hunt_time", "8")),
        "hp_20_action": tk.StringVar(value=pc_set.get("hp_20_action", "텔레포트 (F11)")),
        "hp_danger_pct": tk.StringVar(value=pc_set.get("hp_danger_pct", "45")),
        "abs_return_use": tk.BooleanVar(value=pc_set.get("abs_return_use", False)), # 🚀 신규: 절대귀환 사용여부
        "abs_return_pct": tk.StringVar(value=pc_set.get("abs_return_pct", "15")),   # 🚀 신규: 절대귀환 HP 수치
        "pk_drop_pct": tk.StringVar(value=pc_set.get("pk_drop_pct", "12")),
        "max_combat_time": tk.StringVar(value=pc_set.get("max_combat_time", "15")), 
        "return_cond": tk.StringVar(value=pc_set.get("return_cond", "은화살부족")),
        "move_sens": tk.StringVar(value=pc_set.get("move_sens", "2000")),
        
        "motion_sensitivity": tk.StringVar(value=pc_set.get("motion_sensitivity", "35")),
        "gb_count_normal": tk.StringVar(value=pc_set.get("gb_count_normal", "3")),
        "gb_count_dng": tk.StringVar(value=pc_set.get("gb_count_dng", "4")),
        "use_gb_detect": tk.BooleanVar(value=pc_set.get("use_gb_detect", False)), 
        "gb_exc_user": tk.BooleanVar(value=pc_set.get("gb_exc_user", True)),
        "buy_item": tk.StringVar(value=pc_set.get("buy_item", "은화살")),
        "buy_qty": tk.StringVar(value=pc_set.get("buy_qty", "5000")),
        "buy_count": tk.StringVar(value=pc_set.get("buy_count", "3")),
        "sell_item": tk.StringVar(value=pc_set.get("sell_item", "(추후 추가)")),
        
        # 👇👇👇 [1단계 신규 추가] 창고에서 꺼낼 물건 수량 변수 👇👇👇
        "pick_arrow": tk.StringVar(value=pc_set.get("pick_arrow", "5000")),
        "pick_teleport": tk.StringVar(value=pc_set.get("pick_teleport", "20")),
        "pick_ent": tk.StringVar(value=pc_set.get("pick_ent", "10")),
        
        # 👇👇👇 [신규 추가] 방향 잠금 UI 변수 등록 👇👇👇
        "use_dir_lock": tk.BooleanVar(value=pc_set.get("use_dir_lock", False)),
        "lock_dir": tk.StringVar(value=pc_set.get("lock_dir", "9시")),
        "auth_main_id": tk.StringVar(value=pc_set.get("auth_main_id", "")),
        "auth_main_pw": tk.StringVar(value=pc_set.get("auth_main_pw", "")),
        "auth_main_email": tk.StringVar(value=pc_set.get("auth_main_email", "")),
        "auth_main_phone": tk.StringVar(value=pc_set.get("auth_main_phone", "")),
        "auth_delay_use": tk.BooleanVar(value=pc_set.get("auth_delay_use", False)),
        "auth_auto_captcha": tk.BooleanVar(value=pc_set.get("auth_auto_captcha", False)),
        "auth_delay_start_min": tk.StringVar(value=str(pc_set.get("auth_delay_start_min", "55"))),
        "auth_delay_end_min": tk.StringVar(value=str(pc_set.get("auth_delay_end_min", "58"))),
        "auth_delay_sec": tk.StringVar(value=str(pc_set.get("auth_delay_sec", "180")))
        # 👆👆👆 ======================================= 👆👆👆
    }

current_settings = {}

# ==========================================
# 2. 다중 피코 자동 인식 및 큐 맵핑
# ==========================================
BAUD_RATE, POLLING_RATE = 115200, 0.008  
picos, pico_locks, pico_queues, ai_states = {}, {}, {}, {}
hunt_btn_dict = {} 
shop_btn_dict = {} # 🚀 [추가] 상점 봇 버튼 저장용
recall_btn_dict = {} # 🚀 [신규] 회수 봇 버튼 저장용
saved_buffs = load_buff_times()
now_t = time.time()

for pc in MINI_PCS:
    k = pc["key"]
    pico_locks[k] = threading.Lock()
    pico_queues[k] = queue.Queue()
    
    sb = saved_buffs.get(k, {})
    init_trans = sb.get("trans", 0); init_shield = sb.get("shield", 0); init_holy = sb.get("holy", 0)
    init_enchant = sb.get("enchant", 0); init_blessed = sb.get("blessed", 0)
    init_dex = sb.get("dex", 0); init_decrease = sb.get("decrease", 0)
    init_extra_f10 = sb.get("extra_f10", 0); init_light = sb.get("light", 0) 
    
    sb = saved_buffs.get(k, {})
    
    # 🚀 [냉동 해제 수술] 파일에 저장된 값은 '남은 시간(초)'이므로, 매크로를 켠 '현재 시간(now_t)'에 더해서 알람시계를 복구합니다!
    init_trans = now_t + sb.get("trans", 0); init_shield = now_t + sb.get("shield", 0); init_holy = now_t + sb.get("holy", 0)
    init_enchant = now_t + sb.get("enchant", 0); init_blessed = now_t + sb.get("blessed", 0)
    init_dex = now_t + sb.get("dex", 0); init_decrease = now_t + sb.get("decrease", 0)
    init_extra_f10 = now_t + sb.get("extra_f10", 0); init_light = now_t + sb.get("light", 0)
    init_blue_pot = now_t + sb.get("blue_pot", 0) 
    
    # 🚨 단, 꺼져있을 때 남은 시간이 0초로 저장됐었다면 버프가 만료된 것이므로 시작하자마자 쓰도록 세팅!
    if sb.get("trans", 0) == 0:  init_trans  = now_t + g_val(10, 60)
    if sb.get("shield", 0) == 0: init_shield = now_t + g_val(20, 120)
    if sb.get("holy", 0) == 0:   init_holy   = now_t + g_val(30, 180)
    if sb.get("enchant", 0) == 0: init_enchant = now_t + g_val(40, 200)
    if sb.get("blessed", 0) == 0: init_blessed = now_t + g_val(50, 220)
    if sb.get("dex", 0) == 0:     init_dex     = now_t + g_val(60, 240)
    if sb.get("decrease", 0) == 0: init_decrease = now_t + g_val(70, 260)
    if sb.get("extra_f10", 0) == 0: init_extra_f10 = now_t + g_val(80, 280)
    if sb.get("light", 0) == 0: init_light = now_t + g_val(90, 300)
    # 🚀 [수술] 시작 시 파랭이는 쿨타임 없이 즉시 먹을 수 있게 0으로 세팅!
    if sb.get("blue_pot", 0) == 0: init_blue_pot = 0

    ai_states[k] = {
        # 🚀 [형님 오더 적용] 파일 저장값 쌩까고 켤 때마다 피로도 무조건 백지화(0.0, 1.0) 하드코딩!
        "bot_start_time": now_t, "accum_hunt_time": 0.0,
        "fatigue_mult": 1.0, "next_fatigue_target": 0.0,
        "last_g_time_call": now_t, "is_panic": False, "cooldown": 0, "cursor_pos": [400, 300],
        "patrol_idx": random.choice([0, 4]), "patrol_direction": random.choice([1, -1]),   
        "patrol_start": time.time(), "patrol_duration": g_val(2.0, 3.0),
        "last_chase_dist": 999.0, "stuck_start_time": time.time(), "is_paused": False, "is_hunt_active": False,
        "poison_timer": 0, "antidote_cd": 0, "heal_cd": 0, "potion_cd": 0,
        "buff_trans_time": init_trans, "buff_shield_time": init_shield, "buff_holy_time": init_holy, 
        "buff_enchant_time": init_enchant, "buff_blessed_time": init_blessed,
        "buff_dex_time": init_dex, "buff_decrease_time": init_decrease,
        "buff_extra_f10_time": init_extra_f10, "buff_light_time": init_light, "buff_blue_pot_time": init_blue_pot,
        "arrow_image": None, "next_arrow_check": 0, "last_arrow_change_time": 0.0, "arrow_is_firing": False,
        "is_attacking": False, "attack_cmd_time": 0.0, "has_fired_arrow": False, "humanize_cd": 0.0, 
        "exp_image": None, "next_exp_check": 0, "last_exp_time": now_t, 
        "is_pulling": False, "pull_start_time": 0.0, "next_attack_type": "NORMAL",
        "loot_state": "IDLE", "loot_timeout": 0.0, "loot_f4_cd": 0.0,
        "target_fsm": "IDLE", "hover_start_time": 0.0, "hover_pos": (0, 0),
        "last_cursor_found_time": now_t, "body_to_mind_active": False, "body_cd": 0.0,
        "last_anchor_pos": None, "anchor_lost_time": 0.0, "anchor_image": None, "need_anchor_update": False,
        "anchor_offset": (0, 0), "mob_template": None,
        "dungeon_angle": random.uniform(0, 2 * math.pi), "dungeon_map_pos": None, "dungeon_last_map_pos": None,
        "dungeon_stuck_timer": time.time(), "dungeon_map_lost_timer": 0.0,
        "abort_macro": False,
        "dungeon_global_path": [], "dungeon_path_time": 0.0, "dungeon_target_pt": None,
        "dungeon_corner_idx": 0, 
        "dungeon_going_center": False, 
        "last_pause_time": 0.0,
        "last_mob_pos": None, 
        "last_mob_time": 0.0, 
        "miss_count": 0,
        
        # ==========================================================
        # 🧠 [터미네이터 V2 전투/루팅 뇌 메모리 확장]
        # ==========================================================
        "pre_target_data": None,        # 뼈대 D: 전투 중 몰래 찍어둔 다음 타겟 (좌표 및 모션 여부 기억)
        "exp_drop_wait_timer": 0.0      # 뼈대 E: 몹 사망 후 비동기 드랍 대기 알람시계
    }

def init_hardware_picos():
    print("\n⏳ [하드웨어] 스마트 포트(지문/위치) 추적 및 다중 연결 중...")
    import serial.tools.list_ports
    
    # 현재 윈도우에 꽂혀있는 모든 USB 통신 포트 스캔
    all_ports = list(serial.tools.list_ports.comports())
    
    for pc in MINI_PCS:
        key = pc["key"]
        pc_set = saved_settings.get(key, {})
        
        # 1. 뇌에 각인된 영혼(지문/Location)과 예전 껍데기(COM) 정보를 가져옵니다.
        target_hwid = pc_set.get("pico_hwid", "")
        fallback_port = pc_set.get("com_port", "")
        target_port = None
        
        # 2. 🚀 [1순위 방어막] 이전에 저장된 COM 포트가 여전히 살아있고 지문도 똑같다면 무조건 1순위 채택! (중복 기기 새치기 완벽 차단)
        if fallback_port:
            for p in all_ports:
                if p.device.upper() == fallback_port.upper():
                    current_soul = str(p.serial_number) if p.serial_number else (str(p.location) if p.location else str(p.hwid))
                    # 지문이 없거나, 지문이 일치하면 남의 것 탐내지 않고 무조건 내 자리로 인정!
                    if not target_hwid or (current_soul and (target_hwid in current_soul or current_soul in target_hwid)):
                        target_port = p.device
                        print(f"🎯 [{key}] 기존 지정 포트 [{target_port}] 팩트 체크 완료! 최우선 할당합니다.")
                    break
        
        # 3. 🚀 [2순위 추적] 윈도우가 COM 번호를 바꿔버려서 1순위에서 실패했다면? 그때서야 지문으로 싹 다 뒤져서 찾아냅니다!
        if not target_port and target_hwid:
            for p in all_ports:
                current_soul = str(p.serial_number) if p.serial_number else (str(p.location) if p.location else str(p.hwid))
                if current_soul and (target_hwid in current_soul or current_soul in target_hwid):
                    target_port = p.device
                    print(f"🔍 [{key}] 윈도우 포트 변경 감지! 지문 추적을 통해 [{target_port}](으)로 낚아챘습니다!")
                    break
        
        # 4. 그래도 못 찾았다면, 최후의 보루로 그냥 껍데기(COM)라도 찔러봅니다.
        if not target_port and fallback_port:
            target_port = fallback_port
            
        if target_port:
            if key in gui_vars:
                gui_vars[key]["com_port"].set(target_port) # 💡 GUI 빈칸 숫자도 새 번호로 알아서 덮어씌움
            try: 
                # 💡 BAUD_RATE 전역변수 참조
                baud = globals().get("BAUD_RATE", 115200)
                picos[key] = serial.Serial(target_port, baud, timeout=0, write_timeout=0)
                print(f"✅ [{key}] -> {target_port} 장착 완료!")
                
                # 방금 연결 성공한 포트의 고유 지문을 뽑아서 파이썬 뇌에 실시간 각인!
                for p in all_ports:
                    if p.device.upper() == target_port.upper():
                        if key not in ai_states: ai_states[key] = {}
                        unique_id = str(p.serial_number) if p.serial_number else (str(p.location) if p.location else str(p.hwid))
                        ai_states[key]["pico_hwid"] = unique_id
                        break
                        
            except Exception as e: 
                picos[key] = None
                print(f"⚠️ [{key}] {target_port} 접속 실패! ({e})")
        else: 
            picos[key] = None

init_hardware_picos()

# ==============================================================================
# 🚀 [3단계 수술 완료] 피코 역송신(ACK) 수신 엔진 및 귀(Listener) 스레드
# ==============================================================================
def handle_pico_ack(key):
    if key in ai_states:
        ai_states[key]["pico_arrived"] = True
        # dprint(key, "📡 [역송신 팩트] 피코 하드웨어 완료 신호 수신!")

logger_states = {}

def toggle_intercept_logger(pc_name):
    if pc_name not in logger_states:
        logger_states[pc_name] = {"logging": False, "btn": None, "start_time": 0.0}
    state = logger_states[pc_name]
    btn = state.get("btn")
    
    state["logging"] = not state["logging"]
    
    if state["logging"]:
        state["start_time"] = time.perf_counter() 
        if btn: btn.config(text=f"🔴 {pc_name} 팩트 로깅중", bg="#E91E63")
        print(f"▶ [{pc_name}] 피코 H/W 역송신 절대 진실 로깅 시작! (Pico_RealLogs 폴더 확인)")
    else:
        if btn: btn.config(text=f"⚪ {pc_name} 팩트 로거 대기", bg="#455A64")
        print(f"⏸ [{pc_name}] 로깅 일시정지 (시리얼 통신 버퍼는 계속 비우는 중)")

def pico_echo_listener_thread(key):
    if key not in logger_states:
        logger_states[key] = {"logging": False, "btn": None, "start_time": 0.0}
        
    # 🚀 [수술 3] 스레드 시작 시 포트가 없으면 영원히 죽어버리던 코드(return) 완벽 삭제!

    save_dir = "Pico_RealLogs"
    if not os.path.exists(save_dir): os.makedirs(save_dir)

    buf = bytearray()
    last_btn = 0
    f = None
    file_idx = 1
    total_rows = 0
    write_count = 0
    file_start_time = 0.0

    def open_new_file():
        nonlocal f, total_rows, file_idx, file_start_time
        if f: f.flush(); f.close()
        start_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{save_dir}/RealLog_{key}_{start_str}_part{file_idx}.csv"
        f = open(filename, 'w', encoding='utf-8')
        f.write("xCount,yCount,Time (ms),buttonflags\n") 
        total_rows = 0
        file_idx += 1
        file_start_time = time.time()
        return f

    while True:
        try:
            # 🚀 [수술 3] 매 루프마다 현재 최신 p_serial을 가져오도록 안으로 이동!
            p_serial = picos.get(key)
            if not p_serial:
                time.sleep(0.1)
                continue
                
            state = logger_states.get(key, {})
            is_logging = state.get("logging", False)
            
            if p_serial.in_waiting > 0:
                buf.extend(p_serial.read(p_serial.in_waiting))
                
                while len(buf) > 0:
                    if buf[0] == 0xCC: 
                        handle_pico_ack(key)  # 🚩 파이썬 뇌에 "도착 완료!" 깃발 꽂기
                        del buf[:1]
                        continue
                        
                    elif buf[0] == 0xEE:
                        if len(buf) >= 10:
                            if buf[9] == 0xFE:
                                btn = buf[1]
                                mx = struct.unpack('b', bytes([buf[2]]))[0]
                                my = struct.unpack('b', bytes([buf[3]]))[0]
                                
                                hw_time_us = struct.unpack('<I', buf[5:9])[0]
                                
                                btn_flag = 0
                                if btn != last_btn:
                                    if (btn & 0x01) and not (last_btn & 0x01): btn_flag = 1 
                                    elif not (btn & 0x01) and (last_btn & 0x01): btn_flag = 2 
                                    last_btn = btn
                                    
                                if is_logging:
                                    if f is None: 
                                        f = open_new_file()
                                        state["start_micros"] = hw_time_us
                                    
                                    elapsed_us = hw_time_us - state.get("start_micros", hw_time_us)
                                    if elapsed_us < 0: elapsed_us += 4294967296 
                                    
                                    t_ms = elapsed_us / 1000.0
                                    
                                    f.write(f"{mx},{my},{t_ms:.4f},{btn_flag}\n")
                                    total_rows += 1
                                    write_count += 1
                                    
                                    if write_count >= 200:
                                        f.flush()
                                        write_count = 0

                                    if total_rows >= 500000 or (time.time() - file_start_time) >= 300: 
                                        f = open_new_file()
                                else:
                                    if f: f.flush(); f.close(); f = None
                                    
                                del buf[:10]
                            else:
                                del buf[:1]
                        else:
                            break
                            
                    else:
                        next_valid = -1
                        for i in range(1, len(buf)):
                            if buf[i] == 0xEE or buf[i] == 0xCC:
                                next_valid = i
                                break
                                
                        if next_valid != -1:
                            del buf[:next_valid]
                        else:
                            buf.clear()
            else:
                time.sleep(0.005)
        except Exception as e:
            time.sleep(0.1)

def pico_echo_manager_thread():
    started_keys = set()
    while True:
        try:
            current_keys = list(picos.keys())
            for key in current_keys:
                if key not in started_keys and picos.get(key) is not None:
                    threading.Thread(target=pico_echo_listener_thread, args=(key,), daemon=True).start()
                    started_keys.add(key)
        except Exception:
            pass
        time.sleep(1)

threading.Thread(target=pico_echo_manager_thread, daemon=True).start()
# ==============================================================================

def find_cursor_pos(img_bgr, last_pos=None, check_circle=False, allow_full_scan=True, is_certi_mode=False):
    targets = []
    if is_certi_mode:
        if globals().get("cursor3_color") is not None:
            targets.append((globals().get("cursor3_color"), globals().get("cursor3_mask"), 2, 2))
        if globals().get("cursor4_color") is not None:
            targets.append((globals().get("cursor4_color"), globals().get("cursor4_mask"), 2, 2))
        if is_certi_mode != "WEB" and cursor_color is not None and cursor_mask is not None:
            targets.append((cursor_color, cursor_mask, 5, 5))
    else:
        if cursor_color is not None and cursor_mask is not None: targets.append((cursor_color, cursor_mask, 5, 5)) 
        if cursor2_color is not None and cursor2_mask is not None: targets.append((cursor2_color, cursor2_mask, 5, 5))
        if cursor_talk_color is not None and cursor_talk_mask is not None: 
            th, tw = cursor_talk_color.shape[:2]
            targets.append((cursor_talk_color, cursor_talk_mask, 2, th - 2))
        if img_sword is not None and img_sword_mask is not None: targets.append((img_sword, img_sword_mask, 12, 12))
        if check_circle and img_circle is not None and img_circle_mask is not None: targets.append((img_circle, img_circle_mask, 24, 14))

    if not targets: return None
    h, w = img_bgr.shape[:2]
    search_w = w if is_certi_mode else (w - 30)
    safe_bgr = img_bgr.copy()

    def is_valid_cursor_patch(src_img, px, py, tw, th):
        if not is_certi_mode:
            return True
        patch = src_img[py:py+th, px:px+tw]
        if patch.size == 0:
            return False
        return float(np.std(patch)) >= 18.0

    local_err_limit = 0.12 if is_certi_mode else 0.20
    full_err_limit = 0.10 if is_certi_mode else 0.12

    if last_pos:
        lx, ly = last_pos; pad = 90 
        x1, y1 = max(0, int(lx) - pad), max(0, int(ly) - pad)
        x2, y2 = min(search_w, int(lx) + pad), min(h, int(ly) + pad)
        if x2 > x1 and y2 > y1:
            roi = safe_bgr[y1:y2, x1:x2]
            if roi.shape[0] > 10 and roi.shape[1] > 10:
                best_error = float('inf'); best_pos = None
                for template, mask, hx, hy in targets:
                    try:
                        th_t, tw_t = template.shape[:2]
                        if mask is not None:
                            res = cv2.matchTemplate(roi, template, cv2.TM_SQDIFF_NORMED, mask=mask)
                            res = np.nan_to_num(res, nan=1.0, posinf=1.0, neginf=1.0)
                            min_val, min_loc = 1.0, None
                            for _ in range(15):
                                mv, _, ml, _ = cv2.minMaxLoc(res)
                                if mv > local_err_limit:
                                    min_val, min_loc = mv, ml
                                    break
                                if is_valid_cursor_patch(roi, ml[0], ml[1], tw_t, th_t):
                                    min_val, min_loc = mv, ml
                                    break
                                cv2.circle(res, ml, 6, 1.0, -1)
                        else:
                            res = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
                            _, max_val, _, max_loc = cv2.minMaxLoc(res)
                            min_val = 1.0 - max_val
                            min_loc = max_loc
                            if not is_valid_cursor_patch(roi, min_loc[0], min_loc[1], tw_t, th_t):
                                continue

                        if min_loc is None:
                            continue
                        if min_val <= local_err_limit: return (min_loc[0] + x1 + hx, min_loc[1] + y1 + hy)
                        if min_val < best_error: 
                            best_error = min_val
                            best_pos = (min_loc[0] + x1 + hx, min_loc[1] + y1 + hy)
                    except: continue
                if best_error <= local_err_limit: return best_pos

    if not allow_full_scan: return None

    if not is_certi_mode:
        t_str = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{t_str}] ⚠️ [SYSTEM] 90px 반경 커서 이탈 감지! 전체 화면 풀스캔 가동 중...")

    search_img = safe_bgr[:, :search_w]
    best_error = float('inf'); best_pos = None
    for template, mask, hx, hy in targets:
        try:
            th_t, tw_t = template.shape[:2]
            if mask is not None:
                res = cv2.matchTemplate(search_img, template, cv2.TM_SQDIFF_NORMED, mask=mask)
                res = np.nan_to_num(res, nan=1.0, posinf=1.0, neginf=1.0)
                min_val, min_loc = 1.0, None
                for _ in range(20):
                    mv, _, ml, _ = cv2.minMaxLoc(res)
                    if mv > full_err_limit:
                        min_val, min_loc = mv, ml
                        break
                    if is_valid_cursor_patch(search_img, ml[0], ml[1], tw_t, th_t):
                        min_val, min_loc = mv, ml
                        break
                    cv2.circle(res, ml, 8, 1.0, -1)
            else:
                res = cv2.matchTemplate(search_img, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                min_val = 1.0 - max_val
                min_loc = max_loc
                if not is_valid_cursor_patch(search_img, min_loc[0], min_loc[1], tw_t, th_t):
                    continue

            if min_loc is None:
                continue
            if min_val <= full_err_limit: 
                if not is_certi_mode:
                    t_str = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    print(f"[{t_str}] ✅ [SYSTEM] 자가 치유 성공! 커서 복구 완료 (오차: {min_val*100:.1f}%)")
                return (min_loc[0] + hx, min_loc[1] + hy)
            if min_val < best_error:
                best_error = min_val
                best_pos = (min_loc[0] + hx, min_loc[1] + hy)
        except: continue
        
    if best_error <= full_err_limit: 
        if not is_certi_mode:
            t_str = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{t_str}] ✅ [SYSTEM] 자가 치유 성공! 커서 복구 완료 (오차: {best_error*100:.1f}%)")
        return best_pos
        
    return None


# 🚀 [캡처 병목 수술] 카메라맨은 무식한 상시 커서 스캔(find_cursor_pos)을 멈추고, 사진을 찍은 정확한 '시간'만 뇌로 넘깁니다! (이벤트 방식)
def mss_vision_thread():
    with mss.mss() as sct:
        while True:
            loop_start = time.time() 
            if not CAPTURE_ROIS: time.sleep(0.5); continue
            curr_time = time.time()
            for pc in MINI_PCS:
                key = pc["key"]
                if key in CAPTURE_ROIS:
                    try: 
                        img_np = np.array(sct.grab(CAPTURE_ROIS[key]))
                        latest_frames[key] = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
                        
                        # 🚀 [레이스 컨디션 파괴] 카메라맨이 사진을 찍은 '가장 신선한 시간'을 뇌에 각인!
                        if key in ai_states: 
                            ai_states[key]["last_frame_time"] = curr_time 
                            
                        # 💡 [뻘짓 원천 소각] 여기서 1초에 30번씩 눈알 굴리며 커서를 찾던 무거운 로직 완전 삭제!
                        # 사령관 뇌가 필요할 때(이벤트 발생 시)만 눈알을 굴리도록 통제권을 이관합니다!
                    except: pass
            
            # 👑 [가변 프레임 엔진] GUI에서 설정한 프레임에 맞춰 실시간으로 속도 조절!
            elapsed = time.time() - loop_start
            sleep_t = max(0.005, GLOBAL_FRAME_DELAY - elapsed) 
            time.sleep(sleep_t)
threading.Thread(target=mss_vision_thread, daemon=True).start()

active_manual_target = None

# ====================================================================
# 🏃‍♂️ [루팅 전용] 장애물 회피 8방향 우회 기동 (가우스 난수 적용)
# ====================================================================
def get_evasion_pos(char_cx, char_cy, target_x, target_y, attempt_count):
    import math, random
    dx = target_x - char_cx
    dy = (target_y - char_cy) / 0.85 # 리니지 Y축 원근 보정
    
    if dx == 0 and dy == 0: return char_cx, char_cy

    raw_angle_deg = (math.degrees(math.atan2(dy, dx)) + 360) % 360.0
    snap_angle = min(EVADE_MAP.keys(), key=lambda k: min(abs(k - raw_angle_deg), 360 - abs(k - raw_angle_deg)))

    possible_evades = EVADE_MAP[snap_angle]
    chosen_deg = possible_evades[attempt_count % 2] # 횟수에 따라 지그재그 회피

    jitter_deg = random.gauss(0, 2.5)
    final_rad = math.radians(chosen_deg + jitter_deg)

    evade_dist = max(60.0, min(110.0, random.gauss(85.0, 10.0)))
    tx = int(char_cx + math.cos(final_rad) * evade_dist)
    ty = int(char_cy + math.sin(final_rad) * (evade_dist * 0.85))

    return tx, ty
    
def generate_human_deltas(target_dx, target_dy, duration=None, behavior="NORMAL", key=None):
    distance = math.hypot(target_dx, target_dy)
    if distance == 0: return []
    # 🟢 수정 후 (가우시안 편차 곱연산 추가)
    if duration is None: 
        ideal_dur = 0.05 + 0.04 * math.log2((distance / 20.0) + 1.0)
        duration = apply_human_variance(ideal_dur) # 👈 에러 나지 않도록 ideal_dur을 넣고, 중복 연산은 삭제!

    overshoot_prob = 0.0; noise_mult = 1.0  
    if behavior == "PATROL":
        if random.random() < 0.25: duration *= g_val(0.7, 0.85)
        else: duration *= g_val(1.1, 1.3)
        overshoot_prob = 0.3; noise_mult = g_val(1.5, 2.0) 
    elif behavior == "HOVER":
        duration *= g_val(0.40, 0.52) # 🚀 [스나이핑 가속] 물리 마우스 투척 속도 약 20% 향상!
        dist_factor = max(0.0, min(1.0, (distance - 50.0) / 250.0))
        overshoot_prob = g_val(0.15, 0.35) * dist_factor
        noise_mult = g_val(1.0, 1.5) if random.random() < 0.3 else g_val(0.2, 0.5)

    elif behavior == "SHOP":
        # 🐌 [장사 봇 전용 감속 마우스] 이전 패치가 너무 느려 답답했던 점을 개선하여 30% 속도 상향!
        duration = g_val(0.16, 0.35) + (distance / 600.0) * g_val(0.15, 0.25)
        overshoot_prob = 0.05 
        noise_mult = g_val(0.3, 0.6)

    elif behavior == "DRAG":
        duration *= g_val(0.6, 0.8)
        overshoot_prob = 0.0
        noise_mult = g_val(0.2, 0.3)
    elif behavior == "CERTI":
        overshoot_prob = 0.0
        noise_mult = g_val(0.2, 0.35)
    elif behavior == "NORMAL":
        dist_factor = max(0.0, min(1.0, (distance - 30.0) / 90.0))
        if target_dx > 0: base_prob = g_val(0.45, 0.55)
        else: base_prob = g_val(0.20, 0.35)
        overshoot_prob = base_prob * dist_factor
        noise_mult = g_val(0.3, 0.6)

    has_overshoot = random.random() < overshoot_prob

    # =================================================================
    # 🎯 [수술 4번 적용] 소수점 오차 누적 지갑 (Error Carry)
    # 기존의 stochastic_round를 버리고, 잘려나간 소수점을 다음 프레임에 더해주는 
    # 완벽한 물리 마찰 렌더링(에러 캐리) 기법을 전역으로 적용합니다.
    # =================================================================
    rx, ry = 0.0, 0.0
    current_float_x, current_float_y = 0.0, 0.0
    current_int_x, current_int_y = 0, 0

    def get_curve_deltas(dx, dy, dur, is_homing=False):
        nonlocal rx, ry, current_float_x, current_float_y, current_int_x, current_int_y
        pts = []
        n_pts = max(1, int(dur / POLLING_RATE))
        if n_pts == 0: return pts

        dist_local = math.hypot(dx, dy)
        if dist_local == 0: return pts

        perp_x = -dy / dist_local if dist_local > 0 else 0.0
        perp_y = dx / dist_local if dist_local > 0 else 0.0

        # [수정 후] (로그(log) 대신 제곱근(sqrt)을 써서 거리가 멀 때 훨씬 더 사람 팔처럼 배가 불룩하게 휘어지게 만듦)
        bow_amount = math.sqrt(dist_local) * g_val(0.8, 1.5) * random.choice([1, -1])
        is_s_curve = (dist_local > 150) and (random.random() < 0.3)

        if is_s_curve:
            cp1_x = dx * g_val(0.15, 0.35) + perp_x * bow_amount * g_val(0.8, 1.2)
            cp1_y = dy * g_val(0.15, 0.35) + perp_y * bow_amount * g_val(0.8, 1.2)
            cp2_x = dx * g_val(0.65, 0.85) - perp_x * bow_amount * g_val(0.8, 1.2)
            cp2_y = dy * g_val(0.65, 0.85) - perp_y * bow_amount * g_val(0.8, 1.2)
        else:
            skew = g_val(0.35, 0.65) 
            cp1_x = dx * (skew - 0.15) + perp_x * bow_amount
            cp1_y = dy * (skew - 0.15) + perp_y * bow_amount
            cp2_x = dx * (skew + 0.15) + perp_x * bow_amount
            cp2_y = dy * (skew + 0.15) + perp_y * bow_amount
        
        # 🚀 [수술 1번 적용] 매번 형태가 달라지는 100% 가변형 비대칭 곡선 뼈대
        if is_homing:
            ease_cp1 = random.uniform(0.1, 0.3)
            ease_cp2 = random.uniform(0.5, 0.8)
        else:
            if random.random() < 0.7:
                ease_cp1 = random.uniform(0.05, 0.3)  # 초반 급가속
                ease_cp2 = random.uniform(0.7, 0.95)  # 후반 감속 길게 (롱테일)
            else:
                ease_cp1 = random.uniform(0.3, 0.6)   # 부드러운 출발
                ease_cp2 = random.uniform(0.6, 0.9)   # 후반 빠른 제동

        cx, cy = 0.0, 0.0
        tremor_x, tremor_y = 0.0, 0.0
        
        dist_factor_local = distance if 'distance' in locals() else dist_local
        n_mult = noise_mult if 'noise_mult' in locals() else 1.0
        
        base_noise = min(1.5, (0.85 if is_homing else max(0.2, min(1.2, dist_factor_local * 0.01))) * n_mult)
        warp_intensity = random.uniform(-0.06, 0.06)

        for i in range(1, n_pts + 1):
            t = i / n_pts
            
            if is_homing:
                ease_t = 1.0 - math.pow(1.0 - t, random.uniform(2.5, 3.5)) 
            else:
                warp_noise = math.sin(t * math.pi) * warp_intensity
                t_w = max(0.0, min(1.0, t + warp_noise))
                u_t = 1.0 - t_w
                ease_t = 3 * (u_t**2) * t_w * ease_cp1 + 3 * u_t * (t_w**2) * ease_cp2 + (t_w**3)
                
            u = 1.0 - ease_t
            px = 3 * (u**2) * ease_t * cp1_x + 3 * u * (ease_t**2) * cp2_x + (ease_t**3) * dx
            py = 3 * (u**2) * ease_t * cp1_y + 3 * u * (ease_t**2) * cp2_y + (ease_t**3) * dy
            
            if dist_local > 10:
                envelope = max(0.35, math.sin(t * math.pi)) * base_noise
                raw_noise_x = random.gauss(0, 1.2) * envelope
                raw_noise_y = random.gauss(0, 1.2) * envelope
                tremor_x = tremor_x * 0.85 + raw_noise_x * 0.15
                tremor_y = tremor_y * 0.85 + raw_noise_y * 0.15
            else:
                tremor_x = tremor_x * 0.8 + g_val(-0.15, 0.15) * 0.2
                tremor_y = tremor_y * 0.8 + g_val(-0.15, 0.15) * 0.2
                
            px += tremor_x
            py += tremor_y
            
            step_dx_raw = px - cx
            step_dy_raw = py - cy
            
            # 🚀 서브픽셀 가우시안 노이즈 주입 (브레슨햄 패턴 타파)
            noise_x = random.gauss(0, 0.45) if (n_pts - i) > 5 else 0.0
            noise_y = random.gauss(0, 0.45) if (n_pts - i) > 5 else 0.0
            
            exact_x = current_float_x + step_dx_raw + noise_x
            exact_y = current_float_y + step_dy_raw + noise_y
            
            # 오차 누적 시스템
            dx_float = (exact_x - current_int_x) + rx
            dy_float = (exact_y - current_int_y) + ry
            
            dx_int = int(round(dx_float))
            dy_int = int(round(dy_float))
            
            raw_rx = dx_float - dx_int
            raw_ry = dy_float - dy_int

            # 🚀 [브레즌햄 소각] 마우스 패드의 물리적 마찰로 인해 미세 소수점(텐션)이 증발하는 현상 구현!
            if random.random() < 0.15:
                # 15% 확률로 잘려나간 소수점(물리적 텐션)이 패드에 씹혀서 증발함 (기억 상실)
                # -> 기계적인 계단식 교차 배분 패턴 완벽 파괴!
                rx, ry = 0.0, 0.0
            else:
                # 100% 이월하지 않고, 70~95% 사이의 불규칙한 패드 탄성을 적용
                rx = raw_rx * random.uniform(0.70, 0.95)
                ry = raw_ry * random.uniform(0.70, 0.95)
            
            current_float_x = exact_x
            current_float_y = exact_y
            
            # 형님의 정지 마찰력 (Stiction) 방어 유지
            speed = math.hypot(step_dx_raw, step_dy_raw)
            if speed < 3.6 and i < n_pts:
                stiction_prob = max(0.0, 0.45 - speed * 0.15)
                if (dx_int != 0 or dy_int != 0) and math.hypot(dx_float, dy_float) < 3.5:
                    if random.random() < stiction_prob:
                        rx += dx_int
                        ry += dy_int
                        dx_int, dy_int = 0, 0
            
            current_int_x += dx_int
            current_int_y += dy_int
            
            pts.append((dx_int, dy_int))
            cx, cy = px, py
            
        return pts

    deltas = []
    
    # =================================================================
    # 🎯 [수술 2번 적용] 불규칙적인 오버슈트 & 언더슈트
    # =================================================================
    if has_overshoot:
        if target_dx > 0: over_ratio = g_val(0.08, 0.18)
        else: over_ratio = g_val(0.05, 0.12)
        
        # 🚀 35% 확률로 모자라게 도착(Undershoot)하는 패턴 믹스
        if random.random() < 0.35: 
            over_ratio = -g_val(0.05, 0.15)
            
        max_over_px = min(60.0, distance * abs(over_ratio))

        # 👇👇👇 [여기서부터 하단 UI 침범 물리적 방어막 추가됨] 👇👇👇
        # 마우스가 화면 아래쪽(target_dy > 0)으로 향할 때, 가속도로 인한 오버슈트(관성) 바운스를 강제로 15px 이내로 깎아냅니다!
        if target_dy > 0:
            max_over_px = min(15.0, max_over_px * 0.3)
        # 👆👆👆 [추가 끝] 👆👆👆

        if over_ratio < 0: max_over_px = -max_over_px

        angle = math.atan2(target_dy, target_dx) + g_val(-0.25, 0.25) 
        over_dx = target_dx + math.cos(angle) * max_over_px
        over_dy = target_dy + math.sin(angle) * max_over_px
        
        dur1 = duration * g_val(0.65, 0.75)
        deltas.extend(get_curve_deltas(over_dx, over_dy, dur1, is_homing=False))
        
        pause_ticks = max(1, int(g_val(0.02, 0.05) / POLLING_RATE))
        for p_i in range(pause_ticks): 
            drift_x = int(round(rx + random.gauss(0, 0.3)))
            drift_y = int(round(ry + random.gauss(0, 0.3)))
            current_int_x += drift_x
            current_int_y += drift_y
            rx -= drift_x
            ry -= drift_y
            deltas.append((drift_x, drift_y))
                
        sim_x, sim_y = current_int_x, current_int_y
        corr_dx, corr_dy = target_dx - sim_x, target_dy - sim_y
        
        homing_dur = duration - dur1 + g_val(0.1, 0.2)
        homing_dur = max(0.08, homing_dur)
        deltas.extend(get_curve_deltas(corr_dx, corr_dy, homing_dur, is_homing=True))
    else:
        deltas.extend(get_curve_deltas(target_dx, target_dy, duration, is_homing=False))

    if behavior != "DRAG" and distance > 10:
            for _ in range(max(1, int(g_val(0.01, 0.03) / POLLING_RATE))): 
                # 🚨 [수술 완료] 도착 후 억지로 1픽셀씩 와리가리를 치며 핑퐁을 유발하고 rx를 꼬이게 하던 난수 소각!
                # 사람이 마우스 목적지에 도달한 후 클릭 직전에 갖는 찰나의 숨고르기(관성 정지)를 위해,
                # (0, 0)만 얌전하게 추가하여 물리적으로 완벽한 브레이킹(Resting)을 보장합니다.
                deltas.append((0, 0))

    final_dx = int(target_dx) - current_int_x
    final_dy = int(target_dy) - current_int_y
    if final_dx != 0 or final_dy != 0:
        deltas.append((final_dx, final_dy))

    return deltas

# ==============================================================================
# 🛡️ [다중 피코 호환 안티치트 게이트키퍼] 파섹의 1ms 광클을 인간 근육 속도로 강제 보정!
# ==============================================================================
hw_release_times = {}
hw_down_times = {}
hw_limits_lock = threading.Lock()

def enforce_physical_interval(p_serial, dev_type, code):
    """ DOWN 신호 전, 물리적 연타 쿨타임(간격) 강제 검사 """
    if not p_serial: return
    sid = id(p_serial)
    with hw_limits_lock:
        if sid not in hw_release_times:
            hw_release_times[sid] = {"MOUSE": {}, "KEYBOARD": {}}
        last_up = hw_release_times[sid][dev_type].get(code, 0.0)
    elapsed = time.perf_counter() - last_up
    limit = max(0.065, random.gauss(0.085, 0.015)) if dev_type == "MOUSE" else max(0.055, random.gauss(0.075, 0.015))
    if elapsed < limit: time.sleep(limit - elapsed)

def enforce_human_hold_time(p_serial, dev_type, code):
    """ UP 신호 전, 스위치가 눌려있던 체공 시간(Hold Time) 검사 """
    if not p_serial: return
    sid = id(p_serial)
    with hw_limits_lock:
        if sid not in hw_down_times:
            hw_down_times[sid] = {"MOUSE": {}, "KEYBOARD": {}}
        last_down = hw_down_times[sid][dev_type].get(code, 0.0)
    elapsed = time.perf_counter() - last_down
    min_hold = max(0.045, random.gauss(0.065, 0.015)) if dev_type == "MOUSE" else max(0.040, random.gauss(0.060, 0.015))
    if elapsed < min_hold: time.sleep(min_hold - elapsed)

def record_physical_down(p_serial, dev_type, code):
    if not p_serial: return
    sid = id(p_serial)
    with hw_limits_lock:
        if sid not in hw_down_times:
            hw_down_times[sid] = {"MOUSE": {}, "KEYBOARD": {}}
        hw_down_times[sid][dev_type][code] = time.perf_counter()

def record_physical_release(p_serial, dev_type, code):
    if not p_serial: return
    sid = id(p_serial)
    with hw_limits_lock:
        if sid not in hw_release_times:
            hw_release_times[sid] = {"MOUSE": {}, "KEYBOARD": {}}
        hw_release_times[sid][dev_type][code] = time.perf_counter()

def send_macro_buffer(p_serial, p_lock, deltas, key):
    if not p_serial or not deltas: return
    chunk_size = 10
    next_tick = time.perf_counter()
    
    for i in range(0, len(deltas), chunk_size):
        if active_manual_target == key or ai_states[key].get("is_paused") or ai_states[key].get("abort_macro", False): 
            try:
                last_dx = deltas[max(0, i-1)][0] if i > 0 else deltas[0][0]
                last_dy = deltas[max(0, i-1)][1] if i > 0 else deltas[0][1]
                ai_states[key]["skid_dx"] = last_dx
                ai_states[key]["skid_dy"] = last_dy
                
                if key in ai_states:
                    ai_states[key]["cursor_lost"] = True 
            except: pass
            break
        chunk = deltas[i:i+chunk_size]
        packet = bytearray([0xAA, len(chunk) * 2]) 
        for dx, dy in chunk: 
            packet.extend(struct.pack('bb', max(-127, min(127, dx)), max(-127, min(127, dy))))
            log_intercept(p_serial, action="AUTO_MOVE", dx=dx, dy=dy)

        packet.append(0xFE) 
        
        with p_lock: 
            try: p_serial.write(packet)
            except: pass
            
        chunk_delay = (len(chunk) * POLLING_RATE) - 0.005 
        if chunk_delay < 0: chunk_delay = 0
        now = time.perf_counter()
        if now > next_tick: next_tick = now + chunk_delay
        else: next_tick += chunk_delay
        while True:
            rem = next_tick - time.perf_counter()
            if rem <= 0: break
            if rem > 0.002: time.sleep(0.001)
            elif rem > 0.0005: time.sleep(0)  

def send_super_packet_buffer(p_serial, p_lock, deltas, key):
    """🚀 [0ms 동기화 엔진] 이동(X,Y)과 클릭 상태를 3바이트(0xB1) 캡슐로 묶어 전송"""
    if not p_serial or not deltas: return
    chunk_size = 10 
    next_tick = time.perf_counter()
    
    for i in range(0, len(deltas), chunk_size):
        if active_manual_target == key or ai_states[key].get("is_paused") or ai_states[key].get("abort_macro", False): 
            try:
                last_dx = deltas[max(0, i-1)][0] if i > 0 else deltas[0][0]
                last_dy = deltas[max(0, i-1)][1] if i > 0 else deltas[0][1]
                ai_states[key]["skid_dx"] = last_dx
                ai_states[key]["skid_dy"] = last_dy
                
                if key in ai_states:
                    ai_states[key]["cursor_lost"] = True
            except: pass
            break
            
        chunk = deltas[i:i+chunk_size]
        
        if any(btn == 1 for _, _, btn in chunk):
            enforce_physical_interval(p_serial, "MOUSE", 1)
            next_tick = time.perf_counter() 
            
        packet = bytearray([0xB1, len(chunk) * 3]) 
        for dx, dy, btn in chunk: 
            packet.extend(struct.pack('bbb', max(-127, min(127, int(dx))), max(-127, min(127, int(dy))), int(btn)))
            btn_str = "L_DOWN" if btn == 1 else "L_UP" if btn == 2 else "NONE"
            log_intercept(p_serial, action="AUTO_DRAG_ATTACK", dx=dx, dy=dy, click_val=btn_str)

        packet.append(0xFE) 
        
        with p_lock: 
            try: p_serial.write(packet)
            except: pass
            
        if any(btn == 2 for _, _, btn in chunk):
            record_physical_release(p_serial, "MOUSE", 1)
            
        chunk_delay = (len(chunk) * POLLING_RATE) - 0.005 
        if chunk_delay < 0: chunk_delay = 0
        now = time.perf_counter()
        if now > next_tick: next_tick = now + chunk_delay
        else: next_tick += chunk_delay
        while True:
            rem = next_tick - time.perf_counter()
            if rem <= 0: break
            if rem > 0.002: time.sleep(0.001)
            elif rem > 0.0005: time.sleep(0)

def send_immediate_delta(p_serial, p_lock, dx, dy):
    if not p_serial: return
    # 📸 [CCTV] 수동 마우스 이동 팩트 가로채기
    log_intercept(p_serial, action="MANUAL_MOVE", dx=dx, dy=dy)

    packet = bytearray([0xAB, 2]); packet.extend(struct.pack('bb', max(-127, min(127, dx)), max(-127, min(127, dy)))); packet.append(0xFE)
    with p_lock:
        try: p_serial.write(packet)
        except: pass

def send_mouse_click(p_serial, p_lock, button, state, is_manual=False): # 🚀 is_manual 파라미터 추가
    if not p_serial: return
    
    # 👑 [게이트키퍼 발동] 마우스 누르기(1) 전, 인터벌 무조건 검사!
    if state == 1 and not is_manual:
        enforce_physical_interval(p_serial, "MOUSE", button)

    # 📸 [CCTV] 단일 마우스 클릭 가로채기 (휠 클릭 로깅 지원)
    btn_str = f"{'L' if button==1 else 'R' if button==2 else 'M'}_{'DOWN' if state==1 else 'UP'}"
    log_intercept(p_serial, action="CLICK", click_val=btn_str)

    # ====================================================================
    # 👑 [형님 기획 업그레이드] 스위치를 누르는 순간(DOWN) 15% 확률로 가우시안 장력 튕김 주입!
    # 🚨 [휠 클릭 방어막] 버프 시전용 휠 클릭(3번)은 안정성을 위해 튕김(Jitter) 절대 금지!
    # ====================================================================
    if state == 1 and not is_manual and button != 3 and random.random() < 0.15:
        jx = int(round(random.gauss(0, 1.5)))
        jy = int(round(random.gauss(0, 1.5)))
        
        if jx == 0 and jy == 0:
            if random.random() > 0.5: jx = 1 if random.random() > 0.5 else -1
            else: jy = 1 if random.random() > 0.5 else -1
            
        send_immediate_delta(p_serial, p_lock, jx, jy)
        
        target_key = None
        for k, s in picos.items():
            if s is p_serial:
                target_key = k
                break
        if target_key and target_key in ai_states:
            ai_states[target_key]["cursor_pos"][0] += jx
            ai_states[target_key]["cursor_pos"][1] += jy

    with p_lock: 
        try: p_serial.write(bytearray([0xAC, 2, button, state, 0xFE]))
        except: pass
        
    if state == 0:
        record_physical_release(p_serial, "MOUSE", button)


# 🚀 [보안핵심] 하드웨어 키 상태를 전역으로 기억하는 딕셔너리 (형님의 안티치트 방어막 완벽 유지!)
hw_key_states = {}

def reset_hw_key_states(p_serial):
    """🚨 [기억상실증 치료 백신] 0xFF(하드웨어 리셋) 신호를 쏠 때, 파이썬의 뇌피셜 기억 장부도 함께 찢어버립니다!"""
    if not p_serial: return
    sid = id(p_serial)
    with hw_limits_lock:
        if sid in hw_key_states:
            hw_key_states[sid].clear()


def send_keyboard_key(p_serial, p_lock, keycode, state, is_manual=False): # 🚀 is_manual 파라미터 추가!
    if not p_serial: return
    
    # 🚨 [형님 기획 완벽 보존] 안티치트 로그 수집(연속 DOWN 등)을 막기 위한 절대 방어막!
    sid = id(p_serial)
    with hw_limits_lock:
        if sid not in hw_key_states:
            hw_key_states[sid] = {}
        last_state = hw_key_states[sid].get(keycode, 0)
        
        if last_state == state:
            if state == 1:
                # 🛡️ [자가 치유 엔진] 파이썬은 눌려있다고 착각하는데 실제론 안 눌려있는 '디싱크' 씹힘 상태!
                # 안티치트에게 중복 DOWN 로그를 남기지 않기 위해, 비밀리에 UP(0) 신호를 먼저 보내어 
                # "정상적으로 뗐다가 다시 누르는" 완벽한 물리적 패턴을 창조하여 해결합니다!
                try: p_serial.write(bytearray([0xAE, 1, keycode, 0xFE]))
                except: pass
            else:
                return # 중복 UP(0) 신호는 그냥 쿨하게 무시 (로그 안 남음)
                
        hw_key_states[sid][keycode] = state

    # 👑 [수동 모드 프리패스] 수동일 때는 키보드 물리적 딜레이(80ms) 스킵!
    if state == 1 and not is_manual:
        enforce_physical_interval(p_serial, "KEYBOARD", keycode)

    state_str = "DOWN" if state == 1 else "UP"
    log_intercept(p_serial, action="KEYBOARD", key_val=f"K{keycode}_{state_str}")

    with p_lock: 
        try: p_serial.write(bytearray([0xAD if state == 1 else 0xAE, 1, keycode, 0xFE]))
        except: pass
        
    if state == 0:
        record_physical_release(p_serial, "KEYBOARD", keycode)

def send_mouse_scroll(p_serial, p_lock, wheel_delta):
    if not p_serial: return
    # 📸 [CCTV] 마우스 휠 가로채기
    log_intercept(p_serial, action="SCROLL", click_val=f"WHL_{wheel_delta}")

    packet = bytearray([0xB0, 1]); packet.extend(struct.pack('b', max(-127, min(127, wheel_delta)))); packet.append(0xFE)
    with p_lock: 
        try: p_serial.write(packet)
        except: pass

def safe_sleep_interrupt(q, key, duration):
    end_time = time.perf_counter() + duration
    while time.perf_counter() < end_time:
        if active_manual_target == key or ai_states[key].get("is_paused") or ai_states[key].get("abort_macro", False): return False
        with q.mutex:
            for item in q.queue:
                if item.get("action") in ["ESCAPE", "TELEPORT", "HEAL", "POTION", "ANTIDOTE"]: return False 
        time.sleep(0.02)
    return True

def pico_worker_thread(key):
    # 🚀 [수술 2] 루프 밖에서 p_serial을 고정(캐싱)하던 족쇄 삭제!
    q, p_lock = pico_queues[key], pico_locks[key]
    def h_sleep(a, b):
        target_time = time.perf_counter() + g_time(a, b, key)
        while True:
            rem = target_time - time.perf_counter()
            if rem <= 0 or ai_states[key].get("abort_macro", False): break
            if rem > 0.002: time.sleep(0.001)
            elif rem > 0.0005: time.sleep(0)
            else: pass

    def get_key_bounds(keycode):
            """형님 최적화: 파지 위치별 과하지 않은 편차의 기본 체공 시간"""

            if keycode in [KEY_ANTIDOTE, KEY_POTION]:
                return 0.045, 0.055 
            elif keycode in [194, 195, 196, 197]:       # F1~F4
                return 0.065, 0.075
            elif keycode in [198, 199, 200, 201, KEY_HEAL]: # F5~F8 (힐은 마법이라 그대로 둠)
                return 0.067, 0.078
            else:                                     # F9~F12, ESC, Ctrl 등
                return 0.070, 0.082

    def k_tap(kcode):
            """키보드 누름/뗌과 생체역학 딜레이를 한 줄로 완벽히 처리하는 스마트 함수"""
            # 🚀 [수술 2] 실행 시점의 최신 포트를 딕셔너리에서 실시간으로 뽑아옵니다!
            p_serial = picos.get(key)
            if not p_serial: return
            k_min, k_max = get_key_bounds(kcode)
            send_keyboard_key(p_serial, p_lock, kcode, 1)
            h_sleep(k_min, k_max)
            send_keyboard_key(p_serial, p_lock, kcode, 0)

    while True:
        try:
            cmd = q.get(timeout=0.1)
            
            # 🚀 [수술 2] 무한 루프를 돌 때마다 가장 '최신' 피코 객체를 꺼내옵니다!
            p_serial = picos.get(key)
            
            if key in ai_states: 
                ai_states[key]["abort_macro"] = False
                ai_states[key]["hw_busy"] = True  # 🚨 [센서 ON] 하드웨어가 물리적으로 움직이기 시작함!
            
            if active_manual_target == key or not p_serial: 
                if key in ai_states and q.empty(): ai_states[key]["hw_busy"] = False
                continue
            action = cmd.get("action")

            # 🛡️ [바탕화면 엣지(F1) 실행 원천 차단] 인증 모드(CERTI_) 중에는 잔여 인게임 단축키를 하드웨어 직전에서 폐기!
            curr_fsm_hw = str(ai_states.get(key, {}).get("target_fsm", ""))
            if curr_fsm_hw.startswith("CERTI_"):
                if action in ["ESCAPE", "TELEPORT", "HEAL", "POTION", "TAKE_BLUE_POTION", "ANTIDOTE", "BUFF_COMBO", "SWEEP_START", "TRASH_DELETE"]:
                    dprint(key, f"🛡️ [인증모드 키 차단] 바탕화면 오작동 방지를 위해 잔여 인게임 명령({action})을 폐기합니다.")
                    if key in ai_states and q.empty(): ai_states[key]["hw_busy"] = False
                    continue
                elif action == "HOLD_KEY" and cmd.get("keycode") in [194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205]:
                    # 군주 인게임 접속 완료(CERTI_WAIT_DRAGON) 직후 F1 단축창을 여는 경우만 허용
                    if not (cmd.get("keycode") == KEY_F1 and curr_fsm_hw in ["CERTI_WAIT_DRAGON", "CERTI_DRAGON_CLICK_HASTE", "CERTI_DRAGON_FINISH"]):
                        dprint(key, f"🛡️ [인증모드 F키 차단] 바탕화면 엣지(도움말) 실행 방지를 위해 F키(keycode:{cmd.get('keycode')}) 입력을 폐기합니다.")
                        if key in ai_states and q.empty(): ai_states[key]["hw_busy"] = False
                        continue
            
            if action not in ["HOVER", "SINGLE_ATTACK", "ATTACK", "DRAG_ATTACK", "BODY_TO_MIND", "CUSTOM_MOVE", "POTION", "FORCE_RELEASE", "TRASH_DELETE"]:
                dprint(key, f"⚡ [HW 전송] 매크로 실행: {action}")
            
            # 👑 [안전핀 발동] 하드웨어 큐 소각(0xFF)과 속도 감응형 ABS 브레이크를 '단일 캡슐'로 융합 전송! (0ms 갭리스)
            if action == "FORCE_RELEASE":
                # 🚀 [쉬프트/컨트롤 홀딩 버그 완벽 수술] 
                # 큐가 폭파될 때, 파이썬의 안티치트 뇌피셜 장부를 무시하고 피코(하드웨어)에 다이렉트로 UP(0xAE) 신호를 꽂아버립니다!
                with p_lock:
                    try: 
                        p_serial.write(bytearray([0xAE, 1, 129, 0xFE])) # 129: Shift 강제 해제
                        p_serial.write(bytearray([0xAE, 1, 128, 0xFE])) # 128: Ctrl 강제 해제
                    except: pass
                    
                skid_dx = ai_states[key].get("skid_dx", 0)
                skid_dy = ai_states[key].get("skid_dy", 0)
                
                # 🚀 [형님 맞춤형 최적화] 진짜 현재 속도(픽셀/프레임)를 계산!
                skid_speed = math.hypot(skid_dx, skid_dy)
                
                
                # 🟢 수정된 코드: 0xFF 제거! (잔여 큐를 살려두고 ABS 브레이크만 부드럽게 전송)
                fusion_packet = bytearray() 
                # =========================================================
                
                # 👇 아래부터 시작되는 형님의 ABS 브레이크(J-Curve) 로직은 100% 그대로 유지!
                if skid_speed >= 3.0:
                    skid_frames = random.randint(4, 5) 
                    fusion_packet.extend([0xB1, skid_frames * 3])
                    # ... (이하 동일) ...
                    
                    cx, cy = float(skid_dx), float(skid_dy)
                    for f_idx in range(skid_frames):
                        # 🚨 [3번 결함 수술 완료] X축과 Y축의 마찰 계수를 완전히 분리하여 완벽한 수학적 직선 감소(Mathematical Skidding) 방지!
                        friction_x = random.uniform(0.40, 0.70)
                        friction_y = random.uniform(0.40, 0.70)
                        cx *= friction_x 
                        cy *= friction_y
                        # 🚀 [추가] 브레이킹 시 패드 동마찰력으로 인한 덜컹거림 주입 (수학적 지수 감소 파괴)
                        cx += random.gauss(0, 0.6)
                        cy += random.gauss(0, 0.6)
                        
                        ix, iy = int(round(cx)), int(round(cy))
                        if ix == 0 and abs(cx) > 0.1: ix = 1 if cx > 0 else -1
                        if iy == 0 and abs(cy) > 0.1: iy = 1 if cy > 0 else -1
                        
                        # 🚀 [디싱크 영구 소각 3] 급브레이크 잡으면서 관성으로 미끄러진 픽셀도 뇌피셜에 누적 기록!
                        if key in ai_states:
                            ai_states[key]["cursor_pos"][0] = max(0, min(800, ai_states[key]["cursor_pos"][0] + ix))
                            ai_states[key]["cursor_pos"][1] = max(0, min(600, ai_states[key]["cursor_pos"][1] + iy))
                            
                        btn_cmd = 2 if f_idx == skid_frames - 1 else 0
                        fusion_packet.extend(struct.pack('bbb', max(-127, min(127, ix)), max(-127, min(127, iy)), btn_cmd))
                        
                        # 💥 [CCTV] 큐 폭파 직후 관성으로 미끄러지는 팩트 궤적 로깅!
                        btn_str = "L_UP" if btn_cmd == 2 else "NONE"
                        log_intercept(p_serial, action="AUTO_BRAKE_SKID", dx=ix, dy=iy, click_val=btn_str)

                    fusion_packet.append(0xFE)
                else:
                    # 🚀 [감속/정지 구간] 이미 멈추기 직전이면 억지 브레이크 생략. 깔끔하게 클릭 해제(0xAC)만 융합!
                    fusion_packet.extend([0xAC, 2, 1, 0, 0xFE])
                    # 💥 [CCTV] 멈춰있는 상태에서 클릭 떼기만 로깅
                    log_intercept(p_serial, action="AUTO_BRAKE_STOP", click_val="L_UP")

                # 🚀 조립된 캡슐을 통신 병목 없이 피코 보드로 한 방에 발사!
                with p_lock:
                    try: p_serial.write(fusion_packet)
                    except: pass
                    
                # 👑 [게이트키퍼 기록] 비상 브레이크는 물리적으로 마우스를 무조건 떼버리므로 뗀 시간 강제 각인!
                record_physical_release(p_serial, "MOUSE", 1)
                
                ai_states[key]["skid_dx"], ai_states[key]["skid_dy"] = 0, 0
                h_sleep(0.065, 0.085) # 펌웨어 락 해제 완벽 대기
                continue
            
            if action == "ESCAPE":
                k_tap(KEY_F1)
                h_sleep(0.15, 0.25)
                for _ in range(2):
                    k_tap(KEY_ESCAPE)
                    h_sleep(0.25, 0.35)
            
            elif action == "TELEPORT":
                k_tap(KEY_F1)
                h_sleep(0.15, 0.25)
                k_tap(KEY_F11)
                h_sleep(0.25, 0.35)

            elif action == "HEAL":
                k_tap(KEY_HEAL)
                h_sleep(0.09, 0.15)
                k_tap(KEY_HEAL)
            
            elif action == "POTION":
                k_tap(KEY_POTION)

            elif action == "WHEEL_CLICK":
                # 🚀 [제자리 캐스팅] 캐릭터가 뛰어가지 않게 마우스 휠(3번 버튼)로 클릭!
                h_sleep(0.04, 0.05) 
                send_mouse_click(p_serial, p_lock, 3, 1)
                
                # 🚀 [형님 오더 완벽 적용] 휠클릭 체공 시간을 0.12 ~ 0.25초 (가우스 난수)로 묵직하게 연장하여 씹힘 원천 차단!
                h_sleep(0.12, 0.25)
                
                send_mouse_click(p_serial, p_lock, 3, 0)

            # ====================================================================
            # 🛑 [뼈대 1] 인간화 100% 적용! 비동기(Asynchronous) Shift + Click 급제동 엔진
            # ====================================================================
            elif action == "SHIFT_CLICK_BRAKE":
                # 1. 왼손: Shift(129) 누름
                send_keyboard_key(p_serial, p_lock, 129, 1)
                
                # 2. 뇌 딜레이: Shift 누르고 오른손 클릭까지 (0.04 ~ 0.06초)
                h_sleep(0.04, 0.06)
                
                # 3. 오른손: 제자리 좌클릭(1) 꾹
                send_mouse_click(p_serial, p_lock, 1, 1)
                
                # 4. 손가락 체공 시간 (0.07, 0.11)
                h_sleep(0.07, 0.11)
                
                # 5. 오른손: 좌클릭(1) 뗌 (여기까지만 큐를 점유하고 즉시 다음 큐인 HOVER를 열어줌!)
                send_mouse_click(p_serial, p_lock, 1, 0)
                
                # 🚀 6. [형님 기획: 왼손/오른손 비동기 분리] 
                # Shift 키를 떼는 동작은 최대 0.6초까지 길게 유지하도록 백그라운드 타이머에게 던져버립니다!
                shift_release_delay = g_val(0.05, 0.60)
                def async_release_shift(s_serial, s_lock):
                    time.sleep(shift_release_delay)
                    if s_serial:
                        try: send_keyboard_key(s_serial, s_lock, 129, 0)
                        except: pass
                threading.Thread(target=async_release_shift, args=(p_serial, p_lock), daemon=True).start()
                
                # 7. 오른손은 클릭 직후 숨만 살짝 고르고 (0.04~0.09초) 곧바로 다음 명령(마우스 날리기)을 실행합니다!
                # ➔ Shift가 아직 안 떼진 상태에서 마우스가 날아가는 완벽한 오버랩 컨트롤이 발동됨!
                h_sleep(0.04, 0.09)

            # 🚀 [단축키 충돌 해결] 사냥용 바디투마인드 삭제하고 F7 파랭이 복용으로 완벽 교체!
            elif action == "TAKE_BLUE_POTION":
                dprint(key, "💊 [스마트 자원관리] 결손치 임계점 돌파! 파랭이(F7)를 복용합니다.")
                k_tap(KEY_F7)

            elif action == "ANTIDOTE":
                is_spell = cmd.get("is_spell", False)
                k_tap(KEY_ANTIDOTE)
                if is_spell:
                    h_sleep(0.09, 0.15)
                    k_tap(KEY_ANTIDOTE)

            elif action == "PVP_OFF":
                # 🚀 새끼손가락의 둔탁하고 묵직한 타건 속도로 개조
                k_tap(128) # Ctrl
                h_sleep(0.12, 0.18) 
                k_tap(128)

            elif action == "HOLD_KEY":
                kcode = cmd.get("keycode")
                if kcode: send_keyboard_key(p_serial, p_lock, kcode, 1); h_sleep(cmd.get("duration", 0.3), cmd.get("duration", 0.3) * 1.2); send_keyboard_key(p_serial, p_lock, kcode, 0)

            elif action == "SHIFT_SPACE":
                send_keyboard_key(p_serial, p_lock, 129, 1)
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 32, 1)  
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 32, 0)  
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 129, 0) 
                h_sleep(0.05, 0.1)

            # 🚀 [수술 3] 형님의 기획! 마우스 휠을 아래로 굴리는 하드웨어 액션 (함수명 완벽 적용!)
            elif action == "MOUSE_WHEEL":
                amount = cmd.get("amount", -1) # -1: 휠을 아래로 내림
                try:
                    send_mouse_scroll(p_serial, p_lock, amount) # 👈 형님이 찾아내신 찐 휠 함수 탑재!
                    h_sleep(0.04, 0.08)
                except Exception: pass

            elif action == "WAIT":
                h_sleep(cmd.get("delay_min", 0.09), cmd.get("delay_max", 0.17))

            elif action == "HOME_MACRO":
                # 💡 Win+D를 누르기 직전 현재 화면에 바탕화면 아이콘 3종(1.png, 13.png, sub.png)이 모두 보이는지 팩트 체크!
                def _count_desktop_icons():
                    scr_now = latest_frames.get(key)
                    if scr_now is None:
                        return 0, 3
                    icon_groups = [
                        ["qq/certi/1.png"],
                        ["qq/certi/13.png"],
                        ["qq/certi/sub.png", "qq/sub.png"]
                    ]
                    vis_cnt = 0
                    avail_cnt = 0
                    for cand_paths in icon_groups:
                        actual_path = next((p for p in cand_paths if os.path.exists(p)), None)
                        if not actual_path:
                            continue
                        avail_cnt += 1
                        if actual_path not in loaded_models:
                            try:
                                with open(actual_path, "rb") as _f:
                                    _arr = np.asarray(bytearray(_f.read()), dtype=np.uint8)
                                _bgra = cv2.imdecode(_arr, cv2.IMREAD_UNCHANGED)
                                if _bgra is not None:
                                    if len(_bgra.shape) == 3 and _bgra.shape[2] == 4:
                                        loaded_models[actual_path] = {"color": _bgra[:, :, :3], "mask": _bgra[:, :, 3]}
                                    else:
                                        loaded_models[actual_path] = {"color": _bgra[:, :, :3] if len(_bgra.shape) == 3 else _bgra, "mask": None}
                            except Exception:
                                loaded_models[actual_path] = None
                        _td = loaded_models.get(actual_path)
                        if _td and _td["color"] is not None:
                            try:
                                if _td["mask"] is not None:
                                    _res = cv2.matchTemplate(scr_now, _td["color"], cv2.TM_CCORR_NORMED, mask=cv2.merge([_td["mask"]]*3))
                                else:
                                    _res = cv2.matchTemplate(scr_now, _td["color"], cv2.TM_CCOEFF_NORMED)
                                if cv2.minMaxLoc(_res)[1] >= 0.82:
                                    vis_cnt += 1
                            except Exception:
                                pass
                    return vis_cnt, max(1, avail_cnt)

                visible_icons, target_icon_cnt = _count_desktop_icons()

                if 0 < visible_icons < target_icon_cnt:
                    cur_cx, cur_cy = ai_states.get(key, {}).get("cursor_pos", [400, 300])
                    safe_tx, safe_ty = int(round(g_val(580, 680))), int(round(g_val(280, 380)))
                    send_macro_buffer(p_serial, p_lock, generate_human_deltas(safe_tx - cur_cx, safe_ty - cur_cy, duration=0.18, behavior="CERTI", key=key), key)
                    if key in ai_states:
                        ai_states[key]["cursor_pos"] = [safe_tx, safe_ty]
                    dprint(key, f"👀 [바탕화면 커서 치우기] 아이콘 {visible_icons}/{target_icon_cnt}개 감지 ➔ 커서 가림 확인을 위해 마우스를 옆으로 치웁니다.")
                    h_sleep(0.30, 0.40)
                    visible_icons, target_icon_cnt = _count_desktop_icons()

                if visible_icons >= target_icon_cnt:
                    dprint(key, f"🖥️ [바탕화면 확인 완료] 1.png / 13.png / sub.png ({visible_icons}개) 모두 확인됨! Win+D 입력을 생략합니다.")
                    h_sleep(0.15, 0.25)
                else:
                    dprint(key, f"🖥️ [바탕화면 전환] 아이콘 {visible_icons}/{target_icon_cnt}개만 감지됨 ➔ Win+D를 눌러 창을 내립니다!")
                    send_keyboard_key(p_serial, p_lock, 131, 1) # Win키 DOWN
                    h_sleep(0.04, 0.08)
                    send_keyboard_key(p_serial, p_lock, 100, 1) # 'D'키 DOWN
                    h_sleep(0.07, 0.12)
                    send_keyboard_key(p_serial, p_lock, 100, 0) # 'D'키 UP
                    h_sleep(0.04, 0.08)
                    send_keyboard_key(p_serial, p_lock, 131, 0) # Win키 UP
                    h_sleep(0.5, 0.8)

            elif action == "CERTI_CLICK":
                is_double = cmd.get("double", False)
                h_sleep(0.06, 0.12)
                # 💡 [인간화] 마우스 클릭 체공(Hold) 시간을 50~125ms 범위로 넓게 분산 (15% 튕김 방지를 위해 is_manual=True 유지)
                send_mouse_click(p_serial, p_lock, 1, 1, is_manual=True)
                h_sleep(0.050, 0.125)
                send_mouse_click(p_serial, p_lock, 1, 0, is_manual=True)
                if is_double:
                    h_sleep(0.055, 0.105)
                    send_mouse_click(p_serial, p_lock, 1, 1, is_manual=True)
                    h_sleep(0.048, 0.110)
                    send_mouse_click(p_serial, p_lock, 1, 0, is_manual=True)
                h_sleep(0.18, 0.32)

            elif action == "CLOSE_TAB":
                send_keyboard_key(p_serial, p_lock, 128, 1) # Ctrl DOWN
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 129, 1) # Shift DOWN
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 119, 1) # 'w' DOWN
                h_sleep(0.06, 0.10)
                send_keyboard_key(p_serial, p_lock, 119, 0) # 'w' UP
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 129, 0) # Shift UP
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 128, 0) # Ctrl UP
                h_sleep(0.60, 0.85)

            elif action == "OPEN_TASKMGR":
                # 미니PC 작업 관리자 즉시 호출 (Ctrl + Shift + Esc)
                send_keyboard_key(p_serial, p_lock, 128, 1) # Ctrl DOWN
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 129, 1) # Shift DOWN
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 177, 1) # Esc DOWN
                h_sleep(0.06, 0.11)
                send_keyboard_key(p_serial, p_lock, 177, 0) # Esc UP
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 129, 0) # Shift UP
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 128, 0) # Ctrl UP
                h_sleep(0.85, 1.15)

            elif action == "TASKMGR_DEL":
                # 작업 관리자에서 선택된 리니지 프로세스 강제 종료 (Delete 키)
                h_sleep(0.10, 0.18)
                send_keyboard_key(p_serial, p_lock, 212, 1) # Delete DOWN
                h_sleep(0.06, 0.11)
                send_keyboard_key(p_serial, p_lock, 212, 0) # Delete UP
                h_sleep(0.25, 0.40)

            elif action == "CLOSE_TASKMGR":
                # 작업 관리자 창 닫기 (Alt + F4)
                send_keyboard_key(p_serial, p_lock, 130, 1) # Alt DOWN
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 197, 1) # F4 DOWN
                h_sleep(0.06, 0.10)
                send_keyboard_key(p_serial, p_lock, 197, 0) # F4 UP
                h_sleep(0.04, 0.08)
                send_keyboard_key(p_serial, p_lock, 130, 0) # Alt UP
                h_sleep(0.35, 0.55)

            elif action == "UI_DRAG":
                dx, dy = cmd.get("dx", 0), cmd.get("dy", 0)
                send_mouse_click(p_serial, p_lock, 1, 1)
                h_sleep(0.15, 0.25)
                payload = list(generate_human_deltas(dx, dy, behavior="SHOP", key=key))
                super_payload = [(px, py, 0) for px, py in payload]
                send_super_packet_buffer(p_serial, p_lock, super_payload, key)
                h_sleep(0.15, 0.25)
                send_mouse_click(p_serial, p_lock, 1, 0)
                if key in ai_states:
                    ai_states[key]["cursor_pos"][0] += (sum(p[0] for p in payload) - dx)
                    ai_states[key]["cursor_pos"][1] += (sum(p[1] for p in payload) - dy)

            elif action == "TYPE_STRING":
                text_val = str(cmd.get("text", ""))
                clear_first = cmd.get("clear_first", False)
                press_enter = cmd.get("press_enter", False)

                if clear_first:
                    send_keyboard_key(p_serial, p_lock, 128, 1)
                    h_sleep(0.04, 0.08)
                    send_keyboard_key(p_serial, p_lock, 97, 1)
                    h_sleep(0.05, 0.09)
                    send_keyboard_key(p_serial, p_lock, 97, 0)
                    h_sleep(0.04, 0.08)
                    send_keyboard_key(p_serial, p_lock, 128, 0)
                    h_sleep(0.08, 0.14)
                    k_tap(178)
                    h_sleep(0.10, 0.18)

                shift_char_map = {
                    '!': ord('1'), '@': ord('2'), '#': ord('3'), '$': ord('4'), '%': ord('5'),
                    '^': ord('6'), '&': ord('7'), '*': ord('8'), '(': ord('9'), ')': ord('0'),
                    '_': ord('-'), '+': ord('='), '~': ord('`'), ':': ord(';'), '"': ord("'"),
                    '<': ord(','), '>': ord('.'), '?': ord('/'), '{': ord('['), '}': ord(']'), '|': ord('\\')
                }

                for ch in text_val:
                    if active_manual_target == key or ai_states[key].get("is_paused") or ai_states[key].get("abort_macro", False):
                        break
                    if ch == '\n':
                        k_tap(176)
                        h_sleep(0.05, 0.12)
                    elif ch in shift_char_map:
                        base_k = shift_char_map[ch]
                        send_keyboard_key(p_serial, p_lock, 129, 1)
                        h_sleep(0.04, 0.08)
                        send_keyboard_key(p_serial, p_lock, base_k, 1)
                        h_sleep(0.05, 0.09)
                        send_keyboard_key(p_serial, p_lock, base_k, 0)
                        h_sleep(0.04, 0.08)
                        send_keyboard_key(p_serial, p_lock, 129, 0)
                        h_sleep(0.05, 0.12)
                    elif 'A' <= ch <= 'Z':
                        kcode = ord(ch.lower())
                        send_keyboard_key(p_serial, p_lock, 129, 1)
                        h_sleep(0.04, 0.08)
                        send_keyboard_key(p_serial, p_lock, kcode, 1)
                        h_sleep(0.05, 0.09)
                        send_keyboard_key(p_serial, p_lock, kcode, 0)
                        h_sleep(0.04, 0.08)
                        send_keyboard_key(p_serial, p_lock, 129, 0)
                        h_sleep(0.05, 0.12)
                    else:
                        k_tap(ord(ch))
                        h_sleep(0.05, 0.12)

                if press_enter:
                    h_sleep(0.18, 0.30)
                    k_tap(176)
                    h_sleep(0.20, 0.35)

            elif action == "TRASH_DELETE":
                # 1. 아이템 좌클릭 선택 (근육 기억)
                send_mouse_click(p_serial, p_lock, 1, 1); h_sleep(0.06, 0.09); send_mouse_click(p_serial, p_lock, 1, 0)
                
                # 🧠 [근육 기억] 클릭 후 Delete 키로 손이 가는 시간 (관성대로 움직이므로 살짝 타이트하게)
                h_sleep(0.15, 0.25)
                
                # Delete (212) -> Y (121) -> Enter (176)
                send_keyboard_key(p_serial, p_lock, 212, 1); h_sleep(0.06, 0.09); send_keyboard_key(p_serial, p_lock, 212, 0)
                h_sleep(0.35, 0.60) 
                send_keyboard_key(p_serial, p_lock, 121, 1); h_sleep(0.06, 0.09); send_keyboard_key(p_serial, p_lock, 121, 0)
                h_sleep(0.15, 0.22)
                send_keyboard_key(p_serial, p_lock, 176, 1); h_sleep(0.06, 0.09); send_keyboard_key(p_serial, p_lock, 176, 0)
                h_sleep(0.30, 0.40)

            elif action == "SWEEP_START": send_keyboard_key(p_serial, p_lock, KEY_F4, 1)
            elif action == "SWEEP_STOP": send_keyboard_key(p_serial, p_lock, KEY_F4, 0)

            elif action == "BUFF_COMBO":
                buffs = cmd.get("buffs", [])
                page1, page2, page3 = [b for b in buffs if b["page"] == 1], [b for b in buffs if b["page"] == 2], [b for b in buffs if b["page"] == 3] 
                abort_buff = False 

                for b in page1:
                    if active_manual_target == key or ai_states[key].get("is_paused"): abort_buff = True; break
                    b_key, is_double = b["key"], b["double"]
                    k_tap(b_key)
                    if is_double: 
                        h_sleep(0.09, 0.15)
                        k_tap(b_key)
                    if not safe_sleep_interrupt(q, key, g_time(1.2, 1.5, key)): abort_buff = True; break
                    
                if page2 and not abort_buff and not (active_manual_target == key or ai_states[key].get("is_paused")):
                    # 🚀 [형님 오더 완벽 적용: F2 따닥!]
                    k_tap(KEY_F2)
                    h_sleep(0.05, 0.08)
                    k_tap(KEY_F2)
                    
                    if not safe_sleep_interrupt(q, key, g_time(0.6, 0.9, key)): abort_buff = True 
                    if not abort_buff:
                        for b in page2:
                            if active_manual_target == key or ai_states[key].get("is_paused"): break
                            b_key, is_double = b["key"], b["double"]
                            k_tap(b_key)
                            if is_double: 
                                h_sleep(0.09, 0.15)
                                k_tap(b_key)
                            if not safe_sleep_interrupt(q, key, g_time(1.2, 1.5, key)): break
                                
                if page3 and not abort_buff and not (active_manual_target == key or ai_states[key].get("is_paused")):
                    # 🚀 [형님 오더 완벽 적용: F3 따닥!]
                    k_tap(KEY_F3)
                    h_sleep(0.05, 0.08)
                    k_tap(KEY_F3)
                    
                    if not safe_sleep_interrupt(q, key, g_time(0.6, 0.9, key)): abort_buff = True 
                    if not abort_buff:
                        for b in page3:
                            if active_manual_target == key or ai_states[key].get("is_paused"): break
                            b_key, is_double = b["key"], b["double"]
                            k_tap(b_key)
                            if is_double: 
                                h_sleep(0.09, 0.15)
                                k_tap(b_key)
                            if not safe_sleep_interrupt(q, key, g_time(1.2, 1.5, key)): break
                    
                if (page2 or page3) and not (active_manual_target == key or ai_states[key].get("is_paused")):
                    # 🚀 [형님 오더 완벽 적용: F1 복귀 따닥!]
                    k_tap(KEY_F1)
                    h_sleep(0.05, 0.08)
                    k_tap(KEY_F1)
                    
                    h_sleep(0.5, 0.8)
                # 🚀 시전 중 생존/수동개입으로 캔슬 시 뇌에 보고!
                if key in ai_states: ai_states[key]["buff_aborted"] = abort_buff

            elif action == "HOVER":
                dx, dy = cmd.get("dx", 0), cmd.get("dy", 0)
                send_macro_buffer(p_serial, p_lock, generate_human_deltas(dx, dy, behavior="HOVER", key=key), key)

            # 👇👇👇 [여기서부터 새로 추가!] 👇👇👇
            elif action == "SHOP_HOVER":
                dx, dy = cmd.get("dx", 0), cmd.get("dy", 0)
                # 🚀 위에서 만든 20% 감속된 'SHOP' 행동 패턴을 적용해 마우스를 날립니다.
                send_macro_buffer(p_serial, p_lock, generate_human_deltas(dx, dy, behavior="SHOP", key=key), key)
            # 👆👆👆 ============================== 👆👆👆

            elif action == "SPECIAL_ACK":
                # 🚀 [형님의 마스터피스: 묶음 송신] 파섹 화면 지연 1차 대기 (0.21 -> 0.11 단축)
                h_sleep(0.11, 0.13)
                if key in ai_states:
                    ai_states[key]["special_ack_arrived"] = True

            elif action == "LOOT_ACK":
                h_sleep(0.11, 0.13)
                if key in ai_states:
                    ai_states[key]["loot_ack_arrived"] = True

            elif action == "CUSTOM_MOVE":
                deltas = cmd.get("deltas", [])
                if deltas: send_macro_buffer(p_serial, p_lock, deltas, key)

            elif action == "DRAG_ATTACK":
                # 🚨 [단축키 빠짐 완벽 수술 (하드웨어 락)] 
                # 파이썬 뇌가 미처 통제하지 못하고 큐에 들어온 공격 명령이라도,
                # 현재 커서 Y좌표가 440(단축키 구역)을 넘었다면 물리적 마우스 클릭(DOWN)을 절대 인가하지 않고 취소시킴!
                if key in ai_states and ai_states[key]["cursor_pos"][1] > 430:
                    dprint(key, "🛡️ [하드웨어 방어막] 커서가 단축키 구역에 있습니다! 스킬 빠짐 방지를 위해 드래그를 취소합니다.")
                    if key in ai_states:
                        ai_states[key]["is_attacking"] = False
                        ai_states[key]["target_fsm"] = "IDLE"
                    continue

                is_chain_kill = cmd.get("is_chain_kill", False) 
                
                if not is_chain_kill and random.random() < 0.03:
                    extra_clicks = random.randint(1, 2)
                    for _ in range(extra_clicks): send_mouse_click(p_serial, p_lock, 1, 1); h_sleep(0.04, 0.09); send_mouse_click(p_serial, p_lock, 1, 0); h_sleep(0.12, 0.20)
                
                if key in ai_states:
                    ai_states[key]["arrow_image"] = None 
                    ai_states[key]["arrow_fire_count"] = 0
                    ai_states[key]["arrow_is_firing"] = False
                    ai_states[key]["has_fired_arrow"] = False

                # 1. 몹 잡고 꾹 누르기
                send_mouse_click(p_serial, p_lock, 1, 1)
                
                # 🚀 [형님 세팅 완벽 적용] 무식한 2초 화살 대기 루프 소각! 드래그 전 텐션 모으기 딜레이
                h_sleep(0.28, 0.65)
                
                # 2. 전체 드래그 거리 세팅
                total_dx = cmd.get("drag_dx", int(g_val(100, 180)) * random.choice([-1, 1])) 
                total_dy = cmd.get("drag_dy", int(g_val(-80, 80)))
                
                slip_roll = random.random()
                cut_idx = None 
                
                # 🚨 [가속 폭주 방어] 윈도우 마우스 가속도를 막기 위해 이동 속도를 거리에 비례해 부드럽게 늦춤!
                dist = math.hypot(total_dx, total_dy)
                ideal_dur = 0.10 + 0.06 * math.log2((dist / 20.0) + 1.0)
                flick_dur = max(0.15, apply_human_variance(ideal_dur) * random.uniform(0.8, 1.1))
                
                if slip_roll < 0.74:
                    extra_dx = int(g_val(8, 30)) if total_dx > 0 else int(g_val(-30, -8))
                    extra_dy = int(g_val(5, 20)) if total_dy > 0 else int(g_val(-20, -5))
                    shoot_dx = total_dx + extra_dx
                    shoot_dy = total_dy + extra_dy
                    
                    payload = list(generate_human_deltas(shoot_dx, shoot_dy, duration=flick_dur, behavior="DRAG", key=key))
                    
                    original_dist = math.hypot(total_dx, total_dy)
                    accum_dx, accum_dy = 0.0, 0.0
                    
                    for i, (dx, dy) in enumerate(payload):
                        accum_dx += dx; accum_dy += dy
                        if math.hypot(accum_dx, accum_dy) >= original_dist:
                            cut_idx = i
                            break
                            
                else:
                    payload = list(generate_human_deltas(total_dx, total_dy, duration=flick_dur, behavior="DRAG", key=key))
                    main_len = len(payload)
                    cut_idx = int(main_len * random.uniform(0.90, 0.95)) if main_len > 0 else len(payload)
                    
                    if cut_idx >= 4:
                        start_idx = max(0, cut_idx - 4)
                        end_idx = cut_idx
                        raw_last_dx = sum([p[0] for p in payload[start_idx:end_idx]]) / float(end_idx - start_idx)
                        raw_last_dy = sum([p[1] for p in payload[start_idx:end_idx]]) / float(end_idx - start_idx)
                    else:
                        raw_last_dx, raw_last_dy = (total_dx * 0.1), (total_dy * 0.1)

                    if abs(raw_last_dx) < 1.0 and abs(raw_last_dy) < 1.0:
                        raw_last_dx = random.uniform(1.2, 2.0) if total_dx > 0 else random.uniform(-2.0, -1.2)
                        raw_last_dy = random.uniform(1.2, 2.0) if total_dy > 0 else random.uniform(-2.0, -1.2)

                    last_dx = raw_last_dx * 0.7  
                    last_dy = raw_last_dy * 0.7

                    spin_dir = random.choice([1, -1])
                    hook_frames = random.randint(6, 9)
                    accum_hx, accum_hy = 0.0, 0.0
                    
                    for i in range(hook_frames):
                        angle = (math.pi / hook_frames) * i * spin_dir
                        progress = i / float(hook_frames)
                        base_damping = 1.0 - progress
                        damping_x = max(0.0, base_damping + random.gauss(0, 0.1 * progress))
                        damping_y = max(0.0, base_damping + random.gauss(0, 0.1 * progress))
                        hook_dx = (last_dx * math.cos(angle) - last_dy * math.sin(angle)) * damping_x
                        hook_dy = (last_dx * math.sin(angle) + last_dy * math.cos(angle)) * damping_y
                        accum_hx += hook_dx; accum_hy += hook_dy
                        move_x, move_y = int(accum_hx), int(accum_hy)
                        if move_x != 0 or move_y != 0:
                            payload.append((move_x, move_y))
                            accum_hx -= move_x; accum_hy -= move_y

                if cut_idx is None or cut_idx >= len(payload): cut_idx = len(payload) - 1
                if cut_idx < 0: cut_idx = 0
                while cut_idx > 0 and payload[cut_idx][0] == 0 and payload[cut_idx][1] == 0: cut_idx -= 1

                super_payload = []
                actual_drag_dx = 0 # 🚀 [추가] 피코가 물리적으로 이동한 진짜 픽셀 누적기
                actual_drag_dy = 0 # 🚀 [추가]
                
                for i, (dx, dy) in enumerate(payload):
                    btn_cmd = 0
                    if i == cut_idx:
                        btn_cmd = 2 
                        if random.random() < 0.65:
                            dx += random.randint(2, 7) * random.choice([-1, 1])
                            dy += random.randint(1, 4) * random.choice([-1, 1])
                        if dx == 0 and dy == 0: dx = 1 if random.random() > 0.5 else -1
                    super_payload.append((dx, dy, btn_cmd))
                    
                    actual_drag_dx += dx # 🚀 누적
                    actual_drag_dy += dy # 🚀 누적
                    
                    # 💡 클릭을 뗀 이후의 궤적은 1~2프레임 관성만 주고 잘라냅니다. (오버슈트 방지)
                    if i > cut_idx + 2:
                        break

                send_super_packet_buffer(p_serial, p_lock, super_payload, key)


                if key in ai_states:
                    ai_states[key]["cursor_pos"][0] += (actual_drag_dx - total_dx)
                    ai_states[key]["cursor_pos"][1] += (actual_drag_dy - total_dy)

            elif action == "SINGLE_ATTACK":
                # 🚨 [단축키 빠짐 완벽 수술 (하드웨어 락)] 
                if key in ai_states and ai_states[key]["cursor_pos"][1] > 430:
                    dprint(key, "🛡️ [하드웨어 방어막] 커서가 단축키 구역에 있습니다! 잘못된 클릭 방지를 위해 취소합니다.")
                    continue
                    
                # 🚀 [인지 딜레이 백신] 마우스가 타겟에 도착한 후, 눈으로 확인하고 손가락을 까딱하는 60~120ms 강제 보장!
                h_sleep(0.04, 0.05) 
                send_mouse_click(p_serial, p_lock, 1, 1); h_sleep(0.055, 0.075); send_mouse_click(p_serial, p_lock, 1, 0)

            elif action == "ATTACK":
                dx, dy = cmd.get("dx", 0), cmd.get("dy", 0)
                is_pulling_shot = cmd.get("is_combat", False) # 💡 풀링(빽무빙) 걷기 상태임
                dist = math.hypot(dx, dy)
                
                if active_manual_target == key: continue
                
                # ========================================================================
                # 👑 [형님 기획 완벽 반영: 마우스 이동 거리에 따른 생체 역학적 패턴 자동 라우팅]
                # ========================================================================
                if is_pulling_shot:
                    # [도망/풀링 모드] 확실하게 뒤를 찍어줘야 하므로 단타(A)와 E패턴 위주
                    if dist > 80: patterns, weights = ["E", "A", "B", "C"], [40, 40, 15, 5]
                    else: patterns, weights = ["A", "B", "E", "C"], [50, 35, 10, 5]
                else:
                    if dist <= 40:
                        # 🚀 [CPS 3.0 부스팅 1] 존 1: 무의미한 C패턴(뻘짓) 억제, 무조건 A(단타)로 따닥!
                        patterns = ["A", "C", "D"]
                        weights = [80, 5, 15]
                        
                    elif dist <= 120:
                        # 🚀 [CPS 3.0 부스팅 2] 존 2: A(따닥)와 E(그림판) 비율 폭발!
                        patterns = ["A", "C", "E", "B"]
                        weights = [45, 5, 25, 25]
                        
                    else:
                        # 🚀 [CPS 3.0 부스팅 3] 존 3: 장거리 플릭샷도 A(따닥) 비중 상향
                        patterns = ["E", "B", "C", "A"]
                        weights = [40, 30, 5, 25]
                
                pattern = random.choices(patterns, weights=weights, k=1)[0]
                
                # 🛡️ 최후의 방어막: 거리가 15 미만이면 묻지도 따지지도 않고 A패턴 강제 고정
                if dist < 15: pattern = "A"
                
                # =======================================================
                # 🎨 [비동기 걷기] 패턴 E: 그림판 점/선 흩뿌리기 무빙
                # =======================================================
                if pattern == "E":
                    raw_deltas = list(generate_human_deltas(dx, dy, behavior="PATROL", key=key))
                    total_len = len(raw_deltas)
                    
                    if total_len > 10:
                        super_payload = []
                        is_down = False
                        stroke_starts = []
                        exact_dx, exact_dy = 0, 0
                        
                        if total_len > 32 and dist > 120:
                            num_strokes = random.choices([1, 2], weights=[50, 50])[0]
                        else:
                            num_strokes = 1 
                            
                        curr_idx = random.randint(1, 3) 
                        for _ in range(num_strokes):
                            if curr_idx < total_len - 6:
                                stroke_starts.append(curr_idx)
                                curr_idx += random.randint(16, 26) 
                                
                        next_stroke = stroke_starts.pop(0) if stroke_starts else -1
                        draw_end_idx = -1
                        
                        for i, (px, py) in enumerate(raw_deltas):
                            btn = 0
                            if is_down and i >= draw_end_idx:
                                btn = 2
                                is_down = False
                                px += random.choice([-1, 0, 1]); py += random.choice([-1, 0, 1])
                                if px == 0 and py == 0: px = 1 if random.random() > 0.5 else -1
                            elif not is_down and i == next_stroke:
                                btn = 1
                                is_down = True
                                hold_frames = random.choice([random.randint(6, 7), random.randint(8, 10)])
                                draw_end_idx = min(i + hold_frames, total_len - 1)
                                px += random.choice([-2, -1, 1, 2]); py += random.choice([-2, -1, 1, 2])
                                if px == 0 and py == 0: px = 1 if random.random() > 0.5 else -1
                                next_stroke = stroke_starts.pop(0) if stroke_starts else -1
                                
                            super_payload.append((px, py, btn))
                            exact_dx += px
                            exact_dy += py
                            
                        if is_down:
                            super_payload.append((0, 0, 2))
                            
                        send_super_packet_buffer(p_serial, p_lock, super_payload, key)
                        
                        # 🚀 [우주 비행 원천 차단 5] 패턴 E의 불규칙한 붓칠로 인해 발생한 픽셀 오차를 완벽히 환불합니다!
                        if key in ai_states:
                            ai_states[key]["cursor_pos"][0] -= (dx - exact_dx)
                            ai_states[key]["cursor_pos"][1] -= (dy - exact_dy)
                            
                        h_sleep(0.09, 0.15) 
                    else:
                        pattern = "A" 
                
                # =======================================================
                # 이하 기존 패턴 C, A, B, D 코드는 원본 100% 동일하게 유지
                # =======================================================
                if pattern == "C": 
                    send_macro_buffer(p_serial, p_lock, generate_human_deltas(dx, dy, behavior="PATROL", key=key), key)
                
                elif pattern == "A": 
                    if dist > 0: 
                        send_macro_buffer(p_serial, p_lock, generate_human_deltas(dx, dy, behavior="HOVER", key=key), key)
                        h_sleep(0.08, 0.15) 
                    
                    if is_pulling_shot:
                        click_cnt = random.randint(2, 3) 
                    else:
                        click_cnt = random.choices([1, 2, 3], weights=[10, 60, 30])[0] 
                        
                    for i in range(click_cnt):
                        send_mouse_click(p_serial, p_lock, 1, 1); h_sleep(0.059, 0.095); send_mouse_click(p_serial, p_lock, 1, 0)
                        if i < click_cnt - 1: h_sleep(0.07, 0.12)
                        
                elif pattern == "B": 
                    deltas = generate_human_deltas(dx, dy, behavior="PATROL", key=key)
                    mid = len(deltas) // random.randint(2, 3) 
                    if mid > 0:
                        send_macro_buffer(p_serial, p_lock, deltas[:mid], key)
                    if active_manual_target != key:
                        b_clicks = random.choices([1, 2], weights=[60, 40])[0]
                        for i in range(b_clicks):
                            send_mouse_click(p_serial, p_lock, 1, 1); h_sleep(0.059, 0.095); send_mouse_click(p_serial, p_lock, 1, 0)
                            if i < b_clicks - 1: h_sleep(0.07, 0.12)
                            
                    if mid > 0:
                        send_macro_buffer(p_serial, p_lock, deltas[mid:], key)
                    if active_manual_target != key and (random.random() < 0.75 or is_pulling_shot): 
                        h_sleep(0.06, 0.12) 
                        b_clicks2 = random.choices([1, 2], weights=[60, 40])[0]
                        for i in range(b_clicks2):
                            send_mouse_click(p_serial, p_lock, 1, 1); h_sleep(0.059, 0.095); send_mouse_click(p_serial, p_lock, 1, 0)
                            if i < b_clicks2 - 1: h_sleep(0.07, 0.12)
                        
                elif pattern == "D": 
                    if active_manual_target != key:
                        send_mouse_click(p_serial, p_lock, 1, 1); h_sleep(0.059, 0.095); send_mouse_click(p_serial, p_lock, 1, 0)
                        h_sleep(0.06, 0.12)
                
                    if random.random() < 0.5:
                        # 🚀 [우주 비행 원천 차단 6] 패턴 D에서 마우스를 1픽셀도 안 움직였는데 뇌는 움직였다고 착각 중. 전액 환불!
                        if key in ai_states:
                            ai_states[key]["cursor_pos"][0] -= dx
                            ai_states[key]["cursor_pos"][1] -= dy
                    else:
                        dist_to_go = math.hypot(dx, dy)
                        if dist_to_go > 0:
                            tiny_dist = g_val(10, 20)
                            tiny_dx = int((dx / dist_to_go) * tiny_dist)
                            tiny_dy = int((dy / dist_to_go) * tiny_dist)
                            if tiny_dx != 0 or tiny_dy != 0:
                                deltas_d = generate_human_deltas(tiny_dx, tiny_dy, behavior="PATROL", key=key)
                                send_macro_buffer(p_serial, p_lock, deltas_d, key)
                                # 🚀 [우주 비행 원천 차단 7] 10~20px만 가놓고 100px 갔다고 우기는 피코의 삥땅(미수금) 환불!
                                if key in ai_states:
                                    actual_dx = sum(d[0] for d in deltas_d)
                                    actual_dy = sum(d[1] for d in deltas_d)
                                    ai_states[key]["cursor_pos"][0] -= (dx - actual_dx)
                                    ai_states[key]["cursor_pos"][1] -= (dy - actual_dy)
                            else:
                                if key in ai_states:
                                    ai_states[key]["cursor_pos"][0] -= dx
                                    ai_states[key]["cursor_pos"][1] -= dy
                        else:
                            if key in ai_states:
                                ai_states[key]["cursor_pos"][0] -= dx
                                ai_states[key]["cursor_pos"][1] -= dy
                
                h_sleep(0.05, 0.15)

            # 🚨 [센서 OFF] 현재 명령이 끝났고 밀린 큐도 없다면 완벽 정지 상태 선언!
            if key in ai_states and q.empty():
                ai_states[key]["hw_busy"] = False

        except queue.Empty: 
            # 🚨 [센서 OFF] 큐가 비어서 대기 중일 때도 완벽 정지 상태 선언!
            if key in ai_states:
                ai_states[key]["hw_busy"] = False

for pc in MINI_PCS: threading.Thread(target=pico_worker_thread, args=(pc["key"],), daemon=True).start()

# ==========================================
# 6. 비전 코어 및 자동사냥 인공지능
# ==========================================
def play_tts_alert(msg):
    import re  # 🚀 마법의 정규식 모듈 소환 (함수 안에 넣어서 윗부분 수정 안 해도 됨)
    
    # 💡 1번~99번 숫자를 감지해서 "일, 이, 삼... 십일, 구십구" 로 자동 변환해 주는 뇌피셜 번역기
    def num_to_kor(match):
        num = int(match.group(1))
        if num == 0: return "영번"
        if num >= 100: return match.group(0) # 100번 이상은 그냥 원본 출력
        
        units = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
        tens = ["", "십", "이십", "삼십", "사십", "오십", "육십", "칠십", "팔십", "구십"]
        return tens[num // 10] + units[num % 10] + "번"

    # 🚀 "아무숫자+번" 패턴을 찾아서 무조건 일이번 체계로 강제 교정!
    # 예: "12번 피케이" -> "십이번 피케이"
    safe_msg = re.sub(r'(\d+)번', num_to_kor, str(msg))

    try: 
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(safe_msg)  # 💡 변환된 안전한 메세지(safe_msg)를 스피커에 넘김!
    except: 
        pass
    finally: 
        try: pythoncom.CoUninitialize()
        except: pass

def get_hp_mp_percent(img_bgr, roi_width, roi_height, y_start, y_end):
    try:
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        hp_roi = hsv[y_start:y_end, HP_X1:HP_X2] 
        mp_roi = hsv[y_start:y_end, MP_X1:MP_X2] 
        
        # 빨간색(정상 HP) 및 독(초록) 마스크 추출
        mask_hp_red = cv2.bitwise_or(cv2.inRange(hp_roi, (0, 100, 100), (15, 255, 255)), 
                                     cv2.inRange(hp_roi, (140, 100, 100), (180, 255, 255)))
        mask_poison = cv2.inRange(hp_roi, (45, 100, 50), (80, 255, 255))
        mask_hp = cv2.bitwise_or(mask_hp_red, mask_poison)

 
        mask_mp = cv2.inRange(mp_roi, (65, 20, 40), (160, 255, 255))

        kernel = np.ones((5, 5), np.uint8)
        mask_hp = cv2.morphologyEx(mask_hp, cv2.MORPH_CLOSE, kernel)
        mask_mp = cv2.morphologyEx(mask_mp, cv2.MORPH_CLOSE, kernel)

        def get_gauge_percent(mask, direction):
            col_sums = np.sum(mask > 0, axis=0)
            length = len(col_sums)
            
            if direction == "ltr": 
                # [HP 방식] 왼쪽(빈 공간)에서 오른쪽으로 스캔
                for x in range(length - 1):
                    # 🚀 구멍을 메웠으므로 텍스트 구간도 픽셀이 꽉 찹니다.
                    # 노이즈 방지를 위해 "가로 2칸 연속 2픽셀 이상"일 때만 진짜 게이지로 확정!
                    if col_sums[x] >= 2 and col_sums[x+1] >= 2:
                        return ((length - x) / length) * 100.0
                return 0.0

            elif direction == "rtl":
                # [MP 방식] 오른쪽(빈 공간)에서 왼쪽으로 스캔
                for x in range(length - 1, 0, -1):
                    if col_sums[x] >= 2 and col_sums[x-1] >= 2:
                        return ((x + 1) / length) * 100.0
                return 0.0

        hp_pct = get_gauge_percent(mask_hp, direction="ltr")
        mp_pct = get_gauge_percent(mask_mp, direction="rtl")
        
        is_poisoned = np.sum(mask_poison) > 500
        
        return min(100.0, hp_pct), min(100.0, mp_pct), is_poisoned
        
    except Exception as e: 
        return 100.0, 100.0, False

def check_pvp_mode(img_bgr):
    """용머리 영역의 붉은색(PvP 활성화) 픽셀을 감지하는 함수"""
    if img_bgr is None: return False
    try:
        roi = img_bgr[DRAGON_ROI_Y1:DRAGON_ROI_Y2, DRAGON_ROI_X1:DRAGON_ROI_X2]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # 리니지 용머리의 붉은빛을 잡아내는 HSV 범위 (빨간색은 0도와 180도 양쪽에 걸쳐 있음)
        mask1 = cv2.inRange(hsv, (0, 150, 100), (10, 255, 255))
        mask2 = cv2.inRange(hsv, (170, 150, 100), (180, 255, 255))
        mask_red = cv2.bitwise_or(mask1, mask2)
        
        # 붉은색 픽셀 개수 카운트
        red_pixels = cv2.countNonZero(mask_red)
        
        # 붉은 픽셀이 60개 이상이면 PvP 모드가 켜진 것으로 판단
        return red_pixels > 60
    except:
        return False

def check_exp_changed(key, img_bgr):
    state = ai_states[key]
    roi = img_bgr[EXP_ROI_Y1:EXP_ROI_Y2, EXP_ROI_X1:EXP_ROI_X2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    changed = False
    if state.get("exp_image") is not None:
        diff = cv2.absdiff(gray, state["exp_image"])
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        if cv2.countNonZero(thresh) > 10: changed = True
    state["exp_image"] = gray
    return changed

def check_weight_changed(key, img_bgr):
    """경험치 센서의 로직을 100% 완벽 복제한 무게 픽셀 변화 감지기"""
    state = ai_states[key]
    roi = img_bgr[WEIGHT_ROI_Y1:WEIGHT_ROI_Y2, WEIGHT_ROI_X1:WEIGHT_ROI_X2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    changed = False
    if state.get("weight_image") is not None:
        diff = cv2.absdiff(gray, state["weight_image"])
        # 🚀 [완벽 수술 1] 경험치와 동일한 방탄유리(밝기 25 이상, 픽셀 10개 초과) 적용!
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        if cv2.countNonZero(thresh) > 10: changed = True
    state["weight_image"] = gray
    return changed

def find_anchor_pos(img_bgr, template, offset_x=0, offset_y=0):
    if template is None or template.size == 0 or template.shape[0] == 0 or template.shape[1] == 0: return None
    try:
        th, tw = template.shape[:2]; ih, iw = img_bgr.shape[:2]
        if th > ih or tw > iw: return None
        res = cv2.matchTemplate(img_bgr, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.73: return max_loc[0] + tw//2 - offset_x, max_loc[1] + th//2 - offset_y
    except: pass 
    return None

def update_arrow_status(key, img_bgr, curr_time):
    state = ai_states[key]
    roi = img_bgr[ARROW_ROI_Y1:ARROW_ROI_Y2, ARROW_ROI_X1:ARROW_ROI_X2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    if state.get("arrow_image") is not None:
        diff = cv2.absdiff(gray, state["arrow_image"])
        _, diff_thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
        
        _, curr_bright = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        _, prev_bright = cv2.threshold(state["arrow_image"], 180, 255, cv2.THRESH_BINARY)
        bright_mask = cv2.bitwise_or(curr_bright, prev_bright)
        
        final_mask = cv2.bitwise_and(diff_thresh, bright_mask)
        changed_pixels = cv2.countNonZero(final_mask)
        
        if changed_pixels > 60:
            if state.get("arrow_empty_timer", 0) == 0: state["arrow_empty_timer"] = curr_time + 10.0
        elif changed_pixels >= 3:
            if changed_pixels <= 100: state["arrow_empty_timer"] = 0.0
            state["last_arrow_change_time"] = curr_time
            state["arrow_is_firing"] = True
            state["arrow_fire_count"] = state.get("arrow_fire_count", 0) + 1
        else:
            if curr_time - state.get("last_arrow_change_time", curr_time) >= ARROW_STOP_TIMEOUT:
                state["arrow_is_firing"] = False
                state["arrow_fire_count"] = 0

    if state.get("arrow_empty_timer", 0) > 0 and curr_time > state["arrow_empty_timer"]:
        pico_queues[key].put({"action": "HOLD_KEY", "keycode": KEY_F1, "duration": 0.1})
        state["arrow_empty_timer"] = 0.0

    state["arrow_image"] = gray

# =====================================================================
# 🚀 [아이템 스캔 최적화 1] 매 프레임 파이썬이 새로 만들고 버리던 도장(커널)과 배열을
# 전역 변수로 딱 1번만 선언하여 파이썬 메모리 청소기(GC) 잔렉 원천 소각!
# =====================================================================
ITEM_LOWER_COLOR = np.array([200, 200, 200], dtype=np.uint8)
ITEM_UPPER_COLOR = np.array([255, 255, 255], dtype=np.uint8)
CURSOR_RAW_MIN = np.array([220, 220, 220], dtype=np.uint8)
CURSOR_RAW_MAX = np.array([255, 255, 255], dtype=np.uint8)
ITEM_KERNEL_ERODE = np.ones((4, 4), np.uint8)
ITEM_KERNEL_DILATE = np.ones((8, 8), np.uint8)
ITEM_KERNEL_HORIZ = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))
ITEM_KERNEL_FUSE = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 2))

def find_item_boxes(img_bgr):
    h, w = img_bgr.shape[:2]
    # 🚀 [수정] 기존 640에서 자르던 것을 마우스 활동 한계치까지 풀스캔하도록 확장!
    roi = img_bgr[0:int(h * 0.68), 0:w-20] 

    # 1. 하얀색 테두리 추출 (전역 변수 활용)
    frame_mask = cv2.inRange(roi, ITEM_LOWER_COLOR, ITEM_UPPER_COLOR)

    cv2.rectangle(frame_mask, (0, 0), (145, 130), 0, -1)             # 1. 미니맵 구역 영구 삭제 (검은색 덧칠)
    
    # 2. 우측 버프창 구역 영구 삭제 (★디버그 창의 초록색 영점 조절 시 여기 숫자 160, 250도 똑같이 맞춰주세요!)
    cv2.rectangle(frame_mask, (w - 80, 0), (w, 320), 0, -1)         
    # 👆👆👆 ======================================================== 👆👆👆

    # 2. 커서 스마트 필터링 (전역 변수 활용)
    cursor_raw = cv2.inRange(roi, CURSOR_RAW_MIN, CURSOR_RAW_MAX)
    cursor_core = cv2.erode(cursor_raw, ITEM_KERNEL_ERODE, iterations=1)
    cursor_mask = cv2.dilate(cursor_core, ITEM_KERNEL_DILATE, iterations=1)
    frame_mask = cv2.bitwise_and(frame_mask, cv2.bitwise_not(cursor_mask))

    # 3. 선 복구 및 팽창 (전역 변수 활용)
    horiz_lines = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, ITEM_KERNEL_HORIZ)
    thick_lines = cv2.dilate(horiz_lines, ITEM_KERNEL_FUSE, iterations=1)

    contours, _ = cv2.findContours(thick_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 4. 얇은 뼈대(가로선) 수집
    lines = []
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)   # 🚀 [핵심 수술] w, h를 cw, ch로 변경!
        if cw >= 15 and ch <= 15:              # 🚀 여기도 cw, ch로 변경!
            lines.append({'x': x, 'y': y, 'w': cw, 'h': ch}) # 🚀 여기도 cw, ch로 변경!

    # =========================================================
    # 🚀 [CPU 점유율 1/10 압축: Y축 정렬 및 평행선 루프 가지치기]
    # =========================================================
    lines.sort(key=lambda b: b['y'])

    raw_boxes = []
    # 5. 위아래 평행선 짝짓기 (Pairing)
    for i in range(len(lines)):
        L1 = lines[i]
        for j in range(i + 1, len(lines)):
            L2 = lines[j]
            dy = L2['y'] - L1['y']

            if dy > 24:
                break 

            if 14 <= dy <= 24: 
                overlap_x1 = max(L1['x'], L2['x'])
                overlap_x2 = min(L1['x'] + L1['w'], L2['x'] + L2['w'])

                if overlap_x2 - overlap_x1 >= 15: 
                    box_x = min(L1['x'], L2['x'])
                    box_y = L1['y']
                    box_w = max(L1['x'] + L1['w'], L2['x'] + L2['w']) - box_x
                    box_h = (L2['y'] + L2['h']) - L1['y']

                    if 55 <= box_w <= 500:
                        inner_y1 = box_y + 3
                        inner_y2 = box_y + box_h - 3
                        
                        if inner_y2 > inner_y1:
                            mid_area = thick_lines[inner_y1:inner_y2, box_x:box_x+box_w]
                            if cv2.countNonZero(mid_area) > (box_w * (inner_y2 - inner_y1)) * 0.40:
                                continue

                        raw_boxes.append({'rect': (box_x, box_y, box_w, box_h)})

    boxes = []
    # 6. 중복 제거 및 데이터 규격 변환
    for b in raw_boxes:
        bx, by, bw, bh = b['rect']
        
        virtual_y1 = max(0, by - 5)
        virtual_y2 = min(int(h * 0.68), by + bh + 5) # 🚀 [수정] 460 고정값을 int(h * 0.68)로 교체
        virtual_h = virtual_y2 - virtual_y1

        cx = bx + bw // 2
        cy = virtual_y1 + virtual_h // 2
        
        is_duplicate = False
        for existing_box in boxes:
            if abs(existing_box['x'] - cx) < 20 and abs(existing_box['y'] - cy) < 20: 
                is_duplicate = True
                break
                
        if not is_duplicate: 
            boxes.append({
                'x': cx, 
                'y': cy, 
                'w': bw, 
                'h': virtual_h, 
                'rect': (bx, virtual_y1, bw, virtual_h)
            })

    return boxes

# 🚀 [에러 수술 완료] pc_key 파라미터와 **kwargs를 추가하여 에러를 완벽하게 흡수합니다!
def check_attack_cursor(img_bgr, cx, cy, check_maintain=False, pc_key=None, **kwargs):
    # 🚨 [버그 수정] 칼 이미지가 없으면 기본적으로 조기 종료!
    if img_sword is None: return False 
    try:
        h, w = img_bgr.shape[:2]
        if cx > w - 80: return False # 💡 이건 우측 UI(가방 등) 클릭 방어막이므로 80 그대로 유지!
        
        # 🚀 [형님 오더 적용] 1회성 칼 검사 시야를 기존 80 -> 180으로 대폭 확장! (마찰력 삑사리 완벽 커버)
        x1, x2 = max(0, int(cx) - 100), min(w, int(cx) + 100)
        y1, y2 = max(0, int(cy) - 100), min(h, int(cy) + 100)
        if x2 - x1 < 10 or y2 - y1 < 10: return False
        roi = img_bgr[y1:y2, x1:x2]
        
        finger_err = 1.0
        if cursor_color is not None:
            if cursor_mask is not None:
                res_f = cv2.matchTemplate(roi, cursor_color, cv2.TM_SQDIFF_NORMED, mask=cursor_mask)
                finger_err = cv2.minMaxLoc(res_f)[0]
            else:
                res_f = cv2.matchTemplate(roi, cursor_color, cv2.TM_SQDIFF_NORMED)
                finger_err = cv2.minMaxLoc(res_f)[0]
                
        # ✋ 1순위: 명백한 손가락이면 칼, 서클은 보지도 않고 즉시 기각! (초고속 패스)
        if finger_err <= 0.15: return False
                
        sword_err = 1.0
        if img_sword is not None:
            if img_sword_mask is not None: 
                res_s = cv2.matchTemplate(roi, img_sword, cv2.TM_SQDIFF_NORMED, mask=img_sword_mask)
                sword_err = cv2.minMaxLoc(res_s)[0]
            else: 
                res_s = cv2.matchTemplate(roi, img_sword, cv2.TM_SQDIFF_NORMED)
                sword_err = cv2.minMaxLoc(res_s)[0]

        # =====================================================================
        # 🚀 [서클 무연산 통제] 체인킬 대기 상태(check_maintain=True)일 때만 서클 커서를 대조합니다!
        # =====================================================================
        circle_err = 1.0
        if check_maintain and img_circle is not None:
            if img_circle_mask is not None: 
                res_c = cv2.matchTemplate(roi, img_circle, cv2.TM_SQDIFF_NORMED, mask=img_circle_mask)
                circle_err = cv2.minMaxLoc(res_c)[0]
            else: 
                res_c = cv2.matchTemplate(roi, img_circle, cv2.TM_SQDIFF_NORMED)
                circle_err = cv2.minMaxLoc(res_c)[0]

        # 💡 평상시엔 circle_err가 무조건 1.0이므로 사실상 칼 커서 오차율(sword_err)만 채택됨!
        attack_err = min(sword_err, circle_err)
            
        # 2. ⚖️ [경쟁 판정] 칼/마법보다 손가락 쪽에 오차율이 더 가깝다면(더 똑같이 생겼다면) 손가락으로 판정!
        if finger_err < attack_err and finger_err <= 0.30:
            return False

        # 3. ⚔️ [최종 인가] 손가락이 아님이 확정된 후, 진짜 칼(Sword) 또는 마법(Circle) 커트라인 통과 시 인정
        margin = 0.05 if check_maintain else 0.0

        is_attack_cursor = False
        if attack_err == sword_err and img_sword is not None:
            if img_sword_mask is not None:
                if sword_err <= (0.20 + margin): is_attack_cursor = True
            else:
                if sword_err <= (0.30 + margin): is_attack_cursor = True
        elif attack_err == circle_err and check_maintain and img_circle is not None:
            if img_circle_mask is not None:
                if circle_err <= (0.20 + margin): is_attack_cursor = True
            else:
                if circle_err <= (0.30 + margin): is_attack_cursor = True

        # =================================================================
        # 🚨 [최종 수문장: 보라돌이 절대 방어막 + 즉각 텔레포트 발동]
        # =================================================================
        # 💡 칼표시 유무(is_attack_cursor)와 관계없이, 조준하는 위치에 보라돌이가 있으면 즉각 감지!
        if check_purple_name(img_bgr, cx, cy):
            if pc_key and pc_key in ai_states:
                # 메인 AI 루프에 "보라돌이 발견! 즉시 텔레포트 요망" 긴급 깃발을 꽂습니다!
                ai_states[pc_key]["purple_teleport_trigger"] = True
                
            if DEBUG_MODE:
                from datetime import datetime
                t_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                key_str = f"[{pc_key}] " if pc_key else ""
                print(f"[{t_str}] {key_str}🚨 [PK 절대 방어] 조준 위치(X:{int(cx)}, Y:{int(cy)}) 보라돌이 감지! 공격 취소 및 즉각 텔레포트를 발동합니다.")
            
            return False # 타격을 원천 차단

        return is_attack_cursor

    except: return False

# ==============================================================================
# 🛠️ [무기 손상 팩트 체크 함수] 0.1초 대기 후 찐 실패 시에만 딱 1번 호출됨!
# ==============================================================================
def check_broken_weapon(img_bgr, cx, cy):
    import os
    if not os.path.exists("qq/sword_break.png"): return False
    
    if "img_sword_break" not in loaded_models:
        bgra = cv2.imread("qq/sword_break.png", cv2.IMREAD_UNCHANGED)
        if bgra is not None and len(bgra.shape) == 3 and bgra.shape[2] == 4:
            loaded_models["img_sword_break"] = {"color": bgra[:,:,:3], "mask": bgra[:,:,3]}
        else:
            loaded_models["img_sword_break"] = {"color": cv2.imread("qq/sword_break.png", cv2.IMREAD_COLOR), "mask": None}
            
    tmpl = loaded_models.get("img_sword_break")
    if tmpl and tmpl["color"] is not None:
        h, w = img_bgr.shape[:2]
        
        # 🚀 [수술 1] 검사 영역을 기존 +-40에서 +-80으로 2배 확장! (칼이 가장자리에 있을 때 짤림 방지)
        x1, y1 = max(0, int(cx) - 80), max(0, int(cy) - 80)
        x2, y2 = min(w, int(cx) + 80), min(h, int(cy) + 80)
        
        if x2 > x1 and y2 > y1:
            roi = img_bgr[y1:y2, x1:x2]
            
            # 🚨 [크래시 완벽 차단] 잘라낸 화면(roi)이 비교할 이미지(tmpl)보다 클 때만 검사!
            if roi.shape[0] >= tmpl["color"].shape[0] and roi.shape[1] >= tmpl["color"].shape[1]:
                try:
                    if tmpl["mask"] is not None:
                        res = cv2.matchTemplate(roi, tmpl["color"], cv2.TM_CCORR_NORMED, mask=cv2.merge([tmpl["mask"]]*3))
                    else:
                        res = cv2.matchTemplate(roi, tmpl["color"], cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(res)
                    
                    # 💡 형님 요청대로 80% 커트라인은 원본 그대로 유지합니다!
                    if max_val >= 0.80:
                        return True
                except Exception:
                    pass # 구석 억까 에러 발생 시 조용히 패스하여 스레드 생존 보장!
    return False


def check_purple_name(img_bgr, cx, cy):
    """🚀 [완벽 튜닝] PK 유저 연보라색 이름표 감지 (인게임 픽셀 데이터 기반)"""
    if img_bgr is None: return False
    try:
        h, w = img_bgr.shape[:2]
        # 🚀 이름표가 높은 곳에 뜨는 걸 잡기 위한 Y축 시야 확장은 유지합니다 (-140)
        x1, x2 = max(0, int(cx) - 80), min(w, int(cx) + 80)
        y1, y2 = max(0, int(cy) - 140), min(h, int(cy) + 30)
        if x2 - x1 < 10 or y2 - y1 < 10: return False
        
        roi = img_bgr[y1:y2, x1:x2]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # 🚨 [핵심 1] 제가 오지랖으로 넓혔던 색상값을 형님의 '오리지널 황금 수치'로 100% 원상 복구!
        lower_purple = np.array([145, 70, 60])
        upper_purple = np.array([158, 255, 255])
        mask = cv2.inRange(hsv, lower_purple, upper_purple)


        return cv2.countNonZero(mask) > 20
    except:
        return False

# ====================================================================
# 📡 [뼈대 C] 가변형 다중 모션 레이더 (Multi-Zone Motion Sensor)
# 중심점(cx,cy)과 반경(radius)만 주면, 그 안의 생명체를 0.001초만에 찾아냅니다!
# ====================================================================
def check_motion_in_radius(prev_gray, curr_gray, cx, cy, radius, char_cx=400, char_cy=245, exclude_rect=None, threshold=15, min_area=8):
    """
    반환값: (모션감지여부_Bool, 타겟X, 타겟Y)
    """
    if prev_gray is None or curr_gray is None:
        return False, None, None
        
    h, w = curr_gray.shape
    
    # 1. 검사할 사각형 영역 잘라내기 (화면 밖으로 나가지 않게 조율)
    x1 = max(0, int(cx - radius))
    y1 = max(0, int(cy - radius))
    x2 = min(w, int(cx + radius))
    y2 = min(h, int(cy + radius))
    
    if x2 <= x1 or y2 <= y1:
        return False, None, None
        
    prev_roi = prev_gray[y1:y2, x1:x2]
    curr_roi = curr_gray[y1:y2, x1:x2]
    
    # 2. 픽셀 변화량(Diff) 도출
    diff = cv2.absdiff(prev_roi, curr_roi)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    
    # 3. 🎯 완벽한 원형(레이더) 마스크 적용 (네모 모서리 부분의 오작동 완벽 컷트)
    roi_h, roi_w = thresh.shape
    Y, X = np.ogrid[:roi_h, :roi_w]
    dist_from_center = (X - (cx - x1))**2 + (Y - (cy - y1))**2
    circular_mask = dist_from_center <= radius**2
    thresh[~circular_mask] = 0
    
    # 4. 내 캐릭터 몸뚱이(이펙트 포함) 마스킹 (블랙홀)
    mw, mh_up, mh_down = 20, 33, 25 
    char_x_local = char_cx - x1
    char_y_local = (char_cy - 20) - y1 # 배꼽 기준 보정
    
    mx1 = max(0, int(char_x_local - mw))
    my1 = max(0, int(char_y_local - mh_up))
    mx2 = min(roi_w, int(char_x_local + mw))
    my2 = min(roi_h, int(char_y_local + mh_down))
    
    if mx2 > mx1 and my2 > my1:
        cv2.rectangle(thresh, (mx1, my1), (mx2, my2), 0, -1)

    # 5. 추가 제외 구역 (예: 타격 중인 몹, 잔상 등) 블랙홀 처리
    if exclude_rect:
        ex1, ey1, ex2, ey2 = exclude_rect
        emx1 = max(0, int(ex1 - x1))
        emy1 = max(0, int(ey1 - y1))
        emx2 = min(roi_w, int(ex2 - x1))
        emy2 = min(roi_h, int(ey2 - y1))
        if emx2 > emx1 and emy2 > emy1:
            cv2.rectangle(thresh, (emx1, emy1), (emx2, emy2), 0, -1)
            
    # 6. 찌꺼기 노이즈 필터링 (먼지 무시)
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # 7. 가장 크게 움직인 덩어리(몹/유저)의 정중앙 좌표(무게 중심) 찾기
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    best_target = None
    max_area = min_area
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= max_area:
            M = cv2.moments(cnt)
            if M["m00"] > 0:
                px = int(M["m10"] / M["m00"]) + x1
                py = int(M["m01"] / M["m00"]) + y1
                max_area = area
                best_target = (px, py) # 화면 전체 기준 좌표로 복원
                
    if best_target:
        return True, best_target[0], best_target[1]
        
    return False, None, None
# ====================================================================
# 📡 [뼈대 C: V3] 리니지 전용 타원형 모션 레이더 + 🧱 벽 투시 방어(LOS) 탑재!
# 💡 맵 데이터(map_gray, map_pos)를 던져주면 벽 너머의 모션은 스스로 걸러냅니다!
# ====================================================================
def check_motion_in_cells(prev_gray, curr_gray, cx, cy, cells, char_cx=400, char_cy=245, exclude_rect=None, threshold=12, min_area=5, map_gray=None, char_map_pos=None):
    """
    반환값: (모션감지여부_Bool, 타겟X, 타겟Y)
    """
    if prev_gray is None or curr_gray is None:
        return False, None, None

    # 1. 완벽한 타원형 반경 계산
    rx = int(cells * 50 + 25)  
    ry = int(rx / 2.0)         

    h, w = curr_gray.shape
    
    x1 = max(0, int(cx - rx))
    y1 = max(0, int(cy - ry))
    x2 = min(w, int(cx + rx))
    y2 = min(h, int(cy + ry))
    
    if x2 <= x1 or y2 <= y1:
        return False, None, None
        
    prev_roi = prev_gray[y1:y2, x1:x2]
    curr_roi = curr_gray[y1:y2, x1:x2]
    
    # 2. 픽셀 변화량(Diff) 도출 
    diff = cv2.absdiff(prev_roi, curr_roi)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    
    # 3. 2:1 타원형(Ellipse) 마스크 씌우기
    roi_h, roi_w = thresh.shape
    Y, X = np.ogrid[:roi_h, :roi_w]
    dist_from_center = ((X - (cx - x1))**2) / (rx**2) + ((Y - (cy - y1))**2) / (ry**2)
    elliptical_mask = dist_from_center <= 1.0
    thresh[~elliptical_mask] = 0
    
    # 4. 내 캐릭터 마스킹 (블랙홀)
    mw, mh_up, mh_down = 20, 33, 25
    char_x_local = char_cx - x1
    char_y_local = (char_cy - 20) - y1 
    
    mx1 = max(0, int(char_x_local - mw))
    my1 = max(0, int(char_y_local - mh_up))
    mx2 = min(roi_w, int(char_x_local + mw))
    my2 = min(roi_h, int(char_y_local + mh_down))
    
    if mx2 > mx1 and my2 > my1:
        cv2.rectangle(thresh, (mx1, my1), (mx2, my2), 0, -1)

    # 5. 추가 제외 구역 (타격 중인 몹 시체 등)
    if exclude_rect:
        ex1, ey1, ex2, ey2 = exclude_rect
        emx1 = max(0, int(ex1 - x1))
        emy1 = max(0, int(ey1 - y1))
        emx2 = min(roi_w, int(ex2 - x1))
        emy2 = min(roi_h, int(ey2 - y1))
        if emx2 > emx1 and emy2 > emy1:
            cv2.rectangle(thresh, (emx1, emy1), (emx2, emy2), 0, -1)
            
    # 6. 노이즈 필터링
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # 7. 덩어리 검사 및 🧱 레이캐스팅(LOS) 벽치기 방어!
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    best_target = None
    max_area = min_area
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= max_area:
            M = cv2.moments(cnt)
            if M["m00"] > 0:
                px = int(M["m10"] / M["m00"]) + x1
                py = int(M["m01"] / M["m00"]) + y1
                
                # 🚀 [형님 기획: 미니맵 벽 투시 필터링 적용!]
                if map_gray is not None and char_map_pos is not None:
                    map_dx = (px - char_cx) * 0.1
                    map_dy = (py - char_cy) * 0.1
                    target_map_x = char_map_pos[0] + map_dx
                    target_map_y = char_map_pos[1] + map_dy
                    
                    # 💡 레이캐스팅 발사! 벽에 막혀있으면 이 덩어리는 무시(continue)!
                    if not check_line_of_sight(map_gray, char_map_pos, (target_map_x, target_map_y), margin_steps=1):
                        continue 
                        
                max_area = area
                best_target = (px, py)
                
    if best_target:
        return True, best_target[0], best_target[1]
        
    return False, None, None

# 🚀 [핵심 수술 1] 큐(Queue) 폭파 시 마법/버프는 살리고 '이동 명령'만 완벽하게 도려내는 핀셋 필터링 함수
def clear_movements_only(q_obj):
    target_key = None
    for k, q in pico_queues.items():
        if q is q_obj:
            target_key = k
            break
            
    with q_obj.mutex:
        criticals = []
        refund_dx, refund_dy = 0, 0
        
        for item in q_obj.queue:
            action = item.get("action")
            if action in ["ESCAPE", "TELEPORT", "HEAL", "POTION", "ANTIDOTE", "SWEEP_START", "SWEEP_STOP", "BUFF_COMBO", "TAKE_BLUE_POTION", "HOLD_KEY", "SHIFT_SPACE", "SHIFT_CLICK_BRAKE", "MOUSE_WHEEL", "WAIT", "SPECIAL_ACK", "HOME_MACRO", "CERTI_CLICK", "TYPE_STRING", "CLOSE_TAB", "OPEN_TASKMGR", "TASKMGR_DEL", "CLOSE_TASKMGR"]:
                criticals.append(item)
            else:
                # 👇 [수정] SHOP_HOVER 가 추가되었습니다.
                if action in ["HOVER", "SHOP_HOVER", "ATTACK", "SINGLE_ATTACK"]:
                    refund_dx += item.get("dx", 0)
                    refund_dy += item.get("dy", 0)
                elif action == "CUSTOM_MOVE":
                    deltas = item.get("deltas", [])
                    refund_dx += sum(d[0] for d in deltas)
                    refund_dy += sum(d[1] for d in deltas)
                elif action == "DRAG_ATTACK":
                    refund_dx += item.get("drag_dx", 0)
                    refund_dy += item.get("drag_dy", 0)

        q_obj.queue.clear()
        q_obj.queue.append({"action": "FORCE_RELEASE"})
        
        for item in criticals:
            q_obj.queue.append(item)
            
    if target_key and target_key in ai_states:
        ai_states[target_key]["cursor_pos"][0] -= refund_dx
        ai_states[target_key]["cursor_pos"][1] -= refund_dy

# ==============================================================================
# 🚀 [무기 손상 패치 1] 기존 칼 감지 함수(check_attack_cursor)를 가로채어 손상된 검도 인식!
# ==============================================================================
original_check_attack_cursor = check_attack_cursor

def patched_check_attack_cursor(img_bgr, cx, cy, check_maintain=False, pc_key=None, **kwargs):
    # 1. 원래 함수대로 정상 칼인지 먼저 확인
    is_sword = original_check_attack_cursor(img_bgr, cx, cy, check_maintain=check_maintain, pc_key=pc_key, **kwargs)
    
    # 🚀 정상 칼(하얀 칼)이면 때려도 되므로 True 반환!
    if is_sword:
        return True
        
    # 2. 🚀 [CPU 최적화] 매 프레임 검사 방지! 실패 시 1초에 딱 1번만 손상검사 수행!
    import time
    curr_time = time.time()
    state = ai_states.get(pc_key, {}) if pc_key else {}
    
    if curr_time - state.get("last_broken_check", 0) > 1.0:
        state["last_broken_check"] = curr_time
        
        # 🚀 [수술 4] 길고 지저분했던 중복 로직 삭제! 위에서 완벽하게 고친 함수 하나만 깔끔하게 호출합니다.
        if check_broken_weapon(img_bgr, cx, cy):
            if pc_key in ai_states:
                ai_states[pc_key]["weapon_broken_flag"] = True
                ai_states[pc_key]["cursor_pos"] = [cx, cy] 
            
            # 🚨 [핵심 수술 5] 손상 무기이므로 "정상 칼이 아님"을 뜻하는 False를 반환하여 헛방 타격 차단!
            # (False를 반환하면 공격을 시도하지 않고, 1프레임 뒤 뇌가 텔레포트 수리를 정상 지시합니다)
            return False 
            
    return False

check_attack_cursor = patched_check_attack_cursor

# =====================================================================
# 🚀 [에러 픽스] 창 이름 변수 및 중앙컴 송신 함수 강제 선언!
# =====================================================================
TARGET_PC_TITLE = "Lineage" # 💡 캡처 및 제어할 파섹/문라이트 창 이름 (기존과 동일하게 맞춤)

def send_to_central_pc(client_id, data_dict):
    """중앙컴으로 명령(이동, 완료 등)을 하달하는 헬퍼 함수"""
    import json
    try:
        if client_id in connected_clients:
            client_data = connected_clients[client_id]
            sock = client_data.get("socket") if isinstance(client_data, dict) else client_data
            sock.send((json.dumps(data_dict, ensure_ascii=False) + "\n").encode('utf-8'))
            return True
    except Exception as e:
        print(f"⚠️ [통신 오류] 중앙컴({client_id}) 전송 실패: {e}")
    return False

# =====================================================================
# 👑 [개별 버퍼 뇌] 1타 시전 ➔ 검증 대기 ➔ 잔여 버프 발사 실무자
# =====================================================================
def ai_commander_worker(target_pc):
    import os
    import math
    import time
    import cv2
    key = target_pc["key"]
    state = ai_states[key]
    
    if "cmd_fsm" not in state: 
        state["cmd_fsm"] = "IDLE"

    char_screen_cx, char_screen_cy = 400, 245
    
    my_assigned_server = "대기"
    for server_name, m_list in SERVER_ASSIGNMENTS.items():
        if key in m_list:
            my_assigned_server = server_name
            break
            
    my_direct_queue = mini_queues.get(key)
    
    while True:
        try:
            curr_time = time.time()
            
            is_any_bot_on = (
                state.get("is_hunt_active", False) or
                state.get("is_shop_active", False) or
                state.get("is_recall_active", False) or
                str(state.get("target_fsm", "")).startswith("CERTI_")
            )
            if not DEBUG_MODE and not is_any_bot_on:
                time.sleep(0.1); continue
                
            img_bgr = latest_frames.get(key)
            if img_bgr is None: 
                time.sleep(GLOBAL_FRAME_DELAY); continue
                
            h, w = img_bgr.shape[:2]
            settings = current_settings.get(key, {})
            
            # =========================================================
            # 🩸 [MP 상시 체크 및 필터링]
            # =========================================================
            raw_hp, raw_mp, _ = get_hp_mp_percent(img_bgr, w, h, HP_Y_START, HP_Y_END)
            if "mp_buffer" not in state: state["mp_buffer"] = [raw_mp] * 5
            state["mp_buffer"].append(raw_mp)
            if len(state["mp_buffer"]) > 5: state["mp_buffer"].pop(0)
            mp = sorted(state["mp_buffer"])[2]

            debug_img = img_bgr.copy() if DEBUG_MODE else None

            # ====================================================================
            # 🔐 [군주 통제실 자동 인증 코어] certi.png / ticket2.png 실시간 감지 및 자동 복귀
            # ====================================================================
            current_fsm = str(state.get("target_fsm", "IDLE"))
            is_certi_mode = current_fsm.startswith("CERTI_")

            if is_any_bot_on and not state.get("is_paused", False) and not is_certi_mode:
                if curr_time > state.get("next_certi_check", 0):
                    state["next_certi_check"] = curr_time + 1.0
                    detected_popup_type, detected_val = None, 0.0

                    c_color, c_mask = globals().get("certi_color"), globals().get("certi_mask")
                    if c_color is not None:
                        try:
                            if c_mask is not None:
                                res_c = cv2.matchTemplate(img_bgr, c_color, cv2.TM_CCORR_NORMED, mask=cv2.merge([c_mask]*3))
                            else:
                                res_c = cv2.matchTemplate(img_bgr, c_color, cv2.TM_CCOEFF_NORMED)
                            _, max_val_c, _, _ = cv2.minMaxLoc(res_c)
                            if max_val_c >= 0.90:
                                detected_popup_type, detected_val = "CERTI", max_val_c
                        except Exception: pass

                    if detected_popup_type is None:
                        t2_color, t2_mask = globals().get("ticket2_color"), globals().get("ticket2_mask")
                        if t2_color is not None:
                            try:
                                if t2_mask is not None:
                                    res_t2 = cv2.matchTemplate(img_bgr, t2_color, cv2.TM_CCORR_NORMED, mask=cv2.merge([t2_mask]*3))
                                else:
                                    res_t2 = cv2.matchTemplate(img_bgr, t2_color, cv2.TM_CCOEFF_NORMED)
                                _, max_val_t2, _, _ = cv2.minMaxLoc(res_t2)
                                if max_val_t2 >= 0.90:
                                    detected_popup_type, detected_val = "TICKET2", max_val_t2
                            except Exception: pass

                    # 💀 [커서 가림 회피] 우측 상단 죽음감지창(death.png)이 떴는데 중앙 팝업이 안 보이면 커서가 가린 것이므로 즉시 옆으로 치움!
                    if detected_popup_type is None and img_death is not None and w >= 180 and h >= 180:
                        if curr_time > state.get("death_cursor_evade_cd", 0):
                            try:
                                death_roi = img_bgr[0:min(h, 180), max(0, w - 180):w]
                                if img_death_mask is not None:
                                    res_d = cv2.matchTemplate(death_roi, img_death, cv2.TM_CCORR_NORMED, mask=cv2.merge([img_death_mask]*3))
                                else:
                                    res_d = cv2.matchTemplate(death_roi, img_death, cv2.TM_CCOEFF_NORMED)
                                _, max_val_d, _, _ = cv2.minMaxLoc(res_d)

                                if max_val_d >= 0.83:
                                    state["death_cursor_evade_cd"] = curr_time + 3.0
                                    state["abort_macro"] = True
                                    with pico_queues[key].mutex: pico_queues[key].queue.clear()
                                    clear_movements_only(pico_queues[key])

                                    real_c = find_cursor_pos(img_bgr, last_pos=state.get("cursor_pos", [400, 300]), allow_full_scan=True)
                                    cur_cx, cur_cy = real_c if real_c else state.get("cursor_pos", [400, 300])
                                    # 중앙 팝업창(X:280~520, Y:200~360)을 완전히 벗어난 좌측 상단 안전지대로 커서 이동
                                    safe_tx = int(round(g_val(150, 210)))
                                    safe_ty = int(round(g_val(140, 190)))
                                    dx_ev, dy_ev = safe_tx - cur_cx, safe_ty - cur_cy
                                    dur_ev = apply_human_variance(0.08 + 0.035 * math.log2((math.hypot(dx_ev, dy_ev) / 20.0) + 1.0))
                                    deltas_ev = generate_human_deltas(dx_ev, dy_ev, duration=dur_ev, behavior="CERTI", key=key)
                                    if deltas_ev:
                                        pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": deltas_ev})
                                    state["cursor_pos"] = [safe_tx, safe_ty]
                                    state["next_certi_check"] = curr_time + dur_ev + 0.25
                                    dprint(key, f"💀 [Restart창 감지 ➔ 커서 회피] death.png({max_val_d*100:.1f}%) 포착! 중앙 인증창 가림 해제를 위해 커서를 ({safe_tx}, {safe_ty})로 치웁니다!")
                            except Exception: pass

                    if detected_popup_type is not None:
                        # 🚨 만약 버프 임무 수행 도중 인증창이 떴다면 즉시 통제실 라우터에 보고하여 다른 군주가 이어받게 처리!
                        if state.get("cmd_fsm", "IDLE") != "IDLE" and state.get("target_char_id"):
                            internal_router_queue.put({"action": "TASK_ABORTED", "mini_key": key, "char_id": state["target_char_id"]})
                        state["cmd_fsm"] = "IDLE"
                        if my_direct_queue:
                            with my_direct_queue.mutex: my_direct_queue.queue.clear()

                        state["abort_macro"] = True
                        with pico_queues[key].mutex: pico_queues[key].queue.clear()
                        clear_movements_only(pico_queues[key])
                        pico_queues[key].put({"action": "FORCE_RELEASE"})
                        state["certi_from_closed_game"] = False

                        if detected_popup_type == "CERTI":
                            try:
                                use_delay = bool(settings.get("auth_delay_use", False))
                                start_m = int(float(settings.get("auth_delay_start_min", 55))) % 60
                                end_m = int(float(settings.get("auth_delay_end_min", 58))) % 60
                                delay_s = float(settings.get("auth_delay_sec", 180.0))
                            except Exception:
                                use_delay, start_m, end_m, delay_s = False, 55, 58, 180.0

                            now_dt = datetime.datetime.now()
                            curr_m = now_dt.minute
                            is_in_time_range = (start_m <= curr_m <= end_m) if start_m <= end_m else (curr_m >= start_m or curr_m <= end_m)

                            if use_delay and is_in_time_range and delay_s > 0:
                                final_delay = g_val(max(1.0, delay_s - 2.0), delay_s + 2.0)
                                state["certi_delay_until"] = curr_time + final_delay
                                state["certi_delay_log_time"] = curr_time
                                dprint(key, f"⏳ [특정시간 인증 딜레이] 현재 시각({now_dt.strftime('%H:%M:%S')}) {final_delay:.1f}초 대기 후 인증 시작!")
                                state["target_fsm"] = "CERTI_DELAY_WAIT"
                                current_fsm = "CERTI_DELAY_WAIT"
                            else:
                                dprint(key, f"🚨 [군주 인증 감지] certi.png ({detected_val*100:.1f}%) 포착! 버프 배분에서 일시 열외하고 인증 모드로 진입합니다!")
                                state["target_fsm"] = "CERTI_GOTO_DESKTOP"
                                current_fsm = "CERTI_GOTO_DESKTOP"
                        else:
                            dprint(key, f"🚨 [군주 이용시간 만료 감지] ticket2.png ({detected_val*100:.1f}%) 포착! ok2 ➔ quit 클릭 후 13.png 재접속으로 직행합니다!")
                            state["target_fsm"] = "CERTI_FIND_OK2_FIRST"
                            current_fsm = "CERTI_FIND_OK2_FIRST"

                        state["cooldown"] = curr_time + 0.5
                        is_certi_mode = True

            if is_certi_mode:
                if not is_any_bot_on or state.get("is_paused", False):
                    dprint(key, "🛑 [인증 강제 중단] 봇 정지 감지! 인증 시퀀스를 멈추고 IP 사용권을 반납합니다.")
                    release_central_ip_lock_async(key)
                    state["was_manual_in_certi"] = False
                    state["abort_macro"] = True
                    with pico_queues[key].mutex: pico_queues[key].queue.clear()
                    pico_queues[key].put({"action": "FORCE_RELEASE"})
                    state["target_fsm"] = "IDLE"
                    state["certi_last_box"] = None
                    is_certi_mode = False

                elif active_manual_target == key:
                    if not state.get("was_manual_in_certi", False):
                        state["was_manual_in_certi"] = True
                        if current_fsm != "CERTI_AUTO_RESUME_SCAN":
                            state["certi_fsm_before_manual"] = current_fsm
                        state["abort_macro"] = True
                        with pico_queues[key].mutex: pico_queues[key].queue.clear()
                        pico_queues[key].put({"action": "FORCE_RELEASE"})
                        dprint(key, f"🖐️ [인증 중 수동 개입] 수동 제어 전환! 조치 후 [`] 키를 누르면 현재 화면을 인식해 이어갑니다!")

                    if state.get("certi_locked_central") and curr_time - state.get("certi_lock_hb_time", 0.0) >= 4.0:
                        state["certi_lock_hb_time"] = curr_time
                        threading.Thread(target=request_central_ip_lock, args=(key, state["certi_locked_central"], "ACQUIRE"), daemon=True).start()

                    if DEBUG_MODE and debug_img is not None:
                        cv2.putText(debug_img, f"[ MANUAL IN CERTI : Press ` to Auto-Resume ]", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                        try:
                            if debug_queues[key].full(): debug_queues[key].get_nowait()
                            debug_queues[key].put_nowait(debug_img)
                        except Exception: pass
                    time.sleep(0.05)
                    continue

                elif state.get("was_manual_in_certi", False):
                    state["was_manual_in_certi"] = False
                    real_c = find_cursor_pos(img_bgr, last_pos=state.get("cursor_pos", [400, 300]), allow_full_scan=True, is_certi_mode=True)
                    if real_c:
                        state["cursor_pos"] = [real_c[0], real_c[1]]
                        state["real_cursor_pos"] = [real_c[0], real_c[1]]
                    state["certi_resume_scan_start"] = curr_time
                    state["certi_web_last_fsm"] = None
                    state["certi_last_box"] = None
                    state["target_fsm"] = "CERTI_AUTO_RESUME_SCAN"
                    current_fsm = "CERTI_AUTO_RESUME_SCAN"
                    state["cooldown"] = curr_time + 0.3
                    dprint(key, "🔄 [수동 종료 ➔ 화면 자동 인식 가동] 현재 화면이 몇 단계인지 스캔하여 자동으로 이어갑니다!")

            if is_certi_mode:
                def find_certi_img(target_name, th=0.82, roi_rect=None):
                    path = f"qq/certi/{target_name}" if not target_name.startswith("qq/") else target_name
                    if not os.path.exists(path):
                        return None
                    if path not in loaded_models:
                        try:
                            with open(path, "rb") as f:
                                np_arr = np.asarray(bytearray(f.read()), dtype=np.uint8)
                            bgra = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
                            if bgra is not None:
                                if len(bgra.shape) == 3 and bgra.shape[2] == 4:
                                    loaded_models[path] = {"color": bgra[:, :, :3], "mask": bgra[:, :, 3]}
                                else:
                                    loaded_models[path] = {"color": bgra[:, :, :3] if len(bgra.shape) == 3 else bgra, "mask": None}
                            else:
                                loaded_models[path] = None
                        except Exception:
                            loaded_models[path] = None

                    tmpl_data = loaded_models.get(path)
                    if not tmpl_data or tmpl_data["color"] is None:
                        return None
                    tmpl, mask = tmpl_data["color"], tmpl_data["mask"]

                    # 💡 7.png 검색 시 화면 맨 아래에서 위로 200픽셀(작업표시줄 포함 하단 영역)은 무조건 스캔 제외!
                    if roi_rect is None and target_name in ["7.png", "qq/certi/7.png"]:
                        roi_rect = (0, 0, w, max(100, h - 200))

                    if roi_rect is not None:
                        rx1, ry1, rx2, ry2 = roi_rect
                        rx1, ry1 = max(0, int(rx1)), max(0, int(ry1))
                        rx2, ry2 = min(img_bgr.shape[1], int(rx2)), min(img_bgr.shape[0], int(ry2))
                        search_area = img_bgr[ry1:ry2, rx1:rx2]
                    else:
                        rx1, ry1 = 0, 0
                        search_area = img_bgr

                    if search_area.shape[0] < tmpl.shape[0] or search_area.shape[1] < tmpl.shape[1]:
                        return None
                    try:
                        if mask is not None:
                            res = cv2.matchTemplate(search_area, tmpl, cv2.TM_CCORR_NORMED, mask=cv2.merge([mask]*3))
                        else:
                            res = cv2.matchTemplate(search_area, tmpl, cv2.TM_CCOEFF_NORMED)
                        _, max_val, _, max_loc = cv2.minMaxLoc(res)
                        if max_val >= th:
                            th_h, tw_w = tmpl.shape[:2]
                            abs_x, abs_y = rx1 + max_loc[0], ry1 + max_loc[1]
                            cx_pos, cy_pos = abs_x + tw_w // 2, abs_y + th_h // 2
                            state["certi_last_box"] = (abs_x, abs_y, tw_w, th_h, target_name, max_val)
                            return (cx_pos, cy_pos)
                    except Exception:
                        pass
                    return None

                def find_any_captcha_img(th=0.75):
                    captcha_banner_roi = (240, 90, 550, 290)
                    for idx in range(1, 11):
                        fname = "captcha.png" if idx == 1 else f"captcha{idx}.png"
                        pos = find_certi_img(fname, th=th, roi_rect=captcha_banner_roi)
                        if pos:
                            return pos
                    return None

                # 🔎 qq/certi/recerti/ 폴더 내 re1.png ~ re10.png (재인증/오류 이미지) 통합 스캔 헬퍼 함수
                def find_any_recerti_img(th=0.82):
                    recerti_dir = "qq/certi/recerti"
                    if not os.path.exists(recerti_dir):
                        return None, None
                    checked_files = set()
                    for idx in range(1, 11):
                        for ext in (".png", ".jpg"):
                            fname = f"re{idx}{ext}"
                            fpath = os.path.join(recerti_dir, fname)
                            if os.path.exists(fpath):
                                checked_files.add(fname.lower())
                                pos = find_certi_img(f"recerti/{fname}", th=th)
                                if pos:
                                    return pos, fname
                    try:
                        for fname in os.listdir(recerti_dir):
                            fl = fname.lower()
                            if fl in checked_files or not fl.endswith((".png", ".jpg")):
                                continue
                            if fl.startswith(("lineage", "confirm", "delay", "ok", "rec")):
                                continue
                            if fl.startswith("re"):
                                pos = find_certi_img(f"recerti/{fname}", th=th)
                                if pos:
                                    return pos, fname
                    except Exception:
                        pass
                    return None, None

                # 🔀 re1, re2(강종 없이 ok2/ok3 클릭 종료 후 재인증) vs re3~(작업관리자 강종 후 재인증) 분기 헬퍼 함수
                def handle_recerti_branch(pos_re, re_name, stage_desc):
                    clear_movements_only(pico_queues[key])
                    state["certi_delay_seen_time"] = 0.0
                    base_re = os.path.splitext(re_name)[0].lower()
                    if base_re in ["re1", "re2"]:
                        dprint(key, f"🚨 [{stage_desc} - {re_name} 포착] ({pos_re[0]}, {pos_re[1]}) 강종 없이 'ok2.png' 또는 'ok3.png' 버튼을 눌러 게임을 종료합니다!")
                        state["recerti_ok_find_start"] = curr_time
                        state["recerti_ok_evaded"] = False
                        state["target_fsm"] = "CERTI_RECERTI_OK_FIND"
                        state["cooldown"] = curr_time + 0.1
                    else:
                        dprint(key, f"🚨 [{stage_desc} - {re_name} 포착] ({pos_re[0]}, {pos_re[1]}) 바탕화면 이동 후 작업관리자 강종으로 직행합니다!")
                        pico_queues[key].put({"action": "HOME_MACRO"})
                        state["target_fsm"] = "CERTI_RECERTI_OPEN_TM"
                        state["cooldown"] = curr_time + g_val(1.2, 1.6)

                def start_certi_move_and_action(tx, ty, next_fsm, double=False, type_text=None, press_enter=False, use_jitter=True, post_wait=0.5, desc=""):
                    ingame_fsms = {
                        "CERTI_FIND_OK2_FIRST", "CERTI_FIND_QUIT", "CERTI_STEP_17_FIND", "CERTI_RECERTI_OK_FIND", "CERTI_DRAGON_CLICK_HASTE"
                    }
                    c_mode = True if (current_fsm in ingame_fsms) else "WEB"
                    real_c = find_cursor_pos(img_bgr, last_pos=state.get("cursor_pos", [400, 300]), allow_full_scan=True, is_certi_mode=c_mode)
                    if real_c:
                        cur_cx, cur_cy = real_c[0], real_c[1]
                        state["cursor_pos"] = [cur_cx, cur_cy]
                        state["real_cursor_pos"] = [cur_cx, cur_cy]
                    else:
                        cur_cx, cur_cy = state.get("cursor_pos", [400, 300])

                    if use_jitter:
                        fx = int(max(5, min(w - 5, tx + int(round(g_val(-3, 3))))))
                        fy = int(max(5, min(h - 5, ty + int(round(g_val(-2, 2))))))
                    else:
                        fx = int(max(5, min(w - 5, tx)))
                        fy = int(max(5, min(h - 5, ty)))

                    dx, dy = fx - cur_cx, fy - cur_cy
                    dist = math.hypot(dx, dy)
                    dur = apply_human_variance(0.08 + 0.035 * math.log2((dist / 20.0) + 1.0) if dist > 0 else 0.08) * 1.2
                    deltas = generate_human_deltas(dx, dy, duration=dur, behavior="CERTI", key=key)
                    if deltas:
                        pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": deltas})
                    pico_queues[key].put({"action": "SPECIAL_ACK"})

                    state["special_ack_arrived"] = False
                    state["pico_arrived"] = False
                    state["cursor_pos"] = [fx, fy]
                    state["real_cursor_pos"] = [fx, fy]
                    state["certi_target_pos"] = (fx, fy)
                    state["certi_click_double"] = double
                    state["certi_type_text"] = type_text
                    state["certi_press_enter"] = press_enter
                    state["certi_strict_aim"] = (not use_jitter)
                    state["certi_post_wait"] = post_wait
                    state["certi_next_fsm"] = next_fsm
                    state["certi_action_desc"] = desc
                    state["certi_corr_cnt"] = 0
                    state["certi_ack_timeout"] = curr_time + dur + 1.5
                    state["target_fsm"] = "CERTI_MOVE_VERIFY"
                    state["cooldown"] = curr_time + 0.05

                curr_acc_id = settings.get("auth_main_id", "") or settings.get("auth_main_email", "")
                curr_acc_pw = settings.get("auth_main_pw", "")
                curr_acc_email = settings.get("auth_main_email", "")
                curr_acc_phone = settings.get("auth_main_phone", "")

                is_hw_working = state.get("hw_busy", False) or not pico_queues[key].empty()

                if state.get("certi_locked_central") and curr_time - state.get("certi_lock_hb_time", 0.0) >= 4.0:
                    state["certi_lock_hb_time"] = curr_time
                    threading.Thread(target=request_central_ip_lock, args=(key, state["certi_locked_central"], "ACQUIRE"), daemon=True).start()

                web_timeout_fsms = {
                    "CERTI_STEP_2_FIND", "CERTI_STEP_3_FIND", "CERTI_STEP_5_FIND",
                    "CERTI_STEP_7_FIND", "CERTI_STEP_8_FIND", "CERTI_STEP_8_BRANCH", "CERTI_WAIT_SUC"
                }
                step_limit_sec = 25.0 if current_fsm in {"CERTI_STEP_5_FIND", "CERTI_STEP_7_FIND", "CERTI_STEP_8_BRANCH", "CERTI_WAIT_SUC"} else 15.0

                if current_fsm not in web_timeout_fsms or is_hw_working or state.get("certi_web_last_fsm") != current_fsm:
                    state["certi_web_last_fsm"] = current_fsm
                    state["certi_web_step_start"] = curr_time
                elif curr_time - state.get("certi_web_step_start", curr_time) >= step_limit_sec:
                    pico_queues[key].put({"action": "CLOSE_TAB"})
                    if state.get("certi_use_sub", False):
                        release_central_ip_lock_async(key)
                        my_num = get_my_central_num()
                        prev_c = str(state.get("certi_curr_central") or my_num).strip()
                        next_c = get_next_central_in_order(prev_c)
                        state["certi_curr_central"] = next_c
                        if key not in saved_settings:
                            saved_settings[key] = {}
                        saved_settings[key]["certi_curr_central"] = next_c
                        save_settings()
                        if next_c == my_num:
                            state["certi_use_sub"] = False
                        else:
                            state["certi_use_sub"] = True
                            CURRENT_PROXY_TARGET_NUM[key] = next_c
                        dprint(key, f"⏰ [웹 인증 {step_limit_sec:.0f}초 타임아웃] '{current_fsm}' 지연 초과! [{prev_c}번 ➔ {next_c}번 중앙컴] 회선으로 변경하여 재시도합니다.")
                    else:
                        dprint(key, f"⏰ [웹 인증 {step_limit_sec:.0f}초 타임아웃] '{current_fsm}' 단계 {step_limit_sec:.0f}초 초과! 크롬 창을 닫고 다시 시작합니다.")

                    state["certi_web_last_fsm"] = None
                    state["certi_web_step_start"] = curr_time
                    state["certi_last_box"] = None
                    state["target_fsm"] = "CERTI_WAIT_IP_LOCK"
                    state["cooldown"] = curr_time + 1.2
                    continue

                # 🔄 [14단계 이후 클릭 미스 5초 역추적 워치독]
                post13_retry_map = {
                    "CERTI_FIND_QUIT": {
                        "curr_imgs": ["quit.png"],
                        "prev_list": [("ok2.png", "CERTI_FIND_OK2_FIRST")]
                    },
                    "CERTI_STEP_15_FIND": {
                        "curr_imgs": ["15.png"],
                        "prev_list": [("14.png", "CERTI_WAIT_GAME_LAUNCH")]
                    },
                    "CERTI_STEP_16_FIND": {
                        "curr_imgs": ["16.png"],
                        "prev_list": [("15.png", "CERTI_STEP_15_FIND"), ("14.png", "CERTI_WAIT_GAME_LAUNCH")]
                    },
                    "CERTI_AFTER_16_BRANCH": {
                        "curr_imgs": ["ticket.png", "login.png"],
                        "prev_list": [("16.png", "CERTI_STEP_16_FIND"), ("15.png", "CERTI_STEP_15_FIND")]
                    },
                    "CERTI_TICKET_OK2_FIND": {
                        "curr_imgs": ["ok2.png"],
                        "prev_list": [("ticket.png", "CERTI_AFTER_16_BRANCH")]
                    },
                    "CERTI_STEP_17_FIND": {
                        "curr_imgs": ["17.png"],
                        "prev_list": [("login.png", "CERTI_AFTER_16_BRANCH"), ("16.png", "CERTI_STEP_16_FIND")]
                    },
                    "CERTI_WAIT_DRAGON": {
                        "curr_imgs": ["dragon.png", "ticket2.png"],
                        "prev_list": [("17.png", "CERTI_STEP_17_FIND"), ("login.png", "CERTI_AFTER_16_BRANCH")]
                    }
                }

                if current_fsm not in post13_retry_map:
                    state["certi_post13_last_fsm"] = None
                    state["certi_post13_step_start"] = curr_time
                    state["certi_post13_cursor_moved"] = False
                else:
                    if state.get("certi_post13_last_fsm") != current_fsm:
                        state["certi_post13_last_fsm"] = current_fsm
                        state["certi_post13_step_start"] = curr_time
                        state["certi_post13_cursor_moved"] = False
                    elif not is_hw_working and curr_time >= state.get("cooldown", 0) and (curr_time - state.get("certi_post13_step_start", curr_time) >= 5.0):
                        retry_info = post13_retry_map[current_fsm]
                        curr_target_visible = (
                            any(find_certi_img(c_img, th=0.82) is not None for c_img in retry_info["curr_imgs"]) or
                            (find_any_recerti_img(th=0.82)[0] is not None)
                        )
                        if curr_target_visible:
                            state["certi_post13_step_start"] = curr_time
                            state["certi_post13_cursor_moved"] = False
                        else:
                            if not state.get("certi_post13_cursor_moved", False):
                                real_c = find_cursor_pos(img_bgr, last_pos=state.get("cursor_pos", [400, 300]), allow_full_scan=True, is_certi_mode=True)
                                cur_cx, cur_cy = real_c if real_c else state.get("cursor_pos", [400, 300])
                                state["cursor_pos"] = [cur_cx, cur_cy]

                                offset_x = int(round(g_val(85, 120))) * (-1 if cur_cx > 400 else 1)
                                offset_y = int(round(g_val(65, 95))) * (-1 if cur_cy > 300 else 1)
                                evade_tx = int(max(40, min(w - 40, cur_cx + offset_x)))
                                evade_ty = int(max(40, min(h - 40, cur_cy + offset_y)))

                                dx_ev, dy_ev = evade_tx - cur_cx, evade_ty - cur_cy
                                dist_ev = math.hypot(dx_ev, dy_ev)
                                dur_ev = apply_human_variance(0.08 + 0.035 * math.log2((dist_ev / 20.0) + 1.0) if dist_ev > 0 else 0.08)

                                deltas_ev = generate_human_deltas(dx_ev, dy_ev, duration=dur_ev, behavior="CERTI", key=key)
                                if deltas_ev:
                                    pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": deltas_ev})
                                state["cursor_pos"] = [evade_tx, evade_ty]
                                state["real_cursor_pos"] = [evade_tx, evade_ty]
                                state["certi_post13_cursor_moved"] = True
                                state["cooldown"] = curr_time + dur_ev + g_val(0.25, 0.35)
                                dprint(key, f"👀 [5초 정체 ➔ 커서 회피] '{current_fsm}' 단계 5초 경과! 커서 가림 방지를 위해 마우스를 ({evade_tx}, {evade_ty})로 치운 뒤 이전 이미지를 확인합니다.")
                                continue
                            else:
                                found_prev_fsm = None
                                found_prev_img = None
                                for p_img, p_fsm in retry_info["prev_list"]:
                                    if find_certi_img(p_img, th=0.82) is not None:
                                        found_prev_img = p_img
                                        found_prev_fsm = p_fsm
                                        break

                                if found_prev_fsm:
                                    dprint(key, f"🔄 [클릭 미스 복구] 커서 이동 후에도 이전 단계 이미지('{found_prev_img}')가 화면에 남아있습니다! 이전 단계('{found_prev_fsm}')로 돌아가 다시 클릭합니다!")
                                    state["target_fsm"] = found_prev_fsm
                                    state["certi_post13_last_fsm"] = found_prev_fsm
                                    state["certi_post13_step_start"] = curr_time
                                    state["certi_post13_cursor_moved"] = False
                                    state["cooldown"] = curr_time + g_val(0.15, 0.25)
                                    continue
                                else:
                                    state["certi_post13_step_start"] = curr_time
                                    state["certi_post13_cursor_moved"] = False

                if curr_time >= state.get("cooldown", 0) and (not is_hw_working or current_fsm == "CERTI_MOVE_VERIFY"):
                    if current_fsm == "CERTI_AUTO_RESUME_SCAN":
                        resume_fsm, resume_desc = None, ""
                        auto_cap_on = settings.get("auth_auto_captcha", False)
                        if find_certi_img("suc.png", th=0.82):
                            resume_fsm, resume_desc = "CERTI_WAIT_SUC", "웹 인증 완료(suc.png)"
                        elif find_certi_img("9.png", th=0.80) or find_certi_img("10.png", th=0.80):
                            resume_fsm, resume_desc = "CERTI_STEP_8_BRANCH", "메일/전번 입력(9/10.png)"
                        elif find_certi_img("fail.png", th=0.82):
                            resume_fsm, resume_desc = "CERTI_STEP_8_BRANCH", "인증 한도 초과(fail.png)"
                        elif find_certi_img("8.png", th=0.82):
                            resume_fsm, resume_desc = "CERTI_STEP_8_FIND", "웹 8단계(8.png)"
                        elif find_certi_img("7.png", th=0.82):
                            resume_fsm, resume_desc = "CERTI_STEP_7_FIND", "웹 7단계(7.png)"
                        elif find_certi_img("5.png", th=0.82):
                            resume_fsm, resume_desc = "CERTI_STEP_5_FIND", "웹 5단계(5.png)"
                        elif find_certi_img("3.png", th=0.82):
                            resume_fsm, resume_desc = "CERTI_STEP_3_FIND", "웹 3단계(3.png)"
                        elif find_certi_img("2.png", th=0.82):
                            resume_fsm, resume_desc = "CERTI_STEP_2_FIND", "웹 2단계(2.png)"
                        elif find_any_captcha_img(th=0.75):
                            prev_f = state.get("certi_fsm_before_manual", "")
                            if not state.get("captcha_return_fsm"):
                                state["captcha_return_fsm"] = "CERTI_STEP_5_FIND" if prev_f in ["CERTI_STEP_3_FIND", "CERTI_STEP_5_FIND"] else "CERTI_STEP_8_BRANCH"
                            if auto_cap_on:
                                state["captcha_is_scrolled_down"] = False
                                state["captcha_scroll_cnt"] = 0
                                state["captcha_test_round"] = 1
                                resume_fsm, resume_desc = "CERTI_CAPTCHA_SOLVE", "리캡차 자동 판독 화면(captcha.png)"
                            else:
                                resume_fsm, resume_desc = "CERTI_CAPTCHA_MANUAL_WAIT", "리캡차 수동 대기 화면(captcha.png)"
                        elif find_certi_img("confirm.png", th=0.80) or find_certi_img("next.png", th=0.80) or find_certi_img("skip.png", th=0.80):
                            if auto_cap_on:
                                state["captcha_is_scrolled_down"] = True
                                state["captcha_scroll_cnt"] = 0
                                resume_fsm, resume_desc = "CERTI_CAPTCHA_SCROLL", "리캡차 하단 확인/다음/건너뛰기(confirm/next/skip)"
                            else:
                                resume_fsm, resume_desc = "CERTI_CAPTCHA_MANUAL_WAIT", "리캡차 수동 확인 대기(confirm/next/skip)"

                        if resume_fsm is None:
                            has_ok2 = find_certi_img("ok2.png", th=0.82) is not None
                            has_quit = find_certi_img("quit.png", th=0.82) is not None
                            has_dragon = find_certi_img("dragon.png", th=0.82) is not None
                            if has_ok2:
                                if has_dragon or find_certi_img("certi.png", th=0.85) or find_certi_img("ticket2.png", th=0.85):
                                    resume_fsm, resume_desc = "CERTI_FIND_OK2_FIRST", "인게임 팝업(ok2.png)"
                                else:
                                    resume_fsm, resume_desc = "CERTI_TICKET_OK2_FIND", "런처 팝업(ok2.png)"
                            elif has_quit:
                                resume_fsm, resume_desc = "CERTI_FIND_QUIT", "인게임 종료(quit.png)"
                            elif find_certi_img("17.png", th=0.82):
                                resume_fsm, resume_desc = "CERTI_STEP_17_FIND", "캐릭터 입장(17.png)"
                            elif find_certi_img("login.png", th=0.82) or find_certi_img("ticket.png", th=0.82):
                                resume_fsm, resume_desc = "CERTI_AFTER_16_BRANCH", "로그인/이용권(login/ticket)"
                            elif find_certi_img("16.png", th=0.82):
                                resume_fsm, resume_desc = "CERTI_STEP_16_FIND", "런처 16단계(16.png)"
                            elif find_certi_img("15.png", th=0.82):
                                resume_fsm, resume_desc = "CERTI_STEP_15_FIND", "런처 15단계(15.png)"
                            elif find_certi_img("14.png", th=0.82):
                                resume_fsm, resume_desc = "CERTI_WAIT_GAME_LAUNCH", "런처 14단계(14.png)"
                            elif find_certi_img("waiting.png", th=0.82):
                                state["certi_waiting_seen"] = True
                                state["certi_launch_time"] = curr_time
                                resume_fsm, resume_desc = "CERTI_WAIT_GAME_LAUNCH", "게임 구동 대기중(waiting.png)"
                            elif has_dragon:
                                resume_fsm, resume_desc = "CERTI_WAIT_DRAGON", "인게임 접속 완료(dragon.png)"

                        if resume_fsm is not None:
                            web_stage_set = {
                                "CERTI_STEP_2_FIND", "CERTI_STEP_3_FIND", "CERTI_STEP_5_FIND",
                                "CERTI_STEP_7_FIND", "CERTI_STEP_8_FIND", "CERTI_STEP_8_BRANCH",
                                "CERTI_CAPTCHA_SOLVE", "CERTI_CAPTCHA_CLICK_NEXT", "CERTI_CAPTCHA_SCROLL",
                                "CERTI_CAPTCHA_AFTER_CONFIRM", "CERTI_CAPTCHA_MANUAL_WAIT", "CERTI_WAIT_SUC"
                            }
                            if resume_fsm not in web_stage_set:
                                release_central_ip_lock_async(key)
                            dprint(key, f"✅ [화면 자동 인식 성공] [{resume_desc}] ➔ ({resume_fsm}) 단계부터 진행합니다!")
                            state["certi_web_last_fsm"] = None
                            state["certi_web_step_start"] = curr_time
                            state["target_fsm"] = resume_fsm
                            state["cooldown"] = curr_time + 0.25
                        elif curr_time - state.get("certi_resume_scan_start", curr_time) < 3.5:
                            state["cooldown"] = curr_time + 0.2
                        else:
                            prev_f = state.get("certi_fsm_before_manual", "CERTI_GOTO_DESKTOP")
                            pre_web_set = {"CERTI_DELAY_WAIT", "CERTI_GOTO_DESKTOP", "CERTI_WAIT_IP_LOCK", "CERTI_STEP_1_FIND"}
                            web_progress_set = {
                                "CERTI_STEP_2_FIND", "CERTI_STEP_3_FIND", "CERTI_STEP_5_FIND",
                                "CERTI_STEP_7_FIND", "CERTI_STEP_8_FIND", "CERTI_STEP_8_BRANCH",
                                "CERTI_CAPTCHA_SOLVE", "CERTI_CAPTCHA_CLICK_NEXT", "CERTI_CAPTCHA_SCROLL",
                                "CERTI_CAPTCHA_AFTER_CONFIRM", "CERTI_CAPTCHA_MANUAL_WAIT", "CERTI_WAIT_SUC"
                            }
                            is_desktop_visible = (
                                find_certi_img("13.png", th=0.82) is not None or
                                find_certi_img("1.png", th=0.82) is not None or
                                find_certi_img("sub.png", th=0.82) is not None
                            )
                            if prev_f in pre_web_set:
                                state["target_fsm"] = "CERTI_WAIT_IP_LOCK"
                            elif prev_f in web_progress_set and not is_desktop_visible:
                                fallback_web_fsm = state.get("captcha_return_fsm", "CERTI_STEP_8_BRANCH") if prev_f.startswith("CERTI_CAPTCHA") else prev_f
                                dprint(key, f"🌐 [웹 단계 연속 진행] 브라우저 화면 유지 확인! [{fallback_web_fsm}] 단계를 이어갑니다.")
                                state["certi_web_last_fsm"] = None
                                state["certi_web_step_start"] = curr_time
                                state["target_fsm"] = fallback_web_fsm
                            else:
                                release_central_ip_lock_async(key)
                                if find_certi_img("12.png", th=0.82, roi_rect=(0, 550, 800, 600)) and not state.get("certi_from_closed_game", False):
                                    state["target_fsm"] = "CERTI_STEP_12_FIND"
                                else:
                                    state["certi_13_wait_mode"] = "CLOSED_START"
                                    state["certi_next_desktop_time"] = 0.0
                                    state["target_fsm"] = "CERTI_STEP_13_FIND"
                            state["cooldown"] = curr_time + 0.3

                    elif current_fsm == "CERTI_CAPTCHA_MANUAL_WAIT":
                        ret_fsm = state.get("captcha_return_fsm", "CERTI_STEP_8_BRANCH")
                        save_unseen_banner_if_needed(img_bgr)
                        if settings.get("auth_auto_captcha", False):
                            state["target_fsm"] = "CERTI_CAPTCHA_SOLVE"
                            state["cooldown"] = curr_time + 0.2
                        elif find_certi_img("suc.png", th=0.82):
                            state["certi_web_last_fsm"] = None
                            state["target_fsm"] = "CERTI_WAIT_SUC"
                            state["cooldown"] = curr_time + 0.1
                        elif find_certi_img("fail.png", th=0.82) or find_certi_img("9.png", th=0.80) or find_certi_img("10.png", th=0.80):
                            state["certi_web_last_fsm"] = None
                            state["certi_web_step_start"] = curr_time
                            state["target_fsm"] = "CERTI_STEP_8_BRANCH"
                            state["cooldown"] = curr_time + 0.1
                        elif ret_fsm == "CERTI_STEP_5_FIND" and find_certi_img("5.png", th=0.82):
                            state["certi_web_last_fsm"] = None
                            state["certi_web_step_start"] = curr_time
                            state["target_fsm"] = "CERTI_STEP_5_FIND"
                            state["cooldown"] = curr_time + 0.1
                        elif ret_fsm == "CERTI_STEP_7_FIND" and find_certi_img("7.png", th=0.82):
                            state["certi_web_last_fsm"] = None
                            state["certi_web_step_start"] = curr_time
                            state["target_fsm"] = "CERTI_STEP_7_FIND"
                            state["cooldown"] = curr_time + 0.1
                        elif find_certi_img("8.png", th=0.82) and not find_any_captcha_img(th=0.75):
                            state["certi_web_last_fsm"] = None
                            state["certi_web_step_start"] = curr_time
                            state["target_fsm"] = "CERTI_STEP_8_FIND"
                            state["cooldown"] = curr_time + 0.1
                        else:
                            if curr_time - state.get("captcha_tts_last_time", 0.0) >= 15.0:
                                threading.Thread(target=play_tts_alert, args=(f"통제실 {key} 캡차 대기중",), daemon=True).start()
                                state["captcha_tts_last_time"] = curr_time
                            state["cooldown"] = curr_time + 0.3

                    elif current_fsm == "CERTI_DELAY_WAIT":
                        rem_sec = state.get("certi_delay_until", 0.0) - curr_time
                        if rem_sec <= 0:
                            state["target_fsm"] = "CERTI_GOTO_DESKTOP"
                            state["cooldown"] = curr_time + 0.1
                        else:
                            state["cooldown"] = curr_time + 0.5

                    elif current_fsm == "CERTI_GOTO_DESKTOP":
                        state["certi_fail_streak"] = 0
                        state["certi_last_box"] = None
                        my_num = get_my_central_num()
                        saved_c = str(state.get("certi_curr_central") or saved_settings.get(key, {}).get("certi_curr_central") or "").strip()
                        if saved_c not in CENTRAL_ORDER:
                            saved_c = my_num
                        alive_nums = {c_n for c_n, _ in ALIVE_OTHER_PROXIES}
                        if saved_c != my_num and alive_nums and saved_c not in alive_nums:
                            saved_c = get_next_central_in_order(saved_c)
                        state["certi_curr_central"] = saved_c
                        if saved_c == my_num:
                            state["certi_use_sub"] = False
                        else:
                            state["certi_use_sub"] = True
                            CURRENT_PROXY_TARGET_NUM[key] = saved_c
                        pico_queues[key].put({"action": "HOME_MACRO"})
                        state["certi_ip_lock_log_time"] = 0.0
                        state["target_fsm"] = "CERTI_WAIT_IP_LOCK"
                        state["cooldown"] = curr_time + 1.5

                    elif current_fsm == "CERTI_WAIT_IP_LOCK":
                        my_num = get_my_central_num()
                        target_c = str(state.get("certi_curr_central") or my_num).strip()
                        ok, msg = request_central_ip_lock(key, target_c, action="ACQUIRE")
                        if ok:
                            state["certi_locked_central"] = target_c
                            state["certi_lock_hb_time"] = curr_time
                            if target_c == my_num:
                                state["certi_use_sub"] = False
                                dprint(key, f"🔒 [IP 순차 승인] 커맨드컴(12번 공유회선) 사용권 획득! '1.png' 인증을 시작합니다.")
                            else:
                                state["certi_use_sub"] = True
                                CURRENT_PROXY_TARGET_NUM[key] = target_c
                                dprint(key, f"🔒 [IP 순차 승인] [{target_c}번 중앙컴] 프록시 사용권 획득! 'sub.png' 인증을 시작합니다.")
                            state["target_fsm"] = "CERTI_STEP_1_FIND"
                            state["cooldown"] = curr_time + 0.1
                        else:
                            if msg.startswith("OFFLINE"):
                                state["certi_curr_central"] = get_next_central_in_order(target_c)
                                state["cooldown"] = curr_time + 0.2
                            else:
                                if curr_time - state.get("certi_ip_lock_log_time", 0.0) >= 5.0:
                                    dprint(key, f"⏳ [{target_c}번 회선 대기] {msg} ➔ 앞선 인증 종료 후 자동 출발합니다.")
                                    state["certi_ip_lock_log_time"] = curr_time
                                state["cooldown"] = curr_time + 1.0

                    elif current_fsm == "CERTI_MOVE_VERIFY":
                        if state.pop("special_ack_arrived", False) or curr_time > state.get("certi_ack_timeout", 0):
                            tx, ty = state.get("certi_target_pos", (400, 300))
                            t_text = state.get("certi_type_text")
                            strict_aim = state.get("certi_strict_aim", False)
                            need_correction = False
                            if strict_aim:
                                real_c = find_cursor_pos(img_bgr, last_pos=(tx, ty), allow_full_scan=True, is_certi_mode="WEB")
                                if real_c:
                                    state["cursor_pos"] = list(real_c)
                                    err_dist = math.hypot(tx - real_c[0], ty - real_c[1])
                                    if err_dist > 2.5 and state.get("certi_corr_cnt", 0) < 3:
                                        need_correction = True
                                        dur_c = apply_human_variance(0.06 + 0.03 * math.log2((err_dist / 20.0) + 1.0))
                                        deltas_c = generate_human_deltas(tx - real_c[0], ty - real_c[1], duration=dur_c, behavior="CERTI", key=key)
                                        if deltas_c:
                                            pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": deltas_c})
                                        pico_queues[key].put({"action": "SPECIAL_ACK"})
                                        state["special_ack_arrived"] = False
                                        state["cursor_pos"] = [tx, ty]
                                        state["certi_corr_cnt"] = state.get("certi_corr_cnt", 0) + 1
                                        state["certi_ack_timeout"] = curr_time + dur_c + 1.0
                                        state["cooldown"] = curr_time + 0.05

                            if not need_correction:
                                is_dbl = state.get("certi_click_double", False)
                                p_enter = state.get("certi_press_enter", False)
                                next_fsm_val = state.get("certi_next_fsm", "IDLE")
                                post_wait_val = state.get("certi_post_wait", 0.5)
                                pico_queues[key].put({"action": "CERTI_CLICK", "double": is_dbl})
                                if t_text is not None:
                                    state["cursor_pos"] = [tx, ty]
                                    pico_queues[key].put({"action": "WAIT", "delay_min": 0.22, "delay_max": 0.40})
                                    pico_queues[key].put({"action": "TYPE_STRING", "text": t_text, "clear_first": False, "press_enter": p_enter})
                                state["target_fsm"] = next_fsm_val
                                state["cooldown"] = curr_time + post_wait_val
                        else:
                            state["cooldown"] = curr_time + 0.03

                    elif current_fsm == "CERTI_STEP_1_FIND":
                        use_sub_now = state.get("certi_use_sub", False)
                        pos = (find_certi_img("sub.png", th=0.82) or find_certi_img("qq/sub.png", th=0.82)) if use_sub_now else find_certi_img("1.png", th=0.82)
                        if pos:
                            if use_sub_now:
                                t_num = CURRENT_PROXY_TARGET_NUM.get(key) or state.get("certi_curr_central") or get_next_central_in_order(get_my_central_num())
                                CURRENT_PROXY_TARGET_NUM[key] = t_num
                            start_certi_move_and_action(pos[0], pos[1], next_fsm="CERTI_STEP_2_FIND", double=True, use_jitter=False, desc="웹창 열기")
                        else:
                            state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_2_FIND":
                        pos = find_certi_img("2.png", th=0.82)
                        if pos: start_certi_move_and_action(pos[0], pos[1], next_fsm="CERTI_STEP_3_FIND", double=False, desc="2.png 클릭")
                        else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_3_FIND":
                        pos = find_certi_img("3.png", th=0.82)
                        if pos:
                            start_certi_move_and_action(pos[0], pos[1], next_fsm="CERTI_STEP_5_FIND", double=False, type_text=curr_acc_id, press_enter=True, desc="3.png 계정입력")
                        else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_5_FIND":
                        if find_any_captcha_img(th=0.75):
                            state["captcha_return_fsm"] = "CERTI_STEP_5_FIND"
                            state["captcha_test_round"] = 1
                            state["captcha_is_scrolled_down"] = False
                            state["captcha_scroll_cnt"] = 0
                            state["captcha_need_new"] = False
                            state["target_fsm"] = "CERTI_CAPTCHA_SOLVE" if settings.get("auth_auto_captcha", False) else "CERTI_CAPTCHA_MANUAL_WAIT"
                            state["cooldown"] = curr_time + 2.0
                        else:
                            pos = find_certi_img("5.png", th=0.82)
                            if pos:
                                pico_queues[key].put({"action": "WAIT", "delay_min": 0.22, "delay_max": 0.38})
                                pico_queues[key].put({"action": "TYPE_STRING", "text": curr_acc_pw, "clear_first": False, "press_enter": True})
                                state["target_fsm"] = "CERTI_STEP_7_FIND"
                                state["cooldown"] = curr_time + 0.8
                            else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_7_FIND":
                        if find_any_captcha_img(th=0.75):
                            state["captcha_return_fsm"] = "CERTI_STEP_7_FIND"
                            state["captcha_test_round"] = 1
                            state["captcha_is_scrolled_down"] = False
                            state["captcha_scroll_cnt"] = 0
                            state["captcha_need_new"] = False
                            state["target_fsm"] = "CERTI_CAPTCHA_SOLVE" if settings.get("auth_auto_captcha", False) else "CERTI_CAPTCHA_MANUAL_WAIT"
                            state["cooldown"] = curr_time + 2.0
                        else:
                            pos = find_certi_img("7.png", th=0.82, roi_rect=(0, 0, w, max(100, h - 200)))
                            if pos: start_certi_move_and_action(pos[0], pos[1], next_fsm="CERTI_STEP_8_FIND", double=False, desc="7.png 클릭")
                            else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_8_FIND":
                        pos = find_certi_img("8.png", th=0.82)
                        if pos: start_certi_move_and_action(pos[0], pos[1], next_fsm="CERTI_STEP_8_BRANCH", double=False, desc="8.png 클릭")
                        else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_8_BRANCH":
                        if find_certi_img("fail.png", th=0.82):
                            release_central_ip_lock_async(key)
                            pico_queues[key].put({"action": "WAIT", "delay_min": 0.2, "delay_max": 0.35})
                            pico_queues[key].put({"action": "CLOSE_TAB"})
                            my_num = get_my_central_num()
                            prev_c = str(state.get("certi_curr_central") or my_num).strip()
                            if not state.get("certi_use_sub", False): prev_c = my_num
                            streak = state.get("certi_fail_streak", 0) + 1
                            state["certi_fail_streak"] = streak
                            max_lines = (len(ALIVE_OTHER_PROXIES) + 1) if ALIVE_OTHER_PROXIES else len(CENTRAL_ORDER)
                            if streak >= max_lines:
                                threading.Thread(target=play_tts_alert, args=(f"통제실 {key} 인증 회선 소진",), daemon=True).start()
                                state["is_paused"] = True
                                state["target_fsm"] = "IDLE"
                                state["cooldown"] = curr_time + 1.0
                            else:
                                next_c = get_next_central_in_order(prev_c)
                                state["certi_curr_central"] = next_c
                                if key not in saved_settings: saved_settings[key] = {}
                                saved_settings[key]["certi_curr_central"] = next_c
                                save_settings()
                                if next_c == my_num:
                                    state["certi_use_sub"] = False
                                else:
                                    state["certi_use_sub"] = True
                                    CURRENT_PROXY_TARGET_NUM[key] = next_c
                                state["certi_web_last_fsm"] = None
                                state["target_fsm"] = "CERTI_WAIT_IP_LOCK"
                                state["cooldown"] = curr_time + 1.2
                        elif find_any_captcha_img(th=0.75):
                            state["captcha_return_fsm"] = "CERTI_STEP_8_BRANCH"
                            state["captcha_test_round"] = 1
                            state["captcha_is_scrolled_down"] = False
                            state["captcha_scroll_cnt"] = 0
                            state["captcha_need_new"] = False
                            state["target_fsm"] = "CERTI_CAPTCHA_SOLVE" if settings.get("auth_auto_captcha", False) else "CERTI_CAPTCHA_MANUAL_WAIT"
                            state["cooldown"] = curr_time + 2.0
                        else:
                            pos_9 = find_certi_img("9.png", th=0.0)
                            box_9 = state.get("certi_last_box") if pos_9 else None
                            score_9 = box_9[5] if box_9 else 0.0
                            pos_10 = find_certi_img("10.png", th=0.0)
                            box_10 = state.get("certi_last_box") if pos_10 else None
                            score_10 = box_10[5] if box_10 else 0.0
                            if max(score_9, score_10) >= 0.80:
                                if score_9 >= score_10 and pos_9:
                                    state["certi_last_box"] = box_9
                                    start_certi_move_and_action(pos_9[0], pos_9[1], next_fsm="CERTI_WAIT_SUC", double=False, type_text=curr_acc_email, press_enter=True, desc="9.png 메일입력")
                                elif pos_10:
                                    state["certi_last_box"] = box_10
                                    start_certi_move_and_action(pos_10[0], pos_10[1], next_fsm="CERTI_WAIT_SUC", double=False, type_text=curr_acc_phone, press_enter=True, desc="10.png 전번입력")
                            else:
                                state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_CAPTCHA_SOLVE":
                        round_num = state.get("captcha_test_round", 1)
                        real_c = find_cursor_pos(img_bgr, last_pos=state.get("cursor_pos", [400, 300]), allow_full_scan=True, is_certi_mode="WEB")
                        cur_x, cur_y = real_c if real_c else state.get("cursor_pos", [400, 300])
                        state["cursor_pos"] = [cur_x, cur_y]
                        if state.get("captcha_is_scrolled_down", False):
                            if not (280 <= cur_x <= 510 and 200 <= cur_y <= 500):
                                tx, ty = 397 + int(round(g_val(-15, 15))), 350 + int(round(g_val(-15, 15)))
                                dur_m = apply_human_variance(0.10 + 0.035 * math.log2((math.hypot(tx - cur_x, ty - cur_y) / 20.0) + 1.0))
                                pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": generate_human_deltas(tx - cur_x, ty - cur_y, duration=dur_m, behavior="CERTI", key=key)})
                                pico_queues[key].put({"action": "WAIT", "delay_min": 0.10, "delay_max": 0.18})
                                state["cursor_pos"] = [tx, ty]
                            pico_queues[key].put({"action": "MOUSE_WHEEL", "amount": 5})
                            pico_queues[key].put({"action": "WAIT", "delay_min": 0.45, "delay_max": 0.65})
                            state["captcha_is_scrolled_down"] = False
                            state["cooldown"] = curr_time + 2.0
                            continue

                        click_targets = analyze_captcha_with_gemini(img_bgr)
                        state["captcha_word_matched"] = globals().get("_LAST_CAPTCHA_WORD_MATCHED", False)
                        if click_targets:
                            state["captcha_need_new"] = False
                            state["captcha_target_queue"] = list(click_targets)
                            state["captcha_scroll_cnt"] = 0
                            state["target_fsm"] = "CERTI_CAPTCHA_CLICK_NEXT"
                            state["cooldown"] = curr_time + 0.05
                        else:
                            state["captcha_need_new"] = True
                            tx, ty = 397 + int(round(g_val(-10, 10))), 380 + int(round(g_val(-10, 10)))
                            dx, dy = tx - cur_x, ty - cur_y
                            dist = math.hypot(dx, dy)
                            total_move_dur = 0.0
                            if dist > 10:
                                dur = apply_human_variance(0.10 + 0.035 * math.log2((dist / 20.0) + 1.0))
                                pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": generate_human_deltas(dx, dy, duration=dur, behavior="CERTI", key=key)})
                                state["cursor_pos"] = [tx, ty]
                                total_move_dur += dur
                            state["captcha_scroll_cnt"] = 0
                            state["target_fsm"] = "CERTI_CAPTCHA_SCROLL"
                            state["cooldown"] = curr_time + total_move_dur + 0.4

                    elif current_fsm == "CERTI_CAPTCHA_CLICK_NEXT":
                        t_queue = state.get("captcha_target_queue", [])
                        if t_queue:
                            tx, ty = t_queue.pop(0)
                            state["captcha_target_queue"] = t_queue
                            safe_tx = int(max(10, min(w - 10, tx + int(round(g_val(-2, 2))))))
                            safe_ty = int(max(10, min(h - 10, ty + int(round(g_val(-2, 2))))))
                            start_certi_move_and_action(safe_tx, safe_ty, next_fsm="CERTI_CAPTCHA_CLICK_NEXT", double=False, use_jitter=False, post_wait=g_val(0.28, 0.42), desc="캡차 타일 클릭")
                        else:
                            state["captcha_scroll_cnt"] = 0
                            state["target_fsm"] = "CERTI_CAPTCHA_SCROLL"
                            state["cooldown"] = curr_time + g_val(0.35, 0.50)

                    elif current_fsm == "CERTI_CAPTCHA_SCROLL":
                        if not state.get("captcha_is_scrolled_down", False):
                            cur_x, cur_y = state.get("cursor_pos", [400, 300])
                            safe_tx = 397 + int(round(g_val(-15, 15)))
                            safe_ty = 315 + int(round(g_val(-10, 10)))
                            move_dur = 0.0
                            if math.hypot(safe_tx - cur_x, safe_ty - cur_y) > 15:
                                move_dur = apply_human_variance(0.08 + 0.03 * math.log2((math.hypot(safe_tx - cur_x, safe_ty - cur_y) / 20.0) + 1.0))
                                pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": generate_human_deltas(safe_tx - cur_x, safe_ty - cur_y, duration=move_dur, behavior="CERTI", key=key)})
                                pico_queues[key].put({"action": "WAIT", "delay_min": 0.08, "delay_max": 0.14})
                                state["cursor_pos"] = [safe_tx, safe_ty]

                            pico_queues[key].put({"action": "MOUSE_WHEEL", "amount": -5})
                            pico_queues[key].put({"action": "WAIT", "delay_min": 0.45, "delay_max": 0.65})
                            state["captcha_is_scrolled_down"] = True
                            state["captcha_scroll_cnt"] = 1
                            state["cooldown"] = curr_time + move_dur + 0.9
                            continue

                        def find_captcha_bottom_btn(btn_name, th=0.78):
                            return find_certi_img(btn_name, th=th, roi_rect=(250, 380, 550, 595))

                        if state.get("captcha_need_new", False):
                            if state.get("captcha_word_matched", globals().get("_LAST_CAPTCHA_WORD_MATCHED", False)):
                                # 제시어는 매칭되었으나 해당 사물 타일이 0개인 경우 -> skip(건너뛰기)을 1순위로 클릭!
                                pos_btn = find_captcha_bottom_btn("skip.png", th=0.78) or find_captcha_bottom_btn("new.png", th=0.78)
                                btn_label = "skip(건너뛰기 우선)/new"
                            else:
                                # words 폴더에 없는 미등록 제시어인 경우 -> new(새로고침)를 1순위로 클릭!
                                pos_btn = find_captcha_bottom_btn("new.png", th=0.78) or find_captcha_bottom_btn("skip.png", th=0.78)
                                btn_label = "new(미등록 제시어 새로고침)/skip"
                        else:
                            # 🚨 타일을 정상적으로 찍고 내려왔을 때는 confirm(확인) -> next(다음) -> skip(건너뛰기) 순으로 탐색!
                            pos_btn = (
                                find_captcha_bottom_btn("confirm.png", th=0.78) or
                                find_captcha_bottom_btn("next.png", th=0.78) or
                                find_captcha_bottom_btn("skip.png", th=0.78)
                            )
                            btn_label = "confirm(확인)/next(다음)/skip"

                        if pos_btn:
                            state["captcha_scroll_cnt"] = 0
                            start_certi_move_and_action(pos_btn[0], pos_btn[1], next_fsm="CERTI_CAPTCHA_AFTER_CONFIRM", double=False, post_wait=1.5, desc=f"캡차 {btn_label} 클릭")
                        elif state.get("captcha_scroll_cnt", 0) < 3:
                            pico_queues[key].put({"action": "MOUSE_WHEEL", "amount": -5})
                            pico_queues[key].put({"action": "WAIT", "delay_min": 0.4, "delay_max": 0.6})
                            state["captcha_is_scrolled_down"] = True
                            state["captcha_scroll_cnt"] = state.get("captcha_scroll_cnt", 0) + 1
                            state["cooldown"] = curr_time + 0.9
                        else:
                            state["captcha_is_scrolled_down"] = True
                            state["target_fsm"] = "CERTI_CAPTCHA_AFTER_CONFIRM"
                            state["cooldown"] = curr_time + 0.3

                    elif current_fsm == "CERTI_CAPTCHA_AFTER_CONFIRM":
                        if state.get("captcha_is_scrolled_down", False):
                            pico_queues[key].put({"action": "MOUSE_WHEEL", "amount": 5})
                            pico_queues[key].put({"action": "WAIT", "delay_min": 0.25, "delay_max": 0.35})
                            pico_queues[key].put({"action": "MOUSE_WHEEL", "amount": 5})
                            pico_queues[key].put({"action": "WAIT", "delay_min": 0.5, "delay_max": 0.7})
                            state["captcha_is_scrolled_down"] = False
                            state["cooldown"] = curr_time + 1.0
                            continue
                        ret_fsm = state.get("captcha_return_fsm", "CERTI_STEP_8_BRANCH")
                        if ret_fsm == "CERTI_STEP_5_FIND" and find_certi_img("5.png", th=0.82):
                            state["target_fsm"] = "CERTI_STEP_5_FIND"; state["cooldown"] = curr_time + 0.1; continue
                        if ret_fsm == "CERTI_STEP_7_FIND" and find_certi_img("7.png", th=0.82):
                            state["target_fsm"] = "CERTI_STEP_7_FIND"; state["cooldown"] = curr_time + 0.1; continue
                        if ret_fsm == "CERTI_STEP_8_BRANCH" and (find_certi_img("fail.png", th=0.82) or find_certi_img("9.png", th=0.80) or find_certi_img("10.png", th=0.80)):
                            state["target_fsm"] = "CERTI_STEP_8_BRANCH"; state["cooldown"] = curr_time + 0.1; continue
                        if find_any_captcha_img(th=0.75):
                            next_round = state.get("captcha_test_round", 1) + 1
                            state["captcha_test_round"] = next_round
                            if next_round <= 12:
                                state["captcha_scroll_cnt"] = 0
                                state["captcha_need_new"] = False
                                state["target_fsm"] = "CERTI_CAPTCHA_SOLVE"
                                state["cooldown"] = curr_time + 2.0
                            else:
                                pico_queues[key].put({"action": "CLOSE_TAB"})
                                state["target_fsm"] = "CERTI_STEP_1_FIND"
                                state["cooldown"] = curr_time + 1.2
                        else:
                            state["target_fsm"] = ret_fsm
                            state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_WAIT_SUC":
                        if find_certi_img("suc.png", th=0.82):
                            release_central_ip_lock_async(key)
                            pico_queues[key].put({"action": "WAIT", "delay_min": 0.2, "delay_max": 0.35})
                            pico_queues[key].put({"action": "CLOSE_TAB"})
                            if state.get("certi_from_closed_game", False):
                                state["certi_from_closed_game"] = False
                                state["certi_13_wait_mode"] = "CLOSED_START"
                                state["certi_next_desktop_time"] = curr_time + 2.5
                                state["target_fsm"] = "CERTI_STEP_13_FIND"
                                state["cooldown"] = curr_time + 1.2
                                dprint(key, "✅ [웹 인증 성공 ➔ 13.png 직행] '웹인증➔접속' 모드이므로 12.png를 건너뛰고 바탕화면 13.png(게임 실행)로 바로 이동합니다!")
                            else:
                                state["certi_12_find_start"] = curr_time + 1.0
                                state["target_fsm"] = "CERTI_STEP_12_FIND"
                                state["cooldown"] = curr_time + 1.0
                        else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_12_FIND":
                        pos_12 = find_certi_img("12.png", th=0.82, roi_rect=(0, 550, 800, 600))
                        if pos_12:
                            state["certi_from_closed_game"] = False
                            start_certi_move_and_action(pos_12[0], pos_12[1], next_fsm="CERTI_FIND_OK2_FIRST", double=False, post_wait=0.8, desc="12.png 리니지창 활성화")
                        elif curr_time - state.get("certi_12_find_start", curr_time) >= 3.0:
                            state["certi_from_closed_game"] = False
                            state["certi_13_wait_mode"] = "CLOSED_START"
                            state["certi_next_desktop_time"] = curr_time + 2.0
                            state["target_fsm"] = "CERTI_STEP_13_FIND"
                            state["cooldown"] = curr_time + 0.2
                        else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_FIND_OK2_FIRST":
                        pos_ok2 = find_certi_img("ok2.png", th=0.82)
                        if pos_ok2: start_certi_move_and_action(pos_ok2[0], pos_ok2[1], next_fsm="CERTI_FIND_QUIT", double=False, post_wait=0.6, desc="ok2.png 팝업 닫기")
                        else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_FIND_QUIT":
                        pos_quit = find_certi_img("quit.png", th=0.82)
                        if pos_quit:
                            state["certi_13_wait_mode"] = "NORMAL"
                            state["certi_next_desktop_time"] = 0.0
                            start_certi_move_and_action(pos_quit[0], pos_quit[1], next_fsm="CERTI_STEP_13_FIND", double=False, post_wait=3.0, desc="quit.png 게임 종료")
                        else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_13_FIND":
                        pos_13 = find_certi_img("13.png", th=0.82)
                        if pos_13:
                            w_mode = state.get("certi_13_wait_mode", "NORMAL")
                            wait_sec = g_val(7.0, 10.0) if w_mode == "TICKET" else (g_val(1.2, 2.0) if w_mode in ["RETRY_1MIN", "CLOSED_START"] else g_val(10.0, 20.0))
                            state["certi_13_saved_pos"] = pos_13
                            state["certi_13_exec_time"] = curr_time + wait_sec
                            state["target_fsm"] = "CERTI_STEP_13_WAIT_BEFORE_EXEC"
                            state["cooldown"] = curr_time + 0.2
                        elif curr_time >= state.get("certi_next_desktop_time", 0):
                            pico_queues[key].put({"action": "HOME_MACRO"})
                            state["certi_next_desktop_time"] = curr_time + g_val(2.5, 3.5)
                            state["cooldown"] = curr_time + 0.8
                        else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_13_WAIT_BEFORE_EXEC":
                        if curr_time >= state.get("certi_13_exec_time", 0):
                            pos_13 = find_certi_img("13.png", th=0.82) or state.get("certi_13_saved_pos")
                            if pos_13:
                                start_certi_move_and_action(pos_13[0], pos_13[1], next_fsm="CERTI_LAUNCH_TIMER_INIT", double=True, use_jitter=False, post_wait=1.0, desc="13.png 실행")
                            else:
                                state["certi_next_desktop_time"] = 0.0
                                state["target_fsm"] = "CERTI_STEP_13_FIND"
                                state["cooldown"] = curr_time + 0.2
                        else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_LAUNCH_TIMER_INIT":
                        state["certi_launch_time"] = curr_time
                        state["certi_waiting_seen"] = False
                        state["certi_delay_seen_time"] = 0.0
                        state["certi_rec_seen_time"] = 0.0
                        state["certi_rec_miss_cnt"] = 0
                        state["target_fsm"] = "CERTI_WAIT_GAME_LAUNCH"
                        state["cooldown"] = curr_time + 0.2
                        dprint(key, "👀 [구동 감시 시작] 'purple.png', 'waiting.png', 'rec.png'(10초), 'delay.png'(10초), '14.png' 및 recerti 감지를 시작합니다.")

                    elif current_fsm == "CERTI_WAIT_GAME_LAUNCH":
                        pos_re, re_name = find_any_recerti_img(th=0.82)
                        if pos_re:
                            state["certi_rec_seen_time"] = 0.0
                            handle_recerti_branch(pos_re, re_name, "구동 중 재인증/오류")
                        else:
                            pos_14 = find_certi_img("14.png", th=0.82)
                            if pos_14:
                                state["certi_delay_seen_time"] = 0.0
                                state["certi_rec_seen_time"] = 0.0
                                start_certi_move_and_action(pos_14[0], pos_14[1], next_fsm="CERTI_STEP_15_FIND", double=False, post_wait=0.6, desc="14.png 클릭")
                            else:
                                # 0) 퍼플 꺼짐 팝업(purple.png) 감지 시 즉시 yse.png 클릭 단계로 이동!
                                pos_purple = find_certi_img("purple.png", th=0.82) if curr_time >= state.get("certi_purple_cd", 0.0) else None
                                if pos_purple:
                                    state["certi_delay_seen_time"] = 0.0
                                    state["certi_rec_seen_time"] = 0.0
                                    state["certi_rec_miss_cnt"] = 0
                                    state["certi_purple_find_start"] = curr_time
                                    state["certi_purple_evaded"] = False
                                    dprint(key, f"🟣 [퍼플 미실행 감지] 'purple.png' 포착({pos_purple[0]}, {pos_purple[1]})! 'yse.png'를 찾아 원클릭하여 퍼플 자동 로그인 및 게임 실행을 진행합니다.")
                                    state["target_fsm"] = "CERTI_PURPLE_YSE_FIND"
                                    state["cooldown"] = curr_time + 0.1
                                    continue

                                # 1) delay.png 감지 및 10초 경과 시 강종(recerti) 전환 체크
                                delay_t = state.get("certi_delay_seen_time", 0.0)
                                if delay_t == 0.0:
                                    pos_delay = find_certi_img("delay.png", th=0.82) or find_certi_img("recerti/delay.png", th=0.82)
                                    if pos_delay:
                                        state["certi_delay_seen_time"] = curr_time
                                        dprint(key, f"⏳ [delay.png 감지] ({pos_delay[0]}, {pos_delay[1]}) 포착! 10초 내로 '14.png'가 뜨지 않으면 강종 후 재인증을 진행합니다.")

                                if state.get("certi_delay_seen_time", 0.0) > 0.0 and (curr_time - state["certi_delay_seen_time"] >= 10.0):
                                    dprint(key, "🚨 [delay.png 10초 타임아웃] 'delay.png' 매칭 후 10초가 지나도 '14.png'가 확인되지 않아 강종 후 재인증(recerti)으로 넘어갑니다!")
                                    state["certi_delay_seen_time"] = 0.0
                                    state["certi_rec_seen_time"] = 0.0
                                    clear_movements_only(pico_queues[key])
                                    pico_queues[key].put({"action": "HOME_MACRO"})
                                    state["target_fsm"] = "CERTI_RECERTI_OPEN_TM"
                                    state["cooldown"] = curr_time + g_val(1.2, 1.6)
                                else:
                                    # 2) waiting.png 미출현 상태에서 rec.png / rec2.png / rec3.png 10초 지속 감지 및 1분 타임아웃 체크
                                    if not state.get("certi_waiting_seen", False):
                                        pos_wait = find_certi_img("waiting.png", th=0.82)
                                        if pos_wait:
                                            state["certi_waiting_seen"] = True
                                            state["certi_rec_seen_time"] = 0.0
                                            state["certi_rec_miss_cnt"] = 0
                                            dprint(key, "✅ [정상 구동 확인] 'waiting.png' 감지됨! (rec~3 감시 해제) 이제 14.png가 뜰 때까지 대기합니다.")
                                        else:
                                            pos_rec, rec_name = None, ""
                                            for r_fname in ("rec.png", "rec2.png", "rec3.png"):
                                                pos_rec = find_certi_img(r_fname, th=0.82) or find_certi_img(f"recerti/{r_fname}", th=0.82)
                                                if pos_rec:
                                                    rec_name = r_fname
                                                    break

                                            if pos_rec:
                                                state["certi_rec_miss_cnt"] = 0
                                                if state.get("certi_rec_seen_time", 0.0) == 0.0:
                                                    state["certi_rec_seen_time"] = curr_time
                                                    dprint(key, f"⏳ [{rec_name} 감지] ({pos_rec[0]}, {pos_rec[1]}) 포착! 'waiting.png' 없이 10초간 지속 감지 시 즉시 재인증으로 이동합니다.")
                                                elif curr_time - state["certi_rec_seen_time"] >= 10.0:
                                                    dprint(key, f"🚨 [{rec_name} 10초 연속 감지 확정] 'waiting.png' 미출현 상태로 10초간 '{rec_name}'가 유지되어 즉시 바탕화면 이동 후 재인증을 시작합니다!")
                                                    state["certi_rec_seen_time"] = 0.0
                                                    clear_movements_only(pico_queues[key])
                                                    state["certi_from_closed_game"] = True
                                                    state["target_fsm"] = "CERTI_GOTO_DESKTOP"
                                                    state["cooldown"] = curr_time + 0.2
                                                    continue
                                            else:
                                                if state.get("certi_rec_seen_time", 0.0) > 0.0:
                                                    state["certi_rec_miss_cnt"] = state.get("certi_rec_miss_cnt", 0) + 1
                                                    if state["certi_rec_miss_cnt"] >= 3:
                                                        dprint(key, "✅ [rec~3 사라짐 확인] 10초 이내에 rec~3 이미지가 화면에서 사라졌으므로 재인증 타이머를 초기화합니다.")
                                                        state["certi_rec_seen_time"] = 0.0
                                                        state["certi_rec_miss_cnt"] = 0

                                            # rec.png도 없고 waiting.png도 없는 상태로 60초가 경과했을 때 -> 바탕화면 이동 후 12.png(잔류 게임창) 먼저 서치!
                                            if state.get("certi_delay_seen_time", 0.0) == 0.0 and state.get("certi_rec_seen_time", 0.0) == 0.0 and (curr_time - state.get("certi_launch_time", curr_time) >= 60.0):
                                                dprint(key, "⚠️ [구동 1분 타임아웃] 60초간 아무 반응이 없습니다! 바탕화면 이동 후 작업표시줄에 '12.png'(미종료 게임창)가 남아있는지 먼저 확인합니다.")
                                                clear_movements_only(pico_queues[key])
                                                pico_queues[key].put({"action": "HOME_MACRO"})
                                                state["certi_from_closed_game"] = False
                                                state["certi_12_find_start"] = curr_time + 1.5
                                                state["target_fsm"] = "CERTI_STEP_12_FIND"
                                                state["cooldown"] = curr_time + 1.2
                                    state["cooldown"] = curr_time + 0.3

                    # 14-0단계(퍼플 꺼짐 예외처리): yse.png(또는 yes.png) 찾아 원클릭 후 waiting.png 감시(타이머 리셋)로 복귀
                    elif current_fsm == "CERTI_PURPLE_YSE_FIND":
                        pos_yse = find_certi_img("yse.png", th=0.82) or find_certi_img("yes.png", th=0.82)
                        if pos_yse:
                            state["certi_purple_cd"] = curr_time + 8.0
                            dprint(key, f"🟣 [퍼플 실행 확인] 'yse.png' 발견({pos_yse[0]}, {pos_yse[1]})! 원클릭 후 퍼플 로그인 및 'waiting.png' 감시로 넘어갑니다.")
                            start_certi_move_and_action(
                                pos_yse[0], pos_yse[1],
                                next_fsm="CERTI_LAUNCH_TIMER_INIT",
                                double=False,
                                post_wait=1.5,
                                desc="퍼플 yse.png 원클릭"
                            )
                        else:
                            elapsed_p = curr_time - state.get("certi_purple_find_start", curr_time)
                            if elapsed_p >= 3.0 and not state.get("certi_purple_evaded", False):
                                cur_cx, cur_cy = state.get("cursor_pos", [400, 300])
                                evade_tx, evade_ty = int(round(g_val(560, 650))), int(round(g_val(260, 340)))
                                dur_ev = apply_human_variance(0.10 + 0.035 * math.log2((math.hypot(evade_tx - cur_cx, evade_ty - cur_cy) / 20.0) + 1.0))
                                pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": generate_human_deltas(evade_tx - cur_cx, evade_ty - cur_cy, duration=dur_ev, behavior="CERTI", key=key)})
                                state["cursor_pos"] = [evade_tx, evade_ty]
                                state["certi_purple_evaded"] = True
                                state["cooldown"] = curr_time + dur_ev + 0.3
                                dprint(key, "👀 [yse.png 가림 방지] 커서를 옆으로 치운 뒤 버튼을 다시 찾습니다.")
                            elif elapsed_p >= 10.0:
                                dprint(key, "⚠️ [yse.png 10초 미감지] 구동 감시(waiting.png 대기) 단계로 복귀합니다.")
                                state["certi_purple_cd"] = curr_time + 5.0
                                state["target_fsm"] = "CERTI_LAUNCH_TIMER_INIT"
                                state["cooldown"] = curr_time + 0.2
                            else:
                                state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_15_FIND":
                        pos_re, re_name = find_any_recerti_img(th=0.82)
                        if pos_re:
                            handle_recerti_branch(pos_re, re_name, "15단계 재인증/오류")
                        else:
                            pos_15 = find_certi_img("15.png", th=0.82)
                            if pos_15: start_certi_move_and_action(pos_15[0], pos_15[1], next_fsm="CERTI_STEP_16_FIND", double=False, use_jitter=False, post_wait=0.6, desc="15.png 정밀클릭")
                            else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_STEP_16_FIND":
                        pos_re, re_name = find_any_recerti_img(th=0.82)
                        if pos_re:
                            handle_recerti_branch(pos_re, re_name, "16단계 재인증/오류")
                        else:
                            pos_16 = find_certi_img("16.png", th=0.82)
                            if pos_16: start_certi_move_and_action(pos_16[0], pos_16[1], next_fsm="CERTI_AFTER_16_BRANCH", double=False, post_wait=0.6, desc="16.png 클릭")
                            else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_AFTER_16_BRANCH":
                        pos_re, re_name = find_any_recerti_img(th=0.82)
                        if pos_re:
                            handle_recerti_branch(pos_re, re_name, "16단계 이후 재인증/오류")
                        else:
                            pos_login = find_certi_img("login.png", th=0.82)
                            if pos_login:
                                pico_queues[key].put({"action": "HOLD_KEY", "keycode": 176, "duration": g_val(0.06, 0.09)})
                                pico_queues[key].put({"action": "WAIT", "delay_min": 0.28, "delay_max": 0.34})
                                pico_queues[key].put({"action": "HOLD_KEY", "keycode": 176, "duration": g_val(0.06, 0.09)})
                                state["target_fsm"] = "CERTI_STEP_17_FIND"
                                state["cooldown"] = curr_time + 1.0
                            else:
                                pos_ticket = find_certi_img("ticket.png", th=0.82)
                                if pos_ticket:
                                    dprint(key, "⚠️ [이용권 오류 감지] 'ticket.png' 포착! 1초 대기 후 ESC를 눌러 종료 팝업창으로 전환합니다.")
                                    pico_queues[key].put({"action": "WAIT", "delay_min": 0.95, "delay_max": 1.10})
                                    pico_queues[key].put({"action": "HOLD_KEY", "keycode": 177, "duration": g_val(0.06, 0.10)})
                                    pico_queues[key].put({"action": "WAIT", "delay_min": 0.55, "delay_max": 0.70})
                                    now_real = time.time()
                                    state["ticket_esc_sent_time"] = now_real
                                    state["target_fsm"] = "CERTI_TICKET_OK2_FIND"
                                    state["cooldown"] = now_real + 1.8
                                else:
                                    state["cooldown"] = curr_time + 0.2

                    # =========================================================================
                    # 🟢 [re1, re2 전용: 강종 없이 ok2.png 또는 ok3.png 클릭 ➔ 게임 자동종료 ➔ 바탕화면 후 재인증]
                    # =========================================================================
                    elif current_fsm == "CERTI_RECERTI_OK_FIND":
                        pos_ok = (
                            find_certi_img("ok2.png", th=0.82) or
                            find_certi_img("recerti/ok2.png", th=0.82) or
                            find_certi_img("ok3.png", th=0.82) or
                            find_certi_img("recerti/ok3.png", th=0.82)
                        )
                        if pos_ok:
                            dprint(key, f"🔎 [re1/2 확인 버튼 발견] ok2/ok3 좌표({pos_ok[0]}, {pos_ok[1]})로 커서를 날려 클릭합니다!")
                            start_certi_move_and_action(
                                pos_ok[0], pos_ok[1],
                                next_fsm="CERTI_RECERTI_OK_GOTO_DESKTOP",
                                double=False,
                                post_wait=2.5,
                                desc="re1/2 팝업 ok2/ok3 클릭"
                            )
                        else:
                            elapsed_ok = curr_time - state.get("recerti_ok_find_start", curr_time)
                            if elapsed_ok >= 3.0 and not state.get("recerti_ok_evaded", False):
                                cur_cx, cur_cy = state.get("cursor_pos", [400, 300])
                                evade_tx, evade_ty = int(round(g_val(560, 650))), int(round(g_val(260, 340)))
                                dur_ev = apply_human_variance(0.10 + 0.035 * math.log2((math.hypot(evade_tx - cur_cx, evade_ty - cur_cy) / 20.0) + 1.0))
                                pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": generate_human_deltas(evade_tx - cur_cx, evade_ty - cur_cy, duration=dur_ev, behavior="CERTI", key=key)})
                                state["cursor_pos"] = [evade_tx, evade_ty]
                                state["recerti_ok_evaded"] = True
                                state["cooldown"] = curr_time + dur_ev + 0.3
                                dprint(key, "👀 [ok2/ok3 가림 방지] 커서를 옆으로 치운 뒤 확인 버튼을 다시 스캔합니다.")
                            elif elapsed_ok >= 10.0:
                                dprint(key, "⚠️ [ok2/ok3 10초 미감지] 확인 버튼을 찾지 못해 안전하게 작업관리자 강종 절차로 전환합니다.")
                                pico_queues[key].put({"action": "HOME_MACRO"})
                                state["target_fsm"] = "CERTI_RECERTI_OPEN_TM"
                                state["cooldown"] = curr_time + g_val(1.2, 1.6)
                            else:
                                state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_RECERTI_OK_GOTO_DESKTOP":
                        dprint(key, "🖥️ [re1/2 게임 자동종료 완료] 바탕화면 가기(HOME_MACRO) 실행 후 1단계부터 재인증 절차를 밟습니다!")
                        state["certi_from_closed_game"] = True
                        state["target_fsm"] = "CERTI_GOTO_DESKTOP"
                        state["cooldown"] = curr_time + 0.2

                    # =========================================================================
                    # 🛠️ [re3~ & delay.png 전용: 작업 관리자 실행 ➔ lineage.png 4초 대기 재감지 ➔ 강종 ➔ 재인증]
                    # =========================================================================
                    elif current_fsm == "CERTI_RECERTI_OPEN_TM":
                        dprint(key, "🖥️ [작업관리자 호출] 피코 하드웨어로 Ctrl+Shift+Esc 신호를 전송합니다!")
                        pico_queues[key].put({"action": "OPEN_TASKMGR"})
                        state["recerti_tm_open_time"] = curr_time
                        state["recerti_tm_retried"] = False
                        state["recerti_kill_try_cnt"] = 0
                        state["target_fsm"] = "CERTI_RECERTI_TM_FIND_FIRST"
                        state["cooldown"] = curr_time + g_val(1.2, 1.5)

                    elif current_fsm == "CERTI_RECERTI_TM_FIND_FIRST":
                        pos_lin = find_certi_img("recerti/lineage.png", th=0.82) or find_certi_img("lineage.png", th=0.82)
                        if pos_lin:
                            dprint(key, f"🔎 [리니지 아이콘 최초 감지] 작업관리자 내 'lineage.png' 포착({pos_lin[0]}, {pos_lin[1]})! 목록 움직임 안정화를 위해 4.0초 대기 후 좌표를 재감지합니다.")
                            state["recerti_lineage_stabilize_until"] = curr_time + g_val(4.0, 4.3)
                            state["target_fsm"] = "CERTI_RECERTI_TM_WAIT_4S"
                            state["cooldown"] = curr_time + 0.2
                        else:
                            elapsed_tm = curr_time - state.get("recerti_tm_open_time", curr_time)
                            if elapsed_tm >= 6.0 and not state.get("recerti_tm_retried", False):
                                dprint(key, "⚠️ [작업관리자 재호출] 6초간 'lineage.png' 미감지 ➔ Ctrl+Shift+Esc를 한 번 더 전송합니다.")
                                pico_queues[key].put({"action": "OPEN_TASKMGR"})
                                state["recerti_tm_retried"] = True
                                state["cooldown"] = curr_time + 1.2
                            elif elapsed_tm >= 12.0:
                                dprint(key, "ℹ️ [리니지 프로세스 없음] 12초간 작업관리자에 'lineage.png'가 없습니다(이미 종료됨). 작업관리자를 닫고 1단계 재인증으로 이동합니다.")
                                pico_queues[key].put({"action": "CLOSE_TASKMGR"})
                                state["certi_from_closed_game"] = True
                                state["target_fsm"] = "CERTI_GOTO_DESKTOP"
                                state["cooldown"] = curr_time + 1.0
                            else:
                                state["cooldown"] = curr_time + 0.25

                    elif current_fsm == "CERTI_RECERTI_TM_WAIT_4S":
                        if curr_time >= state.get("recerti_lineage_stabilize_until", 0):
                            pos_lin_now = find_certi_img("recerti/lineage.png", th=0.82) or find_certi_img("lineage.png", th=0.82)
                            if pos_lin_now:
                                dprint(key, f"🎯 [4초 대기 완료 ➔ 좌표 재감지] 현재 'lineage.png' 위치({pos_lin_now[0]}, {pos_lin_now[1]})로 이동하여 원클릭합니다!")
                                start_certi_move_and_action(
                                    pos_lin_now[0], pos_lin_now[1],
                                    next_fsm="CERTI_RECERTI_TM_PRESS_DEL",
                                    double=False,
                                    use_jitter=False,
                                    post_wait=0.35,
                                    desc="작업관리자 lineage.png 원클릭"
                                )
                            else:
                                if curr_time <= state.get("recerti_lineage_stabilize_until", 0) + 2.0:
                                    state["cooldown"] = curr_time + 0.2
                                else:
                                    dprint(key, "ℹ️ [리니지 자동 종료 확인] 4초 대기 후 'lineage.png'가 이미 사라졌습니다! 작업관리자를 닫고 1단계 재인증으로 이동합니다.")
                                    pico_queues[key].put({"action": "CLOSE_TASKMGR"})
                                    state["certi_from_closed_game"] = True
                                    state["target_fsm"] = "CERTI_GOTO_DESKTOP"
                                    state["cooldown"] = curr_time + 1.0
                        else:
                            state["cooldown"] = curr_time + 0.2

                    # R-4단계: 원클릭 직후 Delete 키 1회 전송 (퍼플 오종료 방지를 위해 작업관리자 내 재클릭 금지!)
                    elif current_fsm == "CERTI_RECERTI_TM_PRESS_DEL":
                        state["recerti_kill_try_cnt"] = state.get("recerti_kill_try_cnt", 0) + 1
                        dprint(key, f"💀 [델키 1회 강제종료] Delete 키를 1회 전송합니다! ({state['recerti_kill_try_cnt']}회차)")
                        pico_queues[key].put({"action": "TASKMGR_DEL"})
                        state["target_fsm"] = "CERTI_RECERTI_TM_CLOSE_AND_HOME"
                        state["cooldown"] = curr_time + 0.6

                    # R-5단계: confirm2.png(종료 확인창) 유무만 1회 체크 후 즉시 작업관리자를 닫고 바탕화면으로 이동
                    elif current_fsm == "CERTI_RECERTI_TM_CLOSE_AND_HOME":
                        pos_c2 = find_certi_img("recerti/confirm2.png", th=0.82) or find_certi_img("confirm2.png", th=0.82)
                        if pos_c2:
                            dprint(key, f"⚠️ [종료 확인창 감지] 'confirm2.png' 발견({pos_c2[0]}, {pos_c2[1]})! 클릭 후 즉시 작업관리자를 닫습니다.")
                            start_certi_move_and_action(
                                pos_c2[0], pos_c2[1],
                                next_fsm="CERTI_RECERTI_TM_AFTER_CONFIRM2",
                                double=False,
                                use_jitter=False,
                                post_wait=0.5,
                                desc="confirm2.png 종료오류 확인 클릭"
                            )
                        else:
                            dprint(key, "🖥️ [작업관리자 종료 ➔ 바탕화면] 작업관리자를 닫고 작업표시줄 '12.png' 소멸을 최대 7초간 확인합니다.")
                            pico_queues[key].put({"action": "CLOSE_TASKMGR"})
                            pico_queues[key].put({"action": "HOME_MACRO"})
                            cur_cx, cur_cy = state.get("cursor_pos", [400, 300])
                            if cur_cy >= 530:
                                safe_tx, safe_ty = int(round(g_val(550, 650))), int(round(g_val(260, 340)))
                                pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": generate_human_deltas(safe_tx - cur_cx, safe_ty - cur_cy, duration=0.15, behavior="CERTI", key=key)})
                                state["cursor_pos"] = [safe_tx, safe_ty]
                            now_real = time.time()
                            state["recerti_12_gone_deadline"] = now_real + 8.2
                            state["recerti_12_gone_streak"] = 0
                            state["target_fsm"] = "CERTI_RECERTI_WAIT_12_GONE"
                            state["cooldown"] = now_real + 1.2

                    # R-5-1단계: confirm2.png 클릭 직후 즉시 작업관리자를 닫고 바탕화면으로 이동
                    elif current_fsm == "CERTI_RECERTI_TM_AFTER_CONFIRM2":
                        dprint(key, "🖥️ [확인창 클릭 완료 ➔ 바탕화면] 작업관리자를 닫고 작업표시줄 '12.png' 소멸을 최대 7초간 확인합니다.")
                        pico_queues[key].put({"action": "CLOSE_TASKMGR"})
                        pico_queues[key].put({"action": "HOME_MACRO"})
                        now_real = time.time()
                        state["recerti_12_gone_deadline"] = now_real + 8.2
                        state["recerti_12_gone_streak"] = 0
                        state["target_fsm"] = "CERTI_RECERTI_WAIT_12_GONE"
                        state["cooldown"] = now_real + 1.2

                    # R-6단계: 바탕화면 작업표시줄(Y:550~600)에서 12.png가 사라지기를 최대 7초간 대기 (안 사라지면 작업관리자 재실행!)
                    elif current_fsm == "CERTI_RECERTI_WAIT_12_GONE":
                        pos_12_rem = find_certi_img("12.png", th=0.82, roi_rect=(0, 550, 800, 600))
                        if pos_12_rem is None:
                            state["recerti_12_gone_streak"] = state.get("recerti_12_gone_streak", 0) + 1
                            if state["recerti_12_gone_streak"] >= 2:
                                dprint(key, "✅ [12.png 소멸 확인] 작업표시줄에서 리니지 아이콘(12.png)이 완전히 사라졌습니다! 1단계 재인증으로 이동합니다!")
                                state["certi_from_closed_game"] = True
                                state["target_fsm"] = "CERTI_GOTO_DESKTOP"
                                state["cooldown"] = curr_time + 0.3
                            else:
                                state["cooldown"] = curr_time + 0.15
                        else:
                            state["recerti_12_gone_streak"] = 0
                            if curr_time >= state.get("recerti_12_gone_deadline", 0):
                                dprint(key, f"🚨 [7초 경과 - 12.png 잔류 확인] 작업표시줄에 '12.png'({pos_12_rem[0]}, {pos_12_rem[1]})가 아직 남아있습니다! 작업관리자를 다시 열어 강종을 재시도합니다!")
                                state["target_fsm"] = "CERTI_RECERTI_OPEN_TM"
                                state["cooldown"] = curr_time + 0.2
                            else:
                                state["cooldown"] = curr_time + 0.25

                    elif current_fsm == "CERTI_TICKET_OK2_FIND":
                        # 🛡️ 아직 화면에 ticket.png가 남아있다면 그 안의 우측하단 ok(종료창의 Cancel 위치)를 절대 찍지 않도록 대기!
                        if find_certi_img("ticket.png", th=0.80) is not None:
                            if curr_time - state.get("ticket_esc_sent_time", curr_time) >= 2.5:
                                dprint(key, "🔄 [ticket.png 잔류 감지] ESC가 씹혀 아직 'ticket.png'가 떠 있습니다! ESC를 다시 전송합니다.")
                                pico_queues[key].put({"action": "HOLD_KEY", "keycode": 177, "duration": g_val(0.06, 0.10)})
                                pico_queues[key].put({"action": "WAIT", "delay_min": 0.55, "delay_max": 0.70})
                                state["ticket_esc_sent_time"] = time.time()
                                state["cooldown"] = time.time() + 0.8
                            else:
                                state["cooldown"] = curr_time + 0.15
                        else:
                            pos_ok2 = find_certi_img("ok2.png", th=0.82)
                            if pos_ok2:
                                state["certi_13_wait_mode"] = "TICKET"
                                start_certi_move_and_action(pos_ok2[0], pos_ok2[1], next_fsm="CERTI_TICKET_GOTO_DESKTOP", double=False, post_wait=3.0, desc="ok2.png 클릭")
                            else: state["cooldown"] = curr_time + 0.2

                    elif current_fsm == "CERTI_TICKET_GOTO_DESKTOP":
                        pico_queues[key].put({"action": "HOME_MACRO"})
                        state["certi_next_desktop_time"] = curr_time + g_val(2.0, 3.0)
                        state["target_fsm"] = "CERTI_STEP_13_FIND"
                        state["cooldown"] = curr_time + 1.5

                    elif current_fsm == "CERTI_STEP_17_FIND":
                        pos_re, re_name = find_any_recerti_img(th=0.82)
                        if pos_re:
                            handle_recerti_branch(pos_re, re_name, "17단계 재인증/오류")
                        else:
                            pos_17 = find_certi_img("17.png", th=0.82)
                            if pos_17: start_certi_move_and_action(pos_17[0], pos_17[1], next_fsm="CERTI_WAIT_DRAGON", double=True, post_wait=1.5, desc="17.png 입장 더블클릭")
                            else: state["cooldown"] = curr_time + 0.2

                    # 🐉 [군주 전용 접속 마무리] dragon.png 감지 ➔ F1 단축창 ➔ F6 헤이스트(688, 502) 원클릭으로 마우스 휠 지정!
                    elif current_fsm == "CERTI_WAIT_DRAGON":
                        if find_certi_img("dragon.png", th=0.82):
                            dprint(key, "🐉 [군주 접속 성공] 'dragon.png' 확인! F1 탭을 누른 뒤 F6 헤이스트 아이콘(688, 502)을 원클릭하여 휠에 등록합니다!")
                            pico_queues[key].put({"action": "WAIT", "delay_min": 0.4, "delay_max": 0.6})
                            pico_queues[key].put({"action": "HOLD_KEY", "keycode": KEY_F1, "duration": g_val(0.06, 0.10)})
                            pico_queues[key].put({"action": "WAIT", "delay_min": 0.3, "delay_max": 0.5})
                            state["target_fsm"] = "CERTI_DRAGON_CLICK_HASTE"
                            state["cooldown"] = curr_time + 1.0
                        else:
                            pos_re, re_name = find_any_recerti_img(th=0.82)
                            if pos_re:
                                handle_recerti_branch(pos_re, re_name, "용머리 대기 중 재인증/오류")
                            elif find_certi_img("ticket2.png", th=0.90) or find_certi_img("qq/ticket2.png", th=0.90):
                                dprint(key, "🚨 [접속 직후 ticket2.png 감지] 이용시간 만료 팝업 포착! ok2 ➔ quit 클릭 후 13.png 재접속 단계로 이동합니다!")
                                state["target_fsm"] = "CERTI_FIND_OK2_FIRST"
                                state["cooldown"] = curr_time + 0.3
                            else:
                                state["cooldown"] = curr_time + 0.3

                    elif current_fsm == "CERTI_DRAGON_CLICK_HASTE":
                        dprint(key, f"🪄 [군주 헤이 휠 등록] F6 슬롯({SLOT_F6_CX}, {SLOT_F6_CY})으로 이동하여 원클릭합니다!")
                        start_certi_move_and_action(
                            SLOT_F6_CX, SLOT_F6_CY,
                            next_fsm="CERTI_DRAGON_FINISH",
                            double=False,
                            use_jitter=True,
                            post_wait=0.8,
                            desc="F6 헤이스트 휠단축창 원클릭"
                        )

                    elif current_fsm == "CERTI_DRAGON_FINISH":
                        cur_cx, cur_cy = state.get("cursor_pos", [SLOT_F6_CX, SLOT_F6_CY])
                        safe_tx, safe_ty = 400 + int(round(g_val(-30, 30))), 260 + int(round(g_val(-30, 30)))
                        dur_m = apply_human_variance(0.10 + 0.035 * math.log2((math.hypot(safe_tx - cur_cx, safe_ty - cur_cy) / 20.0) + 1.0))
                        pico_queues[key].put({"action": "CUSTOM_MOVE", "deltas": generate_human_deltas(safe_tx - cur_cx, safe_ty - cur_cy, duration=dur_m, behavior="CERTI", key=key)})
                        state["cursor_pos"] = [safe_tx, safe_ty]
                        state["cmd_fsm"] = "IDLE"
                        state["target_fsm"] = "IDLE"
                        state["certi_last_box"] = None
                        state["was_manual_mode"] = True
                        state["cooldown"] = curr_time + 0.8
                        dprint(key, "👑 [군주 복귀 완료] F6 헤이스트 휠 지정 완료! 즉시 버프/상점/회수 임무로 복귀합니다!")

                if DEBUG_MODE and debug_img is not None:
                    cur_x_c, cur_y_c = state.get("cursor_pos", [400, 300])
                    cv2.putText(debug_img, f"[ CERTI : {current_fsm} ]", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
                    last_box = state.get("certi_last_box")
                    if last_box:
                        bx, by, bw, bh, bname, bval = last_box
                        cv2.rectangle(debug_img, (bx, by), (bx + bw, by + bh), (0, 255, 0), 2)
                        cv2.putText(debug_img, f"{bname} ({bval*100:.0f}%)", (bx, max(15, by - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
                    cv2.circle(debug_img, (int(cur_x_c), int(cur_y_c)), 10, (0, 255, 255), 1, cv2.LINE_AA)
                    try:
                        if debug_queues[key].full(): debug_queues[key].get_nowait()
                        debug_queues[key].put_nowait(debug_img)
                    except Exception: pass

                elapsed_loop = time.time() - curr_time
                time.sleep(max(0.005, GLOBAL_FRAME_DELAY - elapsed_loop))
                continue
            # ====================================================================

            if DEBUG_MODE and debug_img is not None:
                is_shop_mode = state.get("is_shop_active", False)
                is_recall_mode = state.get("is_recall_active", False)
                is_manual = (active_manual_target == key)
                is_idle = not state.get("is_hunt_active", False)
                
                if is_shop_mode:
                    cv2.putText(debug_img, f"SHOP FSM: {state.get('shop_fsm', 'IDLE')}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 100), 2)
                elif is_recall_mode:
                    cv2.putText(debug_img, f"RECALL FSM: {state.get('recall_fsm', 'IDLE')}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
                    cv2.rectangle(debug_img, (0, 0), (400, max(0, h - 150)), (255, 0, 255), 2)
                    cv2.putText(debug_img, "Recall Scan Area", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
                elif is_manual:
                    cv2.putText(debug_img, f"MANUAL MODE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    cv2.putText(debug_img, f"LORD FSM: {state.get('cmd_fsm', 'IDLE')} [{my_assigned_server}]", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                cv2.putText(debug_img, f"MP: {mp:.1f}%", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                if is_shop_mode or is_manual or is_idle:
                    try:
                        tmpl = WW_TEMPLATES.get("shop")
                        if tmpl and tmpl["color"] is not None:
                            if tmpl["mask"] is not None: res = cv2.matchTemplate(img_bgr, tmpl["color"], cv2.TM_CCORR_NORMED, mask=cv2.merge([tmpl["mask"]]*3))
                            else: res = cv2.matchTemplate(img_bgr, tmpl["color"], cv2.TM_CCOEFF_NORMED)
                            _, max_val, _, max_loc = cv2.minMaxLoc(res)
                            if max_val >= 0.75: 
                                h_t, w_t = tmpl["color"].shape[:2]
                                state["shop_ui_pos"] = (max_loc[0] + w_t//2, max_loc[1] + h_t//2)
                    except: pass
                    
                    if "shop_ui_pos" in state:
                        sx, sy = state["shop_ui_pos"]
                        ix, iy = sx + SHOP_INFO_OFFSET_X, sy + SHOP_INFO_OFFSET_Y
                        cv2.rectangle(debug_img, (ix-60, iy-10), (ix+60, iy+10), (0, 255, 0), 2)
                        cv2.putText(debug_img, "INFO", (ix-20, iy-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        ox, oy = sx + SHOP_OK_OFFSET_X, sy + SHOP_OK_OFFSET_Y
                        cv2.rectangle(debug_img, (ox-16, oy-8), (ox+16, oy+8), (0, 0, 255), 2)
                        cv2.circle(debug_img, (ox, oy), 3, (0, 0, 255), -1) 
                        cv2.putText(debug_img, "OK", (ox-10, oy-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                try:
                    if debug_queues[key].full(): debug_queues[key].get_nowait()
                    debug_queues[key].put_nowait(debug_img)
                except Exception: pass

            if active_manual_target == key or state.get("is_paused", False):
                state["was_manual_mode"] = True
                time.sleep(0.05); continue
                
            if state.get("was_manual_mode", False):
                state["was_manual_mode"] = False
                clear_movements_only(pico_queues[key])

            fsm = state.get("cmd_fsm", "IDLE")
            
            # [단계 1] IDLE/ASSIGNED: 할당 대기
            if fsm in ["IDLE", "ASSIGNED"]:
                if my_direct_queue and not my_direct_queue.empty():
                    req = my_direct_queue.get()
                    if req.get("action") == "DO_BUFF_TASK":
                        clear_movements_only(pico_queues[key])
                        
                        state["target_char_id"] = str(req.get("char_id"))
                        state["target_client_id"] = req.get("client_id")
                        state["assigned_casts"] = req.get("cast_count", 0)
                        state["is_first_shooter"] = req.get("is_first_shooter", False)
                        
                        role_str = "★1타 발사대" if state["is_first_shooter"] else "보조 대기"
                        dprint(key, f"📩 임무 하달! 사냥컴({state['target_char_id']})에게 {state['assigned_casts']}방 준비. ({role_str})")
                        
                        state["cmd_fsm"] = "WAIT_FOR_ANGLE"
                        state["wait_timeout"] = curr_time + 10.0 # 🚀 [안전장치 1] 10초 타임아웃
                        state["last_ping_send"] = curr_time
                        
            # [단계 2] WAIT_FOR_ANGLE: 목표 각도 수신 및 1방 장전
            elif fsm == "WAIT_FOR_ANGLE":
                # 🚀 [안전장치 2] 10초간 무응답 시 강제 취소
                if curr_time > state.get("wait_timeout", 0):
                    dprint(key, f"🚨 [타임아웃] 10초간 사냥컴({state['target_char_id']}) 각도 무응답! 임무 강제 파기.")
                    clear_movements_only(pico_queues[key])
                    state["cmd_fsm"] = "IDLE"
                    internal_router_queue.put({"action": "TASK_ABORTED", "mini_key": key, "char_id": state["target_char_id"]})
                    continue
                    
                # 🚀 [안전장치 3] 3초마다 CMD_MOVE_1CELL 재송신 (사냥컴 패킷 유실 방어)
                if state.get("is_first_shooter") and curr_time - state.get("last_ping_send", curr_time) >= 3.0:
                    state["last_ping_send"] = curr_time
                    send_to_central_pc(state["target_client_id"], {"action": "CMD_MOVE_1CELL", "char_id": state["target_char_id"], "commander_pc": key})
                    dprint(key, f"📡 [독촉 통신] 사냥컴({state['target_char_id']})에게 1칸 이동(CMD_MOVE_1CELL) 재명령!")
                    
                if my_direct_queue and not my_direct_queue.empty():
                    q_size = my_direct_queue.qsize()
                    for _ in range(q_size):
                        if my_direct_queue.empty(): break
                        msg = my_direct_queue.get()
                        
                        if msg.get("action") == "SEND_ANGLE" and str(msg.get("char_id")) == state.get("target_char_id"):
                            angle_deg = float(msg.get("angle"))
                            
                            # 👑 [형님 지적 완벽 수용] 단순 2배가 아닌 2차원 픽셀 '벡터(Vector) 뺄셈' 절대 타격 엔진!
                            def get_cell_vector(ang):
                                is_6 = abs(ang - 92.0) <= 10
                                is_horiz = any(abs(ang - a) <= 10 for a in [0.0, 360.0, 359.0, 180.0, 181.0])
                                if is_6: d = 40.0
                                elif is_horiz: d = 50.0
                                else: d = 30.0
                                r = math.radians(ang)
                                return math.cos(r) * d, math.sin(r) * (d * 0.85)

                            settings = current_settings.get(key, {})
                            is_dir_lock = settings.get("use_dir_lock", False)
                            
                            # 1. 사냥컴이 원래 중앙 위치에서 이동한 픽셀 거리 도출 (Target Vector)
                            tgt_dx, tgt_dy = get_cell_vector(angle_deg)
                            
                            if is_dir_lock:
                                # 2. 버퍼가 방향 잠금으로 인해 원래 중앙에서 밀려난 픽셀 거리 도출 (Buffer Vector)
                                lock_dir = settings.get("lock_dir", "9시")
                                lock_angle = LINEAGE_ANGLES.get(lock_dir, 181.0)
                                buf_dx, buf_dy = get_cell_vector(lock_angle)
                                
                                # 3. 🎯 핵심: (타겟 위치 - 내 위치) = 버퍼 화면 정중앙에서 날려야 할 정확한 픽셀 오차!
                                final_dx = tgt_dx - buf_dx
                                final_dy = tgt_dy - buf_dy
                                dprint(key, f"🔒 [방향잠금] 버퍼({lock_dir}) ➔ 사냥컴({angle_deg}도). 2차원 벡터 정밀 타격 장전!")
                            else:
                                final_dx = tgt_dx
                                final_dy = tgt_dy

                            # 🚨 방향을 잠갔을 때는 거리가 멀어지므로 12시 배제 룰(내 피통 클릭 방지)을 자동으로 해제합니다.
                            if abs(angle_deg - 268.0) <= 10 and not is_dir_lock:
                                dprint(key, f"🚫 12시 방향({angle_deg}도) 배제 구역. 발사 생략하고 CHECK_FIRST_BUFF 팩트체크 유도.")
                                if state["is_first_shooter"]:
                                    internal_router_queue.put({"action": "FIRST_SHOT_DONE", "mini_key": key, "char_id": state["target_char_id"]})
                                    state["cmd_fsm"] = "WAIT_FIRST_BUFF_RESULT"
                                    state["wait_timeout"] = curr_time + 6.0 
                                    state["last_ping_send"] = curr_time
                                else:
                                    state["cmd_fsm"] = "WAIT_FIRST_BUFF_RESULT"
                                    state["wait_timeout"] = curr_time + 6.0 
                                break
                            
                            cur_x, cur_y = state.get("cursor_pos", [400, 300])
                            real_cursor = find_cursor_pos(img_bgr, last_pos=(cur_x, cur_y), check_circle=True, allow_full_scan=True)
                            if real_cursor:
                                cur_x, cur_y = real_cursor[0], real_cursor[1]
                                state["cursor_pos"] = [cur_x, cur_y]
                            
                            # 최종 타점 계산 (인간화 난수 주입)
                            jitter_x = int(random.gauss(0, 2.0))
                            jitter_y = int(random.gauss(0, 5.0))
                            
                            # Y축 발밑 보정 (상대적 각도가 6시일 때만 타이트하게 조절)
                            y_offset = -15
                            if not is_dir_lock and abs(angle_deg - 92.0) <= 10:
                                y_offset = -20
                            elif is_dir_lock:
                                rel_rad = math.atan2(final_dy, final_dx)
                                rel_deg = (math.degrees(rel_rad) + 360) % 360
                                if abs(rel_deg - 92.0) <= 15 or abs(rel_deg - 90.0) <= 15:
                                    y_offset = -20
                            
                            # 🚀 형님의 팩트 영점(char_screen_cx, cy)에서 수학적으로 계산된 최종 벡터(final_dx, dy)를 완벽하게 더합니다!
                            tx = max(20, min(w - 20, int(char_screen_cx + final_dx) + jitter_x))
                            ty = max(5, min(int(h * 0.68), int(char_screen_cy + final_dy) + y_offset + jitter_y))
                            
                            pico_queues[key].put({"action": "HOVER", "dx": tx - cur_x, "dy": ty - cur_y})
                            pico_queues[key].put({"action": "WAIT", "delay_min": 0.4, "delay_max": 0.7}) 
                            state["cursor_pos"] = [tx, ty]
                            
                            if state["is_first_shooter"]:
                                pico_queues[key].put({"action": "WHEEL_CLICK"}) 
                                state["assigned_casts"] -= 1 
                                state["cmd_fsm"] = "WAIT_PHYSICAL_FIRST_SHOT"
                                state["wait_timeout"] = curr_time + 5.0 
                                time.sleep(0.05) 
                            else:
                                state["cmd_fsm"] = "WAIT_FIRST_BUFF_RESULT"
                                state["wait_timeout"] = curr_time + 6.0 
                                state["last_ping_send"] = 0
                            break
                        elif msg.get("action") == "ABORT_BUFF" and str(msg.get("char_id")) == state.get("target_char_id"):
                            clear_movements_only(pico_queues[key])
                            state["cmd_fsm"] = "IDLE"
                            break
                        else:
                            my_direct_queue.put(msg)

            # [단계 2.5] WAIT_PHYSICAL_FIRST_SHOT: 1타 물리적 발사 확인 및 중앙컴 검증 지시
            elif fsm == "WAIT_PHYSICAL_FIRST_SHOT":
                if pico_queues[key].empty() and not state.get("hw_busy", False):
                    dprint(key, f"🎯 1타 물리적 발사 완료! 통제실 라우터에 팩트체크 요청 올립니다.")
                    internal_router_queue.put({"action": "FIRST_SHOT_DONE", "mini_key": key, "char_id": state["target_char_id"]})
                    state["cmd_fsm"] = "WAIT_FIRST_BUFF_RESULT"
                    state["wait_timeout"] = curr_time + 6.0 
                    state["last_ping_send"] = curr_time
                    
                if curr_time > state.get("wait_timeout", 0):
                    state["cmd_fsm"] = "IDLE"
                    internal_router_queue.put({"action": "TASK_ABORTED", "mini_key": key, "char_id": state["target_char_id"]})

            # [단계 3] WAIT_FIRST_BUFF_RESULT: 사냥컴의 1타 팩트체크 결과 수신
            elif fsm == "WAIT_FIRST_BUFF_RESULT":
                # 🚀 [안전장치 4] 15초(사냥컴 팩트체크 시간 8초 포함) 동안 결과가 안 오면 사냥컴 추방!
                if curr_time > state.get("wait_timeout", 0):
                    dprint(key, f"🚨 [타임아웃] 사냥컴({state['target_char_id']}) 1타 결과 무응답(6초)! 임무 강제 파기.")
                    clear_movements_only(pico_queues[key])
                    state["cmd_fsm"] = "IDLE"
                    if state.get("is_first_shooter"):
                        internal_router_queue.put({"action": "TASK_ABORTED", "mini_key": key, "char_id": state["target_char_id"]})
                    continue

                # 🚀 [안전장치 5] 3초마다 사냥컴에 "1타 확인 결과 빨리 보내!" 라고 독촉 통신(Ping) 발송
                if state.get("is_first_shooter") and curr_time - state.get("last_ping_send", curr_time) >= 2.0:
                    state["last_ping_send"] = curr_time
                    send_to_central_pc(state["target_client_id"], {"action": "CHECK_FIRST_BUFF", "char_id": state["target_char_id"]})
                    dprint(key, f"📡 [독촉 통신] 사냥컴({state['target_char_id']})에게 1타 검증(CHECK_FIRST_BUFF) 재요청!")

                if my_direct_queue and not my_direct_queue.empty():
                    q_size = my_direct_queue.qsize()
                    for _ in range(q_size):
                        if my_direct_queue.empty(): break
                        msg = my_direct_queue.get()
                        
                        if str(msg.get("char_id")) == state.get("target_char_id"):
                            if msg.get("action") == "PROCEED_BUFF":
                                dprint(key, f"✅ 결제 승인! 남은 {state['assigned_casts']}방을 마저 발사합니다.")
                                if state["assigned_casts"] > 0:
                                    for _ in range(state["assigned_casts"]):
                                        pico_queues[key].put({"action": "WAIT", "delay_min": 2.0, "delay_max": 2.2}) 
                                        pico_queues[key].put({"action": "WHEEL_CLICK"}) 
                                    
                                    # 👇👇👇 [100% 마우스 치우기] 무조건 360도 무작위 20~100px 치움 👇👇👇
                                    cur_x, cur_y = state.get("cursor_pos", [400, 300])
                                    rad_rand = random.uniform(0, 2 * math.pi) 
                                    dist_rand = random.uniform(20.0, 100.0)   
                                    
                                    end_x = max(20, min(w - 20, int(cur_x + math.cos(rad_rand) * dist_rand)))
                                    end_y = max(5, min(int(h * 0.68), int(cur_y + math.sin(rad_rand) * dist_rand)))
                                    
                                    pico_queues[key].put({"action": "WAIT", "delay_min": 0.4, "delay_max": 0.8})
                                    pico_queues[key].put({"action": "HOVER", "dx": end_x - cur_x, "dy": end_y - cur_y})
                                    state["cursor_pos"] = [end_x, end_y]
                                    dprint(key, f"🚶 [인간화] 버프 종료! 마우스를 {int(dist_rand)}px 만큼 무작위로 치웁니다.")
                                    # 👆👆👆 ======================================================= 👆👆👆

                                    state["cmd_fsm"] = "CASTING_REMAINS"
                                    state["cast_timeout"] = curr_time + (state["assigned_casts"] * 3.0) + 5.0
                                else:
                                    # 👇👇👇 (0방 쏠 때도 동일하게 100% 무조건 치우기) 👇👇👇
                                    cur_x, cur_y = state.get("cursor_pos", [400, 300])
                                    rad_rand = random.uniform(0, 2 * math.pi)
                                    dist_rand = random.uniform(20.0, 100.0)
                                    
                                    end_x = max(20, min(w - 20, int(cur_x + math.cos(rad_rand) * dist_rand)))
                                    end_y = max(5, min(int(h * 0.68), int(cur_y + math.sin(rad_rand) * dist_rand)))
                                    
                                    pico_queues[key].put({"action": "WAIT", "delay_min": 0.4, "delay_max": 0.8})
                                    pico_queues[key].put({"action": "HOVER", "dx": end_x - cur_x, "dy": end_y - cur_y})
                                    state["cursor_pos"] = [end_x, end_y]
                                    dprint(key, f"🚶 [인간화] 1타 시전 종료! 마우스를 {int(dist_rand)}px 만큼 무작위로 치웁니다.")

                                    state["cmd_fsm"] = "CASTING_REMAINS"
                                    state["cast_timeout"] = curr_time + 1.0 
                                break
                                
                            elif msg.get("action") == "ABORT_BUFF":
                                dprint(key, f"🚨 1타 팩트체크 실패 지시 수신! 사격을 즉시 중지하고 대기합니다.")
                                clear_movements_only(pico_queues[key])
                                state["cmd_fsm"] = "IDLE"
                                break
                        else:
                            my_direct_queue.put(msg)

            # [단계 4] CASTING_REMAINS: 잔여 타건 종료 팩트 체크 및 통제실에 최종 보고서 제출
            elif fsm == "CASTING_REMAINS":
                if pico_queues[key].empty() and not state.get("hw_busy", False):
                    dprint(key, f"✨ 할당된 임무 완수! 라우터에 최종 보고합니다.")
                    internal_router_queue.put({"action": "TASK_DONE", "mini_key": key, "char_id": state["target_char_id"]})
                    state["cmd_fsm"] = "IDLE"
                
                if curr_time > state.get("cast_timeout", 0):
                    dprint(key, "⚠️ 잔여 시전 타임아웃. 큐 폭파 후 강제 보고.")
                    clear_movements_only(pico_queues[key])
                    internal_router_queue.put({"action": "TASK_DONE", "mini_key": key, "char_id": state["target_char_id"]})
                    state["cmd_fsm"] = "IDLE"

            elapsed_loop = time.time() - curr_time
            time.sleep(max(0.005, GLOBAL_FRAME_DELAY - elapsed_loop))

        except Exception as e:
            time.sleep(1.0)


def safe_ai_commander_worker(pc):
    while True:
        try:
            ai_commander_worker(pc)
        except Exception as e:
            import traceback
            print(f"\n🚨🚨 [{pc['key']}] 사령관 스레드 치명적 에러 방어! (죽지 않고 1초 뒤 자동 부활): {e}")
            traceback.print_exc() # 터미널에 몇 번째 줄에서 무슨 에러가 났는지 상세히 찍어줌
            time.sleep(1.0) # 무한 에러 도배 방지

# 🚀 [최적화 6] 1명이었던 사령관 대신 3명의 전담 불사조 소대장 파견! 
for pc in MINI_PCS:
    threading.Thread(target=safe_ai_commander_worker, args=(pc,), daemon=True).start()

# ==========================================
# 7. 수동/자동 통제 코어
# ==========================================
sensor_raw_dx, sensor_raw_dy = 0, 0
mouse_data_lock = threading.Lock()
SENSITIVITY = 0.75
pressed_keys = {}  # 🚀 [수술 1] set()을 사전(Dict)으로 변경!
overlay_win = None
ignore_clicks = False

# 🚀 [파섹 프리즈 완벽 수술 1] 윈도우 훅(Hook) 마비 방지용 비동기 큐 & 워커 스레드
manual_event_queue = queue.Queue()

# 🚀 [파섹 드래그 끊김 완벽 수술] 마우스 중복 스팸 방어막 장부 (디바운스)
manual_mouse_state = {1: False, 2: False, 3: False}  # 👈 휠 클릭(3) 방 추가!
mouse_release_timers = {}
mouse_debounce_lock = threading.Lock()

def manual_event_worker():
    while True:
        try:
            event = manual_event_queue.get()
            if event[0] == 'MOUSE':
                _, p_serial, p_lock, button, state = event
                # 💡 [핵심] is_manual=True 파라미터를 넘겨서 80ms 딜레이를 0초로 뚫어버립니다!
                send_mouse_click(p_serial, p_lock, button, state, is_manual=True) 
            elif event[0] == 'KEY':
                _, p_serial, p_lock, kcode, state = event
                send_keyboard_key(p_serial, p_lock, kcode, state, is_manual=True) 
            elif event[0] == 'HOME_MACRO':
                _, p_serial, p_lock = event
                send_keyboard_key(p_serial, p_lock, 131, 1, is_manual=True) 
                time.sleep(g_val(0.06, 0.09)) 
                send_keyboard_key(p_serial, p_lock, 100, 1, is_manual=True) 
                time.sleep(random.uniform(0.07, 0.12))
                send_keyboard_key(p_serial, p_lock, 100, 0, is_manual=True) 
                time.sleep(g_val(0.06, 0.09)) 
                send_keyboard_key(p_serial, p_lock, 131, 0, is_manual=True) 
            elif event[0] == 'SPECIAL_KEY':
                _, p_serial, p_lock, kcode = event
                send_keyboard_key(p_serial, p_lock, kcode, 1, is_manual=True)
                send_keyboard_key(p_serial, p_lock, kcode, 0, is_manual=True)
        except Exception:
            pass

threading.Thread(target=manual_event_worker, daemon=True).start()

# =================================================================
# 🚀 [프리징 및 커서 2개 완벽 수술] 스레드 안전성 보장 & 다클라 타겟팅
# =================================================================
overlay_win = None

def sync_overlay_ui(key):
    global overlay_win
    if key is None:
        if overlay_win: 
            try: overlay_win.destroy()
            except: pass
            overlay_win = None
    else:
        if not overlay_win:
            try:
                overlay_win = tk.Toplevel(root)
                overlay_win.attributes("-fullscreen", True)
                overlay_win.attributes("-alpha", 0.01) # 💡 투명도 1%로 본컴 마우스를 완벽히 가림
                overlay_win.attributes("-topmost", True)
                overlay_win.config(bg="black", cursor="none") # 💡 본컴 커서 투명화
                overlay_win.bind("<Button>", lambda e: "break")
            except: pass
    update_gui_status()

def toggle_manual(key):
    global active_manual_target, sensor_raw_dx, sensor_raw_dy, ignore_clicks
    global manual_mouse_state, mouse_release_timers, mouse_debounce_lock

    if key is None:
        if active_manual_target:
            old_key = active_manual_target
            active_manual_target = None 
            
            if picos.get(old_key):
                with pico_locks.get(old_key, threading.Lock()):
                    try: picos[old_key].write(bytearray([0xFF])) 
                    except: pass
                try: reset_hw_key_states(picos[old_key]) 
                except: pass
                
                manual_event_queue.put(('MOUSE', picos.get(old_key), pico_locks.get(old_key), 1, 0))
                manual_event_queue.put(('MOUSE', picos.get(old_key), pico_locks.get(old_key), 2, 0))
                manual_event_queue.put(('KEY', picos.get(old_key), pico_locks.get(old_key), 129, 0))
                
            if old_key in ai_states: 
                ai_states[old_key]["skid_dx"] = 0 
                ai_states[old_key]["skid_dy"] = 0
                
            for k in list(pressed_keys.values()):  # 🚀 [수술 2] .values() 추가!
                manual_event_queue.put(('KEY', picos[old_key], pico_locks[old_key], k, 0))
            pressed_keys.clear() 

            with mouse_debounce_lock:
                for t in mouse_release_timers.values(): t.cancel()
                mouse_release_timers.clear()
                manual_mouse_state[1] = False
                manual_mouse_state[2] = False

            # 🚨 [프리징 완벽 차단] 메인 스레드에 창 삭제를 안전하게 위임!
            root.after(0, sync_overlay_ui, None)
            root.after(10, arrange_windows)
        return

    if active_manual_target == key: return
    
    if active_manual_target:
        old_key = active_manual_target
        if picos.get(old_key):
            with pico_locks.get(old_key, threading.Lock()): 
                try: picos[old_key].write(bytearray([0xFF])) 
                except: pass
            try: reset_hw_key_states(picos[old_key]) 
            except: pass
            
            manual_event_queue.put(('MOUSE', picos.get(old_key), pico_locks.get(old_key), 1, 0))
            manual_event_queue.put(('MOUSE', picos.get(old_key), pico_locks.get(old_key), 2, 0))
            manual_event_queue.put(('KEY', picos.get(old_key), pico_locks.get(old_key), 129, 0))
            for k in list(pressed_keys.values()):  # 🚀 [수술 2] .values() 추가!
                manual_event_queue.put(('KEY', picos[old_key], pico_locks[old_key], k, 0))

    active_manual_target = key
    sensor_raw_dx, sensor_raw_dy = 0, 0
    pressed_keys.clear()
    ignore_clicks = True 
    
    with mouse_debounce_lock:
        for t in mouse_release_timers.values(): t.cancel()
        mouse_release_timers.clear()
        manual_mouse_state[1] = False
        manual_mouse_state[2] = False
        
    if key in pico_queues:
        with pico_queues[key].mutex: pico_queues[key].queue.clear()
    
    if picos.get(key):
        with pico_locks.get(key, threading.Lock()): 
            try: picos[key].write(bytearray([0xFF]))
            except: pass
        try: reset_hw_key_states(picos[key]) 
        except: pass
        
    if key in ai_states:
        ai_states[key]["skid_dx"] = 0
        ai_states[key]["skid_dy"] = 0
        
    # 🚨 [프리징 완벽 차단] 메인 스레드에서만 창을 덮어씌우도록 안전장치 부착!
    root.after(0, sync_overlay_ui, key)

def manual_transmitter_thread():
    global sensor_raw_dx, sensor_raw_dy, ignore_clicks 
    next_tick = time.perf_counter() + POLLING_RATE
    
    accum_x, accum_y = 0.0, 0.0  
    last_target = None 

    while True:
        target = active_manual_target
        
        if target != last_target:
            accum_x, accum_y = 0.0, 0.0
            last_target = target

        if not target or not picos.get(target):
            time.sleep(0.01)
            next_tick = time.perf_counter() + POLLING_RATE
            continue

        p_serial, p_lock = picos[target], pico_locks.get(target)
        
        with mouse_data_lock: 
            dx, dy = sensor_raw_dx, sensor_raw_dy
            sensor_raw_dx, sensor_raw_dy = 0, 0

        accum_x += (dx * SENSITIVITY)
        accum_y += (dy * SENSITIVITY)

        if abs(accum_x) < 2.0 and abs(accum_y) < 2.0:
            send_x = accum_x
            send_y = accum_y
        else:
            send_x = accum_x * 0.55
            send_y = accum_y * 0.55

        send_dx = int(max(-127, min(127, round(send_x))))
        send_dy = int(max(-127, min(127, round(send_y))))

        accum_x -= send_dx
        accum_y -= send_dy

        if send_dx != 0 or send_dy != 0: 
            send_immediate_delta(p_serial, p_lock, send_dx, send_dy)

        now = time.perf_counter()
        
        if next_tick < now - 0.016: 
            next_tick = now 
            
        if next_tick - time.perf_counter() > 0.002: 
            time.sleep(0.001)
            
        while time.perf_counter() < next_tick: 
            pass  
                
        next_tick += POLLING_RATE

threading.Thread(target=manual_transmitter_thread, daemon=True).start()

def rawinput_sensor_thread():
    global sensor_raw_dx, sensor_raw_dy
    class RAWINPUTDEVICE(ctypes.Structure): _fields_ = [("usUsagePage", wintypes.USHORT), ("usUsage", wintypes.USHORT), ("dwFlags", wintypes.DWORD), ("hwndTarget", wintypes.HWND)]
    class RAWMOUSE(ctypes.Structure): _fields_ = [("usFlags", wintypes.USHORT), ("ulButtons", wintypes.ULONG), ("ulRawButtons", wintypes.ULONG), ("lLastX", wintypes.LONG), ("lLastY", wintypes.LONG), ("ulExtraInformation", wintypes.ULONG)]
    class RAWINPUTHEADER(ctypes.Structure): _fields_ = [("dwType", wintypes.DWORD), ("dwSize", wintypes.DWORD), ("hDevice", wintypes.HANDLE), ("wParam", wintypes.WPARAM)]
    class RAWINPUT(ctypes.Structure): _fields_ = [("header", RAWINPUTHEADER), ("mouse", RAWMOUSE)] 

    def wndproc(hwnd, msg, wparam, lparam):
        global sensor_raw_dx, sensor_raw_dy
        current_target = active_manual_target
        
        if not current_target:
            if hasattr(wndproc, "last_target"): wndproc.last_target = None
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

        if msg == 0x00FF: 
            size = wintypes.UINT(ctypes.sizeof(RAWINPUT))
            ri = RAWINPUT()
            if ctypes.windll.user32.GetRawInputData(ctypes.c_void_p(lparam), 0x10000003, ctypes.byref(ri), ctypes.byref(size), ctypes.sizeof(RAWINPUTHEADER)) != -1 and ri.header.dwType == 0:
                dx, dy = ri.mouse.lLastX, ri.mouse.lLastY
                flags = ri.mouse.usFlags

                if getattr(wndproc, "last_target", None) != current_target:
                    wndproc.last_target = current_target
                    if flags & 0x01: wndproc.last_abs_x, wndproc.last_abs_y = dx, dy
                    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

                if flags & 0x01: 
                    if not hasattr(wndproc, "last_abs_x"):
                        wndproc.last_abs_x, wndproc.last_abs_y = dx, dy
                        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
                    screen_w, screen_h = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
                    real_dx = int((dx - wndproc.last_abs_x) / 65535.0 * screen_w)
                    real_dy = int((dy - wndproc.last_abs_y) / 65535.0 * screen_h)
                    wndproc.last_abs_x, wndproc.last_abs_y = dx, dy
                    dx, dy = real_dx, real_dy

                if abs(dx) < 400 and abs(dy) < 400:
                    with mouse_data_lock: 
                        sensor_raw_dx += dx
                        sensor_raw_dy += dy
                        
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    wc = win32gui.WNDCLASS()
    wc.lpszClassName = 'RawInputHidden'; wc.lpfnWndProc = wndproc; wc.hInstance = win32api.GetModuleHandle(None)
    try: win32gui.RegisterClass(wc)
    except: pass 
    hwnd = win32gui.CreateWindow(wc.lpszClassName, 'Watcher', 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)
    rid = RAWINPUTDEVICE(); rid.usUsagePage = 0x01; rid.usUsage = 0x02; rid.dwFlags = 0x00000100; rid.hwndTarget = hwnd
    ctypes.windll.user32.RegisterRawInputDevices(ctypes.byref(rid), 1, ctypes.sizeof(rid))
    win32gui.PumpMessages()

threading.Thread(target=rawinput_sensor_thread, daemon=True).start()

def on_scroll(x, y, dx, dy):
    if active_manual_target and picos.get(active_manual_target):
        if dy > 0: send_mouse_scroll(picos[active_manual_target], pico_locks[active_manual_target], 5)
        elif dy < 0: send_mouse_scroll(picos[active_manual_target], pico_locks[active_manual_target], -5)

def on_click(x, y, button, pressed):
    global active_manual_target, ignore_clicks
    global manual_mouse_state, mouse_release_timers, mouse_debounce_lock
    
    if active_manual_target is not None:
        if ignore_clicks:
            if not pressed: 
                ignore_clicks = False
            return 
            
        p_serial = picos.get(active_manual_target)
        p_lock = pico_locks.get(active_manual_target)
        if p_serial:
            # 🚀 [휠클릭 지원 패치] 파이썬 마우스 모듈에서 마우스 휠버튼(Middle)을 3번으로 파싱!
            btn_code = 1 if button == mouse.Button.left else 2 if button == mouse.Button.right else 3 if button == mouse.Button.middle else 0
            if btn_code == 0: return

            with mouse_debounce_lock:
                if pressed:
                    if btn_code in mouse_release_timers:
                        mouse_release_timers[btn_code].cancel()
                        del mouse_release_timers[btn_code]
                        return
                    
                    if manual_mouse_state.get(btn_code, False): return 
                        
                    manual_mouse_state[btn_code] = True
                    manual_event_queue.put(('MOUSE', p_serial, p_lock, btn_code, 1))
                else:
                    if not manual_mouse_state.get(btn_code, False): return 
                        
                    def delayed_release():
                        with mouse_debounce_lock:
                            if btn_code in mouse_release_timers:
                                del mouse_release_timers[btn_code]
                                manual_mouse_state[btn_code] = False
                                manual_event_queue.put(('MOUSE', p_serial, p_lock, btn_code, 0))

                    t = threading.Timer(0.04, delayed_release)
                    mouse_release_timers[btn_code] = t
                    t.start()
        return 

    if not pressed or active_manual_target is not None: return
    # 🚀 [휠클릭 지원 패치] 수동 모드 전환을 위한 클릭 시 휠 클릭도 인정!
    if button not in [mouse.Button.left, mouse.Button.right, mouse.Button.middle]: return

    def check_window_and_toggle():
        try:
            import win32gui, win32con
            hwnd = win32gui.WindowFromPoint((x, y))
            root_hwnd = win32gui.GetAncestor(hwnd, win32con.GA_ROOT)
            window_title = win32gui.GetWindowText(root_hwnd)
            
            if TARGET_PC_TITLE in window_title:
                left, top = win32gui.ClientToScreen(root_hwnd, (0, 0))
                _, _, right_w, bottom_h = win32gui.GetClientRect(root_hwnd)
                if left <= x <= left + right_w and top <= y <= top + bottom_h: 
                    # 🚀 [에러 완벽 수술] 4개의 창 중 정확히 내가 클릭한 창의 좌푯값을 추적하여 미니1~4 판독!
                    target_key = None
                    for k, roi in CAPTURE_ROIS.items():
                        if roi["left"] <= x <= roi["left"] + roi["width"] and roi["top"] <= y <= roi["top"] + roi["height"]:
                            target_key = k
                            break
                    
                    if not target_key:
                        target_key = MINI_PCS[0]["key"] # 못 찾으면 기본 1호기로 연결
                        
                    toggle_manual(target_key)
        except Exception: pass
        
    threading.Thread(target=check_window_and_toggle, daemon=True).start()

ARDUINO_KEY_MAP = { 
    keyboard.Key.enter: 176, keyboard.Key.backspace: 178, keyboard.Key.tab: 179, keyboard.Key.space: 32, keyboard.Key.shift: 129, 
    keyboard.Key.shift_l: 129, keyboard.Key.shift_r: 133, keyboard.Key.ctrl: 128, keyboard.Key.ctrl_l: 128, keyboard.Key.ctrl_r: 132, 
    keyboard.Key.alt: 130, keyboard.Key.alt_l: 130, keyboard.Key.alt_r: 134, keyboard.Key.esc: 177,
    keyboard.Key.f1: 194, keyboard.Key.f2: 195, keyboard.Key.f3: 196, keyboard.Key.f4: 197,
    keyboard.Key.f5: 198, keyboard.Key.f6: 199, keyboard.Key.f7: 200, keyboard.Key.f8: 201,
    keyboard.Key.f9: 202, keyboard.Key.f10: 203, keyboard.Key.f11: 204, keyboard.Key.f12: 205,
    keyboard.Key.up: 218, keyboard.Key.down: 217, keyboard.Key.left: 216, keyboard.Key.right: 215,
    keyboard.Key.insert: 209, keyboard.Key.delete: 212, keyboard.Key.home: 210, keyboard.Key.end: 213,
    keyboard.Key.page_up: 211, keyboard.Key.page_down: 214
}

def get_arduino_keycode(key):
    if key in ARDUINO_KEY_MAP: return ARDUINO_KEY_MAP[key]
    
    if hasattr(key, 'vk') and key.vk is not None:
        if key.vk == 21 or key.vk == 215: return 234 
        if key.vk == 25 or key.vk == 216: return 235 
        
        # 👇👇👇 [신규 추가] 우측 숫자 키패드(Numpad) 윈도우 고유 신호 가로채기! 👇👇👇
        if 96 <= key.vk <= 111:
            return key.vk + 144  # 96~111번 신호를 피코 전송용 240~255번으로 변환
        if key.vk == 144: # Num Lock 키
            return 239
        # 👆👆👆 ========================================================= 👆👆👆
        
    if hasattr(key, 'char') and key.char is not None:
        try:
            char_code = ord(key.char.lower())
            if 1 <= char_code <= 26: return char_code + 96 
            return char_code
        except: return None
    return None

def on_press(key):
    if hasattr(key, 'char') and key.char == '`':
        # 🚀 [딜레이 0초 수술 3] 단축키로 끌 때도 다이렉트로 즉시 실행!
        if active_manual_target: toggle_manual(None) # root.after 제거!
        return 
        
    if active_manual_target:
        if key == keyboard.Key.home:
            p_serial = picos[active_manual_target]
            p_lock = pico_locks[active_manual_target]
            manual_event_queue.put(('HOME_MACRO', p_serial, p_lock))
            return 

        kcode = get_arduino_keycode(key)
        if kcode:
            if kcode in [234, 235, 134, 132]: 
                p_serial = picos[active_manual_target]
                p_lock = pico_locks[active_manual_target]
                manual_event_queue.put(('SPECIAL_KEY', p_serial, p_lock, kcode))
                return 

            # 🚀 [채팅 씹힘 버그 완벽 수술]
            # Shift 상태에 따라 글자가 바뀌어도 꼬이지 않게 '물리 키보드 고유 아이디'를 장부에 기록!
            physical_id = getattr(key, 'vk', str(key))

            if physical_id not in pressed_keys:
                pressed_keys[physical_id] = kcode
                manual_event_queue.put(('KEY', picos[active_manual_target], pico_locks[active_manual_target], kcode, 1))

def on_release(key):
    if hasattr(key, 'char') and key.char == '`': return 
    if active_manual_target:
        # 🚀 [채팅 씹힘 버그 완벽 수술]
        # 누를 때 저장해둔 '물리 키보드 고유 아이디'를 장부에서 찾아서, 눌렀던 코드 그대로 UP 신호를 쏩니다!
        physical_id = getattr(key, 'vk', str(key))
        if physical_id in pressed_keys:
            kcode = pressed_keys.pop(physical_id)
            manual_event_queue.put(('KEY', picos[active_manual_target], pico_locks[active_manual_target], kcode, 0))

def win32_event_filter(msg, data):
    try:
        vk = getattr(data, 'vkCode', data) 
        if vk == 27:  
            if active_manual_target:
                if msg == 256: on_press(keyboard.Key.esc)
                elif msg == 257: on_release(keyboard.Key.esc)
                return False 
            
            hwnd = win32gui.GetForegroundWindow()
            if hwnd and TARGET_PC_TITLE in win32gui.GetWindowText(hwnd):
                if msg == 256: on_press(keyboard.Key.esc)
                elif msg == 257: on_release(keyboard.Key.esc)
                return False 
    except Exception: pass
    return True

keyboard.Listener(on_press=on_press, on_release=on_release, win32_event_filter=win32_event_filter).start()
mouse.Listener(on_scroll=on_scroll, on_click=on_click).start()

# =================================================================
# 🚀 [긴급 에러 픽스] 삭제되었던 창 이름 변수를 전역으로 100% 강제 고정!
# =================================================================
TARGET_PC_TITLE = "프로젝터"

# =====================================================================
# 💰 [장사 봇 전용 앵커 절대 좌표 오프셋] 'Selling item(shop.png)' 중심점 기준!
# 형님께서 디버그 창의 초록(INFO), 빨강(OK) 네모 박스를 보시면서 이 숫자를 조절하시면 됩니다.
# =====================================================================
SHOP_INFO_OFFSET_X = 30   # shop.png 중심에서 우측으로 이동할 픽셀
SHOP_INFO_OFFSET_Y = 275  # shop.png 중심에서 아래로 이동할 픽셀
SHOP_OK_OFFSET_X = 60     # shop.png 중심에서 우측으로 이동할 픽셀
SHOP_OK_OFFSET_Y = 327    # shop.png 중심에서 아래로 이동할 픽셀

def sync_gui_vars():
    global safe_gui_x, safe_gui_y
    # 🚨 [프리징 완벽 차단 1] 메인 스레드에서만 안전하게 UI 좌표를 읽어서 칠판에 적어둡니다!
    try: 
        safe_gui_x = root.winfo_x()
        safe_gui_y = root.winfo_y()
    except: pass

    import re
    def safe_float(var_obj, default_value):
        try:
            raw_val = str(var_obj.get()).strip()
            clean_val = re.sub(r'[^0-9.]', '', raw_val)
            if clean_val and clean_val != '.': return float(clean_val)
            return float(default_value)
        except Exception: return float(default_value)

    for pc in MINI_PCS:
        k = pc["key"]
        if k in gui_vars:
            blue_def_val = safe_float(gui_vars[k].get("blue_deficit", tk.StringVar(value="11")), 11.0)
            
            st = ai_states.get(k, {})  
            
            current_settings[k] = {
                "com_port": gui_vars[k]["com_port"].get().strip(),
                "pico_hwid": st.get("pico_hwid", saved_settings.get(k, {}).get("pico_hwid", "")),
                "use_blue_pot": gui_vars[k].get("use_blue_pot", tk.BooleanVar(value=False)).get(), 
                "blue_deficit": blue_def_val, # 🚀 파랭이 결손방수 실시간 동기화
                
                "use_dir_lock": gui_vars[k].get("use_dir_lock", tk.BooleanVar(value=False)).get() if "use_dir_lock" in gui_vars[k] else False,
                "lock_dir": gui_vars[k].get("lock_dir", tk.StringVar(value="9시")).get() if "lock_dir" in gui_vars[k] else "9시",

                # 👇👇👇 [신규 추가] 여기에 복사해서 넣으세요! 👇👇👇
                "recall_item1": gui_vars[k].get("recall_item1", tk.StringVar(value="없음")).get() if "recall_item1" in gui_vars[k] else "없음",
                "recall_item2": gui_vars[k].get("recall_item2", tk.StringVar(value="없음")).get() if "recall_item2" in gui_vars[k] else "없음",
                "recall_item3": gui_vars[k].get("recall_item3", tk.StringVar(value="없음")).get() if "recall_item3" in gui_vars[k] else "없음",
                
                "win_x": gui_vars[k].get("win_x", tk.StringVar(value="0")).get(),
                "win_y": gui_vars[k].get("win_y", tk.StringVar(value="0")).get(),
                
                # 🚀 장사봇 설정 실시간 동기화
                "shop_item": gui_vars[k].get("shop_item", tk.StringVar(value="yongi")).get() if "shop_item" in gui_vars[k] else "yongi",
                "shop_qty": gui_vars[k].get("shop_qty", tk.StringVar(value="5000")).get() if "shop_qty" in gui_vars[k] else "5000",
                "shop_price": gui_vars[k].get("shop_price", tk.StringVar(value="700")).get() if "shop_price" in gui_vars[k] else "700",
                "shop_info": gui_vars[k].get("shop_info", tk.StringVar(value="dyddl 700")).get() if "shop_info" in gui_vars[k] else "dyddl 700",
                "auth_main_id": gui_vars[k]["auth_main_id"].get().strip() if "auth_main_id" in gui_vars[k] else "",
                "auth_main_pw": gui_vars[k]["auth_main_pw"].get().strip() if "auth_main_pw" in gui_vars[k] else "",
                "auth_main_email": gui_vars[k]["auth_main_email"].get().strip() if "auth_main_email" in gui_vars[k] else "",
                "auth_main_phone": gui_vars[k]["auth_main_phone"].get().strip() if "auth_main_phone" in gui_vars[k] else "",
                "auth_delay_use": gui_vars[k]["auth_delay_use"].get() if "auth_delay_use" in gui_vars[k] else False,
                "auth_auto_captcha": gui_vars[k]["auth_auto_captcha"].get() if "auth_auto_captcha" in gui_vars[k] else False,
                "auth_delay_start_min": int(safe_float(gui_vars[k]["auth_delay_start_min"], 55.0)) if "auth_delay_start_min" in gui_vars[k] else 55,
                "auth_delay_end_min": int(safe_float(gui_vars[k]["auth_delay_end_min"], 58.0)) if "auth_delay_end_min" in gui_vars[k] else 58,
                "auth_delay_sec": safe_float(gui_vars[k]["auth_delay_sec"], 180.0) if "auth_delay_sec" in gui_vars[k] else 180.0,
                # 👇👇👇 [추가] 뇌에 디버그 저장 좌표 동기화
                "dbg_x": saved_settings.get(k, {}).get("dbg_x", -1),
                "dbg_y": saved_settings.get(k, {}).get("dbg_y", -1)
            }
            
            if k in ai_states and k in hunt_btn_dict:
                if str(st.get("target_fsm", "")).startswith("CERTI_"):
                    fsm_status = f"🔐인증: {st.get('target_fsm')}"
                elif st.get("is_shop_active", False):
                    fsm_status = f"상점봇: {st.get('shop_fsm', 'IDLE')}"
                elif st.get("is_recall_active", False): # 🚀 [신규 추가]
                    fsm_status = f"회수봇: {st.get('recall_fsm', 'IDLE')}"
                elif st.get("is_hunt_active", False):
                    fsm_status = f"버프봇: {st.get('cmd_fsm', 'IDLE')}"
                else:
                    fsm_status = "대기중 (IDLE)"
                btn_dict[k].config(text=f" 👑 [{k}] 군주 통제 패널 (상태: {fsm_status})")

    root.after(500, sync_gui_vars)


def toggle_buff_bot(key):
    state = ai_states[key]
    
    # 🚨 상호 배제: 상점이 켜져 있으면 강제로 끕니다!
    if state.get("is_shop_active", False):
        state["is_shop_active"] = False
        s_btn = shop_btn_dict.get(key)
        if s_btn: s_btn.config(text="🏪 상점 대기", bg="#455A64", fg="white")
        with pico_queues[key].mutex: pico_queues[key].queue.clear()
        
    # 🚨 상호 배제: 회수봇이 켜져 있으면 강제로 끕니다!
    if state.get("is_recall_active", False):
        state["is_recall_active"] = False
        r_btn = recall_btn_dict.get(key)
        if r_btn: r_btn.config(text="🔄 회수 대기", bg="#455A64", fg="white")
        with pico_queues[key].mutex: pico_queues[key].queue.clear()
        
    state["is_hunt_active"] = not state.get("is_hunt_active", False)
    
    if state["is_hunt_active"]:
        my_server = "대기"
        for srv, m_list in SERVER_ASSIGNMENTS.items():
            if key in m_list:
                my_server = srv
                break
                
        if my_server != "대기":
            with global_req_queue.mutex:
                new_queue = []
                for req in global_req_queue.queue:
                    req_cid = str(req.get("char_id"))
                    try: r_pc = int(req_cid.split('-')[0])
                    except: r_pc = 0
                    if get_target_server(r_pc, req_cid) != my_server:
                        new_queue.append(req)
                global_req_queue.queue.clear()
                global_req_queue.queue.extend(new_queue)
                
            with task_lock:
                if my_server in reserved_servers:
                    del reserved_servers[my_server]
            print(f"🧹 [{key}] 버프 봇 가동! [{my_server}] 서버의 기존 대기열을 깔끔하게 리셋했습니다. (새 PING 순서대로 자동 등록됨)")

        state["is_paused"] = False
        state["cmd_fsm"] = "IDLE"
        state["target_client_id"] = None
        state["target_char_id"] = None
        state["was_manual_mode"] = True
        state["blue_pot_cd"] = 0
    else:
        release_central_ip_lock_async(key)
        state["abort_macro"] = True
        state["target_fsm"] = "IDLE"
        state["certi_last_box"] = None
        state["certi_from_closed_game"] = False
        with pico_queues[key].mutex: pico_queues[key].queue.clear()
        pico_queues[key].put({"action": "FORCE_RELEASE"})
            
    b_btn = hunt_btn_dict.get(key)
    if b_btn:
        if state["is_hunt_active"]: b_btn.config(text="▶ 버프 봇 가동 중", bg="#4CAF50", fg="white")
        else: b_btn.config(text="⚔️ 버프 봇 대기 중", bg="#455A64", fg="white")

def toggle_shop_bot(key):
    state = ai_states[key]
    
    # 🚨 상호 배제: 버프가 켜져 있으면 강제로 끕니다!
    if state.get("is_hunt_active", False):
        state["is_hunt_active"] = False
        b_btn = hunt_btn_dict.get(key)
        if b_btn: b_btn.config(text="⚔️ 버프 봇 대기 중", bg="#455A64", fg="white")
        with pico_queues[key].mutex: pico_queues[key].queue.clear()

    # 🚨 상호 배제: 회수봇이 켜져 있으면 강제로 끕니다!
    if state.get("is_recall_active", False):
        state["is_recall_active"] = False
        r_btn = recall_btn_dict.get(key)
        if r_btn: r_btn.config(text="🔄 회수 대기", bg="#455A64", fg="white")
        with pico_queues[key].mutex: pico_queues[key].queue.clear()

    state["is_shop_active"] = not state.get("is_shop_active", False)
    
    if state["is_shop_active"]:
        state["is_paused"] = False
        state["shop_fsm"] = "MONITOR"
        state["was_manual_mode"] = True
    else:
        release_central_ip_lock_async(key)
        state["abort_macro"] = True
        state["target_fsm"] = "IDLE"
        state["certi_last_box"] = None
        state["certi_from_closed_game"] = False
        with pico_queues[key].mutex: pico_queues[key].queue.clear()
        pico_queues[key].put({"action": "FORCE_RELEASE"})
            
    s_btn = shop_btn_dict.get(key)
    if s_btn:
        if state["is_shop_active"]: s_btn.config(text="▶ 상점 가동", bg="#E64A19", fg="white")
        else: s_btn.config(text="🏪 상점 대기", bg="#455A64", fg="white")

def toggle_recall_bot(key):
    state = ai_states[key]
    
    # 🚨 상호 배제: 버프가 켜져 있으면 강제로 끕니다!
    if state.get("is_hunt_active", False):
        state["is_hunt_active"] = False
        b_btn = hunt_btn_dict.get(key)
        if b_btn: b_btn.config(text="⚔️ 버프 봇 대기 중", bg="#455A64", fg="white")
        with pico_queues[key].mutex: pico_queues[key].queue.clear()

    # 🚨 상호 배제: 상점이 켜져 있으면 강제로 끕니다!
    if state.get("is_shop_active", False):
        state["is_shop_active"] = False
        s_btn = shop_btn_dict.get(key)
        if s_btn: s_btn.config(text="🏪 상점 대기", bg="#455A64", fg="white")
        with pico_queues[key].mutex: pico_queues[key].queue.clear()

    state["is_recall_active"] = not state.get("is_recall_active", False)
    
    if state["is_recall_active"]:
        state["is_paused"] = False
        state["recall_fsm"] = "IDLE" 
        state["was_manual_mode"] = True
    else:
        release_central_ip_lock_async(key)
        state["abort_macro"] = True
        state["target_fsm"] = "IDLE"
        state["certi_last_box"] = None
        state["certi_from_closed_game"] = False
        with pico_queues[key].mutex: pico_queues[key].queue.clear()
        pico_queues[key].put({"action": "FORCE_RELEASE"})
            
    r_btn = recall_btn_dict.get(key)
    if r_btn:
        if state["is_recall_active"]: r_btn.config(text="▶ 회수 가동", bg="#8E24AA", fg="white")
        else: r_btn.config(text="🔄 회수 대기", bg="#455A64", fg="white")

def arrange_windows():
    global CAPTURE_ROIS
    import win32gui
    import win32con
    from ctypes.wintypes import RECT
    
    client_w, client_h = 800, 600
    
    for pc_idx, pc in enumerate(MINI_PCS):
        key = pc["key"]
        title = pc["title"]
        hwnd = None
        
        # 🚀 각 미니컴의 고유 창 이름표를 핀셋으로 찾아서 1:1 완벽 매칭!
        def enum_windows_callback(h, _):
            nonlocal hwnd
            if win32gui.IsWindowVisible(h) and title in win32gui.GetWindowText(h):
                hwnd = h
        win32gui.EnumWindows(enum_windows_callback, None)
        
        if hwnd:
            try:
                target_x = int(gui_vars[key]["win_x"].get())
                target_y = int(gui_vars[key]["win_y"].get())
            except Exception:
                continue
                
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            rect = RECT(0, 0, client_w, client_h)
            ctypes.windll.user32.AdjustWindowRectEx(ctypes.byref(rect), style, False, ex_style)
            full_w, full_h, offset_x, offset_y = rect.right - rect.left, rect.bottom - rect.top, -rect.left, -rect.top
            
            try:
                win32gui.MoveWindow(hwnd, target_x, target_y, full_w, full_h, True)
            except Exception as e:
                print(f"⚠️ [{key}] 창 이동 권한 제한 무시 (현재 위치에서 캡처 진행): {e}")
            CAPTURE_ROIS[key] = {"top": target_y + offset_y, "left": target_x + offset_x, "width": client_w, "height": client_h}
            pc["pos"] = (target_x, target_y)
            print(f"🪟 [{key}] '{title}' 창 개별 정렬 완료 (위치: {target_x}, {target_y})")

def update_gui_status():
    if active_manual_target: lbl_status.config(text=f"[수동 모드] 🔴 {active_manual_target} 제어 획득! (종료: ` )", fg="#E53935")
    else: lbl_status.config(text=f"[네트워크] 커맨드 센터 소켓 통신 가동 중 📡", fg="#81C784")


# =================================================================
# 🚀 [디버그 창 표시 버그 완벽 수술] 
# TARGET_PC_KEY 편식을 없애고, 켜져있는 미니1~4 창을 모두 띄웁니다!
# =================================================================
debug_windows_moved = {}
raycast_windows_moved = {}

def debug_render_thread():
    global debug_windows_moved, raycast_windows_moved
    windows_opened = False
    
    while True:
        if DEBUG_MODE:
            windows_opened = True
            
            # 👇👇👇 [수술 4: 4클라 큐 전체 순회 및 렌더링 활성화] 👇👇👇
            for pc in MINI_PCS:
                key = pc["key"]
                has_updates = False
                has_raycast_updates = False
                
                img = None
                while not debug_queues[key].empty():
                    try: img = debug_queues[key].get_nowait()
                    except queue.Empty: break
                    
                if img is not None:
                    try: 
                        cv2.imshow(f"Debug_View_PC_{key[-1]}", img)
                        has_updates = True
                    except Exception: pass

                raycast_img = None
                while not raycast_debug_queues[key].empty():
                    try: raycast_img = raycast_debug_queues[key].get_nowait()
                    except queue.Empty: break
                    
                if raycast_img is not None:
                    try: 
                        cv2.imshow(f"Raycast_Nav_PC_{key[-1]}", raycast_img)
                        has_raycast_updates = True
                    except Exception: pass

                import win32api
                screen_w = win32api.GetSystemMetrics(0)
                
                gui_x, gui_y = safe_gui_x, safe_gui_y
                if gui_x < 0 or gui_y < 0: 
                    try: gui_x, gui_y = start_x, start_y
                    except: gui_x, gui_y = 0, 0
                    
                set_x = current_settings.get(key, {}).get("dbg_x", -1)
                set_y = current_settings.get(key, {}).get("dbg_y", -1)
                
                if set_x != -1 and set_y != -1:
                    debug_base_x = set_x
                    debug_base_y = set_y
                else:
                    # 지정 좌표가 없으면 바둑판 정렬
                    debug_base_x = gui_x
                    if debug_base_x + 800 > screen_w: debug_base_x = screen_w - 800
                    idx = int(key[-1]) - 1
                    debug_base_x = debug_base_x + (idx % 2) * 200
                    debug_base_y = gui_y + 100 + (idx // 2) * 200
                    
                ray_base_x = debug_base_x - 410

                if not isinstance(debug_windows_moved, dict): debug_windows_moved = {}
                if not isinstance(raycast_windows_moved, dict): raycast_windows_moved = {}

                if not debug_windows_moved.get(key, False) and has_updates:
                    try:
                        cv2.moveWindow(f"Debug_View_PC_{key[-1]}", max(0, debug_base_x), max(0, debug_base_y))
                        debug_windows_moved[key] = True
                    except: pass

                if not raycast_windows_moved.get(key, False) and has_raycast_updates:
                    try:
                        cv2.moveWindow(f"Raycast_Nav_PC_{key[-1]}", max(0, ray_base_x), max(0, debug_base_y)) 
                        raycast_windows_moved[key] = True
                    except: pass
            # 👆👆👆 ======================================================= 👆👆👆
            
            try: cv2.waitKey(30)
            except: pass
            
        else:
            if windows_opened:
                try: 
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)
                except: pass
                windows_opened = False
                debug_windows_moved = {}
                raycast_windows_moved = {}
                
            for pc in MINI_PCS:
                k = pc["key"]
                while not debug_queues[k].empty():
                    try: debug_queues[k].get_nowait()
                    except: break
                while not raycast_debug_queues[k].empty():
                    try: raycast_debug_queues[k].get_nowait()
                    except: break
                
        time.sleep(0.01)

style = ttk.Style()
try: style.theme_use('clam')
except: pass

BG_MAIN = "#1E1E1E"; BG_PANEL = "#2D2D30"; FG_TEXT = "#D4D4D4"

root.title(f"🛡️ 커맨드 센터 (중앙 통제실)")

screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
default_gui_x = screen_w - 860 - 20 
default_gui_y = screen_h - 620 - 60 # 👈 30픽셀 더 늘림

try: start_x = int(global_settings.get("gui_x", default_gui_x))
except: start_x = default_gui_x
try: start_y = int(global_settings.get("gui_y", default_gui_y))
except: start_y = default_gui_y

if start_x == 100 and start_y == 100: start_x, start_y = default_gui_x, default_gui_y

root.geometry(f"860x620+{start_x}+{start_y}") # 👈 30픽셀 더 늘림
root.configure(bg=BG_MAIN)

debug_var = tk.BooleanVar(value=DEBUG_MODE)
def toggle_debug():
    global DEBUG_MODE
    DEBUG_MODE = debug_var.get()

top_toolbar = tk.Frame(root, bg="#2D2D30", pady=4) 
top_toolbar.pack(fill="x")

btn_frame = tk.Frame(top_toolbar, bg="#2D2D30")
btn_frame.pack(side="left", padx=5)

# 🚀 [전체 창 정렬] 버튼 (누르면 각자 저장된 X,Y 좌표로 일제히 이동함)
btn_align = tk.Button(btn_frame, text="🪟 전체 창 정렬", font=("맑은 고딕", 8, "bold"), bg="#0E639C", fg="white", relief="flat", command=arrange_windows)
btn_align.pack(side="left", padx=2, ipadx=4, ipady=1)

coord_frame = tk.Frame(top_toolbar, bg="#2D2D30")
coord_frame.pack(side="right", padx=5)

tk.Label(coord_frame, text=" GUI X:", bg="#2D2D30", fg="#81C784", font=("맑은 고딕", 8)).pack(side="left", padx=1)
entry_gui_x = tk.Entry(coord_frame, width=4, font=("맑은 고딕", 8), justify="center", bg="#3E3E42", fg="white", insertbackground="white")
entry_gui_x.insert(0, str(start_x)); entry_gui_x.pack(side="left", padx=1)

tk.Label(coord_frame, text="Y:", bg="#2D2D30", fg="#81C784", font=("맑은 고딕", 8)).pack(side="left", padx=1)
entry_gui_y = tk.Entry(coord_frame, width=4, font=("맑은 고딕", 8), justify="center", bg="#3E3E42", fg="white", insertbackground="white")
entry_gui_y.insert(0, str(start_y)); entry_gui_y.pack(side="left", padx=1)

def save_gui_pos_command():
    entry_gui_x.delete(0, tk.END); entry_gui_x.insert(0, str(root.winfo_x()))
    entry_gui_y.delete(0, tk.END); entry_gui_y.insert(0, str(root.winfo_y()))
    save_settings()
    btn_save_gui.config(text="✅ 저장완료", bg="#2E7D32")
    root.after(2000, lambda: btn_save_gui.config(text="📍 GUI 저장", bg="#455A64"))

btn_save_gui = tk.Button(coord_frame, text="📍 GUI 저장", font=("맑은 고딕", 8, "bold"), bg="#455A64", fg="white", relief="flat", command=save_gui_pos_command)
btn_save_gui.pack(side="left", padx=5, ipadx=4, ipady=1)

lbl_status = tk.Label(root, text="[네트워크] 서버 포트 9999 가동 중 📡", bg=BG_MAIN, fg="#81C784", font=("맑은 고딕", 11, "bold"))
lbl_status.pack(pady=4)

frame_roles = tk.Frame(root, bg=BG_MAIN)
frame_roles.pack(fill="both", expand=True, pady=0, padx=10)
frame_roles.columnconfigure(0, weight=1)
frame_roles.columnconfigure(1, weight=1)

btn_dict = {}
pos_btn_dict = {}

# 🚀 [핵심] 각 미니컴마다 개별적으로 창 좌표를 찾아서 저장하는 전담 명령 함수 생성기
def create_save_pos_cmd(t_key, t_title):
    def cmd():
        import win32gui
        import win32con
        from ctypes.wintypes import RECT
        hwnd = None
        
        def enum_callback(h, _):
            nonlocal hwnd
            if win32gui.IsWindowVisible(h) and t_title in win32gui.GetWindowText(h): hwnd = h
        win32gui.EnumWindows(enum_callback, None)
        
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            gui_vars[t_key]["win_x"].set(str(rect[0]))
            gui_vars[t_key]["win_y"].set(str(rect[1]))
            save_settings()
            
            # 🚀 저장하는 즉시 파이썬의 눈(캡처 영역)을 해당 좌표로 완벽하게 동기화!
            client_w, client_h = 800, 600
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            client_rect = RECT(0, 0, client_w, client_h)
            ctypes.windll.user32.AdjustWindowRectEx(ctypes.byref(client_rect), style, False, ex_style)
            offset_x, offset_y = -client_rect.left, -client_rect.top
            CAPTURE_ROIS[t_key] = {"top": rect[1] + offset_y, "left": rect[0] + offset_x, "width": client_w, "height": client_h}
            
            print(f"✅ [{t_key}] 개별 창 위치 저장 및 캡처망 동기화 완료! (X:{rect[0]}, Y:{rect[1]})")
            
            btn = pos_btn_dict.get(t_key)
            if btn:
                btn.config(text="✅", bg="#2E7D32")
                root.after(1500, lambda b=btn: b.config(text="저장", bg="#455A64"))
        else:
            print(f"⚠️ [{t_key}] 화면에서 '{t_title}' 창을 찾을 수 없습니다! 파섹을 켜주세요.")
    return cmd

style.configure("TNotebook", background=BG_PANEL, borderwidth=0)
style.configure("TNotebook.Tab", background="#3E3E42", foreground="white", padding=[10, 2], font=("맑은 고딕", 8, "bold"))
style.map("TNotebook.Tab", background=[("selected", "#0E639C")], foreground=[("selected", "white")])

for i, pc in enumerate(MINI_PCS):
    key = pc["key"]
    title = pc["title"]
    
    # 최초 실행 시 테트리스처럼 겹치지 않게 가상 위치 부여
    default_x = 350 + (i % 2) * 800
    default_y = 100 + (i // 2) * 600
    
    if key not in gui_vars:
        gui_vars[key] = {}
        
    pc_saved = saved_settings.get(key, {})
    if "com_port" not in gui_vars[key]: gui_vars[key]["com_port"] = tk.StringVar(value=pc_saved.get("com_port", ""))
    if "use_blue_pot" not in gui_vars[key]: gui_vars[key]["use_blue_pot"] = tk.BooleanVar(value=pc_saved.get("use_blue_pot", False))
    if "blue_deficit" not in gui_vars[key]: gui_vars[key]["blue_deficit"] = tk.StringVar(value=str(pc_saved.get("blue_deficit", "11")))
    if "win_x" not in gui_vars[key]: gui_vars[key]["win_x"] = tk.StringVar(value=str(pc_saved.get("win_x", default_x)))
    if "win_y" not in gui_vars[key]: gui_vars[key]["win_y"] = tk.StringVar(value=str(pc_saved.get("win_y", default_y)))

    # 🔐 인증 탭 변수 안전 보장
    if "auth_main_id" not in gui_vars[key]: gui_vars[key]["auth_main_id"] = tk.StringVar(value=pc_saved.get("auth_main_id", ""))
    if "auth_main_pw" not in gui_vars[key]: gui_vars[key]["auth_main_pw"] = tk.StringVar(value=pc_saved.get("auth_main_pw", ""))
    if "auth_main_email" not in gui_vars[key]: gui_vars[key]["auth_main_email"] = tk.StringVar(value=pc_saved.get("auth_main_email", ""))
    if "auth_main_phone" not in gui_vars[key]: gui_vars[key]["auth_main_phone"] = tk.StringVar(value=pc_saved.get("auth_main_phone", ""))
    if "auth_delay_use" not in gui_vars[key]: gui_vars[key]["auth_delay_use"] = tk.BooleanVar(value=pc_saved.get("auth_delay_use", False))
    if "auth_auto_captcha" not in gui_vars[key]: gui_vars[key]["auth_auto_captcha"] = tk.BooleanVar(value=pc_saved.get("auth_auto_captcha", False))
    if "auth_delay_start_min" not in gui_vars[key]: gui_vars[key]["auth_delay_start_min"] = tk.StringVar(value=str(pc_saved.get("auth_delay_start_min", "55")))
    if "auth_delay_end_min" not in gui_vars[key]: gui_vars[key]["auth_delay_end_min"] = tk.StringVar(value=str(pc_saved.get("auth_delay_end_min", "58")))
    if "auth_delay_sec" not in gui_vars[key]: gui_vars[key]["auth_delay_sec"] = tk.StringVar(value=str(pc_saved.get("auth_delay_sec", "180")))
        
    vars_dict = gui_vars[key]
    
    row_idx = i // 2
    col_idx = i % 2
    
    col_frame = tk.LabelFrame(frame_roles, text=f" 👑 [{key}] 군주 제어 패널 ", font=("맑은 고딕", 10, "bold"), padx=6, pady=4, bg=BG_PANEL, fg="#FFD54F", bd=1)
    col_frame.grid(row=row_idx, column=col_idx, padx=5, pady=3, sticky="nsew") 
    btn_dict[key] = col_frame

    notebook = ttk.Notebook(col_frame)
    notebook.pack(side="top", fill="both", expand=True)

    tab_ctrl = tk.Frame(notebook, bg=BG_PANEL)
    tab_auth = tk.Frame(notebook, bg=BG_PANEL)
    notebook.add(tab_ctrl, text="👑 제어")
    notebook.add(tab_auth, text="🔐 인증")
    
    # =========================================================
    # [탭 1: 👑 제어] 기존 UI 100% 그대로 유지
    # =========================================================
    pos_frame = tk.Frame(tab_ctrl, bg=BG_PANEL)
    pos_frame.pack(side="top", fill="x", pady=(2, 2))
    tk.Label(pos_frame, text="📍 X:", bg=BG_PANEL, fg="#4FC3F7", font=("맑은 고딕", 8, "bold")).pack(side="left")
    tk.Entry(pos_frame, textvariable=vars_dict["win_x"], width=5, justify="center", bg="#3E3E42", fg="white", insertbackground="white").pack(side="left", padx=1)
    tk.Label(pos_frame, text="Y:", bg=BG_PANEL, fg="#4FC3F7", font=("맑은 고딕", 8, "bold")).pack(side="left", padx=1)
    tk.Entry(pos_frame, textvariable=vars_dict["win_y"], width=5, justify="center", bg="#3E3E42", fg="white", insertbackground="white").pack(side="left", padx=1)
    
    btn_save = tk.Button(pos_frame, text="저장", font=("맑은 고딕", 8, "bold"), bg="#455A64", fg="white", relief="flat", command=create_save_pos_cmd(key, title), pady=0)
    btn_save.pack(side="left", padx=(4, 0))
    pos_btn_dict[key] = btn_save

    port_frame = tk.Frame(tab_ctrl, bg=BG_PANEL)
    port_frame.pack(side="top", fill="x", pady=(2, 2))
    tk.Label(port_frame, text="🔌 COM", bg=BG_PANEL, fg="#FFF9C4", font=("맑은 고딕", 9, "bold")).pack(side="left", padx=(0, 2))
    
    import serial.tools.list_ports
    live_ports = [p.device for p in serial.tools.list_ports.comports()]
    current_port_val = vars_dict["com_port"].get()
    if current_port_val and current_port_val not in live_ports: live_ports.append(current_port_val)
    live_ports.sort(key=lambda x: int(x.replace("COM", "")) if x.startswith("COM") and x[3:].isdigit() else 999)
    
    cb_port = ttk.Combobox(port_frame, textvariable=vars_dict["com_port"], values=live_ports, width=6, font=("맑은 고딕", 8, "bold"))
    cb_port.pack(side="left", padx=1)
    
    def make_reconnect_cmd(t_key):
        def cmd():
            port_name = gui_vars[t_key]["com_port"].get().strip().upper()
            if port_name and not port_name.startswith("COM"): port_name = f"COM{port_name}"
            gui_vars[t_key]["com_port"].set(port_name)
            
            with pico_locks[t_key]:
                current_pico = picos.get(t_key)
                if current_pico and getattr(current_pico, 'is_open', False) and current_pico.port.upper() == port_name: return 
                if current_pico:
                    try: current_pico.close()
                    except: pass
                if port_name:
                    try: 
                        baud = globals().get("BAUD_RATE", 115200)
                        picos[t_key] = serial.Serial(port_name, baud, timeout=0, write_timeout=0)
                        print(f"✅ [{t_key}] 피코 연결 성공!")
                        if t_key in pico_queues: pico_queues[t_key].queue.clear()
                        reset_hw_key_states(picos[t_key])
                        if t_key in ai_states:
                            ai_states[t_key]["pico_arrived"] = True
                            ai_states[t_key]["hw_busy"] = False
                    except Exception as e:
                        picos[t_key] = None; print(f"⚠️ [{t_key}] 연결 실패! ({e})")
                else: picos[t_key] = None
            save_settings() 
        return cmd
        
    tk.Button(port_frame, text="연결", font=("맑은 고딕", 7), bg="#00838F", fg="white", relief="flat", command=make_reconnect_cmd(key), pady=0).pack(side="left", padx=1)

    def release_hardware_port(t_key):
        with pico_locks[t_key]:
            if picos.get(t_key):
                try: picos[t_key].close()
                except Exception: pass
            picos[t_key] = None
            if t_key in ai_states: ai_states[t_key]["pico_hwid"] = ""
        
        gui_vars[t_key]["com_port"].set("") 
        save_settings()
            
    tk.Button(port_frame, text="해제", font=("맑은 고딕", 7), bg="#C62828", fg="white", relief="flat", command=lambda k=key: release_hardware_port(k), pady=0).pack(side="left", padx=(1, 4))

    tk.Checkbutton(port_frame, text="dbg", variable=debug_var, command=toggle_debug, bg=BG_PANEL, fg="#FFF9C4", selectcolor="#3E3E42", font=("맑은 고딕", 7)).pack(side="left", padx=0)
    
    fps_var = tk.StringVar()
    current_fps = int(round(1.0 / GLOBAL_FRAME_DELAY))
    if current_fps == 24: fps_var.set("24 FPS")
    else: snapped_fps = max(15, min(60, int(round(current_fps / 5.0) * 5))); fps_var.set(f"{snapped_fps} FPS")

    def on_fps_change(event):
        global GLOBAL_FRAME_DELAY
        target_fps = int(event.widget.get().split(" ")[0])
        GLOBAL_FRAME_DELAY = 1.0 / target_fps 
        save_settings() 

    fps_options = ["15 FPS", "20 FPS", "24 FPS", "30 FPS", "40 FPS", "60 FPS"]
    cb_fps = ttk.Combobox(port_frame, textvariable=fps_var, values=fps_options, state="readonly", width=7, font=("맑은 고딕", 8))
    cb_fps.pack(side="left", padx=1)
    cb_fps.bind("<<ComboboxSelected>>", on_fps_change)

    import tkinter.ttk as ttk
    ttk.Separator(tab_ctrl, orient="horizontal").pack(fill="x", padx=2, pady=2)
    
    blue_frame = tk.Frame(tab_ctrl, bg=BG_PANEL)
    blue_frame.pack(side="top", fill="x", pady=1)
    tk.Checkbutton(blue_frame, text="파랭이(F7)", variable=vars_dict["use_blue_pot"], bg=BG_PANEL, fg="#4FC3F7", selectcolor="#3E3E42", font=("맑은 고딕", 8, "bold")).pack(side="left", padx=1)
    tk.Label(blue_frame, text="결손:", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left")
    tk.Entry(blue_frame, textvariable=vars_dict["blue_deficit"], width=4, justify="center", bg="#3E3E42", fg="white", insertbackground="white").pack(side="left", padx=1)
    tk.Label(blue_frame, text="방 이상 부족 시", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left")
    
    if "shop_item" not in gui_vars[key]: gui_vars[key]["shop_item"] = tk.StringVar(value=pc_saved.get("shop_item", "yongi"))
    if "shop_qty" not in gui_vars[key]: gui_vars[key]["shop_qty"] = tk.StringVar(value=pc_saved.get("shop_qty", "5000"))
    if "shop_price" not in gui_vars[key]: gui_vars[key]["shop_price"] = tk.StringVar(value=pc_saved.get("shop_price", "700"))
    if "shop_info" not in gui_vars[key]: gui_vars[key]["shop_info"] = tk.StringVar(value=pc_saved.get("shop_info", "dyddl 700"))

    ttk.Separator(tab_ctrl, orient="horizontal").pack(fill="x", padx=2, pady=2)
    shop_f1 = tk.Frame(tab_ctrl, bg=BG_PANEL)
    shop_f1.pack(side="top", fill="x", pady=1)
    tk.Label(shop_f1, text="🛒상점봇 | 품목:", bg=BG_PANEL, fg="#FFD54F", font=("맑은 고딕", 8, "bold")).pack(side="left", padx=(2,1))
    cb_shop_item = ttk.Combobox(shop_f1, textvariable=vars_dict["shop_item"], values=["yongi", "telleport"], width=8, font=("맑은 고딕", 8, "bold"))
    cb_shop_item.pack(side="left", padx=1)

    tk.Label(shop_f1, text="인출:", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left")
    tk.Entry(shop_f1, textvariable=vars_dict["shop_qty"], width=5, justify="center", bg="#3E3E42", fg="white", insertbackground="white").pack(side="left", padx=1)
    
    shop_f2 = tk.Frame(tab_ctrl, bg=BG_PANEL)
    shop_f2.pack(side="top", fill="x", pady=1)
    tk.Label(shop_f2, text="가격:", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left", padx=(4,0))
    tk.Entry(shop_f2, textvariable=vars_dict["shop_price"], width=5, justify="center", bg="#3E3E42", fg="white", insertbackground="white").pack(side="left", padx=1)
    tk.Label(shop_f2, text="간판(영타):", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left")
    tk.Entry(shop_f2, textvariable=vars_dict["shop_info"], width=13, justify="left", bg="#3E3E42", fg="white", insertbackground="white").pack(side="left", padx=1)

    ttk.Separator(tab_ctrl, orient="horizontal").pack(fill="x", padx=2, pady=2)
    lock_f = tk.Frame(tab_ctrl, bg=BG_PANEL)
    lock_f.pack(side="top", fill="x", pady=1)

    if "use_dir_lock" not in gui_vars[key]: gui_vars[key]["use_dir_lock"] = tk.BooleanVar(value=pc_saved.get("use_dir_lock", False))
    if "lock_dir" not in gui_vars[key]: gui_vars[key]["lock_dir"] = tk.StringVar(value=pc_saved.get("lock_dir", "9시"))

    tk.Checkbutton(lock_f, text="🔒방향잠금(거리2배)", variable=vars_dict["use_dir_lock"], bg=BG_PANEL, fg="#FF9800", selectcolor="#3E3E42", font=("맑은 고딕", 8, "bold")).pack(side="left", padx=1)
    cb_lock = ttk.Combobox(lock_f, textvariable=vars_dict["lock_dir"], values=["12시", "1시", "3시", "5시", "6시", "7시", "9시", "11시"], state="readonly", width=5, font=("맑은 고딕", 8, "bold"))
    cb_lock.pack(side="left", padx=2)
    tk.Label(lock_f, text="| 🔄회수: [qq/leave] 자동보관", bg=BG_PANEL, fg="#BA68C8", font=("맑은 고딕", 8, "bold")).pack(side="left", padx=2)

    test_frame = tk.LabelFrame(tab_ctrl, text=" 🎯 타점 팩트체크 (버튼 누르고 1.5초 내에 파섹화면으로!) ", font=("맑은 고딕", 9, "bold"), bg=BG_PANEL, fg="#FF9800", bd=1)

    def test_move_to_center(t_key):
        def _test_task():
            print(f"\n⏳ [{t_key}] 1.5초 뒤 진짜 영점(X:397, Y:245) 이동! 마우스를 파섹 화면으로 옮기세요!")
            import time
            time.sleep(1.5)
            
            if not picos.get(t_key): return print(f"❌ [{t_key}] 피코 연결 안됨!")
            with pico_queues[t_key].mutex: pico_queues[t_key].queue.clear()
            
            img_bgr = latest_frames.get(t_key)
            cur_x, cur_y = ai_states.get(t_key, {}).get("cursor_pos", [400, 300])
            
            if img_bgr is not None:
                real_cursor = find_cursor_pos(img_bgr, last_pos=(cur_x, cur_y), check_circle=True, allow_full_scan=True)
                if real_cursor:
                    cur_x, cur_y = real_cursor[0], real_cursor[1]
                    print(f"👁️ 팩트 커서 위치 스캔 완료: X:{int(cur_x)}, Y:{int(cur_y)}")
            
            tx, ty = 397, 245
            
            pico_queues[t_key].put({"action": "HOVER", "dx": tx - cur_x, "dy": ty - cur_y})
            pico_queues[t_key].put({"action": "SPECIAL_ACK"}) 
            if t_key in ai_states: ai_states[t_key]["cursor_pos"] = [tx, ty]

        import threading
        threading.Thread(target=_test_task, daemon=True).start()

    def test_throw_cursor(t_key):
        def _test_task():
            dir_str = gui_vars[t_key]["test_dir_var"].get()
            print(f"\n⏳ [{t_key}] 1.5초 뒤 '{dir_str}' 방향 투척! 마우스를 파섹 화면에 올리세요!")
            import time
            time.sleep(1.5) 

            if not picos.get(t_key): return print(f"❌ [{t_key}] 피코 연결 안됨!")
            with pico_queues[t_key].mutex: pico_queues[t_key].queue.clear()
            
            img_bgr = latest_frames.get(t_key)
            cur_x, cur_y = ai_states.get(t_key, {}).get("cursor_pos", [400, 300])
            h, w = 600, 800
            
            if img_bgr is not None:
                h, w = img_bgr.shape[:2]
                real_cursor = find_cursor_pos(img_bgr, last_pos=(cur_x, cur_y), check_circle=True, allow_full_scan=True)
                if real_cursor:
                    cur_x, cur_y = real_cursor[0], real_cursor[1]
                    print(f"👁️ 팩트 커서 위치 스캔 완료: X:{int(cur_x)}, Y:{int(cur_y)}")
            
            LINEAGE_ANGLES = { "1시": 330.0, "3시": 359.0, "5시": 30.0, "6시": 92.0, "7시": 150.0, "9시": 181.0, "11시": 210.0 }
            angle_deg = LINEAGE_ANGLES.get(dir_str, 30.0)
            
            char_screen_cx, char_screen_cy = 397, 245
            is_6_oclock = abs(angle_deg - 92.0) <= 10
            is_horizontal = any(abs(angle_deg - a) <= 10 for a in [0.0, 360.0, 359.0, 180.0, 181.0])
            
            if is_6_oclock: dist = 40.0
            elif is_horizontal: dist = 50.0
            else: dist = 30.0
                
            import math
            rad = math.radians(angle_deg)
            y_offset = -20 if is_6_oclock else -15
            
            tx = int(char_screen_cx + math.cos(rad) * dist)
            ty = int(char_screen_cy + math.sin(rad) * (dist * 0.85)) + y_offset
            
            tx = max(20, min(w - 20, tx))
            ty = max(5, min(int(h * 0.68), ty))

            pico_queues[t_key].put({"action": "HOVER", "dx": tx - cur_x, "dy": ty - cur_y})
            pico_queues[t_key].put({"action": "SPECIAL_ACK"}) 
            if t_key in ai_states: ai_states[t_key]["cursor_pos"] = [tx, ty]
            print(f"👉 팩트 타점 좌표 -> X: {tx}, Y: {ty} (거리: {dist}px, 높이보정: {y_offset}px)")

        import threading
        threading.Thread(target=_test_task, daemon=True).start()

    btn_center = tk.Button(test_frame, text="📍 1. 정중앙 영점(397) 팩트 체크", font=("맑은 고딕", 8, "bold"), bg="#0E639C", fg="white", relief="flat", command=lambda k=key: test_move_to_center(k))
    btn_center.pack(side="top", fill="x", padx=4, pady=2)

    throw_f = tk.Frame(test_frame, bg=BG_PANEL)
    throw_f.pack(side="top", fill="x", padx=4, pady=2)
    
    gui_vars[key]["test_dir_var"] = tk.StringVar(value="5시")
    cb_dir = ttk.Combobox(throw_f, textvariable=gui_vars[key]["test_dir_var"], values=["1시", "3시", "5시", "6시", "7시", "9시", "11시"], state="readonly", width=5, font=("맑은 고딕", 8, "bold"))
    cb_dir.pack(side="left", padx=2)
    
    btn_throw = tk.Button(throw_f, text="▶ 2. 버프 로직 투척", font=("맑은 고딕", 8, "bold"), bg="#E65100", fg="white", relief="flat", command=lambda k=key: test_throw_cursor(k))
    btn_throw.pack(side="left", fill="x", expand=True, padx=2)

    # =========================================================
    # [탭 2: 🔐 인증] 군주 개별 계정 + 딜레이 + 캡차자동(AI) + 수동실행
    # =========================================================
    auth_entries_this_pc = []
    auth_edit_var = tk.BooleanVar(value=False)

    def make_toggle_auth_edit(ent_list, ed_var):
        def _toggle():
            st_val = "normal" if ed_var.get() else "disabled"
            for e_w in ent_list:
                e_w.config(state=st_val)
            if not ed_var.get():
                save_settings()
        return _toggle

    a_row0 = tk.Frame(tab_auth, bg=BG_PANEL)
    a_row0.pack(side="top", fill="x", padx=4, pady=(2, 1))
    tk.Label(a_row0, text="🛡️ 계정 설정", font=("맑은 고딕", 8, "bold"), bg=BG_PANEL, fg="#FFD54F").pack(side="left")
    chk_edit = tk.Checkbutton(a_row0, text="수정", variable=auth_edit_var, bg=BG_PANEL, fg="#FF9800", selectcolor="#3E3E42", font=("맑은 고딕", 8, "bold"))
    chk_edit.pack(side="left", padx=4)
    tk.Checkbutton(a_row0, text="캡차자동(AI)", variable=vars_dict["auth_auto_captcha"], command=save_settings, bg=BG_PANEL, fg="#B2FF59", selectcolor="#3E3E42", font=("맑은 고딕", 8, "bold")).pack(side="right", padx=2)

    a_row1 = tk.Frame(tab_auth, bg=BG_PANEL)
    a_row1.pack(side="top", fill="x", padx=4, pady=1)
    tk.Label(a_row1, text="계정:", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left")
    e_id = tk.Entry(a_row1, textvariable=vars_dict["auth_main_id"], width=14, bg="#3E3E42", fg="white", insertbackground="white", disabledbackground="#252526", disabledforeground="#B0BEC5", state="disabled")
    e_id.pack(side="left", padx=(2, 6))
    tk.Label(a_row1, text="비번:", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left")
    e_pw = tk.Entry(a_row1, textvariable=vars_dict["auth_main_pw"], width=14, bg="#3E3E42", fg="white", insertbackground="white", disabledbackground="#252526", disabledforeground="#B0BEC5", state="disabled")
    e_pw.pack(side="left", padx=2)

    a_row2 = tk.Frame(tab_auth, bg=BG_PANEL)
    a_row2.pack(side="top", fill="x", padx=4, pady=1)
    tk.Label(a_row2, text="메일:", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left")
    e_em = tk.Entry(a_row2, textvariable=vars_dict["auth_main_email"], width=14, bg="#3E3E42", fg="white", insertbackground="white", disabledbackground="#252526", disabledforeground="#B0BEC5", state="disabled")
    e_em.pack(side="left", padx=(2, 6))
    tk.Label(a_row2, text="전번:", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left")
    e_ph = tk.Entry(a_row2, textvariable=vars_dict["auth_main_phone"], width=14, bg="#3E3E42", fg="white", insertbackground="white", disabledbackground="#252526", disabledforeground="#B0BEC5", state="disabled")
    e_ph.pack(side="left", padx=2)

    auth_entries_this_pc.extend([e_id, e_pw, e_em, e_ph])
    chk_edit.config(command=make_toggle_auth_edit(auth_entries_this_pc, auth_edit_var))

    a_row3 = tk.Frame(tab_auth, bg=BG_PANEL)
    a_row3.pack(side="top", fill="x", padx=4, pady=(2, 1))
    tk.Checkbutton(a_row3, text="시간딜레이:", variable=vars_dict["auth_delay_use"], command=save_settings, bg=BG_PANEL, fg="#4FC3F7", selectcolor="#3E3E42", font=("맑은 고딕", 8, "bold")).pack(side="left")
    tk.Entry(a_row3, textvariable=vars_dict["auth_delay_start_min"], width=3, justify="center", bg="#3E3E42", fg="white", font=("맑은 고딕", 8)).pack(side="left", padx=1)
    tk.Label(a_row3, text="~", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left")
    tk.Entry(a_row3, textvariable=vars_dict["auth_delay_end_min"], width=3, justify="center", bg="#3E3E42", fg="white", font=("맑은 고딕", 8)).pack(side="left", padx=1)
    tk.Label(a_row3, text="분 | 대기:", bg=BG_PANEL, fg=FG_TEXT, font=("맑은 고딕", 8)).pack(side="left")
    tk.Entry(a_row3, textvariable=vars_dict["auth_delay_sec"], width=4, justify="center", bg="#3E3E42", fg="#FFD54F", font=("맑은 고딕", 8, "bold")).pack(side="left", padx=1)
    tk.Label(a_row3, text="초", bg=BG_PANEL, fg="#FFD54F", font=("맑은 고딕", 8)).pack(side="left")

    a_row4 = tk.Frame(tab_auth, bg=BG_PANEL)
    a_row4.pack(side="top", fill="x", padx=4, pady=(2, 2))

    def _detect_cc_lan_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            lip = s.getsockname()[0]
            s.close()
            if lip and not lip.startswith("100.") and not lip.startswith("127."):
                return lip
        except Exception:
            pass
        return "192.168.0.141"

    proxy_ip_var = tk.StringVar(value=_detect_cc_lan_ip())
    tk.Label(a_row4, text="IP:", bg=BG_PANEL, fg="#4FC3F7", font=("맑은 고딕", 7, "bold")).pack(side="left")
    tk.Entry(a_row4, textvariable=proxy_ip_var, width=11, justify="center", bg="#3E3E42", fg="white", font=("맑은 고딕", 7)).pack(side="left", padx=(1, 2))

    def create_sub_on_mini_cc(target_key=key, ip_v=proxy_ip_var):
        p_serial = picos.get(target_key)
        p_lock = pico_locks.get(target_key)
        if not p_serial:
            print(f"❌ [{target_key}] 피코 연결 안됨!")
            return
        host_ip = ip_v.get().strip()
        my_port = MINI_PROXY_PORTS.get(target_key, 31281)

        def _worker():
            print(f"\n⚡ [{target_key}] 바탕화면 'sub' 우회 아이콘 자동 생성 시작! ({host_ip}:{my_port})")
            with pico_queues[target_key].mutex:
                pico_queues[target_key].queue.clear()
            reset_hw_key_states(p_serial)
            shift_map = {
                '!': ord('1'), '@': ord('2'), '#': ord('3'), '$': ord('4'), '%': ord('5'),
                '^': ord('6'), '&': ord('7'), '*': ord('8'), '(': ord('9'), ')': ord('0'),
                '_': ord('-'), '+': ord('='), '~': ord('`'), ':': ord(';'), '"': ord("'"),
                '<': ord(','), '>': ord('.'), '?': ord('/'), '{': ord('['), '}': ord(']'), '|': ord('\\')
            }
            def _tap(kcode, hold=0.055, wait=0.055):
                send_keyboard_key(p_serial, p_lock, kcode, 1, is_manual=False)
                time.sleep(hold)
                send_keyboard_key(p_serial, p_lock, kcode, 0, is_manual=False)
                time.sleep(wait)
            def _safe_type(text_str):
                for ch in text_str:
                    if ch in shift_map:
                        base_k = shift_map[ch]
                        send_keyboard_key(p_serial, p_lock, 129, 1, is_manual=False); time.sleep(0.055)
                        send_keyboard_key(p_serial, p_lock, base_k, 1, is_manual=False); time.sleep(0.055)
                        send_keyboard_key(p_serial, p_lock, base_k, 0, is_manual=False); time.sleep(0.055)
                        send_keyboard_key(p_serial, p_lock, 129, 0, is_manual=False); time.sleep(0.065)
                    elif 'A' <= ch <= 'Z':
                        kcode = ord(ch.lower())
                        send_keyboard_key(p_serial, p_lock, 129, 1, is_manual=False); time.sleep(0.055)
                        send_keyboard_key(p_serial, p_lock, kcode, 1, is_manual=False); time.sleep(0.055)
                        send_keyboard_key(p_serial, p_lock, kcode, 0, is_manual=False); time.sleep(0.055)
                        send_keyboard_key(p_serial, p_lock, 129, 0, is_manual=False); time.sleep(0.065)
                    else:
                        _tap(ord(ch), hold=0.050, wait=0.045)

            send_keyboard_key(p_serial, p_lock, 131, 1, is_manual=False); time.sleep(0.06)
            _tap(100, hold=0.06, wait=0.06)
            send_keyboard_key(p_serial, p_lock, 131, 0, is_manual=False); time.sleep(0.8)

            send_keyboard_key(p_serial, p_lock, 131, 1, is_manual=False); time.sleep(0.06)
            _tap(114, hold=0.06, wait=0.06)
            send_keyboard_key(p_serial, p_lock, 131, 0, is_manual=False); time.sleep(0.8)

            _tap(178, hold=0.05, wait=0.1)
            _safe_type("cmd")
            _tap(176, hold=0.06, wait=1.2)

            ps_cmd = (
                f'powershell -noprofile -command "'
                f'$w=new-object -com wscript.shell;'
                f'$s=$w.createshortcut($w.specialfolders(\'desktop\')+\'\\sub.lnk\');'
                f'$c=\'c:\\program files\\google\\chrome\\application\\chrome.exe\';'
                f'$s.targetpath=$c;'
                f'$s.arguments=\'--proxy-server={host_ip}:{my_port} https://store.plaync.com/store/linclassic?locale=ko-kr\';'
                f'$s.iconlocation=$c+\',4\';'
                f'$s.save()" && exit'
            )
            _safe_type(ps_cmd)
            _tap(176, hold=0.07, wait=0.5)
            print(f"✅ [{target_key}] 바탕화면 'sub' 바로가기 생성 완료! ({host_ip}:{my_port})")

        threading.Thread(target=_worker, daemon=True).start()

    def start_manual_certi_cc(target_key=key):
        if not picos.get(target_key):
            print(f"❌ [{target_key}] 피코가 연결되어 있지 않습니다!")
            return
        if active_manual_target == target_key:
            toggle_manual(None)
        st = ai_states[target_key]
        if not (st.get("is_hunt_active") or st.get("is_shop_active") or st.get("is_recall_active")):
            toggle_buff_bot(target_key)
        curr_t = time.time()
        st["certi_from_closed_game"] = True
        st["target_fsm"] = "CERTI_GOTO_DESKTOP"
        st["cooldown"] = curr_t + 0.5
        st["abort_macro"] = True
        with pico_queues[target_key].mutex:
            pico_queues[target_key].queue.clear()
        pico_queues[target_key].put({"action": "FORCE_RELEASE"})
        dprint(target_key, "🚀 [수동 웹인증 ➔ 게임접속] 시퀀스를 시작합니다!")

    def start_step13_cc(target_key=key):
        if not picos.get(target_key):
            print(f"❌ [{target_key}] 피코가 연결되어 있지 않습니다!")
            return
        if active_manual_target == target_key:
            toggle_manual(None)
        st = ai_states[target_key]
        if not (st.get("is_hunt_active") or st.get("is_shop_active") or st.get("is_recall_active")):
            toggle_buff_bot(target_key)
        curr_t = time.time()
        release_central_ip_lock_async(target_key)
        st["certi_13_wait_mode"] = "CLOSED_START"
        st["certi_next_desktop_time"] = 0.0
        st["target_fsm"] = "CERTI_STEP_13_FIND"
        st["cooldown"] = curr_t + 0.5
        st["abort_macro"] = True
        with pico_queues[target_key].mutex:
            pico_queues[target_key].queue.clear()
        pico_queues[target_key].put({"action": "FORCE_RELEASE"})
        dprint(target_key, "🎮 [13.png~ 게임접속] 시퀀스를 시작합니다!")

    tk.Button(a_row4, text="⚡sub생성", font=("맑은 고딕", 7, "bold"), bg="#00838F", fg="white", relief="flat", command=lambda k=key, iv=proxy_ip_var: create_sub_on_mini_cc(k, iv)).pack(side="left", padx=1)
    tk.Button(a_row4, text="🚀웹인증➔접속", font=("맑은 고딕", 7, "bold"), bg="#E65100", fg="white", relief="flat", command=lambda k=key: start_manual_certi_cc(k)).pack(side="left", fill="x", expand=True, padx=1)
    tk.Button(a_row4, text="🎮접속(13~)", font=("맑은 고딕", 7, "bold"), bg="#2E7D32", fg="white", relief="flat", command=lambda k=key: start_step13_cc(k)).pack(side="left", fill="x", expand=True, padx=1)

    # =========================================================
    # [하단 공통 버튼: 버프 봇 / 상점 봇 / 회수 봇]
    # =========================================================
    bottom_frame = tk.Frame(col_frame, bg=BG_PANEL)
    bottom_frame.pack(side="bottom", fill="x", pady=(3, 0))
    
    bottom_frame.columnconfigure(0, weight=2)
    bottom_frame.columnconfigure(1, weight=1)
    bottom_frame.columnconfigure(2, weight=1)
    
    b_btn = tk.Button(bottom_frame, text="⚔️ 버프 봇 대기 중", font=("맑은 고딕", 9, "bold"), bg="#455A64", fg="white", height=1, relief="flat", command=lambda k=key: toggle_buff_bot(k))
    b_btn.grid(row=0, column=0, sticky="ew", padx=(0, 1))
    hunt_btn_dict[key] = b_btn

    s_btn = tk.Button(bottom_frame, text="🏪 상점 대기", font=("맑은 고딕", 9, "bold"), bg="#455A64", fg="white", height=1, relief="flat", command=lambda k=key: toggle_shop_bot(k))
    s_btn.grid(row=0, column=1, sticky="ew", padx=(1, 1))
    shop_btn_dict[key] = s_btn

    r_btn = tk.Button(bottom_frame, text="🔄 회수 대기", font=("맑은 고딕", 9, "bold"), bg="#455A64", fg="white", height=1, relief="flat", command=lambda k=key: toggle_recall_bot(k))
    r_btn.grid(row=0, column=2, sticky="ew", padx=(1, 0))
    recall_btn_dict[key] = r_btn

tk.Label(root, text="※ 수동 제어 후 원래 상태로 복귀하려면 [`] 키(물결표 키)를 누르세요.", font=("맑은 고딕", 9), bg="#1E1E1E", fg="#757575").pack(pady=5)


# =====================================================================
# 💰 [장사 봇 무한 동력 엔진] Shop FSM 스레드
# =====================================================================
def auto_shop_worker_thread():
    # 🚀 매칭률 기본값을 0.82(82%)로 싹 다 하향 조정!
    def find_ww_img(img_bgr, name, threshold=0.82, log_key=None):
        if img_bgr is None or name not in WW_TEMPLATES: return None
        tmpl = WW_TEMPLATES[name]
        try:
            method_name = ""
            if tmpl["mask"] is not None:
                method_name = "컬러 매칭 (TM_CCORR_NORMED + 마스크O)"
                res = cv2.matchTemplate(img_bgr, tmpl["color"], cv2.TM_CCORR_NORMED, mask=cv2.merge([tmpl["mask"]]*3))
            else:
                method_name = "컬러 매칭 (TM_CCOEFF_NORMED + 마스크X)"
                res = cv2.matchTemplate(img_bgr, tmpl["color"], cv2.TM_CCOEFF_NORMED)
            
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            
            if log_key and name not in ["shop", "godam", "pick", "ok"]:
                import datetime
                t = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"[{t}] [{log_key}] 🔎 [물건 스캔] 대상: '{name}' | 방식: {method_name} | 매칭률: {max_val*100:.1f}% (커트라인: {threshold*100:.0f}%)", flush=True)

            if max_val >= threshold:
                h, w = tmpl["color"].shape[:2]
                return (max_loc[0] + w//2, max_loc[1] + h//2)
        except Exception: pass
        return None

    def get_real_cursor(key, img_bgr, state):
        old_cx, old_cy = state.get("cursor_pos", [400, 300])
        real_pos = find_cursor_pos(img_bgr, last_pos=(old_cx, old_cy), check_circle=True, allow_full_scan=True)
        if real_pos:
            state["cursor_pos"] = [real_pos[0], real_pos[1]]
            return real_pos[0], real_pos[1]
        return old_cx, old_cy

    def s_print(key, msg):
        import datetime
        t = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{t}] [{key}] {msg}", flush=True)

    while True:
        try:
            import time
            curr_time = time.time()
            for key in picos.keys():
                state = ai_states.get(key)
                settings = current_settings.get(key, {})
                
                if not state or not state.get("is_shop_active", False) or state.get("is_paused", False) or active_manual_target == key or str(state.get("target_fsm", "")).startswith("CERTI_"):
                    if state and "shop_fsm" in state and state["shop_fsm"] != "IDLE": 
                        s_print(key, "🛑 [장사 봇] 시스템 대기 중 (IDLE / 인증 대기)")
                        state["shop_fsm"] = "IDLE"
                    continue
                
                img_bgr = latest_frames.get(key)
                if img_bgr is None: continue
                
                if "shop_fsm" not in state or state["shop_fsm"] == "IDLE": 
                    s_print(key, "👀 [장사 봇] 상점 품절 감시(스캔) 모드를 시작합니다.")
                    state["shop_fsm"] = "MONITOR"
                    
                fsm = state["shop_fsm"]
                q = pico_queues[key]
                import random 
                import math 
                
                # 💡 [상태 1: 품절 감시]
                if fsm == "MONITOR":
                    if curr_time - state.get("last_shop_check", 0) > 1.0:
                        state["last_shop_check"] = curr_time
                        pos = find_ww_img(img_bgr, "shop", 0.82)
                        if not pos:
                            s_print(key, "🚨 [장사 봇] 상점 UI 증발 감지! (물건 완판). 인벤토리 닫기 및 창고 리필 시작!")
                            
                            # 🚀 [요청 기능 2] 물건 완판 후 창고 찾기 전에 ESC 2~3회 타건하여 열려있는 인벤토리 닫기
                            esc_cnt = random.randint(2, 3)
                            for _ in range(esc_cnt):
                                q.put({"action": "HOLD_KEY", "keycode": 177, "duration": g_val(0.06, 0.12)}) # 177: ESC키
                                q.put({"action": "WAIT", "delay_min": 0.15, "delay_max": 0.22}) # 🚀 속도 UP
                            q.put({"action": "WAIT", "delay_min": 0.3, "delay_max": 0.45}) # 🚀 속도 UP
                            
                            real_cursor = find_cursor_pos(img_bgr, last_pos=(400, 300), check_circle=True, allow_full_scan=True)
                            if real_cursor:
                                state["cursor_pos"] = [real_cursor[0], real_cursor[1]]
                                s_print(key, f"🎯 [영점 조준] 마우스 위치 파악 완료! (X:{int(real_cursor[0])}, Y:{int(real_cursor[1])})")

                            state["shop_fsm"] = "GOTO_WAREHOUSE"
                            state["shop_retry_timer"] = curr_time + 0.75 # 🚀 속도 UP
                            state["pick_fail_count"] = 0 
                            
                # 💡 [상태 2-1: 고담 찾기]
                elif fsm == "GOTO_WAREHOUSE":
                    if curr_time > state.get("shop_retry_timer", 0):
                        pos = find_ww_img(img_bgr, "godam", 0.82)
                        if pos:
                            cx, cy = get_real_cursor(key, img_bgr, state)
                            
                            target_x = pos[0] + int(random.gauss(0, 2))
                            target_y = pos[1] + 30 + int(random.gauss(0, 2))
                            
                            s_print(key, f"🎯 [장사 봇] 창고지기 발견! 대화 시도.")
                            
                            q.put({"action": "SHOP_HOVER", "dx": target_x - cx, "dy": target_y - cy}) 
                            
                            q.put({"action": "WAIT", "delay_min": 0.3, "delay_max": 0.45}) # 🚀 속도 UP
                            q.put({"action": "SINGLE_ATTACK"})
                            q.put({"action": "WAIT", "delay_min": 0.75, "delay_max": 1.1}) # 🚀 속도 UP
                            state["cursor_pos"] = [target_x, target_y] 
                            state["shop_fsm"] = "CLICK_PICK"
                            state["shop_retry_timer"] = curr_time + 1.5 # 🚀 속도 UP
                        else:
                            s_print(key, "🏃 [장사 봇] 창고지기(고담) 찾는 중...")
                            state["shop_retry_timer"] = curr_time + 0.75
                            
                # 💡 [상태 2-2: 물건 찾는다(pick.png) 클릭]
                elif fsm == "CLICK_PICK":
                    if curr_time > state.get("shop_retry_timer", 0):
                        pos = find_ww_img(img_bgr, "pick", 0.82)
                        if pos:
                            state["pick_fail_count"] = 0 
                            cx, cy = get_real_cursor(key, img_bgr, state)
                            
                            target_x = pos[0] + int(random.gauss(0, 2))
                            # 🚨 [오류 원인 제거] Y축 3픽셀 위로 치던 꼼수 삭제! 안전하게 이미지 정중앙 완벽 타격!
                            target_y = pos[1] + int(random.gauss(0, 2))

                            s_print(key, f"📜 [장사 봇] 대화창 '물건을 찾는다' 클릭! (Y축 -3px 상향 보정 타격)")
                            
                            q.put({"action": "SHOP_HOVER", "dx": target_x - cx, "dy": target_y - cy}) 
                            
                            q.put({"action": "WAIT", "delay_min": 0.2, "delay_max": 0.35})
                            q.put({"action": "SINGLE_ATTACK"})
                            q.put({"action": "WAIT", "delay_min": 1.5, "delay_max": 1.8})
                            
                            state["cursor_pos"] = [target_x, target_y]
                            state["shop_scroll_count"] = 0 
                            state["shop_fsm"] = "WITHDRAW_ITEM"
                            state["shop_retry_timer"] = curr_time + 2.2 
                        else:
                            fail_cnt = state.get("pick_fail_count", 0) + 1
                            state["pick_fail_count"] = fail_cnt
                            
                            if fail_cnt >= 10:
                                # 🚀 [3분 수면 모드] 10회 실패 시 끄지 않고, 3분(180초) 동안 동면 후 재시도!
                                s_print(key, "💀 [장사봇 비상] '물건을 찾는다(pick.png)' 10회 탐색 실패! 3분(180초) 대기 후 다시 시도합니다.")
                                state["pick_fail_count"] = 0
                                
                                esc_cnt = random.randint(3, 4)
                                for _ in range(esc_cnt):
                                    q.put({"action": "HOLD_KEY", "keycode": 177, "duration": g_val(0.06, 0.12)})
                                    q.put({"action": "WAIT", "delay_min": 0.15, "delay_max": 0.25})
                                q.put({"action": "WAIT", "delay_min": 0.4, "delay_max": 0.6})
                                
                                state["shop_fsm"] = "SLEEP_RECOVERY"
                                state["shop_retry_timer"] = curr_time + 180.0 # ⏳ 여기서 180초의 가혹한 쿨타임(동면) 적용!
                                state["last_sleep_log"] = curr_time
                            else:
                                # 🚀 [스마트 롤백] ESC 타건 후 NPC 가림 방지를 위해 마우스 중앙 이동 및 팩트 스캔 연계!
                                s_print(key, f"⚠️ [장사 봇] 대화창(pick.png) 확인 실패 ({fail_cnt}/10). ESC 연타 및 마우스 중앙 이동 후 재도전합니다.")
                                
                                # 1. 꼬인 대화창/인벤토리를 닫기 위해 ESC 3~4회 타건
                                esc_cnt = random.randint(3, 4)
                                for _ in range(esc_cnt):
                                    q.put({"action": "HOLD_KEY", "keycode": 177, "duration": g_val(0.06, 0.12)})
                                    q.put({"action": "WAIT", "delay_min": 0.15, "delay_max": 0.25})
                                q.put({"action": "WAIT", "delay_min": 0.3, "delay_max": 0.5})
                                
                                # 2. 현재 커서 위치를 대충 잡고
                                cx, cy = get_real_cursor(key, img_bgr, state)
                                h, w = img_bgr.shape[:2]
                                
                                # 3. 화면 중앙 부근으로 마우스 휙 던지기 (NPC 툴팁 가림 방어)
                                center_x = (w // 2) + int(random.gauss(0, 40))
                                center_y = (h // 2) + int(random.gauss(0, 40))
                                center_x = max(20, min(w - 20, center_x))
                                center_y = max(5, min(int(h * 0.68), center_y))
                                
                                q.put({"action": "SHOP_HOVER", "dx": center_x - cx, "dy": center_y - cy})
                                state["cursor_pos"] = [center_x, center_y]
                                
                                # 4. 던진 자리에서 팩트 커서를 스캔하기 위한 전용 대기 상태로 이관!
                                state["shop_fsm"] = "VERIFY_CURSOR"
                                state["shop_retry_timer"] = curr_time + 1.0 # 마우스 날아가는 시간 대기

                # 💡 [상태 2-2-3: 마우스 던진 후 팩트 커서 스캔 (못 찾으면 비비면서 찾음)]
                elif fsm == "VERIFY_CURSOR":
                    # 🚀 피코 하드웨어가 ESC 연타와 마우스 이동을 완전히 끝냈을 때만(q.empty) 팩트 판독!
                    if curr_time > state.get("shop_retry_timer", 0) and q.empty() and not state.get("hw_busy", False):
                        cx, cy = state.get("cursor_pos", [400, 300])
                        # 팩트 커서 스캔 발동!
                        real_pos = find_cursor_pos(img_bgr, last_pos=(cx, cy), check_circle=True, allow_full_scan=True)
                        
                        if real_pos:
                            s_print(key, f"👁️ [장사 봇] 마우스 팩트 좌표 확보 완료 (X:{int(real_pos[0])}, Y:{int(real_pos[1])}). 고담 탐색 재개!")
                            state["cursor_pos"] = [real_pos[0], real_pos[1]]
                            # 위치를 팩트로 확인했으니 안전하게 창고지기 찾기로 롤백!
                            state["shop_fsm"] = "GOTO_WAREHOUSE"
                            state["shop_retry_timer"] = curr_time + 0.5
                        else:
                            # 🚨 못 찾았다면 마우스를 대각선 아래로 20~30픽셀씩 까딱까딱 움직이며 억지로 모습을 드러내게 만듦!
                            s_print(key, "⚠️ [장사 봇] 커서를 잃어버렸습니다! 조금씩 움직이면서 스캔을 시도합니다.")
                            h, w = img_bgr.shape[:2]
                            
                            move_x = int(random.choice([-1, 1]) * random.uniform(20, 30))
                            move_y = int(random.choice([-1, 1]) * random.uniform(20, 30))
                            
                            next_x = max(20, min(w - 20, cx + move_x))
                            next_y = max(5, min(int(h * 0.68), cy + move_y))
                            
                            q.put({"action": "SHOP_HOVER", "dx": next_x - cx, "dy": next_y - cy})
                            state["cursor_pos"] = [next_x, next_y]
                            state["shop_retry_timer"] = curr_time + 0.5 

                # 💡 [상태 2-2-5: 3분 대기 (수면)]
                elif fsm == "SLEEP_RECOVERY":
                    rem_time = int(state.get("shop_retry_timer", 0) - curr_time)
                    if rem_time > 0:
                        if curr_time - state.get("last_sleep_log", 0) > 10.0:
                            s_print(key, f"💤 [장사 봇] 10회 연속 실패로 인한 3분 휴식 중... 남은 시간: {rem_time}초")
                            state["last_sleep_log"] = curr_time
                    else:
                        s_print(key, "🔥 [장사 봇] 3분 휴식 종료! 마우스를 치우고 팩트 스캔부터 재시작합니다.")
                        # 깨어날 때도 마우스가 꼬여있을 수 있으므로 중앙으로 던지는 로직부터 진입!
                        cx, cy = get_real_cursor(key, img_bgr, state)
                        h, w = img_bgr.shape[:2]
                        center_x = max(20, min(w - 20, (w // 2) + int(random.gauss(0, 40))))
                        center_y = max(5, min(int(h * 0.68), (h // 2) + int(random.gauss(0, 40))))
                        q.put({"action": "SHOP_HOVER", "dx": center_x - cx, "dy": center_y - cy})
                        state["cursor_pos"] = [center_x, center_y]
                        
                        state["shop_fsm"] = "VERIFY_CURSOR"
                        state["shop_retry_timer"] = curr_time + 1.0

                # 💡 [상태 2-3: 창고에서 아이템 빼기]
                elif fsm == "WITHDRAW_ITEM":
                    if curr_time > state.get("shop_retry_timer", 0):
                        item_name = settings.get("shop_item", "yongi").lower()
                        # 👑 [아이템 한정] 창고 물건 찾을 때는 89% 엄격 검사!
                        pos = find_ww_img(img_bgr, item_name, 0.89, log_key=key) 
                        
                        if pos:
                            # 🚀 [버그 수술 1] 큐 비우기! 아직 피코에 전송되지 않고 대기 중인 잔여 휠 스크롤 명령 물리적 폭파!
                            with q.mutex: q.queue.clear()
                            
                            s_print(key, f"⏳ [장사 봇] 창고에서 [{item_name}] 포착! 잔여 휠 삭제 및 스크롤 관성 정지 0.8초 대기...")
                            state["item_search_fail_count"] = 0 # 🚀 발견 성공 시 실패 카운트 초기화
                            state["shop_fsm"] = "WITHDRAW_ITEM_STABLE"
                            # 🚀 [버그 수술 2] 리니지 클라이언트의 부드러운 스크롤(관성)이 완전히 멈추도록 0.8초 픽스
                            state["shop_retry_timer"] = curr_time + 0.8
                        else:
                            scroll_cnt = state.get("shop_scroll_count", 0)
                            if scroll_cnt < 20:
                                s_print(key, f"🔽 [장사 봇] 창고 리스트에 [{item_name}] 없음. 제자리에서 휠을 내립니다. (현재 {scroll_cnt+1}/20회)")
                                
                                q.put({"action": "MOUSE_WHEEL", "amount": -1}) 
                                q.put({"action": "WAIT", "delay_min": 0.15, "delay_max": 0.22}) # 🚀 속도 UP
                                
                                state["shop_scroll_count"] = scroll_cnt + 1
                                state["shop_retry_timer"] = curr_time + 0.3 # 🚀 속도 UP
                            else:
                                fail_cnt = state.get("item_search_fail_count", 0) + 1
                                state["item_search_fail_count"] = fail_cnt
                                state["shop_scroll_count"] = 0
                                
                                if fail_cnt >= 5:
                                    s_print(key, f"💀 [장사봇 비상] 5회 재시도 완료! 창고에 [{item_name}] 재고가 완벽히 오링났습니다! 매크로 강제 정지.")
                                    state["shop_fsm"] = "IDLE"
                                    state["item_search_fail_count"] = 0
                                    import tkinter as tk
                                    root.after(0, lambda k=key: toggle_shop_bot(k) if ai_states[k].get("is_shop_active") else None)
                                else:
                                    s_print(key, f"⚠️ [장사 봇] 창고 스크롤 실패 ({fail_cnt}/5). ESC 연타 후 창고지기(고담)부터 다시 찾습니다.")
                                    
                                    # 1. 꼬인 대화창/인벤토리를 닫기 위해 ESC 3~4회 타건
                                    esc_cnt = random.randint(3, 4)
                                    for _ in range(esc_cnt):
                                        q.put({"action": "HOLD_KEY", "keycode": 177, "duration": g_val(0.06, 0.12)})
                                        q.put({"action": "WAIT", "delay_min": 0.15, "delay_max": 0.25})
                                    q.put({"action": "WAIT", "delay_min": 0.3, "delay_max": 0.5})
                                    
                                    # 2. 툴팁 가림 방지 및 팩트 스캔을 위해 마우스를 화면 중앙 부근으로 던짐
                                    cx, cy = get_real_cursor(key, img_bgr, state)
                                    h, w = img_bgr.shape[:2]
                                    center_x = max(20, min(w - 20, (w // 2) + int(random.gauss(0, 40))))
                                    center_y = max(5, min(int(h * 0.68), (h // 2) + int(random.gauss(0, 40))))
                                    
                                    q.put({"action": "SHOP_HOVER", "dx": center_x - cx, "dy": center_y - cy})
                                    state["cursor_pos"] = [center_x, center_y]
                                    
                                    # 3. 팩트 스캔 후 창고지기 찾기(GOTO_WAREHOUSE)로 돌아가는 루틴으로 이관
                                    state["shop_fsm"] = "VERIFY_CURSOR"
                                    state["shop_retry_timer"] = curr_time + 1.0

                # 👇👇👇 [신규 추가] 스크롤 관성 정지 후 팩트 좌표 타격 👇👇👇
                elif fsm == "WITHDRAW_ITEM_STABLE":
                    if curr_time > state.get("shop_retry_timer", 0):
                        item_name = settings.get("shop_item", "yongi").lower()
                        # 🎯 0.8초 대기 후 완전히 멈춘 프레임에서 진정한 팩트 좌표 재스캔!
                        pos = find_ww_img(img_bgr, item_name, 0.89, log_key=key) 
                        
                        if pos:
                            state["shop_scroll_count"] = 0 
                            cx, cy = get_real_cursor(key, img_bgr, state)
                            qty = str(settings.get("shop_qty", "5000"))
                            
                            target_x = pos[0] + int(random.gauss(0, 2))
                            # 🚀 [완벽 수술 3] Y좌표를 7픽셀 강제로 끌어올려 아이템 칸의 '상단 안전구역'을 찌르도록 보정! (밑 템 클릭 원천 차단)
                            target_y = pos[1] - 7 + int(random.gauss(0, 2))
                            
                            s_print(key, f"📦 [장사 봇] 스크롤 안정화 완료! 상단 안전 좌표(Y:{target_y})에 [{item_name}] {qty}개 인출 시도.")
                            
                            q.put({"action": "SHOP_HOVER", "dx": target_x - cx, "dy": target_y - cy}) 
                            
                            q.put({"action": "WAIT", "delay_min": 0.2, "delay_max": 0.35}) # 🚀 속도 UP
                            q.put({"action": "SINGLE_ATTACK"})
                            
                            q.put({"action": "WAIT", "delay_min": 0.6, "delay_max": 0.9}) # 🚀 속도 UP
                            q.put({"action": "TYPE_STRING", "text": qty + "\n"}) 
                            q.put({"action": "WAIT", "delay_min": 0.6, "delay_max": 0.9}) # 🚀 속도 UP
                            
                            state["cursor_pos"] = [target_x, target_y]
                            state["shop_fsm"] = "CLOSE_WAREHOUSE"
                            state["shop_retry_timer"] = curr_time + 1.8 # 🚀 속도 UP
                        else:
                            # 🚀 관성 탓에 아이템이 화면 밖이나 위아래로 밀려났다면 다시 탐색 (오작동 방지)
                            s_print(key, f"⚠️ [장사 봇] 스크롤 관성 여파로 물건이 빗나갔습니다. 다시 탐색합니다.")
                            state["shop_fsm"] = "WITHDRAW_ITEM"
                            state["shop_retry_timer"] = curr_time + 0.1
                            
                # 💡 [상태 2-4: 창고 닫기 (ok.png)]
                elif fsm == "CLOSE_WAREHOUSE":
                    if curr_time > state.get("shop_retry_timer", 0):
                        pos = find_ww_img(img_bgr, "ok", 0.82)
                        if pos:
                            cx, cy = get_real_cursor(key, img_bgr, state)
                            s_print(key, "🚪 [장사 봇] 창고 닫기(O.K) 클릭. 상점 개설 준비...")
                            
                            target_x = pos[0] + int(random.gauss(0, 2))
                            target_y = pos[1] + int(random.gauss(0, 2))
                            
                            q.put({"action": "SHOP_HOVER", "dx": target_x - cx, "dy": target_y - cy})
                            
                            q.put({"action": "WAIT", "delay_min": 0.2, "delay_max": 0.35}) # 🚀 속도 UP
                            q.put({"action": "SINGLE_ATTACK"})
                            q.put({"action": "WAIT", "delay_min": 0.75, "delay_max": 1.1}) # 🚀 속도 UP
                            state["cursor_pos"] = [target_x, target_y]
                            state["shop_fsm"] = "OPEN_SHOP"
                            state["shop_retry_timer"] = curr_time + 1.5 # 🚀 속도 UP
                        else:
                            state["shop_retry_timer"] = curr_time + 0.75 # 🚀 속도 UP
                            
                # 💡 [상태 3-1: 상점 개설 F5]
                elif fsm == "OPEN_SHOP":
                    if curr_time > state.get("shop_retry_timer", 0):
                        s_print(key, "⛺ [장사 봇] 상점 개설 시도 (F5 -> Y -> Enter)")
                        q.put({"action": "HOLD_KEY", "keycode": KEY_F5, "duration": g_val(0.06, 0.12)})
                        q.put({"action": "WAIT", "delay_min": 0.35, "delay_max": 0.55}) # 🚀 속도 UP
                        q.put({"action": "TYPE_STRING", "text": "y\n"})
                        q.put({"action": "WAIT", "delay_min": 1.1, "delay_max": 1.5}) # 🚀 속도 UP
                        
                        state["shop_fsm"] = "WAIT_SHOP_UI"
                        state["shop_retry_timer"] = curr_time + 0.1 # 🚀 하드웨어 큐(q) 검사로 넘김
                        state["shop_poll_start"] = 0 # 폴링 타이머 초기화
                        
                # 💡 [상태 3-2: 샵 열리는 것 확인]
                elif fsm == "WAIT_SHOP_UI":
                    # 1. 큐(q)가 완전히 비워지고 피코의 움직임이 끝났을 때부터 폴링(실시간 감시) 시작!
                    if q.empty() and not state.get("hw_busy", False):
                        if state.get("shop_poll_start", 0) == 0:
                            state["shop_poll_start"] = curr_time # 하드웨어 완료된 정확한 시점을 기록

                        pos = find_ww_img(img_bgr, "shop", 0.82)
                        
                        if pos:
                            s_print(key, f"✅ [장사 봇] 상점 UI 오픈 팩트 확인! (탐색 소요: {curr_time - state['shop_poll_start']:.2f}초)")
                            state["shop_ui_pos"] = pos
                            state["shop_scroll_count"] = 0 
                            state["shop_fsm"] = "DRAG_ITEM"
                            state["shop_retry_timer"] = curr_time + 0.75 
                            state["shop_poll_start"] = 0 # 다음을 위해 초기화
                        else:
                            # 2. 발견 못 했더라도 즉시 실패처리하지 않고 1.5초 동안 루프 돌면서 계속 감시!
                            if curr_time - state["shop_poll_start"] > 1.5:
                                s_print(key, "⚠️ [장사 봇] 상점 UI 1.5초 감시 초과 (타임아웃). F5 다시 시도합니다.")
                                state["shop_fsm"] = "OPEN_SHOP" 
                                state["shop_retry_timer"] = curr_time + 0.75 
                                state["shop_poll_start"] = 0 # 다음을 위해 초기화
                            
                # 💡 [상태 3-3: 인벤에서 샵으로 드래그 앤 드롭]
                elif fsm == "DRAG_ITEM":
                    if curr_time > state.get("shop_retry_timer", 0):
                        item_name = settings.get("shop_item", "yongi").lower()
                        h, w = img_bgr.shape[:2]
                        inven_roi = img_bgr[:, w//2:]
                        
                        pos_half = find_ww_img(inven_roi, item_name, 0.89, log_key=key) 
                        
                        if pos_half:
                            # 🚀 [버그 수술 1] 인벤토리 스크롤 중에도 잔여 휠 명령 완벽 폭파!
                            with q.mutex: q.queue.clear()
                            
                            s_print(key, f"⏳ [장사 봇] 인벤토리에서 [{item_name}] 포착! 잔여 휠 삭제 및 스크롤 관성 정지 0.8초 대기...")
                            state["shop_fsm"] = "DRAG_ITEM_STABLE"
                            state["shop_retry_timer"] = curr_time + 0.8 # 🚨 관성 대기 유지
                        else:
                            scroll_cnt = state.get("shop_scroll_count", 0)
                            if scroll_cnt < 20:
                                s_print(key, f"🔽 [장사 봇] 인벤토리에 [{item_name}] 없음. 제자리에서 휠을 내립니다. (현재 {scroll_cnt+1}/20회)")
                                
                                q.put({"action": "MOUSE_WHEEL", "amount": -1}) 
                                q.put({"action": "WAIT", "delay_min": 0.15, "delay_max": 0.22}) # 🚀 속도 UP
                                
                                state["shop_scroll_count"] = scroll_cnt + 1
                                state["shop_retry_timer"] = curr_time + 0.3 # 🚀 속도 UP
                            else:
                                s_print(key, f"💀 [장사봇 비상] 20회 스크롤 완료! 인벤토리에 팔려는 [{item_name}] 이/가 전혀 없습니다! 매크로 강제 정지.")
                                state["shop_fsm"] = "IDLE"
                                state["shop_scroll_count"] = 0
                                import tkinter as tk
                                root.after(0, lambda k=key: toggle_shop_bot(k) if ai_states[k].get("is_shop_active") else None)

                # 💡 [상태 3-3-2: 스크롤 관성 정지 후 팩트 좌표 드래그]
                elif fsm == "DRAG_ITEM_STABLE":
                    if curr_time > state.get("shop_retry_timer", 0):
                        item_name = settings.get("shop_item", "yongi").lower()
                        h, w = img_bgr.shape[:2]
                        inven_roi = img_bgr[:, w//2:]
                        
                        # 🎯 0.8초 대기 후 완전히 멈춘 프레임에서 재스캔!
                        pos_half = find_ww_img(inven_roi, item_name, 0.89, log_key=key) 
                        
                        if pos_half:
                            state["shop_scroll_count"] = 0 
                            cx, cy = get_real_cursor(key, img_bgr, state)
                            
                            tx = pos_half[0] + w//2 + int(random.gauss(0, 2))
                            # 🚀 [버그 수술 3] 인벤토리 드래그 시에도 Y좌표 7픽셀 강제 상향 보정!
                            ty = pos_half[1] - 7 + int(random.gauss(0, 2))
                            
                            s_print(key, f"🫴 [장사 봇] 스크롤 안정화 완료! 상단 안전 좌표(Y:{ty})에서 상점으로 정밀 드래그 슛!")
                            
                            q.put({"action": "SHOP_HOVER", "dx": tx - cx, "dy": ty - cy})
                            
                            q.put({"action": "WAIT", "delay_min": 0.3, "delay_max": 0.45}) # 🚀 속도 UP
                            
                            shop_cx, shop_cy = state["shop_ui_pos"]
                            
                            base_target_x = shop_cx + 25  
                            base_target_y = shop_cy + 65  
                            
                            target_x = base_target_x + int(random.gauss(0, 2))
                            target_y = base_target_y + int(random.gauss(0, 2))
                            target_x = max(base_target_x - 25, min(base_target_x + 25, target_x))
                            target_y = max(base_target_y - 25, min(base_target_y + 25, target_y))
                            
                            q.put({"action": "UI_DRAG", "dx": target_x - tx, "dy": target_y - ty})
                            q.put({"action": "WAIT", "delay_min": 0.75, "delay_max": 1.1}) # 🚀 속도 UP
                            state["cursor_pos"] = [target_x, target_y]
                            
                            state["shop_fsm"] = "ENTER_PRICE"
                            state["shop_retry_timer"] = curr_time + 1.5 # 🚀 속도 UP
                        else:
                            s_print(key, f"⚠️ [장사 봇] 스크롤 관성 여파로 물건이 빗나갔습니다. 다시 탐색합니다.")
                            state["shop_fsm"] = "DRAG_ITEM"
                            state["shop_retry_timer"] = curr_time + 0.1
                            
                # 💡 [상태 3-4: 가격/수량 입력]
                elif fsm == "ENTER_PRICE":
                    if curr_time > state.get("shop_retry_timer", 0):
                        price = str(settings.get("shop_price", "700"))
                        s_print(key, f"💰 [장사 봇] 판매가 [{price}]원 및 전체 수량 타이핑 중.")
                        q.put({"action": "TYPE_STRING", "text": price + "\n"})
                        q.put({"action": "WAIT", "delay_min": 0.6, "delay_max": 0.9}) # 🚀 속도 UP
                        
                        q.put({"action": "TYPE_STRING", "text": "\n"})
                        q.put({"action": "WAIT", "delay_min": 0.9, "delay_max": 1.35}) # 🚀 속도 UP
                        
                        state["shop_fsm"] = "WRITE_INFO"
                        state["shop_retry_timer"] = curr_time + 1.5 # 🚀 속도 UP
                        
                # 💡 [상태 4: 간판 영타 작성 및 O.K.]
                elif fsm == "WRITE_INFO":
                    if curr_time > state.get("shop_retry_timer", 0):
                        if "shop_ui_pos" in state:
                            cx, cy = state.get("cursor_pos", [400, 300])
                            
                            shop_cx, shop_cy = state["shop_ui_pos"]
                            base_target_x = shop_cx + SHOP_INFO_OFFSET_X
                            base_target_y = shop_cy + SHOP_INFO_OFFSET_Y
                            
                            target_x = base_target_x + int(random.gauss(0, 2))
                            target_y = base_target_y + int(random.gauss(0, 2))
                            
                            info_text = settings.get("shop_info", "dyddl 700")
                            s_print(key, f"✍️ [장사 봇] 절대좌표 난수타격(X:{target_x}, Y:{target_y}) 간판 작성 중: '{info_text}'")
                            
                            q.put({"action": "SHOP_HOVER", "dx": target_x - cx, "dy": target_y - cy})
                            
                            q.put({"action": "WAIT", "delay_min": 0.2, "delay_max": 0.35}) # 🚀 속도 UP
                            q.put({"action": "SINGLE_ATTACK"})
                            q.put({"action": "WAIT", "delay_min": 0.35, "delay_max": 0.55}) # 🚀 속도 UP
                            state["cursor_pos"] = [target_x, target_y]
                            
                            q.put({"action": "TYPE_STRING", "text": info_text}) 
                            q.put({"action": "WAIT", "delay_min": 0.75, "delay_max": 1.1}) # 🚀 속도 UP
                            
                            state["shop_fsm"] = "FINAL_OK"
                            state["shop_retry_timer"] = curr_time + 1.5 # 🚀 속도 UP
                        else:
                            s_print(key, "⚠️ [장사 봇] 상점 앵커(shop.png) 좌표 상실! 처음부터 다시 시도합니다.")
                            state["shop_fsm"] = "IDLE"
                            
                elif fsm == "FINAL_OK":
                    if curr_time > state.get("shop_retry_timer", 0):
                        if "shop_ui_pos" in state:
                            cx, cy = state.get("cursor_pos", [400, 300])
                            
                            shop_cx, shop_cy = state["shop_ui_pos"]
                            base_target_x = shop_cx + SHOP_OK_OFFSET_X
                            base_target_y = shop_cy + SHOP_OK_OFFSET_Y
                            
                            target_x = base_target_x + int(random.gauss(0, 2))
                            target_y = base_target_y + int(random.gauss(0, 2))
                            
                            s_print(key, f"🎉 [장사 봇] 상점 세팅 완료! O.K 난수타격(X:{target_x}, Y:{target_y}) 누르고 복귀합니다.")
                            
                            q.put({"action": "SHOP_HOVER", "dx": target_x - cx, "dy": target_y - cy})
                            
                            q.put({"action": "WAIT", "delay_min": 0.2, "delay_max": 0.35}) # 🚀 속도 UP
                            q.put({"action": "SINGLE_ATTACK"})
                            
                            # 🚀 [커서 치우기] 상점 O.K 클릭 후 커서를 위쪽 15도 각도 내 70~100픽셀 위로 이동
                            up_rad = math.radians(random.uniform(255.0, 285.0)) 
                            up_dist = random.uniform(70.0, 100.0)
                            
                            end_x = int(target_x + math.cos(up_rad) * up_dist)
                            end_y = int(target_y + math.sin(up_rad) * up_dist)
                            
                            h, w = img_bgr.shape[:2]
                            end_x = max(20, min(w - 20, end_x))
                            end_y = max(5, min(int(h * 0.68), end_y))
                            
                            q.put({"action": "WAIT", "delay_min": 0.3, "delay_max": 0.5}) # 🚀 속도 UP
                            q.put({"action": "SHOP_HOVER", "dx": end_x - target_x, "dy": end_y - target_y})
                            s_print(key, f"↗️ [장사 봇] OK 클릭 후 커서를 위쪽으로 치웁니다. (이동 위치: X:{end_x}, Y:{end_y})")
                            
                            state["cursor_pos"] = [end_x, end_y]
                            
                            state["shop_fsm"] = "MONITOR"
                            state["last_shop_check"] = curr_time
                        else:
                            s_print(key, "⚠️ [장사 봇] 상점 앵커(shop.png) 좌표 상실! 처음부터 다시 시도합니다.")
                            state["shop_fsm"] = "IDLE"
                            
        except Exception: pass
        time.sleep(0.1)

# =====================================================================
# 🔄 [무한 동력 엔진] 회수 봇 (Recall FSM) 일괄 보관 초고속 스레드
# =====================================================================
def auto_recall_worker_thread():
    import os, cv2, time, random, numpy as np
    
    # 1. 회수봇 전용 에셋 로드 (ok.png는 상점봇과 100% 동일한 ww 폴더 에셋 공유)
    recall_assets = {}
    for img_name in ["npc_hakim.png", "leave.png", "ok.png"]:
        path = os.path.join("qq", img_name)
        if not os.path.exists(path): path = os.path.join("ww", img_name) 
        if os.path.exists(path):
            bgra = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if bgra is not None:
                if len(bgra.shape) == 3 and bgra.shape[2] == 4:
                    recall_assets[img_name.split(".")[0]] = {"color": bgra[:, :, :3], "mask": bgra[:, :, 3]}
                else:
                    recall_assets[img_name.split(".")[0]] = {"color": cv2.imread(path, cv2.IMREAD_COLOR), "mask": None}

    def find_asset(img_bgr, name, threshold=0.82):
        if img_bgr is None: return None
        tmpl = recall_assets.get(name) or WW_TEMPLATES.get(name)
        if not tmpl: return None
        try:
            if tmpl["mask"] is not None: res = cv2.matchTemplate(img_bgr, tmpl["color"], cv2.TM_CCORR_NORMED, mask=cv2.merge([tmpl["mask"]]*3))
            else: res = cv2.matchTemplate(img_bgr, tmpl["color"], cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if max_val >= threshold:
                h, w = tmpl["color"].shape[:2]
                return (max_loc[0] + w//2, max_loc[1] + h//2)
        except Exception: pass
        return None

    def find_leave_img(img_bgr, item_name, threshold=0.85):
        if img_bgr is None or item_name == "없음": return None
        target_tmpl = None
        for t in LEAVE_TEMPLATES:
            if t["name"].replace(".png", "").replace(".jpg", "") == item_name:
                target_tmpl = t
                break
        if not target_tmpl: return None
        
        try:
            if target_tmpl["mask"] is not None: res = cv2.matchTemplate(img_bgr, target_tmpl["color"], cv2.TM_CCORR_NORMED, mask=cv2.merge([target_tmpl["mask"]]*3))
            else: res = cv2.matchTemplate(img_bgr, target_tmpl["color"], cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if max_val >= threshold:
                h, w = target_tmpl["color"].shape[:2]
                return (max_loc[0] + w//2, max_loc[1] + h//2)
        except Exception: pass
        return None

    # 🚀 [상점봇과 100% 동일] 매번 팩트 커서를 찾아 동기화합니다!
    def get_real_cursor(key, img_bgr, state):
        old_cx, old_cy = state.get("cursor_pos", [400, 300])
        real_pos = find_cursor_pos(img_bgr, last_pos=(old_cx, old_cy), check_circle=True, allow_full_scan=True)
        if real_pos:
            state["cursor_pos"] = [real_pos[0], real_pos[1]]
            return real_pos[0], real_pos[1]
        return old_cx, old_cy

    def r_print(key, msg):
        import datetime
        t = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{t}] [{key}] {msg}", flush=True)

    while True:
        try:
            curr_time = time.time()
            for key in picos.keys():
                state = ai_states.get(key)
                settings = current_settings.get(key, {})
                
                if not state or not state.get("is_recall_active", False) or state.get("is_paused", False) or active_manual_target == key or str(state.get("target_fsm", "")).startswith("CERTI_"):
                    if state and "recall_fsm" in state and state["recall_fsm"] != "IDLE": 
                        r_print(key, "🛑 [회수 봇] 대기 모드로 전환 (IDLE / 인증 대기)")
                        state["recall_fsm"] = "IDLE"
                    continue
                
                img_bgr = latest_frames.get(key)
                if img_bgr is None: continue
                if "recall_fsm" not in state: state["recall_fsm"] = "IDLE"
                
                fsm = state["recall_fsm"]
                q = pico_queues[key]
                
                if fsm == "IDLE":
                    if curr_time - state.get("last_weight_check", 0) > 1.5:
                        state["last_weight_check"] = curr_time
                        weight_status = check_weight_status(img_bgr)
                        if weight_status > 0:
                            r_print(key, f"⚖️ [회수 봇] 무게 무거움 감지! 하킴 탐색 시작.")
                            state["recall_fsm"] = "FIND_HAKIM"
                            state["recall_retry_timer"] = curr_time + 0.3
                            
                elif fsm == "FIND_HAKIM":
                    # 🚀 이전 명령이 끝나고 큐가 비었을 때만 진행
                    if curr_time > state.get("recall_retry_timer", 0) and q.empty() and not state.get("hw_busy", False):
                        pos = find_asset(img_bgr, "npc_hakim", 0.75)
                        if pos:
                            cx, cy = get_real_cursor(key, img_bgr, state)
                            target_x = pos[0] + random.randint(-1, 1)
                            # 🚀 [오더 적용] 하킴 타격점 +45px (하향 보정)
                            target_y = pos[1] + 45 + random.randint(-1, 1) 
                            
                            r_print(key, f"🎯 [회수 봇] 창고지기 발견! 대화 시도. (Y:+45 타격)")
                            q.put({"action": "SHOP_HOVER", "dx": target_x - cx, "dy": target_y - cy}) 
                            q.put({"action": "WAIT", "delay_min": 0.08, "delay_max": 0.12}) 
                            q.put({"action": "SINGLE_ATTACK"})
                            q.put({"action": "WAIT", "delay_min": 0.5, "delay_max": 0.7})
                            
                            state["cursor_pos"] = [target_x, target_y] 
                            state["recall_fsm"] = "CLICK_LEAVE"
                            state["recall_retry_timer"] = curr_time + 0.5 
                        else:
                            state["recall_retry_timer"] = curr_time + 0.3

                elif fsm == "CLICK_LEAVE":
                    if curr_time > state.get("recall_retry_timer", 0) and q.empty() and not state.get("hw_busy", False):
                        pos = find_asset(img_bgr, "leave", 0.75)
                        if pos:
                            cx, cy = get_real_cursor(key, img_bgr, state)
                            target_x = pos[0] + random.randint(-1, 1)
                            # 🚀 [오더 적용] 맡긴다 타격점 +3px 및 Y 지터(난수) 2 고정
                            target_y = pos[1] + 3 + random.randint(-2, 2)

                            r_print(key, f"📜 [회수 봇] '물건을 맡긴다' 클릭! (Y:+3 타격, 난수 2)")
                            q.put({"action": "SHOP_HOVER", "dx": target_x - cx, "dy": target_y - cy}) 
                            q.put({"action": "WAIT", "delay_min": 0.08, "delay_max": 0.12}) 
                            q.put({"action": "SINGLE_ATTACK"})
                            q.put({"action": "WAIT", "delay_min": 0.4, "delay_max": 0.5}) 
                            
                            state["cursor_pos"] = [target_x, target_y]
                            state["recall_scroll_count"] = 0 
                            state["prev_left_roi"] = None 
                            
                            # 🚀 [수정] qq/leave 폴더에 로드된 모든 아이템 이름을 타겟 리스트로 싹쓸이 장전!
                            raw_items = [t["name"].replace(".png", "").replace(".jpg", "") for t in LEAVE_TEMPLATES]
                            state["target_items"] = list(set(raw_items))
                            
                            if not state["target_items"]:
                                r_print(key, "⚠️ [회수 봇] 설정된 항목이 없습니다! 조기 종료.")
                                state["recall_fsm"] = "EARLY_FINISH"
                                state["recall_retry_timer"] = curr_time + 0.2
                            else:
                                r_print(key, f"📝 [회수 봇] 다중 동시 스캔 리스트 장전: {state['target_items']}")
                                state["recall_fsm"] = "SEARCH_ITEM"
                                state["recall_retry_timer"] = curr_time + 0.3 
                        else:
                            state["recall_fsm"] = "FIND_HAKIM"
                            state["recall_retry_timer"] = curr_time + 0.3

                elif fsm == "SEARCH_ITEM":
                    # 🚨 [가장 중요한 핵심 수술] 하드웨어 큐가 완전히 비어있을 때만 진입! (비동기 엇박자 완벽 방어)
                    if curr_time > state.get("recall_retry_timer", 0) and q.empty() and not state.get("hw_busy", False):
                        target_items = state.get("target_items", [])
                        
                        if not target_items:
                            r_print(key, "✨ [회수 봇] 모든 지정 품목 수량 입력 완료! O.K 버튼 클릭으로 이동.")
                            state["recall_fsm"] = "CLICK_OK"
                            state["recall_retry_timer"] = curr_time + 0.1
                            continue

                        h, w = img_bgr.shape[:2]
                        left_roi = img_bgr[:max(0, h - 150), :400]
                        
                        # 🚀 [스마트 동결 감지] 커서 주변 30x30 구역만 핀셋 스캔!
                        cx, cy = state.get("cursor_pos", [400, 300])
                        sx1, sx2 = max(0, int(cx) - 15), min(w, int(cx) + 15)
                        sy1, sy2 = max(0, int(cy) - 15), min(h, int(cy) + 15)
                        
                        cursor_roi = img_bgr[sy1:sy2, sx1:sx2]
                        gray_cursor = cv2.cvtColor(cursor_roi, cv2.COLOR_BGR2GRAY)
                        
                        is_stuck = False
                        if state.get("prev_left_roi") is not None and state.get("recall_scroll_count", 0) > 0:
                            # 🚀 이전 프레임과 추출 크기가 동일할 때만 연산 (에러 방지)
                            if gray_cursor.shape == state["prev_left_roi"].shape:
                                diff = cv2.absdiff(gray_cursor, state["prev_left_roi"])
                                _, thresh = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)
                                # 30x30(900픽셀) 좁은 구역이므로 10픽셀 미만 변화 시 움직임 없음(동결)으로 판정
                                if cv2.countNonZero(thresh) < 10:
                                    state["scroll_stuck_count"] = state.get("scroll_stuck_count", 0) + 1
                                    # 🚀 [오더 적용] 변화 없을 시 5회 더 시도 (총 5회 누적 시 동결 확정)
                                    if state["scroll_stuck_count"] >= 5: 
                                        is_stuck = True
                                else:
                                    state["scroll_stuck_count"] = 0

                        # 💡 딕셔너리 키 이름(prev_left_roi)은 타 코드와의 호환성을 위해 유지하되 내용물은 30x30 커서 이미지를 담습니다.
                        state["prev_left_roi"] = gray_cursor.copy()
                        
                        if is_stuck:
                            # 🚀 [수정] 폴더 내 전체 아이템 개수를 기준으로 스크롤 바닥 도달 여부 계산!
                            raw_items = [t["name"].replace(".png", "").replace(".jpg", "") for t in LEAVE_TEMPLATES]
                            initial_count = len(set(raw_items))
                            
                            # 초기 개수보다 현재 남은 타겟 개수가 적다면 = 최소 1개는 찾아서 지웠다는 뜻!
                            has_found_any = len(state.get("target_items", [])) < initial_count
                            
                            if not has_found_any:
                                r_print(key, f"🏃 [회수 봇] 바닥 감지되었으나 아직 1개도 못 찾았습니다! 30회까지 강제 스크롤 돌파.")
                                is_stuck = False 
                                state["scroll_stuck_count"] = 0 # 카운터 초기화
                            else:
                                r_print(key, f"🚫 [회수 봇] 5회 연속 스크롤 바닥 감지! 남은 스크롤 횟수 무시하고 O.K 클릭 진행.")
                                state["target_items"] = []
                                state["recall_fsm"] = "CLICK_OK"
                                state["recall_retry_timer"] = curr_time + 0.1
                                continue

                        found_item_name = None
                        for item in target_items:
                            pos = find_leave_img(left_roi, item, 0.80)
                            if pos:
                                found_item_name = item
                                break 
                        
                        if found_item_name:
                            with q.mutex: q.queue.clear()
                            r_print(key, f"📦 [회수 봇] 창고 리스트에서 [{found_item_name}] 발견! 관성 정지 0.2초 대기...")
                            state["current_item_name"] = found_item_name
                            state["recall_scroll_count"] = 0 
                            state["scroll_stuck_count"] = 0
                            state["prev_left_roi"] = None 
                            state["recall_fsm"] = "CLICK_ITEM_STABLE"
                            state["recall_retry_timer"] = curr_time + 0.2 
                        else:
                            scroll_cnt = state.get("recall_scroll_count", 0)
                            if scroll_cnt < 100:
                                r_print(key, f"🔽 [회수 봇] 남은 항목 {target_items} 없음. 제자리 고속 스크롤 ({scroll_cnt+1}/100)")
                                q.put({"action": "MOUSE_WHEEL", "amount": -1}) 
                                q.put({"action": "WAIT", "delay_min": 0.04, "delay_max": 0.07}) 
                                
                                state["recall_scroll_count"] = scroll_cnt + 1
                                state["recall_retry_timer"] = curr_time + 0.1 
                            else:
                                r_print(key, f"⏭️ [회수 봇] 100회 제한 도달. O.K 클릭 진행.")
                                state["target_items"] = []
                                state["recall_fsm"] = "CLICK_OK"
                                state["recall_retry_timer"] = curr_time + 0.1

                # 🚨 [복구 완료] 삭제되었던 상태(fsm) 분기점 다시 이식
                elif fsm == "CLICK_ITEM_STABLE":
                    if curr_time > state.get("recall_retry_timer", 0) and q.empty() and not state.get("hw_busy", False):
                        current_item = state.get("current_item_name")
                        h, w = img_bgr.shape[:2]
                        # 🚀 [회수봇 최적화] 팩트 좌표 타격 시에도 동일하게 하단 채팅창 및 우측 영역 연산 컷!
                        left_roi = img_bgr[:max(0, h - 150), :400]
                        
                        pos = find_leave_img(left_roi, current_item, 0.80) 
                        
                        if pos:
                            state["recall_scroll_count"] = 0
                            cx, cy = get_real_cursor(key, img_bgr, state)
                            target_x = pos[0] + random.randint(-1, 1)
                            target_y = pos[1] - 7 + random.randint(-1, 1) 
                            
                            r_print(key, f"🫴 [회수 봇] 스크롤 안정화 완료. [{current_item}] 빛의 속도로 타격.")
                            q.put({"action": "SHOP_HOVER", "dx": target_x - cx, "dy": target_y - cy}) 
                            q.put({"action": "WAIT", "delay_min": 0.05, "delay_max": 0.08}) 
                            q.put({"action": "SINGLE_ATTACK"})
                            q.put({"action": "WAIT", "delay_min": 0.2, "delay_max": 0.3}) 
                            
                            hits = random.randint(4, 5)
                            num_str = "".join([str(random.randint(2, 9)) for _ in range(hits)])
                            r_print(key, f"⌨️ [회수 봇] 수량 난수 타건: {num_str}")
                            q.put({"action": "TYPE_STRING", "text": num_str + "\n"}) 
                            
                            state["cursor_pos"] = [target_x, target_y]
                            
                            if current_item in state.get("target_items", []):
                                state["target_items"].remove(current_item)
                                r_print(key, f"📝 [회수 봇] [{current_item}] 수량 입력 큐 전달 완료. 남은 품목: {state['target_items']}")
                            
                            state["prev_left_roi"] = None 
                            state["recall_fsm"] = "SEARCH_ITEM"
                            state["recall_retry_timer"] = curr_time + 0.1 
                        else:
                            state["recall_fsm"] = "SEARCH_ITEM"
                            state["recall_retry_timer"] = curr_time + 0.1

                elif fsm == "CLICK_OK":
                    # 🚨 [비동기 엇박자 완벽 방어] 하드웨어 큐가 완전히 비어서 타이핑(엔터)이 끝났을 때만 스캔!
                    if curr_time > state.get("recall_retry_timer", 0) and q.empty() and not state.get("hw_busy", False):
                        pos = find_asset(img_bgr, "ok", 0.82)
                        if pos:
                            cx, cy = get_real_cursor(key, img_bgr, state)
                            r_print(key, f"✅ [회수 봇] 다중 묶음 보관 최종 O.K 버튼 클릭.")
                            target_x = pos[0] + random.randint(-1, 1)
                            target_y = pos[1] + random.randint(-1, 1)
                            
                            q.put({"action": "SHOP_HOVER", "dx": target_x - cx, "dy": target_y - cy})
                            q.put({"action": "WAIT", "delay_min": 0.05, "delay_max": 0.08}) 
                            q.put({"action": "SINGLE_ATTACK"})
                            q.put({"action": "WAIT", "delay_min": 0.3, "delay_max": 0.4}) 
                            
                            state["cursor_pos"] = [target_x, target_y]
                            
                            state["recall_scroll_count"] = 0 
                            state["recall_fsm"] = "EARLY_FINISH"
                            state["recall_retry_timer"] = curr_time + 0.3 
                        else:
                            state["recall_retry_timer"] = curr_time + 0.2 

                elif fsm == "EARLY_FINISH":
                    if curr_time > state.get("recall_retry_timer", 0) and q.empty() and not state.get("hw_busy", False):
                        r_print(key, "🚪 [회수 봇] 임무 완수! ESC 연타로 창 닫기.")
                        
                        state["prev_left_roi"] = None 
                        
                        esc_cnt = random.randint(2, 3)
                        for _ in range(esc_cnt):
                            q.put({"action": "HOLD_KEY", "keycode": 177, "duration": g_val(0.03, 0.06)}) 
                            q.put({"action": "WAIT", "delay_min": 0.05, "delay_max": 0.08})
                        q.put({"action": "WAIT", "delay_min": 0.2, "delay_max": 0.3}) 
                        state["recall_fsm"] = "VERIFY_RECOVERY"
                        state["recall_retry_timer"] = curr_time + 0.4 

                elif fsm == "VERIFY_RECOVERY":
                    if curr_time > state.get("recall_retry_timer", 0) and q.empty() and not state.get("hw_busy", False):
                        weight_status = check_weight_status(img_bgr)
                        if weight_status == 0: 
                            r_print(key, "✨ [회수 봇] 무게 회색(정상) 확인! 대기 모드 복귀.")
                        else:
                            r_print(key, "⚠️ [회수 봇] 창고 정리 후에도 여전히 무겁습니다! 하킴을 다시 찾습니다.")
                        
                        # 🚀 [무한루프 버그 수술] 무겁든 가볍든 무조건 IDLE로 보내야 다시 하킴을 찾을 수 있습니다!
                        state["recall_fsm"] = "IDLE"
                        state["last_weight_check"] = curr_time

        except Exception: pass
        time.sleep(0.03) # 🚀 쓰레드 대기 속도 극강화

# =====================================================================


threading.Thread(target=auto_shop_worker_thread, daemon=True).start()
threading.Thread(target=auto_recall_worker_thread, daemon=True).start() # 🚀 [신규 추가] 회수 봇 가동!

sync_gui_vars() 
# 🚀 프로그램 시작 시 저장된 개별 위치로 전체 창 정렬 자동 실행
root.after(500, arrange_windows)

# 🚀 Tkinter 족쇄를 풀고, 독립된 스레드로 렌더링 엔진 가동! (파이썬 크래시 완벽 차단)
threading.Thread(target=debug_render_thread, daemon=True).start()

def auto_arrange_terminal():
    import ctypes, win32gui, win32con, win32api
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        try:
            if win32gui.IsIconic(hwnd): return
            gui_x, gui_y = root.winfo_x(), root.winfo_y()
            if gui_x < 0 or gui_y < 0: gui_x, gui_y = start_x, start_y
            
            term_w, term_h = 860, 300 # 👈 [수정] 메인 GUI 넓이에 맞춰 터미널도 860으로 확장!
            screen_w = win32api.GetSystemMetrics(0)
            
            target_x = gui_x
            if target_x + term_w > screen_w: target_x = screen_w - term_w
                
            target_y = gui_y - term_h - 10 
            
            flags = win32con.SWP_NOACTIVATE | win32con.SWP_NOZORDER | win32con.SWP_SHOWWINDOW
            win32gui.SetWindowPos(hwnd, 0, target_x, target_y, term_w, term_h, flags)
        except Exception: pass

# root.after(500, auto_arrange_terminal)

def on_closing():
    print("[SYSTEM] 💾 시스템 종료 및 GUI 설정 저장중...")
    try:
        with file_io_lock: _save_settings_internal() 
    except: pass
    if winmm: 
        try: winmm.timeEndPeriod(1)
        except: pass
    print("✅ 안전하게 강제 종료되었습니다.")
    import os
    os._exit(0) 

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
