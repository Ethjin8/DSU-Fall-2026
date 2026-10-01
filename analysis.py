import pandas as pd
import numpy as np


df = pd.read_csv('student-data.csv')


print("--------Q1: Parent's Highest Education is HS--------")
high_school = df[df['parental_education'] == 'High School']
print('Q1 count:', len(high_school))
print('Q1 average attendance:', round(high_school['attendance_percent'].mean(), 1))
print()


print("--------Q2: Relative Improvement--------")
df['improvement'] = ((df['final_exam_score'] - df['previous_grade']) / df['previous_grade'] * 100).round(2)
improved = df[(df['improvement'] >= 20) & (df['improvement'] <= 30)]
print('Q2 count:', len(improved))
print('Q2 % with part-time job:', round((improved['part_time_job'] == 'Yes').mean() * 100, 1))
print()


print("--------Challenge Q1: Study Time vs. Sleep vs. Final Exam Score--------")
print('CQ1 corr study vs score:', round(df['study_time_hours'].corr(df['final_exam_score']), 3))
print('CQ1 corr sleep vs score:', round(df['sleep_hours'].corr(df['final_exam_score']), 3))
print()

study_ranges = [(0, 2), (2, 4), (4, 6), (6, 9)]
sleep_ranges = [(0, 6), (6, 8), (8, 11)]
for study_low, study_high in study_ranges:
    for sleep_low, sleep_high in sleep_ranges:
        group = df[(df['study_time_hours'] > study_low) & (df['study_time_hours'] <= study_high) &
                   (df['sleep_hours'] > sleep_low) & (df['sleep_hours'] <= sleep_high)]
        print(f'study {study_low}-{study_high}h, sleep {sleep_low}-{sleep_high}h:',
              len(group), 'students, avg score', round(group['final_exam_score'].mean(), 1))
print()


print("--------Challenge Q2: Higher/Lower Than Expected Based on Study Time--------")
# Step 1: "expected" score = line of best fit between study hours and score
slope, intercept = np.polyfit(df['study_time_hours'], df['final_exam_score'], 1)
print('Expected score =', round(intercept, 1), '+', round(slope, 1), 'x study hours')
df['expected'] = intercept + slope * df['study_time_hours']

# Step 2: gap = actual score - expected score
df['gap'] = df['final_exam_score'] - df['expected']

# Step 3: "unexpected" = 10+ points above (over) or below (under) expected
over = df[df['gap'] >= 10]
under = df[df['gap'] <= -10]
print('Overperformers (10+ above expected):', len(over))
print('Underperformers (10+ below expected):', len(under))
print()

# Step 4: show the 3 biggest of each
print('Biggest overperformers:')
print(over.nlargest(3, 'gap')[['student_id', 'study_time_hours', 'expected', 'final_exam_score', 'gap']].round(1))
print('Biggest underperformers:')
print(under.nsmallest(3, 'gap')[['student_id', 'study_time_hours', 'expected', 'final_exam_score', 'gap']].round(1))
print()

# Step 5: compare the two groups on other variables
print('                     Over   Under')
print('Avg previous grade: ', round(over['previous_grade'].mean(), 1), ' ', round(under['previous_grade'].mean(), 1))
print('Avg attendance %:   ', round(over['attendance_percent'].mean(), 1), ' ', round(under['attendance_percent'].mean(), 1))
print('Avg sleep hours:    ', round(over['sleep_hours'].mean(), 1), '  ', round(under['sleep_hours'].mean(), 1))
print('% internet access:  ', round((over['internet_access'] == 'Yes').mean() * 100, 1), ' ', round((under['internet_access'] == 'Yes').mean() * 100, 1))
print('% part-time job:    ', round((over['part_time_job'] == 'Yes').mean() * 100, 1), ' ', round((under['part_time_job'] == 'Yes').mean() * 100, 1))
print('% extracurriculars: ', round((over['extracurricular_activities'] == 'Yes').mean() * 100, 1), ' ', round((under['extracurricular_activities'] == 'Yes').mean() * 100, 1))
