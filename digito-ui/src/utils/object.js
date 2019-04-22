
export function update(state, updater) {
    let copy = Object.assign({}, state);
    updater(copy);
    return copy;
}