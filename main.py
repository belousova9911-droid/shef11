import os
import time
import random
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
import vk_api

# ================= НАСТРОЙКИ =================
TOKEN = os.getenv("VK_TOKEN", "vk1.a.4OnPAtK9wtYFprDqBNfAgN5Ibz-8F3zAjcvZOZ-5w2DM3ADmBEWZ_TZMqWqtSIxepkWXDIWkBFtv_dYRN_jz3yBklZDYTGhSjaJevFCRG5nUQwgDbidv0HWXnoTfILBYBdrhFks6XYxOXNJTd2tckihcTfg7wFDPC82ahq85GGNU3ZyTpFw6RP5X_-5v5lkJdxc4rvAPepdRLB4NVHezKg")
GROUP_ID = int(os.getenv("GROUP_ID", 241055687))

# Три рабочих чата
PEER_IDS = [2000000001]

# Часовой пояс Перми
TIMEZONE = ZoneInfo("Asia/Yekaterinburg")

# ================= РАСПИСАНИЕ =================

SCHEDULE = {
    "11:00": "Доброе утро! Отправляем фотоотчет по рису + обработку овощей в солевом растворе @all",
    "14:00": "Отправляем фотоотчет по рису @all",
    "17:00": "Отправляем фотоотчет по рису @all"
}

# ================= ЛОГИРОВАНИЕ =================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

# ================= ИНИЦИАЛИЗАЦИЯ =================

if not TOKEN:
    raise RuntimeError("Не задан VK_TOKEN")

try:
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()

    vk.groups.getById(group_id=GROUP_ID)

    logger.info("Токен проверен. Бот готов к работе.")

except Exception as e:
    logger.error(f"Ошибка авторизации: {e}")
    raise SystemExit(1)

logger.info(f"Группа: {GROUP_ID}")
logger.info(f"Часовой пояс: Пермь ({TIMEZONE})")
logger.info(f"Бот запущен на {len(PEER_IDS)} чатах.")

# ================= ОТПРАВКА СООБЩЕНИЙ =================

def send_message(message: str, peer_id: int):
    try:
        vk.messages.send(
            peer_id=peer_id,
            message=message,
            random_id=0
        )

        logger.info(f"Сообщение отправлено в чат {peer_id}")

    except vk_api.exceptions.ApiError as e:
        logger.error(f"Ошибка API в чате {peer_id}: {e}")

    except Exception as e:
        logger.error(f"Неожиданная ошибка в чате {peer_id}: {e}")


# ================= ОСНОВНОЙ ЦИКЛ =================

sent_today = set()
current_date = None

while True:
    try:
        now = datetime.now(TIMEZONE)
        today = now.date()
        current_minute = now.strftime("%H:%M")

        # Сброс отправленных сообщений в новый день
        if current_date != today:
            sent_today.clear()
            current_date = today

        # Отправка сообщений по расписанию
        if current_minute in SCHEDULE and current_minute not in sent_today:

            message = SCHEDULE[current_minute]

            for peer_id in PEER_IDS:
                send_message(message, peer_id)

            sent_today.add(current_minute)

        time.sleep(5)

    except Exception as e:
        logger.error(f"Ошибка в основном цикле: {e}")
        time.sleep(5)


    except Exception as e:
        logger.error(f"Ошибка в цикле: {e}")
        time.sleep(60)
