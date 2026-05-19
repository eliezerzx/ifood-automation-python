import pyautogui
import pyperclip
import keyboard
import time
from utils import somErro


# Tempo de segurança: se o código der loucura, jogue o mouse para o canto superior esquerdo da tela para parar.
pyautogui.FAILSAFE = True

def editar_produto():
    # 1. Dá um tempo para você clicar na tela do navegador antes de começar
    print("A automação começará em 5 segundos. Clique na página do primeiro produto!")
    time.sleep(5)

    # Defina aqui quantas abas/páginas de produtos você quer alterar
    total_de_produtos = 19 

    for i in range(total_de_produtos):
        print(f"Editando produto {i+1} de {total_de_produtos}...")

        # ----------------------------------------------------
        # PASSO 1: EDITAR O NOME DO PRODUTO
        # ----------------------------------------------------
        # Vamos clicar no campo "Nome". Como a posição pode variar, o ideal é você deixar o mouse
        # posicionado em cima do campo "Nome do Produto" no primeiro produto, ou mapear a coordenada.
        # Para fins práticos, o script assume que você já clicou ou que vai usar o Tab.
        
        # Simulando um clique no início para focar na página (ajuste as coordenadas se necessário)
        pyautogui.click(x=571, y=483) # Exemplo de clique no campo Nome
        
        # Truque: Vamos selecionar tudo no campo Nome, copiar, e reescrever adicionando o sufixo.
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.3)
        
        nome_atual = pyperclip.paste()
        novo_nome = f"{nome_atual} + Coca 1,5l"
        
        pyperclip.copy(novo_nome)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

        # ----------------------------------------------------
        # PASSO 2: EDITAR A DESCRIÇÃO
        # ----------------------------------------------------
        # Pressiona TAB duas vezes para sair do campo Nome e ir para o campo Descrição
        pyautogui.press('tab')
        time.sleep(0.2)

        # Copia o texto atual da descrição
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.2)

        descricao_atual = pyperclip.paste()

        # Limpa o "Foto ilustrativa." antigo se ele existir para não duplicar
        if "Foto ilustrativa." in descricao_atual:
            descricao_limpa = descricao_atual.replace("Foto ilustrativa.", "").strip()
        else:
            descricao_limpa = descricao_atual.strip()

        # Monta a nova descrição inserindo o texto antes de "Foto ilustrativa."
        nova_descricao = f"{descricao_limpa} Acompanha coca-cola 1,5l. Foto ilustrativa."
        
        pyperclip.copy(nova_descricao)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)

        # ----------------------------------------------------
        # PASSO 3: SALVAR AS ALTERAÇÕES
        # ----------------------------------------------------
        # Geralmente o botão de salvar fica fixo embaixo ou você pode usar o TAB até chegar nele.
        # Se o botão "Salvar" aceitar o atalho Ctrl + S na plataforma do iFood, use a linha abaixo:
        # pyautogui.hotkey('ctrl', 's')
        
        # CASO NÃO ACEITE ATALHO: Você precisará mapear onde fica o botão "Salvar" na sua tela.
        # Exemplo (substitua X e Y pelas coordenadas reais do seu botão Salvar):
        pyautogui.click(x=1772, y=982) 
        print("Aguardando salvar...")
        time.sleep(1) # Tempo para a plataforma processar o salvamento

        # ----------------------------------------------------
        # PASSO 4: IR PARA A PRÓXIMA ABA/PÁGINA DO NAVEGADOR
        # ----------------------------------------------------
        # Se você abriu vários produtos em abas diferentes no Chrome/Edge:
        pyautogui.hotkey('ctrl', 'pgdn') # Ctrl + Page Down muda para a próxima aba
        time.sleep(1) # Aguarda a nova aba carregar

        # Opcional: Se precisar clicar novamente no campo Nome da nova aba para reiniciar o ciclo:
        # pyautogui.click(x=500, y=470)
        
    somErro.som_sucesso()
    pyautogui.alert("✅ Cardápio finalizado com sucesso!")


# Executa a função
if __name__ == "__main__":
    editar_produto()