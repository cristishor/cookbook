import crud_ops

APP_GRAPH_ACTIONS_MAP = {
    'MAIN_MENU'         : ['example_menu', '2', '3'],
    'example_menu'      : ['1', '2', '3']
}
APP_ACTIONS_STACK = ['MAIN_MENU']

def CREATE_MENU(_option):
    # ...

    # if it is a menu
    if _option in APP_GRAPH_ACTIONS_MAP:
        rawLines = APP_GRAPH_ACTIONS_MAP[_option]
    else:
        # TO DO: handle if the menu/action = option is not found in the APP_GRAPH_ACTIONS_MAP
        pass
    
    if _option == 'MAIN_MENU':
        lines = rawLines
        # or use a handleMainMenu()
    elif _option == 'example_menu':
        lines = rawLines
        # handleExampleMenu == do something else
        pass

    return lines


def render(lines):
    for line in lines:
        print(line)

while True:
    render(CREATE_MENU(APP_ACTIONS_STACK[-1]))

    user_input_raw = input()

    if user_input_raw == 'q':
        break

    if user_input_raw == 'b' and len(APP_ACTIONS_STACK) > 1:
        APP_ACTIONS_STACK.pop()
        continue
    
    user_input = APP_GRAPH_ACTIONS_MAP[APP_ACTIONS_STACK[-1]][int(user_input_raw) - 1]

    APP_ACTIONS_STACK.append(user_input)



