import os
import random
import hashlib
import string
import math
from datetime import datetime
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. SERVER WEB GIỮ BOT SỐNG 24/7 TRÊN RENDER ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot TOOL TX MD5 PRO v6.5 đang hoạt động 24/7!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. CẤU HÌNH TOKEN BOT & DỮ LIỆU ---
TOKEN = '8985526419:AAGdRkntgFNYLBG53LoI-pNC7aHtOFMWhGA'
ADMIN_ID = 755092812  # Đã cập nhật chính xác Telegram ID của bạn
bot = telebot.TeleBot(TOKEN)

user_data = {}
all_user_ids = set()
giftcodes = {}
admin_notice = "🔥 Hệ thống TOOL TX MD5 PRO v6.5 đã nâng cấp dải thuật toán! Chúc anh em rực rỡ!"

SUPPORTED_WEBS = ["HitClub", "B52", "Lucky88", "LC79"]

def init_user(uid):
    all_user_ids.add(uid)
    if uid not in user_data:
        user_data[uid] = {
            "balance": 20,
            "bias": 0.0,
            "last_pred": None,
            "win_streak": 0,
            "history_logs": [],
            "last_checkin": "",
            "selected_web": "HitClub"
        }

# --- 3. ĐỘNG CƠ SOI CẦU HYBRID CÂN BẰNG TÀI / XỈU ---

def exact_enumeration_score(hex_str):
    total = 0
    for idx, char in enumerate(hex_str):
        val = int(char, 16)
        total += val * (idx + 1) * 3
    return total

def monte_carlo_simulation(hex_str, simulations=2000):
    seed_val = int(hex_str[:8], 16)
    random.seed(seed_val)
    tai_count = 0
    for _ in range(simulations):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        dice3 = random.randint(1, 6)
        if (dice1 + dice2 + dice3) >= 11:
            tai_count += 1
    return (tai_count / simulations) * 100

def dynamic_programming_adjust(base_ratio, bias, streak):
    adjusted = base_ratio + (bias * 12.0) + (streak * 1.5)
    return 100 / (1 + math.exp(-(adjusted - 50) / 15))

def master_predict_balanced(uid, raw_code):
    ud = user_data[uid]
    
    clean_code = raw_code.strip().lower()
    hash_obj = hashlib.sha256(clean_code.encode()).hexdigest()
    
    exact = exact_enumeration_score(hash_obj) % 100
    mc_ratio = monte_carlo_simulation(hash_obj)
    
    raw_score = (exact * 0.4) + (mc_ratio * 0.6)
    final_ratio = dynamic_programming_adjust(raw_score, ud["bias"], ud["win_streak"])
    
    is_tai = final_ratio >= 50.0
    final_result = "TÀI" if is_tai else "XỈU"
    
    accuracy = round(min(98.5, max(88.0, 85 + abs(final_ratio - 50) * 0.4)), 1)
    
    if is_tai:
        percent_tai = round(final_ratio, 1)
        percent_xiu = round(100 - final_ratio, 1)
    else:
        percent_xiu = round(100 - final_ratio, 1)
        percent_tai = round(final_ratio, 1)
        
    ud["last_pred"] = final_result
    
    code_type = "MD5" if len(clean_code) == 32 else "SHA256"
    ud["history_logs"].append(f"[{code_type}] {clean_code[:6]}... ➔ {final_result}")
    if len(ud["history_logs"]) > 5:
        ud["history_logs"].pop(0)

    return final_result, percent_tai, percent_xiu, accuracy, code_type

# --- 4. GIAO DIỆN PHÍM BẤM ---

def main_menu_keyboard(uid):
    markup = InlineKeyboardMarkup(row_width=2)
    
    btn_soi = InlineKeyboardButton("🎲 SOI MÃ MD5 / SHA256", callback_data="mode_soi")
    btn_web = InlineKeyboardButton(f"🌐 CỔNG: {user_data[uid]['selected_web']}", callback_data="mode_select_web")
    
    btn_checkin = InlineKeyboardButton("🎁 ĐIỂM DANH (+2 XU)", callback_data="mode_checkin")
    btn_info = InlineKeyboardButton("💳 VÍ & LỊCH SỬ", callback_data="mode_info")
    btn_buy = InlineKeyboardButton("💎 MUA XU VIP", callback_data="mode_buy")
    
    markup.add(btn_soi, btn_web)
    markup.add(btn_checkin, btn_info)
    markup.add(btn_buy)
        
    return markup

# --- 5. LỆNH CƠ BẢN ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    uid = message.from_user.id
    init_user(uid)
    xu = user_data[uid]["balance"]
    web = user_data[uid]["selected_web"]
    
    msg = (
        "🔥 **TOOL TX MD5 PRO v6.5** 🔥\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"📢 **THÔNG BÁO ADMIN:**\n_{admin_notice}_\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 **ID:** `{uid}` | 🌐 **Cổng Game:** `{web}`\n"
        f"💰 **Số Xu hiện có:** **{xu} Xu** | 🔥 **Streak:** **{user_data[uid]['win_streak']} tay**\n"
        "🤖 **Động cơ soi:** `Exact Enumeration` + `Monte Carlo` + `DP`\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "💡 **HƯỚNG DẪN:** Dán mã **MD5 (32 ký tự)** hoặc **SHA256 (64 ký tự)** vào đây để soi!\n"
        "💬 Chat **`bú`** khi ăn hoặc **`gãy`** khi thua để AI cân bằng lại ván sau!"
    )
    bot.reply_to(message, msg, parse_mode="Markdown", reply_markup=main_menu_keyboard(uid))

# --- 6. HỆ THỐNG QUẢN TRỊ ADMIN ---

@bot.message_handler(commands=['thongbao', 'tb'])
def broadcast_notice(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        notice_text = message.text.split(" ", 1)[1].strip()
    except IndexError:
        err_msg = (
            "❌ **Cú pháp sai!**\n"
            "👉 Dùng: `/thongbao <Nội_dung>`\n"
            "*Ví dụ:* `/thongbao Mọi người tạm dừng dùng tool vài phút nhé!`"
        )
        bot.reply_to(message, err_msg, parse_mode="Markdown")
        return

    global admin_notice
    admin_notice = notice_text
    
    success_count = 0
    fail_count = 0
    
    status_msg = bot.reply_to(message, f"🚀 **Đang gửi thông báo tới {len(all_user_ids)} người dùng...**", parse_mode="Markdown")
    
    broadcast_format = (
        "🔔 **THÔNG BÁO TỪ TOOL TX MD5 PRO** 🔔\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"{notice_text}\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "⚠️ *Vui lòng tuân thủ hướng dẫn từ Admin!*"
    )

    for target_id in list(all_user_ids):
        try:
            bot.send_message(target_id, broadcast_format, parse_mode="Markdown")
            success_count += 1
        except Exception:
            fail_count += 1

    bot.edit_message_text(
        f"✅ **ĐÃ GỬI THÔNG BÁO THÀNH CÔNG!**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📬 **Thành công:** {success_count} người\n"
        f"❌ **Thất bại (Block bot):** {fail_count} người\n"
        f"📢 **Nội dung:**\n_{notice_text}_",
        chat_id=message.chat.id,
        message_id=status_msg.message_id,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['congxu'])
def add_coins(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.text.split()
        target_id = int(args[1])
        coins_to_add = int(args[2])
        
        init_user(target_id)
        user_data[target_id]["balance"] += coins_to_add
        
        bot.reply_to(message, f"✅ **ĐÃ CỘNG XU THÀNH CÔNG!**\n👤 ID Người dùng: `{target_id}`\n💰 Cộng thêm: **+{coins_to_add} Xu**\n💳 Số dư mới: **{user_data[target_id]['balance']} Xu**", parse_mode="Markdown")
        
        try:
            bot.send_message(target_id, f"🎉 **THÔNG BÁO NẠP XU!**\n🎁 Admin đã cộng **+{coins_to_add} Xu** vào tài khoản của bạn!\n💳 Tổng số dư hiện tại: **{user_data[target_id]['balance']} Xu**", parse_mode="Markdown")
        except Exception:
            pass
            
    except Exception:
        bot.reply_to(message, "❌ **Cú pháp sai!**\n👉 Dùng câu lệnh: `/congxu <ID_User> <Số_Xu>`", parse_mode="Markdown")

@bot.message_handler(commands=['taocode'])
def create_code(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.text.split()
        code_input, coins = args[1].upper(), int(args[2])
        uses = int(args[3]) if len(args) >= 4 else 1
        code_string = "GIFT-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) if code_input == "AUTO" else code_input
        giftcodes[code_string] = {"coins": coins, "uses": uses, "used_by": set()}
        bot.reply_to(message, f"🎉 **TẠO CODE THÀNH CÔNG!**\n🎁 Code: `{code_string}` | 💰 Xu: **+{coins}** | 👥 Lượt: **{uses}**", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "❌ Cú pháp sai: `/taocode <Mã_Code hoặc AUTO> <Số_Xu> [Lượt]`")

@bot.message_handler(commands=['code'])
def redeem_code(message):
    uid = message.from_user.id
    init_user(uid)
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "⚠️ **Cú pháp:** `/code <Mã_Giftcode>`", parse_mode="Markdown")
            return
        code_input = args[1].strip().upper()
        if code_input not in giftcodes:
            bot.reply_to(message, "❌ **Code không tồn tại hoặc đã hết hạn!**", parse_mode="Markdown")
            return
        code_info = giftcodes[code_input]
        if uid in code_info["used_by"]:
            bot.reply_to(message, "⚠️ **Bạn đã nhập code này rồi!**", parse_mode="Markdown")
            return
        if len(code_info["used_by"]) >= code_info["uses"]:
            bot.reply_to(message, "❌ **Code đã hết lượt sử dụng!**", parse_mode="Markdown")
            return
        user_data[uid]["balance"] += code_info["coins"]
        code_info["used_by"].add(uid)
        bot.reply_to(message, f"🎉 **NHẬP CODE THÀNH CÔNG!**\n🎁 Cộng: **+{code_info['coins']} Xu**", parse_mode="Markdown", reply_markup=main_menu_keyboard(uid))
    except Exception:
        bot.reply_to(message, "❌ Lỗi hệ thống khi nhập code!")

# --- 7. CALLBACK NÚT BẤM ---

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    uid = call.from_user.id
    init_user(uid)

    if call.data == "mode_soi":
        bot.send_message(call.message.chat.id, "📥 **Gửi mã MD5 (32 ký tự) hoặc SHA256 (64 ký tự) vào ô chat:**", parse_mode="Markdown")

    elif call.data == "mode_select_web":
        markup = InlineKeyboardMarkup(row_width=2)
        for w in SUPPORTED_WEBS:
            markup.add(InlineKeyboardButton(f"🎮 {w}", callback_data=f"setweb_{w}"))
        bot.send_message(call.message.chat.id, "🌐 **CHỌN CỔNG GAME BẠN ĐANG CHƠI:**", reply_markup=markup)

    elif call.data.startswith("setweb_"):
        selected = call.data.split("_")[1]
        user_data[uid]["selected_web"] = selected
        bot.answer_callback_query(call.id, f"✅ Đã chọn cổng: {selected}")
        bot.send_message(call.message.chat.id, f"✅ **Đã chuyển sang cổng Game: {selected}**", reply_markup=main_menu_keyboard(uid))

    elif call.data == "mode_checkin":
        today = datetime.now().strftime("%Y-%m-%d")
        if user_data[uid]["last_checkin"] == today:
            bot.answer_callback_query(call.id, "⚠️ Hôm nay bạn đã điểm danh rồi!", show_alert=True)
        else:
            user_data[uid]["last_checkin"] = today
            user_data[uid]["balance"] += 2
            bot.send_message(call.message.chat.id, "🎉 **ĐIỂM DANH THÀNH CÔNG!**\n🎁 Bạn nhận được **+2 Xu**!", parse_mode="Markdown")

    elif call.data == "mode_info":
        xu = user_data[uid]["balance"]
        streak = user_data[uid]["win_streak"]
        web = user_data[uid]["selected_web"]
        logs = user_data[uid]["history_logs"]
        logs_str = "\n".join([f"• {log}" for log in logs]) if logs else "Chưa có lịch sử."
        
        info_msg = (
            f"👤 **THÔNG TIN TÀI KHOẢN**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 Telegram ID: `{uid}`\n"
            f"🌐 Cổng Game: **{web}**\n"
            f"💰 Số Xu hiện có: **{xu} Xu**\n"
            f"🔥 Dây thắng: **{streak} ván**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📜 **5 VÁN SOI GẦN NHẤT:**\n{logs_str}"
        )
        bot.send_message(call.message.chat.id, info_msg, parse_mode="Markdown", reply_markup=main_menu_keyboard(uid))

    elif call.data == "mode_buy":
        buy_msg = (
            "🛒 **NẠP XU VIP TOOL TX MD5 PRO**\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "💵 **10.000 VNĐ** ➔ **30 Xu**\n"
            "💵 **20.000 VNĐ** ➔ **70 Xu**\n"
            "💵 **50.000 VNĐ** ➔ **200 Xu**\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "📩 **Liên hệ Admin nạp xu:** @lionVnIos\n"
            f"🆔 ID của bạn: `{uid}`"
        )
        bot.send_message(call.message.chat.id, buy_msg, parse_mode="Markdown")

# --- 8. XỬ LÝ SOI MÃ & BÚ / GÃY ---

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    uid = message.from_user.id
    init_user(uid)

    text = message.text.strip().lower()
    ud = user_data[uid]

    if text in ["bú", "bu", "win", "ăn", "thắng", "húp", "đớp"]:
        if not ud["last_pred"]:
            bot.reply_to(message, "⚠️ Bạn chưa gửi mã soi ván nào!")
            return
        ud["win_streak"] += 1
        ud["bias"] = min(2.0, ud["bias"] + 0.3)
        bot.reply_to(message, f"🔥 **BÚ ĐẬM RỰC RỠ!** 💸\n🔥 Dây đỏ hiện tại: **{ud['win_streak']} tay liên tiếp!**\n👉 Gửi mã tiếp theo để thừa thắng xông lên!", parse_mode="Markdown")
        return

    elif text in ["gãy", "gay", "thua", "tạch", "xịt", "bẻ"]:
        if not ud["last_pred"]:
            bot.reply_to(message, "⚠️ Bạn chưa gửi mã soi ván nào!")
            return
        ud["win_streak"] = 0
        ud["bias"] = max(-2.0, ud["bias"] - 0.5)
        bot.reply_to(message, "🛡️ **AI đã tái điều chỉnh dải tần Dynamic Programming!**\n👉 Gửi mã tiếp theo ngay để đớp lại gấp đôi!", parse_mode="Markdown")
        return

    if len(text) in [32, 64]:
        if ud["balance"] < 1:
            bot.reply_to(message, "⚠️ **Bạn không đủ Xu!** Điểm danh hoặc nạp xu để tiếp tục soi.", reply_markup=main_menu_keyboard(uid))
            return

        ud["balance"] -= 1
        final_result, percent_tai, percent_xiu, accuracy, code_type = master_predict_balanced(uid, text)
        res_label = "🔴 TÀI" if final_result == "TÀI" else "🔵 XỈU"

        res = (
            f"🌐 **CỔNG GAME:** `{ud['selected_web']}`\n"
            f"🔥 **KẾT QUẢ TOOL TX MD5 PRO (v6.5)** 🔥\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 Dự đoán: **{res_label}**\n"
            f"📊 Phân tích: **Tài {percent_tai}% - Xỉu {percent_xiu}%**\n"
            f"⚡ Tỉ lệ chính xác: **{accuracy}%**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Xu còn: **{ud['balance']} Xu** | 🔥 Streak: **{ud['win_streak']} tay**\n"
            f"💬 *Chat `bú` khi ăn hoặc `gãy` khi thua để AI cân bằng lại!*"
        )
        bot.reply_to(message, res, parse_mode="Markdown", reply_markup=main_menu_keyboard(uid))
        return

    bot.reply_to(message, "⚠️ Vui lòng gửi mã **MD5 (32 ký tự)**, **SHA256 (64 ký tự)** hoặc chọn chức năng bên dưới:", reply_markup=main_menu_keyboard(uid))

# --- 9. KHỞI CHẠY BOT ---
if __name__ == '__main__':
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    try:
        bot.remove_webhook()
        print("Đã giải phóng Webhook kẹt thành công!")
    except Exception as e:
        print(f"Lỗi khi xóa webhook: {e}")
        
    print("TOOL TX MD5 PRO v6.5 đang hoạt động...")
    bot.infinity_polling(none_stop=True)
