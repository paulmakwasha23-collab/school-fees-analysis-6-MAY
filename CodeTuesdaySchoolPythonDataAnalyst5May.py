import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime,timedelta
import os


os.makedirs("client_deliverables",exist_ok=True)


np.random.seed(101)
grades = ["Form 1","Form 2","Form 3","Form 4","Form 5","Form 6"]
terms = ["Term 1","Term 2","Term 3"]
status =["Paid","Partial","Unpaid","Late"]

df = pd.DataFrame({
    "StudentID":[f"SM{2000+i}" for i in range(3000)],
    "Grade":np.random.choice(grades,3000,p=[0.3,0.25,0.2,0.12,0.08,0.05]),
    "Term":np.random.choice(terms,3000),
    "FeesDue":np.random.randint(250,900,3000),
    "FeesPaid":np.random.randint(0,900,3000),
    "PaymentStatus":np.random.choice(status,3000,p=[0.55,0.2,0.15,0.1]),
    "PaymentDate":pd.to_datetime("2026-01-01")+pd.to_timedelta(np.random.randint(0,120,3000),unit="D")
    })
df["Balance"] =(df["FeesDue"]-df["FeesPaid"]).clip(lower=0)
df["DaysLate"] = np.where(df["PaymentStatus"]=="Late",np.random.randint(1,30,3000),0)



df = df.drop_duplicates(subset=["StudentID","Term"])
df["Grade"] = df["Grade"].str.strip().str.title()
print("Data cleaned.Shape:",df.shape)


total_due = df["FeesDue"].sum()
total_paid = df["FeesPaid"].sum()
recovery_rate = total_paid/total_due

by_grade = df.groupby("Grade").agg(
    TotalDue=("FeesDue","sum"),
    TotalPaid=("FeesPaid","sum"),
    AvgBalance=("Balance","mean"),
    UnpaidCount=("PaymentStatus",lambda x:(x=="Unpaid").sum())
).sort_values("TotalDue",ascending=False)
by_grade["RecoveryRate"]  = by_grade["TotalPaid"]/by_grade["TotalDue"]


plt.figure(figsize=(10,5))
sns.barplot(x=by_grade.index,y=by_grade["TotalDue"])
plt.title("Total Fees Due by Grade")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("client_deliverables/01_total_due_by_grade.png")

plt.figure(figsize=(8,5))
sns.countplot(data=df,x="PaymentStatus",order=df["PaymentStatus"].value_counts().index)
plt.title("Payment Status Distribution")
plt.tight_layout()
plt.savefig("client_deliverables/01_payment_status.png")

summary = f"""
School fees analyst report
geneerated: {datetime.now().date()}


key metrics:
    total fees due: ${total_due:,.2f}
    total collected: ${total_paid:,.2f}
    recovery rate: {recovery_rate:.2f}
    
    
top top 3 insights:
    1. {by_grade.index[0]} has highest total due: ${by_grade.iloc[0]["TotalDue"]:,.2f}
    2. {by_grade["UnpaidCount"].idxmax()} has most unpaid accounts: {by_grade["UnpaidCount"].max()} students
    3. overal recovery is {recovery_rate:.2f}. School target is 85%.
    
recommendations:
    - send sms to {df[df["PaymentStatus"]=="Late"].shape[0]} students with "Late" status.
    - focus recovery efforts on {by_grade.index[0]} and {by_grade.index[1]}.
    - offer early payment discount for term 2 to improve cashflow.
"""                                
with open ("client_deliverables/Executive_Summary.txt","w") as f:
    f.write(summary)
df.to_csv("client_deliverables/cleaned_student_fees.csv",index=False)
by_grade.to_csv("client_deliverables/summary_by_grade.csv")

print("\n PROJECT COMPLETE")
print('Check "client_deliverables" folder for:')
print("1.cleaned_student_fees.csv")
print("2.summary_by_grade.csv")
print("3.2 charts PNG")
print("4.Executive_Summary.txt")
                                 
                                 
                                 


    
    
    
