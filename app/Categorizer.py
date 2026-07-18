from app.Merchant_Dictionary import Merchant_Category_Map
from app.Keyword_Rules import Keyword_Lookup
from app.Ai_Cache import Get_Cached_Category, Save_To_Cache
from app.Ai_Agent import Ask_Ai_For_Category

def Categorize_Merchant(Merchant_text):
    Merchant_upper = Merchant_text.strip().upper()
    Min_Substring_Length = 5

    if Merchant_upper in Merchant_Category_Map: #Layer1 exact dictionary match
        return Merchant_Category_Map[Merchant_upper], "dictionary"
    
    for Known_Merchant, Category in Merchant_Category_Map.items():
        Known_upper = Known_Merchant.upper()
        if len(Known_upper) < Min_Substring_Length:
            continue
        if Known_upper in Merchant_upper or Merchant_upper in Known_upper:
            return Category, "dictionary_partial"
    
    Keyword_Result = Keyword_Lookup(Merchant_text)
    if Keyword_Result: #Layer2 keyword look match
        return Keyword_Result, "keyword"
    
    Cached_Category = Get_Cached_Category(Merchant_upper)
    if Cached_Category:
        return Cached_Category, "Ai_Cache"
    
    Ai_Category = Ask_Ai_For_Category(Merchant_text)
    if Ai_Category:
        Save_To_Cache(Merchant_upper, Ai_Category)
        return Ai_Category, "Ai_Agent"
    
    return "Unknown", "unresolved"


if __name__ == "__main__":
    Test_Merchants = ["CARREFOUR", "كارفور", "UBER", "SEOUDI SUPERMARKET NASR CITY", "Mahmoud El Far", "Some Random New Shop XYZ", "DIdi"]

    for Merchant in Test_Merchants:
        Category, Source = Categorize_Merchant(Merchant)
        print(f"{Merchant!r:45} --> {Category:15} (via {Source})")