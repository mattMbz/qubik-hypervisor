export class RequestHandler {
    
    constructor(){}

    private getEndpoint(parameter: string | number ): string {
        const HTTPSERVER = process.env.HTTPSERVER;
        const DELETE_VM_ENDPOINT = process.env.DELETE_VM_ENDPOINT;
        const endpoint = (parameter: any) => `${HTTPSERVER}/${DELETE_VM_ENDPOINT}/${parameter}`;
        return endpoint(parameter);
    }

    public async makeRequest(method: 'DELETE' | 'POST', parameter: string, body: any) {
        let headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
            'X-CSRFToken': ''
        }
       
        // Setting Django CSRF-Token
        const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]') as HTMLInputElement;
        const csrf: string = csrfElement?.value || '';
        headers['X-CSRFToken'] =  csrf;

        const res = await fetch(this.getEndpoint(parameter), {
            method: method,
            headers: headers,
            body: body
        });
    
        const data = await res.json();
        
        if (res.status !== 200) {
            console.log(data.message , data.status);
        } else {
            return data.status;
        }
    }

} /** End_class */