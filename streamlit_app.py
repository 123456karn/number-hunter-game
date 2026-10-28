import streamlit as st
from random import randint

# 1. ตั้งค่าไอคอนและชื่อแท็บหน้าเว็บเกม
st.set_page_config(page_title="Number Hunter: Boss Battle", page_icon="🎮", layout="centered")

# ตกแต่งสไตล์ CSS เพื่อให้ปุ่มและตัวอักษรดูเหมือนหน้าจอเกมคอนโซล
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-size: 16px !important;
        font-weight: bold;
    }
    .game-title {
        text-align: center;
        font-size: 34px;
        font-weight: bold;
        color: #FF4B4B;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. จัดการเก็บสถานะตัวแปรของเกม (Session State) ไม่ให้รีเซ็ตเมื่อกดปุ่ม
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.player_hp = 100
    st.session_state.boss_hp = 100
    st.session_state.number = 0
    st.session_state.max_number = 100
    st.session_state.mode_name = ""
    st.session_state.log = []

# แสดงหัวข้อเกมด้านบนสุด
st.markdown('<div class="game-title">🏹 NUMBER HUNTER 👾</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>BOSS BATTLE EDITION</p>", unsafe_allow_html=True)
st.markdown("---")

# =========================================================
# ฉากที่ 1: หน้าเมนูหลัก (เลือกความยากก่อนเริ่มสู้)
# =========================================================
if not st.session_state.game_started:
    st.subheader("🔮 เลือกด่านความยากที่คุณต้องการท้าทาย:")
    
    choice = st.radio(
        "ระดับความยากของบอส:",
        ("1️⃣ ง่าย   (Easy)   - สุ่มตัวเลขลับระหว่าง 1-30", 
         "2️⃣ ปกติ   (Normal) - สุ่มตัวเลขลับระหว่าง 1-100", 
         "3️⃣ ยาก   (Hard)   - สุ่มตัวเลขลับระหว่าง 1-200"),
        label_visibility="collapsed"
    )
    
    st.markdown("###")
    if st.button("⚔️ เข้าสู่สนามรบ!", type="primary"):
        if "ง่าย" in choice:
            st.session_state.max_number = 30
            st.session_state.mode_name = "ง่าย (Easy) 🟢"
        elif "ปกติ" in choice:
            st.session_state.max_number = 100
            st.session_state.mode_name = "ปกติ (Normal) 🟡"
        else:
            st.session_state.max_number = 200
            st.session_state.mode_name = "ยาก (Hard) 🔴"
            
        # สุ่มตัวเลขลับของบอสและรีเซ็ตค่าเริ่มต้น
        st.session_state.number = randint(1, st.session_state.max_number)
        st.session_state.player_hp = 100
        st.session_state.boss_hp = 100
        st.session_state.game_started = True
        st.session_state.log = [f"🎮 เริ่มเกมในโหมด: {st.session_state.mode_name}", f"🔮 บอสซ่อนตัวเลขปริศนาไว้ระหว่าง 1-{st.session_state.max_number}!"]
        st.rerun()

# =========================================================
# ฉากที่ 2: หน้าต่างแสดงผลเกม (กำลังต่อสู้)
# =========================================================
else:
    # 📊 ส่วนที่ 1: หลอดเลือด HP แสดงผลแบบกราฟิกอนิเมชัน
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### ❤️ PLAYER HP\n**{st.session_state.player_hp} / 100**")
            st.progress(st.session_state.player_hp / 100)
        with col2:
            st.markdown(f"### 😈 BOSS HP\n**{st.session_state.boss_hp} / 100**")
            st.progress(st.session_state.boss_hp / 100)
            
    st.markdown(f"<p style='text-align: center; color: #888;'>🎮 โหมดเกม: {st.session_state.mode_name} | ขอบเขตตัวเลข: 1-{st.session_state.max_number}</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🛑 ตรวจสอบเงื่อนไขหลังจบวงลูป (แพ้ / ชนะ)
    if st.session_state.player_hp <= 0 or st.session_state.boss_hp <= 0:
        with st.container(border=True):
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🏆 VICTORY! 🏆</h2>", unsafe_allow_html=True)
                st.success("คุณสามารถกำจัดบอสและปกป้องอาณาจักรได้สำเร็จ! 🎉")
            else:
                st.markdown("<h2 style='text-align: center; color: #F44336;'>💀 GAME OVER 💀</h2>", unsafe_allow_html=True)
                st.error("คุณพ่ายแพ้ให้กับความมืดมิดของบอส!")
                
            st.info(f"🔓 เฉลยเลขลับของบอสในรอบนี้คือ: {st.session_state.number}")
            st.markdown("###")
            
            if st.button("🔄 กลับไปหน้าเมนูหลักเพื่อเล่นใหม่", type="primary"):
                st.session_state.game_started = False
                st.rerun()
                
    # ⚔️ เกมยังดำเนินอยู่: แสดงการกรอกและปุ่มโจมตีตามกติกาดั้งเดิมของคุณ
    else:
        # ใช้เลย์เอาต์แบ่งคอลัมน์ซ้ายขวา (กรอกตัวเลขและกดปุ่มโจมตี)
        col_input, col_btn = st.columns([2, 1], vertical_alignment="bottom")
        
        with col_input:
            guess = st.number_input(
                f"🎯 ทายตัวเลข (1-{st.session_state.max_number}):", 
                min_value=1, 
                max_value=st.session_state.max_number, 
                step=1,
                key="player_guess"
            )
            
        with col_btn:
            attack_clicked = st.button("⚔️ โจมตี!", type="primary")

        if attack_clicked:
            # คำนวณระยะห่างระหว่างเลขที่ทายกับเลขลับของบอส
            distance = abs(guess - st.session_state.number)
            
            if distance == 0:
                st.session_state.log.insert(0, f"💥 PERFECT! ทายเลข {guess} ถูกต้องตรงเป๊ะ! คุณปลดปล่อยมหาเวท! บอสได้รับความเสียหาย 40 HP!")
                st.session_state.boss_hp -= 40
            elif distance <= 2:
                st.session_state.log.insert(0, f"🔥 CRITICAL ATTACK! ทายเลข {guess} ใกล้เคียงมาก! ดาบแห่งแสงทำงาน! บอสได้รับความเสียหาย 25 HP!")
                st.session_state.boss_hp -= 25
            elif distance <= 5:
                st.session_state.log.insert(0, f"⚔️ NORMAL ATTACK! ทายเลข {guess} โจมตีโดนบอส! ลูกธนูปักเข้าเป้า! บอสได้รับความเสียหาย 10 HP!")
                st.session_state.boss_hp -= 10
            else:
                hint = "สูงเกินไป 📈" if guess > st.session_state.number else "ต่ำเกินไป 📉"
                st.session_state.log.insert(0, f"❌ MISS! ทายเลข {guess} ผิดห่างไกลเป้าหมายเกินไป! บอสใช้สกิลสวนกลับชาร์จเข้าใส่คุณ! คุณเสีย 20 HP! (คำใบ้จากระบบ: ตัวเลขที่คุณทาย '{hint}')")
                st.session_state.player_hp -= 20
                
            # ป้องกัน HP ติดลบ
            if st.session_state.player_hp < 0: st.session_state.player_hp = 0
            if st.session_state.boss_hp < 0: st.session_state.boss_hp = 0
            
            st.rerun()
            
        # ปุ่มยอมแพ้
        st.markdown("###")
        if st.button("🏳️ ยอมแพ้และกลับหน้าหลัก", type="secondary"):
            st.session_state.game_started = False
            st.rerun()
            
    # 📜 ส่วนที่ 3: แสดงประวัติบันทึกการต่อสู้ (Battle Log) พร้อมแยกไฮไลต์สี
    if st.session_state.log:
        st.markdown("###")
        with st.expander("📜 บันทึกการต่อสู้ (Battle Log)", expanded=True):
            for entry in st.session_state.log:
                if "❌" in entry:
                    st.markdown(f"<span style='color:#FF6B6B;'>{entry}</span>", unsafe_allow_html=True)
                elif "💥" in entry or "🔥" in entry:
                    st.markdown(f"<span style='color:#4DFF4D; font-weight:bold;'>{entry}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span>{entry}</span>", unsafe_allow_html=True)
