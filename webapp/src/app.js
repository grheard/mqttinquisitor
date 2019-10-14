import React, {Component} from 'react';
import InfiniteScroll from "react-infinite-scroll-component";


function MessageList(props) {
    let messages = props.messages;
    const listItems = messages.map((message) =>
        <React.Fragment>
        <tr align="left"><td>{message.ts}</td><td>{message.topic}</td><td>{message.payload}</td></tr>
        </React.Fragment>
    );
    return (
        <table cellPadding="5">
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
            items: []
            , hasMore: true
        };

        this.ws = new WebSocket('ws://' + document.domain + ':' + location.port);

        this.ws.onopen = (event) => {
            if (this.state.items.length === 0) {
                this.query(undefined,100);
            }
        };

        this.ws.onmessage = (event) => {
            console.log(event.data);
            this.processMessage(event.data);
        };
    }


    processMessage(message) {
        let data = JSON.parse(message);

        if (data.msgtype !== 'query') {
            data.payload = this.parsePayload(data.payload);
            let msg = this.state.items;
            msg.unshift(data);
            this.setState({items: msg});
        }
        else {
            this.parseQuery(data);
        }
    }


    parseQuery(query) {
        if (query.results.length === 0) {
            this.setState({hasMore: false});
            return;
        }

        let msg = [];
        for (const m of query.results) {
            m.payload = this.parsePayload(m.payload);
            msg.push(m);
        }
        this.setState({items: this.state.items.concat(msg)});
    }


    parsePayload(payload) {
        let _payload = '';
        try {
            // If the payload was JSON it will get escaped by
            // the encoder on the other end. By parsing and
            // stringify'ing it, the escapes will be removed.
            _payload = JSON.stringify(JSON.parse(payload));
        }
        catch (e) {
            // The payload wasn't JSON.
            _payload = payload;
        }
        return _payload;
    }


    query(ts, count) {
        let m = {"msgtype": "query", "count": count};
        if (ts !== undefined) {
            m.ts = ts;
        }
        this.ws.send(JSON.stringify(m));
    }


    fetch() {
        let ts = this.state.items[this.state.items.length - 1].ts;
        this.query(ts,30);
    }


    onScroll() {
        let el = document.getElementsByClassName("infinite-scroll-component ");
        if (el[0].scrollTop === 0) {
            console.log("To the Top!");
        }
    }


    render() {
        return (
            <div className="App">
                <h3 className="main-header">mqttinquisitor</h3>
                <InfiniteScroll
                    dataLength={this.state.items.length}
                    next={this.fetch.bind(this)}
                    onScroll={this.onScroll.bind(this)}
                    hasMore={this.state.hasMore}
                    loader={<h4>Loading...</h4>}
                    endMessage={
                        <p style={{ textAlign: "center" }}>
                        <b>The End.</b>
                        </p>
                    }
                >
                    <MessageList messages={this.state.items} />
                </InfiniteScroll>
            </div>
        );
    }
}
