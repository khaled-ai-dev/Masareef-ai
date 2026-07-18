import json
import os

Cache_File_Path = "data/ai_merchant_cache.json"

def _load_cache_from_disk():
    if not os.path.exists(Cache_File_Path):
        return {}
    with open(Cache_File_Path, "r", encoding="utf-8") as f:
        return json.load(f)
    

_Cache = _load_cache_from_disk()

def Get_Cached_Category(Merchant_upper):
    return _Cache.get(Merchant_upper)

def Save_To_Cache(Merchant_upper, Category):
    _Cache[Merchant_upper] = Category
    os.makedirs(os.path.dirname(Cache_File_Path), exist_ok=True)
    with open(Cache_File_Path, "w", encoding="utf-8") as f:
        json.dump(_Cache, f, ensure_ascii=False, indent=2)