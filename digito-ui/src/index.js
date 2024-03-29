import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import 'semantic-ui-css/semantic.css';
import {App} from './App';
import * as serviceWorker from './serviceWorker';
import {ErrorBoundary} from "react-error-boundary";
import {ErrorPage} from "./error/error-page";

ReactDOM.render(
    <ErrorBoundary FallbackComponent={ErrorPage} onError={e => console.error('Error while rendering', e)}>
        <App/>
    </ErrorBoundary>,
    document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
