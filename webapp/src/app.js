import React, {Component} from 'react';


function MessageList(props) {
    let messages = props.messages;
    const listItems = messages.map((message) =>
        <React.Fragment>
        <tr align="left"><td>{message.ts}</td><td>{message.topic}</td><td>{message.payload}</td></tr>
        </React.Fragment>
    );
    return (
        <table cellPadding="10">
            <thead>
                <tr align="left">
                    <th>Timestamp</th>
                    <th>Topic</th>
                    <th>Payload</th>
                </tr>
            </thead>
            <tbody>
                {listItems}
            </tbody>
        </table>
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
                // If the payload was JSON it will get escaped by
                // the encoder on the other end. By parsing and
                // stringify'ing it, the escapes will be removed.
                payload = JSON.stringify(JSON.parse(data.payload));
            }
            catch (e) {
                // The payload wasn't JSON.
                payload = data.payload;
            }
            data.payload = payload;
            msg.unshift(data);
            this.setState({messages: msg});
        };
    }

    render() {
        return (
            <div className="App">
                <h3 className="main-header">mqttinquisitor</h3>
                <MessageList messages={this.state.messages} />
            </div>
        );
    }
}
