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


def monta_tabela(tabela):
    cabecalho = 'Classificação\t\t  \tPG\t\t\tJ\t\t\tV\t\t\tE\t\t\tD\t\t\tGP\t\t\tGC\t\t\tSG\t\t\t%\n'
    tabelaStr = ''
    for i in range(20):
        if i < 9:
            tabelaStr += f'{tabela[i].posicao}  {tabela[i].abreviatura}\t\t\t\t\t{tabela[i].pg}\t\t{tabela[i].jogos}\t\t{tabela[i].vitorias}\t\t{tabela[i].empates}\t\t{tabela[i].derrotas}\t\t{tabela[i].golsPro}\t\t{tabela[i].golsContra}\t\t{tabela[i].saldoGols}\t\t{tabela[i].percentual}\n'
        else:
            tabelaStr += f'{tabela[i].posicao} {tabela[i].abreviatura}\t\t\t\t\t{tabela[i].pg}\t{tabela[i].jogos}\t{tabela[i].vitorias}\t{tabela[i].empates}\t{tabela[i].derrotas}\t{tabela[i].golsPro}\t{tabela[i].golsContra}\t{tabela[i].saldoGols}\t{tabela[i].percentual}\n'
    return cabecalho + tabelaStr

def cria_tabela(tabela):
    output = t2a(
        header=["Posição", "Classificação", "PG", "J", "V", "E", "D", "GP", "GC", "SG", "%"],
        body=[[tabela[i].posicao, tabela[i].nome, tabela[i].pg, tabela[i].jogos, tabela[i].vitorias, tabela[i].empates,
               tabela[i].derrotas, tabela[i].golsPro, tabela[i].golsContra, tabela[i].saldoGols, tabela[i].percentual]
              for i in range(20)],
        style=PresetStyle.thin_compact
    )

    return output


# times = info_times()

# tabela = [Time(*times[i]) for i in range(20)]

# print(monta_tabela(tabela))

@bot.command
@lightbulb.command('tabela_brasileirao', 'Bot mostra a classificação do brasileirão')
@lightbulb.implements(lightbulb.SlashCommand)
async def tabelaBot(ctx):
    times = info_times()
    tabela = [Time(*times[i]) for i in range(20)]
    # print(monta_tabela(tabela))
    # await ctx.respond(f'```{monta_tabela(tabela)}```')
    output = t2a(
        header=["Posição", "Classificação", "PG", "J", "V", "E", "D", "GP", "GC", "%"],
        body=[[tabela[0].posicao, tabela[0].nome, tabela[0].pg, tabela[0].jogos, tabela[0].vitorias, tabela[0].empates,
               tabela[0].derrotas, tabela[0].golsPro, tabela[0].golsContra, tabela[0].percentual],
              [tabela[1].posicao, tabela[1].nome, tabela[1].pg, tabela[1].jogos, tabela[1].vitorias, tabela[1].empates,
               tabela[1].derrotas, tabela[1].golsPro, tabela[1].golsContra, tabela[1].percentual]],
        style=PresetStyle.thin_compact
    )

    await ctx.respond(f"```\n{cria_tabela(tabela)}\n```")


bot.run()
