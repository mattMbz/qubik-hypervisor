export class WebSocketConnector {

  public socket!: WebSocket;

  public connectToWebSocket(url: string, html: any) {

    this.socket = new WebSocket(url);

    this.socket.onopen = function (event) {
      console.log("WebSocket CONNECTED");
    };

    this.socket.onmessage = function (event) {
      var data = JSON.parse(event.data);
      // console.log(data);
      html.update(data);
    };

    this.socket.onclose = function (event) {
      console.log("WebSocket DISCONNECTED");
    };

  }

  public sendMessage(mssg: string) {
    this.socket.send(mssg)
  }

  public close() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log('Cerrando el websocket...');
        this.socket.send('stop');
        this.socket.close();
      console.log('WebSocket is Closed!');
    }
  }

}