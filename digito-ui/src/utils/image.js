import b64toBlob from 'b64-to-blob';

export function toBlob(dataUrl) {
    let match = dataUrl.match(/data:([^;]+);base64,(.*)/);
    if (!match) {
        throw Error(`Invalid data URL format: ${dataUrl.substring(0, 20)}`);
    }
    // eslint-disable-next-line
    let [_, contentType, data] = match;
    return b64toBlob(data, contentType);
}