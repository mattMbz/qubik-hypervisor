import { Delete } from '../http/requests';


export class HandlerToDeleteVM {

    private container: HTMLElement;
    private buttons: NodeListOf<Element>;
    private delete: Delete;
    private handleToSearching: HandlerToSearching;

    constructor(containerSelector: string, buttonSelector: string) {
        this.handleToSearching = new HandlerToSearching('#searcherInput');
        this.container = document.querySelector(containerSelector) as HTMLElement;
        this.buttons = this.container.querySelectorAll(buttonSelector);
        this.delete = new Delete();
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
        const response = await this.delete.request({}, componentId);
        if(response.status == componentId)component.remove();
        return response;
    }

    public async addEventListeners() {
        this.buttons.forEach( button => {
            button.addEventListener('click', async (event) => {
                const userPressedRemove = await this.modalAlert();
                if(userPressedRemove) {
                    const response = await this.fetchOnClick(event);
                    if(response.status != 'error'){
                        this.handleToSearching.reload();
                    } else {
                        const messagesDiv = document.querySelector('.delete-alert');
                        if(messagesDiv) {
                            messagesDiv.innerHTML='';
                            const alertDiv = document.createElement('div');
                            alertDiv.className = 'alert alert-warning';
                            alertDiv.innerHTML = `<strong>Warning!</strong> ${response.message}`;
                            messagesDiv?.appendChild(alertDiv);
                        }
                    }
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