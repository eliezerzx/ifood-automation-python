import time
import os
import pyautogui
import pytesseract
from PIL import Image

# Configurações de segurança do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# --- CAMINHO DA SUA PASTA DE FOTOS ---
CAMINHO_PASTA_FOTOS = r"C:\Users\Master\Downloads\Pizzaria Mazzarelli"

# --- COORDENADAS AJUSTADAS ---
COORDENADAS = {
    # Coordenada do botão retangular vermelho "Adicionar" que fica bem no centro do modal do iFood
    "botao_adicionar_vermelho": (473, 733), 
    # Seu botão original de salvar o modal do iFood
    "botao_salvar_ifood": (684, 874),       
}

def localizar_proximo_icone():
    """Busca o ícone cinza de upload na tela usando reconhecimento de imagem."""
    try:
        # Usa a imagem 'icone_foto.png' salva na mesma pasta do script
        posicao = pyautogui.locateOnScreen('icone_foto.png', confidence=0.8, grayscale=True)
        return posicao
    except pyautogui.ImageNotFoundException:
        return None

def extrair_nome_ingrediente(posicao_icone):
    """Usa a posição do ícone encontrado para definir a área do texto ao lado dele"""
    # Desempacota os valores retornados pelo localizador
    x, y, largura_icone, altura_icone = posicao_icone
    
    # --- A CORREÇÃO ESTÁ AQUI ---
    # Forçamos todos os cálculos a virarem INT (números inteiros puros)
    # Isso evita o erro "region argument must be a tuple of four ints"
    regiao_texto = (
        int(x + largura_icone + 10), 
        int(y), 
        int(200), 
        int(altura_icone)
    )
    
    # Agora o PyAutoGUI aceitará a região perfeitamente
    screenshot = pyautogui.screenshot(region=regiao_texto)
    texto_completo = pytesseract.image_to_string(screenshot, lang='por').strip()
    
    print(f"Texto detectado pelo OCR: '{texto_completo}'")
    
    if not texto_completo:
        return None
        
    partes = texto_completo.split()
    return partes[-1].lower() if partes else None

def processar_pizza(posicao_icone):
    """Executa o processo de upload direto por caminho de arquivo, evitando erros de busca"""
    nome_ingrediente = extrair_nome_ingrediente(posicao_icone)
    if not nome_ingrediente:
        print("Não foi possível ler o nome da pizza. Pulando...")
        return False
        
    print(f"Processando ingrediente: {nome_ingrediente}")
    
    # 1. Clica no ícone cinza encontrado na tela para abrir o modal do iFood
    pyautogui.click(pyautogui.center(posicao_icone))
    time.sleep(1.5)
    
    # 2. Clica no botão vermelho "Adicionar" dentro do modal do iFood
    pyautogui.click(COORDENADAS["botao_adicionar_vermelho"])
    time.sleep(1.5) # Aguarda a janela "Abrir" do Windows aparecer
    
    # 3. Verifica se o arquivo é .jpg ou .png para mandar o caminho correto
    caminho_jpg = os.path.join(CAMINHO_PASTA_FOTOS, f"{nome_ingrediente}.jpg")
    caminho_png = os.path.join(CAMINHO_PASTA_FOTOS, f"{nome_ingrediente}.png")
    
    if os.path.exists(caminho_jpg):
        caminho_final = caminho_jpg
    elif os.path.exists(caminho_png):
        caminho_final = caminho_png
    else:
        # Se não achar nenhuma das duas extensões, tenta enviar como .jpg mesmo assim
        caminho_final = caminho_jpg
    
    print(f"Enviando arquivo exato: {caminho_final}")
    
    # 4. Escreve o caminho completo diretamente na caixa de diálogo do Windows
    pyautogui.write(caminho_final)
    pyautogui.press('enter')
    time.sleep(2.0) # Aguarda o processamento do upload da imagem no site
    
    # 5. Clica no botão vermelho "Salvar" do iFood
    pyautogui.click(COORDENADAS["botao_salvar_ifood"])
    time.sleep(1.5) # Aguarda o modal fechar e voltar para a lista principal
    return True

def executar_automacao_inteligente():
    print("Iniciando em 5 segundos... Certifique-se de que o iFood está visível!")
    time.sleep(5)
    
    while True:
        print("\n[Verificação 1] Procurando ícone de imagem na tela...")
        posicao_icone = localizar_proximo_icone()
        
        if posicao_icone:
            # Se encontrou o ícone, faz o processo completo de upload
            processar_pizza(posicao_icone)
            time.sleep(0.5) 
        else:
            # Regra de dupla verificação com Scroll automático
            print("[Aviso] Nenhum ícone visível. Dando scroll para tentar novamente...")
            
            # Move o mouse para o lado esquerdo (iFood) para garantir o foco da rolagem
            pyautogui.moveTo(400, 500)
            pyautogui.scroll(-400) # Rola a página para baixo
            time.sleep(1.5) # Aguarda a página carregar/estabilizar
            
            print("[Verificação 2] Procurando novamente após o scroll...")
            posicao_icone_pos_scroll = localizar_proximo_icone()
            
            if posicao_icone_pos_scroll:
                print("Ícone encontrado após o scroll! Retomando o processo...")
                processar_pizza(posicao_icone_pos_scroll)
                time.sleep(0.5)
            else:
                # Fim do loop caso o segundo teste falhe (fim da página do cardápio)
                print("🛑 Fim do cardápio! Nenhum ícone encontrado após o scroll. Encerrando programa.")
                break

if __name__ == "__main__":
    executar_automacao_inteligente()