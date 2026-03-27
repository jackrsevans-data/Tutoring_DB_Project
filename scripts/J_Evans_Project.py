# Import relevant libraries
import pandas as pd

# Read CSV files to variables
Students = pd.read_csv("../data/Students.csv")
Teachers = pd.read_csv("../data/Teachers.csv")
Courses = pd.read_csv("../data/Courses.csv")
Batches = pd.read_csv("../data/Batches.csv")
Enrollments = pd.read_csv("../data/Enrollments.csv")
Payments = pd.read_csv("../data/Payments.csv")
Sessions = pd.read_csv("../data/Sessions.csv")
Attendance = pd.read_csv("../data/Attendance.csv")

# Test import/read of csvs
# print(Students.to_string())

# 1
print('Task 1 - Number of students')
print(f"There are {Students.shape[0]} students.")

# 2
print('\nTask 2 - Number of students per city')
print(Students.groupby('city').size().reset_index(name='count').sort_values(['count','city'], ascending=[False, True]))

# 3
print('\nTask 3 - Total Revenue')
TotalRev = sum(Payments.amount)
print(TotalRev)

# 4
print('\nTask 4 - Monthly Revenue')
PDate = pd.to_datetime(Payments['payment_date']).dt.strftime('%Y-%m')				# Format month and year for organisation
MonthlyRev = Payments['amount'].groupby(PDate).sum()								# Sum amounts by month
MonthlyRev = MonthlyRev.reset_index(name='Revenue').sort_values('payment_date')		# Set index and sort
MRevPrint = MonthlyRev.rename(columns={'payment_date': 'Month/Year'})				# Rename columns for presentation
print(MRevPrint)

# 5
print('\nTask 5 - Outstanding payments by enrollment')
NewTable1 = Enrollments.merge(Batches, on='batch_id').merge(Courses, on='course_id')	# Merge necessary tables for query
Paid = Payments.groupby('enroll_id')['amount'].sum()								# Calculate Payments per Enroll ID
Due = (NewTable1.set_index('enroll_id')['price'] - Paid).reset_index(name='Outstanding Debt').sort_values('enroll_id')	# Find difference, reset index and order
print(Due)

# 6
print('\nTask 6 - Top 3 courses by revenue')
NewTable2 = Payments.merge(Enrollments, on='enroll_id').merge(Batches, on='batch_id').merge(Courses, on='course_id')	# Merge necessary tables for query
CourseRev = NewTable2.groupby('course_name')['amount'].sum()					# Sum amounts for each Course by Course name
CourseRev = CourseRev.reset_index(name='Total Revenue').sort_values('Total Revenue',ascending=[False]).head(3)			#Order by Revenue and limit to top 3
print(CourseRev)

# 7
print('\nTask 7 - Teacher with most revenue')
TeacherRev = Payments.merge(Enrollments, on='enroll_id').merge(Batches, on='batch_id')		# Create initial merge for calculation
TeacherRev = TeacherRev.groupby('teacher_id')['amount'].sum()								# Group and sum by teacher id
TeacherRev = TeacherRev.reset_index(name='Total Revenue').merge(Teachers[['teacher_id','teacher_name']], on='teacher_id').sort_values('Total Revenue',ascending=[False]).head(1) # Merge teacher names to table, order and take top 1
print(TeacherRev)

# 8
print('\nTask 8 - Average class size per batch')
BatchSize = Enrollments.groupby('batch_id').size()		# Merge CSVs and find batch size per batch
AvgBatch = BatchSize.mean()								# Find average batch size
print(f'The average batchsize is {AvgBatch}.')

# 9
print('\nTask 9 - Overall attendance rate (% present)')
ARate = Attendance['present'].mean()*100					# Find average attendance
RARate = round(ARate,2)									# Round to 2 dp
print(f'{RARate}% attendance on average.')

# 10
print('\nTask 10 - Course with maximum enrollments')
BatchSize = Courses.merge(Batches, on='course_id').merge(Enrollments, on='batch_id').groupby('course_name').size()			# Merge CSVs and group by course, then find size
print(BatchSize)

# 11
print('\nTask 11 - Students enrolled in 2 or more batches')
MultiBatch = Enrollments.groupby('student_id').size()			# Find how many batches a student is enrolled on
MultiBatch = MultiBatch.reset_index(name='CourseEnrollments')	# Rename column for future queries
MultiBatch = MultiBatch.query('CourseEnrollments > 1')			# Find students on more than one batch
MultiBatchP = MultiBatch.merge(Students[['student_id','full_name']], on='student_id')
print(MultiBatchP)

# 12
print('\nTask 12 - Which city generated the highest revenue?')
CityPay = Students.merge(Enrollments[['student_id','enroll_id']], on='student_id')														# First merge
CityPay = CityPay.merge(Payments[['enroll_id','amount']],on='enroll_id').groupby('city')['amount'].sum().reset_index(name='CityRev')	# Merge Payment info, group and sum
CityPay = CityPay.sort_values('CityRev', ascending=False).head(1)																		# Order and limit to top result
print(CityPay)

# 13
print('\nTask 13 - Average course fee per course')
AvgCourseFee = Courses.groupby('course_name')['price'].mean()
print(f'The average fee per course is as listed here \n {AvgCourseFee}')
RealAvgCourseFee = Courses['price'].mean()
print(f'However, the average cost of a course is £{RealAvgCourseFee}.')

# 14
print('\nTask 14 - Weekly enrollment trend (YYYY‑WW)')
WTrend = Enrollments.assign(Week=pd.to_datetime(Enrollments['enroll_date']).dt.strftime('%Y-%U')).groupby('Week')['enroll_id'].count()		# Assign new column in Enrollments to hold number of enrollments per week
WTrend = WTrend.reset_index(name='Number of Enrollments')
print(WTrend)

# 15
print('\nTask 15 - Payment mode split (% of total)')
PayPerc = (Payments.groupby('mode')['payment_id'].count())/Payments['payment_id'].count()
PayPerc = round(PayPerc*100,2)
print(PayPerc)

# 16
print('\nTask 16 - Teacher gross margin (revenue − monthly salary)')
TeacherRev = Payments.merge(Enrollments, on='enroll_id').merge(Batches, on='batch_id')		# Create initial merge for calculation
TeacherRev = TeacherRev.groupby('teacher_id')['amount'].sum().reset_index(name='rev')								# Group and sum by teacher id, name the sum of amount as 'rev'
TeacherProfits = TeacherRev.merge(Teachers[['teacher_id','teacher_name','monthly_salary']],on='teacher_id', how='right').fillna(0)	# Right join to add all terachers to table and replace teachers with no amounts to 0
TeacherProfits = TeacherProfits.assign(gross_margin = TeacherProfits['rev'] - TeacherProfits['monthly_salary']).sort_values('gross_margin', ascending=False)		# Rev - Salary
print(TeacherProfits)

# 17
print('\nTask 17 - On‑time payment rate (≤14 days from enrollment)')
TimeDiff = Enrollments.merge(Payments[['payment_date','enroll_id']],on='enroll_id')		# Merge relevant info
TimeDiff = TimeDiff.assign(DayDiff = (pd.to_datetime(TimeDiff['payment_date']) - pd.to_datetime(TimeDiff['enroll_date'])).dt.days)		# Calculate difference in days
PaidLate = TimeDiff[TimeDiff.DayDiff > 14].count()['DayDiff']		# Count late payments. Change '14' to '7' to it is working
EnrollCount = Enrollments['enroll_id'].count()			# Count enrollements
PaidOnTime = (100/EnrollCount)*(EnrollCount - PaidLate)		# Find percentage
PaidOnTime = round(PaidOnTime,2)		# Round to 2 dp
print(f' The on-time payment rate is {PaidOnTime}%.')

# 18
print('\nTask 18 - Average revenue per student (ARPU)')
Rev = Payments.merge(Enrollments, on='enroll_id').groupby('student_id')['amount'].sum()		# Sum amounts paid by each student
print(f'The average revenue per student is {Rev.mean()} .')

# 19
print('\nTask 19 - Active students in latest month (attendance present=1)')
Attended = Attendance.merge(Sessions[['session_id','session_date']], on='session_id');		# Merge necessary files
MostRecent = pd.to_datetime(Attended['session_date']).max().to_period('M');					# Find most recent session and extract month (Should return Feb 2025)
AttendanceList = Attended[(Attended['present'].eq(1)) & (pd.to_datetime(Attended['session_date']).dt.to_period('M').eq(MostRecent))]['student_id'].unique()		# Create an arrray of students where they had attended as session and the session was in the last month, then remove duplicate student IDs.
AttendanceCount = len(AttendanceList)		# Find the number of students in attendance
print(f'There were {AttendanceCount} active students in attendance in the last month. \nThe student IDs for these students are {AttendanceList}.')

# 20
print('\nTask 20 - Next class date per batch after a given date')
MyGivenDate = pd.to_datetime('2025-01-15')		# Set date to find dates
NextSessions = Sessions.loc[pd.to_datetime(Sessions['session_date']).ge(MyGivenDate)].groupby('batch_id')['session_date'].min().reset_index(name='Next Session')	# Find sessions with a date >= given date and group by batch, then find earliest date using min()
print(f'The date given was {MyGivenDate.to_period("D")}. \nThese batches have an upcoming session.')
print(NextSessions)
