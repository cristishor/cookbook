import crud_ops, cbmenus as cbm
import os

AVAILABLE_COMMANDS = {
    'help': ['.'],

    'config': ['skip_help']

}

ACTIONS_STACK = ['HELP_MAIN_MENU']

def handleAction(command):
    if command in AVAILABLE_COMMANDS:
        command_options = AVAILABLE_COMMANDS[command]
    else:
        raise('MENU / ACTION not defined on the APP GRAPH MAP')

    isDynamic = False
    if 'dyn' in _menu_option:
        isDynamic = True        

    if isDynamic:
        menu_GUI = handleDynamicMenu(_menu_option, commands)
    else:
        menu_GUI =  handleStaticMenu(_menu_option, commands)

    return commands, menu_GUI
        

def handleDynamicMenu(_menu_option, commands):
    pass

def handleStaticMenu(_menu_option, commands):
    match _menu_option:
        case 'HELP_MAIN_MENU':
            return cbm._m_help
        case 'example_menu':
            return 'ce zici bai menu 2'
        
        case _:
            raise('Undefined static menu!')

def renderMenu(menu_lines):
    os.system('cls')
    print(menu_lines)


while True:
    available_commands, menu_GUI = handleMenu(APP_ACTIONS_STACK[-1])
    renderMenu(menu_GUI)

    user_input_raw = input()

    if user_input_raw == 'q':
        break
    if user_input_raw == 'b':
        if len(ACTIONS_STACK) > 1:
            ACTIONS_STACK.pop()
        continue
    
    user_input = APP_GRAPH_ACTIONS_MAP[APP_ACTIONS_STACK[-1]][int(user_input_raw) - 1]

    APP_ACTIONS_STACK.append(user_input)



