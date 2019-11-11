import requests as r
import bs4 as bs
import re
from imdb import IMDb
import matplotlib.pyplot as plt
import sys


# Functions


def rottenTomatoScrap(movieName):
    rottenTomatoMovieName = '_'.join(movieName.lower().split(' '))
    url = 'https://www.rottentomatoes.com/m/'+rottenTomatoMovieName
    # print(url)

    page = r.get(url)
    code = page.status_code
    #print('Code is: ', page.status_code)
    if code is 200:
        #print('Status Code: ', page.status_code)
        soup = bs.BeautifulSoup(page.text, 'lxml')

        for link in soup.find_all("span", class_="mop-ratings-wrap__percentage"):
            rating_text = link.text.strip()
            pattern = "^[0-9]{1,2}%$"
            if re.match(pattern, rating_text):
                # print(link.text)
                rottenDataList.append(rating_text)
        print('Rotten Data List: ', rottenDataList)
        return code
    else:
        return code


def imdbScrap(movieName):
    ia = IMDb()
    s_result = ia.search_movie(movieName)
    the_unt = s_result[0]
    ia.update(the_unt)
    percentageValue = str(int(the_unt['rating']*10))+'%'
    imdbDataList.append(percentageValue)
    print('IMDb Data List: ', imdbDataList)


def plotRatingGraph(database):
    x = ['Rotten Tomato Critics', 'Rotten Tomato Users', 'IMDb']
    y = [int(str(database['1']['critics']).strip('%')),
         int(str(database['1']['audience']).strip('%')),
         int(str(database['2']['ratings']).strip('%'))]
    width = 0.35
    fig, ax = plt.subplots()
    rect1 = plt.bar(x, y, width, label="%")
    plt.ylabel("Rating percentage")
    plt.title(movieName+' ratings')
    for rect in rect1:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.0*height,
                '%d' % int(height),
                ha='center', va='bottom')
    plt.show()
    searchAgain()
    #print('Huh? o_o')


def takeInput():
    return input('Enter the name of movie: ')


def getRequestCode(movieName):
    return rottenTomatoScrap(movieName)


# def weCallThingsHere():
#     movieName = takeInput()
#     print('Movie name: ', movieName)
#     requestCode = getRequestCode(movieName)
#     print('Request Code: ', requestCode)
#     return requestCode, movieName


def startTheExecution():
    movieName = takeInput()
    print('Movie name: ', movieName)
    requestCode = getRequestCode(movieName)
    print('Request Code: ', requestCode)
    # returnData = weCallThingsHere()
    # requestCode = returnData[0]
    # movieName = returnData[1]
    # print('Daheck is this: ', requestCode)
    # print('Daehck its type: ', type(requestCode))
    while requestCode is not 200:
        print('High o_o?')
        print('Enter movie name again o_o')
        movieName = takeInput()
        print('Movie name: ', movieName)
        requestCode = getRequestCode(movieName)
        print('Request Code: ', requestCode)
    imdbScrap(movieName)
    plotTheGraph()


def plotTheGraph():
    rottenData = {'critics': rottenDataList[0],
                  'audience': rottenDataList[len(rottenDataList)-1]}
    imdbData = {'ratings': imdbDataList[0]}

    database = {'1': rottenData,
                '2': imdbData}
    print(database)
    plotRatingGraph(database)


def searchAgain():
    rottenDataList.clear()
    imdbDataList.clear()
    choice = input(
        'Want to search again? Yes? No? Enter Y for Yes and N for No: ')
    if choice is 'Y':
        startTheExecution()
    elif choice is 'N':
        print('Okay, goodbye!')
        sys.exit(1)
    else:
        print('Are you really high o_o?')
        # sys.exit(1)
        searchAgain()
# Main method Thingy


rottenDataList = []
imdbDataList = []
requestCode = 0
movieName = ''

startTheExecution()

# movieName = takeInput()
# print('Movie name: ', movieName)
# requestCode = getRequestCode()
# print('Request Code: ', requestCode)
# while requestCode is not 200:
#     print('High o_o?')
#     print('Enter movie name again o_o')
#     takeInput()
# imdbScrap()

# rottenData = {'critics': rottenDataList[0],
#               'audience': rottenDataList[len(rottenDataList)-1]}
# imdbData = {'ratings': imdbDataList[0]}

# database = {'1': rottenData,
#             '2': imdbData}
# print(database)
# plotRatingGraph()
searchAgain()
