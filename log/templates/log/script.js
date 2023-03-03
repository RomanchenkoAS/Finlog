function recursive(arr) {
    item = arr.pop();
    if (typeof item === 'undefined') {
        console.log('That was the last one :3')
        return 0 
    } else {
        console.log(item);
        recursive(arr);
    }
}


array = [0,1,2];

console.log(array);

recursive(array);
