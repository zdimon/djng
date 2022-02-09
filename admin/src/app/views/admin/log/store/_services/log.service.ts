import { environment } from './../../../../../../environments/environment';
// Angular
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// RxJS
import { Observable, BehaviorSubject } from 'rxjs';
// CRUD
import { QueryParamsModel, QueryResultsModel } from '../../../../../core/_base/crud';
import { HttpUtilsService } from './log.utils';
// Models
import { LogModel } from '../_models/log.model';

const API_LIST_URL = environment.apiUrl + '/logs/list/';
const API_UPDATE_URL = environment.apiUrl + '/logs/update/';
const API_CREATE_URL = environment.apiUrl + '/logs/create/';
const API_DELETE_URL = environment.apiUrl + '/logs/delete/';
const API_DELETE_BULK_URL = environment.apiUrl + '/logs/delete/bulk';
// Real REST API
@Injectable()
export class LogService {
    lastFilter$: BehaviorSubject<QueryParamsModel> = new BehaviorSubject(new QueryParamsModel({}, 'asc', '', 0, 10));

    constructor(private http: HttpClient,
                   private httpUtils: HttpUtilsService) { }

    // CREATE =>  POST: add a new product to the server
    createLog(item): Observable<LogModel> {
        return this.http.post<LogModel>(API_CREATE_URL, item);
    }

    // READ
    getAllLogs(): Observable<LogModel[]> {
        return this.http.get<LogModel[]>(API_LIST_URL);
    }

    getLogById(logId: number): Observable<LogModel> {
        return this.http.get<LogModel>(API_LIST_URL + `/${logId}`);
    }

    // Server should return filtered/sorted result
    findLogs(queryParams: QueryParamsModel): Observable<QueryResultsModel> {
            // Note: Add headers if needed (tokens/bearer)
            const httpHeaders = this.httpUtils.getHTTPHeaders();
            const httpParams = this.httpUtils.getFindHTTPParams(queryParams);

            const url = API_LIST_URL;
            return this.http.get<QueryResultsModel>(url, {
                headers: httpHeaders,
                params:  httpParams
            });
    }

    // UPDATE => PUT: update the product on the server
    updateLog(product: LogModel): Observable<any> {
        // Note: Add headers if needed (tokens/bearer)
        const httpHeaders = this.httpUtils.getHTTPHeaders();
        return this.http.put(`${API_UPDATE_URL}${product.id}/`, product, { headers: httpHeaders });
    }

    

    // DELETE => delete the product from the server
    deleteLog(logId: number): Observable<LogModel> {
        const url = `${API_DELETE_URL}/${logId}`;
        return this.http.delete<LogModel>(url);
    }

    deleteLogs(ids: number[] = []): Observable<any> {
        const body = { itemsIdsForDelete: ids };
        return this.http.post<QueryResultsModel>(API_DELETE_BULK_URL, body);
    }
}
