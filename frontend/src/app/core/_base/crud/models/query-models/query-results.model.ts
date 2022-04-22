export class QueryResultsModel {
    // fields
    results: any;
    results_list: any[];
    items: any[];
    totalCount: number;
    errorMessage: string;

    constructor(_items: any[] = [], _totalCount: number = 0, _errorMessage: string = '', _results = {}, _results_list= []) {
        this.items = _items;
        this.totalCount = _totalCount;
        this.results = _results;
        this.results_list = _results_list;

    }
}

export class DjangoQueryResultsModel {
    // fields
    results_list: any[];
    totalCount: number;
    message: string;
    status: number;

    constructor(_results_list: any[] = [], _totalCount: number = 0, _message: string = '') {
        this.results_list = _results_list;
        this.totalCount = _totalCount;
        this.message = _message;

    }
}
