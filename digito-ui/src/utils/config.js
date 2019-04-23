import * as config from "react-global-configuration";

let API = process.env.API_LOCATION || "http://localhost:5000";

config.set({
    api: API
});