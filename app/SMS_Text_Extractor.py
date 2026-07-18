import re

Amount_Pattern = re.compile(r"(\d[\d,]*\.\d{1,2})") #Matches amounts with or without commas fo ex 1,200.10

Date_Patterns = [r"\d{2}[A-Z]{3}\d{2}", r"\d{2}/\d{2}/\d{4}", r"\d{2} [A-Z]{3} \d{4}", r"\d{2}-\d{2}"] #Matches common different date shapes with ones in the dataset

HSBC_Purchase_Pattern = re.compile(r"From .*?:\s*\S+\s+(.+?)\s+Purchase from")
HSBC_Transfer_Pattern = re.compile(r"Transfer to\s+(.+?)\s+\d")

Merchant_Anchors_ENG = ["at", "Purchase from", "Transfer at", "from", "via"]
Merchant_Anchors_AR = ["ل" ,"لصديقتك" ,"لصديقك", "لدى", "إلى", "عند", "من", "في"]
Non_Merchant_Words = {"حسابك", "حساب", "رقم", "بطاقتك", "بطاقة", "مرتبك", "راتبك", "الخصم", "الائتمان", "الجاري", "التوفير"}

Stop_Markers = re.compile(r"\d|\bon\b|\bat\b|\bfrom\b|/|مبلغ|بتاريخ|عبر|يوم") #a real world character bounday fix after debugging.

def Extract_Amount(text):
    Matches = Amount_Pattern.findall(text)
    if not Matches:
        return None
    return float(Matches[0].replace(",", "")) #If you found multiple numbers (amount & balance), the first number is usually always the amount so return it.

def Extract_Date(text):
    for Pattern in Date_Patterns:
        Match = re.search(Pattern, text)
        if Match:
            return Match.group(0)
    return None

def Clean_Merchant(Merchant, Full_Text):
    if not Merchant or len(Merchant.strip()) == 0:
        return None
    if len(Merchant) > 40 or len(Merchant) >= len(Full_Text) * 0.66:
        return None
    Tokens = set(Merchant.split())
    if Tokens & Non_Merchant_Words:
        return None
    return Merchant.strip()

def Extract_Merchant(text):
    Match = HSBC_Purchase_Pattern.search(text)
    if Match:
        return Match.group(1).strip(" .,-*")
    
    Match = HSBC_Transfer_Pattern.search(text)
    if Match:
        return Match.group(1).strip(" .,-*")

    All_Anchors = Merchant_Anchors_ENG + Merchant_Anchors_AR

    Found_Positions = []
    for Anchor in All_Anchors:
        Pattern = re.compile(r"(?<!\w)" + re.escape(Anchor) + r"(?!\w)")
        Match = Pattern.search(text)
        if Match:
            Found_Positions.append((Match.end(), Anchor))

    if not Found_Positions:
        return None
    
    Found_Positions.sort(key=lambda x: x[0])

    for End_Pos, Anchor in Found_Positions:
        After = text[End_Pos:].strip()
        Stop_Match = Stop_Markers.search(After)
        Merchant = After[:Stop_Match.start()].strip() if Stop_Match else After.strip()
        Merchant = Merchant.strip(" .,-*")
        Merchant = Clean_Merchant(Merchant, text)
        if Merchant:
            return Merchant

    return None #Couldn't extract the merchant.

def Extract_Transaction_Details(SMS_Text):
    return {"amount": Extract_Amount(SMS_Text), "date": Extract_Date(SMS_Text), "merchant": Extract_Merchant(SMS_Text) or "Unrecognized Source"} #Gives the entire sms text to Categorize_Merchant to do substring matching through its dictionary or keyword lookup.