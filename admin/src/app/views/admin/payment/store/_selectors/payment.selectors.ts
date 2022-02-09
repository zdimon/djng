/* -----  --- */
// NGRX
import { createFeatureSelector, createSelector } from '@ngrx/store';
// Lodash
import { each } from 'lodash';
// CRUD
import { QueryResultsModel, HttpExtenstionsModel } from '@core/_base/crud';
// State
import { PaymentsState } from '../_reducers/payment.reducers';
import { PaymentModel } from '../_models/payment.model';

export const selectPaymentsState = createFeatureSelector<PaymentsState>('payment');

export const selectPaymentById = (paymentId: number) => createSelector(
    selectPaymentsState,
    paymentsState => paymentsState.entities[paymentId]
);

export const selectPaymentsPageLoading = createSelector(
    selectPaymentsState,
    paymentsState => paymentsState.listLoading
);

export const selectPaymentsActionLoading = createSelector(
    selectPaymentsState,
    customersState => customersState.actionsloading
);

export const selectPaymentsPageLastQuery = createSelector(
    selectPaymentsState,
    paymentsState => paymentsState.lastQuery
);

export const selectLastCreatedPaymentId = createSelector(
    selectPaymentsState,
    paymentsState => paymentsState.lastCreatedPaymentId
);

export const selectPaymentsInitWaitingMessage = createSelector(
    selectPaymentsState,
    paymentsState => paymentsState.showInitWaitingMessage
);

export const selectPaymentsInStore = createSelector(
    selectPaymentsState,
    paymentState => {
        const items: PaymentModel[] = [];
        each(paymentState.entities, element => {
            items.push(element);
        });
        const httpExtension = new HttpExtenstionsModel();
        const result: PaymentModel[] = httpExtension.sortArray(items, paymentState.lastQuery.sortField, paymentState.lastQuery.sortOrder);
        return new QueryResultsModel(result, paymentState.totalCount, '');
    }
);

export const selectHasPaymentsInStore = createSelector(
    selectPaymentsInStore,
    queryResult => {
        if (!queryResult.totalCount) {
            return false;
        }

        return true;
    }
);
