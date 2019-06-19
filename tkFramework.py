from tkinter import*
from tkinter import font
import urllib
import http.client
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree
import folium
from selenium import webdriver
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import telepot

CITY=0
DISTRICT=1

TOKEN = '886975265:AAGNwVYRGIShdu4tf95OwRp6HHbwaMskYy4'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)


class framework:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("400x600+750+200")
        self.window.title("지진대피소 안내")

        #텔레그램
       # self.telegram = telegram()
       # pprint(bot.getMe())
        #telegram.noti.run()

        #프레임별로 요소들을 한번에 다룸. ex) destroy()
        self.mainFrame=[]
        self.resultFrame=[]
        self.graphFrame=[]
        self.quizFrame=[]
        self.curBookmark=None
        self.rowElements=[]
        self.rowElementsIndoor = []



        #self.InitMainFrame()

        key = 'GPNYeB7snGIfFy9SjaOSs4RJlIn%2B4uAYYlq9ISmcNodo3AQX4uD6DS3M1%2FpXXHQ5IhR%2FUOewInIr%2F0WN4%2BdBdA%3D%3D'
        if not self.rowElements:
            for s in range(5):
                s = str(s)
                conn = http.client.HTTPConnection("apis.data.go.kr")
                conn.request("GET",
                             "/1741000/EarthquakeOutdoorsShelter/getEarthquakeOutdoorsShelterList?serviceKey=" + key + "&pageNo=" + s + "&numOfRows=100&type=xml&flag=Y")
                req = conn.getresponse()

                tree = ElementTree.fromstring(req.read())
                self.rowElements = self.rowElements + list(tree.getiterator("row"))

        if not self.rowElementsIndoor:
            for s in range(5):
                s = str(s)
                conn = http.client.HTTPConnection("apis.data.go.kr")
                conn.request("GET",
                             "/1741000/EarthquakeIndoors/getEarthquakeIndoorsList?serviceKey=" + key + "&pageNo=" + s + "&numOfRows=100&type=xml&flag=Y")
                req = conn.getresponse()

                tree = ElementTree.fromstring(req.read())
                self.rowElementsIndoor = self.rowElementsIndoor + list(tree.getiterator("row"))

        self.InitGraphRadgioButton()

        self.window.mainloop()

    def InitGraphRadgioButton(self):
        self.InitTitleLabel()

        self.radVar = IntVar()

        self.graph_OutdoorButton = Radiobutton(self.window, text="옥외", value=1, variable=self.radVar, relief="solid", command=self.InitGraphFrame_Outdoor)
        self.graph_OutdoorButton.pack()
        self.graph_OutdoorButton.place(x=250, y=20)

        self.graph_IndoorButton = Radiobutton(self.window, text="옥내", value=2, variable=self.radVar, relief="solid", command=self.InitGraphFrame_Indoor)
        self.graph_IndoorButton.pack()
        self.graph_IndoorButton.place(x=300, y=20)

        self.graphFrame.append(self.graph_OutdoorButton)
        self.graphFrame.append(self.graph_IndoorButton)

    def InitGraphFrame_Outdoor(self):
        cities=[]
        cityNames=[]

        for i in self.rowElements:
            cities.append(i.find("ctprvn_nm").text)
            if cities[-1] not in cityNames:
                cityNames.append(i.find("ctprvn_nm").text)

        self.canvas=Canvas(self.window,width=400,height=600)
        self.canvas.pack()
        self.canvas.place(x=0,y=50)

        tmpFont = font.Font(self.window, size=8, family='Consolas')
        histogram=[]
        for  i in cityNames:
            histogram.append(cities.count(i))

        maxCount=int(max(histogram))
        barWidth=25

        for i in range(len(histogram)):
            if(histogram[i] < 1):
                histogram[i]=1
            self.canvas.create_rectangle(0,20+i*5+barWidth*i, 80+(int(self.canvas['width'])-100)*histogram[i]/maxCount,20+i*5+barWidth*(i+1),fill='light green')
            self.canvas.create_text(50,30+i*5+barWidth*i,text=cityNames[i],font=tmpFont)
            self.canvas.create_text(90+(int(self.canvas['width'])-100)*histogram[i]/maxCount,30+i*5+barWidth*i,text=histogram[i],font=tmpFont)

        tmpFont = font.Font(self.window, size=10, weight='bold', family='Consolas')
        self.checkButton=Button(self.window, font=tmpFont, text="검    색", command=self.InitMainFrame)
        self.checkButton.pack()
        self.checkButton.place(x=330,y=570)

        self.graphFrame.append(self.canvas)
        self.graphFrame.append(self.checkButton)

    def InitGraphFrame_Indoor(self):
        cities = []
        cityNames = []

        for i in self.rowElementsIndoor:
            cities.append(i.find("ctprvn_nm").text)
            if cities[-1] not in cityNames:
                cityNames.append(i.find("ctprvn_nm").text)
        self.canvas = Canvas(self.window, width=400, height=600)
        self.canvas.pack()
        self.canvas.place(x=0, y=50)

        tmpFont = font.Font(self.window, size=8, family='Consolas')
        histogram = []
        for i in cityNames:
            histogram.append(cities.count(i))

        maxCount = int(max(histogram))
        barWidth = 25

        for i in range(len(histogram)):
            if (histogram[i] < 1):
                histogram[i] = 1
            self.canvas.create_rectangle(0, 20 + i * 5 + barWidth * i,
                                        80 + (int(self.canvas['width']) - 100) * histogram[i] / maxCount,
                                        20 + i * 5 + barWidth * (i + 1), fill='light green')
            self.canvas.create_text(50, 30 + i * 5 + barWidth * i, text=cityNames[i], font=tmpFont)
            self.canvas.create_text(90 + (int(self.canvas['width']) - 100) * histogram[i] / maxCount,
                                    30 + i * 5 + barWidth * i, text=histogram[i], font=tmpFont)

        tmpFont = font.Font(self.window, size=10, weight='bold', family='Consolas')
        self.checkButton = Button(self.window, font=tmpFont, text="검    색", command=self.InitMainFrame)
        self.checkButton.pack()
        self.checkButton.place(x=330, y=570)

        self.graphFrame.append(self.canvas)
        self.graphFrame.append(self.checkButton)

    def InitMainFrame(self):
        for i in self.graphFrame:
            i.destroy()
        self.graphFrame=[]

        self.OutdoorButton_List = Radiobutton(self.window, text="옥외", value=3, variable=self.radVar, relief="solid")
        self.OutdoorButton_List.pack()
        self.OutdoorButton_List.place(x=250, y=20)
        self.IndoorButton_List = Radiobutton(self.window, text="옥내", value=4, variable=self.radVar, relief="solid")
        self.IndoorButton_List.pack()
        self.IndoorButton_List.place(x=300, y=20)

        self.mainFrame.append(self.OutdoorButton_List)
        self.mainFrame.append(self.IndoorButton_List)

        # title = 지진 대피소 조회
        #self.InitTitleLabel()
        # frame3개
        self.InitSearchLabel()
        # 시군구 검색 박스
        self.InitSearchEntry()
        # 검색, 종료
        self.InitCommandButton()
        # 대피소 리스트
        self.InitShelterList()

    def InitTitleLabel(self):
        tmpFont = font.Font(self.window, size=20, weight='bold', family='Consolas')
        self.title = Label(self.window,text="지진 대피소 조회", font=tmpFont)
        self.title.pack()
        self.title.place(x=20,y=10)

    def InitSearchLabel(self):
        tmpFont = font.Font(self.window, size=12, weight='bold', family='Consolas')

        self.label = [Label(self.window,font=tmpFont,text="시/도"),
                        Label(self.window,font=tmpFont, text="시/군/구")]
        for i in self.label:
            i.pack()
            self.mainFrame.append(i)
        self.label[CITY].place(x=40,y=50)
        self.label[DISTRICT].place(x=180, y=50)

    def InitSearchEntry(self):
        self.entry = [Entry(self.window,width=16),
                        Entry(self.window,width=16)]
        for i in self.entry:
            i.pack()
            self.mainFrame.append(i)

        self.entry[CITY].place(x=20, y=70)
        self.entry[DISTRICT].place(x=160, y=70)

    def InitCommandButton(self):
        tmpFont = font.Font(self.window, size=10, weight='bold', family='Consolas')

        self.searchButton = Button(self.window, font=tmpFont, text="검    색", command=self.SearchShelters)
        self.searchButton.pack()
        self.searchButton.place(x=300,y=65)

        self.mainFrame.append(self.searchButton)

    def InitShelterList(self):
        frame=Frame(self.window)
        frame.pack()
        frame.place(x=10,y=130)
        self.sheltersScrollbar = Scrollbar(frame)
        self.shelterList=Listbox(frame,width=50,height=25,
                                 yscrollcommand=self.sheltersScrollbar.set)
        self.shelterList.pack(side="left")
        self.sheltersScrollbar.pack(side="right", fill="y")
        self.sheltersScrollbar.config(command=self.shelterList.yview)

        tmpFont = font.Font(self.window, size=10, weight='bold', family='Consolas')
        self.bookmarkButton = Button(self.window, font=tmpFont, text="즐겨찾기",command=self.ClickBookmarkSearch)
        self.selectButton=Button(self.window,font=tmpFont,text="선택완료",command=self.ClickSearch)
        self.bookmarkButton.pack()
        self.selectButton.pack()
        self.bookmarkButton.place(x=250,y=550)
        self.selectButton.place(x=315,y=550)

        self.mainFrame.append(self.shelterList)
        self.mainFrame.append(self.sheltersScrollbar)
        self.mainFrame.append(self.bookmarkButton)
        self.mainFrame.append(self.selectButton)

    def SetBookmark(self):
        f = open("Bookmark.txt",'w')
        f.write(self.address)
        f.close()

        map_osm = folium.Map(location=[float(self.yPos), float(self.xPos)], zoom_start=16)
        folium.Marker([float(self.yPos), float(self.xPos)], popup='Mt. Hood Meadows').add_to(map_osm)
        map_osm.save('osm.html')

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.driver.get("C:/Users/CHOI JANGRAK\Desktop/스언어\지진대피소/ScriptLanguage/osm.html")
        self.driver.save_screenshot("bookmarkscreenshot.png")


    def SearchShelters(self):
        #검색해서 찾은 것들을 리스트 박스에 넣는다
        cityName = self.entry[CITY].get()
        districtName = self.entry[DISTRICT].get()

        if len(self.label) == 3:
            self.shelterList.delete(0, len(self.itemList))
        self.itemList=[]

        if self.radVar.get() == 3:
            for item in self.rowElements:
                if districtName == '':
                    if cityName == item.find("ctprvn_nm").text:
                        self.itemList.append(item)
                elif cityName=='':
                    if districtName == item.find("sgg_nm").text:
                        self.itemList.append(item)
                elif cityName == item.find("ctprvn_nm").text:
                    if districtName == item.find("sgg_nm").text:
                        self.itemList.append(item)

        elif self.radVar.get() == 4:
            for item in self.rowElementsIndoor:
                if districtName == '':
                    if cityName == item.find("ctprvn_nm").text:
                        self.itemList.append(item)
                elif cityName=='':
                    if districtName == item.find("sgg_nm").text:
                        self.itemList.append(item)
                elif cityName == item.find("ctprvn_nm").text:
                    if districtName == item.find("sgg_nm").text:
                        self.itemList.append(item)

        self.PrintShelters()

    def PrintShelters(self):
        self.label.append(Label(self.window,text=str(len(self.itemList))+"곳 찾음"))
        self.label[-1].pack()
        self.label[-1].place(x=10,y=110)
        self.mainFrame.append(self.label[-1])
        self.itemList.sort(key=lambda i : i.find("vt_acmdfclty_nm").text)

        for i in range(len(self.itemList)):
            self.shelterList.insert(i, self.itemList[i].find("dtl_adres").text + '  ' + self.itemList[i].find("vt_acmdfclty_nm").text)


    def ClickSearch(self):
        self.address = self.itemList[self.shelterList.curselection()[0]].find("dtl_adres").text + ' ' +\
                       self.itemList[self.shelterList.curselection()[0]].find("vt_acmdfclty_nm").text
        # 위도경도
        self.xPos = self.itemList[self.shelterList.curselection()[0]].find("xcord").text
        self.yPos = self.itemList[self.shelterList.curselection()[0]].find("ycord").text

        self.FindLocation()

    def ClickBookmarkSearch(self):
        f=open("Bookmark.txt")
        self.curBookmark=f.read()
        if self.curBookmark:
            self.address = self.curBookmark
            self.FindBookMark()

    def FindBookMark(self):
        tmpFont = font.Font(self.window, size=10, weight='bold', family='Consolas')
        self.photo = PhotoImage(file="bookmarkscreenshot.png")

        for i in self.mainFrame:
            i.destroy()
        self.mainFrame=[]

        self.label=[Label(self.window,image=self.photo,width=450,height=350),
                    Label(self.window,text=self.address),
                    Label(self.window,justify="left",
                          text="(1) 튼튼한 탁자 아래에 들어가 몸을 보호합니다\n"
                                "(2) 가스, 전기를 차단하고 문을 열어 출구를 확보합니다\n"
                                "(3) 계단을 이용하여 밖으로 대피합니다\n"
                                "(4) 건물 담장과 떨어져 이동합니다\n"
                                "(5) 넓은 공간으로 대피합니다\n")]

        self.gmailButton=Button(self.window,text="Gmail",font=tmpFont,command=self.SendMail)
        self.bookmarkButton=Button(self.window,text="즐겨찾기",font=tmpFont,command=self.SetBookmark)
        self.backButton=Button(self.window,text="뒤로가기",font=tmpFont,command=self.Back)
        self.quizButton=Button(self.window, text="퀴즈", font=tmpFont, command=self.Quiz)

        for i in self.label:
            i.pack()
        self.gmailButton.pack()
        self.bookmarkButton.pack()
        self.backButton.pack()
        self.quizButton.pack()

        self.label[0].place(x=0,y=50)
        self.label[1].place(x=0,y=400)
        self.label[2].place(x=0,y=450)
        self.gmailButton.place(x=310,y=450)
        self.bookmarkButton.place(x=310,y=480)
        self.backButton.place(x=310,y=510)
        self.quizButton.place(x=310,y=540)

        for i in self.label:
            self.resultFrame.append(i)
        self.resultFrame.append(self.gmailButton)
        self.resultFrame.append(self.bookmarkButton)
        self.resultFrame.append(self.backButton)
        self.resultFrame.append(self.quizButton)

    def Quiz(self):
        tmpFont = font.Font(self.window, size=10, weight='bold', family='Consolas')

        for i in self.resultFrame:
            i.destroy()
        self.resultFrame=[]

       #self.photo_smile = PhotoImage(file="smile.png")
        #self.photo_sad = PhotoImage(file="sad.png")

        self.quiz_trueButton = Radiobutton(self.window, text="튼튼한 탁자 아래에 들어가 몸을 보호합니다", value=5, variable=self.radVar, relief="solid")
        self.quiz_trueButton.pack()
        self.quiz_trueButton.place(x=20, y=100)
        self.quiz_falseButton = Radiobutton(self.window, text="좁은 공간으로 대피합니다", value=6, variable=self.radVar, relief="solid")
        self.quiz_falseButton.pack()
        self.quiz_falseButton.place(x=20, y=150)

        self.backButton_Quiz = Button(self.window, text="뒤로가기", font=tmpFont, command=self.Back_Quiz)

        self.backButton_Quiz.pack()
        self.backButton.place(x=310, y=510)

        #if self.radVar == 5:
        #    self.label_quiz = Label(self.window,image=self.photo_smile,width=300,height=300)
        #elif self.radVar == 6:
        #    self.label_quiz = Label(self.window,image=self.photo_sad,width=300,height=300)

        #self.label_quiz.pack()
        #self.label_quiz.place(x=300, y=400)

        self.quizFrame.append(self.backButton_Quiz)
        self.quizFrame.append(self.quiz_trueButton)
        self.quizFrame.append(self.quiz_falseButton)
        ##self.quizFrame.append(self.label_quiz)

    def Back_Quiz(self):
        for i in self.quizFrame:
            i.destroy()
        self.quizFrame = []

        self.InitMainFrame()

    def FindLocation(self):
        tmpFont = font.Font(self.window, size=10, weight='bold', family='Consolas')
        # 이미지 연습중

        # 지도
        map_osm = folium.Map(location=[float(self.yPos), float(self.xPos)], zoom_start=16)
        folium.Marker([float(self.yPos), float(self.xPos)], popup='Mt. Hood Meadows').add_to(map_osm)
        map_osm.save('osm.html')

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.driver.get("C:/Users\CHOI JANGRAK/Desktop/스언어\지진대피소/ScriptLanguage/osm.html")
        self.driver.save_screenshot("bookmarkscreenshot.png")

        self.photo=PhotoImage(file="bookmarkscreenshot.png")
        self.driver.close()
        for i in self.mainFrame:
            i.destroy()
        self.mainFrame=[]

        self.label=[Label(self.window,image=self.photo,width=450,height=350),
                    Label(self.window,text=self.address),
                    Label(self.window,justify="left",
                          text="(1) 튼튼한 탁자 아래에 들어가 몸을 보호합니다\n"
                                "(2) 가스, 전기를 차단하고 문을 열어 출구를 확보합니다\n"
                                "(3) 계단을 이용하여 밖으로 대피합니다\n"
                                "(4) 건물 담장과 떨어져 이동합니다\n"
                                "(5) 넓은 공간으로 대피합니다\n")]

        self.gmailButton=Button(self.window,text="Gmail",font=tmpFont,command=self.SendMail)
        self.bookmarkButton=Button(self.window,text="즐겨찾기",font=tmpFont,command=self.SetBookmark)
        self.backButton=Button(self.window,text="뒤로가기",font=tmpFont,command=self.Back)
        self.quizButton=Button(self.window, text="퀴즈", font=tmpFont, command=self.Quiz)

        for i in self.label:
            i.pack()
        self.gmailButton.pack()
        self.bookmarkButton.pack()
        self.backButton.pack()
        self.quizButton.pack()

        self.label[0].place(x=0,y=50)
        self.label[1].place(x=0,y=400)
        self.label[2].place(x=0,y=450)
        self.gmailButton.place(x=310,y=450)
        self.bookmarkButton.place(x=310,y=480)
        self.backButton.place(x=310,y=510)
        self.quizButton.place(x=310,y=540)

        for i in self.label:
            self.resultFrame.append(i)
        self.resultFrame.append(self.gmailButton)
        self.resultFrame.append(self.bookmarkButton)
        self.resultFrame.append(self.backButton)
        self.resultFrame.append(self.quizButton)

    def Back(self):
        for i in self.resultFrame:
            i.destroy()
        self.resultFrame=[]

        #self.driver.close()

        self.InitMainFrame()

    def SendMail(self):
        host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
        port = "587"
        imgFile='bookmarkscreenshot.png'

        senderAddr = "chlwkdfkr122@gmail.com"  # 보내는 사람 email 주소.
        recipientAddr = "bisu235@naver.com"  # 받는 사람 email 주소.

        msg = MIMEBase("multipart", "mixed")
        msg['Subject'] = "지진 대피소"  # 제목
        msg['From'] = senderAddr
        msg['To'] = recipientAddr

        cont=MIMEText(self.address,'plain','UTF-8')
        msg.attach(cont)

        fp=open(imgFile,'rb')
        img=MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        # 메일을 발송한다.
        s = mysmtplib.MySMTP(host, port)
        # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("chlwkdfkr122@gmail.com", "qaz067808")
        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
        s.close()