import keyboard
import pyautogui
import pyperclip
import time
import os

pyautogui.PAUSE=0.6

def adiciona_complemento(item,preco):
    pyautogui.click(1270,432)
    time.sleep(1)
    pyautogui.click(1391,527)
    pyautogui.click(1284,437)
    time.sleep(0.3)
    pyautogui.click(1384,621)
    pyautogui.moveTo(1444, 650, duration=0.3)  # move lentamente
    pyautogui.click()
    pyperclip.copy(item)
    time.sleep(0.3)
    print(pyperclip.paste())
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press('tab')
    if preco == '0':
        for i in range(5):
            pyautogui.press('tab')
        pyautogui.press('enter')
    else:
        print('Ola')           
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.typewrite(preco)
        for i in range(2):
            pyautogui.press('tab')
        pyautogui.press('enter')

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(diretorio_atual, '..', 'data', 'complemento.txt')
def executar():
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    for i, linha in enumerate(linhas, start=1):
        item = "Adicional "+linha.strip()
        preco = '790'                        
        #linha = linha.split('–')
        #item  = "Borda "+linha[0].strip()
        #preco = linha[1].strip()
        adiciona_complemento(item, preco) 

    pyautogui.alert("Pronto")

if __name__ == "__main__":
    executar()