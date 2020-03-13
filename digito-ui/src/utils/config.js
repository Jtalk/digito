import config from "react-global-configuration";


let API = process.env.REACT_APP_API_LOCATION || "http://localhost:5000";

config.set({
    api: API
});