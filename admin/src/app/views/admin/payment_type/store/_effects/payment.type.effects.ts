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
import { PaymentTypeService } from '../_services';
// State
import { AppState } from '@core/reducers';
// Actions
import {
    PaymentTypeActionTypes,
    PaymentTypesPageRequested,
    PaymentTypesPageLoaded,
    ManyPaymentTypesDeleted,
    OnePaymentTypeDeleted,
    PaymentTypesPageToggleLoading,
    PaymentTypesStatusUpdated,
    PaymentTypeUpdated,
    PaymentTypeCreated,
    PaymentTypeOnServerCreated
} from '../_actions/payment.type.actions';
import { defer, Observable, of } from 'rxjs';

@Injectable()
export class PaymentTypeEffects {
    showPageLoadingDistpatcher = new PaymentTypesPageToggleLoading({ isLoading: true });
    showLoadingDistpatcher = new PaymentTypesPageToggleLoading({ isLoading: true });
    hideActionLoadingDistpatcher = new PaymentTypesPageToggleLoading({ isLoading: false });

    @Effect()
    loadPaymentTypePage$ = this.actions$
        .pipe(
            ofType<PaymentTypesPageRequested>(PaymentTypeActionTypes.PaymentTypesPageRequested),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showPageLoadingDistpatcher);
                const requestToServer = this.paymentTypesService.findPaymentTypes(payload.page);
                const lastQuery = of(payload.page);
                return forkJoin(requestToServer, lastQuery);
            }),
            map(response => {
                const result: QueryResultsModel = response[0];
                const lastQuery: QueryParamsModel = response[1];
                // console.log(result);
                return new PaymentTypesPageLoaded({
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
    deletePaymentTypes$ = this.actions$
        .pipe(
            ofType<ManyPaymentTypesDeleted>(PaymentTypeActionTypes.ManyPaymentTypesDeleted),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.paymentTypesService.deletePaymentTypes(payload.ids);
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
    updatePaymentType$ = this.actions$
        .pipe(
            ofType<PaymentTypeUpdated>(PaymentTypeActionTypes.PaymentTypeUpdated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.paymentTypesService.updatePaymentType(payload.results);
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    createPaymentType$ = this.actions$
        .pipe(
            ofType<PaymentTypeOnServerCreated>(PaymentTypeActionTypes.PaymentTypeOnServerCreated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.paymentTypesService.createPaymentType(payload.paymentType).pipe(
                    tap(res => {
                        this.store.dispatch(new PaymentTypeCreated({ paymentType: res }));
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

    constructor(private actions$: Actions, private paymentTypesService: PaymentTypeService, private store: Store<AppState>) { }
}
