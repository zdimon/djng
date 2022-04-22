/* ----- {{copyright}} --- */
// NGRX
import { createFeatureSelector } from '@ngrx/store';
import { EntityState, EntityAdapter, createEntityAdapter, Update } from '@ngrx/entity';
// Actions
import { %upname%Actions, %upname%ActionTypes } from '../_actions/{{fileprefix}}.actions';
// CRUD
import { QueryParamsModel } from '@core/_base/crud';
// Models
import { %upname%Model } from '../_models/{{fileprefix}}.model';

export interface {{upname}}sState extends EntityState<{{upname}}Model> {
    listLoading: boolean;
    actionsloading: boolean;
    totalCount: number;
    lastQuery: QueryParamsModel;
    lastCreated{{upname}}Id: number;
    showInitWaitingMessage: boolean;
}

export const adapter: EntityAdapter<{{upname}}Model> = createEntityAdapter<{{upname}}Model>();

export const initial{{upname}}sState: {{upname}}sState = adapter.getInitialState({
    listLoading: false,
    actionsloading: false,
    totalCount: 0,
    lastQuery:  new QueryParamsModel({}),
    lastCreated{{upname}}Id: undefined,
    showInitWaitingMessage: true
});

export function {{camelName}}Reducer(state = initial{{upname}}sState, action: {{upname}}Actions): {{upname}}sState {
    switch  (action.type) {
        case {{upname}}ActionTypes.{{upname}}sPageToggleLoading: return {
            ...state, listLoading: action.payload.isLoading, lastCreated{{upname}}Id: undefined
        };
        case {{upname}}ActionTypes.{{upname}}sActionToggleLoading: return {
            ...state, actionsloading: action.payload.isLoading
        };
        case {{upname}}ActionTypes.{{upname}}OnServerCreated: return {
            ...state
        };
        case {{upname}}ActionTypes.{{upname}}Created: return adapter.addOne(action.payload.{{camelName}}, {
             ...state, lastCreatedVideoId: action.payload.{{camelName}}.id
        });
        case {{upname}}ActionTypes.{{upname}}Updated: return adapter.updateOne(action.payload.partial{{upname}}, state);
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
        case {{upname}}ActionTypes.One{{upname}}Deleted: return adapter.removeOne(action.payload.id, state);
        case {{upname}}ActionTypes.Many{{upname}}sDeleted: return adapter.removeMany(action.payload.ids, state);
        case {{upname}}ActionTypes.{{upname}}sPageCancelled: return {
            ...state, listLoading: false, lastQuery: new QueryParamsModel({})
        };
        case {{upname}}ActionTypes.{{upname}}sPageLoaded:
            return adapter.addMany(action.payload.results, {
                ...initial{{upname}}sState,
                totalCount: action.payload.totalCount,
                listLoading: false,
                lastQuery: action.payload.page,
                showInitWaitingMessage: false
            });
        default: return state;
    }
}

export const get{{upname}}State = createFeatureSelector<{{upname}}Model>('{{camelName}}');

export const {
    selectAll,
    selectEntities,
    selectIds,
    selectTotal
} = adapter.getSelectors();
