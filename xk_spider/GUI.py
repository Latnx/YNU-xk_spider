import PySimpleGUI as sg
import json


def login_gui():
    sg.SetOptions(text_justification='center')

    layout = [[sg.Text("学号", size=(10, 1)), sg.Input(key="num", size=(30, 1))],
              [sg.Text("密码", size=(10, 1)), sg.Input(key="psw", size=(30, 1))],
              [sg.Text("token", size=(10, 1)), sg.Input(key="token", size=(30, 1))],
              [sg.Text("验证码", size=(10, 1)), sg.Input(key="check", size=(10, 1)),
               sg.Image(filename=".\\imagetemp.png", key="captcha_img")],
              [sg.Button("登录")]]

    window = sg.Window("登录", layout)
    with open("info.json", "w+", encoding='utf-8') as info:
        info.write(json.dumps({"user": window.read()[1], "course_list": []}))


def set_gui():
    layout = [[sg.Text("待抢课程名", size=(12, 1)), sg.Input(key="course_name")],
              [sg.Text("待抢课程教师", size=(12, 1)), sg.Input(key="teacher")],
              [sg.Text("*删除课程名", size=(12, 1)), sg.Input(key="delete_name")],
              [sg.Text("*删除课程教师名", size=(12, 1)), sg.Input(key="delete_teacher")],
              [sg.Text("*待抢课程id", size=(12, 1)), sg.Input(key="class_id")],
              [sg.Text("*删除课程id", size=(12, 1)), sg.Input(key="delete_id")],
              [sg.Text("课程种类", size=(12, 1)), sg.Combo(("主修", "素选"), size=(10, 1), key="kind")],
              [sg.Button("添加")]]

    window = sg.Window("添加", layout)
    with open("info.json", "r+", encoding='utf-8') as info:
        argue = json.loads(info.read())

    argue['course_list'].append(window.read()[1])

    with open("info.json", "r+", encoding='utf-8') as info:
        info.write(json.dumps(argue))


def course_gui():
    pass


if __name__ == '__main__':
    print(login_gui())
    print(set_gui())
