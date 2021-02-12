from selenium import webdriver
import os
import pyautogui
from time import sleep
import configparser

config = configparser.ConfigParser()
config.read('setings.ini')

def updateRedlink():
    path = r'C:\\Users\\asgard_48\\Documents\\Skrypty\\auto_maile_handlowcow_redlink\\listymailingowe'
    lista_plikow_csv = os.listdir(path)

    l = 'asgard'
    h = config.get('redlink','pass')
    redlink_url = 'https://redlink.pl/appNew/panel/Login.aspx'
    import_url = 'https://redlink.pl/appNew/panel/Contacts/Import.aspx'
    chrome = webdriver.Chrome(r'C:\Users\asgard_48\Documents\chromedriver_win32\chromedriver.exe')
    chrome.get(redlink_url)
    chrome.maximize_window()
    chrome.find_element_by_id('txtLogin').send_keys(l)
    chrome.find_element_by_name('txtPassword').send_keys(h)
    chrome.find_element_by_id('btnLogin').click()

    for plik_do_wgrania in lista_plikow_csv:
        path = os.path.abspath(path)
        nazwa_grupy = plik_do_wgrania.split('.')[0]
        chrome.get(import_url)
        chrome.find_element_by_id('my-awesome-dropzone').click()
        sleep(1)
        pyautogui.write(f'{path}\\{plik_do_wgrania}')
        pyautogui.press('enter')
        sleep(1)
        chrome.find_element_by_id('MainContent_btnAddColumnMap').click()
        chrome.find_element_by_xpath('/html/body/form/div[3]/div/div[3]/div/div/div/div/div/div[2]/div[4]/div[2]/div[3]/ul/li[2]/a').click()
        sleep(1)
        chrome.find_element_by_xpath('//*[@id="lrbGroupList"]/div').click()
        chrome.find_element_by_id('MainContent_ddlGroups_chosen').click()
        pyautogui.write(nazwa_grupy)
        chrome.find_element_by_class_name('active-result').click()
        chrome.find_element_by_xpath('//*[@id="lrbUpdateContactToGroup"]/div').click()
        chrome.find_element_by_xpath('//*[@id="form"]/div[3]/ul/li[3]/a').click()
        sleep(1)

    chrome.close()

if __name__ == "__main__":
    updateRedlink()