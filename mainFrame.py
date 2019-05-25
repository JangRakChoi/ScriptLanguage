from realLauncher import*
import resultFrame
from tkinter import*
from tkinter import font

CITY=0
DISTRICT=1
TOWN=2

class Frame():
    def __init__(self):
        self.mainFrame = Frame(Window.window)
        self.mainFrame.pack()

        self.subframe = [Frame(self.mainFrame), Frame(self.mainFrame), Frame(self.mainFrame)]

        # title = 지진 대피소 조회
        self.InitTitleLabel()
        # frame3개
        self.InitSelectLabel()
        #검색, 종료
        self.InitCommandButton()
        #시군구 리스트박스
        self.InitListBox()


    def InitTitleLabel(self):
        tmpFont = font.Font(self.mainFrame, size=20, weight='bold', family='Consolas')
        self.title = Label(self.mainFrame,text="지진 대피소 조회", font=tmpFont)
        self.title.pack()

    def InitSelectLabel(self):
        tmpFont = font.Font(self.mainFrame, size=12, weight='bold', family='Consolas')

        for i in range(3):
            self.subframe[i].pack(side=LEFT)

        self.label = [Label(self.subframe[CITY],font=tmpFont,text="시/도"),
                        Label(self.subframe[DISTRICT],font=tmpFont, text="시/군/구"),
                        Label(self.subframe[TOWN], font=tmpFont,text="읍/면/리")]

    def InitCommandButton(self):
        tmpFont = font.Font(self.mainFrame, size=10, weight='bold', family='Consolas')

        self.selectFrame = Frame(self.mainFrame)
        self.selectFrame.pack(side=BOTTOM)
        self.searchButton = Button(self.selectFrame, font=tmpFont, text="검색", command=Framework.ShowResult)
        self.quitButton = Button(self.selectFrame, font=tmpFont, text="종료")

        self.searchButton.pack()
        self.quitButton.pack()

    def InitListBox(self):
        self.scrollbar = [Scrollbar(self.frame[i]) for i in range(3)]
        self.listbox = [Listbox(self.frame[i], yscrollcommand=self.scrollbar[i].set) for i in range(3)]

        for i in range(3):
            self.scrollbar[i]["command"] = self.listbox[i].yview
            self.scrollbar[i].pack(side=RIGHT, fill='y')
            self.listbox[i].pack()
            self.label[i].pack()

        for i in range(20):
            self.listbox[CITY].insert(i, "시/도" + str(i))
            self.listbox[DISTRICT].insert(i, "시/군/구" + str(i))
            self.listbox[TOWN].insert(i, "읍/면/동" + str(i))

    def ShowResult(self):
        self.mainFrame.destroy()
        resultFrame.Frame()

        self.resultFrame=Frame(Framework.rFrame)
        self.resultFrame.tkraise()
        self.resultFrame.pack()
        # 이미지 연습중
        # photo=PhotoImage(file="osm.html")

        self.frame = [Frame(self.resultFrame), Frame(self.resultFrame), Frame(self.resultFrame), Frame(self.resultFrame), Frame(self.resultFrame)]
        # 지도
        self.frame[0].grid(row=0, column=0)
        # 주소지
        self.frame[1].grid(row=1, column=0)
        # 지진대피요령
        self.frame[2].grid(row=0, column=1)
        # Gmail, 뒤로가기
        self.frame[3].grid(row=0, column=2)
        # 종료
        self.frame[4].grid(row=1, column=2)

        self.label = []
        # self.label.append(Label(self.frame[0],text="여기에\n 사진이 \n 들어간다"))
        self.label.append(Label(self.frame[0], text="사진 들어감"))
        self.label.append(Label(self.frame[1], text="지진\n 대피소 \n 주소"))
        self.label.append(Label(self.frame[2], text="지진\n 대피 \n 요령"))

        self.gmailButton = Button(self.frame[3], text="Gmail")
        self.backButton = Button(self.frame[3], text="뒤로가기")
        self.quitButton = Button(self.frame[4], text="종료")

        for i in self.label:
            i.pack()
        self.gmailButton.pack()
        self.backButton.pack()
        self.quitButton.pack()