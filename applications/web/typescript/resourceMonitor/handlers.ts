import { WebSocketConnector } from "../websocket/connector";


export class HypervisorResourcesMonitor {

    private resourcesTab: NodeListOf<HTMLElement>;
    private webSocket!: WebSocketConnector;

    constructor() {
        this.resourcesTab = document.querySelectorAll(".tab");
    }

    public addEventListenersForResourcesTab() {

        this.webSocket = new WebSocketConnector();
        const WEBSOCKET_SERVER: string = process.env.WEBSOCKET_SERVER as string;

        this.resourcesTab.forEach(tab => {
            tab.addEventListener('click', _ => {
                const text = tab.textContent;
                const message = text!.replace(/\s+/g, '').toLowerCase();
                if (message != 'resources') {
                    this.webSocket.close();
                    this.webSocket.connectToWebSocket(WEBSOCKET_SERVER, new HtmlHypervisorMonitor());
                    setTimeout(() => {
                        this.webSocket.sendMessage(message);
                    }, 100);
                } else {
                    this.webSocket.close();
                }
            });
        });
    };
}


class HtmlHypervisorMonitor {

    private _htmlCpuMonitor: HTMLElement | null;
    private _htmlMemoryMonitor: HTMLElement | null;
    private _htmlDiskMonitor: HTMLElement | null;

    constructor() {
        this._htmlCpuMonitor = document.getElementById('menu0');
        this._htmlMemoryMonitor = document.getElementById('menu1');
        this._htmlDiskMonitor = document.getElementById('menu2');
    }

    get cpuArrays() {
        return {
            'cpuProgressBar': this._htmlCpuMonitor?.querySelectorAll(".cpu-progress-bar") as NodeListOf<HTMLElement>,
            'percentCpu': this._htmlCpuMonitor?.querySelectorAll(".percent-cpu") as NodeListOf<HTMLElement>,
        } 
        
    }

    get memory() {
        return  {
            'memoryProgressBar': this._htmlMemoryMonitor!.querySelector(".ram-progress-bar") as HTMLElement,
            'usedMemory': this._htmlMemoryMonitor!.querySelector(".used-memory") as HTMLElement,
            'totalMemory': this._htmlMemoryMonitor!.querySelector(".total-memory") as HTMLElement,
            'percentMemory': this._htmlMemoryMonitor!.querySelector(".percent-memory") as HTMLElement,
        }
    }

    get disk() {
        return {
            'diskProgressBar': this._htmlDiskMonitor!.querySelector(".disk-progress-bar") as HTMLElement,
            'usedDisk': this._htmlDiskMonitor!.querySelector(".used-disk") as HTMLElement,
            'totalDisk': this._htmlDiskMonitor!.querySelector(".total-disk") as HTMLElement,
            'percentDisk': this._htmlDiskMonitor!.querySelector(".percent-disk") as HTMLElement
        } 
    }

    public update(data: any) {

        let i = 0;

        if (document.querySelector('.active')?.textContent == 'CPU') {
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                    const value = data[key];
                    this.cpuArrays.percentCpu[i].textContent = ` ${Math.floor(value)}%`;
                    this.cpuArrays.cpuProgressBar[i].style.width = `${Math.floor(value)}%`;
                    // this.cpuArrays.cpuProgressBar[i].textContent = `${Math.floor(value)}%`;
                }
                i++;
            }
        } else if (document.querySelector('.active')?.textContent == 'RAM') {
            const used = data['used'];
            const available = data['available'];
            const percentage = data['percentage'];
            this.memory.usedMemory.textContent = `Used Memory: ${used}`;
            this.memory.totalMemory.textContent = `Total: ${available}`;
            this.memory.percentMemory.textContent = `Used: ${percentage}%`;
            this.memory.memoryProgressBar.style.width = `${percentage}%`;
            this.memory.memoryProgressBar.textContent = `${Math.floor(percentage)}%`;

        } else if (document.querySelector('.active')?.textContent == 'Disk') {
            const used = data['used'];
            const available = data['available'];
            const percentage = data['percentage'];
            this.disk.usedDisk.textContent = `Size HD used: ${used}`;
            this.disk.totalDisk.textContent = `Total: ${available}`;
            this.disk.percentDisk.textContent = `Used ${percentage}`;
            this.disk.diskProgressBar.style.width = `${percentage}`;
            this.disk.diskProgressBar.textContent = `${percentage}`;

        } else {
            console.log("ERRROR");
        }

    }
}

class VirtualMachineResourcesMonitor {}

class HtmlVirtualMachineMonitor {}