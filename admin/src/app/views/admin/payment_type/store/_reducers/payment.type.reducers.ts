/* -----  --- */
// NGRX
import { createFeatureSelector } from '@ngrx/store';
import { EntityState, EntityAdapter, createEntityAdapter, Update } from '@ngrx/entity';
// Actions
import { PaymentTypeActions, PaymentTypeActionTypes } from '../_actions/payment.type.actions';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { PaymentTypeModel } from '../_models/payment.type.model';

export interface PaymentTypesState extends EntityState<PaymentTypeModel> {
    listLoading: boolean;
    actionsloading: boolean;
    totalCount: number;
    lastQuery: QueryParamsModel;
    lastCreatedPaymentTypeId: number;
    showInitWaitingMessage: boolean;
}

export const adapter: EntityAdapter<PaymentTypeModel> = createEntityAdapter<PaymentTypeModel>();

export const initialPaymentTypesState: PaymentTypesState = adapter.getInitialState({
    listLoading: false,
    actionsloading: false,
    totalCount: 0,
    lastQuery:  new QueryParamsModel({}),
    lastCreatedPaymentTypeId: undefined,
    showInitWaitingMessage: true
});

export function paymentTypeReducer(state = initialPaymentTypesState, action: PaymentTypeActions): PaymentTypesState {
    switch  (action.type) {
        case PaymentTypeActionTypes.PaymentTypesPageToggleLoading: return {
            ...state, listLoading: action.payload.isLoading, lastCreatedPaymentTypeId: undefined
        };
        case PaymentTypeActionTypes.PaymentTypesActionToggleLoading: return {
            ...state, actionsloading: action.payload.isLoading
        };
        case PaymentTypeActionTypes.PaymentTypeOnServerCreated: return {
            ...state
        };
        case PaymentTypeActionTypes.PaymentTypeCreated: return adapter.addOne(action.payload.paymentType, {
             ...state, lastCreatedVideoId: action.payload.paymentType.id
        });
        case PaymentTypeActionTypes.PaymentTypeUpdated: return adapter.updateOne(action.payload.partialPaymentType, state);
        // case VideoActionTypes.VideosStatusUpdated: {
        //     const _partialVideos: Update<VideoModel>[] = [];
        //     for (let i = 0; i < action.payload.videos.length; i++) {
        //         _partialVideos.push({
        //             id: action.payload.results[i].id,
        //             changes: {
        //                status: action.payload.status
        //             }
        //         });
        //     }
        //     return adapter.updateMany(_partialVideos, state);
        // }
        case PaymentTypeActionTypes.OnePaymentTypeDeleted: return adapter.removeOne(action.payload.id, state);
        case PaymentTypeActionTypes.ManyPaymentTypesDeleted: return adapter.removeMany(action.payload.ids, state);
        case PaymentTypeActionTypes.PaymentTypesPageCancelled: return {
            ...state, listLoading: false, lastQuery: new QueryParamsModel({})
        };
        case PaymentTypeActionTypes.PaymentTypesPageLoaded:
            return adapter.addMany(action.payload.results, {
                ...initialPaymentTypesState,
                totalCount: action.payload.totalCount,
                listLoading: false,
                lastQuery: action.payload.page,
                showInitWaitingMessage: false
            });
        default: return state;
    }
}

export const getPaymentTypeState = createFeatureSelector<PaymentTypeModel>('paymentType');

export const {
    selectAll,
    selectEntities,
    selectIds,
    selectTotal
} = adapter.getSelectors();
