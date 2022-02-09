/* ----- Autogenerated by Django! Author: Zharikov Dimitry zdimon77@gmail.com --- */
// NGRX
import { createFeatureSelector } from '@ngrx/store';
import { EntityState, EntityAdapter, createEntityAdapter, Update } from '@ngrx/entity';
// Actions
import { LogActions, LogActionTypes } from '../_actions/log.actions';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { LogModel } from '../_models/log.model';

export interface LogsState extends EntityState<LogModel> {
    listLoading: boolean;
    actionsloading: boolean;
    totalCount: number;
    lastQuery: QueryParamsModel;
    lastCreatedLogId: number;
    showInitWaitingMessage: boolean;
}

export const adapter: EntityAdapter<LogModel> = createEntityAdapter<LogModel>();

export const initialLogsState: LogsState = adapter.getInitialState({
    listLoading: false,
    actionsloading: false,
    totalCount: 0,
    lastQuery:  new QueryParamsModel({}),
    lastCreatedLogId: undefined,
    showInitWaitingMessage: true
});

export function logReducer(state = initialLogsState, action: LogActions): LogsState {
    switch  (action.type) {
        case LogActionTypes.LogsPageToggleLoading: return {
            ...state, listLoading: action.payload.isLoading, lastCreatedLogId: undefined
        };
        case LogActionTypes.LogsActionToggleLoading: return {
            ...state, actionsloading: action.payload.isLoading
        };
        case LogActionTypes.LogOnServerCreated: return {
            ...state
        };
        case LogActionTypes.LogCreated: return adapter.addOne(action.payload.log, {
             ...state, lastCreatedVideoId: action.payload.log.id
        });
        case LogActionTypes.LogUpdated: return adapter.updateOne(action.payload.partialLog, state);
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
        case LogActionTypes.OneLogDeleted: return adapter.removeOne(action.payload.id, state);
        case LogActionTypes.ManyLogsDeleted: return adapter.removeMany(action.payload.ids, state);
        case LogActionTypes.LogsPageCancelled: return {
            ...state, listLoading: false, lastQuery: new QueryParamsModel({})
        };
        case LogActionTypes.LogsPageLoaded:
            return adapter.addMany(action.payload.results, {
                ...initialLogsState,
                totalCount: action.payload.totalCount,
                listLoading: false,
                lastQuery: action.payload.page,
                showInitWaitingMessage: false
            });
        default: return state;
    }
}

export const getLogState = createFeatureSelector<LogModel>('log');

export const {
    selectAll,
    selectEntities,
    selectIds,
    selectTotal
} = adapter.getSelectors();
