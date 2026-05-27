import config
import numpy as np
import sympy as sp
from scipy import constants, integrate, optimize
from PIL import Image
from google import genai

client = genai.Client(api_key=config.api_key)

m, v, a, t, d, F, W, P, V, I, R = sp.symbols('m v a t d F W P V I R')

def display_header(title):
    print("\n" + "="*60)
    print(f"{title:^60}")
    print("="*60)

class AppController:
    def init(self):
        self.app_name = "Multi-Media Processor"

    def execute_process(self, user_text, file_path=None):
        try:
            if file_path:
                image = Image.open(file_path)
                import base64
                import io
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG')
                image_bytes = buffer.getvalue()
                image_b64 = base64.b64encode(image_bytes).decode()

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        {
                            "parts": [
                                {"text": user_text},
                                {
                                    "inline_data": {
                                        "mime_type": "image/jpeg",
                                        "data": image_b64
                                    }
                                }
                            ]
                        }
                    ]
                )
            else:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_text
                )
            return response.text
        except Exception as e:
            return f"حدث خطأ: {str(e)}"


def mechanical_laws():
    display_header("MECHANICAL PHYSICS")
    print("1. Newton's Force (F=ma) | 2. Work & Energy | 3. Momentum")


def advanced_scipy():
    display_header("ADVANCED CALCULUS & CONSTANTS")
    print(f"Plank's Constant (h): {constants.h}")
    print(f"Speed of Light (c): {constants.c}")


def main_menu():
    app = AppController()
    while True:
        display_header("THE MIND - ULTIMATE AI PHYSICS SUITE")
        print("1. AI Smart Solver (Text Input)")
        print("2. AI Image Solver (Scan & Solve)")
        print("3. Manual Physics Calculator")
        print("4. Advanced Calculus (SciPy)")
        print("5. Constants & Unit Conversions")
        print("0. Exit")
        choice = input("\nEnter choice (0-5): ")

        if choice == '1':
            text = input("اكتب سؤالك: ")
            print(app.execute_process(text))
        elif choice == '2':
            text = input("اكتب سؤالك: ")
            path = input("مسار الصورة: ")
            print(app.execute_process(text, path))
        elif choice == '3':
            mechanical_laws()
        elif choice == '4':
            advanced_scipy()
        elif choice == '5':
            print(f"Standard Gravity: {constants.g} m/s²")
            print(f"Electron Mass: {constants.m_e} kg")
        elif choice == '0':
            print("Shutting down. Goodbye!")
            break


if __name__ == "__main__":
    main_menu()
