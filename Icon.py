############################################
## VITA ICON GENERATOR - CREATED BY ANTHJ ##
############################################

from pathlib import Path
import PySimpleGUI as sg
from PIL import Image, ImageGrab
import os
import ctypes

sg.theme_add_new('VitaDark', {
    'BACKGROUND': '#0f1923', 'TEXT': '#e2e8f0',
    'INPUT': '#1c2d3f', 'TEXT_INPUT': '#e2e8f0', 'SCROLL': '#2d4a6b',
    'BUTTON': ('#e2e8f0', '#1e3a5f'),
    'PROGRESS': ('#f0c040', '#0f1923'),
    'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
})
sg.theme('VitaDark')
sg.set_options(font=('Helvetica', 11))
ThemeName = ""
default_button = sg.theme_button_color()
ctypes.windll.shcore.SetProcessDpiAwareness(True)
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

ICON_NAMES = [
    'web', 'trophies', 'friends', 'messages', 'party', 'ps4link',
    'parental', 'music', 'videos', 'ps3link', 'cma', 'settings',
    'calendar', 'mail', 'near', 'photos', 'power'
]
NUM_ICONS = len(ICON_NAMES)

BG     = '#0f1923'
C_PRI  = ('#0f1923', '#f0c040')
C_DEST = ('#ffffff', '#7f1d1d')
C_SEC  = ('#e2e8f0', '#1e3a5f')
C_SNAP = ('#f0c040', '#334155')

COLOR_OPTS = ['None.', 'White', 'Black', 'Blue', 'Cyan', 'Dark-Blue', 'Dark-Cyan', 'Dark-Green',
              'Dark-Grey', 'Dark-Red', 'Dark-Yellow', 'Green', 'Grey', 'Pink', 'Purple', 'Red', 'Yellow', 'Default']
BG_OPTS    = ['None.', 'White', 'Black', 'Blue', 'Cyan', 'Dark-Blue', 'Dark-Cyan', 'Dark-Green',
              'Dark-Grey', 'Dark-Red', 'Dark-Yellow', 'Green', 'Grey', 'Pink', 'Purple', 'Red', 'Yellow', 'Custom', 'Snapshot']

# LOAD PREVIOUS SETTINGS AND DELETE PREVIOUS FILES
SETTINGS_PATH = Path.cwd()
settings = sg.UserSettings(
    path=SETTINGS_PATH, filename="assets\\default.ini", use_config_file=True)
filecheck = settings["ICON_GENERATOR"]["filecheck"]
TEMPfolder = 'assets\\IconBuilder\\TEMP'
for filename in os.listdir(TEMPfolder):
    file_path = os.path.join(TEMPfolder, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

if os.path.isfile("assets/tntmp"):
    with open("assets/tntmp", "r") as f:
        ThemeName = f.read()
    os.remove("assets/tntmp")

SnapCount = 0
CloneAll = 0

if filecheck == 'OK':
    icon_col = [settings["ICON_GENERATOR"][f"Icon{i}Color"]            for i in range(1, NUM_ICONS + 1)]
    icon_bgc = [settings["ICON_GENERATOR"][f"Icon{i}Background"]       for i in range(1, NUM_ICONS + 1)]
    custom   = [settings["ICON_GENERATOR"][f"Icon{i}CustomBackground"] for i in range(1, NUM_ICONS + 1)]
else:
    icon_col = ['White'] * NUM_ICONS
    icon_bgc = ['None.'] * NUM_ICONS
    custom   = ['']      * NUM_ICONS

icon_bgnd = [''] * NUM_ICONS


def c(elems):
    return [sg.Stretch(), *elems, sg.Stretch()]


def make_icon_layout(i):
    n = i + 1
    return [
        c([sg.Graph((128, 128), (0, 0), (128, 128), key=f'-Icon{n}-')]),
        [sg.InputCombo(COLOR_OPTS, size=(16, 99), default_value=icon_col[i], key=f'-icon{n}C-')],
        [sg.InputCombo(BG_OPTS,    size=(16, 99), default_value=icon_bgc[i], key=f'-icon{n}B-')],
        c([sg.InputText(k=f'custom{n}', default_text=custom[i], visible=False),
           sg.FileBrowse(button_text='Custom Image', s=13, button_color=C_SEC,
                         file_types=(('Images', '*.png *.jpg *.gif *.bmp'), ('ALL', '*.* *'))),
           sg.Button("●", key=f'Snap{n}', button_color=C_SEC, tooltip='Capture screen region')])
    ]


icon_layouts = [make_icon_layout(i) for i in range(NUM_ICONS)]

layoutx = [
    [sg.Text('VITA ICON GENERATOR', font=('Arial', 18, 'bold'), text_color='#f0c040'),
     sg.Text('by ahjones', font=('Arial', 9), text_color='#64748b'),
     sg.Stretch(),
     sg.Button('Minimise', s=11, button_color=C_SEC),
     sg.Button('Reset All', s=11, button_color=C_DEST, key='- RESET ALL ICONS -', tooltip='Reset all icons to defaults'),
     sg.Button('Close', s=11, button_color=C_DEST, key='-CLOSE-')],
    [sg.HorizontalSeparator()],
    c([sg.Column(col) for col in icon_layouts[0:6]]),
    c([sg.Column(col) for col in icon_layouts[6:11]]),
    c([sg.Column(col) for col in icon_layouts[11:17]]),
    c([sg.ProgressBar(32, orientation='h', bar_color=('#f0c040', '#1c2d3f'), size=(50, 16), key='-progressbar-')]),
    [sg.HorizontalSeparator()],
    [sg.Button("Match Icon Colors\nto First Icon", s=(20, 2), button_color=C_SEC, key='Match all Icon colors\nwith the 1st icon'),
     sg.Button("Match Backgrounds\nto First Icon", s=(20, 2), button_color=C_SEC, key='Match all Backgrounds\nwith the 1st icon'),
     sg.Stretch(),
     sg.Button("Set All to Capture Mode", key='CutALL', s=22, button_color=C_SNAP),
     sg.Button("Capture All", key='SnapALL', s=12, button_color=C_SNAP),
     sg.Stretch(),
     sg.Button("Create Icon Set", s=20, button_color=C_PRI, key='- CREATE ICON SET -')],
]
layout = [[sg.Column(layoutx)]]


def MINIMISED_VIEW():
    layoutMIN = [
        [sg.Text('ICON GENERATOR', font=('Arial', 11, 'bold'), text_color='#f0c040', background_color='#1e293b')],
        [sg.Button('Restore', s=15, k='OK', button_color=C_PRI)]
    ]
    layoutMINx = [[sg.Column(layoutMIN, background_color='#1e293b', element_justification='center')]]
    windowMIN = sg.Window('Minimised', layoutMINx, grab_anywhere=True, no_titlebar=True,
                          keep_on_top=True, finalize=True, background_color='#1e293b', margins=(0, 0))
    while True:
        eventM, valuesM = windowMIN.read()
        if eventM == sg.WIN_CLOSED or eventM == 'Cancel':
            break
        if eventM == 'OK':
            windowMIN.close()
            break


window = sg.Window('VITA ICON GENERATOR', layout, transparent_color='#000001', no_titlebar=True,
                   keep_on_top=True, grab_anywhere=True, background_color=BG, margins=(0, 0), finalize=True)
window['-progressbar-'].update(current_count=0)

custom_old = list(custom)
Icon_old   = [''] * NUM_ICONS
oldSnap = 0

while True:
    event, values = window.read(timeout=1)
    window['-progressbar-'].update(current_count=0)
    old_icon_color = values['-icon1C-']

    # CHECK FOR CUSTOM FILE CHANGES
    for i, name in enumerate(ICON_NAMES):
        n = i + 1
        key = f'custom{n}'
        if values[key] != custom[i]:
            custom_old[i] = values[key]
            custom[i]     = values[key]
            Icon_old[i]   = 'UPDATED'
            window[f'-icon{n}B-'].update('Custom')
            cmdA = f'call assets\\scale.bat -source "{custom[i]}" -target "assets\\IconBuilder\\TEMP\\Temp.png" -max-height 128 -max-width 128 -keep-ratio no -force yes'
            cmdB = f'assets\\pngquant.exe -f "assets\\IconBuilder\\TEMP\\Temp.png" -o "assets\\IconBuilder\\Overlays\\Custom\\icon_{name}.png"'
            os.system(cmdA)
            os.system(cmdB)
            if CloneAll == 1:
                window['-progressbar-'].update(current_count=n)

    if event == sg.WIN_CLOSED or event == '-CLOSE-':
        break

    if event == 'Minimise':
        window.hide()
        MINIMISED_VIEW()
        window.UnHide()

    if event == 'CutALL':
        for n in range(1, NUM_ICONS + 1):
            window[f'-icon{n}B-'].update('Snapshot')
            window[f'Snap{n}'].update(button_color=('Yellow', '#6f6f6f'))

    if event == 'SnapALL':
        for n in range(1, NUM_ICONS + 1):
            window[f'Snap{n}'].update(button_color=default_button)
            window[f'-icon{n}B-'].update('Custom')
        for i in range(NUM_ICONS):
            n = i + 1
            custom_old[i] = values[f'custom{n}']
            custom[i]     = values[f'custom{n}']
            Icon_old[i]   = 'UPDATED'
        cur = 1
        while cur <= NUM_ICONS:
            graph = window[f'-Icon{cur}-']
            bbox = (graph.Widget.winfo_rootx(), graph.Widget.winfo_rooty(),
                    graph.Widget.winfo_rootx() + graph.Widget.winfo_width(),
                    graph.Widget.winfo_rooty() + graph.Widget.winfo_height())
            ImageGrab.grab(bbox=bbox).save(f'assets/IconBuilder/Overlays/Custom/icon_{ICON_NAMES[cur - 1]}.png')
            cur += 1

    for i, name in enumerate(ICON_NAMES):
        n = i + 1
        if event == f'Snap{n}':
            if values[f'-icon{n}B-'] != 'Snapshot':
                if n == 1:
                    old_icon_color = values['-icon1C-']
                    window['-icon1C-'].update('None.')
                window[f'-icon{n}B-'].update('Snapshot')
                window[f'Snap{n}'].update(button_color=('Yellow', '#6f6f6f'))
            else:
                window[f'Snap{n}'].update(button_color=default_button)
                window[f'-icon{n}B-'].update('Custom')
                if n == 1:
                    window['-icon1C-'].update(old_icon_color)
                graph = window[f'-Icon{n}-']
                bbox = (graph.Widget.winfo_rootx(), graph.Widget.winfo_rooty(),
                        graph.Widget.winfo_rootx() + graph.Widget.winfo_width(),
                        graph.Widget.winfo_rooty() + graph.Widget.winfo_height())
                ImageGrab.grab(bbox=bbox).save(f'assets\\IconBuilder\\Overlays\\Custom\\icon_{name}.png')
                if n == 1:
                    if os.path.exists(f'assets\\IconBuilder\\TEMP\\Snap{SnapCount}.png'):
                        os.remove(f'assets\\IconBuilder\\TEMP\\Snap{SnapCount}.png')
                    SnapCount += 1
                    ImageGrab.grab(bbox=bbox).save(f'assets\\IconBuilder\\TEMP\\Snap{SnapCount}.png')
                    window['custom1'].update(f'assets\\IconBuilder\\TEMP\\Snap{SnapCount}.png')

    if event == 'Match all Icon colors\nwith the 1st icon':
        for n in range(2, NUM_ICONS + 1):
            window[f'-icon{n}C-'].update(values['-icon1C-'])

    if event == 'Match all Backgrounds\nwith the 1st icon':
        CloneAll = 1
        for n in range(2, NUM_ICONS + 1):
            window[f'-icon{n}B-'].update(values['-icon1B-'])
            window[f'custom{n}'].update(values['custom1'])

    if event == '- RESET ALL ICONS -':
        for n in range(1, NUM_ICONS + 1):
            window[f'-icon{n}C-'].update('White')
            window[f'-icon{n}B-'].update('None.')
            settings["ICON_GENERATOR"][f"Icon{n}Color"]            = 'White'
            settings["ICON_GENERATOR"][f"Icon{n}Background"]       = 'None.'
            settings["ICON_GENERATOR"][f"Icon{n}CustomBackground"] = ""

    # RENDER ICONS — only redraws when color/background selection changes
    for i, name in enumerate(ICON_NAMES):
        n = i + 1
        if Icon_old[i] != values[f'-icon{n}C-'] + values[f'-icon{n}B-']:
            Icon_old[i]  = values[f'-icon{n}C-'] + values[f'-icon{n}B-']
            window[f'-Icon{n}-'].erase()
            icon_col[i]  = values[f'-icon{n}C-']
            icon_bgc[i]  = values[f'-icon{n}B-']
            icon_file    = f'assets/IconBuilder/Overlays/{icon_col[i]}/icon_{name}.png'
            icon_bgnd[i] = f'assets/IconBuilder/Colors/{icon_bgc[i]}.png'
            if values[f'-icon{n}B-'] == 'Custom':
                icon_bgnd[i] = f'assets/IconBuilder/Overlays/Custom/icon_{name}.png'
            if Path(icon_bgnd[i]).is_file():
                window[f'-Icon{n}-'].draw_image(filename=icon_bgnd[i], location=(0, 128))
            if Path(icon_file).is_file():
                window[f'-Icon{n}-'].draw_image(filename=icon_file, location=(0, 128))
            if CloneAll == 1:
                window['-progressbar-'].update(current_count=17 + n)
            if i == NUM_ICONS - 1 and CloneAll == 1:
                CloneAll = 0

    def ThemeNAME():
        global SetName
        SetName = ''
        layoutTN = [
            [sg.Text("", s=40)],
            [sg.Text('Enter a name for this icon set')],
            [sg.Input(k='-ThemeNAME-', default_text=ThemeName, s=30)],
            [sg.Text()],
            [sg.Button('OK', s=12, k='OK', bind_return_key=True), sg.Button('Cancel', s=12)],
            [sg.Text()],
        ]
        layoutTNx = [[sg.Column(layoutTN, element_justification='center')]]
        windowTN = sg.Window('Theme Name', layoutTNx, grab_anywhere=True, no_titlebar=True,
                             keep_on_top=True, finalize=True, background_color=BG, margins=(0, 0))
        windowTN['-ThemeNAME-'].SetFocus()
        windowTN['-ThemeNAME-'].Widget.icursor('end')
        while True:
            eventN, valuesN = windowTN.read()
            if eventN == sg.WIN_CLOSED or eventN == 'Cancel':
                windowTN.close()
                break
            if eventN == 'OK':
                SetName = valuesN['-ThemeNAME-']
                windowTN.close()
                break

    if event == '- CREATE ICON SET -':
        settings["ICON_GENERATOR"]["filecheck"] = 'OK'
        for i in range(NUM_ICONS):
            n = i + 1
            settings["ICON_GENERATOR"][f"Icon{n}Color"]            = icon_col[i]
            settings["ICON_GENERATOR"][f"Icon{n}Background"]       = icon_bgc[i]
            settings["ICON_GENERATOR"][f"Icon{n}CustomBackground"] = icon_bgnd[i]

        ThemeNAME()

        if SetName == '' or SetName is None:
            print("ERROR.!")
        else:
            layoutPG = [
                [sg.Text('Generating images...')],
                [sg.ProgressBar(17, orientation='h', bar_color=('Yellow', 'Grey'), size=(50, 20), key='-progressbar-')],
            ]
            layoutPGx = [[sg.Column(layoutPG)]]
            windowx = sg.Window("Progress Bar", layoutPGx, keep_on_top=True, no_titlebar=True,
                                background_color=BG, margins=(0, 0), modal=False)
            eventx, valuesx = windowx.read(10)
            windowx['-progressbar-'].update(current_count=0)

            os.system(f'md "IconSET\\{SetName}"')

            for i, name in enumerate(ICON_NAMES):
                n = i + 1
                cmda = f'call assets\\scale.bat -source "assets\\IconBuilder\\Colors\\{icon_bgc[i]}.png" -target "assets\\IconBuilder\\TEMP\\Temp.png" -max-height 128 -max-width 128 -keep-ratio no -force yes'
                cmda = cmda.replace('assets\\IconBuilder\\Colors\\Custom.png', icon_bgnd[i])
                cmdb = f'assets\\combine composite "assets\\IconBuilder\\Overlays\\{icon_col[i]}\\icon_{name}.png" "assets\\IconBuilder\\TEMP\\Temp.png" "assets\\IconBuilder\\TEMP\\Temp2.png"'
                cmdc = f'assets\\pngquant.exe -f "assets\\IconBuilder\\TEMP\\Temp2.png" -o "IconSet\\{SetName}\\icon_{name}.png"'
                os.system(cmda)
                os.system(cmdb)
                os.system(cmdc)
                windowx['-progressbar-'].update(current_count=n)

            windowx.close()
