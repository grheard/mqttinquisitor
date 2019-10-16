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

        this.pause = false;

        this.connect();
    }


    connect() {
        this.ws = new WebSocket('ws://' + document.domain + ':' + location.port);
        this.ws.onopen = this.onOpen.bind(this);
        this.ws.onmessage = this.onMessage.bind(this);
        this.ws.onclose = this.onClose.bind(this);
    }


    onOpen(event) {
        if (this.state.items.length === 0) {
            this.query(undefined,100);
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
        console.debug(event.data);
        this.processMessage(event.data);
    }


    processMessage(message) {
        let data = JSON.parse(message);

        if (data.msgtype !== 'query') {
            if (!this.pause) {
                data.payload = this.parsePayload(data.payload);
                let msg = this.state.items;
                msg.unshift(data);
                this.setState({items: msg});
            }
            else {
                this.evaluatePause();
            }
        }
        else {
            this.parseQuery(data);
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
            this.setState({items: msg.concat(this.state.items).slice(0,101)});
        }
        else {
            this.setState({items: this.state.items.concat(msg)});
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
        this.ws.send(JSON.stringify(m));
    }


    fetch() {
        let ts = this.state.items[this.state.items.length - 1].ts;
        this.query(ts,30);
    }


    evaluatePause() {
        let el = document.getElementById("scrollableDiv");
        console.log("scrollTop = " + el.scrollTop);
        if (el.scrollTop === 0) {
            this.query(this.state.items[0].ts,undefined,true);
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
