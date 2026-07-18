import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

Transaction_Type = {
    "Groceries": "Purchase",
    "Transport": "Purchase",
    "Bills": "Purchase",
    "Dining": "Purchase",
    "Entertainment": "Purchase",
    "Shopping": "Purchase",
    "ATM Withdrawal": "ATM Withdrawal",
    "Transfer": "Transfer",
    "Salary": "Salary Credit"
}

Card_Merchant_Categories = {"Groceries", "Transport", "Bills", "Dining", "Entertainment", "Shopping"}

Categories = {"Groceries": {
               "merchants": [("كارفور", "CARREFOUR"), ("سبينس", "SPINNEYS"), ("سعودي ماركت", "SEOUDI MARKET"),
                              ("محمود الفار", "Mahmoud El Far"), ("مترو ماركت", "METRO MARKET"),
                              ("أولاد رجب", "AWLAD RAGAB"), ("بريدفاست", "BREADFAST"), ("خير زمان", "KHEIR ZAMAN"),
                              ("هايبر وان", "HYPER ONE"), ("جون مارت", "JOHN MART"), ("لولو ماركت", "LULU HYPERMARKET"),
                              ("بيم", "BIM"), ("الفا ماركت", "ALFA MARKET"), ("Gourmet Egypt", "GOURMET EGYPT"), ("Oscar", "OSCAR MARKET")],
                "amount_range": (150, 1200)
                },

               "Transport": {
                 "merchants": [("أوبر", "UBER"), ("كريم", "CAREEM"), ("ديدي", "DIDI"),
                                ("إن درايف", "INDRIVE"), ("سويفل", "SWVL"), ("توتال", "TOTAL FUEL STATION"),
                                ("إمارات مصر", "EMIRATES MISR"), ("بنزينة وطنية", "WATANIYA"), ("شل", "SHELL"),("موبيل", "MOBIL"),
                                ("تشيل أوت", "CHILL OUT"), ("مترو الأنفاق", "CAIRO METRO"), ("السكة الحديد", "EGYPTIAN RAILWAYS")],
                 "amount_range": (20, 300)
                },

               "Bills": {
                 "merchants": [("فودافون مصر", "VODAFONE EGYPT"), ("أورانج مصر", "ORANGE EGYPT"),
                                ("وي", "WE TELECOM"), ("شركة الكهرباء", "ELECTRICITY COMPANY"), ("شركة مياه الشرب", "WATER COMPANY"),
                                ("غاز مصر", "GAS MISR"), ("اتصالات مصر", "ETISALAT MISR")],
                 "amount_range": (100, 800)
                },

               "Dining": {
                 "merchants": [("كنتاكي", "KFC"), ("ماكدونالدز", "MCDONALDS"), ("ستاربكس", "STARBUCKS"),
                               ("تالابات", "TALABAT"), ("أوطلب", "OTLOB"), ("إلمنيوز", "ELMENUS"),
                               ("بريدفاست كوفي", "BREADFAST COFFEE"), ("بازوكا", "BAZOOKA"),
                               ("بوفالو برجر", "BUFFALO BURGER"), ("سيلانترو", "CILANTRO"), ("وينديز", "WENDY'S")],
                 "amount_range": (80, 500)
                },

                "ATM Withdrawal": {
                 "merchants": [("ماكينة صراف آلي", "ATM WITHDRAWAL")],
                 "amount_range": (200, 3000)
                },

                "Transfer": {
                  "merchants": [("إنستا باي", "INSTAPAY"), ("فودافون كاش", "VODAFONE CASH"), ("فوري", "FAWRY"),
                                ("تيلدا" ,"Telda"), ("اتصالات كاش", "Etisalat Cash"), ("اورنج كاش", "Orange Cash")],
                  "amount_range": (100, 5000)
                },

                "Salary": {
                 "merchants": [("راتب شهري", "MONTHLY SALARY")],
                 "amount_range": (6000, 25000)
                },

                "Entertainment": {
                 "merchants": [("نتفليكس", "NETFLIX"), ("سينما فوكس", "VOX CINEMA"), ("سبوتيفاي", "SPOTIFY"),
                                ("شاهد", "SHAHID"), ("WATCH IT", "WATCH IT"), ("OSN+", "OSN+"), ("أنغامي", "ANGHAMI"), ("يوتيوب بريميوم", "YOUTUBE PREMIUM")],
                 "amount_range": (50, 400)
                },

                "Shopping": {
                 "merchants": [("أمازون مصر", "AMAZON EGYPT"), ("نون", "NOON"), ("جوميا", "JUMIA"), ("زارا", "ZARA"),
                               ("H&M", "H&M"), ("LC Waikiki", "LC WAIKIKI"), ("Defacto", "DEFACTO"), ("Carina", "CARINA"),
                               ("Raya Shop", "RAYA SHOP"), ("2B", "2B"), ("B.Tech", "B.TECH"), ("Fresh", "FRESH"), ("Pandora", "Pandora")],
                 "amount_range": (100, 3000)
                }
            }


Bank_Profiles = [{"bank_key": "HSBC", "sender_names": ["HSBC", "HSBC EGYPT"], "message_style": [("hsbc_eng", 0.85), ("ar", 0.15)]},
                 {"bank_key": "NBE", "sender_names": ["BanK-AlAhly", "NBE", "البنك الأهلي المصري"], "message_style": [("ar_nbe", 0.85), ("eng_generic", 0.15)]},
                 {"bank_key": "CIB", "sender_names": ["CIB", "CIB-EGYPT", "CIB Egypt"], "message_style": [("eng_generic", 0.85), ("ar", 0.15)]},
                 {"bank_key": "QNB_ALAHLI", "sender_names": ["QNBAlAhli", "QNB Al Ahli", "QNB-EGYPT", "QNB"], "message_style": [("eng_generic", 0.85), ("ar", 0.15)]},
                 {"bank_key": "BANQUE_MISR", "sender_names": ["Banque Misr", "بنك مصر", "BM-Egypt"], "message_style": [("ar", 0.85), ("eng_generic", 0.15)]},
                 {"bank_key": "BANQUE_DU_CAIRE", "sender_names": ["Banque Du Caire", "بنك القاهرة", "BDC-Egypt", "BdC"], "message_style": [("ar", 0.85), ("eng_generic", 0.15)]},
                 {"bank_key": "AAIB", "sender_names": ["AAIB", "AAIB-EGYPT"], "message_style": [("eng_generic", 0.85), ("ar", 0.15)]},
                 {"bank_key": "Alexbank", "sender_names": ["AlexBank", "بنك الأسكندرية", "بنك اسكندرية", "Alex Bank", "Alex_Bank", "AlexandriaBank", "Alexandria Bank"], "message_style": [("ar", 0.85), ("eng_generic", 0.15)]},
                 {"bank_key": "ADIB", "sender_names": ["ADIB", "ADIB EGYPT", "ADIB_EGYPT"], "message_style": [("eng_generic", 0.85), ("ar", 0.15)]},
                 {"bank_key": "FAB", "sender_names": ["FAB", "FAB EGYPT", "FAB_EGYPT"], "message_style": [("eng_generic", 0.85), ("ar", 0.15)]}]


ARABIC_First_Names = ["محمد", "احمد", "يوسف", "مصطفى", "علي", "جنى", "سارة", "سلمى", "منى", "شهد"]

ATM_Branches = ["الدقي", "المعادي", "مدينة نصر", "المهندسين", "التجمع الخامس", "وسط البلد"]
ATM_Branches_Eng = ["Dokki", "Maadi", "Nasr City", "Mohandessin", "New Cairo", "Madinaty", "Rehab", "Fifth Settlement", "Downtown"]
ATM_Fees = ["2.00", "5.00", "7.50", "10.00", "15.00"]

Transfer_Reference = ["Rent Payment", "Family Support", "Loan Repayment", "Tuition Fees", "Utility Split"]


ARABIC_Purchase_Templates = ["عزيزنا العميل، تم خصم مبلغ {amount} جنيه من حسابك رقم ****{last4} لدى {merchant} بتاريخ {date} - {bank}",
                             "تنبيه: عملية شراء بقيمة {amount} جنيه في {merchant} تمت بنجاح - {bank}",
                             "تمت عملية شراء بمبلغ {amount} ج.م لدى {merchant} باستخدام بطاقتكم المنتهية برقم {last4}. الرصيد المتاح: {balance} ج.م.",
                             "عميلنا العزيز، تم استخدام بطاقتكم الائتمانية المنتهية برقم {last4} لسداد مبلغ {amount} ج.م لدى {merchant}.",
                             "تم الدفع لصالح {merchant} بمبلغ {amount} جنيه عن طريق بطاقتك بتاريخ {date}"]
ARABIC_Transfer_Templates = ["تم تحويل مبلغ {amount} جنيه إلى حساب ****{last4} عبر {merchant} بتاريخ {date}",
                            "تنبيه: تم إضافة تحويل وارد بحسابكم المنتهي برقم {last4} بمبلغ {amount} ج.م من {masked_recipient} بتاريخ اليوم {date}.",
                            "عميلنا العزيز، تم تحويل مبلغ {amount} ج.م من حسابكم عبر تطبيق الهاتف البنكي إلى حساب رقم XXXXX{last4} في {date} {time}.",
                            "حولت لصديقك {masked_recipient} مبلغ {amount} جنيه عن طريق تطبيق البنك على موبايلك.",
                            "قمت بتحويل {amount} ج.م إلى {masked_recipient} بنجاح بتاريخ {date} - {bank}"]
ARABIC_Salary_Templates = ["تم إيداع راتبك الشهري بقيمة {amount} جنيه في حسابك رقم ****{last4} - {bank}",
                           "عميلنا العزيز، تم إضافة مرتبكم بمبلغ {amount} ج.م إلى حسابكم المنتهي برقم {last4} بتاريخ {date}. رصيدكم المتاح الحالي هو {balance} ج.م.",
                           "تم تحويل دفعة راتب واردة بمبلغ {amount} ج.م إلى بطاقة المرتبات الخاصة بكم في {date} الساعة {time}.",
                           "وصلك مبلغ {amount} جنيه في حسابك كراتب هذا الشهر، رصيدك الحالي أصبح {balance} جنيه.",
                           "وصل راتبك بقيمة {amount} ج.م إلى حسابك رقم {last4} بنجاح بتاريخ {date}."]
ARABIC_ATM_Templates = ["سحب نقدي بمبلغ {amount} جنيه من {merchant} بتاريخ {date} - {bank}",
                        "تمت عملية سحب نقدي بمبلغ {amount} ج.م من ماكينة الصراف الآلي فرع {atm_branch} باستخدام بطاقتكم المنتهية برقم {last4}. الرصيد المتاح: {balance} ج.م.",
                        "تنبيه: تم سحب مبلغ {amount} ج.م باستخدام بطاقة الخصم المباشر {last4} من ماكينة بنك آخر. تم تطبيق رسوم سحب بقيمة {atm_fee} ج.م.",
                        "لقد قمت بسحب {amount} جنيه نقدا من فرع البنك الرئيسي باستخدام بطاقتك رقم {last4}.",
                        "قمت بسحب مبلغ {amount} ج.م نقدا بتاريخ {date} من ماكينة صراف آلي - {bank}"]

ENGLISH_Purchase_Templates = ["Dear Customer, your card ending {last4} was used for EGP {amount} at {merchant} on {date} - {bank}",
                               "Transaction Alert: EGP {amount} debited at {merchant} on {date}. Card ****{last4} - {bank}",
                               "{bank} Alert: EGP {amount} debited from {merchant}/Account card ending {last4} at POS transaction."]
ENGLISH_Transfer_Templates = ["You sent EGP {amount} via {merchant} on {date} - {bank}",
                              "{bank} Alert: Outward InstaPay transfer of EGP {amount} from account XXXXX{last4} was successful on {date} {time}. Ref: {Transfer_Reference}.",
                              "Your account ending in {last4} has been credited with EGP {amount} via Inward Local Transfer. Total Available Balance: EGP {balance}"]
ENGLISH_Salary_Templates = ["Your monthly salary of EGP {amount} has been credited to account ****{last4} - {bank}",
                            "Your account XXXXX{last4} has been credited with EGP {amount} via Payroll Deposit on {date}. Thank you",
                            "Your corporate salary of EGP {amount} was credited to your account ending in {last4} on {date}. Your available balance is EGP {balance}."]
ENGLISH_ATM_Templates = ["Cash withdrawal of EGP {amount} from ATM on {date}. Card ****{last4} - {bank}",
                         "Cash withdrawal of EGP {amount} from ({atm_branch_eng}) using card ending {last4} on {date}. Remaining Balance: EGP {balance}",
                         "Dear Customer, EGP {amount} was withdrawn via Cash Advance from your Credit Card ending {last4}"
                         "You withdrew EGP {amount} from your account using your debit card on {date} - {bank}"]


HSBC_Purchase_Template = ["From {bank}: {date} {merchant} Purchase from {masked_card} EGP {amount}- "
                          "Your available balance is EGP {balance}"]
HSBC_Transfer_Template = ["From {bank}: {date} Transfer to {merchant} {masked_card} EGP {amount}- "
                          "Your available balance is EGP {balance}"]
HSBC_Salary_Template = ["From {bank}: {date} Salary Credit {masked_card} EGP {amount}+ "
                        "Your available balance is EGP {balance}"]
HSBC_ATM_Template = ["From {bank}: {date} ATM Cash Withdrawal {masked_card} EGP {amount}- "
                     "Your available balance is EGP {balance}"]

NBE_ARABIC_Purchase_Templates = ["تم خصم {amount} جم من {card_type} رقم {last4} عند {merchant} يوم {date} الساعة {time} المتاح {balance} جم للمزيد اتصل ب 19623"]
NBE_ARABIC_Transfer_Templates = ["تم تنفيذ تحويل لحظي من حسابكم رقم {last4} بمبلغ {amount} جم إلى {masked_recipient} رقم مرجعي {reference_number} يوم {date} الساعة {time} للمزيد اتصل بـ 19623"]
NBE_ARABIC_ATM_Templates = ["تم سحب {amount} جم نقدا من {card_type} رقم {last4} من ماكينة صراف آلي يوم {date} الساعة {time} المتاح {balance} جم للمزيد اتصل ب 19623",
                            "عزيزنا العميل، تم سحب مبلغ {amount} جم من ماكينة الصراف الآلي باستخدام {card_type} رقم {last4} بتاريخ {date} الساعة {time} الرصيد المتاح {balance} جم",
                            "إشعار سحب نقدي: {amount} جم من {card_type} {last4} يوم {date} الساعة {time} المتاح {balance} جم اتصل ب 19623"]
NBE_ARABIC_Salary_Templates = ["تم إيداع {amount} جم في حسابكم رقم {last4} يوم {date} الساعة {time} المتاح {balance} جم للمزيد اتصل ب 19623",
                               "عزيزنا العميل، تم إيداع مرتب بقيمة {amount} جم بحسابكم رقم {last4} بتاريخ {date} الساعة {time} الرصيد المتاح {balance} جم",
                               "إشعار إيداع: مبلغ {amount} جم تم إضافته لحسابكم {last4} يوم {date} الساعة {time} المتاح {balance} جم اتصل ب 19623"]

def masked_card():
    return f"{random.randint(100,999)}-{random.randint(100, 999)}***-{random.randint(100,999)}"

def mask_account():
    last4 = random.randint(1000, 9999)
    style_choice = random.choice(["starts_last4", "dashes_last4", "plain_last4"])
    if style_choice == "starts_last4":
        return f"****{last4}"
    if style_choice == "dashes_last4":
        return f"XXXX-XXXX-XXXX-{last4}"
    return f"{last4}"


def plain_last4():
    return str(random.randint(1000, 9999))


def random_time():
    return f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"

def random_date(style):
    days_back = random.randint(0, 180)
    date_obj = datetime.now() - timedelta(days = days_back)
    if style == "ar":
        return date_obj.strftime("%d/%m/%Y")
    if style == "ar_nbe":
        return date_obj.strftime("%m-%d")
    if style == "hsbc_eng":
        return date_obj.strftime("%d%b%y").upper()
    return date_obj.strftime("%d %b %Y").upper()


def masked_recipient_name():
    first = random.choice(ARABIC_First_Names)
    arabic_initial = random.choice(["م", "ع", "ح", "س", "ي"])
    english_initial = random.choice(["H", "M", "A", "S", "K"])
    return f"{first} {arabic_initial}**** {english_initial}***"


def build_message(category, merchant, amount, bank_display, style, date):
    balance = round(amount + random.uniform(50, 5000), 2)

    fields = {"bank": bank_display, "merchant": merchant, "date": date,
              "time": random_time(), "amount": f"{amount:,.2f}", "balance": f"{balance:,.2f}",
              "masked_card": masked_card(), "masked_account": mask_account(), "last4": plain_last4(),
              "card_type": random.choice(["بطاقة الائتمان", "بطاقة الخصم", "حسابكم"]),
              "reference_number": str(random.randint(100000000000, 999999999999)),
              "masked_recipient": masked_recipient_name(),
              "atm_branch": random.choice(ATM_Branches),
              "atm_fee": random.choice(ATM_Fees),
              "Transfer_Reference": random.choice(Transfer_Reference),
              "atm_branch_eng": random.choice(ATM_Branches_Eng)
              }
    
    style_table = {"hsbc_eng": {"ATM Withdrawal": HSBC_ATM_Template, "Transfer": HSBC_Transfer_Template,
                   "Salary": HSBC_Salary_Template, "_default": HSBC_Purchase_Template},
                   "eng_generic": {"ATM Withdrawal": ENGLISH_ATM_Templates, "Transfer": ENGLISH_Transfer_Templates,
                    "Salary": ENGLISH_Salary_Templates, "_default": ENGLISH_Purchase_Templates},
                    "ar": {"ATM Withdrawal": ARABIC_ATM_Templates, "Transfer": ARABIC_Transfer_Templates,
                    "Salary": ARABIC_Salary_Templates, "_default": ARABIC_Purchase_Templates},
                    "ar_nbe": {"ATM Withdrawal": NBE_ARABIC_ATM_Templates, "Transfer": NBE_ARABIC_Transfer_Templates,
                    "Salary": NBE_ARABIC_Salary_Templates, "_default": NBE_ARABIC_Purchase_Templates}
                   }
    
    templates = style_table[style].get(category, style_table[style]["_default"])
    template = random.choice(templates)
    return template.format(**fields)


def generate_one(category):
    info = Categories[category]
    merchant_ar, merchant_eng = random.choice(info["merchants"])
    low, high = info["amount_range"]
    amount = round(random.uniform(low, high), 2)
    profile = random.choice(Bank_Profiles)
    styles, weights = zip(*profile["message_style"])
    style = random.choices(styles, weights=weights, k=1)[0]
    bank_display = random.choice(profile["sender_names"])

    if category in Card_Merchant_Categories:
        merchant = merchant_eng
    else:
        merchant = merchant_ar if style in ("ar", "ar_nbe") else merchant_eng

    date = random_date(style)
    text = build_message(category, merchant, amount, bank_display, style, date)

    return {
        "sms_text": text,
        "category": category,
        "transaction_type": Transaction_Type[category],
        "amount": amount,
        "merchant": merchant,
        "bank": bank_display,
        "bank_key": profile["bank_key"],
        "date": date,
        "language": "ar" if style in ("ar", "ar_nbe") else "en"
    }

Samples_Per_Category = 180

Rows = []
for category in Categories:
    for i in range(Samples_Per_Category):
        Rows.append(generate_one(category))

df = pd.DataFrame(Rows)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("data/Bank_SMS_Dataset_Final.csv", index=False, encoding="utf-8-sig")

print(f"Generated {len(df)} Artificial SMS Records.")
print(df["category"].value_counts())
print(df["transaction_type"].value_counts())
print(df["language"].value_counts())
print(df["bank"].value_counts())