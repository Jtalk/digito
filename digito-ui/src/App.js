import React, {Component} from 'react';
import './utils/config';
import * as request from 'superagent';
import {Button, Grid, Header, Segment} from "semantic-ui-react";
import FooterLoader from "./footer/footer-loader";
import CanvasDraw from "./canvas-draw/canvas-draw";
import api from "./utils/superagent-api";
import {positions, Provider as AlertProvider, withAlert} from 'react-alert';
import AlertTemplate from 'react-alert-template-basic';
import {toBlob} from "./utils/image";
import {apiDelay} from "./utils/test-api-delay";
import './App.css';
import MenuBar from "./menu/menu";
import {withErrorBoundary} from "react-error-boundary";
import ErrorPage from "./error/error-page";

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return <AlertProvider template={AlertTemplate} position={positions.TOP_CENTER} timeout={10000}>
            <div className="main-content-pushable">
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
        </AlertProvider>
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
        let imgsrc = this.canvas.toDataURL('image/bmp');
        let blob = toBlob(imgsrc);
        let result = await this._recogniseImage(blob);
        console.log(`The image was recognised as ${result}`);
        this.setState({digit: result, loading: false})
    }

    async _recogniseImage(base64Image) {
        try {
            console.log(`Uploading image`);
            let response = await request.post("/recognise")
                .attach('image', base64Image)
                .use(api);
            await apiDelay();
            return response.text;
        } catch (e) {
            console.error("Exception while uploading a new photo", e);
            alert('Cannot connect to the server');
        }
    }

}

export default withErrorBoundary(withAlert()(App), ErrorPage)