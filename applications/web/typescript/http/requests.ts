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
  
        let requestType: any = {};

        requestType = {method: this.method, headers: headers};

        if(this.method != 'GET') requestType['body'] = JSON.stringify(body);

        const res = await fetch(endpoint, requestType);
    
        const data = await res.json();
        
        if (res.status !== 200) {
            console.log(data.message , data.status);
        } else {
            console.log(data);
            return data;
        }
    }
} /**End_class */


export class Delete extends HttpRequestHandler {

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


export class Post extends HttpRequestHandler {

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
        } else if (action=='setup'){
            endpoint = process.env.SETUP_VM_ENDPOINT as string;
        }

        const buildEndpoint = (parameter: any) => `${HTTPSERVER}/${endpoint}/${parameter}`;
        return buildEndpoint(parameter);
    }

    public async request(body: any, parameter?: string) {
        const endpoint = this.getEndpoint(body.action, parameter);
        const response = await this.makeRequest(body, endpoint)
        console.log(response);
    }

} /**End_class */


export class Get extends HttpRequestHandler {

    constructor() {
        super('GET')
    }

    getEndpoint(parameter?: string | number ): string {
        const HTTPSERVER = process.env.HTTPSERVER;
        const CHECK_VM_STATUS = process.env.CHECK_VM_STATUS_ENDPOINT;
        const endpoint = (parameter: any) => `${HTTPSERVER}/${CHECK_VM_STATUS}/${parameter}`;
        return endpoint(parameter);
    }

    public async request(body: any, parameter?: string,){ 
        const endpoint = this.getEndpoint(parameter)
        return await this.makeRequest(body, endpoint)
    }

} /**End_class */