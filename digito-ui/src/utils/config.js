import config from "react-global-configuration";

const api = process.env.REACT_APP_API_LOCATION || "http://localhost:4000";

config.set({
    api
});
