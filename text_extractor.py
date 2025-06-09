import cv2
import pytesseract
import numpy as np
import re

def extract_date_time(display_img):
    h, w = display_img.shape[:2]
    # Crop lightweight (tune if needed!)
    date_img = display_img[0:int(h*0.22), :]
    time_img = display_img[int(h*0.36):int(h*0.75), :]
    
    # == Date extraction ==
    gray_date = cv2.cvtColor(date_img, cv2.COLOR_BGR2GRAY)
    _, thresh_date = cv2.threshold(gray_date, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Guarantee type for pytesseract
    thresh_date = np.ascontiguousarray(thresh_date.astype(np.uint8))
    raw_date = pytesseract.image_to_string(thresh_date, config='--psm 7')
    match_date = re.search(r"\d{2}\.\d{2}\.\d{2}", raw_date)
    extracted_date = match_date.group(0) if match_date else ""

    # == Time extraction ==
    gray_time = cv2.cvtColor(time_img, cv2.COLOR_BGR2GRAY)
    _, thresh_time = cv2.threshold(gray_time, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh_time = np.ascontiguousarray(thresh_time.astype(np.uint8))
    raw_time = pytesseract.image_to_string(
        thresh_time,
        config='--psm 7 -c tessedit_char_whitelist=0123456789:'
    )
    match_time = re.search(r"\d{2}:\d{2}", raw_time)
    extracted_time = match_time.group(0) if match_time else ""

    debug_imgs = {
        "date_crop": thresh_date,
        "time_crop": thresh_time
    }
    debug_raw = {
        "raw_date": raw_date,
        "raw_time": raw_time
    }
    return extracted_date, extracted_time, debug_imgs, debug_raw