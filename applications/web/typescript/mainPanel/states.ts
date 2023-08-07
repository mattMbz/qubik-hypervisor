export class Context {

    private state: State;

    constructor(state: State) {
        this.state = state;
        this.transitionTo(this.state);
    }

    public transitionTo(state: State): void {
        this.state = state;
        this.state.setContext(this);
    }

    public next(): void {
        this.state.next();
    }
}


abstract class State {
    protected context!: Context;

    public setContext(context: Context) {
        this.context = context;
    }

    public abstract next(): void;
}


export class PowerOff extends State {

    public next(): void {
        console.log("Starting...");
        // Transition to Starting State
        const state = new Starting()
        this.context.transitionTo(state)
    }
}


class Starting extends State {

    public next(): void {
        console.log('Running...');
        const state = new Running()
        this.context.transitionTo(state)
    }
}


export class Running extends State {
    public next(): void {
        console.log('Shutting Down...');
        this.context.transitionTo(new ShuttingDown());
    }
}


class ShuttingDown extends State {

    public next(): void {
        console.log('Power off...');
        this.context.transitionTo(new PowerOff());
    }
}


export class VirtualMachine {

    public context: Context;

    constructor(state: State){
        this.context = new Context(state);
    }   
}