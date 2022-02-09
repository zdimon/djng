import { environment } from './../../../../../../environments/environment';
// Angular
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
// RxJS
import { Observable, BehaviorSubject } from 'rxjs';
// CRUD
import { QueryParamsModel, QueryResultsModel } from '../../../../../core/_base/crud';
import { HttpUtilsService } from './payment.utils';
// Models
import { PaymentModel } from '../_models/payment.model';

const API_LIST_URL = environment.apiUrl + '/payment/admin/';
const API_UPDATE_URL = environment.apiUrl + '/payment/admin/';
const API_CREATE_URL = environment.apiUrl + '/payment/admin/';
const API_DELETE_URL = environment.apiUrl + '/payment/admin/';
const API_DELETE_BULK_URL = environment.apiUrl + '/';
// Real REST API
@Injectable()
export class PaymentService {
    lastFilter$: BehaviorSubject<QueryParamsModel> = new BehaviorSubject(new QueryParamsModel({}, 'asc', '', 0, 10));

    constructor(private http: HttpClient,
                   private httpUtils: HttpUtilsService) { }

    // CREATE =>  POST: add a new product to the server
    createPayment(item): Observable<PaymentModel> {
        return this.http.post<PaymentModel>(API_CREATE_URL, item);
    }

    // READ
    getAllPayments(): Observable<PaymentModel[]> {
        return this.http.get<PaymentModel[]>(API_LIST_URL);
    }

    getPaymentById(paymentId: number): Observable<PaymentModel> {
        return this.http.get<PaymentModel>(API_LIST_URL + `/${paymentId}`);
    }

    // Server should return filtered/sorted result
    findPayments(queryParams: QueryParamsModel): Observable<QueryResultsModel> {
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
    updatePayment(product: PaymentModel): Observable<any> {
        // Note: Add headers if needed (tokens/bearer)
        const httpHeaders = this.httpUtils.getHTTPHeaders();
        return this.http.put(`${API_UPDATE_URL}${product.id}/`, product, { headers: httpHeaders });
    }

    

    // DELETE => delete the product from the server
    deletePayment(paymentId: number): Observable<PaymentModel> {
        const url = `${API_DELETE_URL}/${paymentId}`;
        return this.http.delete<PaymentModel>(url);
    }

    deletePayments(ids: number[] = []): Observable<any> {
        const body = { itemsIdsForDelete: ids };
        return this.http.post<QueryResultsModel>(API_DELETE_BULK_URL, body);
    }
}
