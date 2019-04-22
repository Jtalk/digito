import React from "react";
import {Placeholder} from "semantic-ui-react";

export class ImagePlaceholderOr extends React.Component {

    render() {
        if (this.props.loading) {
            return <Placeholder>
                <Placeholder.Image square={this.props.square} rectangular={this.props.rectangular}/>
            </Placeholder>
        } else {
            return this.props.children;
        }
    }
}


export class ContentPlaceholderOr extends React.Component {

    render() {
        if (this.props.loading) {
            return <Placeholder fluid>
                {this.props.header ? <Placeholder.Header>
                    <Placeholder.Line length="medium"/>
                </Placeholder.Header> : null}
                <Placeholder.Paragraph>
                    {Array(this.props.lines).fill().map((_, i) => <Placeholder.Line key={i}/>)}
                </Placeholder.Paragraph>
            </Placeholder>
        } else {
            return this.props.children;
        }
    }
}


export class LinePlaceholderOr extends React.Component {

    render() {
        if (this.props.loading) {
            return <Placeholder>
                <Placeholder.Paragraph>
                    <Placeholder.Line length={this.props.length}/>
                </Placeholder.Paragraph>
            </Placeholder>
        } else {
            return this.props.children;
        }
    }
}