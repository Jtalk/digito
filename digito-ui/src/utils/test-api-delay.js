import {sleep} from "sleepjs";
import config from "react-global-configuration";

/**
 * A "gremlin" for Superagent to ease up designing progress indicators
 */
export async function apiDelay() {
    let delay = config.get("apiDelay");
    if (delay) {
        await sleep(delay.milliseconds());
    }
}