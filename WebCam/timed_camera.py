import threading
from PIL import Image
import cv2
import smtplib
import streamlit as st
from datetime import datetime
from fer import FER
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import io


emotion_detector = FER()

# Streamlit UI components
st.title("Motion and Emotion Detector with Email Alert")
start = st.button('Start Camera')
stop = st.button('Stop Camera')

SENDER_EMAIL = "naurangilal9675329115@gmail.com"
SENDER_PASSWORD = "tjuj lvro aswp gtdq" 
RECIPIENT_EMAIL = "naurangilal15072002@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def email(image_frame):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "Motion Detected!"
        
        img_byte_arr = io.BytesIO()
        img_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(img_frame)
        pil_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        image_attachment = MIMEImage(img_byte_arr.read())
        msg.attach(image_attachment)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")

def detect_motion(prev_frame, current_frame, threshold=10000):
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    frame_diff = cv2.absdiff(prev_gray, current_gray)
    _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
    non_zero_count = cv2.countNonZero(thresh)
    return non_zero_count > threshold, thresh

if start:
    st_image = st.image([])
    camera = cv2.VideoCapture(0)

    prev_frame = None
    motion_detected = False
    camera_active = True

    while camera_active:
        check, frame = camera.read()
        if not check:
            break

        motion = False

        if prev_frame is not None:
            motion, _ = detect_motion(prev_frame, frame)

            if motion and not motion_detected:
                motion_detected = True
                email_thread = threading.Thread(target=email, args=(frame,))
                email_thread.daemon=True
                email_thread.start()

        if not motion:
            motion_detected = False

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        now = datetime.now()
        date_text = now.strftime("%A")
        time_text = now.strftime("%H:%M:%S")

        emotions, score = emotion_detector.top_emotion(frame)
        
        cv2.putText(frame, date_text, (30, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, time_text, (30, 140), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv2.LINE_AA)
        
        if emotions is not None:
            emotion_text = f"Emotion: {emotions}"
            cv2.putText(frame, emotion_text, (30, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv2.LINE_AA)

        st_image.image(frame)

        prev_frame = frame

        if stop:
            camera_active = False
            st.stop()

    camera.release()
    print("Camera stopped.")
    st.stop()