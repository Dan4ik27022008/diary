import pickle, time, webbrowser, os
#os.remove('data.dat')

days = ['понеділок', 'вівторок', 'середу', 'четвер', 'п\'ятницю']

try:
    with open('data.dat', 'rb') as f:
        maindict = pickle.load(f)
except:
    maindict = {'links': {}, 'nmbr_of_lsns': [], 'bgn_tm': [], 'end_tm': [], 'понеділок': [], 'вівторок': [], 'середу': [], 'четвер': [], 'п\'ятницю': []}
    print('Введіть кількість уроків у')
    for day in days:
        maindict['nmbr_of_lsns'].append(int(input(f'{day}:')))
    
    for day in days:
        print(f'Введіть розклад уроків на {day}')
        for i in range(1, maindict['nmbr_of_lsns'][days.index(day)] + 1):
            maindict[day].append(input(f'{i} урок:'))
    
    for i in range(1, max(maindict['nmbr_of_lsns']) + 1):
        bgn_tm = input(f'Введіть час коли починається {i} урок, у такому вигляді - ГГ:XX\n')
        maindict['bgn_tm'].append((int(bgn_tm.split(':')[0]) * 60 + int(bgn_tm.split(':')[1])))

    dur = int(input('Введіть тривалість уроку у хвилинах\n'))
    for i in maindict['bgn_tm']:
        maindict['end_tm'].append(i + dur)
    
    if not '0' == str(input("Якщо потрібно заходити на урок за посиланням ZOOM, натисніть ENTER,\nякщо не потрібно введіть 0\n")):
        lessons = list(set(maindict['понеділок'] + maindict['вівторок'] + maindict['середу'] + maindict['четвер'] + maindict['п\'ятницю']))
        for i in lessons:
            maindict['links'][i] = (input(f'Введіть посилання на урок {i}\n'))
            
    with open('data.dat', 'wb') as f:
        pickle.dump(maindict, f)

d = int(time.localtime().tm_wday)
m = int(time.localtime().tm_min + ((time.localtime().tm_hour) * 60))

if d > 4:
    print('Сьогодні вихідний')
    adm = input()

if d < 5:
    day = days[int(time.localtime().tm_wday)]
    for i in range(len(maindict[day])):
        if m < maindict['bgn_tm'][0]:
            h, m = divmod(maindict['bgn_tm'][i], 60)
            if m <= 9:
                m = f'0{m}'
            print(f'Уроки ще не почалися. Перший урок {maindict[day][i]} о {h}:{m}')
            if not maindict['links'] == {}:
                adm = input('Натисніть ENTER щоб зайти на урок\n')
                webbrowser.open(f'zoommtg://usweb.zoom.us/join?action=join&confno={maindict["links"][maindict[day][i]].split("/")[4].split("?")[0]}&pwd={maindict["links"][maindict[day][i]].split("/")[4].split("?")[1].split("=")[1].split(".")[0]}')
                break
            else:
                adm = input()
            break
        if m >= maindict['bgn_tm'][i] and maindict['end_tm'][i] > m:
            h, m = divmod(maindict['end_tm'][i], 60)
            if m <= 9:
                m = f'0{m}'
            print(f'Зараз урок {maindict[day][i]}, закінчується о {h}:{m}')
            if not maindict['links'] == {}:
                adm = input('Натисніть ENTER щоб зайти на урок\n')
                webbrowser.open(f'zoommtg://usweb.zoom.us/join?action=join&confno={maindict["links"][maindict[day][i]].split("/")[4].split("?")[0]}&pwd={maindict["links"][maindict[day][i]].split("/")[4].split("?")[1].split("=")[1].split(".")[0]}')
                break
            else:
                adm = input()
            
        if m >= maindict['end_tm'][i] and maindict['bgn_tm'][i + 1] > m:
            h, m = divmod(maindict['bgn_tm'][i + 1], 60)
            if m <= 9:
                m = f'0{m}'
            print(f'Зараз перерва. Наступний урок {maindict[day][i + 1]} о {h}:{m}')
            if not maindict['links'] == {}:
                adm = input('Натисніть ENTER щоб зайти на урок\n')
                webbrowser.open(f'zoommtg://usweb.zoom.us/join?action=join&confno={maindict["links"][maindict[day][i + 1]].split("/")[4].split("?")[0]}&pwd={maindict["links"][maindict[day][i + 1]].split("/")[4].split("?")[1].split("=")[1].split(".")[0]}')
                break
            else:
                adm = input()
            
        if m >= maindict['end_tm'][len(maindict[day]) - 1]:
            print('Уроки закінчились')
            adm = input()
            break
