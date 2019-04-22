import React from "react";
import Footer from "./footer";

export default class FooterLoader extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            links: [
                {name: "Source", href: "https://bitbucket.org/__jtalk/digito"},
                {name: "LinkedIn", href: "https://linkedin.com/in/jtalkme"},
                {name: "BitBucket", href: "https://bitbucket.org/__jtalk/"},
                {name: "StackOverflow", href: "https://stackoverflow.com/users/752977/roman-nazarenko"},
            ],
            logos: [
                {
                    href: "https://java.com",
                    src: "/images/disabled.png",
                    name: "Java Logo",
                    height: 55
                },
                {
                    href: "https://www.gnu.org/licenses/agpl-3.0.html",
                    src: "/images/logo_agplv3.svg",
                    name: "GNU AGPL Logo",
                    height: 40
                }
            ]
        }
    }

    render() {
        return <Footer links={this.state.links} logos={this.state.logos} />
    }
}