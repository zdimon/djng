/* ----- {{copyright}} --- */
import { environment } from './../../../../../../environments/environment';
// Angular
import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
// RxJS
import { Observable, forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';
// CRUD
import { HttpUtilsService, QueryParamsModel, QueryResultsModel } from '../../../../../core/_base/crud';
// Models and Consts
import { %class%Model } from '../_models/{{selector}}.tab.model';
// import { SPECIFICATIONS_DICTIONARY } from '../_consts/specification.dictionary';

const API_LIST_URL = environment.apiUrl + '/{{url_list}}';
const API_CREATE_URL = environment.apiUrl + '/{{url_create}}';
const API_UPDATE_URL = environment.apiUrl + '/{{url_update}}';
const API_DELETE_URL = environment.apiUrl + '/{{url_delete}}';
// Real REST API
@Injectable()
export class {{class}}Service {
	constructor(private http: HttpClient, private httpUtils: HttpUtilsService) { }

	// CREATE =>  POST: add a new product specification to the server
	create{{class}}({{class}}): Observable<{{class}}Model> {
		return this.http.post<{{class}}Model>(API_CREATE_URL, {{class}});
	}

	// READ
	// Server should return filtered specs by productId
	getAll{{class}}By{{class}}Id({{class}}Id: number): Observable<{{class}}Model[]> {
		const url = API_LIST_URL + '/' + {{class}}Id;
		return this.http.get<{{class}}Model[]>(url);
	}

	get{{class}}ById({{class}}Id: number): Observable<{{class}}Model> {
		return this.http.get<{{class}}Model>(API_LIST_URL + `/${%class%Id}`);
	}

	// Server should return sorted/filtered specs and merge with items from state
	find{{class}}(queryParams: QueryParamsModel, {{class}}Id: number): Observable<QueryResultsModel> {
		const url = API_LIST_URL + '/' + {{class}}Id;
		const body = {
			state: queryParams
		};
		// return this.http.post<QueryResultsModel>(url, body);
		return this.http.get<QueryResultsModel>(url);

	}

	// UPDATE => PUT: update the product specification on the server
	update{{class}}({{class}}: {{class}}Model): Observable<any> {
		return this.http.put(API_UPDATE_URL, {{class}});
	}

	// DELETE => delete the product specification from the server
	delete{{class}}({{class}}Id: number): Observable<any> {
		const url = `${API_DELETE_URL}/${%class%Id}`;
		return this.http.delete<{{class}}Model>(url);
	}

	deleteMany{{class}}(ids: number[] = []): Observable<any> {
		const body = { {{class}}IdsForDelete: ids };
        return this.http.post<QueryResultsModel>(API_DELETE_URL, body);
	}

	getSpecs(): string[] {

        return [];

		// return SPECIFICATIONS_DICTIONARY;
	}
}
