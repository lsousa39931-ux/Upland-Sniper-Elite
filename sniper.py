import requests
import time
import sys

# Configurações MR_BEANS1
TOKEN_TG = "8536212315:AAFV9jLLfYEpB4J0GjrRN3ybeBQHjUWGh3c"
CHAT_ID = "8410443642"
MAX_PRICE = 100000

# Servidores da Rede EOS (Nodes)
NODES = [
    "https://eos.greymass.com", 
    "https://api.main.alohaeos.com",
    "https://eos.api.eosnation.io"
]

def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN_TG}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print(f"Erro Telegram: {e}", flush=True)

# Mensagem de início no console do GitHub
print("🚀 SNIPER GITHUB ATIVO - MR_BEANS1", flush=True)
print(f"🎯 Monitorando ofertas até {MAX_PRICE} UPX...", flush=True)

vistas = set()

# Define o tempo de funcionamento: 5 horas (300 minutos)
timeout = time.time() + (60 * 60 * 5)

while time.time() < timeout:
    for node in NODES:
        try:
            # Consulta o Ledger do Upland (uplandmarket)
            payload = {"account_name": "uplandmarket", "pos": -1, "offset": -50}
            r = requests.post(f"{node}/v1/history/get_actions", json=payload, timeout=10)
            
            if r.status_code == 200:
                actions = r.json().get("actions", [])
                
                # Analisa as transações da mais nova para a mais antiga
                for action in reversed(actions):
                    seq = action.get("global_action_seq")
                    
                    if seq not in vistas:
                        vistas.add(seq)
                        # Mantém a memória limpa
                        if len(vistas) > 1000: vistas.clear()
                        
                        act = action.get("action_trace", {}).get("act", {})
                        # Filtra ações de listagem (n1, n2, listprop)
                        if act.get("name") in ["listprop", "updateprop", "n1", "n2"]:
                            data = act.get("data", {})
                            
                            # Tenta extrair o preço
                            p_raw = data.get("price") or data.get("amount") or "0"
                            try:
                                price = float(str(p_raw).split()[0])
                                
                                # Se o preço estiver no seu limite, envia o alerta
                                if 0 < price <= MAX_PRICE:
                                    prop_id = data.get("prop_id") or data.get("asset_id")
                                    msg = (
                                        f"⚡ **NOVA OFERTA: MR_BEANS1**\n"
                                        f"💰 Preço: `{price:,.0f}` UPX\n"
                                        f"🆔 ID: `{prop_id}`\n"
                                        f"🔗 [Ver no Upland](https://play.upland.me/p/{prop_id})"
                                    )
                                    enviar_telegram(msg)
                                    print(f"✅ Oferta encontrada: {price} UPX", flush=True)
                            except:
                                continue
                break # Se o node funcionou, pula para o próximo ciclo
        except:
            continue # Se o node falhar, tenta o próximo da lista
    
    # Sinal de vida para o GitHub não derrubar a conexão (imprime um ponto)
    if int(time.time()) % 60 == 0:
        print(".", end="", flush=True)
        
    # Espera 2 segundos antes de checar novamente (Alta Velocidade)
    time.sleep(2)

print("\n⏰ Tempo de 5 horas atingido. Reiniciando via Workflow...", flush=True)
