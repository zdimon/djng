/* -----  --- */
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
import { ModerationService } from '../_services';
// State
import { AppState } from '@core/reducers';
// Actions
import {
    ModerationActionTypes,
    ModerationsPageRequested,
    ModerationsPageLoaded,
    ManyModerationsDeleted,
    OneModerationDeleted,
    ModerationsPageToggleLoading,
    ModerationsStatusUpdated,
    ModerationUpdated,
    ModerationCreated,
    ModerationOnServerCreated
} from '../_actions/moderation.actions';
import { defer, Observable, of } from 'rxjs';

@Injectable()
export class ModerationEffects {
    showPageLoadingDistpatcher = new ModerationsPageToggleLoading({ isLoading: true });
    showLoadingDistpatcher = new ModerationsPageToggleLoading({ isLoading: true });
    hideActionLoadingDistpatcher = new ModerationsPageToggleLoading({ isLoading: false });

    @Effect()
    loadModerationPage$ = this.actions$
        .pipe(
            ofType<ModerationsPageRequested>(ModerationActionTypes.ModerationsPageRequested),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showPageLoadingDistpatcher);
                const requestToServer = this.moderationsService.findModerations(payload.page);
                const lastQuery = of(payload.page);
                return forkJoin(requestToServer, lastQuery);
            }),
            map(response => {
                const result: QueryResultsModel = response[0];
                const lastQuery: QueryParamsModel = response[1];
                // console.log(result);
                return new ModerationsPageLoaded({
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
    deleteModerations$ = this.actions$
        .pipe(
            ofType<ManyModerationsDeleted>(ModerationActionTypes.ManyModerationsDeleted),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.moderationsService.deleteModerations(payload.ids);
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
    updateModeration$ = this.actions$
        .pipe(
            ofType<ModerationUpdated>(ModerationActionTypes.ModerationUpdated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.moderationsService.updateModeration(payload.results);
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    createModeration$ = this.actions$
        .pipe(
            ofType<ModerationOnServerCreated>(ModerationActionTypes.ModerationOnServerCreated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.moderationsService.createModeration(payload.moderation).pipe(
                    tap(res => {
                        this.store.dispatch(new ModerationCreated({ moderation: res }));
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

    constructor(private actions$: Actions, private moderationsService: ModerationService, private store: Store<AppState>) { }
}
