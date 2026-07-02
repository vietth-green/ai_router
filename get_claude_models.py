import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Tải API Key từ file .env
load_dotenv()

def list_anthropic_models():
    try:
        # Khởi tạo client với API Key của Anthropic
        client = Anthropic(api_key=os.getenv("CLAUDE_KEY"))
        
        print("⏳ Đang kết nối và tải danh sách mô hình từ Anthropic...")
        print("-" * 60)
        
        # Gọi API lấy danh sách models
        models = client.models.list(limit=20)
        
        # Duyệt qua danh sách và in ra màn hình
        for model in models.data:
            print(f"📌 Model Name: {model.display_name}")
            print(f"   Model ID  : '{model.id}'")
            print(f"   Created At: {model.created_at}")
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ Không thể lấy danh sách model. Lỗi: {e}")
        print("💡 Vui lòng kiểm tra lại CLAUDE_KEY trong file .env hoặc số dư tài khoản.")

if __name__ == "__main__":
    list_anthropic_models()