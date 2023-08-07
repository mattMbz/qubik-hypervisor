abstract class HttpRequestHandler {

    protected method: string;

    constructor(method: string){
        this.method = method;
    }

    protected abstract getEndpoint(action: string, parameter: string | number ): string;

    protected async makeRequest(body: any, endpoint: string) {
        let headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
            'X-CSRFToken': ''
        }
       
        // Setting Django CSRF-Token
        const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]') as HTMLInputElement;
        const csrf: string = csrfElement?.value || '';
        headers['X-CSRFToken'] =  csrf;
  
        const res = await fetch(endpoint, {
            method: this.method,
            headers: headers,
            body: body
        });
    
        const data = await res.json();
        
        if (res.status !== 200) {
            console.log(data.message , data.status);
        } else {
            // console.log(data);
            return data;
        }
    }
} /**End_class */


export class DeleteRequest extends HttpRequestHandler {

    constructor() {
        super('DELETE')
    }

    getEndpoint(parameter?: string | number ): string {
        const HTTPSERVER = process.env.HTTPSERVER;
        const DELETE_VM_ENDPOINT = process.env.DELETE_VM_ENDPOINT;
        const endpoint = (parameter: any) => `${HTTPSERVER}/${DELETE_VM_ENDPOINT}/${parameter}`;
        return endpoint(parameter);
    }

    public async request(body: any, parameter?: string,){ 
        const endpoint = this.getEndpoint(parameter)
        return await this.makeRequest(body, endpoint)
    }

} /**End_class */


export class PostRequest extends HttpRequestHandler {

    constructor() {
        super('POST')
    }

    protected getEndpoint( action: string, parameter?: string | number ): string {
        const HTTPSERVER = process.env.HTTPSERVER;
        let endpoint: string;

        if (action =='start'){
            endpoint = process.env.START_VM_ENDPOINT as string;
        } else if (action=='shutdown') {
            endpoint = process.env.SHUTDOWN_VM_ENDPOINT as string;
        }

        const buildEndpoint = (parameter: any) => `${HTTPSERVER}/${endpoint}/${parameter}`;
        return buildEndpoint(parameter);
    }

    public async request(body: any, parameter?: string) {
        const endpoint = this.getEndpoint(body.action, parameter);
        const response = await this.makeRequest(body, endpoint)
        console.log(`Recibido <- ${response}`);
    }

} /**End_class */