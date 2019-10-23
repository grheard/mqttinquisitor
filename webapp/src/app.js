import React, {Component} from 'react';
import InfiniteScroll from "react-infinite-scroll-component";


const QUERY_ALL = undefined
const QUERY_INITIAL_COUNT = 100;
const QUERY_ADDITIONAL_COUNT = 50;
const TRIM_COUNT = 199;


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

        this.pause = false;

        this.connect();
    }


    connect() {
        this.ws = new WebSocket('ws://' + document.domain + ':' + location.port);
        this.ws.onopen = this.onOpen.bind(this);
        this.ws.onmessage = this.onMessage.bind(this);
        this.ws.onclose = this.onClose.bind(this);
    }


    send(message) {
        let msg = JSON.stringify(message)
        console.debug('send: ' + msg);
        this.ws.send(msg);
    }


    onOpen(event) {
        if (this.state.items.length === 0) {
            this.query(undefined,QUERY_INITIAL_COUNT);
        }
    }


    onClose(event) {
        this.pause = false;
        this.setState({items: [], hasMore: true});
        setTimeout(() => {
            this.connect();
        }, 3000);
    }


    onMessage(event) {
        console.debug('recv: ' + event.data);
        this.processMessage(event.data);
    }


    processMessage(message) {
        let data = JSON.parse(message);

        if (data.msgtype === 'mqtt'
            || data.msgtype === 'status') {
                this.parseData(data);
        }
        else if (data.msgtype === 'query') {
            this.parseQuery(data);
        }
    }


    parseData(data) {
        if (!this.pause) {
            data.payload = this.parsePayload(data.payload);
            let msg = this.state.items;
            if (msg.length > TRIM_COUNT) {
                msg.length = TRIM_COUNT;
            }
            msg.unshift(data);
            this.setState({items: msg});
        }
        else {
            this.evaluatePause();
        }
    }


    parseQuery(query) {
        if (query.results.length === 0) {
            if (!query.gt) {
                this.setState({hasMore: false});
            }
            return;
        }

        let msg = [];
        for (const m of query.results) {
            m.payload = this.parsePayload(m.payload);
            msg.push(m);
        }
        if (query.gt) {
            this.pause = false;
            this.setState({items: msg.concat(this.state.items).slice(0,TRIM_COUNT)});
        }
        else {
            this.setState({items: this.state.items.concat(msg), hasMore: (query.results.length >= QUERY_ADDITIONAL_COUNT)});
        }
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


    query(ts, count, gt) {
        let m = {"msgtype": "query"};
        if (ts !== undefined) {
            m.ts = ts;
        }
        if (count !== undefined) {
            m.count = count;
        }
        if (gt !== undefined) {
            m.gt = gt;
        }
        this.send(m);
    }


    fetch() {
        let ts = this.state.items[this.state.items.length - 1].ts;
        this.query(ts,QUERY_ADDITIONAL_COUNT);
    }


    evaluatePause() {
        let el = document.getElementById("scrollableDiv");
        console.log("scrollTop = " + el.scrollTop);
        if (el.scrollTop === 0) {
            this.query(this.state.items[0].ts,QUERY_ALL,true);
        }
        else {
            this.pause = true;
        }
    }


    onScroll() {
        this.evaluatePause();
    }


    render() {
        return (
            <div className="App">
                <h3 className="main-header">mqttinquisitor</h3>
                <div id="scrollableDiv">
                    <InfiniteScroll
                        dataLength={this.state.items.length}
                        next={this.fetch.bind(this)}
                        onScroll={this.onScroll.bind(this)}
                        hasMore={this.state.hasMore}
                        loader={<h4>Loading...</h4>}
                        scrollableTarget="scrollableDiv"
                        endMessage={
                            <p style={{ textAlign: "center" }}>
                            <b>The End.</b>
                            </p>
                        }
                    >
                        <MessageList messages={this.state.items} />
                    </InfiniteScroll>
                </div>
            </div>
        );
    }
}
