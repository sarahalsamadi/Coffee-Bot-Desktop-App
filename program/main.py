import sys
from PyQt6.QtWidgets import QApplication, QWidget,QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from pymongo import MongoClient
from chatbot import ChatbotWindow
import google.generativeai as genai

class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('Home.ui', self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar
        self.HomeButton.clicked.connect(self.home)
        self.AboutButton.clicked.connect(self.about)
        self.MenuButton.clicked.connect(self.menu)
        self.ChatButton.clicked.connect(self.chat)
        self.ExitButton.clicked.connect(self.close)
        self.CartButton.clicked.connect(self.cart)
        self.About_Button.clicked.connect(self.about)

    def home(self):
        self.home_ = HomeWindow()
        self.home_.show()
        self.close()
    
    def about(self):
        self.about_ = AboutWindow()
        self.about_.show()
        self.close()

    def menu(self):
        self.menu_ = MenuWindow()
        self.menu_.show()
        self.close()

    def cart(self):
        self.cart_ = CartWindow()
        self.cart_.show()
        self.close()


    def chat(self):
        """Open the chatbot window."""
        self.chat_window = ChatbotWindow()
        self.chat_window.show()
        self.close()

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('About.ui', self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar
        self.HomeButton.clicked.connect(self.home)
        self.AbouButton.clicked.connect(self.about)
        self.MenuButton.clicked.connect(self.menu)
        self.ChatButton.clicked.connect(self.chat)
        self.ExitButton.clicked.connect(self.close)
        self.CartButton.clicked.connect(self.cart)
        self.Menu_Button.clicked.connect(self.menu)

    def home(self):
        self.home_ = HomeWindow()
        self.home_.show()
        self.close()
    
    def about(self):
        self.about_ = AboutWindow()
        self.about_.show()
        self.close()

    def menu(self):
        self.menu_ = MenuWindow()
        self.menu_.show()
        self.close()

    def cart(self):
        self.cart_ = CartWindow()
        self.cart_.show()
        self.close()

    def chat(self):
        """Open the chatbot window."""
        self.chat_window = ChatbotWindow()
        self.chat_window.show()
        self.close()

class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('Menu.ui', self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar
        self.HomeButton.clicked.connect(self.home)
        self.AbouButton.clicked.connect(self.about)
        self.MenuButton.clicked.connect(self.menu)
        self.ChatButton.clicked.connect(self.chat)
        self.ExitButton.clicked.connect(self.close)
        self.CartButton.clicked.connect(self.cart)
        self.add_price_cart1.clicked.connect(lambda: self.add_to_cart("Latte", 15.99))
        self.add_price_cart2.clicked.connect(lambda: self.add_to_cart("Iced Coffee", 15.99))
        self.add_price_cart3.clicked.connect(lambda: self.add_to_cart("Hot Chocolate", 15.99))

    def add_to_cart(self, product_name, price):
        for item in AppData.cart:
            if item["name"] == product_name:
                item["quantity"] += 1
                break
        else:
            AppData.cart.append({"name": product_name, "price": price, "quantity": 1})

        self.save_cart()

    def save_cart(self):
        if AppData.current_user:
            DatabaseConnection.db["users"].update_one(
                {"username": AppData.current_user},
                {"$set": {"cart": AppData.cart}}
            )

    def home(self):
        self.home_ = HomeWindow()
        self.home_.show()
        self.close()
    
    def about(self):
        self.about_ = AboutWindow()
        self.about_.show()
        self.close()

    def menu(self):
        self.menu_ = MenuWindow()
        self.menu_.show()
        self.close()

    def cart(self):
        self.cart_ = CartWindow()
        self.cart_.show()
        self.close()

    def chat(self):
        """Open the chatbot window."""
        self.chat_window = ChatbotWindow()
        self.chat_window.show()
        self.close()

class AppData:
    """بيانات مشتركة بين النوافذ"""
    current_user = None
    cart = []  # سلة المستخدم الحالي
    conversations = []

class CartWindow(QWidget):
    """نافذة السلة"""
    def __init__(self):
        super().__init__()
        loadUi('Cart.ui', self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.output_button.clicked.connect(self.back)
        self.ExitButton.clicked.connect(self.close)

        # ربط أزرار إضافة الكمية
        self.addbutton1.clicked.connect(lambda: self.update_cart("Latte", 1))
        self.addbutton2.clicked.connect(lambda: self.update_cart("Iced Coffee", 1))
        self.addbutton3.clicked.connect(lambda: self.update_cart("Hot Chocolate", 1))

        # ربط أزرار تقليل الكمية
        self.subbutton1.clicked.connect(lambda: self.update_cart("Latte", -1))
        self.subbutton2.clicked.connect(lambda: self.update_cart("Iced Coffee", -1))
        self.subbutton3.clicked.connect(lambda: self.update_cart("Hot Chocolate", -1))

        # ربط أزرار الحذف (تصفير الكمية)
        self.deletebutton1.clicked.connect(lambda: self.reset_item("Latte"))
        self.deletebutton2.clicked.connect(lambda: self.reset_item("Iced Coffee"))
        self.deletebutton3.clicked.connect(lambda: self.reset_item("Hot Chocolate"))

        # تحديث عرض السلة عند فتح النافذة
        self.update_cart_view()

    def update_cart(self, product_name, quantity_change):
        """تحديث كمية المنتج في السلة"""
        for item in AppData.cart:
            if item["name"] == product_name:
                item["quantity"] += quantity_change
                if item["quantity"] <= 0:
                    item["quantity"] = 0  # منع الكمية من أن تكون سالبة
                break
        else:
            # إذا لم يكن المنتج موجودًا وأضيفت كمية موجبة
            if quantity_change > 0:
                AppData.cart.append({"name": product_name, "price": 15.99, "quantity": 1})

        # حفظ التعديلات في قاعدة البيانات وتحديث العرض
        self.save_cart()
        self.update_cart_view()

    def reset_item(self, product_name):
        """تصفير كمية المنتج"""
        for item in AppData.cart:
            if item["name"] == product_name:
                item["quantity"] = 0  # تصفير الكمية
                break

        # حفظ التعديلات في قاعدة البيانات وتحديث العرض
        self.save_cart()
        self.update_cart_view()

    def save_cart(self):
        """حفظ السلة في قاعدة البيانات"""
        if AppData.current_user:
            DatabaseConnection.db["users"].update_one(
                {"username": AppData.current_user},
                {"$set": {"cart": AppData.cart}}
            )

    def update_cart_view(self):
        """تحديث واجهة السلة"""
        # تعيين القيم الافتراضية للـ labels إلى صفر
        if hasattr(self, "socurelabel1"):
            self.socurelabel1.setText("0")
            self.socurelabel2.setText("0")
            self.socurelabel3.setText("0")

            # تحديث القيم بناءً على السلة
            for item in AppData.cart:
                if item["name"] == "Latte":
                    self.socurelabel1.setText(str(item["quantity"]))
                elif item["name"] == "Iced Coffee":
                    self.socurelabel2.setText(str(item["quantity"]))
                elif item["name"] == "Hot Chocolate":
                    self.socurelabel3.setText(str(item["quantity"]))

    def back(self):
        """العودة إلى الصفحة الرئيسية"""
        self.back_ = HomeWindow()
        self.back_.show()
        self.close()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('Login.ui', self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar
        self.ExitButton.clicked.connect(self.close)
        self.output_button.clicked.connect(self.back)
        self.Login_Button.clicked.connect(self.handle_login)
        self.Sign_up_Button.clicked.connect(self.sign_up)
        self.users_collection = DatabaseConnection.db["users"]

    def handle_login(self):
        """التحقق من تسجيل الدخول باستخدام قاعدة بيانات MongoDB."""
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        # التحقق من الحقول الفارغة
        if not username or not password:
            QMessageBox.warning(self, "خطأ", "الحقول فارغة.")
            return

        try:
            # البحث عن المستخدم في قاعدة البيانات
            user = self.users_collection.find_one({"username": username})

            if user:
            # التحقق من كلمة المرور
                if user and user["password"] == password:
                    AppData.current_user = username  # تعيين المستخدم الحالي
                    AppData.cart = user.get("cart", [])
                    print(f"تم تسجيل الدخول: {AppData.current_user}")  # Debugging
                    self.home()  # الانتقال إلى الشاشة الرئيسية
                else:
                    message_box = create_message_box("خطأ", "كلمة المرور غير صحيحة.")
                    message_box.exec()
            else:
                message_box = create_message_box("خطأ", "اسم المستخدم غير موجود.")
                message_box.exec()
        except Exception as e:
            message_box = create_message_box("خطأ", f"حدث خطأ أثناء تسجيل الدخول: {e}")
            message_box.exec()

    def login_user(self, username):
        """تسجيل دخول المستخدم واسترجاع بياناته"""
        user = self.users_collection.find_one({"username": username})
        if user:
            AppData.current_user = username
            AppData.cart_count = user.get("cart_count", 0)  # استرجاع قيمة العداد أو استخدام 0 كافتراضي
            print(f"تم تسجيل الدخول باسم: {username}, قيمة العداد: {AppData.cart_count}")
        else:
            print("المستخدم غير موجود!")
    
    def sign_up(self):
        self.sign_up_=CreateWindow()
        self.sign_up_.show()
        self.close()

    def home(self):
        self.home_=HomeWindow()
        self.home_.show()
        self.close()

    def back(self):
        self.back_ = CreateWindow()
        self.back_.show()
        self.close()



class CreateWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('Create.ui', self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Disable the default title bar
        self.ExitButton.clicked.connect(self.close)
        self.Create_Button.clicked.connect(self.handle_register)
        self.Sign_In_Button.clicked.connect(self.sign_in)
        self.users_collection = DatabaseConnection.db["users"]
 
    def handle_register(self):
        """التحقق من صحة البيانات وإنشاء حساب جديد."""
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        confirm_password = self.input_confirmpassword.text().strip()

        # التحقق من الحقول الفارغة
        if not username or not password or not confirm_password:
            message_box = create_message_box("خطأ",  "جميع الحقول مطلوبة.",QMessageBox.Icon.Warning)
            message_box.exec()
            return

        if len(password) < 6:
            message_box = create_message_box("خطأ", "يجب أن تكون كلمة المرور 8 أحرف أو أكثر.", QMessageBox.Icon.Warning)
            message_box.exec()
            return

        # التحقق من مطابقة كلمة المرور
        if password != confirm_password:
            message_box = create_message_box("خطأ",  "كلمة المرور وتأكيد كلمة المرور غير متطابقين.",QMessageBox.Icon.Warning)
            message_box.exec()
            return

        try:
            # التحقق من إذا كان اسم المستخدم موجود بالفعل
            if self.users_collection.find_one({"username": username}):
                message_box = create_message_box("خطأ", "اسم المستخدم موجود بالفعل.",QMessageBox.Icon.Warning)
                message_box.exec()
                return

            # إضافة المستخدم إلى قاعدة البيانات
            self.users_collection.insert_one({
                "username": username,
                "password": password,
                "cart": [],
            })
            self.home()

        except Exception as e:
            message_box = create_message_box("خطأ", f"حدث خطأ أثناء إنشاء الحساب: {e}",QMessageBox.Icon.Critical)
            message_box.exec()

    def home(self):
        self.home_=HomeWindow()
        self.home_.show()
        self.close()
    
    def sign_in(self):
        self.sign_in_=LoginWindow()
        self.sign_in_.show()
        self.close()

class DatabaseConnection:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["U_database"]

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreateWindow()
    window.show()
    sys.exit(app.exec())
