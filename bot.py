import PySimpleGUI as sg
from botcity.web import WebBot, Browser, By
from webdriver_manager.firefox import GeckoDriverManager
import openpyxl
import pandas as pd

class Youtube():
    def main(self):
        sg.theme('DarkBlue13')  # Escolha o tema desejado

        layout = [
            [sg.Text("Digite sua pesquisa:", font=("Helvetica", 14))],
            [sg.InputText(key='pesquisa', font=("Helvetica", 12), size=(50, 1))],
            [sg.Text("Número de tentativas:", font=("Helvetica", 14))],
            [sg.Combo(values=list(range(1, 21)), default_value=1, key='tentativas', font=("Helvetica", 12))],
            [sg.Button("Iniciar", font=("Helvetica", 12), size=(10, 1)), sg.Button("Cancelar", font=("Helvetica", 12), size=(10, 1))]
        ]

        window = sg.Window("Youtube Scraper", layout, icon="youtube_icon.ico", finalize=True)  # Adicione um ícone se desejar

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Cancelar":
                break
            if event == "Iniciar":
                self.configuracao_nav()
                self.acessando_tela_youtube("https://www.youtube.com/")
                self.pesquisar_assunto(values['pesquisa'])
                self.iniciar_excel()  

                tentativa = 1
                while tentativa <= values['tentativas']:
                    if not self.resgate_informacao(tentativa):
                        values['tentativas'] += 1
                    tentativa += 1
                    if tentativa > values['tentativas']:  
                        break
                
                self.salvar_excel() 
                self.bot.stop_browser()
                sg.popup("Dados coletados com sucesso e salvos em 'youtube_data.xlsx'!", title="Sucesso", font=("Helvetica", 12))
                break

        window.close()

    def configuracao_nav(self):
        self.bot = WebBot()
        self.bot.browser = Browser.FIREFOX
        self.bot.driver_path = GeckoDriverManager().install()
        self.bot.headless = False

    def acessando_tela_youtube(self, link):
        self.bot.browse(link)
        self.bot.maximize_window()

    def pesquisar_assunto(self, pesquisa):
        self.bot.find_element('logo-icon', By.ID).click()
        self.bot.wait(3200)
        self.bot.find_element('search-form', By.ID).click()
        self.bot.type_keys(pesquisa)
        self.bot.enter()
        self.bot.wait(2500)

    def resgate_informacao(self, tentativa):
        try:
            canal = self.bot.find_element(f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{tentativa}]/div[1]/div/div[2]/ytd-channel-name/div/div/yt-formatted-string/a', By.XPATH).text
            nome_do_video = self.bot.find_element(f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{tentativa}]/div[1]/div/div[1]/div/h3/a/yt-formatted-string', By.XPATH).text
            visualizacao = self.bot.find_element(f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{tentativa}]/div[1]/div/div[1]/ytd-video-meta-block/div[1]/div[2]/span[1]', By.XPATH).text
            link = self.bot.find_element(f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{tentativa}]/div[1]/div/div[1]/div/h3/a', By.XPATH).get_attribute('href')
            data, descricao = self.resgatar_likes_deslikes(link)

            if not self.verificar_duplicados(nome_do_video, link):
                self.adicionar_ao_excel(canal, nome_do_video, visualizacao, link, data, descricao)
                return True
            return False

        except Exception as e:
            print(f"Erro ao resgatar informações: {e}")
            return False

    def resgatar_likes_deslikes(self, link):
        self.bot.navigate_to(link)
        data = self.bot.find_element('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-watch-info-text/div/yt-formatted-string/span[3]', By.XPATH).text
        descricao = self.bot.find_element('description-inner', By.ID).text.replace('\n', '').strip().split("TranscriptFollow")[0]
        self.bot.back()
        return data, descricao

    def iniciar_excel(self):
        try:
            self.df = pd.read_excel('youtube_data.xlsx')
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=["Canal", "Nome do Video", "Visualizações", "Link", "Data", "Descrição"])
    
    def verificar_duplicados(self, nome_do_video, link):
        return not self.df[(self.df['Nome do Video'] == nome_do_video) & (self.df['Link'] == link)].empty

    def adicionar_ao_excel(self, canal, nome_do_video, visualizacao, link, data, descricao):
        novo_dado = pd.DataFrame([[canal, nome_do_video, visualizacao, link, data, descricao]], columns=["Canal", "Nome do Video", "Visualizações", "Link", "Data", "Descrição"])
        self.df = pd.concat([self.df, novo_dado], ignore_index=True)

    def salvar_excel(self):
        self.df.to_excel("youtube_data.xlsx", index=False)

if __name__ == '__main__':
    yt = Youtube()
    yt.main()
