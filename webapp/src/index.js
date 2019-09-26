import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import './index.css'

class App extends Component {
    render() {
        return (
            <div className="App">
                <h1 className="main-header">Hello There!</h1>
            </div>
        )
    }
}

ReactDOM.render(<App/>, document.getElementById('root'));

let ws = new WebSocket('ws://' + document.domain + ':' + location.port + '/test', 'foo');

ws.onopen = function(event) {
    ws.send("{\"text\": \"I am foo!\"}");
};

ws.onmessage = function(event) {
    console.log(event.data);
};
