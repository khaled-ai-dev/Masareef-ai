Keyword_Category_Rules = [(["MARKET", "SUPERMARKET", "MART", "HYPER", "ماركت", "سوبر ماركت", "مارت", "هايبر"], "Groceries"),
                          (["Pharmacy", "صيدلية"], "Bills"),
                          (["CAFE", "COFFEE", "RESTAURANT", "كوفي", "مطعم", "كافيه"], "Dining"),
                          (["UBER", "TAXI", "FUEL", "PETROL", "تاكسي", "تاكسي", "موصلات"], "Transport"),
                          (["TELECOM", "MOBILE", "أورانج مصر", "فودافون كاش", "اتصالات مصر"], "Bills"),
                          (["CINEMA", "سينما", "NETFLIX", "STREAMING", "FUN_ZONE"], "Entertainment")] #This is layer 2 (for merchants not in dictionary).

#Loops through different keyword groups to check a substring match, not an exact match.
def Keyword_Lookup(Merchant_text):
    text_upper = Merchant_text.upper()
    for keywords, category in Keyword_Category_Rules:
        for keyword in keywords:
            if keyword.upper() in text_upper:
                return category
    return None