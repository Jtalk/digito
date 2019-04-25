import React, {Component} from 'react';
import {Header, Icon} from "semantic-ui-react";

export default class ErrorPage extends Component {

    render() {
        return <div className={'screen-centred'}>
            <Header icon as={'h1'}>
                <Icon name={'bug'}/>
                System Error
                <Header.Subheader>
                    Something went wrong
                </Header.Subheader>
            </Header>
        </div>
    }
}