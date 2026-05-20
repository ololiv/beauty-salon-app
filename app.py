import streamlit as st
import pandas as pd
import datetime
import os
import base64

#  блок дизайна страницы
st.set_page_config(page_title="Пространство гармонии и красоты", layout="wide", page_icon="✨")

def get_base64_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    return ""

bg_base64 = get_base64_background("bg.png")
if bg_base64:
    css_background = f"""
    background-image: linear-gradient(rgba(13, 8, 20, 0.75), rgba(22, 17, 36, 0.75)), url("{bg_base64}");
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    """
else:
    css_background = "background: linear-gradient(135deg, #0d0814 0%, #161124 50%, #0a1118 100%);"

st.markdown(f"""
<style>
 .stApp {{ {css_background} color: #e3d7f4; }}
 [data-testid="stSidebar"] {{ background-color: #0d0916 !important; border-right: 1px solid #4a3b68; }}
 h1, h2, h3 {{ color: #f3e1b7 !important; font-family: 'Georgia', serif; text-shadow: 0px 0px 12px rgba(243, 225, 183, 0.4); }}
 .stButton>button {{ background: linear-gradient(90deg, #5c437a 0%, #3d2a55 100%) !important; color: #f3e1b7 !important; border: 1px solid #8e6fbc !important; border-radius: 8px !important; transition: all 0.3s ease; }}
 .stButton>button:hover {{ transform: translateY(-2px); box-shadow: 0px 0px 15px rgba(142, 111, 188, 0.6); border-color: #f3e1b7 !important; }}
 .stAlert {{ background-color: #1a122c !important; border: 1px solid #5c437a !important; color: #e3d7f4 !important; }}
 .streamlit-expanderHeader {{ background-color: #140e22 !important; border: 1px solid #332350 !important; color: #f3e1b7 !important; border-radius: 6px; }}
</style>
""", unsafe_allow_html=True)

# база данных и сотрудников (временная)
STAFF_CREDENTIALS = {
 "Елена (Лазерная эстетика)": "Elena_Silk_777",
 "Ольга (Уход за лицом)": "Olga_Beauty_888",
 "Игорь (Мастер массажа)": "Igor_Relax_101",
 "Анна (Спа-терапевт)": "Anna_Spa_202",
 "Татьяна (Нумеролог)": "Tanya_Matrix_303",
 "Мария (Астролог)": "Masha_Cosmos_404",
 "Алексей (Энерготерапевт)": "Alex_Reiki_505"
}
ADMIN_PASSWORD = "Admin_Garmoniya_2026"

# Прейскурант, услуга: цена, маржа салона, прибыль Сотрудника
PRICE_LIST = {
 "Лазерная эпиляция (Женская)": {
    "Лицо полностью": [3200, 1700, 1500],
    "Бикини классическое": [2000, 1000, 1000],
    "Глубокое бикини": [4000, 2000, 2000],
    "Ноги полностью": [7000, 3900, 3100],
    "Комплекс: Все тело": [15000, 8000, 7000]
 },
 "Лазерная эпиляция (Мужская)": {
    "Подмышки": [1500, 700, 800],
    "Бикини": [5000, 2500, 2500],
    "Глубокое бикини": [6500, 3100, 3400],
    "Ноги": [8500, 4200, 4300]
 },
 "Аппаратные процедуры (Лицо)": {
    "Фотоомоложение: Лицо полностью": [7000, 3500, 3500],
    "Комплекс: Лицо + Шея + Декольте": [12000, 6000, 6000],
    "Удаление сосудов": [3200, 1500, 1700],
    "Удаление пигментации": [3500, 1700, 1800]
 },
 "Уход за лицом & Чистки": {
    "Пилинг «Знакомство»": [3200, 1500, 1700],
    "Пилинг «Age control»": [4200, 2100, 2100],
    "Маска «Anti-age»": [2000, 1000, 1000],
    "Чистка лица «Атравматическая»": [4000, 2000, 2000],
    "УЗ чистка": [3000, 1500, 1500]
 },
 "Авторский & Энергетический массаж": {
    "Огненный массаж «Императорский» (60 мин)": [10000, 5000, 5000],
    "Императорский массаж (Рейки, 120 мин)": [18000, 9000, 9000],
    "Консультация энерготерапевта": [5500, 2750, 2750]
 },
 "Классический массаж & Коррекция фигуры": {
    "Массаж спины + ШВЗ (35 мин)": [2100, 1000, 1100],
    "Общий массаж (45 мин)": [2600, 1200, 1400],
    "Лимфодренажный массаж": [2800, 1300, 1500],
    "Общий массаж тела (60 мин)": [3100, 1500, 1600],
    "Спа-массаж «Гармония и сияние»": [3250, 1600, 1650]
 },
 "Астрология & Нумерология": {
    "Астролог: Натальная карта (60 мин)": [3900, 1800, 2100],
    "Астролог: Прогноз (45 мин)": [3500, 1700, 1800],
    "Нумеролог: Консультация (45 мин)": [2100, 1000, 1100],
    "Нумеролог: Матрица Судьбы (90 мин)": [5500, 2700, 2800]
 }
}

# Инициализация баз данных в сессии
if "products_db" not in st.session_state:
 st.session_state.products_db = pd.DataFrame([
 {"Товар": "Пало Санто (Перу), премиум щепа 3 шт.", "Категория": "Благовония и ароматы", "Закупка": 250, "Розничная": 690, "Остаток": 12, "Забронировано": 0, "Описание": "Очищение пространства, снятие стресса"},
 {"Товар": "Скрутка белого шалфея для окуривания", "Категория": "Благовония и ароматы", "Закупка": 320, "Розничная": 850, "Остаток": 8, "Забронировано": 0, "Описание": "Энергетическое очищение помещения"},
 {"Товар": "Скрутка лаванды и горной полыни", "Категория": "Благовония и ароматы", "Закупка": 220, "Розничная": 650, "Остаток": 15, "Забронировано": 0, "Описание": "Расслабление, защита от негатива"},
 {"Товар": "Свеча соевая в гипсе «Гармония души»", "Категория": "Свечи ручной работы", "Закупка": 450, "Розничная": 1200, "Остаток": 7, "Забронировано": 0, "Описание": "С ароматом лотоса и эфирными маслами"},
 {"Товар": "Свеча в стекле «Привлечение изобилия»", "Категория": "Свечи ручной работы", "Закупка": 500, "Розничная": 1350, "Остаток": 6, "Забронировано": 0, "Описание": "С лепестками календулы и цитрином"}
 ])

if "appointments" not in st.session_state:
 st.session_state.appointments = pd.DataFrame(columns=["Дата", "Время", "Клиент", "Категория", "Услуга", "Мастер", "Стоимость", "Статус", "Маржа_Директора", "Прибыль_Мастера"])

if "sales" not in st.session_state:
 st.session_state.sales = pd.DataFrame(columns=["Дата", "Товар", "Категория", "Количество", "Закупка_Итого", "Выручка_Итого", "Прибыль"])

# баланс и счет
if "director_balance" not in st.session_state:
    st.session_state.director_balance = 0.0
if "employee_balances" not in st.session_state:
    st.session_state.employee_balances = {name: 0.0 for name in STAFF_CREDENTIALS.keys()}

# управление доступом
st.sidebar.markdown("### 🔑 Портал доступа")
role = st.sidebar.selectbox("Выберите Ваш статус:", ["Клиент", "Сотрудник", "Директор"])

access_granted = False
current_user_name = ""

if role == "Клиент":
 access_granted = True
elif role == "Сотрудник (Мастер)":
 selected_master = st.sidebar.selectbox("Выберите ваше имя:", list(STAFF_CREDENTIALS.keys()))
 password = st.sidebar.text_input("Введите личный пароль:", type="password")
 if password == STAFF_CREDENTIALS[selected_master]:
  access_granted = True
  current_user_name = selected_master
 elif password: st.sidebar.error("❌ Пароль неверный")
elif role == "Директор":
 password = st.sidebar.text_input("Введите мастер-ключ администратора:", type="password")
 if password == ADMIN_PASSWORD: access_granted = True
 elif password: st.sidebar.error("❌ Доступ заблокирован")

if access_granted:
 st.title("✨ Салон «Пространство гармонии и красоты»")
 st.caption("ИП Комарова М.В. | г. Санкт-Петербург, Европейский пр., д. 22 | Часы работы: 12:00 - 21:00 ежедневно")

 if role == "Клиент":
  menu = st.sidebar.radio("Навигация:", ["О салоне. Наша команда", "Онлайн-запись на визит", "🛍️ Волшебная лавка"])
 elif role == "Сотрудник (Мастер)":
  menu = st.sidebar.radio("Навигация:", [f"Моё расписание ({current_user_name})", "Продажа товаров на смене"])
 else:
  menu = st.sidebar.radio("Навигация:", ["О салоне & Наша команда", "Панель записей (Администратор)", "Продажа товаров на смене", "📊 Аналитика директора & Склад"])

 # О салоне (стартовая страница)
 if menu == "О салоне & Наша команда":
  st.header("🔮 О нашем пространстве")
  st.write("Место комплексного восстановления тела и души. Ждем вас ежедневно с 12:00 до 21:00.")
  
  st.subheader("📜 Наш прейскурант услуг")
  for cat, items in PRICE_LIST.items():
   with st.expander(cat):
    for item, values in items.items(): 
        st.write(f"🔹 **{item}** — {values[0]:,} ₽")

 # запись на процедуры. дизайн интерфейса
 elif menu in ["Онлайн-запись на визит", "Панель записей (Администратор)", "Расписание записей"]:
  st.header("📅 Запись на процедуры")
 
  if role in ["Клиент", "Администратор / Директор"]:
   with st.form("magic_app_form"):
    col1, col2 = st.columns(2)
    with col1:
     c_name = st.text_input("Имя и контактный телефон")
     cat = st.selectbox("Направление", list(PRICE_LIST.keys()))
     serv = st.selectbox("Процедура/Сеанс", list(PRICE_LIST[cat].keys()))
    with col2:
     mast = st.selectbox("Мастер пространства", list(STAFF_CREDENTIALS.keys()))
     date = st.date_input("Дата визита", datetime.date(2026, 7, 1))
     working_hours = sorted([f"{hour}:00" for hour in range(12, 21)] + [f"{hour}:30" for hour in range(12, 21)])
     time_selection = st.selectbox("Доступное время для визита:", working_hours)
 
    submit = st.form_submit_button("Подтвердить визит")
 
    if submit and c_name:
     price = PRICE_LIST[cat][serv][0]
     dir_margin = PRICE_LIST[cat][serv][1]
     emp_profit = PRICE_LIST[cat][serv][2]
     
     # Создание записи в журнале
     new_app = pd.DataFrame([{"Дата": str(date), "Template": time_selection, "Время": time_selection, "Клиент": c_name, "Категория": cat, "Услуга": serv, "Мастер": mast, "Стоимость": price, "Статус": "Подтвержден", "Маржа_Директора": dir_margin, "Прибыль_Мастера": emp_profit}])
     st.session_state.appointments = pd.concat([st.session_state.appointments, new_app], ignore_index=True)
     
     # НОбновление баланса в реальном времени
     st.session_state.director_balance += dir_margin
     st.session_state.employee_balances[mast] += emp_profit
     
     st.success(f"🎉 Запись подтверждена! Деньги распределены по счетам.")

  st.subheader("📋 Журнал текущих записей:")
  if role == "Сотрудник (Мастер)":
   filtered_apps = st.session_state.appointments[st.session_state.appointments["Мастер"] == current_user_name]
   st.dataframe(filtered_apps, use_container_width=True, hide_index=True)
  else:
   st.dataframe(st.session_state.appointments, use_container_width=True, hide_index=True)

 #  проект кабинета сотрудника
 if role == "Сотрудник (Мастер)" and menu == f"Моё расписание ({current_user_name})":
     st.markdown("---")
     st.subheader("💳 Мой финансовый счет (Личный кабинет)")
     
     # баланс сотрудника
     my_balance = st.session_state.employee_balances.get(current_user_name, 0.0)
     st.metric(label="Ваша чистая прибыль за текущую смену", value=f"{my_balance:,.2f} ₽")
     st.caption("Данные обновляются автоматически после проведения каждой записи или процедуры на ваше имя.")

 # витрина эзотерических товаов 
 elif menu == "🛍️ Волшебная лавка (Витрина & Бронь)":
  st.header("🔮 Витрина артефактов и товаров")
  display_df = st.session_state.products_db[["Товар", "Категория", "Розничная", "Остаток", "Забронировано", "Описание"]].copy()
  st.dataframe(display_df, use_container_width=True, hide_index=True)

 # касса магазина
 elif menu == "Продажа товаров на смене":
  st.header("💵 Кассовый модуль лавки")
  with st.form("cash_sale_form"):
   selected_p = st.selectbox("Товар:", st.session_state.products_db["Товар"].tolist())
   qty_sell = st.number_input("Количество (шт)", min_value=1, max_value=15, value=1)
   btn_sell = st.form_submit_button("Провести продажу")
 
   if btn_sell:
    idx = st.session_state.products_db[st.session_state.products_db["Товар"] == selected_p].index
    if st.session_state.products_db.loc[idx, "Остаток"].values[0] >= qty_sell:
     st.session_state.products_db.loc[idx, "Остаток"] -= qty_sell
     z_p = st.session_state.products_db.loc[idx, "Закупка"].values[0]
     r_p = st.session_state.products_db.loc[idx, "Розничная"].values[0]
     profit_shop = (r_p - z_p) * qty_sell
 
     new_sale = pd.DataFrame([{"Дата": str(datetime.date.today()), "Товар": selected_p, "Категория": st.session_state.products_db.loc[idx, "Категория"].values[0], "Количество": qty_sell, "Закупка_Итого": z_p * qty_sell, "Выручка_Итого": r_p * qty_sell, "Прибыль": profit_shop}])
     st.session_state.sales = pd.concat([st.session_state.sales, new_sale], ignore_index=True)
     
     # Прибыль с товаров полностью идет на счет директора!! 
     st.session_state.director_balance += float(profit_shop)
     st.success("💰 Продажа совершена! Чистая прибыль лавки переведена на счет директора.")
  st.dataframe(st.session_state.sales, use_container_width=True)

 # Аналитика директора
 elif menu == "📊 Аналитика директора & Склад":
  st.header("📊 Управленческий учет и Главный счет")
 
  # Дашборд счетов
  st.subheader("🏦 Состояние счетов в реальном времени")
  col_d1, col_d2 = st.columns(2)
  with col_d1:
      # маржа с услуг + прибыль от товаров 
      st.metric("ГЛАВНЫЙ СЧЕТ ДИРЕКТОРА (Накопленная маржа)", f"{st.session_state.director_balance:,.2f} ₽")
  with col_d2:
      total_emp_payout = sum(st.session_state.employee_balances.values())
      st.metric("Всего начислено мастерам (Фонд выплат)", f"{total_emp_payout:,.2f} ₽")
  
  # Таблица детализации по мастерам для директора
  with st.expander("👀 Посмотреть детализацию счетов по сотрудникам"):
      emp_df = pd.DataFrame(list(st.session_state.employee_balances.items()), columns=["Мастер / Специалист", "Текущий баланс к выплате (₽)"])
      st.dataframe(emp_df, use_container_width=True, hide_index=True)

  st.markdown("---")
  st.subheader("📈 Интерактивное прогнозирование (Модель таблицы AS-IS)")
 
  with st.expander("⚙️ Настройка фиксированных параметров сценария"):
   col_p1, col_p2 = st.columns(2)
   with col_p1:
    advertising = st.number_input("Реклама в месяц, руб.", value=20000.0)
    client_costs = st.number_input("Затраты на клиента в месяц, руб.", value=60000.0)
   with col_p2:
    acquiring = st.number_input("Эквайринг, руб. в месяц", value=21228.0)
    admin_salary = st.number_input("Зарплата админа, руб.", value=15000.0)

  # Совмещение статической модели и живых данных со счетов
  calculated_net_profit = st.session_state.director_balance - (advertising + client_costs + acquiring + admin_salary)

  st.markdown("### 📋 Экономическая эффективность текущей сессии")
  dm1, dm2 = st.columns(2)
  dm1.metric("Фактическая маржа на счете", f"{st.session_state.director_balance:,.2f} ₽")
  dm2.metric("Расчетная чистая прибыль салона (Маржа минус расходы)", f"{calculated_net_profit:,.2f} ₽")

  st.markdown("   ")
  st.subheader("📦 Складской отчет:")
  st.dataframe(st.session_state.products_db, use_container_width=True, hide_index=True)
