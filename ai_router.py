import os
from google import genai
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv

# Tải cấu hình từ file .env vào hệ thống
load_dotenv()

# Khởi tạo các "nhân viên" AI bằng Key lấy từ môi trường (.env)
gemini_client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
claude_client = Anthropic(api_key=os.getenv("CLAUDE_KEY"))

def get_responses(cau_hoi):
    """Hàm điều phối câu hỏi đến đồng thời 3 mô hình AI"""
    results = {}

    # 1. Gọi Gemini
    try:
        response_gemini = gemini_client.models.generate_content(
            model='gemini-2.5-flash', # Phiên bản tối ưu tốc độ
            contents=cau_hoi
        )
        results['Gemini'] = response_gemini.text
    except Exception as e:
        results['Gemini'] = f"Lỗi: {e}"

    # 2. Gọi ChatGPT
    try:
        response_openai = openai_client.chat.completions.create(
            model="gpt-4o-mini", # Phiên bản nhẹ, tiết kiệm chi phí
            messages=[{"role": "user", "content": cau_hoi}]
        )
        results['ChatGPT'] = response_openai.choices[0].message.content
    except Exception as e:
        results['ChatGPT'] = f"Lỗi: {e}"

    # 3. Gọi Claude
    try:
        response_claude = claude_client.messages.create(
            model="claude-haiku-4-5-20251001", # Bản Haiku phản hồi nhanh
            max_tokens=1000,
            messages=[{"role": "user", "content": cau_hoi}]
        )
        results['Claude'] = response_claude.content[0].text
    except Exception as e:
        results['Claude'] = f"Lỗi: {e}"

    return results

def main():
    print("🚀 Khởi động hệ thống Multi-AI Router...")
    print("Hệ thống tích hợp: Gemini, ChatGPT, Claude.")
    print("-" * 60)
    
    while True:
        cau_hoi = input("\n👤 Nhập câu hỏi của bạn (hoặc gõ 'exit' để thoát): ")
        
        if cau_hoi.lower() in ['exit', 'quit']:
            print("Đang đóng hệ thống Router. Tạm biệt!")
            break
            
        if not cau_hoi.strip():
            continue
            
        print("\n⏳ Đang điều phối request tới các LLM Providers...")
        cac_cau_tra_loi = get_responses(cau_hoi)
        
        # In kết quả định dạng rõ ràng để so sánh
        for ai_name, resposta in cac_cau_tra_loi.items():
            print(f"\n==================== {ai_name.upper()} TRẢ LỜI ====================")
            print(resposta)
            
        print("\n" + "="*60)

if __name__ == "__main__":
    main()