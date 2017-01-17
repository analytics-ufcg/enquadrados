function count_workers(data) {
    var total = 0;
    for (worker_type in data) {
        if (data[worker_type]['ativo']) {
            total += data[worker_type]['quantidade'];
        }
    }
    return total;
}

function count_workers_com_inativos(data) {
    var total = 0;
    for (worker_type in data) {
        total += data[worker_type]['quantidade'];
    }
    return total;
}
