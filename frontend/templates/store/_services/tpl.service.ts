import { environment } from './../../../../../../environments/environment';
// Angular
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// RxJS
import { Observable, BehaviorSubject } from 'rxjs';
// CRUD
import { QueryParamsModel, QueryResultsModel } from '../../../../../core/_base/crud';
import { HttpUtilsService } from './{{fileprefix}}.utils';
// Models
import { %upname%Model } from '../_models/{{fileprefix}}.model';

const API_LIST_URL = environment.apiUrl + '/{{ url_list }}';
const API_UPDATE_URL = environment.apiUrl + '/{{ url_update }}';
const API_CREATE_URL = environment.apiUrl + '/{{ url_create }}';
const API_DELETE_URL = environment.apiUrl + '/{{ url_delete }}';
const API_DELETE_BULK_URL = environment.apiUrl + '/{{ url_delete_bulk }}';
// Real REST API
@Injectable()
export class {{upname}}Service {
    lastFilter$: BehaviorSubject<QueryParamsModel> = new BehaviorSubject(new QueryParamsModel({}, 'asc', '', 0, 10));

    constructor(private http: HttpClient,
                   private httpUtils: HttpUtilsService) { }

    // CREATE =>  POST: add a new product to the server
    create{{upname}}(item): Observable<{{upname}}Model> {
        return this.http.post<{{upname}}Model>(API_CREATE_URL, item);
    }

    // READ
    getAll{{upname}}s(): Observable<{{upname}}Model[]> {
        return this.http.get<{{upname}}Model[]>(API_LIST_URL);
    }

    get{{upname}}ById({{camelName}}Id: number): Observable<{{upname}}Model> {
        return this.http.get<{{upname}}Model>(API_LIST_URL + `/${%camelName%Id}`);
    }

    // Server should return filtered/sorted result
    find{{upname}}s(queryParams: QueryParamsModel): Observable<QueryResultsModel> {
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
    update{{upname}}(product: {{upname}}Model): Observable<any> {
        // Note: Add headers if needed (tokens/bearer)
        const httpHeaders = this.httpUtils.getHTTPHeaders();
        return this.http.put(`${API_UPDATE_URL}${product.id}/`, product, { headers: httpHeaders });
    }

    

    // DELETE => delete the product from the server
    delete{{upname}}({{camelName}}Id: number): Observable<{{upname}}Model> {
        const url = `${API_DELETE_URL}/${%camelName%Id}`;
        return this.http.delete<{{upname}}Model>(url);
    }

    delete{{upname}}s(ids: number[] = []): Observable<any> {
        const body = { itemsIdsForDelete: ids };
        return this.http.post<QueryResultsModel>(API_DELETE_BULK_URL, body);
    }
}
