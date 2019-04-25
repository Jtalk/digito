import React from "react";
import Footer from "./footer";

export default class FooterLoader extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            links: [
                {name: "Source", href: "https://bitbucket.org/__jtalk/digito"},
                {name: "LinkedIn", href: "https://linkedin.com/in/jtalkme"},
                {name: "BitBucket", href: "https://bitbucket.org/__jtalk/"}
            ]
        }
    }

    render() {
        return <Footer links={this.state.links} logos={this.state.logos} />
    }
}