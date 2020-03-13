import React from "react";
import {Menu} from "semantic-ui-react";

export const MenuBar = function () {
    return <Menu inverted widths={3} size={'large'}>
        <Menu.Item><a href={'https://www.wolframcloud.com/objects/mewolfram0/Published/Classify%20MNIST'}>About</a></Menu.Item>
        <Menu.Item><a href={'https://bitbucket.org/__jtalk/digito'}>Source</a></Menu.Item>
        <Menu.Item><a href={'https://jtalk.me'}>Author</a></Menu.Item>
    </Menu>
};
