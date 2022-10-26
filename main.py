import discord
from discord.ui import Button, View
from discord.ext import commands
import youtube_dl
import asyncio
from youtube_search import YoutubeSearch
import time
import random
from discord import app_commands



intents = discord.Intents.all()

bot = commands.Bot(intents=intents, command_prefix=';', help_command=None)

lockbot_status = True
remove_all_status = True
remove_all_code = 0
num = 0
i = 0
playlist = []
loop_status = False
now_num = 0
select_num = 0
select_num_int = 0
page_control_num_int = 0

def set_Embed(title='', description=''):
    return discord.Embed(title=title, description=description)

@bot.event
async def on_ready():
    print('logged in as \nname: {}\n  id: {}'.format(bot.user.name, bot.user.id))
    print('=' * 80)

    game = discord.Game("코딩 수정")
    await bot.change_presence(status=discord.Status.online, activity=game)


# @bot.event
# async def is_playing():
#     global voice
#     global i
#     voice = bot.voice_clients[0]
#     if voice.is_playing() and voice.is_paused():
#         print("노래 실행중")
#     elif not voice.is_playing() and not voice.is_paused():
#         print("노래 실행중 아님")
#     else:
#         print("on_voice_state_update ERROR!!!!!")

@bot.command()
async def clear_hidden(ctx, amount: int):
    if ctx.author.id == 389398074184695808 or ctx.author.id == 348285753245302785:
        await ctx.channel.purge(limit=amount + 1)
        print('{0}개의 대화내용을 삭제했습니다.'.format(amount))
    else:
        print('{} is Attempt "clear_hidden" command'.format(ctx.author))
        await ctx.send("Permission Deny")

@bot.command()
async def clearkkk(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    print('{0}개의 대화내용을 삭제했습니다.'.format(amount))

@bot.command(pass_context=True)
async def admin_help(ctx):
    if ctx.author.id == 389398074184695808:
        embed = discord.Embed(title="시윤이의 실험실 봇 명령어", description="모든 명령어 앞에 ; 붙이셈")
        embed.add_field(name="관리자 명령어",
                        value="lockbot : 봇잠금/잠금풀기\nlockbotst : 봇잠금상태\nloop_st : loop 상태 확인\nrestart : 봇 초기화\nsiyunsave siyuns : 파일은 main.py와 같은 경로, 플레이리스트 저장\nsiyunload siyuns : 파일은 main.py와 같은 경로, 플레이리스트 불러오기\nclear_hidden : 대화내용 삭제",
                        inline=False)
        await ctx.channel.send("administrator!! permission allow!!", embed=embed)
    else:
        print('{} is Attempt "admin_help" command'.format(ctx.author))
        await ctx.send("Permission Deny")

@bot.command()
async def var_st(ctx):
    global lockbot_status
    global remove_all_status
    global remove_all_code
    global num
    global i
    global playlist
    global loop_status
    global now_num
    global select_num
    global select_num_int
    print("lockbot_status : ", lockbot_status)
    print("remove_all_status : ", remove_all_status)
    print("remove_all_code : ", remove_all_code)
    print("num : ", num)
    print("i : ", i)
    print("playlist : ", playlist)
    print("loop_status : ", loop_status)
    print("now_num : ", now_num)
    print("select_num : ", select_num)
    print("select_num_int : ", select_num_int)

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="시윤이의 실험실 봇 명령어", description="모든 명령어 앞에 ; 붙이셈")
    embed.add_field(name="입장 명령어", value="c : 봇입장\nf : 봇퇴장", inline=False)
    embed.add_field(name="노래 명령어1", value="a : 노래 추가\np : 노래재생 (음성채널에 봇이 없는경우 자동 입장)\nq : 재생목록\nnow : 현재노래",
                    inline=False)
    embed.add_field(name="노래 명령어2",
                    value="rm [번호] : 번호에 해당하는 노래 삭제\nrma : 모든 노래 삭제\nloop : 반복재생 on/off\nps : 일시정지\nr : 일시정지 풀기",
                    inline=False)
    await ctx.channel.send("귀찮은데...", embed=embed)


# @bot.command(pass_context=True)
# async def p(ctx):
#     await ctx.channel.send(ctx.author.avatar_url)

@bot.command(pass_context=True)
async def f(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        await ctx.channel.send("shit!")
        await bot.voice_clients[0].disconnect()
        await restart
        await rma
    else:
        await ctx.send("bot is locked by administrator")


@bot.command(pass_context=True)
async def c(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        try:
            global i
            global remove_all_code
            global num
            global playlist
            i = 0
            remove_all_code = 0
            num = 0
            playlist = [[]]
            channel = ctx.author.voice.channel
            if not channel:
                await ctx.send("Error : Connect to voice channel")
                return
            else:
                print(ctx.author.voice.channel)
                print("↑ 입장함")
                await ctx.author.voice.channel.connect()
        except:
            await ctx.send("connect Error")
    else:
        await ctx.send("bot is locked by administrator")


# @bot.command()
# async def song_start(voice, i):
#     try:
#         if not voice.is_playing() and not voice.is_paused():
#             ydl_opts = {'format': 'bestaudio'}
#             FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
#                               'options': '-vn'}
#             with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(f'https://www.youtube.com{playlist[i][1]}', download=False)
#                 URL = info['formats'][0]['url']
#
#             voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#
#         while voice.is_playing() or voice.is_paused():
#             await asyncio.sleep(0.1)
#     except:
#         print("FFMPEG_ERROR!!!")
#         return

@bot.command()
async def whoisenemy(ctx):
    await ctx.send("우리의 주적은 짱승과 빡스")

@bot.command()
async def song_start(voice, i):
    try:
        if not voice.is_playing() and not voice.is_paused():
            ydl_opts = {'format': 'bestaudio'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f'https://www.youtube.com{playlist[i][1]}', download=False)
                URL = info['formats'][0]['url']

            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(0.1)
    except:
        print("FFMPEG_ERROR")
        return


@bot.command()
async def restart(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        bot.voice_clients[0].stop()
        global i
        global remove_all_status
        global remove_all_code
        global num
        global now_num
        global loop_status
        global select_num
        i = 0
        remove_all_status = True
        remove_all_code = 0
        num = 0
        i = 0
        loop_status = False
        now_num = 0
        select_num = 0
        await ctx.send("초기화함")
    else:
        await ctx.send("bot is locked by administrator")


@bot.command()
async def a(ctx, *, keyword):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        try:
            global num
            global playlist
            global select_num_int
            selectlist = []
            results = YoutubeSearch(keyword, max_results=5).to_dict()
            for results_num in range(5):
                selectlist.append([results[results_num]['title'], results[results_num]['url_suffix']])
            queText = ''
            for selectlist_num in range(5):
                try:
                    queText = f'{queText}\n' + f'{selectlist_num + 1}. {selectlist[selectlist_num][0]}'
                except:
                    del selectlist[selectlist_num]
            await ctx.send(embed=set_Embed(title='리스트', description=f"{queText}"))
            await ctx.send("숫자만 입력하셈")
            while True:
                def check(m):
                    return m.author == ctx.message.author and m.channel == ctx.message.channel

                try:
                    select_num = await bot.wait_for('message', check=check, timeout=100)
                except asyncio.TimeoutError:
                    await ctx.send(f'시간초과로 다시입력하셈')
                else:
                    select_num_int = int(select_num.content)
                if select_num_int > 0 and select_num_int < 6:
                    break
                else:
                    return
            playlist.append([selectlist[select_num_int - 1][0], selectlist[select_num_int - 1][1]])
            await ctx.send(embed=set_Embed(title='노래 추가', description=f"{results[select_num_int - 1]['title']}"))
            print(playlist)
            print(playlist[num][0] + " ** 추가")
            num += 1
            await clearkkk(ctx, 4)
        except:
            await ctx.send("add song Error")
    else:
        await ctx.send("bot is locked by administrator")

@bot.command()
async def loop_st(ctx):
    global loop_status
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        if loop_status == True:
            await ctx.send("loop on")
        else:
            await ctx.send("loop off")
    else:
        await ctx.send("bot is locked by administrator")

@bot.command()
async def loop(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        global loop_status
        if loop_status == True:
            loop_status = False
            await ctx.send("전체 반복재생 끄기")
        else:
            loop_status = True
            await ctx.send("전체 반복재생 켜기")
    else:
        await ctx.send("bot is locked by administrator")


@bot.command()
async def now(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        global playlist
        global now_num
        await ctx.send(embed=set_Embed(title='현재노래', description=f"{playlist[now_num][0]}"))
    else:
        await ctx.send("bot is locked by administrator")


@bot.command()
async def p(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        try:
            global playlist
            global i

            channel = ctx.author.voice.channel
            if bot.voice_clients == []:
                await channel.connect()

            voice = bot.voice_clients[0]
            if not voice.is_playing() and not voice.is_paused():
                while True:
                    global remove_all_status
                    global loop_status
                    global now_num
                    if not voice.is_playing() and not voice.is_paused() and i < len(
                            playlist) and remove_all_status == True:
                        print(playlist[i][0] + " **** play")
                        now_num = i
                        await song_start(bot.voice_clients[0], i)
                        i += 1
                    elif not voice.is_playing() and not voice.is_paused() and remove_all_status == False:
                        remove_all_status = True
                        i = remove_all_code
                        now_num = i
                        print(playlist[i][0] + " **** play")
                        await song_start(bot.voice_clients[0], i)
                        i += 1
                        remove_all_code = 0
                    elif loop_status == True:
                        i = 0
                        await ctx.send("처음부터 다시시작 ~")
                        continue
                    else:
                        i = 0
                        await ctx.send("노래 끝났음 ~")
                        break
        except:
            await ctx.send("Play Error")
    else:
        await ctx.send("bot is locked by administrator")


@bot.command()
async def q(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        global playlist
        global page_num
        global playlist_range
        global total_num
        global page_num_5
        page_num = 1
        playlist_range = len(playlist)
        total_num = (playlist_range // 10) + 1
        try:
            while True:
                page_num_5 = (page_num - 1) * 10
                queText = ''
                for title in range(10):
                    try:
                        queText = f'{queText}\n' + f'{title + page_num_5 + 1}. {playlist[title + page_num_5][0]}'
                    except:
                        break

                await ctx.send(embed=set_Embed(title='플레이리스트', description=f"{queText}"))
                if page_num == 1 and page_num == total_num:
                    await ctx.send("{}/{}페이지\t그만보기 : 3".format(page_num, total_num))
                elif page_num == 1:
                    await ctx.send("{}/{}페이지\t다음페이지 : 2\t그만보기 : 3".format(page_num, total_num))
                elif page_num == total_num:
                    await ctx.send("{}/{}페이지\t이전페이지 : 1\t그만보기 : 3".format(page_num, total_num))
                else:
                    await ctx.send("{}/{}페이지\t이전페이지 : 1\t다음페이지 : 2\t그만보기 : 3".format(page_num, total_num))

                def check(m):
                    return m.author == ctx.message.author and m.channel == ctx.message.channel

                try:
                    page_control_num = await bot.wait_for('message', check=check, timeout=100)
                except asyncio.TimeoutError:
                    await ctx.send(f'시간초과로 다시입력하셈')
                else:
                    page_control_num_int = int(page_control_num.content)
                if page_control_num_int > 0 and page_control_num_int < 4:
                    if page_control_num_int == 1:
                        page_num -= 1
                        await clearkkk(ctx, 2)
                    elif page_control_num_int == 2:
                        page_num += 1
                        await clearkkk(ctx, 2)
                    elif page_control_num_int == 3:
                        page_num = 1
                        await clearkkk(ctx, 2)
                        break
                    else:
                        await clearkkk(ctx, 2)
                        await ctx.send("뭔가 잘못됨")
                        continue
                else:
                    print("page control error")
        except:
            await ctx.send("selector error!!!!!!!!!")
            pass
    else:
        await ctx.send("bot is locked by administrator")


@bot.command()
async def rma(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        global playlist
        global i
        global num
        global remove_all_status
        global remove_all_code
        await ctx.send("Remove Que all")
        if not bot.voice_clients == []:
            voice = bot.voice_clients[0]
            if not voice.is_playing() and not voice.is_paused():
                playlist = [[]]
            else:
                song_info = playlist[i][i]
                playlist = [[]]
                results = YoutubeSearch(song_info, max_results=1).to_dict()
                playlist.append([results[0]['title'], results[0]['url_suffix']])
            i = 1
            remove_all_code = i
            num = 1
            remove_all_status = False
            time.sleep(0.5)
            await q(ctx)
        else:
            i = 1
            remove_all_code = i
            num = 1
            playlist = [[]]
            await q(ctx)
        print("remove all")
    else:
        await ctx.send("bot is locked by administrator")


@bot.command()
async def rm(ctx, arg):
    global lockbot_status
    global i
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        try:
            global playlist
            remove_song = playlist[int(arg) - 1][0]
            del (playlist[int(arg) - 1])
            i = i - 1
            if (i + 1) == int(arg) - 1:
                bot.voice_clients[0].stop()
            await ctx.send(embed=set_Embed(title='노래 삭제', description=f"{remove_song}"))
            await q(ctx)
            print("{}번째 노래 삭제".format(arg))
        except:
            await ctx.send('노래 제거 중 오류 발생!')
    else:
        await ctx.send("bot is locked by administrator")


@bot.command()
async def s(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        try:
            global i
            global now_num
            i = now_num
            bot.voice_clients[0].stop()
        except:
            await ctx.send("Skip Error")
    else:
        await ctx.send("bot is locked by administrator")


@bot.command()
async def ps(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        try:
            bot.voice_clients[0].pause()
        except:
            await ctx.send("Pause Error")
    else:
        await ctx.send("bot is locked by administrator")


@bot.command()
async def lockbot(ctx):
    if ctx.author.id == 389398074184695808:
        global lockbot_status
        if lockbot_status == True:
            lockbot_status = False
            print("bot is lock")
            await ctx.send("bot is lock")
        elif lockbot_status == False:
            lockbot_status = True
            print("bot is unlock")
            await ctx.send("bot is unlock")
    else:
        print('{} is Attempt "lockbot" command'.format(ctx.author))
        await ctx.send("Permission Deny")

@bot.command()
async def lockbotst(ctx):
    if ctx.author.id == 389398074184695808:
        global lockbot_status
        if lockbot_status == True:
            await ctx.send("bot is unlock")
        elif lockbot_status == False:
            await ctx.send("bot is lock")
    else:
        print('{} is Attempt "lockbotst" command'.format(ctx.author))
        await ctx.send("Permission Deny")


# @bot.command()
# async def sel(ctx, arg):
#     global i

@bot.command()
async def r(ctx):
    global lockbot_status
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        try:
            bot.voice_clients[0].resume()
        except:
            await ctx.send("Resume Error")
    else:
        await ctx.send("bot is locked by administrator")


@bot.command()
async def siyunsave(ctx, *, arg):
    if ctx.author.id == 389398074184695808:
        with open(f'./{arg}.txt', 'w', encoding='UTF-8') as f:
            global playlist
            f.write(str(playlist))
            print('{}.txt file save success'.format(arg))
    else:
        print('{} is Attempt "siyunsave" command'.format(ctx.author))
        await ctx.send("Permission Deny")


@bot.command()
async def siyunload(ctx, *, arg):
    if ctx.author.id == 389398074184695808:
        with open(f'./{arg}.txt', 'r', encoding='UTF-8') as f:
            global playlist
            playlist = eval(f.read())
            print('{}.txt file load success'.format(arg))
    else:
        print('{} is Attempt "siyunload" command'.format(ctx.author))
        await ctx.send("Permission Deny")


@bot.command()
async def tts(ctx, *, arg):
    if lockbot_status == True or ctx.author.id == 389398074184695808:
        try:
            await ctx.channel.send(arg, tts=True)
        except:
            await ctx.send("TTS Error")
    else:
        await ctx.send("bot is locked by administrator")
'''
class hanButton(Button):
    def __init__(self, label, finish_jaum):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)

    async def callback(self, interaction):
        await interaction.response.edit_message(content=, view=None)
'''
@bot.command()
async def 훈민정음(ctx, arg):
    await clearkkk(ctx, 0)
    str="ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ"
    jaum = list(str)
    jaum_title = ''
    merge_jaum = ''
    char_range_var = int(arg)
    for char_range_num in range(char_range_var):
        random.shuffle(jaum)
        merge_jaum = f'{merge_jaum}' + f'{jaum[1]}'
    jaum_title = "랜덤 "+f'{char_range_var}'+"글자 훈민정음"
    await ctx.send(embed=set_Embed(title=f"{jaum_title}", description=f"{merge_jaum}"))


# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def korean_to_be_englished(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함.
        if '가' <= w <= '힣':
            ## 588개 마다 초성이 바뀜.
            ch1 = (ord(w) - ord('가')) // 588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst.append([w])
    return r_lst

@bot.command()
async def 초성퀴즈(ctx, guelja):
    hanguel2 = ''
    hanguel = korean_to_be_englished(guelja)
    await clearkkk(ctx, 0)
    for guel_num in range(len(guelja)):
        hanguel2 = f'{hanguel2}' + f'{hanguel[guel_num][0]}'
    await ctx.send(embed=set_Embed(title=초성퀴즈, description=f"{hanguel2}"))


class GreenButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green)

    async def callback(self, interaction):
        global page_control_num_int
        page_control_num_int = 1
        #await interaction.response.edit_message(content="이전 목록", view=None)

class RedButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.red)

    async def callback(self, interaction):
        global page_control_num_int
        page_control_num_int = 2

        #await interaction.response.edit_message(content="다음 목록", view=None)

class GrayButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.gray)

    async def callback(self, interaction=None):
        global page_control_num_int
        page_control_num_int = 3
        #await interaction.response.edit_message(content="끝내기", view=None)

@bot.command()
async def testbutton(ctx):
    button1 = GreenButton("버튼 Test!")
    button2 = Button(label="Click Test!", style=discord.ButtonStyle.red)

    view = View()
    view.add_item(button1)
    view.add_item(button2)
    await ctx.send(view=view)

@bot.command()
async def l(ctx, arg):
    ipchal4 = int(arg) * 64.78 / 100
    ipchal8 = int(arg) * 75.56 / 100
    ipchal_title = "경매 " + f'{arg}' + "원 입찰가"
    text_ipchal = "4인 / " + f'{int(ipchal4)}\n' + "8인 / " + f'{int(ipchal8)}'
    await ctx.send(embed=set_Embed(title=f"{ipchal_title}", description=f"{text_ipchal}"))

token = open("token", "r").readline()
bot.run(token)
