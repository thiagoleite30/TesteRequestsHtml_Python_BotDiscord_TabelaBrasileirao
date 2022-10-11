from requests_html import HTMLSession
import lightbulb
from table2ascii import table2ascii as t2a, PresetStyle

bot = lightbulb.BotApp(token=open('tokens/token_ds.txt', 'r').read(),
                       default_enabled_guilds=(int(open('tokens/ds_channel_id.txt', 'r').read())))

class Time():
    def __init__(self, posicao, nome, abreviatura, pg, jogos, vitorias, empates, derrotas, golsPro, golsContra,
                 saldoGols, percentual):
        self.posicao = posicao
        self.nome = nome
        self.abreviatura = abreviatura
        self.pg = pg
        self.jogos = jogos
        self.vitorias = vitorias
        self.empates = empates
        self.derrotas = derrotas
        self.golsPro = golsPro
        self.golsContra = golsContra
        self.saldoGols = saldoGols
        self.percentual = percentual


def info_times():
    session = HTMLSession()
    requisicao = session.get('https://www.uol.com.br/esporte/futebol/campeonatos/brasileirao/')
    infoTimes = requisicao.html.find('.team')
    times = []
    for i in range(20):
        i += 1
        times.append(infoTimes[i].text.split('\n'))

    timePontos = info_scores()

    for i in range(20):
        for j in range(9):
            times[i].append(timePontos[i][j])
        # print(times[i])

    return times


def info_scores():
    session = HTMLSession()
    requisicao = session.get('https://www.uol.com.br/esporte/futebol/campeonatos/brasileirao/')
    infoTimesScore = requisicao.html.find('.data-table')
    scores = infoTimesScore[1].text.split('\n')
    scores = scores[9:]
    timePontos = []
    for i in range(20):
        timePontos.append(scores[0:9])
        scores = scores[9:]

    return timePontos


def busca_time(tabela, time):
    for i in range(len(tabela)):
        if time.lower() == tabela[i].nome.lower():
            print(f'Tem esse time no indice {i}')
            print(f'{time.lower()} e {tabela[i].nome.lower()}')
            return i
            break
    return -1


def cria_tabela(tabela):
    output = t2a(
        header=["Posição", "Classificação", "PG", "J", "V", "E", "D", "GP", "GC", "SG", "%"],
        body=[[tabela[i].posicao, tabela[i].nome, tabela[i].pg, tabela[i].jogos, tabela[i].vitorias, tabela[i].empates,
               tabela[i].derrotas, tabela[i].golsPro, tabela[i].golsContra, tabela[i].saldoGols, tabela[i].percentual]
              for i in range(20)],
        style=PresetStyle.thin_compact
    )

    return output

#Abaixo inicializamos a conexão com o site UOL e já pegamos todos os times
times = info_times()

#Cria lista tabela com objetos da classe Time que recebem os valores da lista times em seus respectivos atributos
tabela = [Time(*times[i]) for i in range(20)]


@bot.command
@lightbulb.command('tabela_brasileirao', 'Bot mostra a classificação do brasileirão')
@lightbulb.implements(lightbulb.SlashCommand)
async def tabelaBot(ctx):

    await ctx.respond(f"```\n{cria_tabela(tabela)}\n```")


bot.run()

