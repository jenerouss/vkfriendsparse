import tok
import datetime
import os
import requests
import vk_api
import vk_api.longpoll
from bs4 import BeautifulSoup
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from time import sleep
from winotify import Notification, audio
from os import getcwd
from random import randint
tg_token = tok.token['TG']
bot = Bot(token=tg_token)
dp = Dispatcher(bot)
vk_token = tok.token['VK']


@dp.message_handler()
async def sender(text):
    while True:
        try:
            await bot.send_message(chat_id='501209907', text=text)
        except Exception as e:
            print(e)
            await send_win_notification(title1="Парсинг друзей вк", desc1='Ошибка: ' + str(e))
            sleep(1)
        break


async def send_win_notification(title1, desc1):
    toast = Notification(app_id=f"{randint(0, 100)}",
                         title=title1,
                         msg=desc1,
                         duration="short",
                         icon=getcwd() + "\pyc.ico")
    toast.set_audio(audio.Mail, loop=False)
    toast.show()


async def parsevk():
    while True:
        try:
            time = str(datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))
            session = vk_api.VkApi(token=vk_token)
            vkapi = session.get_api()
            friends = session.method('friends.get')
            number = str(friends['count'])
            items = str(friends['items'])
            with open(time + '.conf', 'a', newline='\n', encoding='utf-8') as file:
                file.write(f'friends:[{number}]\nitems:')
                file.write(items)
        except Exception as e:
            print('Ошибка: ' + str(e) + '\nДелаю еще одну попытку...')
            await send_win_notification(title1="Парсинг друзей вк", desc1='Ошибка: ' + str(e) + '\nДелаю еще одну попытку...')
            sleep(1)
            continue
        break
    return


async def getfriends(id):
    while True:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                "Accept-Encoding": "*",
                "Connection": "keep-alive"
            }
            url = f'https://vk.com/id{id}'
            api = requests.get(url, timeout=20, headers=headers)
            soup = BeautifulSoup(api.text, 'lxml')
            name = soup.find("title")
        except Exception as e:
            print('Ошибка: ' + str(e) + '\nДелаю еще одну попытку...')
            await send_win_notification(title1="Парсинг друзей вк", desc1='Ошибка: ' + str(e) + '\nДелаю еще одну попытку...')
            sleep(1)
            continue
        return name.text[:-12]


async def getfiles(debug):
    files = os.listdir()
    filenames = []
    x = 0
    for i in range(len(files) - 1):
        try:
            if len(files[i]) > 5:
                if (files[i][-5] == '.' and files[i][-4] == 'c' and files[i][-3] == 'o' and files[i][-2] == 'n' and
                        files[i][-1] == 'f'):
                    x += 1
                    forsplit = files[i].rsplit('.')
                    filenames.append(''.join(forsplit[0]))
                    if debug == '1':
                        print(files[i])
        except Exception as e:
            print("Ошибка: " + str(e))
            await send_win_notification(title1="Парсинг друзей вк", desc1='Ошибка: ' + str(e))
            continue
    slicedfilenames = filenames.copy()
    for i in range(len(slicedfilenames)):
        check = False
        for j in range(len(slicedfilenames[i])):
            if slicedfilenames[i][j] == '-':
                check = True
        if check:
            slovo = slicedfilenames[i].split('-')
            slovo = ''.join(slovo)
            slicedfilenames[i] = slovo
    if x > 2:
        for i in range(len(slicedfilenames)):
            if slicedfilenames[i] != max(slicedfilenames):
                if debug == '1':
                    print('max != ' + str(filenames[i]) + ' id = ' + str(i))
                os.remove(filenames[i] + '.conf')
                if debug == '1':
                    print('removed')
                break
    if debug == '1':
        print(str(slicedfilenames) + ' sliced\n' + str(filenames))
    for i in range(len(slicedfilenames)):
        if slicedfilenames[i] == max(slicedfilenames):
            r = open(filenames[i] + '.conf', "r", encoding='utf-8').read()
            rr = open(filenames[i-1] + '.conf', "r", encoding='utf-8').read()
            return r, rr

async def fileworkvk(debug):
    time = str(datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))
    names, oldnames = await getfiles(debug=0)
    count = ''
    qw = False
    for s in range(len(names)):
        if names[s] == 'd':
            s += 4
            for i in range(s, len(names)):
                if names[i] == ']':
                    qw = True
                    break
                if names[i] != ',' and names[i] != ' ':
                    count += ''.join(names[i])
        if qw:
            break
    friends = []
    friendsstr = ''
    qq = False
    for k in range(len(names)):
        if names[k] == 'm':
            k += 4
            for i in range(k, len(names)):
                if names[i] == ']':
                    friends.append(friendsstr)
                    qq = True
                    break
                if names[i] == ',':
                    friends.append(friendsstr)
                    friendsstr = ''
                    continue
                if names[i] != ' ':
                    friendsstr += ''.join(names[i])
        if qq:
            break
    oldcount = ''
    qw = False
    for s in range(len(oldnames)):
        if oldnames[s] == 'd':
            s += 4
            for i in range(s, len(oldnames)):
                if oldnames[i] == ']':
                    qw = True
                    break
                if oldnames[i] != ',' and oldnames[i] != ' ':
                    oldcount += ''.join(oldnames[i])
        if qw:
            break
    oldfriends = []
    oldfriendsstr = ''
    qq = False
    for k in range(len(oldnames)):
        if oldnames[k] == 'm':
            k += 4
            for i in range(k, len(oldnames)):
                if oldnames[i] == ']':
                    oldfriends.append(oldfriendsstr)
                    qq = True
                    break
                if oldnames[i] == ',':
                    oldfriends.append(oldfriendsstr)
                    oldfriendsstr = ''
                    continue
                if oldnames[i] != ' ':
                    oldfriendsstr += ''.join(oldnames[i])
        if qq:
            break
    for i in range(len(friends) - 1):
        for j in range(len(oldfriends) - 1):
            if friends[i] == oldfriends[j]:
                break
        else:
            await sender(text= f'Добавление в друзья: {str(await getfriends(friends[i]))}\nhttps://vk.com/id{friends[i]}')
            await send_win_notification(title1="Парсинг друзей вк", desc1= f'Добавление в друзья: {str(await getfriends(friends[i]))}')
    for i in range(len(oldfriends) - 1):
        for j in range(len(friends) - 1):
            if oldfriends[i] == friends[j]:
                break
        else:
            await sender(text= f'Удаление из друзей: {str(await getfriends(oldfriends[i]))}\nhttps://vk.com/id{oldfriends[i]}')
            await send_win_notification(title1="Парсинг друзей вк", desc1= f'Удаление из друзей: {str(await getfriends(oldfriends[i]))}')


async def main(a):
    while True:
        await parsevk()
        await fileworkvk(debug=0)
        sleep(100)

if __name__ == '__main__':
    toast = Notification(app_id=f"{randint(0, 100)}",
                         title="Парсинг друзей вк",
                         msg="Запуск программы",
                         duration="short",
                         icon=getcwd() + "\pyc.ico")
    toast.set_audio(audio.Mail, loop=False)
    toast.show()
    executor.start_polling(dp, skip_updates=True, on_startup=main)
