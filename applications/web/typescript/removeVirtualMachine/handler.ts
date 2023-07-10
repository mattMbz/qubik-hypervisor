import { RequestHandler } from '../http/requests';


export class HandlerToRemoveVM {

    private container: HTMLElement;
    private buttons: NodeListOf<Element>;
    private requestHandler: RequestHandler;

    constructor(containerSelector: string, buttonSelector: string) {
        this.container = document.querySelector(containerSelector) as HTMLElement;
        this.buttons = this.container.querySelectorAll(buttonSelector);
        this.requestHandler = new RequestHandler();
        this.fetchOnClick = this.fetchOnClick.bind(this);
    }
 
    private async fetchOnClick(event: Event) {
        const button = event.target as HTMLElement;
        const component = button.parentNode?.parentNode as HTMLElement;
        const componentId = component.id;
        console.log(componentId);
        const status = await this.requestHandler.makeRequest("DELETE", componentId, {});
        if(status == componentId) component.remove();
    }

    public addEventListeners() {
        this.buttons.forEach( button => {
            button.addEventListener('click', this.fetchOnClick);
        });
    }

} // End_class
