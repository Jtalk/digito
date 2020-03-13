import React from 'react';
import ReactDOM from 'react-dom';
import {ErrorPage} from "./error-page";

it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<ErrorPage/>, div);
    ReactDOM.unmountComponentAtNode(div);
});
