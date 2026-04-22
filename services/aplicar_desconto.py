import pyautogui
import time
import os
from utils import somErro

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
NOME_IMAGEM = os.path.join(BASE_DIR, "image", "botao_tag.png")

def apli_desconto():
    print("--- INICIANDO AUTOMAÇÃO ---")
    time.sleep(3) # Tempo para mudar de janela

    tentativas_vazias = 0  # Contador para controlar os scrolls e finalização

    while True:
        print("\n🔍 Escaneando a tela em busca de tags cinzas...")
        encontrou_neste_ciclo = False
        
        # Fazemos uma captura de tela uma única vez por ciclo para ganhar velocidade
        try:
            tags = list(pyautogui.locateAllOnScreen(NOME_IMAGEM, confidence=0.7))
        except Exception as e:
            print(f"Erro ao buscar imagem: {e}")
            tags = []

        for box in tags:
            x, y = pyautogui.center(box)
            cor = pyautogui.pixel(int(x), int(y))
            r, g, b = cor

            # --- Lógica de verificação de cor cinza ( R, G, B)
            if abs(r - g) < 10 and abs(g - b) < 10 and abs(r - b) < 10 and g < (r + 15):
                print(f"✅ Tag cinza detectada em ({x}, {y}). Processando...")
                
                # --- 1. Clica na tag cinza
                pyautogui.click(x, y)
                time.sleep(1)

                # --- 2. Clica no campo de valor
                pyautogui.click(1633, 351) 
                time.sleep(0.5)

                # --- 3. Cola o valor
                pyautogui.hotkey("ctrl", "v")
                time.sleep(1)

                # --- 4. Clica em aplicar
                pyautogui.click(1861, 859)
                print("💰 Desconto aplicado!")
                
                encontrou_neste_ciclo = True
                tentativas_vazias = 0 # Resetamos o contador pois algo foi processado
                
                # IMPORTANTE: Após aplicar um, a tela pode mudar. 
                # Damos um break para re-escanear do topo.
                time.sleep(2) 
                break 
        
        if not encontrou_neste_ciclo:
            tentativas_vazias += 1
            
            if tentativas_vazias == 1:
                print("⏬ Nenhuma tag encontrada. Rolando a página para baixo...")
                pyautogui.scroll(-800) 
                time.sleep(2) 
            else:
                # Se for a segunda tentativa seguida sem achar nada, finaliza
                print("💤 Nenhuma tag cinza pendente após scroll.")
                somErro.som_sucesso()
                pyautogui.alert("✅ Descontos finalizado com sucesso!")
                break

if __name__ == "__main__":
    try:
        apli_desconto()
    except KeyboardInterrupt:
        print("\n🛑 Programa encerrado pelo usuário.")
        somErro.som_error()
        pyautogui.alert(f"❌ Programa encerrado pelo usuário.")
