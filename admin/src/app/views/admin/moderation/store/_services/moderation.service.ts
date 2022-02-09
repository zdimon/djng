import { environment } from './../../../../../../environments/environment';
// Angular
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// RxJS
import { Observable, BehaviorSubject } from 'rxjs';
// CRUD
import { QueryParamsModel, QueryResultsModel } from '../../../../../core/_base/crud';
import { HttpUtilsService } from './moderation.utils';
// Models
import { ModerationModel } from '../_models/moderation.model';

const API_LIST_URL = environment.apiUrl + '/moderation/admin/';
const API_UPDATE_URL = environment.apiUrl + '/moderation/admin/';
const API_CREATE_URL = environment.apiUrl + '/moderation/admin/';
const API_DELETE_URL = environment.apiUrl + '/moderation/admin/';
const API_DELETE_BULK_URL = environment.apiUrl + '/moderation/admin/';
// Real REST API
@Injectable()
export class ModerationService {
    lastFilter$: BehaviorSubject<QueryParamsModel> = new BehaviorSubject(new QueryParamsModel({}, 'asc', '', 0, 10));

    constructor(private http: HttpClient,
                   private httpUtils: HttpUtilsService) { }

    // CREATE =>  POST: add a new product to the server
    createModeration(item): Observable<ModerationModel> {
        return this.http.post<ModerationModel>(API_CREATE_URL, item);
    }

    // READ
    getAllModerations(): Observable<ModerationModel[]> {
        return this.http.get<ModerationModel[]>(API_LIST_URL);
    }

    getModerationById(moderationId: number): Observable<ModerationModel> {
        return this.http.get<ModerationModel>(API_LIST_URL + `/${moderationId}`);
    }

    // Server should return filtered/sorted result
    findModerations(queryParams: QueryParamsModel): Observable<QueryResultsModel> {
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
    updateModeration(product: ModerationModel): Observable<any> {
        // Note: Add headers if needed (tokens/bearer)
        const httpHeaders = this.httpUtils.getHTTPHeaders();
        return this.http.put(`${API_UPDATE_URL}${product.id}/`, product, { headers: httpHeaders });
    }

    

    // DELETE => delete the product from the server
    deleteModeration(moderationId: number): Observable<ModerationModel> {
        const url = `${API_DELETE_URL}/${moderationId}`;
        return this.http.delete<ModerationModel>(url);
    }

    deleteModerations(ids: number[] = []): Observable<any> {
        const body = { itemsIdsForDelete: ids };
        return this.http.post<QueryResultsModel>(API_DELETE_BULK_URL, body);
    }
}
