import { WebSocketConnector } from "../websocket/connector";

export class HypervisorResourcesMonitor {

    private resourcesTab: NodeListOf<HTMLElement>;
    private webSocket!: WebSocketConnector;
    private url: string;

    constructor() {
        this.resourcesTab = document.querySelectorAll(".tab");
        this.url = "ws://127.0.0.1:8000/ws/some_url/";
    }

    public addEventListenersForResourcesTab() {

        this.webSocket = new WebSocketConnector();
        
        this.resourcesTab.forEach( tab => {
            tab.addEventListener('click', _ => {
                const text = tab.textContent;
                const message = text!.replace(/\s+/g, '').toLowerCase();
                if (message != 'resources') {
                    this.webSocket.close();
                    this.webSocket.connectToWebSocket(this.url, new HtmlHypervisorMonitor());
                    setTimeout( () => {
                        this.webSocket.sendMessage(message);
                    }, 100);
                } else {
                    this.webSocket.close();
                }
            });
        });
    };
}

class HtmlHypervisorMonitor{
    
    private _htmlCpuMonitor:    HTMLElement | null;
    private _htmlMemoryMonitor: HTMLElement | null;
    private _htmlDiskMonitor:   HTMLElement | null;

    constructor(){
        this._htmlCpuMonitor = document.getElementById('menu0');
        this._htmlMemoryMonitor = document.getElementById('menu1');
        this._htmlDiskMonitor = document.getElementById('menu2');
    }

    get cpuArray() {
        return this._htmlCpuMonitor?.querySelectorAll(".cpu-progress-bar") as NodeListOf <HTMLElement>;
    } 

    get memory() {
        return this._htmlMemoryMonitor?.querySelectorAll(".ram-progress-bar") as NodeListOf <HTMLElement>;
    }

    get disk() {
        return this._htmlDiskMonitor?.querySelectorAll(".disk-progress-bar") as NodeListOf <HTMLElement>;
    }

    public update(data: any){
        let i = 0;
        if(document.querySelector('.active')?.textContent=='CPU'){
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                  const value = data[key];
                  this.cpuArray[i].style.width=`${value}%`;
                  this.cpuArray[i].textContent=`${value}%`;
                }
                i++;
            }
        } else if(document.querySelector('.active')?.textContent=='RAM') {
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                  const value = data[key];
                  this.memory[i].style.width=`${value}%`;
                  this.memory[i].textContent=`${value}%`;
                }
                i++;
            }
        } else if(document.querySelector('.active')?.textContent=='Disk'){
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                  const value = data[key];
                  this.disk[i].style.width=`${value}%`;
                  this.disk[i].textContent=`${value}%`;
                }
                i++;
            }
        } else {
            console.log("ERRROR");
        }

    }

}

class VirtualMachineResourcesMonitor{

}

class HtmlVirtualMachineMonitor{

}