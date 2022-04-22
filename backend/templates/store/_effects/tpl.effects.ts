/* ----- {{copyright}} --- */
import { forkJoin } from 'rxjs';
// Angular
import { Injectable } from '@angular/core';
// RxJS
import { mergeMap, map, tap } from 'rxjs/operators';
// NGRX
import { Effect, Actions, ofType } from '@ngrx/effects';
import { Store, Action } from '@ngrx/store';
// CRUD
import { QueryResultsModel, QueryParamsModel, DjangoQueryResultsModel } from '@core/_base/crud';
// Services
import { %upname%Service } from '../_services';
// State
import { AppState } from '@core/reducers';
// Actions
import {
    {{upname}}ActionTypes,
    {{upname}}sPageRequested,
    {{upname}}sPageLoaded,
    Many{{upname}}sDeleted,
    One{{upname}}Deleted,
    {{upname}}sPageToggleLoading,
    {{upname}}sStatusUpdated,
    {{upname}}Updated,
    {{upname}}Created,
    {{upname}}OnServerCreated
} from '../_actions/{{fileprefix}}.actions';
import { defer, Observable, of } from 'rxjs';

@Injectable()
export class {{upname}}Effects {
    showPageLoadingDistpatcher = new {{upname}}sPageToggleLoading({ isLoading: true });
    showLoadingDistpatcher = new {{upname}}sPageToggleLoading({ isLoading: true });
    hideActionLoadingDistpatcher = new {{upname}}sPageToggleLoading({ isLoading: false });

    @Effect()
    load{{upname}}Page$ = this.actions$
        .pipe(
            ofType<{{upname}}sPageRequested>({{upname}}ActionTypes.{{upname}}sPageRequested),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showPageLoadingDistpatcher);
                const requestToServer = this.{{camelName}}sService.find{{upname}}s(payload.page);
                const lastQuery = of(payload.page);
                return forkJoin(requestToServer, lastQuery);
            }),
            map(response => {
                const result: QueryResultsModel = response[0];
                const lastQuery: QueryParamsModel = response[1];
                // console.log(result);
                return new {{upname}}sPageLoaded({
                    results: result.results_list,
                    totalCount: result.totalCount,
                    page: lastQuery
                });
            }),
        );

    // @Effect()
    // deleteProduct$ = this.actions$
    //     .pipe(
    //         ofType<OneProductDeleted>(ProductActionTypes.OneProductDeleted),
    //         mergeMap(( { payload } ) => {
    //                 this.store.dispatch(this.showLoadingDistpatcher);
    //                 return this.productsService.deleteProduct(payload.id);
    //             }
    //         ),
    //         map(() => {
    //             return this.hideActionLoadingDistpatcher;
    //         }),
    //     );

    @Effect()
    delete{{upname}}s$ = this.actions$
        .pipe(
            ofType<Many{{upname}}sDeleted>({{upname}}ActionTypes.Many{{upname}}sDeleted),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.{{camelName}}sService.delete{{upname}}s(payload.ids);
                }
            ),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    // @Effect()
    // updateProductsStatus$ = this.actions$
    //     .pipe(
    //         ofType<ProductsStatusUpdated>(ProductActionTypes.ProductsStatusUpdated),
    //         mergeMap(( { payload } ) => {
    //             this.store.dispatch(this.showLoadingDistpatcher);
    //             return this.productsService.updateStatusForProduct(payload.products, payload.status);
    //         }),
    //         map(() => {
    //             return this.hideActionLoadingDistpatcher;
    //         }),
    //     );

    @Effect()
    update{{upname}}$ = this.actions$
        .pipe(
            ofType<{{upname}}Updated>({{upname}}ActionTypes.{{upname}}Updated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.{{camelName}}sService.update{{upname}}(payload.results);
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    create{{upname}}$ = this.actions$
        .pipe(
            ofType<{{upname}}OnServerCreated>({{upname}}ActionTypes.{{upname}}OnServerCreated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.{{camelName}}sService.create{{upname}}(payload.{{camelName}}).pipe(
                    tap(res => {
                        this.store.dispatch(new {{upname}}Created({ {{camelName}}: res }));
                    })
                );
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    // // @Effect()
    // // init$: Observable<Action> = defer(() => {
    // //     const queryParams = new QueryParamsModel({});
    // //     return of(new ProductsPageRequested({ page: queryParams }));
    // // });

    constructor(private actions$: Actions, private {{camelName}}sService: {{upname}}Service, private store: Store<AppState>) { }
}
