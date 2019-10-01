import React, {Component} from 'react';


function MessageList(props) {
    let messages = props.messages;
    const listItems = messages.map((message) =>
      <li>{message}</li>
    );
    return (
      <ul>{listItems}</ul>
    );
}


export class App extends Component {
    constructor() {
        super();

        this.state = {
            messages: []
        };

        this.ws = new WebSocket('ws://' + document.domain + ':' + location.port);

        this.ws.onopen = (event) => {
            this.ws.send("{\"text\": \"I am foo!\"}");
        };

        this.ws.onmessage = (event) => {
            console.log(event.data);
            let msg = this.state.messages;
            let data = JSON.parse(event.data);
            let payload = '';
            try {
                payload = JSON.stringify(JSON.parse(data.payload));
            }
            catch (e) {
                payload = data.payload;
            }
            let s = data.ts + " :: " + data.topic + " :: " + payload;
            msg.unshift(s);
            this.setState({messages: msg});
        };
    }

    render() {
        return (
            <div className="App">
                <h1 className="main-header">Hello There!</h1>
                <MessageList messages={this.state.messages} />
            </div>
        );
    }
}
