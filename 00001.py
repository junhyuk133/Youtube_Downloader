from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube #유튜브 비디오 다운로드 
import time

#Global 
Folder_Name = "" 
select = []

#functions

def openLocation():
    global Folder_Name
    Folder_Name = filedialog.askdirectory()
    if(len(Folder_Name) > 1):
        locationError.config(text=Folder_Name)
    else:
        locationError.config(text="저장 디렉토리를 선택해 주세요.")

#callback function
def progress_function(stream, chunk, bytes_remaining):
    global select
    prog = round((1-bytes_remaining/select.filesize)*100,1)
    print(prog,'% done...')
    messagelabel.configure(text="다운로드 중입니다.") 
    messagelabel.update()
    disnum.configure(text=prog)
    disnum.update()


def DownloadVideo():
    global select

    choice = ytdChoices.get()
    print(choice)
    url = ytdEntry.get()
    if(len(url) > 1):
        ytdError.config(text="")
        yt = YouTube(url, on_progress_callback=progress_function)


        #선택한 비디오 필터의 옵션을 다르게 하여 확인 
        for e in yt.streams.filter(res='1080p').all():
            print(e)

        #Resolution
        
        if(choice == choices[0]): #1080p
            select = yt.streams.filter(res='1080p').first()
        elif(choice == choices[1]): #720p
            select = yt.streams.filter(progressive='True', res='720p').first()
        elif(choice == choices[2]):
            select = yt.streams.filter(progressive='True', res='360p').first()
        elif(choice == choices[3]):
            select = yt.streams.filter(only_audio=True).first()
        else:
            select = None
            messagelabel.config(text="해상도를 선택해 주세요.", fg="red")
            messagelabel.update()
        
        #download func.
        if(select != None):
            select.download(Folder_Name)
            messagelabel.config(text="다운로드 완료!")
        else:
            messagelabel.config(text="선택한 해상도를 지원하지 않습니다.")
           
        

    else:
        messagelabel.config(text="URL를 입력해 주세요.")

    print(Folder_Name)
    if(Folder_Name == ""):
        messagelabel.config(text="폴더를 지정해 주세요.")

root = Tk()
root.title("Youtube Downloader")
root.geometry("450x400+300+200")
root.columnconfigure(0, weight=1) #센터에 자리잡기

#유튜브 영상 url 입력창 
ytdLabel = Label(root, text="다운로드 할 영상 URL을 입력하세요.", font=("jost", 12))
ytdLabel.grid(pady=10)

ytdEntryVar = StringVar() #변수타입에 유의
ytdEntry = Entry(root, width=55, textvariable=ytdEntryVar)
ytdEntry.grid()

#에러메세지 출력
ytdError = Label(root, text="", fg="red", font=("jost", 9))
ytdError.grid()

saveLabel = Label(root, text="저장 폴더를 선택하세요.", font=("jost", 12))
saveLabel.grid(pady=5)

#save button
saveEntry = Button(root, width=15, bg="#333", fg="white", text="경로 선택", command=openLocation)
saveEntry.grid()

#Error Msg
locationError = Label(root, text="", fg="red", font=("jost", 9))
locationError.grid()

#다운로드 품질 설정
ytdQuality = Label(root, text="다운로드 품질(720p 영상+mp3)",  font=("jost", 12))
ytdQuality.grid(pady=5)

#콤보박스 출력
choices = ["1080p", "720p", "360p", "mp3"]
ytdChoices = ttk.Combobox(root, value=choices)
ytdChoices.grid()

#다운로드 버튼
downloadBtn = Button(root, width=15, bg="#333", fg="white", text="다운로드", command=DownloadVideo)
downloadBtn.grid(pady=5)

#기타 
messagelabel = Label(root, text="Youtube Downloader ", font=("jost", 11))
messagelabel.grid()

#다운로드 진행율
disnum = Label(root, text='', font=('jost', 36))
disnum.grid(pady=20)

root.mainloop()


