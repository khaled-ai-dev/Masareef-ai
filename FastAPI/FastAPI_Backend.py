from fastapi import FastAPI
from pydantic import BaseModel
from FastAPI.Database import Create_Database, Save_Transaction
from app.Categorizer import Categorize_Merchant
from app.SMS_Text_Extractor import Extract_Transaction_Details
from app.Text_Normalizer import normalize_text
from fastapi.middleware.cors import CORSMiddleware

import re
import joblib
import traceback
import sys
import sqlite3
sys.stdout.reconfigure(line_buffering=True)


app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

Create_Database()

model = joblib.load("models/Transaction_Type_Classifier.jonlib")
vectorizer = joblib.load("models/tfidf_vectorizer.joblib")

class SMSRequest(BaseModel):
    sms: str

@app.get("/")
def home():
    return {"message": "Masareef AI Backend is running"}

@app.post("/process-transaction")
def process_transaction(request: SMSRequest):
    try:
        SMS_text = request.sms
        Details = Extract_Transaction_Details(SMS_text)
        Merchant = Details["merchant"]
        Cleaned = normalize_text(SMS_text)
        Vector = vectorizer.transform([Cleaned])
        transaction_type = model.predict(Vector)[0]
        Category, Source = Categorize_Merchant(Details["merchant"]) #Takes the merchant name and run through the 3 layers created(dictionary, keyword, ai agent)

        Save_Transaction(merchant=Details["merchant"], category=Category, amount=Details["amount"], transaction_type=transaction_type, transaction_date=Details["date"] if Details["date"] else "Date Not Provided", Original_SMS=SMS_text)

        return {"Received_SMS": SMS_text,
                "Merchant": Details["merchant"],
                "Amount": Details["amount"],
                "Date": Details["date"] if Details["date"] else "Date Not Provided",
                "Transaction_Type": transaction_type,
                "Category": Category,
                "Category_Source": Source} #this will be return to the n8n to continue the rest of the operations.
    
    except Exception as e:
        print("=" * 60)
        print("REQUEST FAILED - FULL TRACEBACK BELOW:")
        traceback.print_exc()
        print("=" * 60)
        return {"error": str(e)}


@app.get("/spending-summary")
def spending_summary():
    Connection = sqlite3.connect("Database/transactions.db")
    Cursor = Connection.cursor()

    Cursor.execute("""
                   SELECT category, transaction_type, SUM(amount), COUNT(*)
                   FROM transactions
                   GROUP BY category, transaction_type
                   """)
    
    Rows = Cursor.fetchall()

    Cursor.execute("SELECT merchant, category, amount, transaction_date, transaction_type FROM transactions ORDER BY id DESC LIMIT 20")
    Recents = Cursor.fetchall()

    Connection.close()

    Summary = [{"category": Row[0], "transaction_type": Row[1], "total_amount": Row[2], "count": Row[3]}
               for Row in Rows]
    Recent_List = [{"merchant": r[0], "category": r[1], "amount": r[2], "date": r[3], "transaction_type": r[4]}
                   for r in Recents]
    
    return {"Summary_By_Category": Summary, "Recent_Transactions": Recent_List}