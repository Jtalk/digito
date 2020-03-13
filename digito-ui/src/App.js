import React, {useState} from 'react';
import './utils/config';
import * as request from 'superagent';
import {Button, Grid, Header, Segment} from "semantic-ui-react";
import {Footer} from "./footer/footer";
import CanvasDraw from "./canvas-draw/canvas-draw";
import api from "./utils/superagent-api";
import {toBlob} from "./utils/image";
import {apiDelay} from "./utils/test-api-delay";
import './App.css';
import {MenuBar} from "./menu/menu";

export const App = function () {

    let [digit, setDigit] = useState(null);
    let [loading, setLoading] = useState(false);

    let canvas;

    async function submitImage() {
        setDigit(null);
        setLoading(true);
        try {
            let imgsrc = canvas.toDataURL('image/png');
            console.debug('Image extracted from the canvas: size=', imgsrc.length, 'content=', imgsrc.substr(0, 20));
            let blob = toBlob(imgsrc);
            let result = await recogniseImage(blob);
            console.log(`The image was recognised as ${result}`);
            setDigit(result);
        } finally {
            setLoading(false);
        }
    }

    let clear = () => {
        try {
            canvas.clear();
            setDigit(undefined);
        } catch (e) {
            console.error('Error while clearing the canvas', e);
        }
    };

    return <div className="main-content-pushable">
        <MenuBar/>
        <div className="main-content-pusher">
            <div className={'drawing-column'}>
                <Header as={'h2'}>Draw a digit below</Header>
                <Segment compact textAlign={'center'} className={'centred drawing'} size={'large'}>
                    <CanvasDraw ref={cd => (canvas = cd)}
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
                                <Button primary loading={loading}
                                        onClick={submitImage}>Recognise</Button>
                                <Button.Or/>
                                <Button secondary onClick={clear}>Clear</Button>
                            </Button.Group>
                        </Grid.Row>
                        <Grid.Row>
                            {digit && 'We think that digit was: ' + digit}
                        </Grid.Row>
                    </Grid>
                </Segment>
            </div>
        </div>
        <Footer/>
    </div>
};

async function recogniseImage(imageBlob) {
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
