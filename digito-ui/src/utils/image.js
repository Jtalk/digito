

import * as b64toBlob from 'b64-to-blob';

export function toBlob(dataUrl) {
    // eslint-disable-next-line
    let [_, contentType, data] = dataUrl.match('data:([^;]+);base64,(.*)');
    return b64toBlob(data, contentType);
}