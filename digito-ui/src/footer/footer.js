import React from "react";
import {Container, Segment} from "semantic-ui-react";

export const Footer = function () {
    let links = [
        {name: "Source", href: "https://bitbucket.org/__jtalk/digito"},
        {name: "LinkedIn", href: "https://linkedin.com/in/jtalkme"},
        {name: "BitBucket", href: "https://bitbucket.org/__jtalk/"}
    ];
    return <FooterStateless links={links}/>
};
export const FooterStateless = function ({links}) {
    return <Segment inverted basic className="footer" as="footer" textAlign="center">
        <Container textAlign="center">
            <Segment inverted basic textAlign="center">
                <FlatLinksList links={links} separator="|"/>
            </Segment>
            <Segment inverted basic textAlign={'center'}>
                Copyright 2019-2020 Roman Nazarenko
            </Segment>
        </Container>
    </Segment>
};

export const FlatLinksList = function ({links, separator}) {
    let result = links.flatMap(link => {
        return [
            <a href={link.href} key={link.name}>{link.name}</a>,
            <VerticalSeparator key={link.name + "-separator"} separator={separator}/>
        ];
    });
    if (result.length > 1) {
        result.pop(); // Remove trailing "|"
    }
    return result;
};

export const VerticalSeparator = function ({sparse = true, separator}) {

    return <span>{prepareSeparator(sparse, separator)}</span>
};

function prepareSeparator(sparse, separator) {
    if (!sparse) {
        return separator || '';
    }
    if (!separator) {
        return ' ';
    }
    if (!separator.startsWith(" ")) {
        separator = " " + separator;
    }
    if (!separator.endsWith(" ")) {
        separator += " ";
    }
    return separator;
}