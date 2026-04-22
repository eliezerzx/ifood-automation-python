import pyautogui
import time
import os
from utils import somErro

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
NOME_IMAGEM = os.path.join(BASE_DIR, "image", "botao_verde.png")


def box_valido(box):
    """
    Valida se o tamanho encontrado é parecido com o ícone esperado.
    Ajuste os limites se necessário.
    """
    return (
        10 <= box.width <= 40 and
        10 <= box.height <= 40
    )


def remover_desconto():
    print("--- INICIANDO AUTOMAÇÃO ---")
    time.sleep(3)

    # Se souber a área onde os ícones aparecem, coloque aqui:
    # region = (x, y, largura, altura)
    # Exemplo:
    # region = (1200, 200, 500, 800)
    region = None

    while True:
        print("\n🔍 Escaneando a tela em busca do ícone exato...")
        encontrou_neste_ciclo = False

        try:
            tags = list(pyautogui.locateAllOnScreen(
                NOME_IMAGEM,
                confidence=0.90, # aumente se ainda houver falso positivo
                grayscale=False,
                region=region
            ))
        except Exception as e:
            print(f"Erro ao buscar imagem: {e}")
            tags = []

        if tags:
            print(f"Foram encontrados {len(tags)} ícones.")
        else:
            print("Nenhum ícones encontrado.")

        for box in tags:
            if not box_valido(box):
                print(f"❌ Ignorado: tamanho fora do padrão ({box.width}x{box.height})")
                continue

            x, y = pyautogui.center(box)
            print(f"✅ Ícone encontrado em ({x}, {y}) | tamanho: {box.width}x{box.height}")

            # Clica no ícone exato
            pyautogui.click(x, y)
            time.sleep(1)

            # Clica em remover
            pyautogui.click(1763, 848)
            time.sleep(0.5)

            encontrou_neste_ciclo = True

            # após remover, reescaneia a tela
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
                print("💤 Nenhuma tag verde pendente após scroll.")
                somErro.som_sucesso()
                pyautogui.alert("✅ Descontos removidos com sucesso!")
                break


if __name__ == "__main__":
    try:
        remover_desconto()
    except KeyboardInterrupt:
        print("\n🛑 Programa encerrado pelo usuário.")
        somErro.som_erro()
        pyautogui.alert("❌ Programa encerrado pelo usuário.")