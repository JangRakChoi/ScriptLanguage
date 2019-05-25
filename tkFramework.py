from tkinter import*
from tkinter import font
import urllib
import http.client
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree

CITY=0
DISTRICT=1
TOWN=2

class framework:
    def __init__(self):
        #self.conn = http.client.HTTPConnection("apis.data.go.kr")
        #self.conn.request("GET", "/1741000/EarthquakeIndoors/getEarthquakeIndoorsList?serviceKey=GPNYeB7snGIfFy9SjaOSs4RJlIn%2B4uAYYlq9ISmcNodo3AQX4uD6DS3M1%2FpXXHQ5IhR%2FUOewInIr%2F0WN4%2BdBdA%3D%3D&pageNo=1&numOfRows=10&type=xml&flag=Y")
        #self.req = self.conn.getresponse()
#
        #tree = ElementTree.fromstring(self.req.read())
        #rowElements = tree.getiterator("row")
#
        #self.cityName = []
#
        #for item in rowElements:
        #    ctprvn_nm = item.find("ctprvn_nm")
        #    self.cityName.append(ctprvn_nm.text)
#
        #k = 0
        #for j in self.cityName:
        #    print(j)
        #    k += 1
        #    if k > 500:
        #        break

        self.window = Tk()
        self.window.geometry("400x600+750+200")

        #프레임별로 요소들을 한번에 다룸. ex) destroy()
        self.mainFrame=[]
        self.resultFrame=[]

        # title = 지진 대피소 조회
        self.InitTitleLabel()
        # frame3개
        self.InitSearchLabel()
        #시군구 검색 박스
        self.InitSearchEntry()
        #검색, 종료
        self.InitCommandButton()
        #대피소 리스트
        self.InitShelterList()

        self.window.mainloop()

    def InitTitleLabel(self):
        tmpFont = font.Font(self.window, size=20, weight='bold', family='Consolas')
        self.title = Label(self.window,text="지진 대피소 조회", font=tmpFont)
        self.title.pack()
        self.title.place(x=20,y=10)

    def InitSearchLabel(self):
        tmpFont = font.Font(self.window, size=12, weight='bold', family='Consolas')

        self.label = [Label(self.window,font=tmpFont,text="시/도"),
                        Label(self.window,font=tmpFont, text="시/군/구"),
                        Label(self.window,font=tmpFont,text="읍/면/리")]
        for i in self.label:
            i.pack()
            self.mainFrame.append(i)
        self.label[CITY].place(x=0+10,y=50)
        self.label[DISTRICT].place(x=110+10, y=50)
        self.label[TOWN].place(x=220+10, y=50)

    def InitSearchEntry(self):
        self.entry = [Entry(self.window,width=13),
                        Entry(self.window,width=13),
                        Entry(self.window,width=13)]
        for i in self.entry:
            i.pack()
            self.mainFrame.append(i)

        self.entry[CITY].place(x=0, y=70)
        self.entry[DISTRICT].place(x=110, y=70)
        self.entry[TOWN].place(x=220, y=70)

    def InitCommandButton(self):
        tmpFont = font.Font(self.window, size=10, weight='bold', family='Consolas')

        self.searchButton = Button(self.window, font=tmpFont, text="검    색", command=self.SearchShelters)
        self.bookmarkButton = Button(self.window, font=tmpFont, text="즐겨찾기")
        self.searchButton.pack()
        self.bookmarkButton.pack()
        self.searchButton.place(x=330,y=70)
        self.bookmarkButton.place(x=330,y=100)

        self.mainFrame.append(self.searchButton)
        self.mainFrame.append(self.bookmarkButton)

    def InitShelterList(self):
        frame=Frame(self.window)
        frame.pack()
        frame.place(x=10,y=150)
        self.sheltersScrollbar = Scrollbar(frame)
        self.shelterList=Listbox(frame,width=50,height=25,
                                 yscrollcommand=self.sheltersScrollbar.set)
        self.shelterList.pack(side="left")
        self.sheltersScrollbar.pack(side="right", fill="y")
        self.sheltersScrollbar.config(command=self.shelterList.yview)

        tmpFont = font.Font(self.window, size=10, weight='bold', family='Consolas')
        self.selectButton=Button(self.window,font=tmpFont,text="선택완료",command=self.FindLocation)
        self.selectButton.pack()
        self.selectButton.place(x=315,y=550)

        self.mainFrame.append(self.shelterList)
        self.mainFrame.append(self.sheltersScrollbar)
        self.mainFrame.append(self.selectButton)

    def SearchShelters(self):
        #검색해서 찾은 것들을 리스트 박스에 넣는다
        cityName = self.entry[CITY].get()
        self.itemList=[]

        for s in range(10):
            s = str(s)
            conn = http.client.HTTPConnection("apis.data.go.kr")
            conn.request("GET",
                         "/1741000/EarthquakeIndoors/getEarthquakeIndoorsList?serviceKey=GPNYeB7snGIfFy9SjaOSs4RJlIn%2B4uAYYlq9ISmcNodo3AQX4uD6DS3M1%2FpXXHQ5IhR%2FUOewInIr%2F0WN4%2BdBdA%3D%3D&pageNo=" + s + "&numOfRows=1000&type=xml&flag=Y")
            req = conn.getresponse()

            tree = ElementTree.fromstring(req.read())
            rowElements = tree.getiterator("row")

            for item in rowElements:
                if cityName == item.find("ctprvn_nm").text:
                    self.itemList.append(item)

        self.PrintShelters()

    def PrintShelters(self):
        self.label.append(Label(self.window,text=str(len(self.itemList))+"곳 찾음"))
        self.label[-1].pack()
        self.label[-1].place(x=10,y=130)
        self.mainFrame.append(self.label[-1])
        for i in range(len(self.itemList)):
            self.shelterList.insert(i, self.itemList[i].find("vt_acmdfclty_nm").text)


    def FindLocation(self):

        tmpFont = font.Font(self.window, size=10, weight='bold', family='Consolas')
        # 이미지 연습중
        photo=PhotoImage(file="우주소녀.gif")

        address = self.itemList[self.shelterList.curselection()[0]].find("dtl_adres").text

        for i in self.mainFrame:
            i.destroy()

        self.label=[Label(self.window,text="Im here",image=photo),
                    Label(self.window,text=address),
                    Label(self.window,text="여기\n대피 요령\n들어간다")]

        self.gmailButton=Button(self.window,text="Gmail",font=tmpFont)
        self.bookmarkButton=Button(self.window,text="즐겨찾기",font=tmpFont)
        self.backButton=Button(self.window,text="뒤로가기",font=tmpFont)

        for i in self.label:
            i.pack()
        self.gmailButton.pack()
        self.bookmarkButton.pack()
        self.backButton.pack()

        self.label[0].place(x=0,y=200)
        self.label[1].place(x=0,y=500)
        self.label[2].place(x=200,y=200)
        self.gmailButton.place(x=300,y=400)
        self.bookmarkButton.place(x=300,y=425)
        self.backButton.place(x=300,y=450)



