import os
from dotenv import load_dotenv
from google import genai
from openai import OpenAI, AzureOpenAI
from anthropic import Anthropic

# Tải cấu hình bảo mật từ file .env
load_dotenv()

PROVIDER = os.getenv("ACTIVE_PROVIDER", "GEMINI").upper()
KB_FILE = "kb.txt"

def tim_kiem_gan_dung_kb(cau_hoi, threshold=0.25):
    """
    Tìm kiếm gần đúng (Fuzzy/Keyword Match) dựa trên mật độ trùng khớp từ khóa 
    trong từng đoạn văn bản của file kb.txt
    """
    if not os.path.exists(KB_FILE):
        return None
        
    try:
        with open(KB_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Chuẩn hóa ký tự xuống dòng và tách thành từng đoạn văn bản riêng biệt
        content = content.replace("\r\n", "\n")
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        
        # Danh sách các từ dừng (stop words) tiếng Việt cơ bản cần loại bỏ khi bóc tách từ khóa
        stop_words = {"là", "gì", "về", "với", "và", "của", "các", "theo", "cho", "để", "tại", "như", "được", "việc"}
        
        # Bóc tách từ khóa từ câu hỏi của người dùng
        cac_tu_cau_hoi = [w.strip(",.?\"'") for w in cau_hoi.lower().split() if w.strip()]
        tu_khoa_tim_kiem = set([w for w in cac_tu_cau_hoi if w not in stop_words and len(w) > 1])
        
        if not tu_khoa_tim_kiem:
            return None
            
        doan_tot_nhat = None
        diem_cao_nhat = 0.0
        
        for paragraph in paragraphs:
            doan_lower = paragraph.lower()
            # Đếm xem đoạn văn này chứa bao nhiêu từ khóa trong câu hỏi
            tu_trung_khop = sum(1 for tu in tu_khoa_tim_kiem if tu in doan_lower)
            
            # Tính toán mật độ trùng khớp (Score)
            score = tu_trung_khop / len(tu_khoa_tim_kiem)
            
            # Cập nhật đoạn văn bản có điểm số trùng khớp cao nhất
            if score > diem_cao_nhat:
                diem_cao_nhat = score
                doan_tot_nhat = paragraph
                
        # Nếu điểm số vượt qua ngưỡng thiết lập tối thiểu (threshold)
        if diem_cao_nhat >= threshold:
            return doan_tot_nhat
            
    except Exception as e:
        print(f"⚠️ Cảnh báo lỗi hệ thống khi đọc dữ liệu kb.txt: {e}")
        
    return None

def goi_duy_nhat_mot_llm(cau_hoi):
    try:
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

        elif PROVIDER == "OPENAI":
            client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": cau_hoi}]
            )
            return response.choices[0].message.content

        elif PROVIDER == "GEMINI":
            client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=cau_hoi
            )
            return response.text

        elif PROVIDER == "CLAUDE":
            client = Anthropic(api_key=os.getenv("CLAUDE_KEY"))
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": cau_hoi}]
            )
            return response.content[0].text
        else:
            return f"❌ Nền tảng '{PROVIDER}' không được cấu hình hợp lệ."
    except Exception as e:
        return f"❌ Lỗi kết nối đến nhà cung cấp đám mây {PROVIDER}: {e}"

def main():
    print(f"🏦 FUZZY ENTERPRISE KNOWLEDGE ROUTER - ACTIVE: {PROVIDER}")
    print("Hệ thống tự động phân tích từ khóa và quét văn bản thô nội bộ trước.")
    print("Gõ 'exit' hoặc 'thoat' để dừng chương trình.")
    print("-" * 60)
    
    while True:
        cau_hoi = input("\n👤 Bạn hỏi: ")
        
        if cau_hoi.strip().lower() in ['exit', 'thoat', 'quit']:
            print("👋 Đã đóng kết nối hệ thống AI Agent Level 2. Tạm biệt!")
            break
            
        if not cau_hoi.strip():
            continue
            
        print("⏳ [BƯỚC 1]: Đang phân tích từ khóa và quét thực địa văn bản thô (kb.txt)...")
        tri_thuc_noi_bo = tim_kiem_gan_dung_kb(cau_hoi)
        
        if tri_thuc_noi_bo:
            print(f"\n🤖 AI ANSWER:")
            print(tri_thuc_noi_bo)
            print(f"📍 NGUỒN TRÍCH XUẤT: Cơ sở tri thức thô Cục bộ (File kb.txt - Fuzzy Match)")
            print("-" * 60)
            continue
            
        print(f"⏳ [BƯỚC 2]: Từ khóa không khớp dữ liệu nội bộ. Định tuyến sang {PROVIDER} Cloud...")
        ket_qua_cloud = goi_duy_nhat_mot_llm(cau_hoi)
        
        print(f"\n🤖 AI ANSWER ({PROVIDER}):")
        print(ket_qua_cloud)
        print(f"📍 NGUỒN TRÍCH XUẤT: Mô hình LLM Đám mây trên Internet ({PROVIDER} Cloud Global Service)")
        print("-" * 60)

if __name__ == "__main__":
    main()