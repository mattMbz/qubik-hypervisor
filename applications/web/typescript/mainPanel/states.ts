import {
    secondaryBadge,
    successBadge,
    warningBadge,
    smallSpinner,
    dangerBadge
} from '../html/HTMLComponents';

export class Context {

    private state: State;
    private _virtualMachine: VirtualMachine;

    constructor(state: State, virtualMachine: VirtualMachine) {
        this.state = state;
        this._virtualMachine = virtualMachine;
        this.transitionTo(this.state);
    }

    public transitionTo(state: State): void {
        this.state = state;
        this.state.setContext(this);
    }

    public next(): void {
        this.state.next();
    }

    get virtualMachine(): VirtualMachine {
        return this._virtualMachine;
    }
}


abstract class State {

    protected context!: Context;
    protected _description: string;
    protected _action: string;

    constructor(description: string, action: string) {
        this._description = description;
        this._action = action;
    }

    public setContext(context: Context) {
        this.context = context;
    }

    public abstract next(): void;
}


export class PowerOff extends State {

    private _finalState : boolean = false;

    constructor() {
        super('Power OFF', '');
    }

    get description(): string {
        return this._description;
    }

    set finalState(value: boolean) {
        this._finalState = value;
    }

    public next(): void {

        // Extract Elements from the context
        const HTMLVirtualMachine = this.context.virtualMachine.HTMLVirtualMachine;
        const virtualMachineId = this.context.virtualMachine.id;
        console.log(`ID: ${virtualMachineId} is ${this.description}`);

        const statusBadge = HTMLVirtualMachine.querySelector(`.status-${virtualMachineId}`) as HTMLElement;

        // Transition Messages
        if (statusBadge !== null) statusBadge.innerHTML = secondaryBadge(this._description);

        // Transition to Starting State
        const nextState = new Starting();
        this.context.transitionTo(nextState);
        this._finalState ? null : this.context.virtualMachine.context.next();
    }
}


class Starting extends State {

    constructor() {
        super('Starting...', 'Loading app...');
    }

    get description(): string {
        return this._description;
    }

    public next(): void {

        // Extract Elements from the context
        const HTMLVirtualMachine = this.context.virtualMachine.HTMLVirtualMachine;
        const virtualMachineId = this.context.virtualMachine.id;
        console.log(`ID: ${virtualMachineId} is ${this.description}`);

        // Defining auxiliary variables
        let loop = true;
        const toggleSwitch = HTMLVirtualMachine.querySelector(`#toggle-${virtualMachineId}`) as HTMLInputElement;
        const statusBadge = HTMLVirtualMachine.querySelector(`.status-${virtualMachineId}`) as HTMLElement;
        const virtualMachineInfo = HTMLVirtualMachine.querySelector('.vm-info') as HTMLElement;
        let savedVirtualMachineInfo: any;

        if (HTMLVirtualMachine !== null) {
            savedVirtualMachineInfo = HTMLVirtualMachine.querySelector('.vm-info')?.cloneNode(true);
        }

        toggleSwitch.disabled = true;

        // Transition Messages
        if (statusBadge !== null) statusBadge.innerHTML = warningBadge(this._description);

        if (virtualMachineInfo !== null) {
            virtualMachineInfo.innerHTML = '';
            virtualMachineInfo.innerHTML = smallSpinner(this._action);
        }

        const startInterval = setInterval(() => {
            if (loop) {
                console.log("Consultado API: vm_State");
            } else {
                clearInterval(startInterval);
                toggleSwitch.disabled = false;

                if (virtualMachineInfo !== null) {
                    while (virtualMachineInfo.firstChild) {
                        virtualMachineInfo.removeChild(virtualMachineInfo.firstChild);
                    }
                    virtualMachineInfo.append(savedVirtualMachineInfo);
                }
                // Transition to Running State
                const nextState = new Running();
                nextState.finalState = true;
                this.context.transitionTo(nextState);
                this.context.virtualMachine.context.next();
            }
        }, 5000);

        // Simula el cambio de loop después de 15 segundos
        setTimeout(() => {
            loop = false;
        }, 15000);
    }
}

export class Running extends State {

    private _finalState : boolean = false;

    constructor() {
        super('Running','');
    }

    get description(): string {
        return this._description;
    }

    set finalState(value: boolean) {
        this._finalState = value;
    }

    public next(): void {
        // Extract Elements from the context
        const HTMLVirtualMachine = this.context.virtualMachine.HTMLVirtualMachine;
        const virtualMachineId = this.context.virtualMachine.id;

        const statusBadge = HTMLVirtualMachine.querySelector(`.status-${virtualMachineId}`) as HTMLElement;

        console.log(`ID: ${virtualMachineId} is ${this._description}`);

        // Transition Messages
        if (statusBadge !== null) statusBadge.innerHTML = successBadge(this._description);

        // Transition to Shutting Down state
        const nextState = new ShuttingDown();
        this.context.transitionTo(nextState);
        this._finalState ? null : this.context.virtualMachine.context.next();
    }
}


class ShuttingDown extends State {

    constructor() {
        super( 'Shutting Down...','Closing...');
    }

    get description(): string {
        return this._description;
    }

    public next(): void {

        // Extract Elements from the context
        const HTMLVirtualMachine = this.context.virtualMachine.HTMLVirtualMachine;
        const virtualMachineId = this.context.virtualMachine.id;
        console.log(`ID: ${virtualMachineId} is ${this.description}`);

        // Defining auxiliary variables
        let loop = true;
        const toggleSwitch = HTMLVirtualMachine.querySelector(`#toggle-${virtualMachineId}`) as HTMLInputElement;
        const statusBadge = HTMLVirtualMachine.querySelector(`.status-${virtualMachineId}`) as HTMLElement;
        const virtualMachineInfo = HTMLVirtualMachine.querySelector('.vm-info') as HTMLElement;
        let savedVirtualMachineInfo: any;

        if (HTMLVirtualMachine !== null) {
            savedVirtualMachineInfo = HTMLVirtualMachine.querySelector('.vm-info')?.cloneNode(true);
        }

        toggleSwitch.disabled = true;

        // Transition Messages
        if (statusBadge !== null) statusBadge.innerHTML = dangerBadge(this._description);

        if (virtualMachineInfo !== null) {
            virtualMachineInfo.innerHTML = '';
            virtualMachineInfo.innerHTML = smallSpinner(this._action);
        }

        const startInterval = setInterval(() => {
            if (loop) {
                console.log("Consultado API: vm_State");
            } else {
                clearInterval(startInterval);
                toggleSwitch.disabled = false;

                if (virtualMachineInfo !== null) {
                    while (virtualMachineInfo.firstChild) {
                        virtualMachineInfo.removeChild(virtualMachineInfo.firstChild);
                    }
                    virtualMachineInfo.append(savedVirtualMachineInfo);
                }
                // Transition to Power OFF state
                const nextState = new PowerOff();
                nextState.finalState=true;
                this.context.transitionTo(nextState);
                this.context.virtualMachine.context.next();
            }
        }, 5000);

        // Simula el cambio de loop después de 15 segundos
        setTimeout(() => {
            loop = false;
        }, 15000)
    }
}


export class VirtualMachine {

    public context: Context;
    private _id: string;
    private _HTMLVirtualMachine!: HTMLElement;

    constructor(state: State, id: string) {
        this._id = id;
        this._HTMLVirtualMachine = document.querySelector(`#${this._id}`)!;
        this.context = new Context(state, this);
    }

    get id(): string {
        return this._id;
    }

    get HTMLVirtualMachine() {
        return this._HTMLVirtualMachine;
    }
}