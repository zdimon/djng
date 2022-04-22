// Angular
import { Injectable } from '@angular/core';
// NGRX
import { Actions, Effect, ofType } from '@ngrx/effects';
import { Action, Store } from '@ngrx/store';
import { forkJoin } from 'rxjs';
import { defer, Observable, of } from 'rxjs';
// RxJS
import { map, mergeMap, tap } from 'rxjs/operators';
// CRUD
import { DjangoQueryResultsModel, QueryParamsModel, QueryResultsModel } from '../../../_base/crud';
// State
import { AppState } from '../../../reducers';
// Actions
import {
    ManyVideosDeleted,
    OneVideoDeleted,
    VideoActionTypes,
    VideoCreated,
    VideoOnServerCreated,
    VideosPageLoaded,
    VideosPageRequested,
    VideosPageToggleLoading,
    VideosStatusUpdated,
    VideoUpdated,
} from '../_actions/video.actions';
// Services
import { VideoService } from '../_services';

@Injectable()
export class VideoEffects {
    showPageLoadingDistpatcher = new VideosPageToggleLoading({ isLoading: true });
    showLoadingDistpatcher = new VideosPageToggleLoading({ isLoading: true });
    hideActionLoadingDistpatcher = new VideosPageToggleLoading({ isLoading: false });

    @Effect()
    loadVideoPage$ = this.actions$
        .pipe(
            ofType<VideosPageRequested>(VideoActionTypes.VideosPageRequested),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showPageLoadingDistpatcher);
                const requestToServer = this.productsService.findProducts(payload.page);
                const lastQuery = of(payload.page);
                return forkJoin(requestToServer, lastQuery);
            }),
            map(response => {
                const result: QueryResultsModel = response[0];
                const lastQuery: QueryParamsModel = response[1];
                console.log(result);
                return new VideosPageLoaded({
                    results: result.results_list,
                    totalCount: result.totalCount,
                    page: lastQuery,
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

    // @Effect()
    // deleteProducts$ = this.actions$
    //     .pipe(
    //         ofType<ManyProductsDeleted>(ProductActionTypes.ManyProductsDeleted),
    //         mergeMap(( { payload } ) => {
    //             this.store.dispatch(this.showLoadingDistpatcher);
    //             return this.productsService.deleteProducts(payload.ids);
    //             }
    //         ),
    //         map(() => {
    //             return this.hideActionLoadingDistpatcher;
    //         }),
    //     );

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

    // @Effect()
    // updateProduct$ = this.actions$
    //     .pipe(
    //         ofType<ProductUpdated>(ProductActionTypes.ProductUpdated),
    //         mergeMap(( { payload } ) => {
    //             this.store.dispatch(this.showLoadingDistpatcher);
    //             return this.productsService.updateProduct(payload.product);
    //         }),
    //         map(() => {
    //             return this.hideActionLoadingDistpatcher;
    //         }),
    //     );

    // @Effect()
    // createProduct$ = this.actions$
    //     .pipe(
    //         ofType<ProductOnServerCreated>(ProductActionTypes.ProductOnServerCreated),
    //         mergeMap(( { payload } ) => {
    //             this.store.dispatch(this.showLoadingDistpatcher);
    //             return this.productsService.createProduct(payload.product).pipe(
    //                 tap(res => {
    //                     this.store.dispatch(new ProductCreated({ product: res }));
    //                 })
    //             );
    //         }),
    //         map(() => {
    //             return this.hideActionLoadingDistpatcher;
    //         }),
    //     );

    // // @Effect()
    // // init$: Observable<Action> = defer(() => {
    // //     const queryParams = new QueryParamsModel({});
    // //     return of(new ProductsPageRequested({ page: queryParams }));
    // // });

    constructor(private actions$: Actions, private productsService: VideoService, private store: Store<AppState>) { }
}
