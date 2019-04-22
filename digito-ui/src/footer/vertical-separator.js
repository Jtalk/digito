import React from "react";
import {isUndefined} from "typechecker";

export default class VerticalSeparator extends React.Component {

    render() {
        let sparse = isUndefined(this.props.sparse) ? true : this.props.sparse;
        return <span>{this._prepareSeparator(sparse)}</span>
    }

    /**
     * Links will glue to one another or their splitter if no whitespaces were inserted.
     */
    _prepareSeparator(sparse) {
        if (!sparse) {
            return this.props.separator || '';
        }
        if (!this.props.separator) {
            return ' ';
        }
        var separator = this.props.separator;
        if (!separator.startsWith(" ")) {
            separator = " " + separator;
        }
        if (!separator.endsWith(" ")) {
            separator += " ";
        }
        return separator;
    }
}