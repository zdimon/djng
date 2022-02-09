/* ----- Autogenerated by Django! Author: Zharikov Dimitry zdimon77@gmail.com --- */
// NGRX
import { createFeatureSelector } from '@ngrx/store';
import { EntityState, EntityAdapter, createEntityAdapter, Update } from '@ngrx/entity';
// Actions
import { PlanActions, PlanActionTypes } from '../_actions/plan.actions';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { PlanModel } from '../_models/plan.model';

export interface PlansState extends EntityState<PlanModel> {
    listLoading: boolean;
    actionsloading: boolean;
    totalCount: number;
    lastQuery: QueryParamsModel;
    lastCreatedPlanId: number;
    showInitWaitingMessage: boolean;
}

export const adapter: EntityAdapter<PlanModel> = createEntityAdapter<PlanModel>();

export const initialPlansState: PlansState = adapter.getInitialState({
    listLoading: false,
    actionsloading: false,
    totalCount: 0,
    lastQuery:  new QueryParamsModel({}),
    lastCreatedPlanId: undefined,
    showInitWaitingMessage: true
});

export function planReducer(state = initialPlansState, action: PlanActions): PlansState {
    switch  (action.type) {
        case PlanActionTypes.PlansPageToggleLoading: return {
            ...state, listLoading: action.payload.isLoading, lastCreatedPlanId: undefined
        };
        case PlanActionTypes.PlansActionToggleLoading: return {
            ...state, actionsloading: action.payload.isLoading
        };
        case PlanActionTypes.PlanOnServerCreated: return {
            ...state
        };
        case PlanActionTypes.PlanCreated: return adapter.addOne(action.payload.plan, {
             ...state, lastCreatedVideoId: action.payload.plan.id
        });
        case PlanActionTypes.PlanUpdated: return adapter.updateOne(action.payload.partialPlan, state);
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
        case PlanActionTypes.OnePlanDeleted: return adapter.removeOne(action.payload.id, state);
        case PlanActionTypes.ManyPlansDeleted: return adapter.removeMany(action.payload.ids, state);
        case PlanActionTypes.PlansPageCancelled: return {
            ...state, listLoading: false, lastQuery: new QueryParamsModel({})
        };
        case PlanActionTypes.PlansPageLoaded:
            return adapter.addMany(action.payload.results, {
                ...initialPlansState,
                totalCount: action.payload.totalCount,
                listLoading: false,
                lastQuery: action.payload.page,
                showInitWaitingMessage: false
            });
        default: return state;
    }
}

export const getPlanState = createFeatureSelector<PlanModel>('plan');

export const {
    selectAll,
    selectEntities,
    selectIds,
    selectTotal
} = adapter.getSelectors();