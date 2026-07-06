import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
PROVIDER = os.getenv("ACTIVE_PROVIDER", "GEMINI").upper()
KB_FILE = "kb2.txt"

def tim_kiem_tri_thuc_scale(cau_hoi):
    if not os.path.exists(KB_FILE):
        return None
        
    try:
        with open(KB_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        cau_hoi_clean = cau_hoi.strip().lower()
        
        for line in lines:
            if not line.strip() or "|" not in line:
                continue
                
            # Bóc tách 5 thành phần chuẩn doanh nghiệp dựa trên ký tự |
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 5:
                continue
                
            tu_khoa_he_thong = parts[0].lower().split(", ")
            noi_dung_chuan = parts[1]
            template_phan_hoi = parts[2]
            muc_do_review = parts[3]
            escalation_rule = parts[4]
            
            # Kiểm tra xem câu hỏi người dùng có chứa từ khóa nào không (Fuzzy Match)
            for tu in tu_khoa_he_thong:
                if tu in cau_hoi_clean:
                    # Trả về một dictionary chứa đầy đủ metadata quản trị
                    return {
                        "noi_dung_chuan": noi_dung_chuan,
                        "template_phan_hoi": template_phan_hoi,
                        "muc_do_review": muc_do_review,
                        "escalation_rule": escalation_rule
                    }
    except Exception as e:
        print(f"⚠️ Lỗi cấu trúc KB: {e}")
    return None

def main():
    print(f"🏦 ENTERPRISE ROUTER LEVEL 2 - CONNECTED: {PROVIDER}")
    print("Hệ thống tự động điều phối dữ liệu và kiểm soát giọng điệu phản hồi.")
    print("-" * 60)
    
    while True:
        cau_hoi = input("\n👤 Bạn hỏi: ")
        if cau_hoi.strip().lower() in ['exit', 'thoat']:
            break
            
        print("⏳ [BƯỚC 1]: Quét file cấu trúc tri thức KB...")
        data_match = tim_kiem_tri_thuc_scale(cau_hoi)
        
        if data_match:
            print(f"\n🤖 AI ANSWER (Template phản hồi chuẩn):")
            print(data_match["template_phan_hoi"])
            print(f"\n📑 [METADATA QUẢN TRỊ]")
            print(f"├─ Nguồn gốc pháp lý: {data_match['noi_dung_chuan']}")
            print(f"├─ Cấp độ phê duyệt nội dung: {data_match['muc_do_review']}")
            print(f"└─ Quy tắc chuyển cấp & Giọng điệu: {data_match['escalation_rule']}")
            print("-" * 60)
        else:
            print(f"⏳ [BƯỚC 2]: Không khớp từ khóa an toàn. Kích hoạt Escalation Rule -> Định tuyến tới {PROVIDER} Cloud...")
            # Đoạn này gọi client = genai.Client() và push lên internet như các bài trước
            print(f"\n🤖 AI ANSWER ({PROVIDER}): (Nội dung tự động tổng hợp từ mô hình đám mây)")
            print("-" * 60)

if __name__ == "__main__":
    main()