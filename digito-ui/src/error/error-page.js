import React from 'react';
import {Header, Icon} from "semantic-ui-react";

export const ErrorPage = function () {
    return <div className={'screen-centred'}>
        <Header icon as={'h1'}>
            <Icon name={'bug'}/>
            System Error
            <Header.Subheader>
                Something went wrong
            </Header.Subheader>
        </Header>
    </div>
};