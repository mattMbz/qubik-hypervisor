import { RequestHandler } from '../http/requests';


export class HandlerToDeleteVM {

    private container: HTMLElement;
    private buttons: NodeListOf<Element>;
    private requestHandler: RequestHandler;
    private handleToSearching: HandlerToSearching;

    constructor(containerSelector: string, buttonSelector: string) {
        this.handleToSearching = new HandlerToSearching('#searcherInput');
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
                if(userPressedRemove) {
                    this.fetchOnClick(event);
                    this.handleToSearching.reload();
                }
            });
        });
    }

} // End_class


export class HandlerToSearching {

    private searcherInput: HTMLInputElement;

    constructor(searcherInputId: string){
        this.searcherInput = document.querySelector(searcherInputId) as HTMLInputElement;
    }

    public reload() {
        location.reload();
    }

    private filterList = () => {
        var filterTxt: string;
        var virtualMachineDiv: HTMLElement;
        var i: number, txtValue;
        const li = document.getElementsByClassName('vm-item') as HTMLCollectionOf<HTMLElement>;

        filterTxt = this.searcherInput.value.toUpperCase();

        // Loop through all list items, and hide those who don't match the search query
        for(i=0; i < li.length; i++) {
            virtualMachineDiv = li[i].querySelector('.vm-name') as HTMLElement;
            txtValue = virtualMachineDiv.textContent as string;
            if(txtValue.toUpperCase().indexOf(filterTxt) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }

    }

    public addEventListenerForSearcherInput() {
        this.searcherInput.addEventListener( 'keyup', this.filterList);
        
        // Disable spell checker
        this.searcherInput.spellcheck = false;
    }

} // End_class