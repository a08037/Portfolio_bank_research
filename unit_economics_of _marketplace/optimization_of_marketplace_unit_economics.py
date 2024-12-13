# -*- coding: utf-8 -*-
"""Optimization of marketplace unit economics.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EiDH7uw3QDqz1zLf2cTMI77SZKmgnX2z
"""

import pandas as pd

# Load the dataset to examine its structure and data
file_path = '/content/drive/MyDrive/Seller_data.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataset to understand its structure
data.head()

# 1. Средний чек с каждой продажи (среднее значение 'Order_Value')
average_order_value = data['Order_Value'].mean()

# 2. Средняя комиссия с каждой продажи
data['Commission_Income'] = data['Order_Value'] * data['Commission_Rate']
average_commission_per_sale = data['Commission_Income'].mean()

# 3. Средний доход продавца (учитываем доходы от продвижения и подписки)
data['Seller_Income'] = data['Promotion_Income'] + data['Subscription_Income']
average_seller_income = data['Seller_Income'].mean()

# 4. Процент продавцов, использующих платные инструменты продвижения
promotion_used_percentage = (data['Promotion_Used'].sum() / len(data)) * 100

# 5. Процент продавцов, использующих платную подписку
subscription_used_percentage = (data['Subscription'].sum() / len(data)) * 100

# Подготовим результаты
results = {
    'Средний чек с каждой продажи (руб.)': average_order_value,
    'Средняя комиссия с каждой продажи (руб.)': average_commission_per_sale,
    'Средний доход продавца (руб.)': average_seller_income,
    'Процент продавцов, использующих платные инструменты продвижения (%)': promotion_used_percentage,
    'Процент продавцов, использующих платную подписку (%)': subscription_used_percentage
}

results

# Загружаем данные для когортного анализа
cohort_data_path = '/content/drive/MyDrive/Cohort_analysis_data.csv'
cohort_data = pd.read_csv(cohort_data_path)

# Посмотрим на структуру данных, чтобы понять, как их можно обработать для когортного анализа
cohort_data.head()

# Преобразуем столбец с датой регистрации в формат datetime
cohort_data['registration_date'] = pd.to_datetime(cohort_data['registration_date'])

# Добавляем новый столбец, который показывает месяц и год регистрации для создания когорт
cohort_data['cohort_month'] = cohort_data['registration_date'].dt.to_period('M')

# Группируем данные по когорте (месяц регистрации) и считаем процент активных пользователей в каждом периоде
cohort_pivot = cohort_data.groupby('cohort_month').agg({
    'activity_1_month': 'mean',
    'activity_3_month': 'mean',
    'activity_6_month': 'mean',
    'activity_12_month': 'mean'
}) * 100  # Преобразуем в проценты

# Построим тепловую карту для визуализации когортного анализа
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.heatmap(cohort_pivot, annot=True, fmt=".1f", cmap="Blues", cbar_kws={'label': 'Удержание (%)'})
plt.title('Когортный анализ удержания пользователей')
plt.xlabel('Период (месяцы)')
plt.ylabel('Когорта (месяц регистрации)')
plt.show()

# Загружаем данные для когортного анализа продавцов
sellers_cohort_data_path = '/content/drive/MyDrive/Sellers_cohort_analysis_data.csv'
sellers_cohort_data = pd.read_csv(sellers_cohort_data_path)

# Посмотрим на структуру данных, чтобы понять, как их можно обработать для когортного анализа
sellers_cohort_data.head()

# Преобразуем столбец с датой регистрации в формат datetime
sellers_cohort_data['registration_date'] = pd.to_datetime(sellers_cohort_data['registration_date'])

# Добавляем новый столбец, который показывает месяц и год регистрации для создания когорт
sellers_cohort_data['cohort_month'] = sellers_cohort_data['registration_date'].dt.to_period('M')

# Группируем данные по когорте (месяц регистрации) и считаем процент активных продавцов в каждом периоде
sellers_cohort_pivot = sellers_cohort_data.groupby('cohort_month').agg({
    'activity_1_month': 'mean',
    'activity_3_month': 'mean',
    'activity_6_month': 'mean',
    'activity_12_month': 'mean'
}) * 100  # Преобразуем в проценты

# Построим тепловую карту для визуализации когортного анализа
plt.figure(figsize=(10, 6))
sns.heatmap(sellers_cohort_pivot, annot=True, fmt=".1f", cmap="Blues", cbar_kws={'label': 'Удержание (%)'})
plt.title('Когортный анализ удержания продавцов')
plt.xlabel('Период (месяцы)')
plt.ylabel('Когорта (месяц регистрации)')
plt.show()