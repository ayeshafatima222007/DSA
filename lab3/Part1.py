import pandas as pd
import matplotlib.pyplot as plt

# ---------- Population bar chart ----------
df = pd.read_csv('population_by_country_2020.csv')

print(df.dtypes)
list1 = df['Country (or dependency)'].values.tolist()
list2 = df['Population (2020)'].values.tolist()

plt.bar(list1, list2, width=1, color=['red', 'green'])
plt.show()

# ---------- 1. Line chart: total steps per day ----------
daily = pd.read_csv('dailyActivity_merged.csv')
daily['ActivityDate'] = pd.to_datetime(daily['ActivityDate'], format='%m/%d/%Y')

steps = daily.groupby('ActivityDate')['TotalSteps'].sum()

plt.figure(figsize=(10, 5))
plt.plot(steps.index, steps.values, marker='o')
plt.title('Total Steps per Day')
plt.xlabel('Date')
plt.ylabel('Total Steps')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------- 2. Bar chart: daily distance covered ----------
dist = daily.groupby('ActivityDate')['TotalDistance'].sum()

plt.figure(figsize=(10, 5))
plt.bar(dist.index, dist.values, color='green')
plt.title('Total Distance Covered per Day')
plt.xlabel('Date')
plt.ylabel('Distance (km)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------- 3. Scatter chart: total time in bed ----------
sleep = pd.read_csv('sleepDay_merged.csv')
sleep['SleepDay'] = pd.to_datetime(sleep['SleepDay'], format='%m/%d/%Y %I:%M:%S %p')

plt.figure(figsize=(10, 5))
plt.scatter(sleep['SleepDay'], sleep['TotalTimeInBed'], color='purple', alpha=0.6)
plt.title('Total Time in Bed')
plt.xlabel('Date')
plt.ylabel('Minutes in Bed')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------- 4. Pie chart: hourly steps on 12 April 2016 ----------
hourly = pd.read_csv('hourlySteps_merged.csv')
hourly['ActivityHour'] = pd.to_datetime(hourly['ActivityHour'], format='%m/%d/%Y %I:%M:%S %p')

day = hourly[hourly['ActivityHour'].dt.date == pd.to_datetime('2016-04-12').date()]
by_hour = day.groupby(day['ActivityHour'].dt.hour)['StepTotal'].sum()
by_hour = by_hour[by_hour > 0]

plt.figure(figsize=(8, 8))
plt.pie(by_hour.values, labels=[f'{h}:00' for h in by_hour.index],
        autopct='%1.1f%%', startangle=90, pctdistance=0.85)
plt.title('Hourly Steps on 12 April 2016')
plt.show()
