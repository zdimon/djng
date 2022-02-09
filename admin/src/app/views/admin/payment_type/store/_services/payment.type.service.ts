import { environment } from './../../../../../../environments/environment';
// Angular
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// RxJS
import { Observable, BehaviorSubject } from 'rxjs';
// CRUD
import { QueryParamsModel, QueryResultsModel } from '../../../../../core/_base/crud';
import { HttpUtilsService } from './payment.type.utils';
// Models
import { PaymentTypeModel } from '../_models/payment.type.model';

const API_LIST_URL = environment.apiUrl + '/payment/admin/type/';
const API_UPDATE_URL = environment.apiUrl + '/payment/admin/type/';
const API_CREATE_URL = environment.apiUrl + '/payment/admin/type/';
const API_DELETE_URL = environment.apiUrl + '/payment/admin/type/';
const API_DELETE_BULK_URL = environment.apiUrl + '/';
// Real REST API
@Injectable()
export class PaymentTypeService {
    lastFilter$: BehaviorSubject<QueryParamsModel> = new BehaviorSubject(new QueryParamsModel({}, 'asc', '', 0, 10));

    constructor(private http: HttpClient,
                   private httpUtils: HttpUtilsService) { }

    // CREATE =>  POST: add a new product to the server
    createPaymentType(item): Observable<PaymentTypeModel> {
        return this.http.post<PaymentTypeModel>(API_CREATE_URL, item);
    }

    // READ
    getAllPaymentTypes(): Observable<PaymentTypeModel[]> {
        return this.http.get<PaymentTypeModel[]>(API_LIST_URL);
    }

    getPaymentTypeById(paymentTypeId: number): Observable<PaymentTypeModel> {
        return this.http.get<PaymentTypeModel>(API_LIST_URL + `/${paymentTypeId}`);
    }

    // Server should return filtered/sorted result
    findPaymentTypes(queryParams: QueryParamsModel): Observable<QueryResultsModel> {
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
    updatePaymentType(product: PaymentTypeModel): Observable<any> {
        // Note: Add headers if needed (tokens/bearer)
        const httpHeaders = this.httpUtils.getHTTPHeaders();
        return this.http.put(`${API_UPDATE_URL}${product.id}/`, product, { headers: httpHeaders });
    }

    

    // DELETE => delete the product from the server
    deletePaymentType(paymentTypeId: number): Observable<PaymentTypeModel> {
        const url = `${API_DELETE_URL}/${paymentTypeId}`;
        return this.http.delete<PaymentTypeModel>(url);
    }

    deletePaymentTypes(ids: number[] = []): Observable<any> {
        const body = { itemsIdsForDelete: ids };
        return this.http.post<QueryResultsModel>(API_DELETE_BULK_URL, body);
    }
}
