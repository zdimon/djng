/* -----  --- */
// NGRX
import { createFeatureSelector, createSelector } from '@ngrx/store';
// Lodash
import { each } from 'lodash';
// CRUD
import { QueryResultsModel, HttpExtenstionsModel } from '@core/_base/crud';
// State
import { PaymentTypesState } from '../_reducers/payment.type.reducers';
import { PaymentTypeModel } from '../_models/payment.type.model';

export const selectPaymentTypesState = createFeatureSelector<PaymentTypesState>('paymentType');

export const selectPaymentTypeById = (paymentTypeId: number) => createSelector(
    selectPaymentTypesState,
    paymentTypesState => paymentTypesState.entities[paymentTypeId]
);

export const selectPaymentTypesPageLoading = createSelector(
    selectPaymentTypesState,
    paymentTypesState => paymentTypesState.listLoading
);

export const selectPaymentTypesActionLoading = createSelector(
    selectPaymentTypesState,
    customersState => customersState.actionsloading
);

export const selectPaymentTypesPageLastQuery = createSelector(
    selectPaymentTypesState,
    paymentTypesState => paymentTypesState.lastQuery
);

export const selectLastCreatedPaymentTypeId = createSelector(
    selectPaymentTypesState,
    paymentTypesState => paymentTypesState.lastCreatedPaymentTypeId
);

export const selectPaymentTypesInitWaitingMessage = createSelector(
    selectPaymentTypesState,
    paymentTypesState => paymentTypesState.showInitWaitingMessage
);

export const selectPaymentTypesInStore = createSelector(
    selectPaymentTypesState,
    paymentTypeState => {
        const items: PaymentTypeModel[] = [];
        each(paymentTypeState.entities, element => {
            items.push(element);
        });
        const httpExtension = new HttpExtenstionsModel();
        const result: PaymentTypeModel[] = httpExtension.sortArray(items, paymentTypeState.lastQuery.sortField, paymentTypeState.lastQuery.sortOrder);
        return new QueryResultsModel(result, paymentTypeState.totalCount, '');
    }
);

export const selectHasPaymentTypesInStore = createSelector(
    selectPaymentTypesInStore,
    queryResult => {
        if (!queryResult.totalCount) {
            return false;
        }

        return true;
    }
);
