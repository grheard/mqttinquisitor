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
