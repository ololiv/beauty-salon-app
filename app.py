import streamlit as st
import pandas as pd
import datetime

# Настройка страницы
st.set_page_config(page_title="Пространство гармонии и красоты", layout="wide", page_icon="✨")

# Инициализация базы данных в сессии (симуляция БД)
if "appointments" not in st.session_state:
    st.session_state.appointments = pd.DataFrame(columns=[
        "Дата", "Время", "Клиент", "Услуга", "Мастер", "Стоимость", "Статус"
    ])
if "sales" not in st.session_state:
    st.session_state.sales = pd.DataFrame(columns=[
        "Дата", "Товар", "Категория", "Количество", "Сумма"
    ])

# Шапка сайта
st.title("✨ Салон «Пространство гармонии и красоты»")
st.caption("Официальное открытие: Июль 2026 | ИП Комарова М.В. | г. Санкт-Петербург, Европейский пр., д. 22")

# Боковое меню навигации
menu = st.sidebar.radio(
    "Навигация по системе",
    ["Главная & Визитка", "Онлайн-запись", "Магазин товаров", "Панель директора (Аналитика)"]
)

# Раздел 1: Главная страница / Визитка
if menu == "Главная & Визитка":
    st.header("О салоне")
    st.write("""
    Добро пожаловать в место комплексного восстановления тела и души. 
    На площади **65 кв.м.** мы создали идеальные условия для вашей восстановления.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💆‍♀️ Наши услуги")
        st.markdown("""
        * **Косметология и депиляция** (неинвазивные процедуры, мастера со средним мед. образованием)
        * **Массаж** (различные техники для расслабления)
        * **Духовный баланс** (консультации сертифицированного психолога и астролога)
        """)
    with col2:
        st.subheader("📍 Контакты и сервис")
        st.markdown("""
        * **Адрес:** г. Санкт-Петербург, проспект Европейский, дом 22
        * **Удобства:** Современный ремонт, 2 изолированных санузла для комфорта гостей
        * **Персонал:** Команда из 6 квалифицированных специалистов под управлением Комаровой М.В.
        """)

# Раздел 2: Онлайн-запись
elif menu == "Онлайн-запись":
    st.header("📅 Запись на процедуры")
    
    services = {
        "Косметологический уход": 3500,
        "Аппаратная депиляция": 2000,
        "Массаж классический (60 мин)": 3000,
        "Консультация психолога": 4000,
        "Составление натальной карты (Астролог)": 5000
    }
    
    staff = ["Елена (Косметолог)", "Ольга (Косметолог)", "Игорь (Массажист)", "Анна (Массажист)", "Татьяна (Психолог)", "Мария (Астролог)"]

    with st.form("appointment_form"):
        col1, col2 = st.columns(2)
        with col1:
            client_name = st.text_input("Ваше имя и телефон")
            service = st.selectbox("Выберите услугу", list(services.keys()))
            master = st.selectbox("Выберите специалиста", staff)
        with col2:
            date = st.date_input("Дата визита", datetime.date(2026, 7, 1))
            time = st.time_input("Время визита", datetime.time(10, 0))
            submit = st.form_submit_button("Записаться")
            
        if submit:
            if client_name:
                new_app = pd.DataFrame([{
                    "Дата": str(date), "Время": str(time), "Клиент": client_name,
                    "Услуга": service, "Мастер": master, "Стоимость": services[service], "Статус": "Подтвержден"
                }])
                st.session_state.appointments = pd.concat([st.session_state.appointments, new_app], ignore_index=True)
                st.success(f"Вы успешно записаны к мастеру {master}!")
            else:
                st.error("Пожалуйста, введите имя и контактный телефон.")

    st.subheader("Текущие записи на день")
    st.dataframe(st.session_state.appointments, use_container_width=True)

# Раздел 3: Магазин эзотерических товаров
elif menu == "Магазин товаров":
    st.header("🔮 Эзотерическая лавка")
    st.write("Дополнительный доход салона: продажа сопутствующих товаров.")
    
    products = {
        "Ароматические свечи из соевого воска": 800,
        "Набор натуральных минералов/кристаллов": 2500,
        "Благовония и палочки Пало Санто": 600,
        "Карты Таро (авторская колода)": 3000
    }
    
    with st.form("sale_form"):
        prod_name = st.selectbox("Товар", list(products.keys()))
        quantity = st.number_input("Количество", min_value=1, max_value=10, value=1)
        btn_sell = st.form_submit_button("Оформить продажу")
        
        if btn_sell:
            total_price = products[prod_name] * quantity
            new_sale = pd.DataFrame([{
                "Дата": str(datetime.date.today()), "Товар": prod_name,
                "Категория": "Эзотерика", "Количество": quantity, "Сумма": total_price
            }])
            st.session_state.sales = pd.concat([st.session_state.sales, new_sale], ignore_index=True)
            st.success(f"Продано: {prod_name} ({quantity} шт.) на сумму {total_price} руб.")

    st.subheader("История продаж за смену")
    st.dataframe(st.session_state.sales, use_container_width=True)

# Раздел 4: Кабинет директора
elif menu == "Панель директора (Аналитика)":
    st.header("📊 Аналитическая панель ИП Комаровой М.В.")
    
    total_services_rev = st.session_state.appointments["Стоимость"].sum() if not st.session_state.appointments.empty else 0
    total_sales_rev = st.session_state.sales["Сумма"].sum() if not st.session_state.sales.empty else 0
    total_revenue = total_services_rev + total_sales_rev
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Общая выручка (руб)", f"{total_revenue:,.0f}")
    kpi2.metric("Записей на процедуры", len(st.session_state.appointments))
    kpi3.metric("Штат сотрудников", "6 мастеров + 1 директор")
    
    st.subheader("Эффективность направлений")
    
    if not st.session_state.appointments.empty:
        # Встроенный график Streamlit, не зависящий от конфликтов numpy/plotly
        chart_data = st.session_state.appointments.groupby("Мастер")["Стоимость"].sum()
        st.bar_chart(chart_data)
    else:
        st.info("Нет данных о записях для построения графиков загрузки персонала.")
        
    st.subheader("Структура недвижимости и мощностей")
    st.info("Помещение: 65 кв.м. | Доступно рабочих зон: 4 кабинета + 2 санузла.")
