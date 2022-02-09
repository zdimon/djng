/* -----  --- */
// NGRX
import { Action } from '@ngrx/store';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { PaymentModel } from '../_models/payment.model';
import { Update } from '@ngrx/entity';

export enum PaymentActionTypes {
    PaymentOnServerCreated = '[Edit Payment Component] Payment On Server Created',
    PaymentCreated = '[Edit Payment Component] Payment Created',
    PaymentUpdated = '[Edit Payment Component] Payment Updated',
    PaymentsStatusUpdated = '[Payment List Page] Payment Status Updated',
    OnePaymentDeleted = '[Payment List Page] One Video Deleted',
    ManyPaymentsDeleted = '[Payment List Page] Many Selected Payments Deleted',
    PaymentsPageRequested = '[Payment List Page] Payments Page Requested',
    PaymentsPageLoaded = '[Payment API] Payments Page Loaded',
    PaymentsPageCancelled = '[Payment API] Payments Page Cancelled',
    PaymentsPageToggleLoading = '[Payment] Payments Page Toggle Loading',
    PaymentsActionToggleLoading = '[Payment] Payments Action Toggle Loading'
}

export class PaymentOnServerCreated implements Action {
    readonly type = PaymentActionTypes.PaymentOnServerCreated;
    constructor(public payload: { payment: PaymentModel }) { }
}

export class PaymentCreated implements Action {
    readonly type = PaymentActionTypes.PaymentCreated;
    constructor(public payload: { payment: PaymentModel }) { }
}

export class PaymentUpdated implements Action {
    readonly type = PaymentActionTypes.PaymentUpdated;
    constructor(public payload: {
        partialPayment: Update<PaymentModel>, // For State update
        results: PaymentModel // For Server update (through service)
    }) { }
}

export class PaymentsStatusUpdated implements Action {
    readonly type = PaymentActionTypes.PaymentsStatusUpdated;
    constructor(public payload: {
        results: PaymentModel[],
        status: number
    }) { }
}

export class OnePaymentDeleted implements Action {
    readonly type = PaymentActionTypes.OnePaymentDeleted;
    constructor(public payload: { id: number }) {}
}

export class ManyPaymentsDeleted implements Action {
    readonly type = PaymentActionTypes.ManyPaymentsDeleted;
    constructor(public payload: { ids: number[] }) {}
}

export class PaymentsPageRequested implements Action {
    readonly type = PaymentActionTypes.PaymentsPageRequested;
    constructor(public payload: { page: QueryParamsModel }) { }
}

export class PaymentsPageLoaded implements Action {
    readonly type = PaymentActionTypes.PaymentsPageLoaded;
    constructor(public payload: { results: PaymentModel[], totalCount: number, page: QueryParamsModel }) { }
}

export class PaymentsPageCancelled implements Action {
    readonly type = PaymentActionTypes.PaymentsPageCancelled;
}

export class PaymentsPageToggleLoading implements Action {
    readonly type = PaymentActionTypes.PaymentsPageToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export class PaymentsActionToggleLoading implements Action {
    readonly type = PaymentActionTypes.PaymentsActionToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export type PaymentActions = PaymentOnServerCreated
| PaymentCreated
| PaymentUpdated
| PaymentsStatusUpdated
| OnePaymentDeleted
| ManyPaymentsDeleted
| PaymentsPageRequested
| PaymentsPageLoaded
| PaymentsPageCancelled
| PaymentsPageToggleLoading
| PaymentsActionToggleLoading;
