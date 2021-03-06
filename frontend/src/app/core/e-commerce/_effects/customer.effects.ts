// Angular
import { Injectable } from '@angular/core';
// NGRX
import { Actions, Effect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { forkJoin } from 'rxjs';
import { of } from 'rxjs';
// RxJS
import { delay, map, mergeMap, tap } from 'rxjs/operators';
// State
import { AppState } from '../../../core/reducers';
// CRUD
import { QueryResultsModel } from '../../_base/crud';
// Actions
import {
    CustomerActionToggleLoading,
    CustomerActionTypes,
    CustomerCreated,
    CustomerOnServerCreated,
    CustomersPageLoaded,
    CustomersPageRequested,
    CustomersPageToggleLoading,
    CustomersStatusUpdated,
    CustomerUpdated,
    ManyCustomersDeleted,
    OneCustomerDeleted,
} from '../_actions/customer.actions';
// Services
import { CustomersService } from '../_services/';
import { QueryParamsModel } from './../../_base/crud/models/query-models/query-params.model';

@Injectable()
export class CustomerEffects {
    showPageLoadingDistpatcher = new CustomersPageToggleLoading({ isLoading: true });
    showActionLoadingDistpatcher = new CustomerActionToggleLoading({ isLoading: true });
    hideActionLoadingDistpatcher = new CustomerActionToggleLoading({ isLoading: false });

    @Effect()
    loadCustomersPage$ = this.actions$.pipe(
        ofType<CustomersPageRequested>(CustomerActionTypes.CustomersPageRequested),
        mergeMap(( { payload } ) => {
            this.store.dispatch(this.showPageLoadingDistpatcher);
            const requestToServer = this.customersService.findCustomers(payload.page);
            const lastQuery = of(payload.page);
            return forkJoin(requestToServer, lastQuery);
        }),
        map(response => {
            const result: QueryResultsModel = response[0];
            const lastQuery: QueryParamsModel = response[1];
            const pageLoadedDispatch = new CustomersPageLoaded({
                customers: result.items,
                totalCount: result.totalCount,
                page: lastQuery,
            });
            return pageLoadedDispatch;
        }),
    );

    @Effect()
    deleteCustomer$ = this.actions$
        .pipe(
            ofType<OneCustomerDeleted>(CustomerActionTypes.OneCustomerDeleted),
            mergeMap(( { payload } ) => {
                    this.store.dispatch(this.showActionLoadingDistpatcher);
                    return this.customersService.deleteCustomer(payload.id);
                },
            ),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    deleteCustomers$ = this.actions$
        .pipe(
            ofType<ManyCustomersDeleted>(CustomerActionTypes.ManyCustomersDeleted),
            mergeMap(( { payload } ) => {
                    this.store.dispatch(this.showActionLoadingDistpatcher);
                    return this.customersService.deleteCustomers(payload.ids);
                },
            ),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    updateCustomer$ = this.actions$
        .pipe(
            ofType<CustomerUpdated>(CustomerActionTypes.CustomerUpdated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showActionLoadingDistpatcher);
                return this.customersService.updateCustomer(payload.customer);
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    updateCustomersStatus$ = this.actions$
        .pipe(
            ofType<CustomersStatusUpdated>(CustomerActionTypes.CustomersStatusUpdated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showActionLoadingDistpatcher);
                return this.customersService.updateStatusForCustomer(payload.customers, payload.status);
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    @Effect()
    createCustomer$ = this.actions$
        .pipe(
            ofType<CustomerOnServerCreated>(CustomerActionTypes.CustomerOnServerCreated),
            mergeMap(( { payload } ) => {
                this.store.dispatch(this.showActionLoadingDistpatcher);
                return this.customersService.createCustomer(payload.customer).pipe(
                    tap(res => {
                        this.store.dispatch(new CustomerCreated({ customer: res }));
                    }),
                );
            }),
            map(() => {
                return this.hideActionLoadingDistpatcher;
            }),
        );

    constructor(private actions$: Actions, private customersService: CustomersService, private store: Store<AppState>) { }
}
