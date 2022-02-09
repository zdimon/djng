import { environment } from './../../../../../../environments/environment';
// Angular
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// RxJS
import { Observable, BehaviorSubject } from 'rxjs';
// CRUD
import { QueryParamsModel, QueryResultsModel } from '../../../../../core/_base/crud';
import { HttpUtilsService } from './plan.utils';
// Models
import { PlanModel } from '../_models/plan.model';

const API_LIST_URL = environment.apiUrl + '/settings/plan/admin/list/';
const API_UPDATE_URL = environment.apiUrl + '/settings/plan/admin/update/';
const API_CREATE_URL = environment.apiUrl + '/settings/plan/admin/create/';
const API_DELETE_URL = environment.apiUrl + '/settings/plan/admin/delete/';
const API_DELETE_BULK_URL = environment.apiUrl + '/settings/plan/admin/delete/bulk/';
// Real REST API
@Injectable()
export class PlanService {
    lastFilter$: BehaviorSubject<QueryParamsModel> = new BehaviorSubject(new QueryParamsModel({}, 'asc', '', 0, 10));

    constructor(private http: HttpClient,
                   private httpUtils: HttpUtilsService) { }

    // CREATE =>  POST: add a new product to the server
    createPlan(item): Observable<PlanModel> {
        return this.http.post<PlanModel>(API_CREATE_URL, item);
    }

    // READ
    getAllPlans(): Observable<PlanModel[]> {
        return this.http.get<PlanModel[]>(API_LIST_URL);
    }

    getPlanById(planId: number): Observable<PlanModel> {
        return this.http.get<PlanModel>(API_LIST_URL + `/${planId}`);
    }

    // Server should return filtered/sorted result
    findPlans(queryParams: QueryParamsModel): Observable<QueryResultsModel> {
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
    updatePlan(product: PlanModel): Observable<any> {
        // Note: Add headers if needed (tokens/bearer)
        const httpHeaders = this.httpUtils.getHTTPHeaders();
        return this.http.put(`${API_UPDATE_URL}${product.id}/`, product, { headers: httpHeaders });
    }

    

    // DELETE => delete the product from the server
    deletePlan(planId: number): Observable<PlanModel> {
        const url = `${API_DELETE_URL}/${planId}`;
        return this.http.delete<PlanModel>(url);
    }

    deletePlans(ids: number[] = []): Observable<any> {
        const body = { itemsIdsForDelete: ids };
        return this.http.post<QueryResultsModel>(API_DELETE_BULK_URL, body);
    }
}
