import { HttpClient } from '@angular/common/http';
// Angular
import { Injectable } from '@angular/core';
// RxJS
import { BehaviorSubject, Observable } from 'rxjs';
// CRUD
import { HttpUtilsService, QueryParamsModel, QueryResultsModel } from '../../../_base/crud';
// Models
import { VideoModel } from '../_models/video.model';
import { environment } from './../../../../../environments/environment';

const API_PRODUCTS_URL = environment.apiUrl + '/usermedia/admin/video';
// Real REST API
@Injectable()
export class VideoService {
    lastFilter$: BehaviorSubject<QueryParamsModel> = new BehaviorSubject(new QueryParamsModel({}, 'asc', '', 0, 10));

    constructor(private http: HttpClient,
                private httpUtils: HttpUtilsService) { }

    // CREATE =>  POST: add a new product to the server
    createProduct(product): Observable<VideoModel> {
        const httpHeaders = this.httpUtils.getHTTPHeaders();
        return this.http.post<VideoModel>(API_PRODUCTS_URL, product, { headers: httpHeaders });
    }

    // READ
    getAllProducts(): Observable<VideoModel[]> {
        return this.http.get<VideoModel[]>(API_PRODUCTS_URL);
    }

    getProductById(productId: number): Observable<VideoModel> {
        return this.http.get<VideoModel>(API_PRODUCTS_URL + `/${productId}`);
    }

    // Server should return filtered/sorted result
    findProducts(queryParams: QueryParamsModel): Observable<QueryResultsModel> {
            // Note: Add headers if needed (tokens/bearer)
            const httpHeaders = this.httpUtils.getHTTPHeaders();
            const httpParams = this.httpUtils.getFindHTTPParams(queryParams);

            const url = API_PRODUCTS_URL;
            return this.http.get<QueryResultsModel>(url, {
                headers: httpHeaders,
                // params:  httpParams
            });
    }

    // UPDATE => PUT: update the product on the server
    updateProduct(product: VideoModel): Observable<any> {
        // Note: Add headers if needed (tokens/bearer)
        const httpHeaders = this.httpUtils.getHTTPHeaders();
        return this.http.put(API_PRODUCTS_URL, product, { headers: httpHeaders });
    }

    // DELETE => delete the product from the server
    deleteProduct(productId: number): Observable<VideoModel> {
        const url = `${API_PRODUCTS_URL}/${productId}`;
        return this.http.delete<VideoModel>(url);
    }

    deleteProducts(ids: number[] = []): Observable<any> {
        const url = API_PRODUCTS_URL + '/delete';
        const httpHeaders = this.httpUtils.getHTTPHeaders();
        const body = { prdocutIdsForDelete: ids };
        return this.http.put<QueryResultsModel>(url, body, { headers: httpHeaders} );
    }
}
