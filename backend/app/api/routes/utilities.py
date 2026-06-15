from fastapi import APIRouter

router = APIRouter()

# Mock Data
EXCHANGE_RATES = {
    "base": "LAK",
    "rates": {
        "THB": 0.0015,  # 1 LAK ≈ 0.0015 THB (หรือ 1 THB ≈ 650 LAK)
        "USD": 0.000045  # 1 LAK ≈ 0.000045 USD
    },
    "last_updated": "2024-04-27"
}

PHRASES = [
    {"id": 1, "thai_text": "สวัสดี", "lao_text": "สะบายดี",
        "pronunciation": "Sabaidee"},
    {"id": 2, "thai_text": "ขอบคุณ", "lao_text": "ขอบใจ",
        "pronunciation": "Khop Chai"},
    {"id": 3, "thai_text": "ราคาเท่าไหร่?",
        "lao_text": "ราคาเท่าได?", "pronunciation": "Raka Tao Dai?"},
    {"id": 4, "thai_text": "ไม่เผ็ด",
        "lao_text": "บ่เผ็ด", "pronunciation": "Bor Phet"},
    {"id": 5, "thai_text": "ห้องน้ำอยู่ไหน?",
        "lao_text": "ห้องน้ำอยูใส?", "pronunciation": "Hong Nam You Sai?"}
]

TRANSPORTS = [
    {"id": 1, "type": "รถสกายแล็บ (Tuk-Tuk)", "price": "20,000 - 50,000 LAK",
     "contact": "เรียกได้ตามจุดท่องเที่ยว"},
    {"id": 2, "type": "เช่ารถมอเตอร์ไซค์",
        "price": "150,000 LAK/วัน", "contact": "ร้านเช่าใกล้ริมโขง"},
    {"id": 3, "type": "รถเมล์ประจำทาง", "price": "10,000 LAK",
        "contact": "สถานีขนส่งสะหวันนะเขต"}
]


@router.get("/exchange-rates")
async def get_exchange_rates():
    return EXCHANGE_RATES


@router.get("/phrases")
async def get_phrases():
    return PHRASES


@router.get("/transports")
async def get_transports():
    return TRANSPORTS
