/* ----- {{copyright}} --- */
// Angular
import { Injectable } from '@angular/core';
import { HttpParams, HttpHeaders } from '@angular/common/http';
// CRUD
import { QueryResultsModel } from '@core/_base/crud/models/query-models/query-results.model';
import { QueryParamsModel } from '@core/_base/crud/models/query-models/query-params.model';
import { HttpExtenstionsModel } from '@core/_base/crud/models/http-extentsions-model';

@Injectable()
export class HttpUtilsService {
    /**
     * Prepare query http params
     * @param queryParams: QueryParamsModel
     */
    getFindHTTPParams(queryParams): HttpParams {
        const offset = queryParams.pageSize*queryParams.pageNumber;
        let params = new HttpParams()


            .set('offset', offset.toString())
            .set('limit', queryParams.pageSize.toString());

{% for i in filter_fields %}
            if(queryParams.filter.{{i.name}} !== undefined && queryParams.filter.{{i.name}}.length > 0) {
                params = params.set('{{i.name}}', queryParams.filter.{{i.name}});
            }
{% endfor %}
        return params;
    }

    /**
     * get standard content-type
     */
    getHTTPHeaders(): HttpHeaders {
        const result = new HttpHeaders();
        result.set('Content-Type', 'application/json');
        return result;
    }

    baseFilter(_entities: any[], _queryParams: QueryParamsModel, _filtrationFields: string[] = []): QueryResultsModel {
        const httpExtention = new HttpExtenstionsModel();
        return httpExtention.baseFilter(_entities, _queryParams, _filtrationFields);
    }

    sortArray(_incomingArray: any[], _sortField: string = '', _sortOrder: string = 'asc'): any[] {
        const httpExtention = new HttpExtenstionsModel();
        return httpExtention.sortArray(_incomingArray, _sortField, _sortOrder);
    }

    searchInArray(_incomingArray: any[], _queryObj: any, _filtrationFields: string[] = []): any[] {
        const httpExtention = new HttpExtenstionsModel();
        return httpExtention.searchInArray(_incomingArray, _queryObj, _filtrationFields);
    }
}
