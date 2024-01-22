export class CreationVMButtonInteraction {
    
    private createNewVmButton: HTMLElement;

    constructor(){
        this.createNewVmButton = document.getElementById('create-vm-btn')!;
    }

    public addEventListener(){
        this.createNewVmButton.addEventListener('click', function(){
            const vmNameInput = document.getElementById('virtualMachineName') as HTMLInputElement;
            const vmApplicationNameInput = document.getElementById('applicationName') as HTMLInputElement;
            const bootstrap5Loader = document.getElementById('loader')!;
            const waitMessage = document.getElementById('wait')!;
            if(vmNameInput.value.trim() != '' && vmApplicationNameInput.value.trim() != '') {
                this.innerHTML = '<span class="spinner-border spinner-border-sm" id="loader"></span> Creating vm';
                // bootstrap5Loader.hidden = false;
                waitMessage.hidden = false;
            }
        });
    }
}