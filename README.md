Read Me
As part of my Data Analysis course I was provided with a set of data in excel which I exported to .csv files and created the following schema.

Schema (tables & key columns):

• Students(student_id PK, full_name, city, phone)

• Teachers(teacher_id PK, teacher_name, expertise, base_city, monthly_salary)

• Courses(course_id PK, course_name, duration_weeks, price)

• Batches(batch_id PK, course_id FK, teacher_id FK, start_date, days_per_week, time_slot)

• Enrollments(enroll_id PK, student_id FK, batch_id FK, enroll_date)

• Payments(payment_id PK, enroll_id FK, payment_date, amount, mode)

• Sessions(session_id PK, batch_id FK, session_date, topic)

• Attendance(session_id FK, student_id FK, present)

I then used Python and Pandas in Thonny to answer the following questions.

No.	Task (Python/pandas)
1	Total number of students.
2	City-wise student count (descending).
3	Total revenue collected from payments.
4	Monthly revenue (YYYY‑MM).
5	Outstanding by enrollment (Course price − sum of payments).
6	Top 3 courses by revenue.
7	Teacher with highest revenue attribution.
8	Average class size per batch.
9	Overall attendance rate (% present).
10	Course with maximum enrollments.
11	Students enrolled in 2 or more batches.
12	Which city generated the highest revenue?
13	Average course fee per course.
14	Weekly enrollment trend (YYYY‑WW).
15	Payment mode split (% of total).
16	Teacher gross margin (revenue − monthly salary).
17	On‑time payment rate (≤14 days from enrollment).
18	Average revenue per student (ARPU).
19	Active students in latest month (attendance present=1).
20	Next class date per batch after a given date.
