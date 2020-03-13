import React, {Component} from 'react';
import './utils/config';
import * as request from 'superagent';
import {Button, Grid, Header, Segment} from "semantic-ui-react";
import FooterLoader from "./footer/footer-loader";
import CanvasDraw from "./canvas-draw/canvas-draw";
import api from "./utils/superagent-api";
import {toBlob} from "./utils/image";
import {apiDelay} from "./utils/test-api-delay";
import './App.css';
import MenuBar from "./menu/menu";

export class App extends Component {

    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return <div className="main-content-pushable">
            <MenuBar/>
            <div className="main-content-pusher">
                <div className={'drawing-column'}>
                    <Header as={'h2'}>Draw a digit below</Header>
                    <Segment compact textAlign={'center'} className={'centred drawing'} size={'large'}>
                        <CanvasDraw ref={cd => (this.canvas = cd)}
                                    lazyRadius={0}
                                    brushColor={'black'}
                                    backgroundColor={'white'}
                                    hideGrid={true}
                                    className={'digit draw'}/>
                    </Segment>
                    <Segment basic textAlign={'center'} className={'centred'}>
                        <Grid>
                            <Grid.Row textAlign={'center'}>
                                <Button.Group widths={3} size={'large'}>
                                    <Button primary loading={this.state.loading}
                                            onClick={e => this.submitImage()}>Recognise</Button>
                                    <Button.Or/>
                                    <Button secondary onClick={e => this.clear()}>Clear</Button>
                                </Button.Group>
                            </Grid.Row>
                            <Grid.Row>
                                {this.state.digit ? 'We think that digit was: ' + this.state.digit : null}
                            </Grid.Row>
                        </Grid>
                    </Segment>
                </div>
            </div>
            <FooterLoader/>
        </div>
    }

    clear() {
        try {
            this.canvas.clear();
            this.setState({digit: undefined, loading: this.state.loading});
        } catch (e) {
            console.error('Error while clearing the canvas', e);
        }
    }

    async submitImage() {
        this.setState({digit: undefined, loading: true});
        let imgsrc = this.canvas.toDataURL('image/png');
        console.debug('Image extracted from the canvas: size=', imgsrc.length, 'content=', imgsrc.substr(0, 20));
        let blob = toBlob(imgsrc);
        let result = await this._recogniseImage(blob);
        console.log(`The image was recognised as ${result}`);
        this.setState({digit: result, loading: false})
    }

    async _recogniseImage(imageBlob) {
        try {
            console.log(`Uploading image`);
            console.debug('Image data:', imageBlob);
            let response = await request.post("/recognise")
                .attach('image', imageBlob)
                .use(api);
            await apiDelay();
            return response.text;
        } catch (e) {
            console.error("Exception while uploading a new photo", e);
            alert('Error connecting to the server: ' + e.message);
        }
    }

}
