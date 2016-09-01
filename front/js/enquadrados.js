function count_workers(data) {
    var total = 0;
    for (worker_type in data) {
        total += data[worker_type];
    }
    return total;
}
