import telebot

TOKEN = '7975718778:AAEIyvExGWAPyLFFBl4FBs55Y46WEbQQ1Hg'
bot = telebot.TeleBot(TOKEN)

oyuncular = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    oyuncular[user_id] = {'puan': 0, 'envanter': []}
    bot.send_message(message.chat.id, "🧙‍♂️ Akademiye hoş geldin! Karakter adını yaz:")
    bot.register_next_step_handler(message, karakter_adi_al)

def karakter_adi_al(message):
    user_id = message.from_user.id
    oyuncular[user_id]['isim'] = message.text
    bot.send_message(message.chat.id, "🔮 Mesleğini seç:\n1. Büyücü\n2. Savaşçı\n3. Hırsız")
    bot.register_next_step_handler(message, meslek_sec)

def meslek_sec(message):
    user_id = message.from_user.id
    secimler = {'1': 'Büyücü', '2': 'Savaşçı', '3': 'Hırsız'}
    meslek = secimler.get(message.text.strip(), 'Büyücü')
    oyuncular[user_id]['meslek'] = meslek

    bot.send_message(message.chat.id,
        f"🎭 Karakterin hazır: {oyuncular[user_id]['isim']} ({meslek})\n"
        "🌑 Gecenin bir vakti tuhaf bir ses duyuyorsun.\n"
        "Ne yaparsın?\nA) Kapıyı aç\nB) Saklan\nC) Büyü hazırla"
    )
    bot.register_next_step_handler(message, sahne_1)

def sahne_1(message):
    user_id = message.from_user.id
    secim = message.text.lower()

    sahneler = {
        'a': "🚪 Kapıyı açtın... ayak sesleri yaklaşıyor!",
        'b': "🕳️ Kitaplığa saklandın, nefesini tuttun...",
        'c': "✨ Koruma büyüsü hazırladın, ışıklar parladı."
    }

    if secim not in sahneler:
        bot.send_message(message.chat.id, "❓ Lütfen A, B ya da C seç.")
        return bot.register_next_step_handler(message, sahne_1)

    bot.send_message(message.chat.id, sahneler[secim])
    bot.send_message(message.chat.id,
        "🔍 Labirente geldin. Hangi yolu seçeceksin?\n"
        "A) Sol\nB) Sağ\nC) Ortadaki yol"
    )
    bot.register_next_step_handler(message, labirent)

def labirent(message):
    user_id = message.from_user.id
    secim = message.text.lower()

    if secim == 'a':
        bot.send_message(message.chat.id, "🚫 Sol yol çıkmaz sokak. Geri dönmelisin.")
    elif secim == 'b':
        oyuncular[user_id]['puan'] += 10
        bot.send_message(message.chat.id, f"✅ Gizli geçidi buldun! +10 puan. Toplam puan: {oyuncular[user_id]['puan']}")
    elif secim == 'c':
        bot.send_message(message.chat.id, "💥 Tuzak! Yaralandın ama hayattasın...")
    else:
        bot.send_message(message.chat.id, "❓ A, B ya da C?")
        return bot.register_next_step_handler(message, labirent)

    bot.send_message(message.chat.id,
        "🪞 Bir aynalar odasına geldin. Sadece bir ayna yansımanı göstermiyor.\n"
        "Ne yaparsın?\nA) Aynaya dokun\nB) Aynaları kır\nC) Bekle"
    )
    bot.register_next_step_handler(message, aynalar_odasi)

def aynalar_odasi(message):
    user_id = message.from_user.id
    secim = message.text.lower()
    puan = oyuncular[user_id]['puan']
    envanter = oyuncular[user_id]['envanter']

    sahne = ""

    if secim == 'a':
        puan += 20
        envanter.append("Boyut Anahtarı")
        sahne = f"🌌 Başka boyuta geçtin! +20 puan.\nToplam puan: {puan}"
    elif secim == 'b':
        puan += 10
        sahne = "🪞 Aynaları kırdın, karanlık versiyonun belirdi! Savaş başlasın. +10 puan."
    elif secim == 'c':
        sahne = "⏳ Bekledin ve bir ses duyuldu: 'Kaderin seni çağırıyor...'"
    else:
        bot.send_message(message.chat.id, "❓ Lütfen A, B ya da C seç.")
        return bot.register_next_step_handler(message, aynalar_odasi)

    oyuncular[user_id]['puan'] = puan
    oyuncular[user_id]['envanter'] = envanter

    bot.send_message(message.chat.id, sahne)
    bot.send_message(message.chat.id,
        "🎮 Oyun bitti!\n"
        f"Puan: {puan}\n"
        f"Envanter: {', '.join(envanter) or 'Boş'}\n"
        "Yeniden başlamak için /start yazabilirsin."
    )

@bot.message_handler(commands=['envanter'])
def envanter_goster(message):
    user_id = message.from_user.id
    envanter = oyuncular.get(user_id, {}).get('envanter', [])
    bot.send_message(message.chat.id,
        f"📦 Envanter: {', '.join(envanter) if envanter else 'Boş'}"
    )

    bot.send_message(message.chat.id, "📖 Hikayenin devamını görmek ister misin? (Evet / Hayır)")
    bot.register_next_step_handler(message, devam_istegi)
def devam_istegi(message):
    user_id = message.from_user.id
    cevap = message.text.lower()

    if "evet" in cevap:
        karakter = oyuncular[user_id]
        isim = karakter.get('isim', 'Bilinmeyen')
        meslek = karakter.get('meslek', 'Maceracı')
        puan = karakter.get('puan', 0)
        envanter = ', '.join(karakter.get('envanter', [])) or 'boş'

        sahne_ozeti = (
            f"🧙 Karakter: {isim} ({meslek})\n"
            f"🎯 Puan: {puan}\n"
            f"🎒 Envanter: {envanter}\n\n"
            "🔮 Hikaye burada bitmedi... Gölgeler arasında bir figür yaklaşıyor.\n"
            "💬 Devamını görmek için bir şeyler yaz ya da bekle..."
        )

        bot.send_message(message.chat.id, sahne_ozeti)

        devam_sahnesi = (
            "🌫️ Sislerin içinden bir silüet belirdi. 'Seninle işim henüz bitmedi,' dedi.\n"
            "Bir sonraki karar anı geliyor...\n"
            "Ne yapacaksın?\n"
            "A) Savaş\nB) Kaç\nC) Konuş"
        )
        bot.send_message(message.chat.id, devam_sahnesi)

    else:
        bot.send_message(message.chat.id, "🎮 Oyun burada sona erdi. Yeniden başlamak için /start yazabilirsin.")
def devam_sahne_cevap(message):
    user_id = message.from_user.id
    secim = message.text.lower()
    
    if secim == 'a':
        bot.send_message(message.chat.id, "⚔️ Cesurca savaşa girdin. Güçlü bir büyü kullandın!")
        oyuncular[user_id]['puan'] += 15
    elif secim == 'b':
        bot.send_message(message.chat.id, "🏃‍♂️ Koşmaya başladın ama karanlık seni takip ediyor...")
    elif secim == 'c':
        bot.send_message(message.chat.id, "🗣️ 'Neden buradasın?' diye sordun. Figür yavaşça yaklaşıyor...")
    else:
        bot.send_message(message.chat.id, "❓ A, B ya da C'den birini seçmelisin.")
        return bot.register_next_step_handler(message, devam_sahne_cevap)
    
    bot.send_message(message.chat.id, "✨ Macera burada şimdilik sona erdi. Devamı yakında...\n/start yazarak tekrar başlayabilirsin.")


bot.polling(none_stop=True)
