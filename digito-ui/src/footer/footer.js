import React from "react";
import {Container, Segment} from "semantic-ui-react";
import FlatLinksList from "./flat-links-list";
import FlatLogoList from "./flat-logo-list";

export default class Footer extends React.Component {

    render() {
        return <Segment inverted basic className="footer" as="footer" textAlign="center">
            <Container textAlign="center">
                <Segment inverted basic textAlign="center">
                    <FlatLinksList links={this.props.links} separator="|"/>
                </Segment>
                <FlatLogoList logos={this.props.logos}/>
            </Container>
        </Segment>
    }
}