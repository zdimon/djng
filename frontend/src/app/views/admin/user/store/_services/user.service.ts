import { environment } from './../../../../../../environments/environment';
// Angular
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// RxJS
import { Observable, BehaviorSubject } from 'rxjs';
// CRUD
import { QueryParamsModel, QueryResultsModel } from '../../../../../core/_base/crud';
import { HttpUtilsService } from './user.utils';
// Models
import { UserModel } from '../_models/user.model';

const API_LIST_URL = environment.apiUrl + '/account/user/list';
const API_UPDATE_URL = environment.apiUrl + '/account/user/list';
const API_CREATE_URL = environment.apiUrl + '/account/user/list';
const API_DELETE_URL = environment.apiUrl + '/account/user/list';
const API_DELETE_BULK_URL = environment.apiUrl + '/';
// Real REST API
@Injectable()
export class UserService {
    lastFilter$: BehaviorSubject<QueryParamsModel> = new BehaviorSubject(new QueryParamsModel({}, 'asc', '', 0, 10));

    constructor(private http: HttpClient,
                   private httpUtils: HttpUtilsService) { }

    // CREATE =>  POST: add a new product to the server
    createUser(item): Observable<UserModel> {
        return this.http.post<UserModel>(API_CREATE_URL, item);
    }

    // READ
    getAllUsers(): Observable<UserModel[]> {
        return this.http.get<UserModel[]>(API_LIST_URL);
    }

    getUserById(userId: number): Observable<UserModel> {
        return this.http.get<UserModel>(API_LIST_URL + `/${userId}`);
    }

    // Server should return filtered/sorted result
    findUsers(queryParams: QueryParamsModel): Observable<QueryResultsModel> {
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
    updateUser(product: UserModel): Observable<any> {
        // Note: Add headers if needed (tokens/bearer)
        const httpHeaders = this.httpUtils.getHTTPHeaders();
        return this.http.put(`${API_UPDATE_URL}${product.id}/`, product, { headers: httpHeaders });
    }

    

    // DELETE => delete the product from the server
    deleteUser(userId: number): Observable<UserModel> {
        const url = `${API_DELETE_URL}/${userId}`;
        return this.http.delete<UserModel>(url);
    }

    deleteUsers(ids: number[] = []): Observable<any> {
        const body = { itemsIdsForDelete: ids };
        return this.http.post<QueryResultsModel>(API_DELETE_BULK_URL, body);
    }
}
