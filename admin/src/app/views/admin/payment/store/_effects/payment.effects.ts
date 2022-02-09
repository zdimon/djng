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
import { PaymentService } from '../_services';
// State
import { AppState } from '@core/reducers';
// Actions
import {
    PaymentActionTypes,
    PaymentsPageRequested,
    PaymentsPageLoaded,
    ManyPaymentsDeleted,
    OnePaymentDeleted,
    PaymentsPageToggleLoading,
    PaymentsStatusUpdated,
    PaymentUpdated,
    PaymentCreated,
    PaymentOnServerCreated
} from '../_actions/payment.actions';
import { defer, Observable, of } from 'rxjs';

@Injectable()
export class PaymentEffects {
    showPageLoadingDistpatcher = new PaymentsPageToggleLoading({ isLoading: true });
    showLoadingDistpatcher = new PaymentsPageToggleLoading({ isLoading: true });
    hideActionLoadingDistpatcher = new PaymentsPageToggleLoading({ isLoading: false });

    @Effect()
    loadPaymentPage$ = this.actions$
        .pipe(
            ofType<PaymentsPageRequested>(PaymentActionTypes.PaymentsPageRequested),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showPageLoadingDistpatcher);
                const requestToServer = this.paymentsService.findPayments(payload.page);
                const lastQuery = of(payload.page);
                return forkJoin(requestToServer, lastQuery);
            }),
            map(response => {
                const result: QueryResultsModel = response[0];
                const lastQuery: QueryParamsModel = response[1];
                // console.log(result);
                return new PaymentsPageLoaded({
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
    deletePayments$ = this.actions$
        .pipe(
            ofType<ManyPaymentsDeleted>(PaymentActionTypes.ManyPaymentsDeleted),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.paymentsService.deletePayments(payload.ids);
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
    updatePayment$ = this.actions$
        .pipe(
            ofType<PaymentUpdated>(PaymentActionTypes.PaymentUpdated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.paymentsService.updatePayment(payload.results);
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    createPayment$ = this.actions$
        .pipe(
            ofType<PaymentOnServerCreated>(PaymentActionTypes.PaymentOnServerCreated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showLoadingDistpatcher);
                return this.paymentsService.createPayment(payload.payment).pipe(
                    tap(res => {
                        this.store.dispatch(new PaymentCreated({ payment: res }));
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

    constructor(private actions$: Actions, private paymentsService: PaymentService, private store: Store<AppState>) { }
}
