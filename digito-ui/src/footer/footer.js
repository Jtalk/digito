import React from "react";
import {Container, Segment} from "semantic-ui-react";
import FlatLinksList from "./flat-links-list";

export default class Footer extends React.Component {

    render() {
        return <Segment inverted basic className="footer" as="footer" textAlign="center">
            <Container textAlign="center">
                <Segment inverted basic textAlign="center">
                    <FlatLinksList links={this.props.links} separator="|"/>
                </Segment>
                <Segment inverted basic textAlign={'center'}>
                    Copyright 2019 Roman Nazarenko
                </Segment>
            </Container>
        </Segment>
    }
}