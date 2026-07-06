import os
from dotenv import load_dotenv
from google import genai
from openai import OpenAI, AzureOpenAI
from anthropic import Anthropic

# Tải dữ liệu cấu hình từ file .env vào hệ thống
load_dotenv()

# Lấy nhà cung cấp được chọn duy nhất cho phiên làm việc này
PROVIDER = os.getenv("ACTIVE_PROVIDER", "GEMINI").upper()

def goi_duy_nhat_mot_llm(cau_hoi):
    try:
        # TRƯỜNG HỢP 1: Chỉ gọi Azure OpenAI
        if PROVIDER == "AZURE":
            client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                api_version="2024-02-15-preview",
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            response = client.chat.completions.create(
                model=os.getenv("AZURE_DEPLOYMENT_NAME"),
                messages=[{"role": "user", "content": cau_hoi}]
            )
            return response.choices[0].message.content

        # TRƯỜNG HỢP 2: Chỉ gọi OpenAI (ChatGPT)
        elif PROVIDER == "OPENAI":
            client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": cau_hoi}]
            )
            return response.choices[0].message.content

        # TRƯỜNG HỢP 3: Chỉ gọi Google Gemini
        elif PROVIDER == "GEMINI":
            client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=cau_hoi
            )
            return response.text

        # TRƯỜNG HỢP 4: Chỉ gọi Anthropic Claude
        elif PROVIDER == "CLAUDE":
            client = Anthropic(api_key=os.getenv("CLAUDE_KEY"))
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1000,
                messages=[{"role": "user", "content": cau_hoi}]
            )
            return response.content[0].text
            
        else:
            return f"❌ Nền tảng '{PROVIDER}' trong cấu hình .env không hợp lệ."
            
    except Exception as e:
        return f"❌ Lỗi khi kết nối đến nhà cung cấp {PROVIDER}: {e}"

def main():
    print(f"🚀 AI ROUTER SWITCH - ĐANG KẾT NỐI DUY NHẤT ĐẾN: {PROVIDER}")
    print("Nhập câu hỏi của bạn. Gõ 'exit' hoặc 'thoat' để đóng chương trình.")
    print("-" * 60)
    
    while True:
        cau_hoi = input("\n👤 Bạn: ")
        
        # Nhận diện lệnh thoát từ bàn phím để bẻ gãy vòng lặp vô hạn
        if cau_hoi.strip().lower() in ['exit', 'thoat', 'quit']:
            print("👋 Đã đóng kết nối hệ thống Router. Tạm biệt!")
            break
            
        if not cau_hoi.strip():
            continue
            
        print(f"⏳ Đang định tuyến request và xử lý real-time tại {PROVIDER}...")
        tra_loi = goi_duy_nhat_mot_llm(cau_hoi)
        
        print(f"\n🤖 AI ({PROVIDER}):")
        print(tra_loi)
        print("-" * 60)

if __name__ == "__main__":
    main()