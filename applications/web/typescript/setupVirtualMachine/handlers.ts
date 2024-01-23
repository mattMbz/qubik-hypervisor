import { Post } from "../http/requests";

class VirtualMachineSelector {
    private vmSelector: HTMLSelectElement;
    private vmSelectorInvalidMessage: HTMLElement;

    constructor() {
        this.vmSelector = document.getElementById('vm-selector') as HTMLSelectElement;
        this.vmSelectorInvalidMessage = document.querySelector('.invalid-message') as HTMLElement;
    }

    getValue(){
        const vmSelected: string = this.vmSelector.options[this.vmSelector.selectedIndex].textContent || '';
        return vmSelected;
    }

    setClassVMSelector(newClass: string){
        this.vmSelector.classList.add(newClass)
    }

    setClassVmSelectorInvalidMessage(newClass: string) {
        this.vmSelectorInvalidMessage.classList.add(newClass);
    }

    innerMessage(message: string) {
        this.vmSelectorInvalidMessage.innerText=message;
    }

}


class StackRadioSelector {

    private _webServer: NodeListOf<HTMLInputElement>;
    private _appServer: NodeListOf<HTMLInputElement>;
    private _backend: NodeListOf<HTMLInputElement>;
    private _database:  NodeListOf<HTMLInputElement>;
    private _typeScript:  NodeListOf<HTMLInputElement>;

    constructor() {
        this._webServer = document.querySelectorAll('input[type="radio"][name="webserver"]');
        this._appServer = document.querySelectorAll('input[type="radio"][name="appserver"]');
        this._backend = document.querySelectorAll('input[type="radio"][name="backend"]');
        this._database = document.querySelectorAll('input[type="radio"][name="database"]');
        this._typeScript = document.querySelectorAll('input[type="radio"][name="typescript"]');
    }

    get webServer() {
        const webServerArray = Array.from(this._webServer);
        const checkedTechnology = webServerArray.find(technology => technology.checked);
        return checkedTechnology ? checkedTechnology.value : "";
    }

    get appServer() {
        const appServerArray = Array.from(this._appServer);
        const checkedTechnology = appServerArray.find(technology => technology.checked);
        return checkedTechnology ? checkedTechnology.value : "";
    }

    get backend() {
        const backendArray = Array.from(this._backend);
        const checkedTechnology = backendArray.find(technology => technology.checked);
        return checkedTechnology ? checkedTechnology.value : "";
    }

    get database() {
        const databaseArray = Array.from(this._database);
        const checkedTechnology = databaseArray.find(technology => technology.checked);
        return checkedTechnology ? checkedTechnology.value : "";
    }

    get typescript() {
        const typeScriptArray = Array.from(this._typeScript);
        const checkedTechnology = typeScriptArray.find(technology => technology.checked);
        return checkedTechnology ? checkedTechnology.value : "";
    }

}


export class VirtualMachineSetup {

    private installButton: HTMLElement;
    private virtualMachineSelector: VirtualMachineSelector;
    private stackRadioSelector: StackRadioSelector;
    private post: Post;

    constructor() {
        this.installButton = document.getElementById('install')!;
        this.virtualMachineSelector = new VirtualMachineSelector();
        this.stackRadioSelector = new StackRadioSelector();
        this.post = new Post()
    }

    public async addEventListener(){
        this.installButton.addEventListener('click', async (event: Event) => {
            event.preventDefault();
            let vm = this.virtualMachineSelector.getValue();
            if(vm.includes('-- Choose an option --')) {
                    this.virtualMachineSelector.setClassVMSelector('invalid-input');
                    this.virtualMachineSelector.innerMessage("* You must choose a virtual machine");
                    this.virtualMachineSelector.setClassVmSelectorInvalidMessage('invalid-message');
            } else {
                const virtualMachine = this.virtualMachineSelector.getValue().split('-');
                const virtualMachineName = virtualMachine[0].split(" ");
                const virtualMachineObject = {
                    "vmName": virtualMachineName[1],
                    "appName": virtualMachine[1],
                    "uuid": virtualMachine[2]
                }

                let stack = {}

                stack = {
                    "webServer": this.stackRadioSelector.webServer,
                    "appServer": this.stackRadioSelector.appServer,
                    "backend": this.stackRadioSelector.backend,
                    "database": this.stackRadioSelector.database,
                    "typeScript": this.stackRadioSelector.typescript
                }
                const choice = {
                    action: 'setup',
                    virtualMachine: virtualMachineObject,
                    stack: stack
                }

                console.log(choice);
                
                const response = await this.post.request(choice, virtualMachineObject.uuid);
            }
        });
    }

}
