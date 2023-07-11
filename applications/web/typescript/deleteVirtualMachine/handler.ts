import { RequestHandler } from '../http/requests';


export class HandlerToDeleteVM {

    private container: HTMLElement;
    private buttons: NodeListOf<Element>;
    private requestHandler: RequestHandler;

    constructor(containerSelector: string, buttonSelector: string) {
        this.container = document.querySelector(containerSelector) as HTMLElement;
        this.buttons = this.container.querySelectorAll(buttonSelector);
        this.requestHandler = new RequestHandler();
        this.fetchOnClick = this.fetchOnClick.bind(this);
    }

    private modalAlert(): Promise<boolean> {
        return new Promise((resolve) => {
          const deleteButton = document.getElementById('confirm') as HTMLButtonElement;
          const cancelButton = document.getElementById('cancel') as HTMLButtonElement;

          deleteButton.addEventListener('click', function() {
            resolve(true);
          });
          cancelButton.addEventListener('click', function() {
            resolve(false);
          });
        });
    }

    private async fetchOnClick(event: Event) {
        const button = event.target as HTMLElement;
        const component = button.parentNode?.parentNode as HTMLElement;
        const componentId = component.id;
        const status = await this.requestHandler.makeRequest("DELETE", componentId, {});
        if(status == componentId) component.remove();
    }

    public async addEventListeners() {
        this.buttons.forEach( button => {
            button.addEventListener('click', async (event) => {
                const userPressedRemove = await this.modalAlert();
                if(userPressedRemove) this.fetchOnClick(event)
            });
        });
    }

} // End_class
