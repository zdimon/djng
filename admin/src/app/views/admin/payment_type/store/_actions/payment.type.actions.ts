/* -----  --- */
// NGRX
import { Action } from '@ngrx/store';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { PaymentTypeModel } from '../_models/payment.type.model';
import { Update } from '@ngrx/entity';

export enum PaymentTypeActionTypes {
    PaymentTypeOnServerCreated = '[Edit PaymentType Component] PaymentType On Server Created',
    PaymentTypeCreated = '[Edit PaymentType Component] PaymentType Created',
    PaymentTypeUpdated = '[Edit PaymentType Component] PaymentType Updated',
    PaymentTypesStatusUpdated = '[PaymentType List Page] PaymentType Status Updated',
    OnePaymentTypeDeleted = '[PaymentType List Page] One Video Deleted',
    ManyPaymentTypesDeleted = '[PaymentType List Page] Many Selected PaymentTypes Deleted',
    PaymentTypesPageRequested = '[PaymentType List Page] PaymentTypes Page Requested',
    PaymentTypesPageLoaded = '[PaymentType API] PaymentTypes Page Loaded',
    PaymentTypesPageCancelled = '[PaymentType API] PaymentTypes Page Cancelled',
    PaymentTypesPageToggleLoading = '[PaymentType] PaymentTypes Page Toggle Loading',
    PaymentTypesActionToggleLoading = '[PaymentType] PaymentTypes Action Toggle Loading'
}

export class PaymentTypeOnServerCreated implements Action {
    readonly type = PaymentTypeActionTypes.PaymentTypeOnServerCreated;
    constructor(public payload: { paymentType: PaymentTypeModel }) { }
}

export class PaymentTypeCreated implements Action {
    readonly type = PaymentTypeActionTypes.PaymentTypeCreated;
    constructor(public payload: { paymentType: PaymentTypeModel }) { }
}

export class PaymentTypeUpdated implements Action {
    readonly type = PaymentTypeActionTypes.PaymentTypeUpdated;
    constructor(public payload: {
        partialPaymentType: Update<PaymentTypeModel>, // For State update
        results: PaymentTypeModel // For Server update (through service)
    }) { }
}

export class PaymentTypesStatusUpdated implements Action {
    readonly type = PaymentTypeActionTypes.PaymentTypesStatusUpdated;
    constructor(public payload: {
        results: PaymentTypeModel[],
        status: number
    }) { }
}

export class OnePaymentTypeDeleted implements Action {
    readonly type = PaymentTypeActionTypes.OnePaymentTypeDeleted;
    constructor(public payload: { id: number }) {}
}

export class ManyPaymentTypesDeleted implements Action {
    readonly type = PaymentTypeActionTypes.ManyPaymentTypesDeleted;
    constructor(public payload: { ids: number[] }) {}
}

export class PaymentTypesPageRequested implements Action {
    readonly type = PaymentTypeActionTypes.PaymentTypesPageRequested;
    constructor(public payload: { page: QueryParamsModel }) { }
}

export class PaymentTypesPageLoaded implements Action {
    readonly type = PaymentTypeActionTypes.PaymentTypesPageLoaded;
    constructor(public payload: { results: PaymentTypeModel[], totalCount: number, page: QueryParamsModel }) { }
}

export class PaymentTypesPageCancelled implements Action {
    readonly type = PaymentTypeActionTypes.PaymentTypesPageCancelled;
}

export class PaymentTypesPageToggleLoading implements Action {
    readonly type = PaymentTypeActionTypes.PaymentTypesPageToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export class PaymentTypesActionToggleLoading implements Action {
    readonly type = PaymentTypeActionTypes.PaymentTypesActionToggleLoading;
    constructor(public payload: { isLoading: boolean }) { }
}

export type PaymentTypeActions = PaymentTypeOnServerCreated
| PaymentTypeCreated
| PaymentTypeUpdated
| PaymentTypesStatusUpdated
| OnePaymentTypeDeleted
| ManyPaymentTypesDeleted
| PaymentTypesPageRequested
| PaymentTypesPageLoaded
| PaymentTypesPageCancelled
| PaymentTypesPageToggleLoading
| PaymentTypesActionToggleLoading;
