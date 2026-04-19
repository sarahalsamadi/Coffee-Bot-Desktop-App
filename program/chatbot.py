from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout,QMessageBox,QFrame,QApplication,QSizePolicy
import sys
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
import google.generativeai as genai
from gtts import gTTS
import os
import speech_recognition as sr

# إعداد Google Generative AI
genai.configure(api_key="AIzaSyCYpzya0Rf7pf7Ay4u3Is-x0v94YYgiTdA")  # Replace with your API key


# إعداد مكتبة Google Generative AI

def get_gpt_response(prompt):
    try:
        # تحديد النموذج (يمكنك تغيير اسم النموذج إذا لزم الأمر)
        model = genai.GenerativeModel(model_name='gemini-pro')

        prompt_ = f'''
                أنت روبوت متخصص في مجال القهوة والشاي والمشروبات فقط، ولا يمكنك تقديم أي معلومات خارج هذا النطاق.
                إذا كان السؤال يتعلق بما يتعلق بالقهوة والشاي والمشروبات، أجب عليه بالتفصيل.
                إذا كان السؤال خارج هذا النطاق، أخبر المستخدم أنك لا تستطيع الإجابة على الأسئلة غير المتعلقة بالقهوة والمشروبات.

                سؤال المستخدم:
                {prompt}
                '''
        response = model.generate_content(prompt_)
        if response :
                return response.text
        else:
                return "لم أحصل على رد من الشات بوت."

    except Exception as e:
        return f"حدث خطأ: {e}"

# Function for text-to-speech
def text_to_speech(text, filename="response.mp3"):
    try:
        tts = gTTS(text=text, lang="ar")
        tts.save(filename)
        os.system(f"start {filename}" if os.name == "nt" else f"open {filename}")
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

# Function for speech-to-text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        message_box=create_message_box('معلومة','Please speak now...')
        message_box.exec()

        print("Please speak now...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="ar")
    except sr.UnknownValueError:
        return "Could not recognize the speech."
    except sr.RequestError:
        return "Error connecting to the speech recognition service."


def create_message_box( title, text, icon=QMessageBox.Icon.Information):
    message_box = QMessageBox()
    message_box.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setIcon(icon)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.setStyleSheet("""
        QMessageBox {
            background-color: rgba(232, 174, 133, 0.4);
            color: white;
            font-size: 14px;
        }
        QMessageBox QLabel {
            color: white;
        }
        QMessageBox QPushButton {
            background-color: black;
            color: white;
            border: none;
            padding: 5px;
        }
        QMessageBox QPushButton:hover {
            background-color: #555;
        }
    """)
    return message_box

class ChatbotWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('Chat.ui', self)  # تحميل ملف التصميم
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # إعداد تخطيط الحاوية الداخلية لـ QScrollArea
        existing_layout = self.chat_display.widget().layout()
        if existing_layout:
            QWidget().setLayout(existing_layout)  # إزالة التخطيط القديم إذا كان موجودًا

        self.chat_layout = QVBoxLayout(self.chat_display.widget())
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # محاذاة الرسائل للأعلى
      

        # تأكد من أن QScrollArea قابلة للتكيف مع المحتوى
        self.chat_display.setWidgetResizable(True)

        # ربط الأزرار بالأحداث
        self.send_button.clicked.connect(self.handle_text_input)
        self.voice_button.clicked.connect(self.handle_voice_input)
        self.output_button.clicked.connect(self.go_back)
        self.clear_button.clicked.connect(self.clear_chat)
        self.ExitButton.clicked.connect(self.close)

    def clear_chat(self):
        """مسح جميع الرسائل من صندوق الدردشة"""
        while self.chat_layout.count() > 0:
            item = self.chat_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
    def add_message_to_chatbox(self, sender, text):
        """إضافة الرسائل إلى نافذة الدردشة مع تحسين العرض"""
    # إنشاء إطار لحاوية الرسالة
        message_frame = QFrame()
        message_frame.setStyleSheet("border: none;")
        message_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

    # إعداد التخطيط الداخلي للرسالة
        message_layout = QVBoxLayout(message_frame)
        message_layout.setContentsMargins(0, 0, 0, 0)  # إزالة الهوامش الداخلية
        message_layout.setSpacing(0)  # إزالة المسافات الداخلية

    # إنشاء النص
        message_label = QLabel(text)
        message_label.setWordWrap(True)  # تغليف النصوص الطويلة
        message_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        message_label.setStyleSheet("padding: 10px; font-size: 14px;")

    # تخصيص تنسيق الرسالة بناءً على المرسل
        if sender == "user":
            message_label.setStyleSheet("""
        background-color: #707070;
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-size: 14px;
        """)
            message_layout.setAlignment(Qt.AlignmentFlag.AlignRight)  # محاذاة الرسالة لليمين
        else:
            message_label.setStyleSheet("""
        background-color: black;
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-size: 14px;
        """)
            message_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # محاذاة الرسالة لليسار

    # تحديد الحد الأقصى للعرض (80% من عرض نافذة التمرير)
        max_width = int(self.chat_display.width() * 0.8)
        message_label.setMaximumWidth(max_width)

    # إضافة الرسالة إلى التخطيط الداخلي
        message_layout.addWidget(message_label)

    # إضافة الرسالة إلى التخطيط الرئيسي
        self.chat_layout.addWidget(message_frame)

    # تحديث الحاوية الداخلية
        self.chat_display.widget().adjustSize()

    # تمرير الشاشة إلى آخر رسالة
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
        
    def handle_text_input(self):
        """معالجة إدخال نص المستخدم"""
        user_input = self.text_input.text().strip()
        if not user_input:
            return
        # إضافة رسالة المستخدم
        self.add_message_to_chatbox("user", user_input)
        self.text_input.clear()

        # استدعاء رد البوت
        response = self.get_bot_response(user_input)
        self.add_message_to_chatbox("bot", response)

    def handle_voice_input(self):
        """معالجة الإدخال الصوتي"""
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.add_message_to_chatbox("bot", "Listening...")  # إضافة رسالة "الاستماع..."
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language="ar-EG")  # التعرف على الصوت باللغة العربية
                self.add_message_to_chatbox("user", text)  # إضافة النص الذي تم التعرف عليه كرسالة من المستخدم
                response = self.get_bot_response(text)  # الحصول على رد من النظام
                self.add_message_to_chatbox("bot", response)
        except sr.UnknownValueError:
            self.add_message_to_chatbox("bot", "لم أتمكن من التعرف على الصوت. حاول مرة أخرى.")
        except sr.RequestError as e:
            self.add_message_to_chatbox("bot", f"حدث خطأ في خدمة التعرف على الصوت: {e}")

    def get_bot_response(self, user_input):
        """الحصول على رد البوت باستخدام Google Generative AI"""
        return get_gpt_response(user_input)

    def go_back(self):
        """العودة إلى الشاشة الرئيسية"""
        from main import HomeWindow
        self.home_window = HomeWindow()
        self.home_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotWindow()
    window.show()
    sys.exit(app.exec())