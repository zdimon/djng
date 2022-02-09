/* -----  --- */
// NGRX
import { createFeatureSelector } from '@ngrx/store';
import { EntityState, EntityAdapter, createEntityAdapter, Update } from '@ngrx/entity';
// Actions
import { PaymentActions, PaymentActionTypes } from '../_actions/payment.actions';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { PaymentModel } from '../_models/payment.model';

export interface PaymentsState extends EntityState<PaymentModel> {
    listLoading: boolean;
    actionsloading: boolean;
    totalCount: number;
    lastQuery: QueryParamsModel;
    lastCreatedPaymentId: number;
    showInitWaitingMessage: boolean;
}

export const adapter: EntityAdapter<PaymentModel> = createEntityAdapter<PaymentModel>();

export const initialPaymentsState: PaymentsState = adapter.getInitialState({
    listLoading: false,
    actionsloading: false,
    totalCount: 0,
    lastQuery:  new QueryParamsModel({}),
    lastCreatedPaymentId: undefined,
    showInitWaitingMessage: true
});

export function paymentReducer(state = initialPaymentsState, action: PaymentActions): PaymentsState {
    switch  (action.type) {
        case PaymentActionTypes.PaymentsPageToggleLoading: return {
            ...state, listLoading: action.payload.isLoading, lastCreatedPaymentId: undefined
        };
        case PaymentActionTypes.PaymentsActionToggleLoading: return {
            ...state, actionsloading: action.payload.isLoading
        };
        case PaymentActionTypes.PaymentOnServerCreated: return {
            ...state
        };
        case PaymentActionTypes.PaymentCreated: return adapter.addOne(action.payload.payment, {
             ...state, lastCreatedVideoId: action.payload.payment.id
        });
        case PaymentActionTypes.PaymentUpdated: return adapter.updateOne(action.payload.partialPayment, state);
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
        case PaymentActionTypes.OnePaymentDeleted: return adapter.removeOne(action.payload.id, state);
        case PaymentActionTypes.ManyPaymentsDeleted: return adapter.removeMany(action.payload.ids, state);
        case PaymentActionTypes.PaymentsPageCancelled: return {
            ...state, listLoading: false, lastQuery: new QueryParamsModel({})
        };
        case PaymentActionTypes.PaymentsPageLoaded:
            return adapter.addMany(action.payload.results, {
                ...initialPaymentsState,
                totalCount: action.payload.totalCount,
                listLoading: false,
                lastQuery: action.payload.page,
                showInitWaitingMessage: false
            });
        default: return state;
    }
}

export const getPaymentState = createFeatureSelector<PaymentModel>('payment');

export const {
    selectAll,
    selectEntities,
    selectIds,
    selectTotal
} = adapter.getSelectors();
