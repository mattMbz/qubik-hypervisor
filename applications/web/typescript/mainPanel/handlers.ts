import { PowerOff, Running, VirtualMachine } from './states';
import { WebSocketConnector } from '../websocket/connector';

export class HandlerToMainPanel {

    private virtualMachineComponents: NodeListOf<HTMLInputElement>;
    private webSocketForVCPU!: WebSocketConnector;
    private webSocketForVMemory!: WebSocketConnector;
    private webSocketForVDisk!: WebSocketConnector;
    private initialState!: any;
    private openSockets: boolean;

    constructor() {
        this.virtualMachineComponents = document.querySelectorAll('.vm-component');
        this.openSockets = false;
    }

    public addEventListenersForToggleSwitches() {

        this.virtualMachineComponents.forEach(component => {

            const toggleSwitch = component.querySelector(`#toggle-${component.id}`) as HTMLInputElement;

            // starting the state machine for handle all VMs
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


    public addEventListenerForVMResources() {

        this.virtualMachineComponents.forEach(component => {
            const WEBSOCKET_SERVER_VM: string = process.env.WEBSOCKET_SERVER_VM as string;
            const dropdownMenu = document.querySelector('.dropdown-menu');
    
            const options = {
                root: null, 
                rootMargin: '0px',
                threshold: 0, 
            };
    
            // Create an Intersection Observer with a callback function
            const observer = new IntersectionObserver( (entries) => {

                entries.forEach((entry) => {
                    
                    if (entry.isIntersecting) {
                        this.webSocketForVCPU = new WebSocketConnector();
                        this.webSocketForVMemory = new WebSocketConnector();
                        this.webSocketForVDisk = new WebSocketConnector();
                        this.openSockets = true;
                        console.log(`active -> ${component.id}`);
                        this.webSocketForVCPU.connectToWebSocket(WEBSOCKET_SERVER_VM, new HtmlCPUMonitor(component.id));
                        this.webSocketForVMemory.connectToWebSocket(WEBSOCKET_SERVER_VM, new HtmlVRamMonitor(component.id));
                        this.webSocketForVDisk.connectToWebSocket(WEBSOCKET_SERVER_VM, new HtmlVDiskMonitor(component.id));

                        setTimeout(() => {
                            this.webSocketForVCPU.sendMessage(`vcpu-${component.id}`);
                            this.webSocketForVMemory.sendMessage(`vram-${component.id}`);
                            this.webSocketForVDisk.sendMessage(`vdisk-${component.id}`);
                        }, 2000);

                    } else {
                        console.log(`idle -> ${component.id}`);
                        if (this.openSockets) {
                            this.webSocketForVCPU.close();
                            this.webSocketForVMemory.close();
                            this.webSocketForVDisk.close();
                            this.openSockets = false;
                        }
                    }
                } );
            }, options );
    
            // Observe the dropdown-menu element where we will see the data
            if (dropdownMenu) {
                observer.observe(dropdownMenu);
            }
        });
    }
}


abstract class HtmlVirtualMachineMonitor {

    protected _htmlDropDownMenu: HTMLElement | null;

    constructor(virtualMachineId: string) {
        this._htmlDropDownMenu = document.getElementById(`dropdown-${virtualMachineId}`);
    }

    public abstract update(data: any): void;
}


class HtmlCPUMonitor extends HtmlVirtualMachineMonitor {
    
    private _htmlCpuMonitor: any;

    constructor(virtualMachineId: string) {
        super(virtualMachineId);
        this._htmlCpuMonitor = this._htmlDropDownMenu?.querySelector('.vcpu');
    }

    get cpu() {
        return {
            'vcpusArray': this._htmlCpuMonitor.querySelector('.vcpu-array'),
        }
    }

    public update(data: any): void {
        
        let percentages = 'Not available';

        if(data.message != 'not_available') {
            const vcpusArray = data;
            percentages = '';
            for (let key in vcpusArray) {
                percentages = percentages.concat(`${key}:[${vcpusArray[key]}%] `);
            }
        }
        this.cpu.vcpusArray.textContent=`${percentages}`;
    }

}


class HtmlVRamMonitor extends HtmlVirtualMachineMonitor {

    private _htmlMemoryMonitor: any;

    constructor(virtualMachineId: string) {
        super(virtualMachineId);
        this._htmlMemoryMonitor = this._htmlDropDownMenu?.querySelector('.vram');
    }

    get memory(){
        return {
            'used': this._htmlMemoryMonitor.querySelector(".vram-used"),
            'percentage': this._htmlMemoryMonitor.querySelector(".vram-percent")
        }
    }

    public update(data: any): void {
        let used = 'Not available';
        if (data.message != 'not_available') {
            used = `Used: ${data['Used']} of ${data['Total']} (${data['percentage']}%)`;
        }
        this.memory.used.textContent = used;
    }
}


class HtmlVDiskMonitor extends HtmlVirtualMachineMonitor {

    private _htmlDiskMonitor: any;

    constructor(virtualMachineId: string) {
        super(virtualMachineId);
        this._htmlDiskMonitor = this._htmlDropDownMenu?.querySelector('.vdisk');
    }

    get disk() {
        return {
            'used': this._htmlDiskMonitor.querySelector(".vdisk-used"),
            'percentage': this._htmlDiskMonitor.querySelector(".vdisk-percent")
        }
    }

    public update(data: any): void {
        
        let used = 'Not available';

        if (data.message != 'not_available') {
            used = `Used: ${data['used']} (${data['percentage']}%)`;
        }
        this.disk.used.textContent = used;
    }
}