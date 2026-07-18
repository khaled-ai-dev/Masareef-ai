import httpx
import json

Ollama_url = "http://localhost:11434/api/generate"
Ollama_model = "llama3.2"

Current_Categories = ["Groceries", "Transport", "Bills", "Dining", "Entertainment", "Shopping", "Other"]

def Ask_Ai_For_Category(Merchant_text):
    prompt = ("You are a financial transaction categorization assistant for Egypt. "
              "Classify the merchant name below into exactly one of these categories: "
              f"{', '.join(Current_Categories)}. "
              'Respond with ONLY a JSON object like this: {"Category": "Groceries"}. '
              "No explanation, no extra text.\n\n"
              f"Merchant name: {Merchant_text}")
    
    try:
        response = httpx.post(Ollama_url, json={"model": Ollama_model, "prompt": prompt, "stream": False, "format": "json"}, timeout = 30.0)
        response.raise_for_status()
        Result_text = response.json()["response"]
        Parsed = json.loads(Result_text)
        Category = Parsed.get("Category", "").strip()

        if Category in Current_Categories:
            return Category
        return None
    
    except Exception as e:
        print(f"AI Agent unavailable or failed: {e}")
        return None