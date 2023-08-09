import {PowerOff, Running, VirtualMachine} from './states';


export class HandlerToMainPanel {
    
    private virtualMachineComponents: NodeListOf<HTMLInputElement>;
    private initialState!: any; 
    
    constructor() {
        this.virtualMachineComponents = document.querySelectorAll('.vm-component');
    }

    public addEventListenersForToggleSwitches() {
        this.virtualMachineComponents.forEach( component => {
            
            const toggleSwitch = component.querySelector(`#toggle-${component.id}`) as HTMLInputElement;
            
            if (toggleSwitch.checked) {
                this.initialState = new Running();
            } else {
                this.initialState = new PowerOff();
            }
            console.log(component.id);
            const virtualMachine = new VirtualMachine(this.initialState, component.id);

            console.log(`ID: ${component.id} is ${this.initialState.description}`);

            toggleSwitch.addEventListener('change', () => {
                virtualMachine.context.next();
            });

        });
    }
}
