import requests
import time
import sys

# Configurações MR_BEANS1
TOKEN_TG = "8536212315:AAFV9jLLfYEpB4J0GjrRN3ybeBQHjUWGh3c"
CHAT_ID = "8410443642"
MAX_PRICE = 100000

NODES = ["https://eos.greymass.com", "https://api.main.alohaeos.com"]

def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN_TG}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

print("🚀 SNIPER GITHUB ATIVO - MR_BEANS1", flush=True)
vistas = set()

# Roda por 5 horas (O GitHub Actions permite até 6h por execução)
timeout = time.time() + 60*60*5 

while time.time() < timeout:
    for node in NODES:
        try:
            payload = {"account_name": "uplandmarket", "pos": -1, "offset": -50}
            r = requests.post(f"{node}/v1/history/get_actions", json=payload, timeout=10)
            
            if r.status_code == 200:
                actions = r.json().get("actions", [])
                if not actions:
                    print("⚠️ Sem ações recentes no nó...", flush=True)
                
                for action in reversed(actions):
                    seq = action.get("global_action_seq")
                    if seq not in vistas:
                        vistas.add(seq)
                        if len(vistas) > 1000: vistas.clear() # Limpa cache para não pesar
                        
                        act = action.get("action_trace", {}).get("act", {})
                        if act.get("name") in ["listprop", "updateprop", "n1", "n2"]:
                            data = act.get("data", {})
                            p_raw = data.get("price") or data.get("amount") or "0"
                            try:
                                price = float(str(p_raw).split()[0])
                                if 0 < price <= MAX_PRICE:
                                    prop_id = data.get("prop_id") or data.get("asset_id")
                                    enviar_telegram(f"⚡ **GITHUB SNIPER: MR_BEANS1**\n💰 Preço: `{price:,.0f}` UPX\n🆔 ID: `{prop_id}`\n🔗 [Upland](https://play.upland.me/p/{prop_id})")
                                    print(f"✅ Alerta enviado: {price} UPX", flush=True)
                            except: continue
                break
        except Exception as e:
            print(f"❌ Erro no nó {node}: {e}", flush=True)
            continue
    
    time.sleep(3) # Intervalo de segurança para o GitHub não banir o IP

print("⏰ Tempo limite atingido. Reiniciando via Cron...", flush=True)

