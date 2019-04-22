
export function ifMount(target, closure) {
    if (!target._asyncIsUnmount) {
        closure();
    }
}