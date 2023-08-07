from tlk.utilities.menu import CustomMenu

# Complete the header information inside the list
header = [
    'Qubik Hypervisor version 1.0.0',
    'Author: Matias Barboza',
    'GNU General Public License v3.0'
]

# Complete the menu items inside the items list
items = [
    'Create   VM',
    'Remove   VM',
    'Rename   VM',
    'Start    VM',
    'Shutdown VM',
    'List     VM',
    'Monitor',
    'Exit'
]


if __name__=='__main__':
    hypervisorMenu = CustomMenu()
    hypervisorMenu.show(header, items)

# END
